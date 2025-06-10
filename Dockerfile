FROM python:3.11-slim

# Install mkvtoolnix
RUN apt update && apt install -y mkvtoolnix mkvtoolnix-gui

# Install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt
