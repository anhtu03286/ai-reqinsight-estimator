# Kiểm tra deterministic: review FAIL phải có lesson ID
# Usage: .\scripts\verify-knowledge-loop.ps1
# Exit 0 = OK, 1 = thiếu lesson

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$reviewsDir = Join-Path $root "docs\planning\reviews"
$issues = @()

if (-not (Test-Path $reviewsDir)) {
    Write-Host "OK: no docs/planning/reviews/"
    exit 0
}

Get-ChildItem $reviewsDir -Filter "*.md" -File | Where-Object { $_.Name -ne "README.md" } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $isFail = $content -match '(?i)\bFAIL\b|Request changes|blocking'
    $hasLesson = $content -match 'Lesson:\s*KL-[GP]-\d+'

    if ($isFail -and -not $hasLesson) {
        $issues += $_.FullName
    }
}

if ($issues.Count -gt 0) {
    Write-Host "FAIL: Review FAIL nhung thieu 'Lesson: KL-G-NNN' hoac 'KL-P-NNN':"
    $issues | ForEach-Object { Write-Host "  $_" }
    exit 1
}

Write-Host "OK: knowledge loop verify passed"
exit 0
