import os
import uuid
import pandas as pd
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# Загрузка переменных
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

COSMOS_ENDPOINT = os.getenv("AZURE_COSMOSDB_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOSDB_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOSDB_DATABASE")
CONTAINER_NAME = os.getenv("AZURE_COSMOSDB_CONTAINER")

# Подключение к Cosmos
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = client.get_database_client(DATABASE_NAME)
container = db.get_container_client(CONTAINER_NAME)

print("COSMOS_ENDPOINT:", COSMOS_ENDPOINT)
print("COSMOS_KEY:", COSMOS_KEY[:4] + "..." + COSMOS_KEY[-4:] if COSMOS_KEY else "None")


def upload_csv(file_path: str, doc_type: str):
    print(f"📤 Загрузка {file_path} как type='{doc_type}'")

    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        doc = row.to_dict()
        doc["id"] = str(uuid.uuid4())
        doc["type"] = doc_type
        container.upsert_item(doc)

    print(f"✅ Загружено {len(df)} записей из {file_path}")


if __name__ == "__main__":
    upload_csv("data/faq_en.csv", "faq")
    upload_csv("data/services_en.csv", "service")
    upload_csv("data/doctors_en.csv", "doctor")
    upload_csv("data/locations_en.csv", "location")
