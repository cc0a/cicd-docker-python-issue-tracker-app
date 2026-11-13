FROM python:3.13-slim

# Prevent Python from generating bytecode
ENV PYTHONDONTWRITEBYTECODE=1

# Display application logs immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ ./app/

# Create persistent data directory
RUN mkdir -p /app/data

# Run as non-root user
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

# Application port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
