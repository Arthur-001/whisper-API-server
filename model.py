import whisper
import librosa
import torch
import config

def transcribe_audio(file_path: str):
    model = whisper.load_model(config.MODEL_NAME, config.DEVICE)
    try:
        # Load audio using librosa
        audio = librosa.load(file_path, sr=16000)[0]
        result = model.transcribe(audio)
        text = result["text"]

    finally:
        # Explicitly release VRAM
        del model
        torch.cuda.empty_cache()  # Clears cached memory
        torch.cuda.synchronize()  # Ensures all pending GPU ops are done
    
    return text