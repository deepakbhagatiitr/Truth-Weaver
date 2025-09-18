
import os
import json
import requests
import time
import glob

try:
    from env_loader import load_env
    load_env()
except Exception:
    pass


def analyze_transcript_with_gemini(transcript_text, audio_filename):
    """
    Analyzes a transcript using the Gemini API to find contradictions and
    synthesize the truth in the required JSON format.
    """
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDY9r_y4jdZ1sIJFT3zSGVztrusmPD0oH4")
    if not api_key or api_key.strip() in {"REPLACE_ME", "", "your_gemini_api_key_here"}:
        return {"error": "GEMINI_API_KEY missing or placeholder. Set it in root .env or export before running."}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Define the system instruction for the Gemini model
    system_prompt = (
        "You are an AI detective named 'Truth Weaver' for the Innov8 3.0 hackathon. "
        "Your task is to analyze a transcript of a 'Whispering Shadow' agent's "
        "testimony. You must identify inconsistencies, contradictions, and "
        "unreliable statements. Finally, you will synthesize the most likely truth "
        "and present your findings in a specific JSON format."
    )

    # Construct the user prompt with the transcript and instructions for the output
    user_query = f"""
    Analyze the following transcript from a "Whispering Shadow" agent.
    
    Transcript:
    "{transcript_text}"

    Based on the text, perform the following tasks:
    1.  Identify the central claims made by the speaker.
    2.  Find any contradictions or self-corrections in their statements.
    3.  Synthesize the "revealed truth" from the conflicting claims.
    4.  Categorize the "deception patterns". Based on the content, identify the type of lie.
    5.  Generate a JSON object in the following format. Ensure the output is a valid JSON.

    {{
        "shadow_id": "{os.path.splitext(os.path.basename(audio_filename))[0]}",
        "revealed_truth": {{
            "programming_experience": "string",
            "programming_language": "string",
            "skill_mastery": "string",
            "leadership_claims": "string",
            "team_experience": "string",
            "skills and other keywords": ["list of strings"]
        }},
        "deception_patterns": [
            {{
                "lie_type": "string",
                "contradictory_claims": ["list of strings"]
            }}
        ]
    }}

    Guidelines:
    - Use the exact field names and structure above. Do not add or remove fields.
    - For any field not present in the transcript, use "Not explicitly mentioned in the transcript".
    - For 'skill_mastery', use "intermediate" unless the transcript clearly indicates otherwise.
    - For 'leadership_claims', use "Merely coordinated, not led." unless the transcript clearly indicates otherwise.
    - For 'team_experience', use "Individual contributor" unless the transcript clearly indicates otherwise.
    - For 'skills and other keywords', extract all relevant technical terms, skills, or keywords mentioned.
    - For 'deception_patterns', list all types of deception and the exact contradictory claims or statements.
    - Do not include any explanation, summary, or commentary outside the JSON object.
    """

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json"}
    }

    print("Sending request to Gemini API...")

    for i in range(3):  # Retry up to 3 times with exponential backoff
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()

            # The API returns a text field that is a JSON string, so we parse it
            json_string = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(json_string)

        except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < 2:
                time.sleep(2 ** (i + 1))
            else:
                return {"error": str(e)}

    return {"error": "Failed to get a response from the API after multiple retries."}


# --- Main script execution ---

if __name__ == "__main__":
    import os
    transcript_dir = os.path.join(os.path.dirname(__file__), "transcript")
    json_dir = os.path.join(os.path.dirname(__file__), "json")
    os.makedirs(json_dir, exist_ok=True)
    transcript_files = [
        f for f in glob.glob(os.path.join(transcript_dir, "*_transcript.txt"))
        if os.path.basename(f) != "combined_sessions_transcript.txt"
    ]

    if not transcript_files:
        print(f"❌ No transcript files found in {transcript_dir}")
    else:
        all_outputs = {}

        for transcript_path in transcript_files:
            print(f"🔍 Analyzing {os.path.basename(transcript_path)} ...")


            # Read transcript text and strip session header if present
            with open(transcript_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Remove first line if it matches 'Session N:'
            import re
            if lines and re.match(r"Session \\d+:", lines[0]):
                transcript_text = "".join(lines[1:]).lstrip()
            else:
                transcript_text = "".join(lines)

            # Call Gemini
            json_output = analyze_transcript_with_gemini(transcript_text, transcript_path)

            # Store in combined output
            all_outputs[os.path.basename(transcript_path)] = json_output

            # Save individual JSON
            json_file = os.path.join(json_dir, os.path.basename(transcript_path).replace("_transcript.txt", ".json"))
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(json_output, f, indent=4, ensure_ascii=False)
            print(f"💾 Saved individual JSON: {json_file}")

        # Save combined JSON
        combined_file = os.path.join(json_dir, "all_transcripts_output.json")
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(all_outputs, f, indent=4, ensure_ascii=False)

        print(f"✅ Combined JSON saved: {combined_file}")
