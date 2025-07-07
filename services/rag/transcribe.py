import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from utils.prepare_audio_for_recognition import prepare_audio_for_recognition

# Загрузка .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

def speech_to_text(audio_path: str) -> str:
    try:
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")

        wav_path = prepare_audio_for_recognition(audio_path)

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = speechsdk.AudioConfig(filename=wav_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"✅ RecognizedSpeech: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("❌ NoMatch.")
            return ""
        else:
            raise Exception(f"Speech recognition error: {result.reason}")

    except Exception as e:
        print(f"❌ Speech recognition error speech_to_text: {e}")
        raise