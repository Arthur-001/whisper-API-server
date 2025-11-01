from datetime import datetime
from zoneinfo import ZoneInfo
import torch

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac', 'wma', 'oga'}

# API and file configurations
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
UPLOAD_FOLDER = 'uploads'

# Time zone and timestamp
TIMEZONE = 'Europe/Istanbul'
CURRENT_TIME = datetime.now(ZoneInfo(TIMEZONE)).isoformat()

# Whisper model configuration
MODEL_NAME = "small"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
