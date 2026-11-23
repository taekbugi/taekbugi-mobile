# 0002. KMP 공유 범위와 iOS UI

- 상태: Proposed (Q-04 결정 필요)

## 배경
기획서는 iOS UI를 "SwiftUI(또는 Compose Multiplatform)"로 열어 두었습니다. WidgetKit·Share Extension·Live Activity는 어차피 SwiftUI가 필요합니다.

## 제안
- 공유: domain + data + **presentation(ViewModel·UiState)**. `androidx.lifecycle:lifecycle-viewmodel`의 KMP 버전을 씁니다.
- UI: Android는 Jetpack Compose + Glance, iOS는 **SwiftUI**.
- Swift 연동: **SKIE**로 `Flow` → `AsyncSequence`, sealed class → Swift enum, suspend → async 변환.
- 프레임워크: `:shared:umbrella`를 `isStatic = true`로 빌드, 앱·위젯·공유 확장에 링크.

## 대안
- Compose Multiplatform으로 iOS 앱 화면 공유: 화면 코드가 한 벌이지만 위젯·확장은 SwiftUI로 따로 필요하고, iOS 네이티브 감각(공유 시트, 붙여넣기 컨트롤)과 맞추는 비용이 있습니다.

## 결과
- 화면은 두 벌이지만 상태·규칙은 한 벌입니다. 화면 차이는 디자인 정본 기준으로만 둡니다.
