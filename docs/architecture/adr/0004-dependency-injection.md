# 0004. DI: Koin

- 상태: Proposed

## 제안
- **Koin**(KMP 지원)으로 앱 셸에서만 조립합니다. domain에는 Koin 의존이 없습니다 (생성자 주입만).
- 모듈 단위: `domainModule`, `dataModule`, `presentationModule`, 플랫폼별 `androidPlatformModule` / `iosPlatformModule`.
- `checkModules`/`verify()` 테스트로 그래프를 검증합니다.

## 대안
- 수동 DI: 의존성은 없지만 위젯·워커·확장 진입점이 많아 조립 코드가 흩어집니다.
- Hilt: Android 전용이라 공유 코드에 못 씁니다.
