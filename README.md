# Whisper API Server

This project provides a Flask-based API server for transcribing audio files using OpenAI's Whisper model.

## Overview

The API allows you to upload audio files and receive the transcribed text. It's designed to be simple to use and can be integrated into various workflows. The server can be configured to run on either a CPU or a GPU (if a compatible NVIDIA GPU with CUDA is available).

## Features

-   Transcribe a variety of audio formats, including `.mp3`, `.wav`, `.ogg`, and more.
-   Upload audio files using either `multipart/form-data` or as raw binary data.
-   A `/healthstatus` endpoint to monitor the API's health.
-   Configurable Whisper model size and processing device (CPU/GPU).
-   Automatic cleanup of uploaded audio files after transcription.
-   Efficient VRAM management when using a GPU.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Arthur-001/whisper-API-server.git
    cd whisper-API-server
    ```

2.  **Install dependencies:**

    It is recommended to create a `requirements.txt` file with the following content:

    ```
    Flask
    torch
    openai-whisper
    librosa
    werkzeug
    ```

    Then, install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration:**

    The server can be configured by editing the `config.py` file. Here you can set:
    -   `ALLOWED_EXTENSIONS`: The set of allowed audio file extensions.
    -   `MAX_CONTENT_LENGTH`: The maximum allowed file size for uploads.
    -   `UPLOAD_FOLDER`: The directory where uploaded files are temporarily stored.
    -   `MODEL_NAME`: The Whisper model to use (e.g., "tiny", "base", "small", "medium", "large").
    -   `DEVICE`: The device to use for transcription ("cuda" for GPU, "cpu" for CPU).

## Usage

1.  **Run the server:**

    ```bash
    python flaskAPI.py
    ```
    The server will start on `http://0.0.0.0:8010`.

2.  **API Endpoints:**

    -   **`POST /upload`**: Upload an audio file for transcription.

        -   **Using `multipart/form-data`:**

            ```bash
            curl -X POST -F "file=@/path/to/your/audio.mp3" http://localhost:8010/upload
            ```

        -   **Using raw binary data:**

            ```bash
            curl -X POST --data-binary "@/path/to/your/audio.wav" -H "Content-Type: application/octet-stream" http://localhost:8010/upload
            ```

    -   **`GET /healthstatus`**: Check the health of the API.

        ```bash
        curl http://localhost:8010/healthstatus
        ```

## Checking for CUDA

To check if a compatible NVIDIA GPU with CUDA is available on your system, you can run the `check_cuda.py` script:

```bash
python check_cuda.py
```

This will print information about your CUDA setup and available GPUs.
