import os
import logging
import config
from model import transcribe_audio
from flaskAPI import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_transcription(file_path: str):
    """
    Handle the transcription of an uploaded audio file.
    """
    try:
        logger.info(f"Transcribing file: {file_path}")
        text = transcribe_audio(file_path)

        return [{
            "text": text,
            "error": False,
            "error_message": ""
        }]

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}", exc_info=True)
        return [{
            "text": "",
            "error": True,
            "error_message": str(e)
        }]

    finally:
        # Optionally clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted temporary file: {file_path}")

if __name__ == '__main__':
    logger.info("Starting Flask Audio Transcription API...")
    app.run(host='0.0.0.0', port=8000, debug=True)
