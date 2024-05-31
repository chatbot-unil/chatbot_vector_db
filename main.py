import chromadb
import os
from dotenv import load_dotenv
import chromadb.utils.embedding_functions as embedding_functions
import json
import uuid
from langchain.schema import Document
import logging

logging_level = os.getenv("LOGGING_LEVEL", "DEBUG")

if logging_level == "DEBUG":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
elif logging_level == "INFO":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

load_dotenv()

config_path = 'config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

chroma_host = os.getenv("CHROMADB_HOST", "localhost")
chroma_port = int(os.getenv("CHROMADB_PORT", 3003))

def pretty_print(json_data):
    return json.dumps(json_data, indent=4, ensure_ascii=False)

def convert_value(value, target_type):
    conversion_functions = {
        'integer': lambda x: int(x),
        'float': lambda x: float(x),
        'boolean': lambda x: bool(x),
        'string': lambda x: str(x)
    }
    try:
        return conversion_functions[target_type](value)
    except (ValueError, TypeError, KeyError):
        return None

def process_flat_file(data, file_config, context):
    documents = []
    root_key = file_config.get('root_key')
    
    for key, value in data[root_key].items():
        metadata = {'context': context}
        document_content = {key: value}
        documents.append(Document(page_content=json.dumps(document_content, ensure_ascii=False), metadata=metadata))
        logger.debug(f"Contenu du document: {pretty_print(document_content)}")
        logger.debug(f"Métadonnées: {pretty_print(metadata)}")

    return documents

def process_nested_file(data, file_config, context):
    documents = []
    root_key = file_config.get('root_key')
    nested_structure = file_config.get('nested_structure', [])
    metadata_keys = [item['key'] for item in nested_structure if item.get('add_to_metadata')]
    logger.info(f"Ajout de documents à partir de la clé racine {root_key } et de la structure imbriquée {nested_structure}")

    for root_item, nested_data in data[root_key].items():
        for nested_key, nested_values in nested_data.items():
            metadata = {}
            document_content = {}

            for level in nested_structure:
                key = level['key']
                if level.get('is_root'):
                    value = root_item
                else:
                    value = nested_key
                
                if key in metadata_keys:
                    metadata[key] = value
                document_content[key] = value

                if 'fields' in level:
                    for field in level['fields']:
                        print(f"Field: {field}")
                        field_name = field['name']

                        if isinstance(nested_values, dict):
                            field_value = nested_values.get(field_name, None)
                        elif isinstance(nested_values, list):
                            try:
                                field_value = nested_values[int(field_name)]
                            except (IndexError, ValueError):
                                field_value = None
                        else:
                            field_value = convert_value(nested_values, field['type'])
                        
                        document_content[field_name] = field_value
                        if field_name in metadata_keys:
                            metadata[field_name] = field_value

            metadata['context'] = context
            documents.append(Document(page_content=json.dumps(document_content, ensure_ascii=False), metadata=metadata))
            logger.debug(f"Contenu du document: {pretty_print(document_content)}")
            logger.debug(f"Métadonnées: {pretty_print(metadata)}")

    return documents

def process_file(file_config, collection):
    documents = []
    file_path = file_config['path']
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            context = data.get('context', '')

            if file_config.get('structure') == 'nested':
                documents = process_nested_file(data, file_config, context)

            elif file_config.get('structure') == 'flat':
                documents = process_flat_file(data, file_config, context)
        
        for doc in documents:
            collection.upsert(
                ids=[str(uuid.uuid1())],
                metadatas=[doc.metadata],
                documents=[doc.page_content]
            )
        
        logger.info(f"Ajout de {len(documents)} documents à la collection {collection.name}")

    except Exception as e:
        logger.error(f"Erreur lors du traitement du fichier {file_path}: {str(e)}")

def process_files(file_configs, collection):
    for file_config in file_configs:
        process_file(file_config, collection)

if __name__ == "__main__":
    try:
        chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name=config["embedding_model"])
        
        for collection_config in config["collections"]:
            collection = chroma_client.get_or_create_collection(name=collection_config["name"], embedding_function=openai_ef)
            process_files(collection_config["files"], collection)

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du script: {str(e)}")
