import os
import json
import requests
from dotenv import load_dotenv

# Загрузка .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX", "knowledge-index")

# Чтение схемы индекса
with open(os.path.join(os.path.dirname(__file__), "knowledge-index.json"), "r") as f:
    index_schema = json.load(f)

url = f"{endpoint}/indexes/{index_name}?api-version=2024-03-01-preview"
headers = {
    "Content-Type": "application/json",
    "api-key": key
}

print("🧠 Creating index via REST API...")

# Удаление старого индекса
delete_resp = requests.delete(url, headers=headers)
if delete_resp.status_code in (200, 204):
    print("⚠️ Old index removed")
elif delete_resp.status_code != 404:
    print("❗️ Error while removing indexes:")
    print(delete_resp.status_code, delete_resp.text)

# Создание нового индекса
response = requests.put(url, headers=headers, data=json.dumps(index_schema))
if response.status_code == 201:
    print("✅ Index created!")
else: 
    print("❌ Error:")
    print(response.status_code)
    print(response.text)