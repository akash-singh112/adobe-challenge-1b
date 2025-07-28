FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Update system packages for security
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip for latest features and security
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements-docker.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Create non-root user for security
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -u 1000 appuser && \
    chown -R appuser:appgroup /app
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1