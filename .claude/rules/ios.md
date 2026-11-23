---
paths:
  - "iosApp/**"
  - "**/*.swift"
---

# iOS 규칙 (SwiftUI · WidgetKit · Share Extension)

## Swift
- Swift 6 언어 모드, strict concurrency. UI 상태 타입은 `@MainActor`.
- `struct`·`let` 우선, 강제 언래핑(`!`)·`try!` 금지.
- 공유 로직은 `Shared` 프레임워크(KMP)만 씁니다. Swift 쪽에 비즈니스 규칙(판별·주기·지연 판단)을 다시 구현하지 않습니다.
- KMP ViewModel은 SKIE가 만든 `AsyncSequence`로 구독해서 `@Observable` 래퍼에 연결합니다 (ADR-0002).

## SwiftUI
- 뷰는 상태를 그리고 동작을 전달만 합니다. 작은 뷰로 나누고 `#Preview`를 상태별로 둡니다.
- 색·글꼴·모서리·그림자는 `TaekbugiTokens`(값은 `docs/design/tokens.md`)에서만.
- 문자열은 String Catalog(`Localizable.xcstrings`), 디자인 문구 그대로. 이모지 금지, 택배사 로고 금지.
- 접근성: `accessibilityLabel`은 디자인의 `aria-label` 그대로. Dynamic Type 지원.
- QA용 `accessibilityIdentifier`를 주요 요소에 답니다.

## App Group · 확장
- 앱·위젯·공유 확장이 같은 App Group 컨테이너의 DB·임시 큐를 씁니다. 그 경로는 `Shared` 쪽 한 곳에서만 정합니다.
- 공유 확장: 메모리 제한(약 120MB)이 있으니 무거운 초기화 금지. 앱을 열지 않고 등록합니다(디자인 Share 화면). 로그인 전이면 임시 큐에 넣고 로그인 화면을 띄우지 않습니다(기획 0장).
- iOS 공유 확장은 택배사 **자동 판별만**. 후보 선택 UI를 만들지 않습니다(기획 0장).
- 위젯: Timeline Provider는 로컬 DB만 읽습니다. 데이터가 바뀌면 앱이 `WidgetCenter.shared.reloadAllTimelines()`.
- Live Activity는 G-02 결정 전 금지.

## 백그라운드
- `BGAppRefreshTask`는 최선 노력일 뿐입니다(Q-07). 조용한 푸시는 서버 API 문서 이후(F-21).

## 보안
- 암호화 키는 Keychain(`kSecAttrSynchronizable`로 iCloud 키체인, 접근 그룹 공유). `UserDefaults`에 비밀 값 금지.
- ATS 예외를 만들지 않습니다.
- 클립보드: `UIPasteboard.detectPatterns`로 먼저 확인하고 실제 읽기는 사용자 동작(`UIPasteControl`) 뒤에.
