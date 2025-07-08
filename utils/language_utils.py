import os
import requests
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)


AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "westeurope")

# Общие заголовки
headers = {
    "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
    "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
    "Content-Type": "application/json"
}

def detect_language(text: str) -> str:
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translator/text/v3.0/detect?api-version=3.0"
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    return result[0]["language"]

def translate_to_english(text: str, source_lang: str) -> str:
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translator/text/v3.0/translate?api-version=3.0&to=en&from={source_lang}"
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]

def translate_back(text: str, target_lang: str) -> str:
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/translator/text/v3.0/translate?api-version=3.0&to={target_lang}"
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]