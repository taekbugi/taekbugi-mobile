# 0001. Clean Architecture와 모듈 경계

- 상태: Accepted (사용자 지정, 2026-11-23)

## 배경
Android·iOS·위젯·공유 확장·백그라운드 작업이 같은 규칙(송장 판별, 조회 주기, 지연 판단)을 써야 하고, 택배사 사이트 개편과 백엔드 API 미정이라는 두 가지 변동 요인이 있습니다.

## 결정
- `:shared:domain`(순수 Kotlin) ← `:shared:data` / `:shared:presentation` ← 앱 셸 구조를 씁니다.
- domain은 포트(인터페이스)만 정의하고, 레시피 해석기·DB·서버 API는 data가 구현합니다.
- 레이어 단위 Gradle 모듈 + 모듈 안 기능 단위 패키지로 나눕니다. 기능이 늘어 빌드가 느려지면 기능 모듈 분리를 새 ADR로 검토합니다.
- 경계는 Gradle 의존성과 Konsist 테스트로 강제합니다.

## 결과
- 택배사 사이트 개편은 data(레시피)만, 서버 API 도착은 data(`remote/server`)만 바꾸면 됩니다.
- 모듈이 늘어나는 만큼 초기 설정 비용이 있습니다 (`build-logic` convention plugin으로 줄임).
