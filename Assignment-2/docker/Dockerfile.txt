# Dockerfile for Flask application
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
