# AGENTS.md — 택부기 모바일

모든 AI 코딩 에이전트(Claude Code, Codex 등)가 따르는 공통 지침입니다. Claude Code 전용 설정은 `CLAUDE.md`와 `.claude/`에 있습니다.

## 프로젝트
**택부기 – 드래그하면 추적되는 택배 위젯.** 어디서든 송장번호를 선택하면 택배사를 판별해 등록하고, 기기에서 택배사 페이지를 직접 조회(서버 드리븐 레시피)해서 위젯으로 보여 주는 Android·iOS 앱입니다. 이 저장소는 **모바일**만 다룹니다(백엔드는 별도).

| 무엇 | 어디 |
|---|---|
| 기획서 v3.1 원문 | `docs/product/mvp-spec.md` |
| **디자인 정본** | Claude Design 캔버스 https://claude.ai/artifact/6xmzzowC1QjoEWtrLCKqHh (요약 `docs/design/`) |
| 기획↔디자인 불일치 | `docs/product/spec-design-gaps.md` |
| 확정 필요 항목 | `docs/product/open-questions.md` |
| 기능 백로그·상태 | `docs/features/backlog.md` |
| 아키텍처·ADR | `docs/architecture/` |
| 테스트 전략 | `docs/testing/strategy.md` |
| QA 절차·보고서 | `docs/qa/` |
| 에이전트 작업 흐름 | `docs/workflow/agentic-workflow.md` |
| 문서 지도 | `docs/README.md` |

## 절대 규칙
1. **기획과 디자인 중 한쪽에만 있거나 서로 다른 내용은 추측해서 구현하지 않는다.** 작업을 멈추고 `spec-design-gaps.md`에 기록한 뒤 사용자에게 보고한다. 디자인이 정본이지만, 디자인에만 있는 기능을 임의로 넣지 않는다.
2. **백엔드 API를 예단하지 않는다.** `docs/api/specs/`에 API 문서가 오기 전에는 엔드포인트·필드·인증·오류 코드를 추측한 코드를 만들지 않는다 (ADR-0006).
3. **테스트는 단위 + 통합 둘 다 필수. 테스트 코드에 `if`·`for`·`when`·`while`·`forEach`·`try/catch`·`?:` 등 제어문·반복문 절대 금지.** 케이스마다 테스트 함수를 나눈다 (ADR-0005, `scripts/check_test_control_flow.py`).
4. **Clean Architecture**: `domain`(순수 Kotlin) ← `data` / `presentation` ← 앱. 안쪽은 바깥을 모른다 (ADR-0001).
5. **기능 하나가 끝나면 QA 에이전트가 에뮬레이터·시뮬레이터를 직접 조작해 확인한다.** QA PASS 전에는 완료가 아니다. QA 스크립트(`qa/maestro/`)와 실행 보고서(`docs/qa/reports/`)는 버전 관리하며, 끝난 보고서는 고치지 않고 재실행은 새 실행으로 남긴다.
6. README.md·AGENTS.md·CLAUDE.md 외 문서는 `docs/` 하위 폴더에 둔다.
7. 택배사 레시피는 직접 분석해서 처음부터 작성한다. **delivery-tracker(Elastic License 2.0) 코드·구조 참고 금지.**
8. UI에 **이모지 금지, 택배사 로고 금지**. 색·글꼴은 디자인 토큰으로만.
9. 송장번호·이메일은 로그·테스트 데이터·스크린샷에 원문으로 남기지 않는다. 택배사 응답의 기사 전화번호·수령인 이름·상세 주소는 저장하지 않는다.
10. 커밋·푸시는 사용자가 요청할 때만.

## 기술 스택
- Kotlin Multiplatform: Ktor, Ksoup, kotlinx.serialization, kotlinx-coroutines, `kotlin.time`, SQLDelight(제안), Koin(제안), Kermit
- Android: Jetpack Compose, Glance, WorkManager, `ACTION_PROCESS_TEXT`
- iOS: SwiftUI(제안), WidgetKit, Share Extension, App Group, SKIE(제안)
- 테스트: kotlin.test, kotlinx-coroutines-test, Turbine, Ktor MockEngine, Konsist, Kover, compose-ui-test, work-testing, Swift Testing
- 품질: ktlint, detekt
- QA: Android Emulator + adb/uiautomator, iOS Simulator + `xcrun simctl`, Maestro

"제안"은 `Proposed` ADR이며 사용자 확인 대상입니다.

## 모듈 (요약)
```
shared/domain        Entity·정책·포트·UseCase (순수 Kotlin)
shared/data          레시피 해석기·SQLDelight·포트 구현 (remote/server는 API 문서 이후)
shared/presentation  공유 ViewModel·UiState
shared/testing       Fake·테스트 데이터 빌더
shared/umbrella      iOS 정적 프레임워크
androidApp/          Compose·Glance·WorkManager·PROCESS_TEXT
iosApp/              SwiftUI·WidgetKit·Share Extension
qa/maestro/          QA 흐름 (버전 관리)
```
상세: `docs/architecture/overview.md`

## 명령
| 목적 | 명령 |
|---|---|
| 전체 검증 | `scripts/verify.sh` (`--android-device`, `--ios`) |
| 테스트 제어문 검사 | `python3 scripts/check_test_control_flow.py --all` |
| 공유 모듈 테스트 | `./gradlew :shared:domain:allTests :shared:data:allTests` |
| Android 빌드·설치 | `./gradlew :androidApp:installDebug` |
| 정적 분석 | `./gradlew ktlintCheck detekt` |
| QA 실행 폴더 생성 | `python3 scripts/qa/new_run.py F-XX android\|ios` |

Gradle 프로젝트는 F-00(부트스트랩)에서 만들어집니다. 그 전에는 Gradle 명령이 없습니다.

## 코딩 관례 (요약)
- Kotlin: `explicitApi()`, 불변 우선, `value class`, sealed + 전수 `when`, `!!` 금지, suspend에서 `runCatching` 금지, 디스패처·`Clock` 주입, 구조적 동시성.
- Compose: Route(상태 연결) + Stateless Screen, `Modifier` 첫 선택 매개변수, 상태별 Preview, 토큰·문자열 리소스, `testTag`.
- Swift: Swift 6 strict concurrency, 공유 규칙을 Swift로 재구현하지 않음, `accessibilityIdentifier`.
- 상세: `.claude/rules/kotlin.md`, `android.md`, `ios.md`, `architecture.md`

## 기능 개발 순서
명세(기획·디자인 대조) → 설계 → **테스트 먼저** → 구현(shared → Android/iOS) → `scripts/verify.sh` → 리뷰 → **에뮬레이터 QA** → 백로그 갱신 → 커밋 여부 확인.
상세: `docs/workflow/agentic-workflow.md`

## 멈추고 물어야 할 때
기획↔디자인 불일치 · 서버 API가 필요한 작업 · 미정 항목(Q-) · 되돌리기 어려운 결정(ADR Proposed, 새 라이브러리, 권한, 패키지명) · 디자인 에셋 부재 · 같은 실패 3회 반복 · 커밋/푸시/외부 전송.
