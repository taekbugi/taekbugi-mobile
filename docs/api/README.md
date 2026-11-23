# 백엔드 API

> **현재 상태: API 문서 없음 → 서버 연동 작업 금지** (ADR-0006)

## 규칙
- 백엔드 API 문서가 전달되기 전에는 엔드포인트·필드·인증 방식·오류 코드를 **추측하지 않습니다.**
- `shared/data/src/**/remote/server/**` 경로에 파일을 만들면 Claude Code 훅(`.claude/hooks/guard-backend-api.sh`)이 막습니다. `specs/`에 문서가 들어오면 풀립니다.
- 기획서 6장의 Django 모델은 **백엔드 내부 설계 참고용**이며 API 계약이 아닙니다. 이것으로 DTO를 만들지 않습니다.

## 문서가 오면
1. 받은 원문을 그대로 `specs/`에 넣습니다 (예: `specs/openapi-v1.yaml`, `specs/2026-12-01-api.md`). 원문은 고치지 않습니다.
2. `/api-onboarding` 스킬을 실행합니다 → `contract-notes.md`(요약)와 차이 보고가 만들어집니다.
3. 사용자 확인 후 BLOCKED_API 기능(F-17~F-21)을 차례로 풉니다.

## 폴더
- `specs/` — 백엔드가 준 원문 (현재 비어 있음)
- `contract-notes.md` — 원문 요약, 앱 쪽 해석, 미해결 질문 (문서 도착 후 작성)
