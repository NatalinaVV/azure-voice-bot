import os
import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from embedding import get_embedding

# Чтение файла
df = pd.read_csv("data/faq.csv")

# Подключение к Cognitive Search
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# Преобразование данных в формат для индексации
docs = []
for i, row in df.iterrows():
    question = str(row['question'])
    answer = str(row['answer'])
    full_text = f"Q: {question}\nA: {answer}"
    embedding = get_embedding(full_text)

    docs.append({
        "id": f"faq-{i}",
        "content": full_text,
        "vector": embedding
    })

# Загрузка в индекс
result = search_client.upload_documents(documents=docs)
print(f"Upload result: {result}")
