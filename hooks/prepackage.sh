#!/bin/sh
# TaskMaster Pro - AZD prepackage hook
# Runs before 'azd package' builds the backend Docker image.
# Uses POSIX sh so it works on any Linux/macOS runner without Windows paths.

set -e

echo "==> [prepackage] Validating backend package prerequisites..."

# Ensure the Dockerfile is present in the backend directory
if [ ! -f "backend/Dockerfile" ]; then
  echo "ERROR: backend/Dockerfile not found. Cannot package the backend service."
  exit 1
fi

# Ensure the requirements file is present
if [ ! -f "backend/requirements.txt" ]; then
  echo "ERROR: backend/requirements.txt not found. Cannot package the backend service."
  exit 1
fi

echo "==> [prepackage] All prerequisites validated. Proceeding with Docker build."
