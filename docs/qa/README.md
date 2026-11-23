# QA

기능 하나가 끝날 때마다(검증·리뷰 통과 후) QA 에이전트가 **실제 에뮬레이터·시뮬레이터를 직접 켜고 앱을 조작**해서 확인합니다. QA PASS 전에는 기능이 `DONE`이 아닙니다.

| 에이전트 | 대상 | 절차 |
|---|---|---|
| `qa-android` | Android Emulator (AVD) | `.claude/skills/qa-android/SKILL.md` |
| `qa-ios` | iOS Simulator | `.claude/skills/qa-ios/SKILL.md` |

## 무엇을 어디에 두나 (버전 관리)

| 대상 | 위치 | git | 규칙 |
|---|---|---|---|
| QA 스크립트 (Maestro 흐름) | `qa/maestro/<android\|ios>/F-XX-<slug>.yaml` | 커밋 | 기능마다 하나 이상. 머리 주석 `feature` `spec` `covers`(AC) `changed`(날짜·이유) 필수. 화면이 의도적으로 바뀔 때만 수정. 실패를 숨기려고 고치지 않음 |
| 실행 보고서 | `docs/qa/reports/F-XX/<platform>/<날짜>-r<번호>/report.md` | 커밋 | `scripts/qa/new_run.py`로만 생성. **실행마다 새 폴더, 끝난 보고서는 수정 금지.** FAIL 실행도 지우지 않고 남김 |
| 핵심 스크린샷 | 같은 폴더 `screenshots/` | 커밋 | 최대 10장, 폭 540px로 축소, 가짜 데이터만 |
| 원본 로그·전체 스크린샷·Maestro 출력 | 같은 폴더 `raw/` | 제외(`.gitignore`) | 로컬 확인용 |
| 실행 기록 색인 | `docs/qa/reports/INDEX.md` | 커밋 | 추가만. 실행 끝나면 그 행의 결과 칸만 갱신 |
| 최신 결과 링크 | `docs/features/backlog.md` QA 보고서 칸 | 커밋 | 기능 DONE 시 마지막 PASS 실행 링크 |

각 보고서에는 `new_run.py`가 **커밋 해시, 작업 트리 변경 여부와 diff 해시, 명세 파일 해시, 흐름 파일별 git blob 해시**를 적습니다. QA 에이전트는 앱 버전·기기·도구 버전·직전 실행을 채웁니다. 덕분에 "어떤 코드와 어떤 스크립트로 확인한 결과인지"를 나중에 되짚을 수 있습니다.

커밋할 때는 코드·테스트·흐름·보고서를 **같은 기능 커밋**에 넣습니다 (`docs-and-git` 규칙).

## 회귀
기능 QA 때마다 해당 플랫폼의 `qa/maestro/<platform>/` 전체를 다시 돌려 이미 끝난 기능이 깨지지 않았는지 보고서 "회귀" 절에 남깁니다.

## 판정 기준
- 기능 명세의 QA 시나리오 전부 + 수용 기준(AC) 전부
- 디자인 정본과 비교: 문구, 배치, 색 토큰, 상태 칩·아이콘. 차이는 목록으로 보고하고, 기획↔디자인 불일치로 보이면 `STOP:`
- 공통 점검: 비정상 종료 없음, 다크 모드·큰 글씨에서 잘림 없음, 오프라인 시 동작, 로그에 송장번호 원문 없음
- 결과: `PASS` / `FAIL` / `BLOCKED`(환경 문제 — 원인과 필요한 조치 기록)
