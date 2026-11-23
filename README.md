# 택부기 (mobile)

**택부기 – 드래그하면 추적되는 택배 위젯.** 송장번호를 선택하면 택배사를 판별해 등록하고, 택부기가 대신 지켜보며 위젯으로 알려 주는 Android·iOS 앱입니다.

> 현재 상태: 개발 준비 단계 (에이전트 작업 흐름·규칙·문서만 있음). 코드는 F-00 부트스트랩부터 시작합니다.

## 구성
- Kotlin Multiplatform 공유 로직 (Clean Architecture: domain · data · presentation)
- Android: Jetpack Compose + Glance 위젯 + WorkManager + PROCESS_TEXT
- iOS: SwiftUI + WidgetKit + Share Extension

## 시작하기
1. 개발 환경: [`docs/setup/dev-environment.md`](docs/setup/dev-environment.md)
2. 문서 지도: [`docs/README.md`](docs/README.md)
3. 기능 목록: [`docs/features/backlog.md`](docs/features/backlog.md)

## 검증
```sh
scripts/verify.sh            # 테스트 제어문 검사 + Gradle check
scripts/verify.sh --ios      # + iOS 테스트
```

## AI 에이전트로 개발하기
- 공통 지침: [`AGENTS.md`](AGENTS.md) · Claude Code: [`CLAUDE.md`](CLAUDE.md)
- 기능 하나 진행: Claude Code에서 `/feature-dev F-01`
- 흐름 설명: [`docs/workflow/agentic-workflow.md`](docs/workflow/agentic-workflow.md)

## 디자인
정본: Claude Design 캔버스 「택부기 앱 디자인」 — 요약은 [`docs/design/`](docs/design/)
