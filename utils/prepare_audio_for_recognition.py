from pydub import AudioSegment
import os

def prepare_audio_for_recognition(audio_path: str) -> str:
    """
    Преобразует аудиофайл (в формате webm) во временный WAV-файл, подходящий для распознавания.
    Возвращает путь к новому .wav файлу.
    """
    # Читаем исходный файл как WEBM
    sound = AudioSegment.from_file(audio_path, format="webm")

    # Сохраняем как WAV
    wav_path = audio_path.replace(".webm", ".wav")
    sound.export(wav_path, format="wav")
    
    return wav_path