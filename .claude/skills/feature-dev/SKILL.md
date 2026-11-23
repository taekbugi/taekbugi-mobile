---
name: feature-dev
description: 백로그의 기능 하나(F-XX)를 명세 → 설계 → 테스트 먼저 → 구현 → 검증 → 리뷰 → 에뮬레이터 QA → 마무리까지 하위 에이전트로 진행한다. "F-08 개발해줘", "/feature-dev F-01", 다음 기능 진행 요청에 사용.
argument-hint: "F-XX"
---

# 기능 개발 파이프라인

메인 세션이 오케스트레이터입니다. 하위 에이전트는 다른 에이전트를 부르지 못하므로 **메인 세션이 단계마다 Agent 도구로 호출**하고 결과를 다음 단계에 넘깁니다. 각 에이전트의 결과 첫 줄(`READY`/`STOP:`/`PASS`/`FAIL`/`BLOCKED`/`APPROVE`/`CHANGES_REQUIRED`)로 다음 행동을 정합니다.

흐름도와 역할표: `docs/workflow/agentic-workflow.md`

## 0. 착수 확인 (메인 세션)
1. `docs/features/backlog.md`에서 `$ARGUMENTS` 행을 찾습니다. 이미 `IN_PROGRESS`인 다른 기능이 있으면 사용자에게 먼저 묻습니다.
2. 선행 기능이 `DONE`인지 확인합니다.
3. 막힘 칸의 G-/Q- 항목이 `OPEN`이거나 `BLOCKED_API`면 **멈추고** 사용자에게 보고합니다: 무엇이 막혔는지, 결정할 선택지, 막힘과 무관하게 먼저 할 수 있는 부분.
4. 백로그 상태를 `IN_PROGRESS`로 바꿉니다. 브랜치 생성은 사용자에게 물어서 정합니다 (`feat/F-XX-<slug>`).

## 1. 명세 — `planner`
- 넘길 것: 기능 ID, 백로그 행.
- `STOP:` → 사용자에게 그대로 보고하고 결정을 기다립니다. 결정되면 `spec-design-gaps.md`/`open-questions.md`의 결정 칸을 채우고 1단계를 다시 합니다.

## 2. 설계 — `architect`
- 넘길 것: 명세 경로.
- `Proposed` ADR이 생기면 사용자 확인 후 진행합니다.

## 3. 테스트 먼저 — `test-engineer`
- 넘길 것: 명세 경로, 설계 요약.
- 결과: 실패하는 단위·통합 테스트 + Fake. 컴파일에 필요한 시그니처 목록은 4단계에 넘깁니다.

## 4. 구현
- `shared-engineer` 먼저 (domain → data → presentation). 레시피가 필요하면 `recipe-engineer`를 따로 부릅니다.
- shared 공개 API가 정해지면 `android-engineer`와 `ios-engineer`를 **한 메시지에서 병렬로** 부릅니다 (기능의 플랫폼 범위만).
- 각 에이전트의 "다른 에이전트에게 넘길 목록"을 모아 필요한 쪽에 다시 넘깁니다.

## 5. 검증 (메인 세션)
- `scripts/verify.sh` (iOS 범위면 `--ios`, 기기 테스트가 있으면 `--android-device`). 실패하면 실패 출력과 함께 해당 구현 에이전트를 다시 부릅니다.

## 6. 리뷰 — `code-reviewer`
- `CHANGES_REQUIRED`의 [차단] 항목을 구현 에이전트에 넘겨 고친 뒤 5 → 6을 반복합니다. 3회를 넘으면 멈추고 보고합니다.
- [질문]은 사용자에게 전달합니다.

## 7. QA — `qa-android` / `qa-ios`
- 백로그 상태 `IN_QA`. 플랫폼 범위에 맞춰 부릅니다 (둘 다면 병렬).
- 넘길 것: 기능 ID, 명세 경로, android/ios-engineer가 알려 준 패키지·테스트 태그·debug 도구.
- `FAIL` → 보고서 경로를 구현 에이전트에 넘겨 4단계부터 다시 (5·6 거쳐 QA 재실행, 새 실행 폴더가 생김). 3회를 넘으면 보고.
- `BLOCKED` → 환경 조치를 사용자에게 안내 (`! <명령>` 형태로 제안).
- `STOP:` → 불일치 보고.

## 8. 마무리 (메인 세션)
1. 백로그: 상태 `DONE`, 명세·최신 QA 보고서 링크.
2. 명세 "7. 진행 기록"에 날짜별 단계 기록.
3. 사용자에게 요약: 구현 범위, 테스트 수(단위/통합), QA 결과·보고서 경로, 남은 G-/Q-/BLOCKED, 다음 추천 기능.
4. 커밋 여부를 묻습니다. 커밋할 때는 코드 + 테스트 + Maestro 흐름 + QA 보고서(PASS 실행과 그 전 FAIL 실행 모두)를 같은 기능 커밋에 넣습니다.
