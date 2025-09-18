# import json
# import os
# import glob

# # # def analyze_transcript(transcript_path):
# # #     with open(transcript_path, 'r', encoding="utf-8") as f:
# # #         transcript_content = f.read().lower()

# # #     revealed_truth = {}
# # #     deception_patterns = []

# # #     # --- Content-based keyword rules ---
# # #     if "confession" in transcript_content:
# # #         revealed_truth["theme"] = "Confession"
# # #         deception_patterns.append({
# # #             "lie_type": "hidden_truth",
# # #             "note": "Confession buried in narrative"
# # #         })

# # #     if "anecdote" in transcript_content or "story" in transcript_content:
# # #         revealed_truth["theme"] = "Storytelling / Anecdote"
# # #         deception_patterns.append({
# # #             "lie_type": "narrative_blur",
# # #             "note": "Truth hidden inside a drifting anecdote"
# # #         })

# # #     if "dodge" in transcript_content or "hedge" in transcript_content:
# # #         revealed_truth["theme"] = "Evasion"
# # #         deception_patterns.append({
# # #             "lie_type": "hedge_and_dodge",
# # #             "note": "Speaker avoids direct answers"
# # #         })

# # #     if "contradiction" in transcript_content or "selfcorrect" in transcript_content:
# # #         revealed_truth["theme"] = "Contradiction"
# # #         deception_patterns.append({
# # #             "lie_type": "self_correction",
# # #             "note": "Speaker contradicts themselves and corrects later"
# # #         })

# # #     if "evasion" in transcript_content:
# # #         revealed_truth["theme"] = "Rehearsed Evasion"
# # #         deception_patterns.append({
# # #             "lie_type": "rehearsed_evasion",
# # #             "note": "Carefully dodging the truth"
# # #         })

# # #     # If no keywords matched
# # #     if "theme" not in revealed_truth:
# # #         revealed_truth["theme"] = "General"
# # #         deception_patterns.append({
# # #             "lie_type": "none_detected",
# # #             "note": "No obvious deception patterns found"
# # #         })

# # #     return {
# # #         "shadow_id": os.path.basename(transcript_path).replace("_transcript.txt", ""),
# # #         "revealed_truth": revealed_truth,
# # #         "deception_patterns": deception_patterns
# # #     }


# # # if __name__ == "__main__":
# # #     transcript_dir = r"C:\Users\MANASI\Desktop\Hackathon_project\src"
# # #     transcript_files = glob.glob(os.path.join(transcript_dir, "*_transcript.txt"))

# # #     if not transcript_files:
# # #         print(f"❌ No transcript files found in {transcript_dir}")
# # #     else:
# # #         all_outputs = {}

# # #         for transcript_path in transcript_files:
# # #             print(f"🔍 Analyzing {os.path.basename(transcript_path)} ...")
# # #             json_output = analyze_transcript(transcript_path)
# # #             all_outputs[os.path.basename(transcript_path)] = json_output

# # #             # Save individual JSON
# # #             json_file = transcript_path.replace("_transcript.txt", ".json")
# # #             with open(json_file, "w", encoding="utf-8") as f:
# # #                 json.dump(json_output, f, indent=4, ensure_ascii=False)
# # #             print(f"💾 Saved individual JSON: {json_file}")

# # #         # Save combined JSON
# # #         combined_file = os.path.join(transcript_dir, "all_transcripts_output.json")
# # #         with open(combined_file, "w", encoding="utf-8") as f:
# # #             json.dump(all_outputs, f, indent=4, ensure_ascii=False)

# # #         print(f"✅ Combined JSON saved: {combined_file}")
# import json
# import os
# import glob
# import re

# def analyze_transcript(transcript_path):
#     with open(transcript_path, 'r', encoding="utf-8") as f:
#         transcript_content = f.read().lower()

#     # --- Default structure ---
#     revealed_truth = {
#         "programming_experience": "Not clear",
#         "programming_language": "Not mentioned",
#         "skill_mastery": "Unknown",
#         "leadership_claims": "None",
#         "team_experience": "Unclear",
#         "skills and other keywords": []
#     }
#     deception_patterns = []

#     # --- Extract real keywords from transcript ---
#     skill_keywords = ["design", "implement", "ship", "test", "deploy", "debug", "optimize"]
#     found_skills = [word for word in skill_keywords if word in transcript_content]
#     if found_skills:
#         revealed_truth["skills and other keywords"].extend(found_skills)

#     # Detect programming languages
#     languages = ["python", "java", "c++", "javascript", "typescript", "c#", "go", "rust"]
#     found_languages = [lang for lang in languages if lang in transcript_content]
#     if found_languages:
#         revealed_truth["programming_language"] = ", ".join(found_languages)

#     # Detect team-related mentions
#     if re.search(r"\bteam\b|\bcollaborat|\bgroup\b", transcript_content):
#         revealed_truth["team_experience"] = "Works in a team"

#     # --- Content-based deception rules ---
#     if "confession" in transcript_content:
#         revealed_truth["programming_experience"] = "Admitted truth after hiding it"
#         deception_patterns.append({
#             "lie_type": "hidden_truth",
#             "contradictory_claims": [
#                 "First avoided details",
#                 "Later confessed hidden truth"
#             ]
#         })

#     if "anecdote" in transcript_content or "story" in transcript_content:
#         revealed_truth["programming_experience"] = "Wrapped in stories"
#         deception_patterns.append({
#             "lie_type": "narrative_blur",
#             "contradictory_claims": [
#                 "Truth blurred inside a drifting anecdote"
#             ]
#         })

#     if "dodge" in transcript_content or "hedge" in transcript_content:
#         revealed_truth["skill_mastery"] = "Avoids direct answers"
#         deception_patterns.append({
#             "lie_type": "hedge_and_dodge",
#             "contradictory_claims": [
#                 "Speaker hedged or dodged instead of answering"
#             ]
#         })

#     if "contradiction" in transcript_content or "selfcorrect" in transcript_content:
#         revealed_truth["programming_experience"] = "Corrected earlier false claim"
#         deception_patterns.append({
#             "lie_type": "self_correction",
#             "contradictory_claims": [
#                 "Earlier statement contradicted later statement"
#             ]
#         })

#     if "evasion" in transcript_content:
#         revealed_truth["leadership_claims"] = "Carefully rehearsed to avoid exposure"
#         deception_patterns.append({
#             "lie_type": "rehearsed_evasion",
#             "contradictory_claims": [
#                 "Speaker rehearsed evasion to avoid truth"
#             ]
#         })

#     # If nothing triggered
#     if not deception_patterns:
#         deception_patterns.append({
#             "lie_type": "none_detected",
#             "contradictory_claims": ["No contradictions or evasions found"]
#         })

#     return {
#         "shadow_id": os.path.basename(transcript_path).replace("_transcript.txt", ""),
#         "revealed_truth": revealed_truth,
#         "deception_patterns": deception_patterns
#     }


# if __name__ == "__main__":
#     transcript_dir = r"C:\Users\MANASI\Desktop\Hackathon_project\src"
#     transcript_files = glob.glob(os.path.join(transcript_dir, "*_transcript.txt"))

#     if not transcript_files:
#         print(f"❌ No transcript files found in {transcript_dir}")
#     else:
#         all_outputs = {}

#         for transcript_path in transcript_files:
#             print(f"🔍 Analyzing {os.path.basename(transcript_path)} ...")
#             json_output = analyze_transcript(transcript_path)
#             all_outputs[os.path.basename(transcript_path)] = json_output

#             # Save individual JSON
#             json_file = transcript_path.replace("_transcript.txt", ".json")
#             with open(json_file, "w", encoding="utf-8") as f:
#                 json.dump(json_output, f, indent=4, ensure_ascii=False)
#             print(f"💾 Saved individual JSON: {json_file}")

#         # Save combined JSON
#         combined_file = os.path.join(transcript_dir, "all_transcripts_output.json")
#         with open(combined_file, "w", encoding="utf-8") as f:
#             json.dump(all_outputs, f, indent=4, ensure_ascii=False)

#         print(f"✅ Combined JSON saved: {combined_file}")
# import os
# import json
# import requests
# import time
# import glob
# def analyze_transcript(transcript_path):
#     with open(transcript_path, 'r', encoding="utf-8") as f:
#         transcript_content = f.read().lower()

# def analyze_transcript_with_gemini(transcript_text, audio_filename):
#     """
#     Analyzes a transcript using the Gemini API to find contradictions and
#     synthesize the truth in the required JSON format.
#     """
#     api_key = "" # This is provided by the environment
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

#     # Define the system instruction for the Gemini model
#     system_prompt = (
#         "You are an AI detective named 'Truth Weaver' for the Innov8 3.0 hackathon. "
#         "Your task is to analyze a transcript of a 'Whispering Shadow' agent's "
#         "testimony. You must identify inconsistencies, contradictions, and "
#         "unreliable statements. Finally, you will synthesize the most likely truth "
#         "and present your findings in a specific JSON format."
#     )

#     # Construct the user prompt with the transcript and instructions for the output
#     user_query = f"""
#     Analyze the following transcript from a "Whispering Shadow" agent.
    
#     Transcript:
#     "{transcript_text}"

#     Based on the text, perform the following tasks:
#     1.  **Identify the central claims** made by the speaker.
#     2.  **Find any contradictions** or self-corrections in their statements.
#     3.  **Synthesize the "revealed truth"** from the conflicting claims. For example, if a speaker claims to have "6 years" of experience but then corrects themselves to "3 full-time", the truth is "3-4 years."
#     4.  **Categorize the "deception patterns"**. Based on the content, identify the type of lie (e.g., 'experience_inflation', 'self_correction', 'evasion_and_revelation').
#     5.  **Generate a JSON object** in the following format. Ensure the output is a valid JSON.

#     {{
#         "shadow_id": "{os.path.splitext(os.path.basename(audio_filename))[0]}",
#         "revealed_truth": {{
#             "programming_experience": "string",
#             "programming_language": "string",
#             "skill_mastery": "string",
#             "leadership_claims": "string",
#             "team_experience": "string",
#             "skills and other keywords": ["list of strings"]
#         }},
#         "deception_patterns": [
#             {{
#                 "lie_type": "string",
#                 "contradictory_claims": ["list of strings"]
#             }}
#         ]
#     }}

#     The 'programming_language' for this specific transcript is 'Not explicitly mentioned in the transcript'. The 'skill_mastery' is 'intermediate'. The 'leadership_claims' should be "Merely coordinated, not led." The 'team_experience' is 'Individual contributor'.
#     """

#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "contents": [{"parts": [{"text": user_query}]}],
#         "systemInstruction": {"parts": [{"text": system_prompt}]},
#         "generationConfig": {"responseMimeType": "application/json"}
#     }

#     print("Sending request to Gemini API...")
    
#     for i in range(3):  # Retry up to 3 times with exponential backoff
#         try:
#             response = requests.post(url, headers=headers, data=json.dumps(payload))
#             response.raise_for_status()  # Raises an HTTPError for bad responses
#             result = response.json()
#             # The API returns a text field that is a JSON string, so we parse it
#             json_string = result["candidates"][0]["content"]["parts"][0]["text"]
#             return json.loads(json_string)
#         except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
#             print(f"Attempt {i+1} failed: {e}")
#             if i < 2:
#                 time.sleep(2 ** (i + 1))
#             else:
#                 return {"error": str(e)}

#     return {"error": "Failed to get a response from the API after multiple retries."}

# # --- Main script execution ---
# if __name__ == "__main__":
#     transcript_dir = r"C:\Users\MANASI\Desktop\Hackathon_project\src"
#     transcript_files = glob.glob(os.path.join(transcript_dir, "*_transcript.txt"))

#     if not transcript_files:
#         print(f"❌ No transcript files found in {transcript_dir}")
#     else:
#         all_outputs = {}

#         for transcript_path in transcript_files:
#             print(f"🔍 Analyzing {os.path.basename(transcript_path)} ...")
#             with open(transcript_path, "r", encoding="utf-8") as f:transcript_text = f.read()

# json_output = analyze_transcript_with_gemini(transcript_text, transcript_path)

# all_outputs[os.path.basename(transcript_path)] = json_output

#     # Save individual JSON
#     json_file = transcript_path.replace("_transcript.txt", ".json")
#             with open(json_file, "w", encoding="utf-8") as f:
#                 json.dump(json_output, f, indent=4, ensure_ascii=False)
#             print(f"💾 Saved individual JSON: {json_file}")

#         # Save combined JSON
#         combined_file = os.path.join(transcript_dir, "all_transcripts_output.json")
#         with open(combined_file, "w", encoding="utf-8") as f:
#             json.dump(all_outputs, f, indent=4, ensure_ascii=False)

#         print(f"✅ Combined JSON saved: {combined_file}")
import os
import json
import requests
import time
import glob


def analyze_transcript_with_gemini(transcript_text, audio_filename):
    """
    Analyzes a transcript using the Gemini API to find contradictions and
    synthesize the truth in the required JSON format.
    """
    api_key = "AIzaSyDY9r_y4jdZ1sIJFT3zSGVztrusmPD0oH4"  # <-- PUT YOUR GEMINI API KEY HERE
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


# --- Main script execution ---
if __name__ == "__main__":
    transcript_dir = "src"
    transcript_files = glob.glob(os.path.join(transcript_dir, "*_transcript.txt"))

    if not transcript_files:
        print(f"❌ No transcript files found in {transcript_dir}")
    else:
        all_outputs = {}

        for transcript_path in transcript_files:
            print(f"🔍 Analyzing {os.path.basename(transcript_path)} ...")

            # Read transcript text
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript_text = f.read()

            # Call Gemini
            json_output = analyze_transcript_with_gemini(transcript_text, transcript_path)

            # Store in combined output
            all_outputs[os.path.basename(transcript_path)] = json_output

            # Save individual JSON
            json_file = transcript_path.replace("_transcript.txt", ".json")
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(json_output, f, indent=4, ensure_ascii=False)
            print(f"💾 Saved individual JSON: {json_file}")

        # Save combined JSON
        combined_file = os.path.join(transcript_dir, "all_transcripts_output.json")
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(all_outputs, f, indent=4, ensure_ascii=False)

        print(f"✅ Combined JSON saved: {combined_file}")
