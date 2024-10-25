# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to avoid Python buffering issues
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /MercaditoNicaAIModels

# Copy only the requirements file first for better caching of dependencies
COPY requirements.txt .

# Install Rust and Cargo, and Python dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    . "$HOME/.cargo/env" && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Update PATH for Rust to ensure it's available for all sessions
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the specific CSV file into the container
COPY api/endpoints/asistente.csv api/endpoints/asistente.csv

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application runs on
EXPOSE 80

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
