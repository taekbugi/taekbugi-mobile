# 0005. 테스트 정책: 단위 + 통합, 제어문 금지

- 상태: Accepted (사용자 지정, 2026-11-23)

## 결정
- 모든 기능은 **단위 테스트와 통합 테스트**를 함께 갖습니다. 둘 중 하나라도 없으면 완료가 아닙니다.
- 테스트 코드에 `if`·`else`·`when`·`for`·`while`·`do`·`forEach`·`repeat`·`try/catch`·`?:`·`takeIf` 같은 **제어문·반복문을 절대 쓰지 않습니다.** 입력이 여러 개면 테스트 함수를 여러 개 씁니다. 반복을 대신하는 데이터 주도 테스트(`withData`, `@ParameterizedTest`, `@Test(arguments:)`)도 쓰지 않습니다.
- 판단이 필요한 테스트 대역(Fake)은 `:shared:testing` 모듈의 일반 소스에 둡니다. 테스트 소스셋은 제어문 검사 대상이고, Fake는 단순하게 유지합니다.
- 검사: `scripts/check_test_control_flow.py` (Claude Code 훅, `scripts/verify.sh`, CI에서 실행).

자세한 내용: [`../../testing/strategy.md`](../../testing/strategy.md)
