FROM python:3.12.3-slim

WORKDIR /app

COPY weight_app.py .
COPY requirements.txt .
COPY index.html .
COPY weightdb.sql .
RUN mkdir -p /app/in /app/out

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV DATABASE_URL mysql://root:root@w-db/weight
CMD ["flask", "--app=weight_app.py", "run", "--host=0.0.0.0", "--port=5000"]

