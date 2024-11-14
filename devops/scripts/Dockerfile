FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app/ ./
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
