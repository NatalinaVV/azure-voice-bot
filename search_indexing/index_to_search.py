import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from search_indexing.chunking import split_text
from search_indexing.embedding import get_embedding

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# CosmosDB config
COSMOS_ENDPOINT = os.getenv("AZURE_COSMOSDB_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOSDB_KEY")
COSMOS_DB = os.getenv("AZURE_COSMOSDB_DATABASE")
COSMOS_CONTAINER = os.getenv("AZURE_COSMOSDB_CONTAINER")

# Azure Search config
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

# Init clients
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_container = cosmos_client.get_database_client(COSMOS_DB).get_container_client(COSMOS_CONTAINER)
search_client = SearchClient(SEARCH_ENDPOINT, SEARCH_INDEX, AzureKeyCredential(SEARCH_KEY))


def prepare_documents():
    print("📦 Reading data from Cosmos DB...")
    documents = list(cosmos_container.read_all_items())
    print(f"🔍 Find docs: {len(documents)}")

    search_documents = []

    for doc in documents:
        doc_id = doc.get("id")
        doc_type = doc.get("type", "").lower()
        base_text = ""

        if doc_type == "faq":
            q = doc.get("Question", "").strip()
            a = doc.get("Answer", "").strip()
            base_text = f"{q}\n{a}"
        elif doc_type == "service":
            name = doc.get("Name", "").strip()
            desc = doc.get("Description", "").strip()
            base_text = f"{name}\n{desc}"
        elif doc_type == "doctor":
            name = doc.get("Name", "").strip()
            spec = doc.get("Specialty", "").strip()
            base_text = f"{name}\n{spec}"
        elif doc_type == "location":
            name = doc.get("Name", "").strip()
            address = doc.get("Address", "").strip()
            phone = doc.get("Phone", "").strip()
            base_text = f"{name}\n{address}\n{phone}"
        else:
            continue  # неизвестный тип — пропустить

        chunks = split_text(base_text)

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            search_documents.append({
                "id": f"{doc_id}-{i}",
                "chunk": chunk,
                "type": doc_type,
                "embedding": embedding
            })

    return search_documents


def upload_to_search(docs):
    print(f"🚀 Sending {len(docs)} docs in Azure Search...")
    result = search_client.upload_documents(documents=docs)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"✅ Success uploaded: {succeeded} docs")


if __name__ == "__main__":
    docs = prepare_documents()
    upload_to_search(docs)