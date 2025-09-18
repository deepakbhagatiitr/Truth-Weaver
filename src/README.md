
# Truth Weaver: AI-Powered Transcript & Deception Analysis

## Overview

Truth Weaver is an AI-powered system for analyzing human communication. It processes transcripts, detects key information, and uncovers potential deception patterns using the Gemini API. The project includes:

- **Backend (Python):** Analyzes transcripts and generates structured JSON results.
- **Frontend (React + Vite):** (in `../frontend/`) Modern UI for uploading audio, viewing transcripts, and exploring AI analysis.

---

## How It Works

1. **Transcript Scanning:** Scans the `src/` directory for all files ending with `_transcript.txt`.
2. **AI Analysis:** Sends each transcript to the Gemini API for deep analysis.
3. **Structured Output:** Receives a JSON object with a "revealed truth" summary and a list of "deception patterns".
4. **Result Storage:** Saves a `.json` file for each transcript and a combined `all_transcripts_output.json`.

---

## Getting Started

### Prerequisites

- Python 3.6+
- `requests` library (`pip install requests`)
- Gemini API key

### Usage

1. Place your transcript files (e.g., `interview1_transcript.txt`) in the `src/` directory.
2. Set your Gemini API key in `src/truth_weaver.py`:
	```python
	api_key = "YOUR_GEMINI_API_KEY"
	```
3. Run the script from your project root:
	```
	python src/truth_weaver.py
	```
4. Find the output `.json` files in the `src/` directory.

---

## Frontend

A modern React + Vite frontend is available in the `../frontend/` folder. It allows you to:

- Upload audio files for transcription (future feature)
- View transcripts and AI analysis results
- Enjoy a clean, user-friendly interface

See `../frontend/README.md` for setup instructions.

---

## Project Structure

```
/src         # Python backend (transcript analysis)
/frontend    # React + Vite frontend (UI)
/audio       # (Optional) Audio files for future transcription
```

---

## License

MIT

---