#!/usr/bin/env bash
# Pre-tool hook: ensures config.json exists before running any MPV2 command.
# Only checks when the Bash command references src/main.py, src/cron.py, or
# the plugin's helper scripts.

set -euo pipefail

# Read the tool input from stdin
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")

# Only gate MPV2-related commands
if echo "$COMMAND" | grep -qE '(src/main\.py|src/cron\.py|claude-plugin/scripts/)'; then
  PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
  CONFIG="$PROJECT_ROOT/config.json"

  if [ ! -f "$CONFIG" ]; then
    echo '{"decision": "block", "reason": "config.json not found. Run: cp config.example.json config.json — then fill in required values (ollama_model, nanobanana2_api_key, firefox_profile)."}'
    exit 0
  fi
fi

# Allow all other commands
exit 0
