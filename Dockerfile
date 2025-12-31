# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code directory (including the model files) into the container
COPY src/ ./src/

# Expose port 8000 for the API
EXPOSE 8000

# Define environment variable to ensure output is flushed immediately
ENV PYTHONUNBUFFERED=1

# Run the command to start the API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
