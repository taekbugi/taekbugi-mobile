---
name: api-onboarding
description: 백엔드 API 문서를 전달받았을 때 원문 보관 → 계약 요약 → 기획·디자인과 차이 보고 → ADR → BLOCKED_API 기능 해제 순서로 서버 연동을 시작한다. "API 문서 왔어", "/api-onboarding <파일>"에 사용. 문서 없이 실행하면 아무것도 하지 않는다.
argument-hint: "<API 문서 경로 또는 URL>"
---

# API 문서 온보딩

## 0. 원문 보관 (메인 세션)
- 사용자가 준 문서를 수정 없이 `docs/api/specs/`에 저장합니다. 파일명에 받은 날짜·버전: `2026-12-01-openapi-v1.yaml`.
- URL이면 사용자 확인 후 받아 저장합니다. 비공개 문서 링크는 사용자에게 파일로 달라고 합니다.
- 문서가 없으면 여기서 끝냅니다.

## 1. 계약 요약 — `api-integrator`
`docs/api/contract-notes.md` 작성:
- 문서 버전·출처·받은 날짜
- 환경(base URL), 인증 방식(로그인 3종: Apple·카카오·이메일 코드), 토큰 수명·갱신, 오류 형식, 페이지네이션, 버전 정책, 요청 제한
- 엔드포인트 표: 메서드·경로·용도·관련 기능(F-17~F-21)·요청/응답 핵심 필드
- **질문**: 문서에 없는데 앱에 필요한 것 (추측해서 채우지 않음)

## 2. 차이 보고
- 기획서(6장 모델, 송장 저장 방식 `tracking_hmac`/`tracking_ciphertext`, tombstone, 약관 동의 기록, 계정 삭제)와 문서 비교
- 디자인(로그인·이메일 코드·설정 화면의 동작)과 비교 — 예: 코드 유효시간, 재전송 쿨다운 값
- 차이·질문을 사용자에게 보고하고 **확인을 받은 뒤** 3단계로 갑니다.

## 3. ADR — `architect`
- HTTP 클라이언트 구성(Ktor, 인증 플러그인·토큰 갱신), 토큰 저장소, 오프라인·재시도, 동기화 충돌 규칙, 클라이언트 암호화 키 보관(iCloud 키체인 / Android Block Store)
- `Proposed` → 사용자 확인 → `Accepted`

## 4. 해제
- `docs/features/backlog.md`에서 문서로 풀리는 기능을 `TODO`로 바꾸고, 기능별로 `/feature-dev`를 진행합니다.
- 서버 코드 위치: `shared/data/src/commonMain/kotlin/com/taekbugi/data/remote/server/` (문서가 들어오면 훅이 허용)
- 통합 테스트 픽스처는 문서의 예시 요청·응답 그대로 (`shared/data/src/commonTest/resources/api/`).

## 문서가 바뀌면
새 버전 파일을 `specs/`에 추가(이전 버전 유지) → `contract-notes.md`에 변경 절 추가 → 영향 기능 보고.
