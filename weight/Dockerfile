FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# ENV FLASK_APP=app.py

ENTRYPOINT ["python", "app.py"]
# CMD ["flask", "run", "--host=0.0.0.0"]

# Use a lightweight Python base image
# FROM python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . /app/

# # Define the network port the container will listen on at runtime
# EXPOSE 8080

# # Start the application
# ENTRYPOINT ["python", "app.py"]

