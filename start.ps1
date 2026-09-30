# ULPF PowerShell Launcher
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  ULPF - Universal Log Pre-processing Framework" -ForegroundColor Cyan
Write-Host "  Opening at http://localhost:8000" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$env:PYTHONPATH = "src"

if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "[ULPF] Active runtime: .venv" -ForegroundColor Green
    & .venv\Scripts\python.exe -m main api
} else {
    Write-Host "[ULPF] Active runtime: Global Python" -ForegroundColor Yellow
    python -m main api
}
