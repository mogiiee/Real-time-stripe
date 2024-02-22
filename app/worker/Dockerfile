# app/worker/Dockerfile

# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the necessary directories and files into the container at /app
COPY app/worker /app/worker
COPY app /app/app
COPY requirements.txt /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Celery worker
CMD ["celery", "-A", "worker.celery_worker", "worker", "--loglevel=info"]
