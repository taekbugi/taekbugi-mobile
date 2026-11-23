# 에이전트 작업 흐름

## 한눈에

```
사용자: "/feature-dev F-08"
   │
   ▼
[메인 세션 = 오케스트레이터]  하위 에이전트끼리는 서로 부르지 못하므로 메인 세션이 순서대로 호출
   │
   ├─0 착수 확인 ── 백로그 상태, 선행 기능, G-/Q-/API 막힘 확인 ── 막혔으면 ■ 중단·보고
   ├─1 planner ──── 기획·디자인 대조 → docs/features/F-XX-*.md (AC, QA 시나리오)
   │                불일치 발견 → spec-design-gaps.md 기록 → ■ 중단·보고
   ├─2 architect ── 모듈·포트·UseCase 설계, 필요하면 ADR (Proposed면 사용자 확인)
   ├─3 test-engineer ── AC → 실패하는 단위·통합 테스트 먼저 (제어문 금지)
   ├─4 구현 ─────── shared-engineer (domain → data → presentation)
   │                └▶ android-engineer ∥ ios-engineer (shared 계약이 정해진 뒤 병렬)
   │                레시피가 필요하면 recipe-engineer
   ├─5 검증 ─────── scripts/verify.sh 전부 통과 (실패 시 4로)
   ├─6 code-reviewer ── 규칙·아키텍처·보안 검토 (차단 지적 → 4로, 최대 3회 후 보고)
   ├─7 QA ───────── qa-android / qa-ios 가 에뮬레이터·시뮬레이터 직접 조작 → docs/qa/reports/
   │                FAIL → 보고서를 구현 에이전트에 넘겨 4로
   └─8 마무리 ───── 백로그 DONE, 명세 진행 기록, 사용자에게 요약 + 커밋 여부 질문
```

■ = 메인 세션이 작업을 멈추고 사용자에게 보고하는 지점.

## 에이전트

| 에이전트 | 역할 | 쓰기 권한 | 미리 읽는 스킬 |
|---|---|---|---|
| `planner` | 기획·디자인 대조, 기능 명세, 불일치 탐지 | `docs/` | design-reference |
| `architect` | 모듈 경계, 포트·UseCase 설계, ADR | `docs/architecture/`, 명세 4장 | adr |
| `test-engineer` | 테스트 먼저 작성, 통합 테스트, 테스트 규칙 감사 | 테스트 소스셋, `:shared:testing` | kmp-testing |
| `shared-engineer` | KMP domain·data·presentation 구현 | `shared/` | kmp-testing |
| `android-engineer` | Compose·Glance·WorkManager·PROCESS_TEXT | `androidApp/` | design-reference, kmp-testing |
| `ios-engineer` | SwiftUI·WidgetKit·Share Extension·App Group | `iosApp/` | design-reference |
| `recipe-engineer` | 택배사 분석(클린룸)·레시피·골든 샘플 | `docs/carriers/`, 레시피·골든 리소스 | carrier-recipe |
| `code-reviewer` | 읽기 전용 리뷰 | 없음 | — |
| `qa-android` | Android 에뮬레이터 조작 QA | `docs/qa/reports/`, `qa/maestro/android/` | qa-android |
| `qa-ios` | iOS 시뮬레이터 조작 QA | `docs/qa/reports/`, `qa/maestro/ios/` | qa-ios |
| `api-integrator` | API 문서 도착 후에만: 계약 요약, 서버 연동 | `docs/api/`, `shared/data/**/remote/server/` | api-onboarding |

## 스킬 (슬래시 명령)

| 스킬 | 용도 |
|---|---|
| `/feature-dev F-XX` | 위 0~8단계 전체 진행 |
| `/verify` | 검사·빌드·테스트 전부 실행 |
| `/qa-android F-XX`, `/qa-ios F-XX` | QA만 단독 실행 |
| `/api-onboarding` | API 문서를 받았을 때 |
| `/carrier-recipe <carrier>` | 레시피 추가·수정 |
| `/adr <제목>` | ADR 작성 |
| `/report-gap` | 기획↔디자인 불일치 기록·보고 |
| `design-reference`, `kmp-testing` | 다른 단계에서 참조하는 지식 스킬 |

## 규칙이 적용되는 방식

| 수단 | 위치 | 강제력 |
|---|---|---|
| `AGENTS.md` | 루트 | 모든 에이전트 도구 공통 지침 |
| `CLAUDE.md` | 루트 | Claude Code 전용 (AGENTS.md를 불러옴) |
| `.claude/rules/*.md` | 경로별 규칙 | 해당 경로 파일을 다룰 때 자동으로 읽힘 |
| `.claude/hooks/check-test-control-flow.sh` | PostToolUse | 테스트 파일 저장 시 제어문 발견하면 즉시 되돌려 보냄 |
| `.claude/hooks/guard-backend-api.sh` | PreToolUse | API 문서 없이 `remote/server/` 작성 차단 |
| `scripts/verify.sh` | 수동·CI | 제어문 검사 + Gradle check + iOS 테스트 |

## 사용자에게 멈추고 묻는 경우 (요약)
1. 기획과 디자인 중 한쪽에만 있는 내용, 서로 다른 내용
2. 서버 API가 필요한 작업 (문서 도착 전)
3. `open-questions.md`의 미정 항목에 걸린 작업
4. `Proposed` ADR 중 되돌리기 어려운 선택
5. 리뷰·QA 수정 반복이 3회를 넘을 때
6. 커밋·푸시·외부 서비스 전송
