FROM python:3.11-slim

# Install mkvtoolnix
RUN apt update && apt install -y mkvtoolnix mkvtoolnix-gui

# Set working directory
WORKDIR /app

# Copy source code
COPY src/ ./src/

# Install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt
