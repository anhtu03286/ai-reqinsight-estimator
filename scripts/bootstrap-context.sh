#!/usr/bin/env bash
# In context bắt buộc cho agent (Ollama, Claude CLI, Linux/macOS, ...)
# Usage: ./scripts/bootstrap-context.sh
#        ollama run llama3 "$(./scripts/bootstrap-context.sh; echo 'Your task')"

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

read_or_placeholder() {
  local path="$1" label="$2"
  if [[ -f "$path" ]]; then
    cat "$path"
  else
    echo "[$label not found: $path]"
  fi
}

INDEX="$(read_or_placeholder .ai-factory/knowledge/INDEX.md INDEX)"
PROTOCOL="$(read_or_placeholder .ai-factory/skills/session-protocol.md session-protocol)"
BOOTSTRAP="$(read_or_placeholder AGENT-BOOTSTRAP.md AGENT-BOOTSTRAP)"

cat <<EOF
=== AI FACTORY — BOOTSTRAP CONTEXT ===
Repo: $ROOT

--- AGENT-BOOTSTRAP (tóm tắt) ---
$BOOTSTRAP

--- SESSION PROTOCOL ---
$PROTOCOL

--- KNOWLEDGE INDEX (đọc và tuân thủ) ---
$INDEX

=== HẾT BOOTSTRAP — bắt đầu task bên dưới ===
EOF
