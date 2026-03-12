# TaskMaster Pro - Backend Dockerfile
# Builds the FastAPI backend for Azure Container Apps deployment
# Uses only relative paths; no host-machine-specific paths required

FROM python:3.11-slim

WORKDIR /app

# Install OS-level build dependencies, then clean up to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose the default uvicorn port
EXPOSE 8000

# Run the application with uvicorn (production mode, no reload)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
