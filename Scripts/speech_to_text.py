import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import json
import os

# Optional: point directly to ffmpeg if not in PATH
AudioSegment.converter = which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe   = which("ffprobe") or r"C:\ffmpeg\bin\ffprobe.exe"

def convert_to_wav(input_path):
    """Convert mp3/m4a to wav if needed and return wav path"""
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".wav":
        return input_path  # already wav
    
    wav_path = "converted_audio.wav"
    audio = AudioSegment.from_file(input_path)
    audio.export(wav_path, format="wav")
    print(f"Converted {input_path} -> {wav_path}")
    return wav_path

def speech_to_text(audio_path, output_path="transcribed_text.txt"):
    try:
        wav_path = convert_to_wav(audio_path)

        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        checkpoint = {
            "mode": "file",
            "original_audio": audio_path,
            "converted_audio": wav_path,
            "transcribed_text_length": len(text),
            "output_file": output_path
        }
        with open("speech_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"[File] Text transcribed to {output_path}. Checkpoint saved.")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

def mic_to_text(output_path="mic_transcribed_text.txt"):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Speak now... (press Ctrl+C to stop)")
            r.adjust_for_ambient_noise(source)  # reduce background noise
            audio = r.listen(source)
        
        text = r.recognize_google(audio)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        checkpoint = {
            "mode": "microphone",
            "transcribed_text_length": len(text),
            "output_file": output_path
        }
        with open("speech_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"[Mic] Text transcribed to {output_path}. Checkpoint saved.")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    choice = input("Do you want to transcribe a file or record from mic? (file/mic): ").lower()
    
    if choice == "file":
        audio_file = input("Enter audio path (WAV/MP3/M4A): ")
        if os.path.exists(audio_file):
            speech_to_text(audio_file)
        else:
            print("Audio file not found!")
    elif choice == "mic":
        mic_to_text()
    else:
        print("Invalid choice!")
