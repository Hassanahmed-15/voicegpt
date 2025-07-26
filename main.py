from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
import openai
import os
import tempfile
import librosa
import soundfile as sf
import logging
import requests

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App setup
app = FastAPI(title="Voice Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Directory setup
os.makedirs("static", exist_ok=True)
os.makedirs("temp_audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Whisper model (CPU)
try:
    logger.info("Loading Whisper model...")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
except Exception as e:
    logger.error("Failed to load Whisper model:", exc_info=e)
    raise

# OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

# ElevenLabs API config
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_2c3169a73d06a6432620f680470cbca76674f1ebf0e03b1f")
VOICE_ID = "9urT9HNw6olb6wpbHM0r"  # User-provided


def preprocess_audio(audio_path: str) -> str:
    try:
        audio, sr = librosa.load(audio_path, sr=16000)
        audio = librosa.util.normalize(audio)
        audio = librosa.effects.preemphasis(audio)
        audio, _ = librosa.effects.trim(audio, top_db=30)
        processed_path = os.path.join("temp_audio", "processed.wav")
        sf.write(processed_path, audio, sr, subtype='PCM_16')
        return processed_path
    except Exception as e:
        logger.warning("Audio preprocessing failed, using original:", exc_info=e)
        return audio_path


def elevenlabs_tts(text: str, output_path: str, voice_id: str, api_key: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"ElevenLabs API error {response.status_code}: {response.text}")


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def handle_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(400, "Only audio files supported")

    try:
        file_ext = os.path.splitext(file.filename)[1] or ".webm"
        with tempfile.NamedTemporaryFile(dir="temp_audio", suffix=file_ext, delete=False) as tmp:
            content = await file.read()
            if len(content) < 2048:
                raise HTTPException(400, "Audio file too small")
            tmp.write(content)
            tmp_path = tmp.name

        processed_path = preprocess_audio(tmp_path)
        segments, _ = model.transcribe(processed_path, language="en")
        transcription = " ".join(segment.text for segment in segments).strip()

        if not transcription:
            raise HTTPException(400, "No speech detected")

        # GPT reply
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Hassan, a helpful voice assistant."},
                {"role": "user", "content": transcription}
            ],
            max_tokens=150
        )
        reply = response.choices[0].message.content

        # ElevenLabs TTS
        tts_path = os.path.join("static", "response.mp3")
        elevenlabs_tts(reply, tts_path, VOICE_ID, ELEVENLABS_API_KEY)

        return JSONResponse({
            "status": "success",
            "transcription": transcription,
            "reply": reply,
            "audio_url": "/static/response.mp3"
        })

    except Exception as e:
        logger.error("Failed to process audio:", exc_info=e)
        raise HTTPException(500, "Internal server error")
