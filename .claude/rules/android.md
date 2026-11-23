---
paths:
  - "androidApp/**"
---

# Android 규칙 (Compose · Glance · WorkManager · PROCESS_TEXT)

## Compose
- 화면은 `XxxRoute`(ViewModel 연결, `collectAsStateWithLifecycle`) + `XxxScreen`(상태와 콜백만 받는 Stateless) 두 단계.
- Composable 매개변수: 필수 → `modifier: Modifier = Modifier`(첫 번째 선택 매개변수) → 나머지 선택. `Modifier`는 루트에 한 번만 적용.
- 매개변수는 안정 타입(불변 data class, `ImmutableList`). 람다는 `remember`가 필요한지 확인.
- 상태 끌어올리기. Composable 안에서 UseCase·Repository 호출 금지, `LaunchedEffect`로 비즈니스 로직 실행 금지.
- 모든 화면·컴포넌트에 상태별 `@Preview`(빈 상태, 로딩, 오류, 긴 문자열, 다크 모드, 글씨 1.3배).
- 색·글꼴·모서리·그림자는 `TaekbugiTheme`(값은 `docs/design/tokens.md`)에서만. 화면 코드에 `Color(0xFF…)` 금지.
- 문자열은 `strings.xml`(한국어). 디자인 문구를 **한 글자도 바꾸지 않고** 옮깁니다. 디자인에 없는 문구가 필요하면 멈추고 보고.
- 이모지 금지. 아이콘은 1.8px 라인 아이콘 벡터(`ImageVector`/드로어블)로. 택배사 로고 금지(이름 텍스트만).
- 접근성: 아이콘 버튼 `contentDescription`(디자인의 `aria-label` 그대로), 터치 영역은 `minimumInteractiveComponentSize()`로 확보하되 보이는 크기는 디자인대로.
- QA·테스트용 `Modifier.testTag("…")`를 주요 요소에 달고, 루트에 `semantics { testTagsAsResourceId = true }`를 켜서 uiautomator·Maestro가 찾게 합니다.
- 내비게이션: Navigation Compose 타입 안전 라우트(`@Serializable` 객체).

## PROCESS_TEXT
- 전용 액티비티(투명/하단 시트 테마), `intent-filter`: `android.intent.action.PROCESS_TEXT`, `mimeType="text/plain"`, 라벨 "택배 추적"(디자인 문구).
- `EXTRA_PROCESS_TEXT`만 읽고, 결과를 돌려주지 않으므로 `EXTRA_PROCESS_TEXT_READONLY`와 무관하게 원문을 바꾸지 않습니다.
- 로그인 전이면 로그인 화면을 띄우지 않고 임시 큐에 넣습니다 (기획 0장). 안내 UI는 G-14 결정 전 금지.

## 클립보드
- 앱이 포그라운드일 때만 읽습니다(Android 10+ 제한). 읽기 시 시스템 토스트가 뜨는 것(Android 12+)을 고려해 앱 시작 시 한 번만.

## WorkManager
- `CoroutineWorker` + 생성자 주입(Koin `WorkerFactory`). 네트워크 제약(`NetworkType.CONNECTED`).
- 상태별 주기(6시간/2시간/30분)는 domain `RefreshPolicy`가 정하고, 워커는 계산된 지연으로 `OneTimeWorkRequest`를 고유 이름(`refresh-<parcelId>`)으로 `enqueueUniqueWork(REPLACE)`. 최소 15분 제한 준수.
- 실패는 `Result.retry()` + 백오프. 차단 신호(403·캡차)는 재시도하지 않고 도메인 오류로 기록.
- 조회 후 위젯 갱신(`GlanceAppWidget.updateAll`).

## Glance
- 위젯은 로컬 DB에서 읽은 상태만 그립니다(위젯에서 네트워크 금지).
- Glance 전용 Composable 사용(`androidx.glance.*`), 일반 Compose 컴포넌트를 섞지 않습니다.
- 크기: 디자인 4×2 · 2×2 (`SizeMode.Responsive`).

## 디버그 도구 (QA용, `src/debug`만)
- 위젯 고정 요청(`requestPinAppWidget`), 즉시 조회 실행, 클립보드 값 주입, 시간 이동은 **debug 소스셋에만** 둡니다. release에 섞이지 않게 합니다.

## 권한·보안
- 권한 추가(알림 `POST_NOTIFICATIONS` 등)는 기능 명세에 적고 사용자 확인 후.
- `android:exported`를 명시합니다. 네트워크는 HTTPS만(`cleartextTrafficPermitted=false`).
- 백업 규칙: DB·키 저장소는 자동 백업에서 제외(`dataExtractionRules`).
