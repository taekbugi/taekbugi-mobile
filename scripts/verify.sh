#!/usr/bin/env bash
# 저장소 전체 검증. 사용: scripts/verify.sh [--android-device] [--ios]
set -euo pipefail

cd "$(dirname "$0")/.."

ANDROID_DEVICE=false
IOS=false
for arg in "$@"; do
  case "$arg" in
    --android-device) ANDROID_DEVICE=true ;;
    --ios) IOS=true ;;
    *) echo "알 수 없는 옵션: $arg" >&2; exit 2 ;;
  esac
done

step() { printf '\n==> %s\n' "$1"; }

step "테스트 제어문 검사 (ADR-0005)"
python3 scripts/check_test_control_flow.py --all
echo "통과"

if [ -x ./gradlew ]; then
  step "Gradle check (ktlint · detekt · 단위/통합 테스트 · Kover)"
  ./gradlew check --continue

  if $ANDROID_DEVICE; then
    step "Android 기기 테스트 (켜진 에뮬레이터 필요)"
    adb get-state >/dev/null
    ./gradlew :androidApp:connectedDebugAndroidTest
  fi
else
  step "Gradle 래퍼 없음 — F-00 부트스트랩 전이라 건너뜀"
fi

if $IOS; then
  if [ -d iosApp ] && xcrun simctl help >/dev/null 2>&1; then
    step "iOS 테스트 (시뮬레이터)"
    xcodebuild test -project iosApp/iosApp.xcodeproj -scheme iosApp \
      -destination "platform=iOS Simulator,name=iPhone 16" -derivedDataPath build/ios | tail -n 40
  else
    step "iOS 건너뜀 — iosApp 없음 또는 Xcode(simctl) 사용 불가"
    exit 1
  fi
fi

step "모든 검증 통과"
