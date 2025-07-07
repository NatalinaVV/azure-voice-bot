import azure.functions as func
import logging
import tempfile

from services.rag.transcribe import speech_to_text
from services.rag.rag import run_rag_pipeline
from services.rag.synthesize import text_to_speech

app = func.FunctionApp()

@app.function_name(name="chatbot_voice_entrypoint")
@app.route(route="ask", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("VoiceBot function triggered.")

    try:
        text_input = req.form.get('text')
        audio_file = req.files.get('audio')

        # 1. Если есть аудио — сначала делаем STT
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(audio_file.read())
                tmp_audio_path = tmp_audio.name
            logging.info(f"Audio file saved to {tmp_audio_path}")
            text_input = speech_to_text(tmp_audio_path)

        if not text_input:
            return func.HttpResponse("No input provided", status_code=400)

        # 2. Выполняем RAG (поиск + генерация)
        answer = run_rag_pipeline(text_input)

        # 3. Генерируем аудио-ответ (TTS)
        audio_bytes = text_to_speech(answer)

        return func.HttpResponse(
            body=audio_bytes,
            status_code=200,
            mimetype="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=response.mp3"}
        )

    except Exception as e:
        logging.exception("Error in voicebot function")
        return func.HttpResponse(str(e), status_code=500)