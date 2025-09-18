
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

try:
    import whisper  # openai-whisper package
except ImportError as e:
    raise SystemExit("Whisper package not installed. Run: pip install openai-whisper") from e

def transcribe_and_label_audio(audio_file_path, model):
    """Transcribes an audio file with silence-based segmentation.
       Falls back to full file if no chunks detected.
    """
    try:
        audio = AudioSegment.from_file(audio_file_path)
    except Exception as e:
        print(f"❌ Error loading {audio_file_path}: {e}")
        return None

    print(f"\n🔊 Processing {os.path.basename(audio_file_path)}...")

    try:
        audio_chunks = split_on_silence(
            audio,
            min_silence_len=500,
            silence_thresh=-40
        )
    except Exception as e:
        print(f"❌ Error splitting audio: {e}")
        return None

    final_transcript = ""
    speaker_id = "Speaker"

    if not audio_chunks:
        print("⚠ No chunks detected → transcribing full file instead...")
        temp_file = f"full-{os.getpid()}.wav"
        audio.export(temp_file, format="wav")
        result = model.transcribe(temp_file)
        final_transcript += f"{speaker_id}: {result['text']}\n"
        os.remove(temp_file)
        return final_transcript

    print(f"✅ Found {len(audio_chunks)} chunks. Transcribing...")

    for i, chunk in enumerate(audio_chunks):
        temp_file = f"chunk-{os.getpid()}-{i}.wav"
        chunk.export(temp_file, format="wav")
        result = model.transcribe(temp_file)
        final_transcript += f"{speaker_id}: {result['text']}\n"

        os.remove(temp_file)

    return final_transcript


if __name__ == "__main__":
    import os
    model_name = "base"
    print(f"⏳ Loading Whisper model '{model_name}' ...")
    try:
        model = whisper.load_model(model_name)
    except AttributeError:
        raise SystemExit(
            "AttributeError: 'whisper' has no attribute 'load_model'.\n"
            "This usually means you installed the wrong package.\n"
            "Fix with: pip uninstall whisper -y && pip install openai-whisper"
        )

    # Supported audio extensions
    exts = [".wav", ".mp3", ".mp4", ".m4a", ".flac", ".ogg", ".webm"]
    base_dir = os.path.dirname(__file__)
    audio_dir = os.path.join(base_dir, "audio")
    transcript_dir = os.path.join(base_dir, "transcript")
    os.makedirs(transcript_dir, exist_ok=True)
    # Find all supported audio files in src/audio/
    audio_files = [
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if os.path.splitext(f)[1].lower() in exts
    ]
    audio_files.sort()  # Alphabetical order for reproducibility

    if not audio_files:
        print("No supported audio files found in analysis/audio/. Nothing to transcribe.")
        exit(0)

    combined_segments = []  # (session_index, header, transcript_text)

    for idx, audio_path in enumerate(audio_files, start=1):
        transcript = transcribe_and_label_audio(audio_path, model)
        file_name_without_ext = os.path.splitext(os.path.basename(audio_path))[0]
        output_file = os.path.join(transcript_dir, f"{file_name_without_ext}_transcript.txt")
        if transcript:
            # Include session header at top of individual file too
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Session {idx}: {file_name_without_ext}\n\n{transcript}")
            print(f"💾 Transcript saved: {output_file}")
            combined_segments.append((idx, file_name_without_ext, transcript))
        else:
            print(f"⚠ No transcript generated for {os.path.basename(audio_path)}")

    # Write combined multi-session transcript if we have at least one segment
    if combined_segments:
        combined_filename = os.path.join(transcript_dir, "combined_sessions_transcript.txt")
        combined_segments.sort(key=lambda x: x[0])
        with open(combined_filename, "w", encoding="utf-8") as cf:
            for session_index, base_name, text in combined_segments:
                cf.write(f"===== Session {session_index}: {base_name} =====\n")
                cf.write(text.strip() + "\n\n")
        print(
            f"✅ Combined multi-session transcript written: {combined_filename}\n"
            "Hint: This file is suitable for hackathon submission (contains Session headers for all detected files)."
        )
    else:
        print("⚠ No sessions transcribed; combined transcript not created.")
