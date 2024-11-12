# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy

# Copy the rest of the Django project code
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/static /app/media

# Create and switch to non-root user for security
RUN useradd -m django
RUN chown -R django:django /app /app/static /app/media
USER django

# Remove the CMD since it's specified in docker-compose.yml
# This allows for different commands in development and production