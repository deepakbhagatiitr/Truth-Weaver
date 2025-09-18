
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import whisper

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
    os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-8.0-essentials_build\bin"

    audio_files = [
        r"C:\Users\MANASI\Desktop\Hackathon_project\src\rehearsed_evasion.wav",
        r"C:\Users\MANASI\Desktop\Hackathon_project\src\selfcorrect_contradictions.wav",
        r"C:\Users\MANASI\Desktop\Hackathon_project\src\buried_confession.wav",
        r"C:\Users\MANASI\Desktop\Hackathon_project\src\drifted_anecdote.wav",
        r"C:\Users\MANASI\Desktop\Hackathon_project\src\hedge_and_dodge.wav",
    ]

    print("⏳ Loading Whisper model...")
    model = whisper.load_model("base")

    for audio_path in audio_files:
        if os.path.exists(audio_path):
            transcript = transcribe_and_label_audio(audio_path, model)
            if transcript:
                file_name_without_ext = os.path.splitext(os.path.basename(audio_path))[0]
                output_file = f"{file_name_without_ext}_transcript.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(transcript)
                print(f"💾 Transcript saved: {output_file}")
            else:
                print(f"⚠ No transcript generated for {os.path.basename(audio_path)}")
        else:
            print(f"❌ File not found: {audio_path}")
