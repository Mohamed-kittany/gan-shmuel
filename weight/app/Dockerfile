FROM python:3.12.3-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app=weight_app.py", "run", "--host=0.0.0.0", "--port=5000"]