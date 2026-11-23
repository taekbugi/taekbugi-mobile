---
paths:
  - "**/src/*Test/**"
  - "**/src/test/**"
  - "**/src/androidTest/**"
  - "**/*Tests/**"
  - "shared/testing/**"
---

# 테스트 규칙

전체 전략: `docs/testing/strategy.md` · 예시: `kmp-testing` 스킬

## 절대 금지 (테스트 소스셋 전부)
`if` `else` `when` `for` `while` `do` `.forEach` `.forEachIndexed` `repeat(` `try` `catch` `?:` `?.let` `takeIf` `takeUnless`
Swift: `if` `guard` `switch` `for` `while` `repeat` `.forEach` `??` `do { } catch`

- 입력이 여러 개면 **테스트 함수를 여러 개** 만듭니다. 데이터 주도 테스트(`withData`, `@ParameterizedTest`, `@Test(arguments:)`)도 금지.
- 예외: `assertFailsWith<T> { }`. null: `val x = assertNotNull(y)`. 타입: `val s = assertIs<Success>(r)`.
- 저장할 때마다 훅이 `scripts/check_test_control_flow.py`를 돌려 위반을 되돌려 보냅니다. 위반을 우회하려고 문법을 비틀지 말고 테스트를 나눕니다.

## 반드시
- 기능마다 **단위 + 통합** 둘 다.
- 이름: 한글 행위 문장 + 밑줄 (`fun 배송완료_상태면_조회를_멈춘다()`). 백틱 공백 이름 금지.
- `// given` `// when` `// then` 구역, 테스트 하나에 행위 하나.
- 결정적: `FixedClock`, `runTest` 가상 시간, `MockEngine`, 메모리 DB. 실제 네트워크·시간·난수·`Thread.sleep` 금지.
- Fake는 `:shared:testing`(`shared/testing/src/commonMain`)에. 테스트 소스셋 안에 분기 있는 헬퍼를 만들지 않습니다.
- 골든 응답은 개인정보 마스킹 후 커밋. 실제 송장번호 대신 `000000000000` 형식.
- 실패하는 테스트를 먼저 쓰고(AC 기준) 구현합니다.
- 테스트를 지우거나 `@Ignore`로 통과시키지 않습니다. 필요하면 이유를 보고합니다.
