FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies required by OpenCV and RTMP/FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Make startup script executable and ensure proper permissions
RUN chmod +x start.sh && \
    ls -la start.sh

# Expose FastAPI port
EXPOSE 8000

# Default command - use bash to execute the script
CMD ["bash", "start.sh"]


