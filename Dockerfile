FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY .env .
COPY config.json .

COPY data /app/data

CMD ["python", "main.py"]