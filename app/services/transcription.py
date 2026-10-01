from pathlib import Path

from groq import Groq

from app.config import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

async def transcribe_audio(audio_path: str) -> str:
    file_path = Path(audio_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        with open(file_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=(file_path.name,audio_file),
                model= settings.GROQ_STT_MODEL,
                response_format="verbose_json",
                language="en"
            )
        return transcription.text

    except Exception as exc:
        raise RuntimeError(f"Error during transcription: {str(exc)}") from exc