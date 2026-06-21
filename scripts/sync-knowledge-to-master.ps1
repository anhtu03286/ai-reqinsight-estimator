# Sync global lessons từ dự án hiện tại → repo template master (AgentV1)
# Usage: .\scripts\sync-knowledge-to-master.ps1 -MasterPath "D:\AI\5 Days\AgentV1"

param(
    [Parameter(Mandatory = $true)]
    [string]$MasterPath
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$srcLessons = Join-Path $projectRoot ".ai-factory\knowledge\global\lessons"
$dstLessons = Join-Path $MasterPath ".ai-factory\knowledge\global\lessons"
$srcIndex = Join-Path $projectRoot ".ai-factory\knowledge\INDEX.md"
$dstIndex = Join-Path $MasterPath ".ai-factory\knowledge\INDEX.md"

if (-not (Test-Path $MasterPath)) {
    Write-Error "MasterPath không tồn tại: $MasterPath"
}

New-Item -ItemType Directory -Force -Path $dstLessons | Out-Null

$copied = 0
if (Test-Path $srcLessons) {
    Get-ChildItem $srcLessons -File | ForEach-Object {
        $dest = Join-Path $dstLessons $_.Name
        if (-not (Test-Path $dest)) {
            Copy-Item $_.FullName $dest
            Write-Host "Copied: $($_.Name)"
            $copied++
        } else {
            Write-Host "Skip (exists): $($_.Name)"
        }
    }
}

Write-Host ""
Write-Host "Copied $copied new lesson file(s)."
Write-Host "Luu y: INDEX.md can merge thu cong hoac nhờ agent merge bang KL-ID."
Write-Host "Project INDEX: $srcIndex"
Write-Host "Master INDEX:  $dstIndex"
