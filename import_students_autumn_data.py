import chromadb
import os
from dotenv import load_dotenv
import chromadb.utils.embedding_functions as embedding_functions
import json
import uuid

from langchain.schema import Document

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

chroma_host = os.getenv("CHROMADB_HOST")
chroma_port = int(os.getenv("CHROMADB_PORT"))

chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small")

collection = chroma_client.create_collection(name="students_autumn_2011_2021", embedding_function=openai_ef)

files = [
    "data/students_autumn/FBM.json",
    "data/students_autumn/FCUE.json",
    "data/students_autumn/FDCA.json",
    "data/students_autumn/FGSE.json",
    "data/students_autumn/FTSR.json",
    "data/students_autumn/HEC.json",
    "data/students_autumn/Lettres.json",
    "data/students_autumn/SSP.json",
    "data/students_autumn/TOTAL.json",
]

def process_json_files(file_paths):
    documents = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            context = data.get('context', '')
            for year, content in data.get('data', {}).items():
                for faculty, stats in content.items():
                    document_content = json.dumps({
                        "year": year,
                        "faculty": faculty,
                        "stats": stats
                    }, ensure_ascii=False)
                    metadata = {
                        "context": context,
                        "year": year,
                        "faculty": faculty
                    }
                    documents.append(Document(page_content=document_content, metadata=metadata))

    for doc in documents:
        collection.add(
            ids=[str(uuid.uuid1())],
            metadatas=[doc.metadata],
            documents=[doc.page_content]
        )
    
    return documents

documents = process_json_files(files)

print(f"Ajout de {len(documents)} documents dans la collection {collection.name}")