# 테스트 전략

## 절대 규칙
1. 모든 기능에 **단위 테스트 + 통합 테스트**를 둡니다.
2. 테스트 코드(테스트 소스셋 전부)에 **제어문·반복문 금지**: `if` `else` `when` `for` `while` `do` `.forEach` `.forEachIndexed` `repeat` `try` `catch` `?:` `?.let` `takeIf` `takeUnless` / Swift `if` `guard` `switch` `for` `while` `repeat` `.forEach` `??` `do-catch`.
   - 반복 대신 **테스트 함수를 나눕니다.** 데이터 주도 테스트 도구도 쓰지 않습니다.
   - 예외 검증은 `assertFailsWith<T> { … }` (Swift: `#expect(throws:)` / `XCTAssertThrowsError`).
   - null 처리는 `assertNotNull(x)`가 돌려주는 값을 씁니다 (Swift: `try XCTUnwrap`, `try #require`).
3. 테스트는 결정적이어야 합니다: 실제 시간·난수·네트워크·`Thread.sleep` 금지. 시간은 주입한 `Clock`(테스트는 `FixedClock`), 코루틴은 `runTest` 가상 시간, 네트워크는 Ktor `MockEngine`.

자동 검사: `python3 scripts/check_test_control_flow.py --all` (Claude Code는 테스트 파일을 저장할 때마다 훅이 실행)

## 테스트 종류

| 종류 | 위치 | 대상 | 도구 |
|---|---|---|---|
| 단위 | `shared/*/src/commonTest` | domain 정책·UseCase, 매퍼, 레시피 단계 하나, ViewModel(Fake 주입) | kotlin.test, kotlinx-coroutines-test, Turbine |
| 통합 (shared) | `shared/data/src/jvmTest` 또는 `commonTest` | 레시피 해석기 + MockEngine + 골든 응답 → 정규화 결과 / Repository + SQLDelight 메모리 DB / UseCase + 실제 data 구현 | MockEngine, JdbcSqliteDriver |
| 통합 (Android) | `androidApp/src/androidTest` (기기) · `src/test` (Robolectric) | Compose 화면 + ViewModel, PROCESS_TEXT 인텐트 → 등록 시트, WorkManager 스케줄, Glance 위젯 렌더 | compose-ui-test, work-testing, glance-appwidget-testing, ActivityScenario |
| 통합 (iOS) | `iosApp/iosAppTests` | 공유 확장 텍스트 처리 → 큐 저장, App Group DB 접근, 위젯 Timeline Provider | Swift Testing / XCTest |
| 아키텍처 | `shared/architecture-test` | 레이어 의존 방향, 이름 규칙 | Konsist |
| QA (수동 자동화) | `qa/maestro/`, `docs/qa/reports/` | 기능 완료 시 실제 에뮬레이터·시뮬레이터 조작 | adb, xcrun simctl, Maestro |

## 작성 규칙
- 이름: 한글 행위 문장 + 밑줄. `fun 이동중_상태면_다음_조회는_2시간_뒤다()` (모든 플랫폼에서 안전한 식별자. 공백 있는 백틱 이름은 쓰지 않음)
- 구조: `// given` `// when` `// then` 세 구역. 테스트 하나에 행위 하나.
- 검증: `assertEquals(expected, actual)` 순서. 컬렉션은 통째로 비교 (`assertEquals(listOf(A, B), result)`).
- 테스트 데이터: `:shared:testing`의 빌더 `aParcel(status = InTransit)`. 기본값을 두고 테스트에 필요한 값만 씁니다.
- Fake 우선, Mock 라이브러리 도입은 ADR 필요. Fake는 `:shared:testing/src/commonMain`에 두고, 상태 기록용 리스트(`savedParcels`)를 노출해 검증합니다.
- 골든 응답: `shared/data/src/commonTest/resources/golden/<carrier>/<case>.(html|json)`. **실제 송장번호·이름·전화번호·상세 주소는 마스킹**한 뒤 커밋합니다. 마스킹 전 원본은 저장소에 넣지 않습니다.
- 커버리지(Kover): domain 라인 90% 이상, data 80% 이상을 목표로 하고 `koverVerify`로 막습니다 (F-00에서 설정).

## 좋은 예 / 나쁜 예

```kotlin
// 나쁜 예 — 반복문과 분기
@Test
fun 상태별_조회_주기() {
    for ((status, expected) in cases) {            // 금지
        if (status == Delivered) continue           // 금지
        assertEquals(expected, policy.intervalOf(status))
    }
}

// 좋은 예 — 케이스마다 테스트 하나
@Test
fun 집하전_상태면_조회_주기는_6시간이다() {
    // given
    val policy = RefreshPolicy()
    // when
    val interval = policy.intervalOf(DeliveryStatus.NotPickedUp)
    // then
    assertEquals(6.hours, interval)
}

@Test
fun 배송완료_상태면_조회를_멈춘다() {
    val policy = RefreshPolicy()

    val interval = policy.intervalOf(DeliveryStatus.Delivered)

    assertNull(interval)
}
```

```kotlin
// 통합 — 레시피 해석기 + 골든 응답
@Test
fun CJ_배송출발_응답을_배송출발_상태로_정규화한다() = runTest {
    // given
    val engine = goldenEngine("cj/out_for_delivery.json")
    val source = RecipeTrackingSource(httpClient(engine), bundledRecipe("cj"), FixedClock(NOW))
    // when
    val result = source.track(CarrierCode.CJ, TrackingNumber("000000000000"))
    // then
    assertEquals(DeliveryStatus.OutForDelivery, assertIs<TrackingResult.Success>(result).status)
}
```
