---
paths:
  - "androidApp/src/**/ui/**"
  - "androidApp/src/**/widget/**"
  - "androidApp/src/main/res/**"
  - "iosApp/**/*.swift"
  - "iosApp/**/*.xcstrings"
  - "shared/presentation/**"
---

# 디자인·UI 규칙

- 정본: Claude Design 캔버스 https://claude.ai/artifact/6xmzzowC1QjoEWtrLCKqHh (읽는 법: `design-reference` 스킬, 요약: `docs/design/`)
- 화면을 만들기 전에 해당 아트보드 파일(`project/<화면>.dc.html`)을 직접 읽고 값을 확인합니다. 기억이나 요약만으로 그리지 않습니다.
- 문구는 디자인 그대로. 간격·크기·모서리·그림자·색은 `docs/design/tokens.md`의 토큰 이름으로.
- 톤: 흰 톤 + 그림자, 포인트 컬러는 올리브 그린(`#3F7A2A`) 하나. 테두리 대신 그림자로 카드 구분.
- **이모지 금지.** 배송 상태는 라인 아이콘 + 상태 칩 색으로만.
- **택배사 로고 금지**, 택배사 이름은 텍스트로만. 공식 앱처럼 보이는 표현 금지 (심사 5.2.2).
- 캐릭터·로고 자리(디자인의 점선 박스)는 에셋 슬롯 컴포넌트로 만들고, 실제 에셋이 없으면 보고합니다. 꼬부기를 연상시키는 그림을 임의로 그리지 않습니다.
- 디자인에 없는 화면·상태·문구(빈 목록, 오류, 확인 다이얼로그 등)를 임의로 만들지 않습니다 → `00-stop-and-report.md`.
- 디자인 예시 데이터("겨울 니트", "6087 1234 5678")는 Preview·테스트 데이터로만 씁니다.
