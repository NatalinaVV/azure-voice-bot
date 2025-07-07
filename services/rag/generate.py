# from openai import AzureOpenAI
# import os
# from dotenv import load_dotenv

# # Загрузка .env
# env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
# load_dotenv(dotenv_path=env_path)

# def generate_answer(question: str, context_chunks: list[str]) -> str:
#     client = AzureOpenAI(
#         api_key=os.getenv("AZURE_OPENAI_KEY"),
#         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#         api_version=os.getenv("AZURE_OPENAI_API_VERSION")
#     )

#     deployment = os.getenv("AZURE_GPT_DEPLOYMENT")

#     context = "\n\n".join(context_chunks)
#     prompt = f"""Use the following knowledge to answer the user's question.

# Context:
# {context}

# Question:
# {question}

# Answer:"""
#     print(f"this is context{context}")
#     print("💬 DEPLOYMENT MODEL:", deployment)
#     print("💬 MESSAGES SENT:", [
#     {"role": "system", "content": "You are a helpful medical assistant."},
#     {"role": "user", "content": prompt}
# ])
    
#     response = client.chat.completions.create(
#         model=deployment,
#         messages=[
#             {"role": "system", "content": "You are a helpful medical assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3,
#         max_tokens=500
#     )
#     print("💬 Sending to OpenAI:", response.choices[0].message.content.strip())
#     return response.choices[0].message.content.strip()


from openai import AzureOpenAI
from dotenv import load_dotenv
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_NEW"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_NEW")
)

deployment_name = os.getenv("AZURE_GPT_DEPLOYMENT", "gpt-35-turbo")


def generate_answer(context, user_input):
    if isinstance(context, list):
        context = "\n\n".join(context)
    if isinstance(user_input, list):
        user_input = " ".join(user_input)

    if not user_input or not user_input.strip():
        return "Sorry, I didn't catch that. Could you please repeat?"

    prompt = f"""Use the following knowledge to answer the user's question.

Context:
{context}

Question:
{user_input}

Answer:"""

    response = client.chat.completions.create(
        model=deployment_name,  
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()