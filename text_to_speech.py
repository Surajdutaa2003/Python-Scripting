from gtts import gTTS
import pygame
import json
import os
import time

def text_to_speech(text, output_path="output.mp3", play_audio=True):
    try:
        # Generate speech
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        print(f"✅ Audio saved to {output_path}")

        # Optional playback
        if play_audio:
            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            print("🔊 Playing audio...")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        # Save checkpoint
        checkpoint = {
            "mode": "text-to-speech",
            "original_text": text,
            "characters": len(text),
            "output_file": output_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("tts_checkpoint.json", "w") as f:
            json.dump(checkpoint, f, indent=4)

        print("📌 Checkpoint saved to tts_checkpoint.json")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    text = input("Enter text: ").strip()
    if text:
        text_to_speech(text)
    else:
        print("⚠️ No text provided!")
