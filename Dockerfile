# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p build/graph build/report public/graph public/report

# Run tests to verify the installation
RUN python tests/run_tests.py

# Default command: run tests
CMD ["python", "tests/run_tests.py"]
