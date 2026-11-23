---
name: carrier-recipe
description: 택배사 하나의 조회 레시피를 클린룸으로 추가·수정한다 — 직접 관찰 기록, 송장번호 규칙, 선언형 레시피 JSON, 상태 매핑, 마스킹 골든 응답, 골든 테스트. "/carrier-recipe cj", 택배사 사이트 개편 대응, 매핑 누락 대응에 사용.
argument-hint: "<carrier-code: epost|cj|lotte|hanjin|logen>"
---

# 택배사 레시피 작업

## 전제
- 레시피 해석기(F-02)가 있어야 합니다. 형식: `docs/architecture/recipe-format.md`.
- **클린룸**: delivery-tracker(ELv2) 등 외부 구현을 보지 않습니다. 검색 결과에 나와도 열지 않습니다.
- 실제 택배사 서버 요청은 사용자 확인 후, 적은 횟수로만. 실제 송장번호는 사용자에게 받고 어디에도 기록하지 않습니다.
- 우체국은 공공데이터포털 서비스 키 처리(Q-03)가 결정돼야 합니다.

## 절차
1. **관찰** — 공개 조회 페이지의 요청 흐름(URL, 메서드, 쿠키·토큰, 파라미터 이름, 응답 형식)을 확인해 `docs/carriers/<code>.md`에 적습니다 (형식: `docs/carriers/README.md`). 관찰 방법(브라우저 개발자 도구 / 사용자가 준 HAR 등)도 적습니다.
2. **송장번호 규칙** — 자릿수·체크섬. 공개 출처가 있으면 출처를 적고, 없으면 "관찰 기반"이라고 적습니다. 규칙은 domain `CarrierDetector`에 들어가므로 shared-engineer에게 넘길 목록으로.
3. **골든 응답** — 응답 샘플을 마스킹해서 `shared/data/src/commonTest/resources/golden/<code>/`에 저장: 집하 전 / 이동 중 / 배송 출발 / 배송 완료 / 없는 송장 / 차단(403) 각각 가능한 만큼. 파일 머리(가능한 형식이면)에 관찰일.
4. **레시피** — `shared/data/src/commonMain/resources/recipes/<code>.json`. 허용 도메인 안의 HTTPS만. 버릴 필드(전화번호·수령인·상세 주소)는 추출하지 않습니다.
5. **상태 매핑** — 원본 코드/문구 → `DeliveryStatus`. 모르는 값은 `Unmapped(rawCode)`. 매핑 표를 노트에 적습니다.
6. **테스트** — 골든 파일마다 통합 테스트 하나 이상 (제어문 금지, 파일마다 함수 하나). 개인정보 필드가 결과에 없는지 검증하는 테스트 포함.
7. **서명** — 번들 레시피는 테스트 키로 서명한 테스트 리소스와, 운영 서명(사용자/CI 보유 비밀키) 절차를 분리합니다. 운영 비밀키를 요청하거나 저장하지 않습니다.
8. `scripts/verify.sh` 통과.

## 사이트 개편 대응
- 새 골든 샘플 추가(이전 것 유지, 파일명에 날짜) → 레시피 `version` 올림 → 노트에 "변경 이력" 절 추가.
