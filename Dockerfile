# Change the base image to the specific version you want
FROM python:3.12.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your actual application code
COPY server_generator.py .

# Expose the port FastAPI runs on
EXPOSE 8000

# The command to start the server
CMD ["uvicorn", "server_generator:app", "--host", "0.0.0.0", "--port", "8000"]