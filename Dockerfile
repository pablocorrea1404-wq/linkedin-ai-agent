# Lightweight Python 3.12 runtime
FROM python:3.12-slim

# Set environment variables for optimal container execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and entry points
COPY . .

# Entrypoint
CMD ["python", "main.py"]
