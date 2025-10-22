#!/bin/bash
# A script to send the same prompt to multiple AI CLIs.

if [ -z "$1" ]; then
  echo "Usage: $0 \"Your question here\""
  exit 1
fi

PROMPT="$1"

echo "========================="
echo "🤖 Querying Claude..."
echo "========================="
# IMPORTANT: Replace 'claude' with the actual command for your Claude CLI.
claude -p "$PROMPT"

echo ""
echo "=========================
echo "🤖 Querying Codex..."
echo "========================="
codex e "$PROMPT"