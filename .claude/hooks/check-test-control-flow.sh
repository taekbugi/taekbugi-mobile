#!/usr/bin/env bash
# PostToolUse(Write|Edit|MultiEdit): 테스트 파일을 저장하면 제어문 검사를 돌리고, 위반이 있으면 Claude에게 되돌려 보낸다.
set -uo pipefail

file_path=$(jq -r '.tool_input.file_path // empty')
[ -z "$file_path" ] && exit 0

case "$file_path" in
  *.kt|*.kts|*.swift) ;;
  *) exit 0 ;;
esac

output=$(python3 "$CLAUDE_PROJECT_DIR/scripts/check_test_control_flow.py" "$file_path" 2>&1)
status=$?
if [ $status -ne 0 ]; then
  echo "$output" >&2
  exit 2
fi
exit 0
