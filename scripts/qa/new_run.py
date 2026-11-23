#!/usr/bin/env python3
"""QA 실행 폴더를 새로 만들고 버전 메타데이터가 채워진 보고서 초안을 만든다.

사용: python3 scripts/qa/new_run.py F-08 android
출력(stdout): 만든 실행 폴더 경로 한 줄 (예: docs/qa/reports/F-08/android/2026-12-01-r02)

- 실행 폴더는 기능·플랫폼별로 번호가 계속 올라갑니다. 이전 실행 폴더는 절대 고치지 않습니다.
- docs/qa/reports/INDEX.md 에 RUNNING 행을 추가합니다 (추가만, 기존 행 수정 없음).
- 보고서에 기록: 커밋, 작업 트리 변경 여부와 diff 해시, 명세 파일 해시, Maestro 흐름 파일별 해시.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "docs" / "qa" / "reports"
TEMPLATE = ROOT / "docs" / "qa" / "report-template.md"
INDEX = REPORTS / "INDEX.md"
PLATFORMS = {"android", "ios"}


def git(*args: str) -> str | None:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def working_tree_snapshot() -> str | None:
    """추적 안 된 파일까지 포함한 현재 작업 트리 내용의 git tree 해시 (실제 인덱스는 건드리지 않음).

    같은 내용이면 같은 해시가 나오므로, 커밋 전 상태에서 돌린 QA도 어떤 코드였는지 구분할 수 있다.
    """
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        added = subprocess.run(["git", "add", "-A"], cwd=ROOT, env=env, capture_output=True)
        if added.returncode != 0:
            return None
        tree = subprocess.run(["git", "write-tree"], cwd=ROOT, env=env, capture_output=True, text=True)
        return tree.stdout.strip()[:12] if tree.returncode == 0 else None


def file_hash(path: Path) -> str:
    return git("hash-object", str(path)) or hashlib.sha1(path.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not re.fullmatch(r"F-\d{2}", argv[0]) or argv[1] not in PLATFORMS:
        print("사용: python3 scripts/qa/new_run.py F-XX android|ios", file=sys.stderr)
        return 2
    feature, platform = argv

    today = dt.date.today().isoformat()
    platform_dir = REPORTS / feature / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    run_number = len([p for p in platform_dir.iterdir() if p.is_dir()]) + 1
    run_id = f"{today}-r{run_number:02d}"
    run_dir = platform_dir / run_id
    (run_dir / "screenshots").mkdir(parents=True)
    (run_dir / "raw").mkdir()

    head = git("rev-parse", "--short", "HEAD")
    porcelain = git("status", "--porcelain") or ""
    changed = [line for line in porcelain.splitlines() if line.strip()]
    untracked = [line for line in changed if line.startswith("??")]
    snapshot = working_tree_snapshot() or "계산 실패"
    commit = head or "커밋 없음"
    tree = (
        f"깨끗함 (tree {snapshot})"
        if not changed
        else f"변경 {len(changed)}개 (추적 안 된 파일 {len(untracked)}개), 작업 트리 스냅샷 tree {snapshot}"
    )

    specs = sorted((ROOT / "docs" / "features").glob(f"{feature}-*.md"))
    spec_line = ", ".join(f"`{p.relative_to(ROOT).as_posix()}` ({file_hash(p)[:12]})" for p in specs) or "명세 없음"

    flows = sorted((ROOT / "qa" / "maestro" / platform).glob("*.yaml"))
    flow_rows = "\n".join(
        f"| `{p.relative_to(ROOT).as_posix()}` | {file_hash(p)[:12]} | {'이번 기능' if p.name.startswith(feature) else '회귀'} |"
        for p in flows
    ) or "| (흐름 없음) | | |"

    template = TEMPLATE.read_text(encoding="utf-8")
    values = {
        "FEATURE": feature,
        "PLATFORM": platform,
        "RUN_ID": run_id,
        "DATE": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "COMMIT": commit,
        "TREE": tree,
        "SPEC": spec_line,
        "FLOWS": flow_rows,
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    (run_dir / "report.md").write_text(template, encoding="utf-8")

    if not INDEX.exists():
        INDEX.write_text(
            "# QA 실행 기록\n\n"
            "> 추가만 합니다. 실행이 끝나면 그 행의 결과 칸만 RUNNING → PASS/FAIL/BLOCKED 로 바꿉니다.\n\n"
            "| 실행 | 기능 | 플랫폼 | 결과 | 커밋 | 작업 트리 | 보고서 |\n"
            "|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    report_link = run_dir.relative_to(REPORTS).as_posix() + "/report.md"
    with INDEX.open("a", encoding="utf-8") as index:
        index.write(f"| {run_id} | {feature} | {platform} | RUNNING | {commit} | {'clean' if not changed else 'dirty'} tree {snapshot} | [보고서]({report_link}) |\n")

    print(run_dir.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
