# F-XX. <기능 이름>

- 상태: TODO
- 플랫폼: Android / iOS / 공통
- 담당 에이전트: planner → architect → test-engineer → shared-engineer / android-engineer / ios-engineer → code-reviewer → qa-android / qa-ios

## 1. 근거
### 기획
- `docs/product/mvp-spec.md` §N "…" (인용)

### 디자인
- 화면: [Main](https://claude.ai/artifact/6xmzzowC1QjoEWtrLCKqHh#artboard-Main) …
- 화면에서 읽은 값: 문구(그대로), 크기, 색 토큰(`docs/design/tokens.md` 이름), 상태별 변화

### 불일치 · 미정
- 관련 G-/Q- ID. **OPEN 항목이 하나라도 있으면 여기서 멈추고 보고합니다.**

## 2. 범위
- 포함:
- 제외: (특히 서버 연동 — API 문서 전 금지)

## 3. 수용 기준 (Given / When / Then)
각 줄이 테스트 하나 이상과 QA 시나리오 하나 이상으로 이어집니다.

| AC | Given | When | Then | 단위 | 통합 | QA |
|---|---|---|---|---|---|---|
| AC-1 | | | | | | |

## 4. 설계
- 영향 모듈·패키지:
- 새 포트 / UseCase / ViewModel:
- 플랫폼 구현:
- ADR 필요 여부:

## 5. 테스트 계획
- 단위:
- 통합:
- 제어문 없는 테스트로 쪼갤 케이스 목록:

## 6. QA 시나리오
| # | 사전 조건 | 조작 | 기대 결과 | 디자인 비교 화면 |
|---|---|---|---|---|
| 1 | | | | |

## 7. 진행 기록
- YYYY-MM-DD: 명세 작성
- YYYY-MM-DD: 검증 통과 (`scripts/verify.sh`)
- YYYY-MM-DD: 리뷰 통과
- YYYY-MM-DD: QA PASS → `docs/qa/reports/…`
