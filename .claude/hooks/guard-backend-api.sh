#!/usr/bin/env bash
# PreToolUse(Write|Edit|MultiEdit): 백엔드 API 문서(docs/api/specs/) 없이 서버 연동 코드를 만들지 못하게 막는다 (ADR-0006).
set -uo pipefail

file_path=$(jq -r '.tool_input.file_path // empty')
[ -z "$file_path" ] && exit 0

case "$file_path" in
  */shared/data/src/*/remote/server/*|shared/data/src/*/remote/server/*) ;;
  *) exit 0 ;;
esac

specs_dir="$CLAUDE_PROJECT_DIR/docs/api/specs"
spec_count=$(find "$specs_dir" -type f ! -name '.gitkeep' ! -name 'README.md' 2>/dev/null | wc -l | tr -d ' ')

if [ "$spec_count" = "0" ]; then
  cat >&2 <<'MSG'
차단: 백엔드 API 문서가 아직 없습니다 (docs/api/specs/ 비어 있음, ADR-0006).
서버 엔드포인트·필드·인증 방식을 추측해서 코드를 만들지 않습니다.
작업을 멈추고 사용자에게 API 문서가 필요하다고 보고하세요. 다른 경로로 우회하지 마세요.
MSG
  exit 2
fi
exit 0
