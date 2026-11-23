# 기능 백로그

> 상태: `TODO` · `IN_PROGRESS` · `IN_QA` · `DONE`(QA PASS 후에만) · `BLOCKED_GAP`(기획↔디자인 불일치 결정 대기) · `BLOCKED_API`(API 문서 대기) · `BLOCKED_Q`(확정 필요 항목 대기)
> 한 번에 한 기능만 `IN_PROGRESS`로 둡니다. 순서는 의존 관계 기준 제안이며 사용자가 바꿀 수 있습니다.
> 명세 파일: `docs/features/F-XX-<slug>.md` (`_template.md` 복사)

| ID | 기능 | 플랫폼 | 선행 | 막힘 | 상태 | 명세 | QA 보고서 |
|---|---|---|---|---|---|---|---|
| F-00 | 프로젝트 부트스트랩: Gradle KMP 골격, build-logic, 버전 카탈로그, detekt·ktlint·Kover, `:shared:testing`·`:shared:architecture-test`, iOS 프로젝트 + 정적 프레임워크, CI, 빈 화면 실행 | 공통 | — | Q-04, Q-05 확인 | TODO | | |
| F-01 | 도메인 모델 + 송장번호 추출·택배사 후보 판별(자릿수·체크섬) | 공통 | F-00 | | TODO | | |
| F-02 | 레시피 해석기: 형식 초안, 서명 검증(Ed25519), 도메인 허용 목록, `min_interpreter_version`, 번들 레시피 로더, 마지막 성공 캐시 | 공통 | F-01 | Q-06 | TODO | | |
| F-03 | 택배사 레시피 5종 (우체국·CJ·롯데·한진·로젠) + 골든 테스트 | 공통 | F-02 | Q-03(우체국) | TODO | | |
| F-04 | 로컬 저장소(SQLDelight) + 로그인 전 임시 보관 큐 | 공통 | F-01 | G-14(안내 화면) | TODO | | |
| F-05 | 스플래시 (산타 스킨) | Android · iOS | F-00 | G-12 | BLOCKED_GAP | | |
| F-06 | 온보딩 · 로그인 화면 (Apple · 카카오 · 이메일 진입) — 화면만, 서버 연동 제외 | Android · iOS | F-00 | Q-08, 서버 연동은 API | TODO | | |
| F-07 | 이메일 가입 3단계 + 약관 동의 화면 — 화면·입력 검증만 | Android · iOS | F-06 | G-09, G-10, G-11, 서버 연동은 API | BLOCKED_GAP | | |
| F-08 | Android 드래그 등록: PROCESS_TEXT "택배 추적" + 등록 시트(후보 선택·별칭) + 앱 실행 시 클립보드 감지 | Android | F-01, F-04 | G-04, G-14, G-17 | BLOCKED_GAP | | |
| F-09 | iOS 공유 확장 등록 + `detectPatterns` 클립보드 감지 + `UIPasteControl` + 뒷면 탭 단축어 | iOS | F-01, F-04 | G-04, G-13, G-14, G-17 | BLOCKED_GAP | | |
| F-10 | 홈(내 택배: 진행 중/완료, 히어로 카드) + 택배 상세(별칭 편집, 송장 복사, 배송 기록) + 삭제 | Android · iOS | F-03, F-04 | G-03, G-06, G-16, G-17 | BLOCKED_GAP | | |
| F-11 | 자동 추적 스케줄링 (Android WorkManager, iOS BGAppRefresh) | Android · iOS | F-03, F-04 | G-05, Q-07, iOS 조용한 푸시는 API | BLOCKED_GAP | | |
| F-12 | Android Glance 위젯 (4×2 · 2×2) | Android | F-10, F-11 | G-03, G-06, G-18 | BLOCKED_GAP | | |
| F-13 | iOS WidgetKit 위젯 (소·중·대) + Live Activity | iOS | F-10, F-11 | G-02, G-03, G-18 | BLOCKED_GAP | | |
| F-14 | 조회 지연 알림 (기기 판단 → 로컬 알림) | Android · iOS | F-11 | G-01, G-03, Q-02 | BLOCKED_GAP | | |
| F-15 | 완료 택배 정리 [N]일 | 공통 | F-04 | G-15, Q-01 | BLOCKED_Q | | |
| F-16 | 설정 화면 (알림 토글, 정리 기간, 개인정보처리방침, 버전) | Android · iOS | F-14, F-15 | G-01, G-07, G-08, G-09, G-10 | BLOCKED_GAP | | |
| F-17 | 계정 삭제 | Android · iOS | F-16 | G-16, API | BLOCKED_API | | |
| F-18 | 내 택배 동기화 (tracking_hmac·ciphertext, tombstone, 암호화 키 보관) | 공통 | F-04 | API | BLOCKED_API | | |
| F-19 | 로그인·인증 연동 (Apple · 카카오 · 이메일 코드), 로그인 후 임시 큐 등록 | 공통 | F-06, F-07 | API | BLOCKED_API | | |
| F-20 | 레시피 서버 수신 + 성공/실패 지표 보고 | 공통 | F-02 | API | BLOCKED_API | | |
| F-21 | iOS 조용한 푸시 수신 → 백그라운드 조회 | iOS | F-11 | API | BLOCKED_API | | |

## 지금 바로 시작할 수 있는 순서
F-00 → F-01 → F-02 → F-03 / F-04 (병렬 가능) → F-06

나머지는 `docs/product/spec-design-gaps.md`, `docs/product/open-questions.md` 결정과 API 문서 도착에 따라 풀립니다.
