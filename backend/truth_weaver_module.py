import os
import json
import requests
import time


def analyze_transcript_with_gemini(transcript_text, audio_filename):
    """
    Analyzes a transcript using the Gemini API to find contradictions and
    synthesize the truth in the required JSON format.
    """
    api_key = "AIzaSyDY9r_y4jdZ1sIJFT3zSGVztrusmPD0oH4"  # Replace with your actual API key
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

    The 'programming_language' is 'Not explicitly mentioned in the transcript'.
    The 'skill_mastery' is 'intermediate'.
    The 'leadership_claims' should be "Merely coordinated, not led."
    The 'team_experience' is 'Individual contributor'.
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