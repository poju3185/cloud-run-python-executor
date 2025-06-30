# Dockerfile.cloudrun - Optimized for Cloud Run deployment

# Use lightweight Python image
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our application code
# Note: We will modify app/main.py to remove nsjail
COPY ./app /app/

# Set environment variables for Gunicorn to know which app to run
ENV APP_MODULE="main:app"
ENV PORT=8080

# Expose port 8080
EXPOSE 8080

# Start application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "main:app"] 