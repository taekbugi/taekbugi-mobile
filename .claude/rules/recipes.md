---
paths:
  - "shared/data/**/recipe/**"
  - "shared/data/**/recipes/**"
  - "shared/data/**/golden/**"
  - "docs/carriers/**"
---

# 레시피·택배사 규칙

- 절차: `carrier-recipe` 스킬. 형식: `docs/architecture/recipe-format.md` (Draft).
- 클린룸: delivery-tracker(ELv2) 등 외부 구현을 보지 않습니다. 근거는 `docs/carriers/<code>.md`의 직접 관찰 기록뿐.
- 택배사 사이트를 실제로 호출하는 분석은 **사용자 확인 후**, 사람이 브라우저에서 하는 수준의 요청 횟수로만 합니다. 자동 대량 요청 금지.
- 분석 기록·골든 샘플에 실제 송장번호·이름·전화번호·주소를 남기지 않습니다. 마스킹 후 저장.
- 레시피 변경 = 골든 테스트 추가/갱신 + 상태 매핑 표 갱신. 매핑에 없는 원본 상태는 `Unmapped(rawCode)`로 남기고 임의의 상태로 끼워 맞추지 않습니다.
- 번들 레시피도 서명 검증 경로를 그대로 탑니다(테스트용 키는 테스트 리소스에만, 운영 비밀키는 저장소에 없음).
