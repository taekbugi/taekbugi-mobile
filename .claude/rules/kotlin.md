---
paths:
  - "**/*.kt"
  - "**/*.kts"
---

# Kotlin 규칙

## 기본
- Kotlin 2.x(K2), 공식 코딩 컨벤션, ktlint + detekt 통과가 기본입니다.
- shared 모듈은 `explicitApi()` 모드. 기본 가시성은 `internal`, 밖에 보여 줄 것만 `public`.
- `val` 우선, 읽기 전용 컬렉션(`List`, `Map`) 노출. UI 상태 컬렉션은 `kotlinx.collections.immutable`(`ImmutableList`).
- 의미 있는 원시값은 `@JvmInline value class`로 감쌉니다 (`TrackingNumber`, `CarrierCode`, `ParcelId`).
- 닫힌 경우의 수는 `sealed interface` + `when` 전수 검사. 도메인 `when`에 `else` 분기를 두지 않습니다 (새 경우를 놓치지 않게).
- `!!` 금지. 플랫폼 타입을 바로 노출하지 않습니다.
- `lateinit`은 DI·테스트 외에는 쓰지 않습니다.
- 확장 함수는 도메인 의미가 있을 때만. 유틸 남발 금지.
- 매직 넘버는 이름 있는 상수 또는 `Duration`(`30.minutes`, `6.hours`).
- 주석은 "왜"만. "무엇"은 이름으로.

## 오류 처리
- 도메인 오류는 sealed 타입(`TrackingError.Blocked`, `TrackingError.Unmapped(rawCode)` …)으로 표현합니다.
- 예외는 data 경계에서 잡아 도메인 오류로 바꿉니다. `CancellationException`은 절대 삼키지 않습니다.
  - suspend 코드에서 `runCatching` 금지 (`CancellationException`을 잡음). 필요한 예외 타입만 `catch`합니다.

## 코루틴
- 구조적 동시성. `GlobalScope`, 직접 만든 `CoroutineScope()` 남발 금지. 수명은 `viewModelScope`, WorkManager `CoroutineWorker`, 주입된 앱 스코프.
- 디스패처는 주입합니다 (`ioDispatcher: CoroutineDispatcher`). 코드에 `Dispatchers.IO`를 박지 않습니다(DI 모듈에서만).
- suspend 함수는 main-safe: 호출 측이 디스패처를 신경 쓰지 않게 `withContext(ioDispatcher)`는 data에서.
- Flow: 차가운 Flow 기본. UI 노출은 `stateIn(scope, SharingStarted.WhileSubscribed(5_000), initial)`.
- `delay` 기반 폴링 대신 스케줄러(WorkManager / BGTask)를 씁니다.

## 시간
- `kotlin.time.Clock` / `kotlin.time.Instant`를 주입해서 씁니다. `Clock.System`은 DI 모듈에서만. `System.currentTimeMillis()` 금지.
- 표시용 날짜 변환(`TimeZone.currentSystemDefault()`)은 presentation·UI에서만.

## 직렬화·네트워크 (data)
- kotlinx.serialization. `Json { ignoreUnknownKeys = true }`는 외부 택배사 응답 파싱에만. 레시피 파싱은 엄격 모드 + `min_interpreter_version` 확인.
- Ktor `HttpClient`는 DI로 하나를 공유하고 엔진은 플랫폼별(OkHttp / Darwin). 테스트는 `MockEngine`.
- 타임아웃, 재시도(지수 백오프), User-Agent를 명시합니다. 허용 도메인 밖 요청은 보내기 전에 거부합니다.
- HTML 파싱은 Ksoup. 셀렉터·경로는 코드가 아니라 레시피에 둡니다.

## 로깅
- Kermit 사용(F-00에서 도입). 송장번호·이메일·토큰 원문을 로그에 남기지 않습니다 (`TrackingNumber.masked()` → `6087****5678`).
- `println` 금지.

## Gradle
- 버전 카탈로그만 사용, 하드코딩 버전 금지. 공통 설정은 `build-logic` convention plugin.
- configuration cache·build cache 호환을 유지합니다.
