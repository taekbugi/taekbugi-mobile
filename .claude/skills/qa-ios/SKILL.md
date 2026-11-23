---
name: qa-ios
description: iOS 시뮬레이터를 부팅하고 앱을 빌드·설치해 xcrun simctl·Maestro로 직접 조작하며 기능 QA(앱·위젯·공유 확장)를 수행하고, 버전 정보가 남는 QA 보고서를 쓴다. qa-ios 에이전트가 쓰는 절차이며 "/qa-ios F-XX"로 단독 실행도 가능.
argument-hint: "F-XX"
---

# iOS QA 절차

값(임시, Q-05 결정 후 갱신): 번들 ID `com.taekbugi.ios`, 스킴 `iosApp`, 기기 `iPhone 16`. F-00 이후 실제 값은 Xcode 프로젝트에서 확인합니다.

## 1. 환경 확인
```sh
xcode-select -p          # /Applications/Xcode.app/... 이어야 함 (CommandLineTools면 simctl 없음)
xcrun simctl list devices available
command -v maestro
```
- Xcode가 없거나 CommandLineTools가 선택돼 있으면 BLOCKED. 사용자 조치: Xcode 설치 후 `! sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`.

## 2. 실행 폴더 만들기 (버전 기록)
```sh
RUN_DIR=$(python3 scripts/qa/new_run.py F-XX ios)
```
이전 실행 폴더는 고치지 않습니다. 재실행 = 새 폴더.

## 3. 부팅·빌드·설치
```sh
UDID=$(xcrun simctl list devices available | grep -m1 "iPhone 16 (" | grep -oE '[0-9A-F-]{36}')
xcrun simctl boot "$UDID" 2>/dev/null; open -a Simulator
xcrun simctl bootstatus "$UDID" -b
xcodebuild -project iosApp/iosApp.xcodeproj -scheme iosApp -configuration Debug \
  -destination "id=$UDID" -derivedDataPath build/ios build
xcrun simctl uninstall "$UDID" com.taekbugi.ios 2>/dev/null
xcrun simctl install "$UDID" build/ios/Build/Products/Debug-iphonesimulator/iosApp.app
xcrun simctl status_bar "$UDID" override --time 9:41 --batteryState charged --batteryLevel 100
```
앱 버전(`CFBundleShortVersionString`, `CFBundleVersion`)을 보고서 메타데이터에 적습니다:
`/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" build/ios/Build/Products/Debug-iphonesimulator/iosApp.app/Info.plist`

## 4. 조작 방법
| 목적 | 명령 |
|---|---|
| 앱 실행 | `xcrun simctl launch "$UDID" com.taekbugi.ios` |
| 클립보드 넣기 | `printf '운송장번호 000000000000' \| xcrun simctl pbcopy "$UDID"` |
| 딥링크 | `xcrun simctl openurl "$UDID" "<스킴>://..."` |
| 공유 확장 | Maestro로 메모 앱(또는 Safari)에서 텍스트 선택 → 공유 → 택부기. 흐름: `qa/maestro/ios/` |
| 탭·입력 | Maestro (`tapOn: { id: "<accessibilityIdentifier>" }`, `inputText`) |
| 스크린샷 | `xcrun simctl io "$UDID" screenshot $RUN_DIR/screenshots/NN-<장면>.png` |
| 다크 모드 | `xcrun simctl ui "$UDID" appearance dark` / `light` |
| 글씨 크기 | `xcrun simctl ui "$UDID" content_size extra-extra-large` / `large` |
| 알림 권한 | `xcrun simctl privacy "$UDID" grant notifications com.taekbugi.ios` (지원 버전에서) |
| 푸시 시뮬레이션 | `xcrun simctl push "$UDID" com.taekbugi.ios payload.json` (조용한 푸시 F-21은 API 이후) |
| 위젯 | 홈 화면 길게 누르기 → 편집 → 위젯 추가 (Maestro + 수동 단계 기록) |
| 로그 | `xcrun simctl spawn "$UDID" log show --last 10m --predicate 'subsystem BEGINSWITH "com.taekbugi"' > $RUN_DIR/raw/device.log` |
| 크래시 | `~/Library/Logs/DiagnosticReports/` 에서 `iosApp*` 최근 파일 |

테스트 데이터는 가짜 값만 씁니다.

## 5. Maestro 흐름 (회귀용, git으로 버전 관리)
- 위치 `qa/maestro/ios/F-XX-<slug>.yaml`, 머리 주석(`feature`, `spec`, `covers`, `changed`)과 `appId: com.taekbugi.ios` — 형식은 `qa-android` 스킬 6절과 같습니다.
- 이번 기능: `maestro --device "$UDID" test qa/maestro/ios/F-XX-*.yaml --test-output-dir $RUN_DIR/raw/maestro`
- 회귀: `maestro --device "$UDID" test qa/maestro/ios/ --test-output-dir $RUN_DIR/raw/regression`

## 6. 판정 · 7. 보고서 마무리
`qa-android` 스킬 7·8절과 같습니다 (스크린샷 직접 확인, 디자인 아트보드 비교, 공통 점검, 핵심 스크린샷 축소, INDEX 행 갱신, 시뮬레이터 설정 원복: `xcrun simctl status_bar "$UDID" clear`, 외형 light, 글씨 large).
