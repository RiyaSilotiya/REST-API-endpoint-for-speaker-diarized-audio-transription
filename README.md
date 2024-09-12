


# REST API Endpoint for Speaker-Diarized Audio Transcription

This Django project provides a REST API that processes audio files, performs speaker diarization and transcription, and returns the results in a structured JSON format. The project integrates speaker diarization and automatic speech recognition (ASR) techniques to deliver accurate transcriptions tagged with speaker identities and timestamps.

REST API: The API accepts audio files as input and returns results in JSON format.

Postman Testing: The API is tested and can be easily interacted with using Postman.

## Installation

1. **Clone the repository:**

    Open Command Prompt and run:
    ```bash
    git clone https://github.com/RiyaSilotiya/REST-API-endpoint-for-speaker-diarized-audio-transription.git
    cd REST-API-endpoint-for-speaker-diarized-audio-transription
    ```

2. **Create a virtual environment and activate it:**

    In Command Prompt or PowerShell, run:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**

    With the virtual environment activated, run:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    Apply migrations by running:
    ```bash
    python manage.py migrate
    ```

5. **Run the Django development server:**

    Start the server with:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### POST /api/transcribe/

Upload an audio file to be diarized and transcribed. The API will return a JSON response containing:

- **Transcriptions**
- **Speaker segments with timestamps**
- **Speaker labels**

#### Request

```bash
POST /api/transcribe/
Content-Type: multipart/form-data
File: <audio-file>

