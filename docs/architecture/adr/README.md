# ADR (Architecture Decision Records)

- 파일명: `NNNN-kebab-title.md`, 번호는 이어서 매깁니다.
- 상태: `Proposed`(제안, 사용자 확인 전) · `Accepted` · `Superseded by NNNN`
- `Proposed`인 ADR은 사용자가 승인해야 `Accepted`가 됩니다. 승인 전에도 F-00 부트스트랩은 제안대로 진행할 수 있지만, 바꾸기 어려운 선택(DB, DI, iOS UI)은 진행 전에 사용자에게 한 번 확인합니다.
- 작성 절차: `/adr` 스킬

| 번호 | 제목 | 상태 |
|---|---|---|
| [0001](0001-clean-architecture.md) | Clean Architecture와 모듈 경계 | Accepted |
| [0002](0002-kmp-sharing-scope.md) | KMP 공유 범위와 iOS UI | Proposed |
| [0003](0003-local-database.md) | 로컬 DB: SQLDelight | Proposed |
| [0004](0004-dependency-injection.md) | DI: Koin | Proposed |
| [0005](0005-testing-policy.md) | 테스트 정책: 단위 + 통합, 제어문 금지 | Accepted |
| [0006](0006-backend-api-deferral.md) | 백엔드 API 연동 보류 | Accepted |
