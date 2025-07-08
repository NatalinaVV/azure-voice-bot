# search_indexing/embedding.py или где ты решишь оставить
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY_NEW")
#here we could change the model for more huge and better text-embedding-3-large
DEPLOYMENT_NAME = "text-embedding-3-small"
API_VERSION = "2023-05-15"
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_NEW")

def get_embedding(text: str):
    url = f"{OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/embeddings?api-version={API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY,
    }

    data = {
        "input": [text],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["data"][0]["embedding"]