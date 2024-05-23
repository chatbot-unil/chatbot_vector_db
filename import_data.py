
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

collection = chroma_client.create_collection(name="annuaire_statistique", embedding_function=openai_ef)

autumn_students_data = "data/students_autumn/student_enrollment_by_faculty_2011_2021.json"

def process_json_files(file_paths):
	documents = []

	for file_path in file_paths:
		with open(file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
			context = data.get('context', '')
			for year, faculties in data.get('data', {}).items():
				for faculty, stats in faculties.items():
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
	
	print(f"Ajout de {len(documents)} documents dans la collection {collection.name}")

process_json_files([autumn_students_data])

glossary = "data/glossary/glossary.txt"

def process_glossary(file_path):
	documents = []

	with open(file_path , 'r', encoding='utf-8') as f:
		data = f.read()
		documents.append(Document(page_content=data, metadata={"context": "c'est donnée contient des définitions (glossaire) de l'annuaire statistique de l'Université de Lausanne"}))
	
	for doc in documents:
		collection.add(
			ids=[str(uuid.uuid1())],
			metadatas=[doc.metadata],
			documents=[doc.page_content]
		)
	
	print(f"Ajout de {len(documents)} documents dans la collection {collection.name}")

process_glossary(glossary)

autumn_students_data_by_domicile = "data/students_autumn/student_enrollment_by_domicile_2011_2021.json"

def process_json_files(file_paths):
    documents = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            context = data.get('context', '')
            for category, faculties in data.get('data', {}).items():
                for faculty, stats in faculties.items():
                    for year, value in enumerate(stats, start=2011):
                        document_content = json.dumps({
                            "year": year,
                            "faculty": faculty,
                            "category": category,
                            "value": value
                        }, ensure_ascii=False)
                        metadata = {
                            "context": context,
                            "year": year,
                            "faculty": faculty,
                            "category": category
                        }
                        documents.append(Document(page_content=document_content, metadata=metadata))

    for doc in documents:
        collection.add(
            ids=[str(uuid.uuid1())],
            metadatas=[doc.metadata],
            documents=[doc.page_content]
        )

    print(f"Ajout de {len(documents)} documents dans la collection {collection.name}")

process_json_files([autumn_students_data_by_domicile])