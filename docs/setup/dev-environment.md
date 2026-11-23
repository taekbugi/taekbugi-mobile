# 개발 환경

## 필요한 것
| 도구 | 용도 | 확인 |
|---|---|---|
| JDK 21 (Homebrew `openjdk@21`. 26도 설치돼 있지만 Gradle·AGP 호환을 위해 LTS 21 사용) | Gradle | `java -version` |
| Android Studio + SDK (platform 35, build-tools, emulator, platform-tools) | Android 빌드·에뮬레이터 | `adb version`, `emulator -list-avds` |
| Xcode (최신 정식) — Command Line Tools만으로는 시뮬레이터 불가 | iOS 빌드·시뮬레이터 | `xcrun simctl list devices` |
| Python 3 | 테스트 제어문 검사 스크립트·훅 | `python3 --version` |
| jq | Claude Code 훅 | `jq --version` |
| Maestro (권장) | QA 에이전트의 화면 조작 자동화 | `maestro --version` |

## macOS 설정 예
```sh
# ~/.zshrc
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"   # Homebrew openjdk@21 (keg-only라 직접 지정)
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"

# Xcode: App Store 또는 `brew install mas && mas get 497799835`
# 설치 후 (Command Line Tools가 선택돼 있으면 simctl이 없음)
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license accept
xcodebuild -runFirstLaunch
xcodebuild -downloadPlatform iOS   # iOS 시뮬레이터 런타임

# Maestro
curl -fsSL "https://get.maestro.mobile.dev" | bash
```

## QA용 AVD 만들기
```sh
sdkmanager "system-images;android-35;google_apis;arm64-v8a"
avdmanager create avd -n taekbugi_api35 -k "system-images;android-35;google_apis;arm64-v8a" -d pixel_8
```
Intel Mac이면 `x86_64` 이미지를 씁니다.

## 비밀 값
- `local.properties`, `*.keystore`, `*.jks`, `.env`, 카카오 앱 키, 우체국 서비스 키, 레시피 서명 비밀키는 **커밋하지 않습니다.** (`.gitignore`)
- 빌드에 필요한 키는 `local.properties` 또는 환경 변수에서 읽고, 없으면 빌드가 분명한 오류를 내게 합니다.
