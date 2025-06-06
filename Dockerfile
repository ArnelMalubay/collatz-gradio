FROM python:3.13-slim

# Install dependencies (FFmpeg + basic tools)
RUN apt-get update && apt-get install -y ffmpeg

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add your app files
COPY . /app
WORKDIR /app

# Command to run your script or Gradio app
CMD ["python", "main.py"]
