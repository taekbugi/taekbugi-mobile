---
name: verify
description: 저장소 전체 검사를 실행한다 — 테스트 제어문 검사, Gradle check(ktlint·detekt·단위·통합 테스트·Kover), 선택적으로 Android 기기 테스트와 iOS 테스트. 구현 후, 리뷰 전, "검증 돌려줘"에 사용.
argument-hint: "[--android-device] [--ios]"
---

# 검증

```sh
scripts/verify.sh $ARGUMENTS
```

- 옵션 없음: 테스트 제어문 검사 + `./gradlew check`
- `--android-device`: 켜진 에뮬레이터에서 `connectedDebugAndroidTest`까지
- `--ios`: `xcodebuild test` (시뮬레이터)

## 실패했을 때
- 출력에서 **첫 번째 실패 원인**을 찾아 파일:줄과 함께 요약합니다.
- 제어문 위반: 테스트를 케이스별 함수로 나눠서 고칩니다. 검사 스크립트를 고치거나 우회하지 않습니다.
- Gradle 래퍼가 아직 없으면(F-00 전) 해당 단계는 건너뛰었다고 그대로 보고합니다.
- 테스트를 지우거나 `@Ignore`로 통과시키지 않습니다.
