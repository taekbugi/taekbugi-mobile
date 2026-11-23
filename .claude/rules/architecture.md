---
paths:
  - "shared/**"
  - "androidApp/**"
  - "iosApp/**"
  - "build-logic/**"
  - "**/*.gradle.kts"
---

# Clean Architecture 규칙

전체 그림: `docs/architecture/overview.md`

## 의존 방향
- `:shared:domain`은 아무 shared 모듈에도 의존하지 않습니다. 순수 Kotlin + coroutines-core + `kotlin.time`만.
  - 금지 import: `io.ktor.*`, `app.cash.sqldelight.*`, `com.fleeksoft.ksoup.*`, `kotlinx.serialization.*`, `org.koin.*`, `android.*`, `androidx.*`, `platform.*`
- `:shared:presentation`은 domain만 봅니다. data 구현 클래스를 import하지 않습니다.
- `:shared:data`는 domain의 포트를 구현합니다. presentation·앱을 모릅니다.
- 앱 셸(androidApp, iosApp)은 DI 조립에서만 data를 압니다. 화면·위젯·워커는 UseCase 또는 ViewModel만 씁니다.

## 각 레이어의 책임
- **domain**: Entity, Value Object(`@JvmInline value class TrackingNumber`), 정책(`RefreshPolicy`, `DelayAlertPolicy`, `CarrierDetector`), 포트(`interface ParcelRepository`), UseCase(`class RegisterParcelUseCase(...) { suspend operator fun invoke(...) }`), 도메인 오류(sealed).
- **data**: 포트 구현, 레시피 해석기, SQLDelight, 매퍼. 외부 타입(Row, DTO, HTML Element)은 data 밖으로 나가지 않습니다.
- **presentation**: `ViewModel` + 불변 `UiState`(data class) + 사용자 동작 함수. `StateFlow<UiState>` 하나로 노출합니다. 문자열 리소스·색은 들고 있지 않습니다 (상태만).
- **UI(앱)**: 상태를 그리고 동작을 전달합니다. 비즈니스 판단 금지.

## UseCase
- 동사로 시작하는 이름, 하나의 일. `invoke` 연산자 하나.
- 의존성은 생성자 주입. 시간은 `Clock`, 디스패처는 주입.
- 결과는 `Result`류 sealed 타입으로 돌려주고 예외를 레이어 밖으로 던지지 않습니다.

## 플랫폼 기능
- `expect/actual`보다 **domain 포트 + 플랫폼 구현 + DI**를 먼저 고려합니다 (`LocalNotifier`, `WidgetRefresher`, `SecureKeyStore`, `ClipboardReader`).
- `expect/actual`은 아주 작은 기술 유틸(예: 파일 경로)에만.

## 새 모듈·의존성
- 새 Gradle 모듈, 새 외부 라이브러리는 ADR 후 추가합니다 (`/adr`).
- 버전은 `gradle/libs.versions.toml`에만 씁니다. 공통 설정은 `build-logic/` convention plugin으로.
