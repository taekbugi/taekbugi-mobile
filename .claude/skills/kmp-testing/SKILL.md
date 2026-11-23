---
name: kmp-testing
description: 택부기 테스트 작성법 — 레이어별 단위·통합 테스트 패턴, Fake·빌더, MockEngine 골든 테스트, SQLDelight 메모리 DB, ViewModel·Flow 테스트, Compose/WorkManager 통합 테스트, 그리고 제어문 없이 쪼개는 방법. 테스트를 쓰거나 리뷰할 때 사용.
---

# 테스트 작성법

규칙 전문: `docs/testing/strategy.md`. 핵심: **단위 + 통합 필수, 테스트 코드에 제어문·반복문 금지, 결정적.**

## 도구
kotlin.test · kotlinx-coroutines-test(`runTest`, `StandardTestDispatcher`) · Turbine(Flow) · Ktor `MockEngine` · SQLDelight `JdbcSqliteDriver` · Kover · (Android) compose-ui-test, work-testing, glance-appwidget-testing · (iOS) Swift Testing / XCTest

## 단위: 정책 (domain)
```kotlin
class RefreshPolicyTest {
    private val policy = RefreshPolicy()

    @Test
    fun 이동중_상태면_조회_주기는_2시간이다() {
        assertEquals(2.hours, policy.intervalOf(DeliveryStatus.InTransit))
    }

    @Test
    fun 배송출발_상태면_조회_주기는_30분이다() {
        assertEquals(30.minutes, policy.intervalOf(DeliveryStatus.OutForDelivery))
    }
}
```
여러 입력 = 여러 함수. 공통 준비는 프로퍼티나 `@BeforeTest`로 (분기 없이).

## 단위: UseCase + Fake
```kotlin
@Test
fun 로그인_전이면_송장을_임시_큐에_넣는다() = runTest {
    // given
    val queue = FakePendingRegistrationQueue()
    val useCase = RegisterParcelUseCase(FakeSession(loggedIn = false), queue, FakeParcelRepository())
    // when
    useCase(TrackingNumber("000000000000"), CarrierCode("cj"))
    // then
    assertEquals(listOf(TrackingNumber("000000000000")), queue.enqueued)
}
```
Fake 위치: `shared/testing/src/commonMain/kotlin/com/taekbugi/testing/fake/`. 상태 기록 프로퍼티(`enqueued`, `saved`)를 노출합니다.

## 단위: ViewModel + Turbine
```kotlin
@Test
fun 삭제하면_목록에서_사라진다() = runTest {
    val repo = FakeParcelRepository(initial = listOf(aParcel(id = "p1")))
    val vm = HomeViewModel(ObserveParcelsUseCase(repo), DeleteParcelUseCase(repo))

    vm.state.test {
        skipItems(1)
        vm.onDelete(ParcelId("p1"))
        assertEquals(emptyList(), awaitItem().active)
    }
}
```
`Dispatchers.setMain(StandardTestDispatcher())`는 공통 규칙 클래스/`@BeforeTest`에서.

## 통합: 레시피 + MockEngine + 골든
```kotlin
@Test
fun 한진_HTML의_수령인_이름과_전화번호는_결과에_남지_않는다() = runTest {
    val source = recipeSourceWith(golden("hanjin/delivered.html"))

    val result = assertIs<TrackingResult.Success>(source.track(HANJIN, TrackingNumber("000000000000")))

    assertEquals(listOf("서울 마포구"), result.events.map { it.location })
}
```
- 골든 파일: `shared/data/src/commonTest/resources/golden/<carrier>/<case>.(json|html)`, 마스킹 필수.
- `MockEngine`은 요청 URL이 허용 도메인인지도 검증하는 헬퍼(`:shared:testing`)로 감쌉니다.

## 통합: Repository + 메모리 DB
```kotlin
private val driver = JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY).also { TaekbugiDb.Schema.create(it) }

@Test
fun 같은_송장을_두번_등록하면_하나만_남는다() = runTest {
    val repo = SqlParcelRepository(TaekbugiDb(driver), FixedClock(NOW))

    repo.add(aParcel(tracking = "000000000000"))
    repo.add(aParcel(tracking = "000000000000"))

    assertEquals(1, repo.observeAll().first().size)
}
```

## 통합: Android
- Compose: `createAndroidComposeRule<…>()` 또는 `createComposeRule()` + 실제 ViewModel + Fake/메모리 DB. `onNodeWithTag("register_submit").performClick()`.
- PROCESS_TEXT: `ActivityScenario.launch<ProcessTextActivity>(Intent(Intent.ACTION_PROCESS_TEXT).putExtra(Intent.EXTRA_PROCESS_TEXT, "…000000000000…"))`.
- WorkManager: `WorkManagerTestInitHelper.initializeTestWorkManager`, `TestDriver.setInitialDelayMet(id)` 후 상태 검증.

## 통합: iOS
```swift
@Test func 공유한_텍스트에서_송장을_찾아_큐에_넣는다() async throws {
    let queue = InMemoryPendingQueue()
    let handler = ShareHandler(queue: queue)
    try await handler.handle(text: "등기번호 0000000000000")
    #expect(queue.items == ["0000000000000"])
}
```

## 제어문 없이 쪼개는 법
| 하고 싶은 것 | 금지 | 대신 |
|---|---|---|
| 여러 입력 확인 | `for`, `forEach`, `withData` | 입력마다 테스트 함수 |
| 예외 확인 | `try/catch` | `assertFailsWith<E> { }` / `#expect(throws:)` |
| null 아님 확인 후 사용 | `?.let`, `if (x != null)` | `val v = assertNotNull(x)` / `try #require(x)` |
| 타입 확인 후 사용 | `when (r) { is … }` | `val s = assertIs<Success>(r)` |
| 기본값 | `?:` | 빌더 기본 매개변수 |
| 여러 번 호출 | `repeat(3)` | 호출을 세 줄로 쓰기 |

검사: `python3 scripts/check_test_control_flow.py --all`
