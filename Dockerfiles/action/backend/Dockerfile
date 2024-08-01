# Dockerfiles/backend/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/
CMD ["gunicorn","core.wsgi","--bind","0.0.0.0:4001"]
CMD ["python","manage.py","makemigrations"]
CMD ["python","manage.py","migrate"]
