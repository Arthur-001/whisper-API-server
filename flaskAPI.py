from flask import Flask, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
import logging
import os
import config
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

def is_allowed_file(filename):
    """Check if file has an allowed audio extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/healthstatus', methods=['GET'])
def health_status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': config.CURRENT_TIME,
        'service': 'Audio File API'
    }), 200


@app.route('/upload', methods=['POST'])
def upload_audio():
    """Handle audio file uploads (multipart or binary from n8n)"""
    try:
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

        # Case 1: multipart/form-data (regular file upload)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                logger.warning("No file selected")
                return jsonify([{
                    "text": "",
                    "error": True,
                    "error_message": "No file selected"
                }]), 400

            if not is_allowed_file(file.filename):
                logger.warning(f"Invalid file type: {file.filename}")
                return jsonify([{
                    "text": "",
                    "error": True,
                    "error_message": f"Invalid file type. Allowed types: {list(config.ALLOWED_EXTENSIONS)}"
                }]), 400

            file_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            logger.info(f"File uploaded successfully: {file_path}")

        # Case 2: raw binary data (e.g., from n8n)
        elif request.data:
            logger.info("Received binary data stream from n8n")

            # n8n usually sends binary field "data"
            filename = request.headers.get("X-Filename", "uploaded_audio.wav")
            if not is_allowed_file(filename):
                filename += ".wav"

            file_path = os.path.join(config.UPLOAD_FOLDER, filename)
            with open(file_path, "wb") as f:
                f.write(request.data)
            logger.info(f"Binary data written to: {file_path}")

        else:
            logger.warning("No file or binary data found in request")
            return jsonify([{
                "text": "",
                "error": True,
                "error_message": "No file or binary data found in request"
            }]), 400

        # Call the transcription function (imported from main.py)
        from main import handle_transcription
        response = handle_transcription(file_path)
        return jsonify(response), 200

    except RequestEntityTooLarge:
        logger.error("File too large")
        return jsonify([{
            "text": "",
            "error": True,
            "error_message": "File too large (max 50MB)"
        }]), 413

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify([{
            "text": "",
            "error": True,
            "error_message": str(e)
        }]), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify([{
        "text": "",
        "error": True,
        "error_message": "Endpoint not found"
    }]), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify([{
        "text": "",
        "error": True,
        "error_message": "Internal server error"
    }]), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)
