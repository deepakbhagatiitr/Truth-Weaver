# Truth Weaver Backend

Flask backend for the Truth Weaver AI-powered transcript analysis system.

## Features

- **Audio Transcription**: Convert audio files to text using Google Speech Recognition
- **AI Analysis**: Analyze transcripts for deception patterns using Gemini AI
- **RESTful API**: Clean API endpoints for frontend integration
- **CORS Support**: Enabled for frontend communication

## API Endpoints

### 1. Health Check
```
GET /health
```
Returns server status.

### 2. Transcribe Audio
```
POST /transcribe
Content-Type: multipart/form-data
Body: audio file (key: 'audio')
```
Converts audio to text transcript.

### 3. Analyze Transcript
```
POST /analyze
Content-Type: application/json
Body: {"transcript": "text", "filename": "optional"}
```
Analyzes transcript for deception patterns.

### 4. Transcribe and Analyze (Combined)
```
POST /transcribe-and-analyze
Content-Type: multipart/form-data
Body: audio file (key: 'audio')
```
One-step process: transcribe audio and analyze in single request.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Gemini API Key:**
   Edit `truth_weaver_module.py` and add your API key:
   ```python
   api_key = "YOUR_GEMINI_API_KEY"
   ```

3. **Run the server:**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`

## Dependencies

- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- speech_recognition: Audio-to-text conversion
- pydub: Audio file processing
- requests: HTTP requests for Gemini API

## Usage

The backend is designed to work with the React frontend. It accepts audio files, transcribes them, and provides AI-powered analysis of potential deception patterns in the transcript.

## Project Structure

```
backend/
├── app.py                    # Main Flask application
├── truth_weaver_module.py    # AI analysis module
├── requirements.txt          # Python dependencies
└── README.md                # This file
```