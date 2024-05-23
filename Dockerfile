FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY import_data.py .
COPY attente_chromadb.sh .
COPY .env .

COPY data /app/data

RUN chmod +x attente_chromadb.sh

CMD ["./attente_chromadb.sh", "python", "import_data.py"]