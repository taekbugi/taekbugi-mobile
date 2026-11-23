# 문서·Git 규칙 (항상 적용)

## 문서
- 루트에는 `README.md`, `AGENTS.md`, `CLAUDE.md`만 둡니다. 나머지 문서는 전부 `docs/` 아래 맞는 하위 폴더에 (`docs/README.md` 지도 참고). 새 폴더를 만들면 지도에 한 줄 추가.
- `docs/product/mvp-spec.md`(기획 원문)와 `docs/api/specs/`(API 원문)는 고치지 않습니다. 새 버전을 받으면 교체합니다.
- 기능 상태는 `docs/features/backlog.md` 한 곳에서 관리합니다. 명세 진행 기록과 백로그 상태를 함께 갱신합니다.
- 결정은 ADR(`docs/architecture/adr/`), 미정은 `open-questions.md`, 기획↔디자인 차이는 `spec-design-gaps.md`.
- 문서는 한국어, 짧은 문장, 표 우선.

## Git
- 커밋·푸시·PR은 **사용자가 요청할 때만** 합니다. 기능이 끝나면 커밋 여부를 묻습니다.
- 브랜치: `feat/F-XX-<slug>`, `fix/<slug>`, `chore/<slug>`, `docs/<slug>`. main에 직접 커밋하지 않습니다(첫 부트스트랩 커밋은 사용자 확인 후 예외 가능).
- 커밋 메시지: Conventional Commits 접두어(`feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `chore:`) + 한국어 설명. 기능 ID를 적습니다 (`feat(F-08): PROCESS_TEXT 등록 시트`).
- 한 커밋에 한 의도. 생성 파일·빌드 산출물·비밀 값은 커밋하지 않습니다.
