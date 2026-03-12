# TaskMaster Pro - AZD prepackage hook (Windows)
# Runs before 'azd package' builds the backend Docker image on Windows runners.
# Uses only relative paths; no host-machine-specific paths.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "==> [prepackage] Validating backend package prerequisites..."

# Ensure the Dockerfile is present in the backend directory
if (-not (Test-Path -Path (Join-Path "backend" "Dockerfile") -PathType Leaf)) {
    Write-Error "ERROR: backend/Dockerfile not found. Cannot package the backend service."
    exit 1
}

# Ensure the requirements file is present
if (-not (Test-Path -Path (Join-Path "backend" "requirements.txt") -PathType Leaf)) {
    Write-Error "ERROR: backend/requirements.txt not found. Cannot package the backend service."
    exit 1
}

Write-Host "==> [prepackage] All prerequisites validated. Proceeding with Docker build."
