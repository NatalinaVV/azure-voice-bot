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
from utils.language_utils import detect_language, translate_back, translate_to_english

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
    files: UploadFile = File(None)
):
    print("📥 ---------- New Req ---------- 📥")
    content_type = request.headers.get("content-type", "")
    print(f"📨 Headers: {request.headers}")
    print(f"📨 Request: {request}")
    print(f"📎 File: {files if files else 'None'}")

    transcribe = None
    query_text = None

    # if audio
    if files:
      with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        await files.seek(0)
        shutil.copyfileobj(files.file, tmp)

        # Конвертируем в WAV
        audio_path = prepare_audio_for_recognition(tmp.name)
        print(f"📁 Save temporary file : {audio_path}")
        print("📦 Size file:", os.path.getsize(audio_path), "bite")
        transcribe = speech_to_text(audio_path)
        query_text = transcribe

    #if text
    if not query_text and "application/json" in content_type:
        body = await request.json()
        print(f"💬 JSON Body: {body}")
        if "messages" in body:
            query_text = body["messages"][-1]["text"]

    if not query_text:
        print("❌ No input provided")
        return {"error": "No input provided."}
    
  # Multilingual processing
    user_lang = detect_language(query_text)
    query_en = translate_to_english(query_text, user_lang) if user_lang != "en" else query_text
    print(f"🔤 Detected: {user_lang}, translated: {query_en}")

    print(f"🧠 transcribe in RAG: {query_en}")
    answer_en = run_rag_pipeline(query_en)
    print(f"✅ answer: {answer_en}")
    
    final_answer = translate_back(answer_en, user_lang) if user_lang != "en" else answer_en
    audio_output = text_to_speech(final_answer, user_lang=user_lang)
    print("🔊 Responce text_to_speech")

    audio_base64 = base64.b64encode(audio_output).decode("utf-8")
    audio_data_uri = f"data:audio/mpeg;base64,{audio_base64}"

    return JSONResponse([{
        "role": "ai",
        "text": final_answer,
        "audio": audio_data_uri
    }])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)