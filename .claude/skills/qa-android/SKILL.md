---
name: qa-android
description: Android 에뮬레이터를 부팅하고 앱을 설치해 adb·uiautomator·Maestro로 직접 조작하며 기능 QA를 수행하고, 버전 정보가 남는 QA 보고서를 쓴다. qa-android 에이전트가 쓰는 절차이며 "/qa-android F-XX"로 단독 실행도 가능.
argument-hint: "F-XX"
---

# Android QA 절차

값(임시, Q-05 결정 후 갱신): 패키지 `com.taekbugi.android.debug`, 런처 액티비티 `com.taekbugi.android.MainActivity`, AVD `taekbugi_api35`.
F-00 이후 실제 값은 `androidApp/build.gradle.kts`와 매니페스트에서 확인합니다.

## 1. 환경 확인
```sh
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home}"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
adb version && emulator -list-avds && command -v maestro
```
- AVD가 없으면 `docs/setup/dev-environment.md`의 생성 명령을 사용자에게 제안하고 BLOCKED (임의로 큰 이미지 내려받지 않음).
- Maestro가 없으면 adb + uiautomator만으로 진행하고 보고서에 적습니다.

## 2. 실행 폴더 만들기 (버전 기록)
```sh
RUN_DIR=$(python3 scripts/qa/new_run.py F-XX android)
```
- `docs/qa/reports/F-XX/android/<날짜>-r<번호>/` 를 만들고 `report.md`에 커밋·작업 트리 상태·명세 해시·흐름 파일 해시를 채우며 `docs/qa/reports/INDEX.md`에 `RUNNING` 행을 추가합니다.
- 이전 실행 폴더는 **절대 고치지 않습니다.** 재실행은 항상 새 폴더입니다.

## 3. 에뮬레이터 부팅
```sh
adb devices | grep -q emulator || (emulator -avd taekbugi_api35 -no-snapshot-save -no-boot-anim -netdelay none -netspeed full >/dev/null 2>&1 &)
adb wait-for-device
until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = "1" ]; do sleep 2; done
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
```
(부팅 대기 반복문은 QA 셸 스크립트이며 테스트 코드 규칙 대상이 아닙니다.)

## 4. 빌드·설치·초기화
```sh
./gradlew :androidApp:installDebug
adb shell pm clear com.taekbugi.android.debug
adb shell dumpsys package com.taekbugi.android.debug | grep -E "versionName|versionCode"   # 보고서 메타데이터에 기록
adb logcat -c
```

## 5. 조작 방법
| 목적 | 명령 |
|---|---|
| 앱 실행 | `adb shell am start -n com.taekbugi.android.debug/com.taekbugi.android.MainActivity` |
| 드래그 등록(PROCESS_TEXT) | `adb shell am start -a android.intent.action.PROCESS_TEXT -t text/plain --es android.intent.extra.PROCESS_TEXT "운송장번호 000000000000 로 조회하세요" -p com.taekbugi.android.debug` |
| 실제 선택 메뉴 경로 | 메모·메시지 앱에 텍스트 입력 → 길게 눌러 선택 → 메뉴의 "택배 추적" 탭 (uiautomator로 위치 찾기) |
| 화면 요소 찾기 | `adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml $RUN_DIR/raw/` → `resource-id`(testTag), `text`, `content-desc`, `bounds` 확인 |
| 탭 / 입력 / 뒤로 | `adb shell input tap X Y` · `adb shell input text "..."` · `adb shell input keyevent KEYCODE_BACK` |
| 스크린샷 | `adb exec-out screencap -p > $RUN_DIR/screenshots/NN-<장면>.png` |
| 알림 확인 | `adb shell cmd statusbar expand-notifications` → 스크린샷, `adb shell dumpsys notification --noredact` |
| 다크 모드 | `adb shell cmd uimode night yes` / `no` |
| 글씨 1.3배 | `adb shell settings put system font_scale 1.3` (끝나면 `1.0`) |
| 오프라인 | `adb shell svc wifi disable && adb shell svc data disable` (끝나면 enable) |
| 위젯 | debug 도구의 위젯 고정 요청 → 시스템 확인 다이얼로그 탭, 또는 홈 길게 누르기 → 위젯 목록 |
| 백그라운드 조회 | debug 도구 "지금 조회 실행", 또는 `adb shell cmd jobscheduler run -f com.taekbugi.android.debug <jobId>` |
| 크래시 확인 | `adb logcat -b crash -d` |
| 앱 로그 | `adb logcat -d --pid=$(adb shell pidof com.taekbugi.android.debug) > $RUN_DIR/raw/logcat.txt` |

- 테스트 데이터는 가짜 값만(`000000000000`, `qa@example.com`). 실제 택배사 조회가 필요한 시나리오는 사용자에게 테스트용 송장번호를 받고, 보고서·스크린샷에는 마스킹합니다.

## 6. Maestro 흐름 (회귀용, git으로 버전 관리)
- 위치: `qa/maestro/android/F-XX-<slug>.yaml`. 기능마다 하나 이상. 머리 주석 필수:
```yaml
# feature: F-08
# spec: docs/features/F-08-process-text.md
# covers: AC-1, AC-2, AC-4
# changed: 2026-11-30 — 후보 선택 단계 추가
appId: com.taekbugi.android.debug
---
- launchApp:
    clearState: true
- assertVisible:
    id: "home_add_button"
- takeScreenshot: "01-home"
```
- 화면이 의도적으로 바뀐 경우에만 흐름을 고치고 `changed:` 줄을 갱신합니다. 흐름을 고쳐서 실패를 숨기지 않습니다.
- 이번 기능 흐름: `maestro test qa/maestro/android/F-XX-*.yaml --test-output-dir $RUN_DIR/raw/maestro`
- **회귀**: 이미 `DONE`인 기능의 흐름 전체 `maestro test qa/maestro/android/ --test-output-dir $RUN_DIR/raw/regression` — 결과를 보고서 "회귀" 절에.
- Maestro가 못 하는 단계(시스템 다이얼로그 등)는 adb로 직접 조작하고 보고서에 수동 단계로 적습니다.

## 7. 판정
1. 명세 "6. QA 시나리오"와 AC를 하나씩 실행하고 장면마다 스크린샷.
2. 스크린샷을 Read 도구로 열어 **직접 보고** 판단합니다.
3. `design-reference` 스킬로 같은 화면 아트보드를 읽고 문구·배치·색·칩·아이콘을 비교합니다.
4. 공통 점검: 크래시 없음, 다크 모드, 글씨 1.3배, 오프라인, 로그에 송장번호·이메일 원문 없음(`grep -E '[0-9]{10,13}' raw/logcat.txt`).

## 8. 보고서 마무리
- `$RUN_DIR/report.md`를 채웁니다 (new_run.py가 버전 정보를 채워 둔 초안. 앱 버전·기기·도구·이전 실행 칸은 직접 채움).
- 커밋할 스크린샷은 핵심 장면 최대 10장, 폭 540px로 줄입니다: `sips --resampleWidth 540 <파일>` (macOS). 나머지 원본·로그는 `raw/`(git 제외)에 둡니다.
- `docs/qa/reports/INDEX.md`에서 이 실행의 `RUNNING`을 `PASS`/`FAIL`/`BLOCKED`로 바꿉니다. 다른 행은 건드리지 않습니다.
- 에뮬레이터 설정을 원래대로(글씨 1.0, 네트워크 켬, 라이트 모드) 돌려놓습니다.
