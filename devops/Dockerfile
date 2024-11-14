FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh
WORKDIR /app
COPY requirements.txt .
COPY webhook_listener.py .
COPY scripts ./scripts/
RUN pip install -r requirements.txt
RUN chmod +x scripts/*.py
EXPOSE 5000
CMD ["python", "webhook_listener.py"]