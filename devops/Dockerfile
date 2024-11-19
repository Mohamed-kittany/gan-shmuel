FROM python:3.9-slim-buster
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
RUN curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '\"tag_name\": \"\K[^\"]*')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose
WORKDIR /app
# COPY ../../../.env.test .env.test
# COPY ../../../.env.prod .env.prod
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY webhook_listener.py .
COPY scripts .
EXPOSE 5000
CMD ["python", "webhook_listener.py"]