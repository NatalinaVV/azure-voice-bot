import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Загрузка .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

def text_to_speech(text: str) -> bytes:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")

    if not speech_key:
        raise Exception("AZURE_SPEECH_KEY not found in .env")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

    # Сюда будет записан результат синтеза
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise Exception(f"TTS synthesis canceled: {cancellation.reason} - {cancellation.error_details}")
    else:
        raise Exception("TTS synthesis failed for unknown reason")