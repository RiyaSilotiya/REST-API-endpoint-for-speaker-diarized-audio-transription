


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

### POST

Upload an audio file. The API will return a JSON response containing:

#### Request

In Postman:
1. **Method:** POST
2. **URL:** `http://127.0.0.1:8000/predicts/`
3. **Body:** Select **form-data**
    - **Key:** `audio_file` (set the type to `File`)
    - **Value:** Click `Choose Files` and select the audio file you want to upload.

#### Response

**Example JSON Response:**
```json
{
    "speaker_info": [
        {
            "speaker": "Speaker 1",
            "start": 0.0000,
            "end": 10.0000,
            "transcription": "Hello, how are you?"
        },
        {
            "speaker": "Speaker 2",
            "start": 10.0000,
            "end": 20.0000,
            "transcription": "I'm good, thanks."
        }
    ],
    "overall_transcription": "Complete transcription of the audio."
}
