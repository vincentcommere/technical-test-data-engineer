# micro-services/fastAPI/Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy FastAPI source code
COPY /src/moovitamix_fastapi /app

# Install dependencies
COPY micro-services/fastAPI/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
