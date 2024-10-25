# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to avoid Python buffering issues
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /MercaditoNicaAIModels

# Copy only the requirements file first for better caching of dependencies
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application runs on
EXPOSE 80

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
