# In context bắt buộc cho agent (Cursor, Ollama, Claude API, ...)
# Usage: .\scripts\bootstrap-context.ps1
#        .\scripts\bootstrap-context.ps1 | Set-Clipboard

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

function Read-OrPlaceholder($path, $label) {
    if (Test-Path $path) {
        return Get-Content $path -Raw -Encoding UTF8
    }
    return "[$label not found: $path]"
}

$index = Read-OrPlaceholder ".ai-factory\knowledge\INDEX.md" "INDEX"
$protocol = Read-OrPlaceholder ".ai-factory\skills\session-protocol.md" "session-protocol"
$bootstrap = Read-OrPlaceholder "AGENT-BOOTSTRAP.md" "AGENT-BOOTSTRAP"

@"

=== AI FACTORY — BOOTSTRAP CONTEXT ===
Repo: $root

--- AGENT-BOOTSTRAP (tóm tắt) ---
$bootstrap

--- SESSION PROTOCOL ---
$protocol

--- KNOWLEDGE INDEX (đọc và tuân thủ) ---
$index

=== HẾT BOOTSTRAP — bắt đầu task bên dưới ===

"@
