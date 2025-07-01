FROM python:3.11-slim

# Install mkvtoolnix
RUN apt update && apt install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy source code
COPY src/ ./

# Install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run main.py with no buffering for stdout
CMD ["python", "-u", "main.py"]
