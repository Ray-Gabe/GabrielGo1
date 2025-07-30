# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all app files
COPY . /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional, needed for Flask)
EXPOSE 8000

# Start the app
CMD ["python", "main.py"]
