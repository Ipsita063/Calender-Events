# Use the official Python image with a slim version
FROM python:3.12-slim

# Copy requirements file and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY app/ app/

# Create an empty db directory inside the container if not present
RUN mkdir -p /app/db

# Set the working directory
WORKDIR /app

# Set PYTHONPATH to the current working directory
ENV PYTHONPATH="/"

# Expose the application port
EXPOSE 8000

# Run the application with uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
