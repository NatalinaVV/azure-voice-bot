import base64
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import tempfile
import uvicorn
import shutil
import os

from services.rag.transcribe import speech_to_text
from services.rag.rag import run_rag_pipeline
from services.rag.synthesize import text_to_speech
from utils.save_file import save_upload_file
from utils.prepare_audio_for_recognition import prepare_audio_for_recognition

app = FastAPI(title="VoiceBot RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(
    request: Request,
    files: UploadFile = File(None),
    messages: str = Form(None)
):
    print("📥 ---------- New Req ---------- 📥")
    print(f"📨 Headers: {request.headers}")
    print(f"📨 Request: {request}")
    print(f"📎 File: {files if files else 'None'}")
    print(f"💬 Messages: {messages}")

    transcribe = None

    # Если пришёл файл — обрабатываем
    if files:
      with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        await files.seek(0)
        shutil.copyfileobj(files.file, tmp)

# Конвертируем в WAV
    audio_path = prepare_audio_for_recognition(tmp.name)
    print(f"📁 Save temporary file : {audio_path}")
    print("📦 Size file:", os.path.getsize(audio_path), "bite")
    transcribe = speech_to_text(audio_path)

    if not transcribe:
        print("❌ transcribe NO transcribe")
        return {"error": "No input provided."}
    
    query_text = transcribe or messages

    print(f"🧠 transcribe in RAG: {query_text}")
    answer = run_rag_pipeline(query_text)
    print(f"✅ answer: {answer}")

    audio_output = text_to_speech(answer)
    print("🔊 Responce text_to_speech")

    audio_base64 = base64.b64encode(audio_output).decode("utf-8")
    audio_data_uri = f"data:audio/mpeg;base64,{audio_base64}"

    return JSONResponse([{
        "role": "ai",
        "text": answer,
        "audio": audio_data_uri
    }])
    # return JSONResponse({
    #    "role": "ai",
    #     "text": answer,
    #     "audio": audio_data_uri,
    #     "headers": {"Content-Disposition": "inline; filename=answer.mp3"}
    # })

    # return Response(
    #     content=audio_output,
    #     # content={"role": "ai", "text": "Message from bob"},
    #     media_type="audio/mpeg",
    #     headers={"Content-Disposition": "inline; filename=answer.mp3"}
    # )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)