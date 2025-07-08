# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # Загрузка .env
# env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
# load_dotenv(dotenv_path=env_path)

# def get_embedding(text: str):
#     client = OpenAI(
#         api_key=os.getenv("AZURE_OPENAI_KEY")
#     )

#     response = client.embeddings.create(
#         input=[text],
#         model="text-embedding-3-small"
#     )

#     # Возвращаем первый (и единственный) эмбеддинг
#     return response.data[0].embedding


# from openai import AzureOpenAI
# import os
# from dotenv import load_dotenv

# # Загрузка .env
# env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
# load_dotenv(dotenv_path=env_path)

# def get_embedding(text: str):
#     if not text or not text.strip():
#         raise ValueError("❌  ERROR get_embedding")

#     deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
#     if not deployment:
#         raise ValueError("❌  AZURE_EMBEDDING_DEPLOYMENT в .env")

#     client = AzureOpenAI(
#         api_key=os.getenv("AZURE_OPENAI_KEY"),
#         api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
#         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
#     )
#     if not text or not text.strip():
#       raise ValueError("❌ Text is empty, cannot generate embedding.")
#     print("📥 Embedding input text:", repr(text))

#     response = client.embeddings.create(
#         model=deployment,
#         input=[text]
#     )
    
#     print(f"THIS is EMBADININGGGGGGGGGGGG", response.data[0].embedding)
#     if not response.data or not response.data[0].embedding:
#         raise RuntimeError("❌ haven't Azure OpenAI")

#     return response.data[0].embedding


from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# # Загрузка .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

# 🔐 Создаём клиент OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_NEW"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_NEW")
)

deployment = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_embedding(text: str):
    if not text or not text.strip():
        print("⚠️ Empty input text for embedding.")
        return None

    print("📥 Embedding input:", repr(text))

    try:
        response = client.embeddings.create(
            model=deployment,
            input=[text]
        )
    except Exception as e:
        print(f"❌ Error during embedding: {e}")
        return None

    embedding = response.data[0].embedding if response.data else None

    if not embedding:
        print("❌ No embedding returned from OpenAI.")
        return None

    print("✅ Embedding generated successfully.")
    return embedding