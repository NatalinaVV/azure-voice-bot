import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Загрузка .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

LANGUAGE_VOICES = {
    "en": "en-US-AriaNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "es": "es-ES-ElviraNeural",
    "it": "it-IT-ElsaNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "uk": "uk-UA-OstapNeural",
    "pl": "pl-PL-ZofiaNeural",
    "pt": "pt-PT-FernandaNeural",
    "zh": "zh-CN-XiaoxiaoNeural",
    "ja": "ja-JP-NanamiNeural",
    # Add language as needed
}

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

# def text_to_speech(text: str, lang_code: str = "en") -> bytes:
#     speech_key = os.getenv("AZURE_SPEECH_KEY")
#     service_region = os.getenv("AZURE_SPEECH_REGION", "westeurope")

#     if not speech_key:
#         raise Exception("AZURE_SPEECH_KEY not found in .env")

#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

#     # Выбираем голос по языку, если доступен
#     # Тут можно сделать настройку и выбрать особенный голос
#     voice_name = LANGUAGE_VOICES.get(lang_code, "en-US-AriaNeural")
#     speech_config.speech_synthesis_voice_name = voice_name

#     synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
#     result = synthesizer.speak_text_async(text).get()

#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         return result.audio_data
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         cancellation = result.cancellation_details
#         raise Exception(f"TTS synthesis canceled: {cancellation.reason} - {cancellation.error_details}")
#     else:
#         raise Exception("TTS synthesis failed for unknown reason")