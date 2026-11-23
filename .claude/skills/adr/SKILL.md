---
name: adr
description: 아키텍처 결정 기록(ADR)을 docs/architecture/adr/에 쓴다. 새 모듈·외부 라이브러리·저장 형식·권한·레이어 경계 변경 등 되돌리기 어려운 결정이 필요할 때 사용.
argument-hint: "<결정 제목>"
---

# ADR 작성

1. `docs/architecture/adr/README.md` 표에서 다음 번호를 정합니다.
2. `docs/architecture/adr/NNNN-<kebab-title>.md`:
```markdown
# NNNN. <제목>

- 상태: Proposed
- 날짜: YYYY-MM-DD
- 관련: F-XX, Q-XX, ADR-NNNN

## 배경
왜 지금 결정이 필요한가. 제약(기획·디자인·플랫폼).

## 제안
무엇을 어떻게. 버전·라이선스(외부 라이브러리면 필수).

## 대안
검토한 다른 선택과 고르지 않은 이유.

## 결과
좋아지는 점, 비용, 되돌리는 방법, 테스트·QA 영향.
```
3. README 표에 행 추가.
4. 사용자에게 승인을 요청합니다. 승인되면 `Accepted`로, 기존 ADR을 대체하면 기존 것에 `Superseded by NNNN`.
