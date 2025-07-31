# Use a slim Python image based on Debian
FROM python:3.10-slim

# Install system dependencies (including Tesseract)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit server
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
