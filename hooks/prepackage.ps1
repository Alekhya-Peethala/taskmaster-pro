# TaskMaster Pro - AZD prepackage hook (Windows / PowerShell)
# Runs before 'azd package' builds the backend Docker image.
# Mirror of hooks/prepackage.sh for Windows runners.

$ErrorActionPreference = "Stop"

Write-Host "==> [prepackage] Validating backend package prerequisites..."

# Ensure the Dockerfile is present in the backend directory
if (-not (Test-Path "backend\Dockerfile")) {
    Write-Error "ERROR: backend\Dockerfile not found. Cannot package the backend service."
    exit 1
}

# Ensure the requirements file is present
if (-not (Test-Path "backend\requirements.txt")) {
    Write-Error "ERROR: backend\requirements.txt not found. Cannot package the backend service."
    exit 1
}

Write-Host "==> [prepackage] All prerequisites validated. Proceeding with Docker build."
