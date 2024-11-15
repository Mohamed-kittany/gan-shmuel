# Use the official Python slim image
FROM python:3.9-slim
# Set the working directory inside the container
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app ./
EXPOSE 5000

# Set environment variable for Flask app
ENV FLASK_APP=app.py

# Command to run the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
