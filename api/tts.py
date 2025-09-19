import io
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas import tts as tts_schema
from google.cloud import texttospeech
from google.oauth2 import service_account
from fastapi.concurrency import run_in_threadpool

# --- Router Setup ---
router = APIRouter(prefix="/api/tts", tags=["Text-to-Speech"])

# --- Configuration ---
VOICE_PARAMS = {
    "english": {"language_code": "en-IN", "name": "en-IN-Wavenet-A"},
    "hindi": {"language_code": "hi-IN", "name": "hi-IN-Wavenet-A"},
    "marathi": {"language_code": "mr-IN", "name": "mr-IN-Wavenet-A"},
    "malayalam": {"language_code": "ml-IN", "name": "ml-IN-Wavenet-A"},
}

# --- Google TTS Client Initialization (Updated) ---
tts_client = None
try:
    # Get the specific credentials file path from the new environment variable
    tts_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_tts")
    
    if not tts_credentials_path:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS_tts not set. TTS will be unavailable.")
    else:
        # Create a credentials object from that specific file
        credentials = service_account.Credentials.from_service_account_file(tts_credentials_path)
        # Initialize the client with the specific credentials
        tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
        print("✅ TTS Client initialized with specific credentials.")

except Exception as e:
    print(f"CRITICAL: Could not initialize Google TTS Client. Error: {e}")
    # tts_client remains None

# --- API Endpoint (No changes needed here) ---
@router.post("/synthesize",
             response_class=StreamingResponse,
             summary="Convert text to speech",
             description="Takes text and a supported language, returns an MP3 audio stream.")
async def synthesize_speech(request_body: tts_schema.TTSRequest):
    if not tts_client:
        raise HTTPException(status_code=503, detail="Text-to-Speech service is currently unavailable.")

    try:
        voice_config = VOICE_PARAMS.get(request_body.language.value)
        synthesis_input = texttospeech.SynthesisInput(text=request_body.text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_config["language_code"], name=voice_config["name"]
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        response = await run_in_threadpool(
            tts_client.synthesize_speech,
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mpeg")

    except Exception as e:
        print(f"An error occurred during TTS synthesis: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while synthesizing speech.")

