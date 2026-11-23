@AGENTS.md

# Claude Code 전용

공통 지침은 위의 AGENTS.md입니다. 여기에는 Claude Code에서만 쓰는 구성만 적습니다.

## 메인 세션의 역할
- 메인 세션은 **오케스트레이터**입니다. 기능 개발은 `/feature-dev F-XX`로 시작하고, 단계마다 하위 에이전트를 Agent 도구로 호출합니다 (하위 에이전트는 다른 에이전트를 부르지 못함).
- 하위 에이전트 결과 첫 줄이 `STOP:`이면 그 내용을 사용자에게 그대로 보고하고 결정을 기다립니다. 대신 판단해서 진행하지 않습니다.
- Android·iOS 구현, Android·iOS QA처럼 서로 독립인 단계는 한 메시지에서 병렬로 호출합니다.
- 디자인 정본은 Artifact 도구(`action: "read"`)로 읽습니다. 캔버스를 수정·게시하지 않습니다.

## 하위 에이전트 (`.claude/agents/`)
| 이름 | 언제 |
|---|---|
| `planner` | 명세 작성, 기획↔디자인 대조 |
| `architect` | 설계, ADR |
| `test-engineer` | 테스트 먼저, 통합 테스트, 테스트 규칙 감사 |
| `shared-engineer` | KMP domain·data·presentation |
| `android-engineer` | Compose·Glance·WorkManager·PROCESS_TEXT |
| `ios-engineer` | SwiftUI·WidgetKit·Share Extension |
| `recipe-engineer` | 택배사 분석·레시피·골든 샘플 (클린룸) |
| `code-reviewer` | 읽기 전용 리뷰 |
| `qa-android` / `qa-ios` | 에뮬레이터·시뮬레이터 직접 조작 QA |
| `api-integrator` | API 문서 도착 후에만 |

## 스킬 (`.claude/skills/`)
`/feature-dev` · `/verify` · `/qa-android` · `/qa-ios` · `/api-onboarding` · `/carrier-recipe` · `/adr` · `/report-gap` · (참조용) `design-reference`, `kmp-testing`

## 규칙 (`.claude/rules/`)
항상 적용: `00-stop-and-report`, `backend-api`, `security-privacy`, `docs-and-git`
경로별 적용: `architecture`, `kotlin`, `android`, `ios`, `testing`, `design-ui`, `recipes`

## 훅 (`.claude/settings.json`)
- `PostToolUse` → `.claude/hooks/check-test-control-flow.sh`: 테스트 파일에 제어문이 있으면 저장 직후 되돌려 보냅니다. 검사를 피하려고 문법을 바꾸지 말고 테스트를 나눕니다.
- `PreToolUse` → `.claude/hooks/guard-backend-api.sh`: API 문서 없이 `shared/data/**/remote/server/**`를 만들면 차단합니다. 다른 경로로 우회하지 않습니다.
- 훅은 `python3`와 `jq`가 필요합니다.

## 사용자에게 명령 실행을 부탁할 때
대화형 로그인, `sudo`, 대용량 SDK 설치는 사용자가 직접 실행하도록 `! <명령>` 형태로 제안합니다.
