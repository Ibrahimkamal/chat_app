# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
