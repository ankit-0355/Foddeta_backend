FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (optional; Cloud Run doesn’t strictly need this)
EXPOSE 8080

# Command to run FastAPI
# Use the PORT environment variable provided by Cloud Run
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
