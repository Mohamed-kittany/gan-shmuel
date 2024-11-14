# Use the official Python slim image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local app code to the container
COPY ./app /app

# Install Flask
RUN pip install --no-cache-dir flask

# Expose the port the app will run on
EXPOSE 5000

# Set environment variable for Flask app
ENV FLASK_APP=app.py

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

