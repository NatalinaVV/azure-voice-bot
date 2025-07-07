import shutil
import tempfile
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        contents = upload_file.file.read()
        tmp.write(contents)
        return tmp.name