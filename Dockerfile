# Use a lightweight Python base
FROM python:3.9-slim

# Install system dependencies for OpenCV (Updated for newer Debian)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages
RUN pip install --no-cache-dir fastapi uvicorn opencv-python-headless ultralytics python-multipart

COPY . .

# Unit 3: Port exposure
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]