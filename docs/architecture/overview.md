# 아키텍처 개요

> 결정 근거: [ADR 목록](adr/README.md). 이 문서와 코드가 다르면 코드를 고치거나 ADR을 새로 씁니다.

## 원칙: Clean Architecture

```
          ┌──────────────────────────── 앱 셸 (DI 조립, 플랫폼 진입점) ────────────────────────────┐
          │  androidApp (Compose · Glance · WorkManager · PROCESS_TEXT)                              │
          │  iosApp     (SwiftUI · WidgetKit · Share Extension)                                       │
          └───────────────┬───────────────────────────────────────────────┬──────────────────────────┘
                          │ 사용                                          │ 조립(DI)
              ┌───────────▼───────────┐                       ┌───────────▼───────────┐
              │ :shared:presentation  │                       │     :shared:data      │
              │ ViewModel · UiState   │                       │ Repository 구현        │
              └───────────┬───────────┘                       │ 레시피 해석기 · 로컬 DB │
                          │ 의존                               │ (서버 API: 문서 대기)   │
                          ▼                                   └───────────┬───────────┘
              ┌───────────────────────────────────────────────────────────▼───────────┐
              │                         :shared:domain                                 │
              │  Entity · Value Object · Repository/Port 인터페이스 · UseCase · 정책     │
              │  (순수 Kotlin. Ktor·SQLDelight·Android·iOS 의존 금지)                     │
              └────────────────────────────────────────────────────────────────────────┘
```

의존 방향은 **바깥 → 안쪽(domain)** 하나뿐입니다.

| 모듈 | 의존 가능 | 의존 금지 |
|---|---|---|
| `:shared:domain` | Kotlin 표준 라이브러리, kotlinx-coroutines-core, kotlinx-datetime(`kotlin.time`) | Ktor, SQLDelight, Ksoup, serialization 어노테이션, Koin, 플랫폼 API, 다른 shared 모듈 |
| `:shared:data` | domain, Ktor, Ksoup, kotlinx.serialization, SQLDelight, 암호화 라이브러리 | presentation, 앱 모듈 |
| `:shared:presentation` | domain, androidx.lifecycle ViewModel(KMP) | data (구현 클래스 직접 사용 금지), Ktor, SQLDelight |
| `:shared:testing` | domain (Fake·테스트 데이터 빌더) | data 구현, 앱 모듈 |
| `:shared:umbrella` | 모든 shared 모듈 (iOS 정적 프레임워크 export + Koin 조립) | — |
| `androidApp` | presentation, domain, data(DI 조립용으로만) | data 내부 클래스를 화면에서 직접 사용 |
| `iosApp` | `Shared` 프레임워크 | — |

경계 위반은 Gradle 의존성 선언으로 1차 차단하고, `:shared:architecture-test`(Konsist)로 2차 검증합니다.

## 모듈과 패키지

패키지 루트(임시, Q-05): `com.taekbugi`

```
build-logic/                      Gradle convention plugin (kmp-library, android-app, detekt, kover)
gradle/libs.versions.toml         버전 카탈로그 (버전은 여기에만)
shared/
  domain/src/commonMain/kotlin/com/taekbugi/domain/
    model/        Parcel, TrackEvent, DeliveryStatus, Carrier, CarrierCode, TrackingNumber(value class) …
    carrier/      CarrierDetector(자릿수·체크섬 후보 판별), TrackingNumberExtractor(텍스트에서 추출)
    tracking/     RefreshPolicy(상태별 조회 주기), TrackingResult
    alert/        DelayAlertPolicy(조회 지연 판단)
    archive/      ArchivePolicy(완료 택배 정리)
    repository/   ParcelRepository, PendingRegistrationQueue, TrackingSource, SettingsRepository … (포트)
    usecase/      RegisterParcelUseCase, RefreshParcelUseCase, DeleteParcelUseCase …
    error/        도메인 오류 sealed 타입
  data/src/commonMain/kotlin/com/taekbugi/data/
    carrier/recipe/   레시피 모델(@Serializable) · 서명 검증 · 도메인 허용 목록 · 해석기
    carrier/          TrackingSource 구현 (레시피 실행 → 정규화)
    local/            SQLDelight 스키마·DAO, 임시 보관 큐 저장
    repository/       포트 구현
    mapper/           DTO/Row ↔ domain
    remote/server/    ⛔ 백엔드 API — docs/api/specs/ 에 문서가 오기 전까지 생성 금지 (훅으로 차단)
  data/src/commonMain/resources/recipes/   번들 레시피(JSON) — 서버 배포 전 기본값
  data/src/commonTest/resources/golden/    택배사 응답 골든 샘플(개인정보 마스킹)
  presentation/src/commonMain/kotlin/com/taekbugi/presentation/
    <feature>/    XxxViewModel, XxxUiState, XxxAction
  testing/src/commonMain/kotlin/com/taekbugi/testing/
    fake/         FakeParcelRepository, FakeTrackingSource, FixedClock …
    fixture/      aParcel(), aTrackEvent() 등 테스트 데이터 빌더
  umbrella/       iOS용 Shared.framework (isStatic = true), KoinIos 조립
  architecture-test/   Konsist 경계 테스트 (JVM)
androidApp/src/main/kotlin/com/taekbugi/android/
  ui/<feature>/   Compose 화면(Stateless) + Route(ViewModel 연결)
  ui/theme/       TaekbugiTheme (docs/design/tokens.md 값)
  widget/         Glance 위젯
  work/           WorkManager 조회 스케줄러
  processtext/    PROCESS_TEXT 진입 액티비티 (등록 하단 시트)
  di/             Koin 모듈 조립
androidApp/src/debug/   QA용 디버그 도구 (위젯 고정 요청, 즉시 조회 실행, 클립보드 주입)
iosApp/
  iosApp/         SwiftUI 앱
  TaekbugiWidget/ WidgetKit 확장
  ShareExtension/ 공유 확장
  iosAppTests/ · iosAppUITests/
qa/maestro/{android,ios}/   QA 에이전트가 쓰는 Maestro 흐름
```

## 데이터 흐름

```
[등록]  선택 텍스트 ─▶ TrackingNumberExtractor ─▶ CarrierDetector(후보)
         ├ 로그인 전  ─▶ PendingRegistrationQueue (App Group / 로컬 DB) ─▶ 로그인 후 자동 등록
         └ 로그인 후  ─▶ RegisterParcelUseCase ─▶ ParcelRepository(로컬 DB)

[조회]  Scheduler(WorkManager / BGAppRefresh) ─▶ RefreshParcelUseCase
         ─▶ TrackingSource(레시피 해석기 → 택배사 사이트 직접 요청, 허용 도메인만)
         ─▶ 정규화(DeliveryStatus + raw_code, 위치는 시·구까지, 개인정보 제거)
         ─▶ 로컬 DB 저장 ─▶ 위젯 갱신 ─▶ DelayAlertPolicy ─▶ 로컬 알림

[동기화] ⛔ API 문서 대기 — 내 택배 동기화, tombstone, 지표 보고, 레시피 수신, 로그인/계정
```

- 택배사 조회는 **사용자 기기에서만** 합니다.
- 서버로 보낼 데이터의 모양은 API 문서가 오면 정합니다. 그 전에는 서버 전송 코드를 만들지 않습니다.

## 상태 모델 (초안)

- `DeliveryStatus`: `NotPickedUp`(집하 전) · `InTransit`(이동 중) · `OutForDelivery`(배송 출발) · `Delivered`(배송 완료)
- 조회 실패·지연 표시는 G-03 결정 후 모델링합니다. 결정 전에는 만들지 않습니다.
- 택배사 원본 코드는 `rawCode`로 함께 보관합니다.

## 플랫폼 경계

- `expect/actual`은 최소화합니다. 플랫폼 기능은 **domain의 포트 인터페이스 + 앱 셸의 구현 + DI 주입**으로 연결합니다 (예: `LocalNotifier`, `WidgetRefresher`, `SecureKeyStore`).
- iOS는 `:shared:umbrella`를 정적 프레임워크로 빌드해 앱·위젯·공유 확장에 링크합니다. 확장은 메모리 제한이 있으므로 확장에서 쓰는 진입점은 가볍게 유지합니다.
- 로컬 DB 파일과 임시 큐는 iOS App Group 컨테이너에 둡니다 (앱·위젯·공유 확장이 함께 읽음).
