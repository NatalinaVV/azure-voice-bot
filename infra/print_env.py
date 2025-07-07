
python
Copy
Edit
import os
from dotenv import load_dotenv

# Если используешь .env — раскомментируй:
# load_dotenv()

keys = [
    "AZURE_COSMOSDB_CONTAINER",
    "AZURE_OPENAI_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_KEY",
    "AZURE_SEARCH_INDEX",
    "OPENAI_EMBEDDING_MODEL"
]

print("🔐 Текущие значения переменных окружения:\n")

for key in keys:
    value = os.getenv(key)
    masked = value[:4] + "..." + value[-4:] if value and "key" in key.lower() else value
    print(f"{key}: {masked}")