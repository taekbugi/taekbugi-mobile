#!/usr/bin/env python3
"""테스트 코드의 제어문·반복문 사용을 찾아내는 검사 (ADR-0005).

사용:
  python3 scripts/check_test_control_flow.py --all          # 저장소의 모든 테스트 파일
  python3 scripts/check_test_control_flow.py <파일> [...]    # 지정 파일 (테스트 파일이 아니면 무시)

종료 코드: 0 = 위반 없음, 1 = 위반 있음.
대상: Kotlin 테스트 소스셋(src/*Test/, src/test/, src/androidTest/)과 Swift 테스트 타깃(*Tests/).
Fake·테스트 데이터 빌더는 shared/testing/src/commonMain 에 두며 이 검사 대상이 아닙니다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "build", ".gradle", ".idea", "node_modules", "DerivedData", ".kotlin", "Pods"}

KOTLIN_TEST_PATH = re.compile(r"(^|/)src/([A-Za-z]+Test|test|androidTest)/")
SWIFT_TEST_PATH = re.compile(r"(^|/)[^/]*Tests/")

KOTLIN_RULES = [
    (r"\bif\s*\(", "if"),
    (r"\belse\b", "else"),
    (r"\bwhen\s*[({]", "when"),
    (r"\bfor\s*\(", "for"),
    (r"\bwhile\s*\(", "while"),
    (r"\bdo\s*\{", "do"),
    (r"\.forEach(Indexed)?\s*[({]", "forEach"),
    (r"\brepeat\s*\(", "repeat"),
    (r"\btry\s*\{", "try"),
    (r"\bcatch\s*\(", "catch"),
    (r"\?:", "엘비스 ?:"),
    (r"\?\.let\b", "?.let"),
    (r"\.takeIf\b", "takeIf"),
    (r"\.takeUnless\b", "takeUnless"),
    (r"\bwithData\b", "데이터 주도 테스트 withData"),
    (r"@ParameterizedTest\b", "데이터 주도 테스트 @ParameterizedTest"),
    (r"\bThread\.sleep\b", "Thread.sleep (비결정적)"),
    (r"\bSystem\.currentTimeMillis\b", "System.currentTimeMillis (FixedClock 사용)"),
    (r"\bClock\.System\b", "Clock.System (FixedClock 사용)"),
    (r"\bRandom\b", "Random (비결정적)"),
]

SWIFT_RULES = [
    (r"\bif\s", "if"),
    (r"\bguard\s", "guard"),
    (r"\belse\b", "else"),
    (r"\bswitch\s", "switch"),
    (r"\bfor\s", "for"),
    (r"\bwhile\s", "while"),
    (r"\brepeat\s*\{", "repeat"),
    (r"\.forEach\s*[({]", "forEach"),
    (r"\?\?", "?? 기본값"),
    (r"\bdo\s*\{", "do-catch"),
    (r"\bcatch\b", "catch"),
    (r"@Test\s*\(.*\barguments\s*:", "데이터 주도 테스트 @Test(arguments:)"),
    (r"\bsleep\s*\(", "sleep (비결정적)"),
    (r"\bThread\.sleep\b", "Thread.sleep (비결정적)"),
]


def _blank_keep_newlines(match: re.Match[str]) -> str:
    return "\n" * match.group(0).count("\n")


def strip_comments_and_strings(source: str) -> list[str]:
    """주석과 문자열 리터럴을 지워서 그 안의 단어가 오탐되지 않게 한다. 줄 번호는 유지한다."""
    source = re.sub(r'"""[\s\S]*?"""', _blank_keep_newlines, source)
    source = re.sub(r"/\*[\s\S]*?\*/", _blank_keep_newlines, source)
    lines = []
    for line in source.split("\n"):
        line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
        line = re.sub(r"//.*$", "", line)
        lines.append(line)
    return lines


def rules_for(rel_path: str):
    if rel_path.endswith((".kt", ".kts")) and KOTLIN_TEST_PATH.search(rel_path):
        return KOTLIN_RULES
    if rel_path.endswith(".swift") and SWIFT_TEST_PATH.search(rel_path):
        return SWIFT_RULES
    return None


def check_file(path: Path) -> list[str]:
    try:
        rel = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rel = path.as_posix()
    rules = rules_for(rel)
    if rules is None or not path.is_file():
        return []
    violations = []
    lines = strip_comments_and_strings(path.read_text(encoding="utf-8", errors="replace"))
    for number, line in enumerate(lines, start=1):
        for pattern, label in rules:
            if re.search(pattern, line):
                violations.append(f"{rel}:{number}: 테스트 코드 금지 구문 [{label}] → {line.strip()}")
    return violations


def all_candidate_files() -> list[Path]:
    result = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in {".kt", ".kts", ".swift"}:
            result.append(path)
    return result


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    files = all_candidate_files() if argv == ["--all"] else [Path(a) for a in argv]
    violations = [v for f in files for v in check_file(f)]
    if violations:
        print("\n".join(violations))
        print(
            f"\n위반 {len(violations)}건. 테스트에는 제어문·반복문을 쓰지 않습니다 (ADR-0005).\n"
            "케이스마다 테스트 함수를 나누고, assertFailsWith / assertNotNull / assertIs 를 쓰세요.\n"
            "분기가 필요한 Fake는 shared/testing/src/commonMain 으로 옮깁니다."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
