# Use Python 3.13 slim as the base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app folder
COPY app/ .

# Expose Gradio's default port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
