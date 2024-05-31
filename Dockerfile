FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY attente_chromadb.sh .
COPY .env .
COPY config.json .

COPY data /app/data

RUN chmod +x attente_chromadb.sh

CMD ["./attente_chromadb.sh", "python", "main.py"]