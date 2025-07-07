from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

def search_similar_chunks(embedding: list[float], k: int = 5) -> list[str]:
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX")

    search_client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key)
    )

    vector_query = VectorizedQuery(
       vector=embedding,
       fields="embedding",
       k_nearest_neighbors=k
    )

    results = search_client.search(
       search_text=None,
        vector_queries=[vector_query],
        top=k,
    )

    # Собираем найденные чанки
    return [doc["chunk"] for doc in results]
