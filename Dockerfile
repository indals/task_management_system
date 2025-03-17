# Use a slim Python image for a smaller size
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (helps with caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (Modify in .env - better approach below)
# ENV FLASK_APP=run.py  # Not needed with wsgi:app
# ENV FLASK_ENV=development # Set in config.py
# ENV DEBUG=True  # Set in config.py

# Copy the .env file (if you have one) - Be careful with this in production!

# Set environment variables from .env (better than ENV in Dockerfile)
# If you don't have .env, comment the next line.

# Expose the Flask application port (default 5000)
EXPOSE 5000

# Production command (Gunicorn)
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--threads", "4", "--timeout", "30", "wsgi:app"]

# Development command (Flask) - Keep this for development
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"] # Better for dev