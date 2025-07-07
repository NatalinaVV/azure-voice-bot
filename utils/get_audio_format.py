import mimetypes
import os

def get_audio_format(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == "audio/wav":
        return "wav"
    elif mime_type == "audio/mpeg":
        return "mp3"
    else:
        return "unknown"