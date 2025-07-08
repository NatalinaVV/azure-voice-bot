from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)


endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
region = os.getenv("AZURE_TRANSLATOR_REGION")
key = os.getenv("AZURE_TRANSLATOR_KEY")

client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def detect_language(text: str) -> str:
    detection = client.detect_language(content=[text])
    return detection[0].language

def translate_to_english(text: str) -> str:
    response = client.translate(content=[text], to=["en"])
    return response[0].translations[0].text

def translate_from_english(text: str, to_lang: str) -> str:
    response = client.translate(content=[text], to=[to_lang])
    return response[0].translations[0].text