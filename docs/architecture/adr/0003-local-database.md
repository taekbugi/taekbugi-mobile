# 0003. 로컬 DB: SQLDelight

- 상태: Proposed

## 배경
앱·위젯·공유 확장(iOS App Group)이 같은 DB를 읽고, 로그인 전 임시 큐도 저장해야 합니다. 통합 테스트에서 실제 SQL을 메모리 DB로 돌릴 수 있어야 합니다.

## 제안
- **SQLDelight** (Android: `AndroidSqliteDriver`, iOS: `NativeSqliteDriver` + App Group 경로, 테스트: JVM `JdbcSqliteDriver(IN_MEMORY)`).
- 스키마 변경은 `.sqm` 마이그레이션 파일로 관리하고 `verifyMigrations`를 켭니다.
- 쿼리는 `Flow`로 노출하고 domain 모델로 매핑한 뒤 내보냅니다 (Row 타입이 domain 밖으로 나가지 않음).

## 대안
- Room KMP: Google 공식, 어노테이션 기반. SQL을 직접 쓰는 SQLDelight가 App Group 경로 지정과 다중 프로세스 접근 제어가 더 명시적이라 제안에서 제외했습니다. 사용자가 원하면 바꿉니다.

## 결과
- 위젯·확장 프로세스가 동시에 쓰는 경우를 대비해 WAL 모드와 쓰기 경로 단일화(앱 또는 큐만 쓰기)를 지킵니다.
