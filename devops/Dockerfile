FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY webhook_listener.py .
COPY scripts .
EXPOSE 5000
CMD ["python", "webhook_listener.py"]