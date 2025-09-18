from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import json
from truth_weaver_module import analyze_transcript_with_gemini

app = Flask(__name__)
CORS(app)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Truth Weaver Backend is running"})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file to text
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            # Convert and optimize audio for speech recognition
            try:
                # First, try to load the audio file
                audio = AudioSegment.from_file(temp_file.name)
                
                # Optimize audio: convert to mono, 16kHz sample rate, normalize volume
                audio = audio.set_channels(1)  # Convert to mono
                audio = audio.set_frame_rate(16000)  # Set to 16kHz sample rate
                audio = audio.normalize()  # Normalize volume
                
                # Export as WAV (most compatible format)
                wav_path = temp_file.name.replace('.wav', '_converted.wav')
                audio.export(wav_path, format="wav", parameters=["-ac", "1", "-ar", "16000"])
                
                print(f"Audio converted successfully: {wav_path}")
                
            except Exception as audio_error:
                print(f"Audio conversion failed: {audio_error}")
                # If conversion fails, try to use the original file
                wav_path = temp_file.name
                
                # If original file isn't WAV, try basic ffmpeg conversion
                if not temp_file.name.endswith('.wav'):
                    import subprocess
                    try:
                        wav_path = temp_file.name.replace('.wav', '_ffmpeg.wav')
                        subprocess.run([
                            'ffmpeg', '-i', temp_file.name, 
                            '-ac', '1', '-ar', '16000', 
                            '-y', wav_path
                        ], check=True, capture_output=True)
                        print(f"FFmpeg conversion successful: {wav_path}")
                    except subprocess.CalledProcessError:
                        print("FFmpeg conversion also failed, using original file")
                        wav_path = temp_file.name
            
            # Use speech recognition with improved settings
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300  # Adjust for noise
            recognizer.dynamic_energy_threshold = True
            
            try:
                with sr.AudioFile(wav_path) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    
                    # Try Google Speech Recognition with language specification
                    try:
                        transcript = recognizer.recognize_google(audio_data, language='en-US')
                    except sr.UnknownValueError:
                        # Fallback: try without language specification
                        transcript = recognizer.recognize_google(audio_data)
                
                # Clean up temp files
                os.unlink(temp_file.name)
                if wav_path != temp_file.name:
                    os.unlink(wav_path)
                
                return jsonify({
                    "transcript": transcript,
                    "success": True
                })
            
            except sr.UnknownValueError:
                return jsonify({"error": "Could not understand audio"}), 400
            except sr.RequestError as e:
                return jsonify({"error": f"Speech recognition service error: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"error": f"Audio processing error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze_transcript():
    """
    Analyze transcript using Truth Weaver AI
    """
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({"error": "No transcript provided"}), 400
        
        transcript_text = data['transcript']
        filename = data.get('filename', 'uploaded_audio')
        
        # Use the existing Truth Weaver analysis
        analysis_result = analyze_transcript_with_gemini(transcript_text, filename)
        
        if 'error' in analysis_result:
            return jsonify({"error": analysis_result['error']}), 500
        
        return jsonify({
            "analysis": analysis_result,
            "success": True
        })
    
    except Exception as e:
        return jsonify({"error": f"Analysis error: {str(e)}"}), 500

@app.route('/transcribe-and-analyze', methods=['POST'])
def transcribe_and_analyze():
    """
    Combined endpoint: transcribe audio and analyze in one request
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Transcribe audio (reuse logic from transcribe endpoint)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            try:
                # First, try to load the audio file
                audio = AudioSegment.from_file(temp_file.name)
                
                # Optimize audio: convert to mono, 16kHz sample rate, normalize volume
                audio = audio.set_channels(1)  # Convert to mono
                audio = audio.set_frame_rate(16000)  # Set to 16kHz sample rate
                audio = audio.normalize()  # Normalize volume
                
                # Export as WAV (most compatible format)
                wav_path = temp_file.name.replace('.wav', '_converted.wav')
                audio.export(wav_path, format="wav", parameters=["-ac", "1", "-ar", "16000"])
                
            except Exception as audio_error:
                print(f"Audio conversion failed: {audio_error}")
                # If conversion fails, try to use the original file
                wav_path = temp_file.name
                
                # If original file isn't WAV, try basic ffmpeg conversion
                if not temp_file.name.endswith('.wav'):
                    import subprocess
                    try:
                        wav_path = temp_file.name.replace('.wav', '_ffmpeg.wav')
                        subprocess.run([
                            'ffmpeg', '-i', temp_file.name, 
                            '-ac', '1', '-ar', '16000', 
                            '-y', wav_path
                        ], check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        wav_path = temp_file.name
            
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            
            try:
                with sr.AudioFile(wav_path) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    
                    # Try Google Speech Recognition with language specification
                    try:
                        transcript = recognizer.recognize_google(audio_data, language='en-US')
                    except sr.UnknownValueError:
                        # Fallback: try without language specification
                        transcript = recognizer.recognize_google(audio_data)
                
                # Analyze transcript
                analysis_result = analyze_transcript_with_gemini(transcript, audio_file.filename)
                
                # Clean up temp files
                os.unlink(temp_file.name)
                if wav_path != temp_file.name:
                    os.unlink(wav_path)
                
                return jsonify({
                    "transcript": transcript,
                    "analysis": analysis_result,
                    "success": True
                })
            
            except sr.UnknownValueError:
                return jsonify({"error": "Could not understand audio"}), 400
            except sr.RequestError as e:
                return jsonify({"error": f"Speech recognition service error: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"error": f"Processing error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)