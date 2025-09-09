import requests
import json
import logging
import time
import os
from dotenv import load_dotenv

# .env file se variables load karo
load_dotenv()

# Environment variables se ENDPOINT aur API_KEY lo
ENDPOINT = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("API_KEY")

# Check karo ki variables set hain
if not ENDPOINT or not API_KEY:
    print("Error: API_ENDPOINT ya API_KEY .env file mein nahi hai!")
    exit(1)

# Logging setup karo
logging.basicConfig(filename="comparator_log.txt", level=logging.INFO)

def compare_texts(content_text, transcript_text, max_retries=3):
    """
    Do texts ko compare karta hai using API aur results return karta hai.
    """
    logging.info("Checkpoint 1: Starting comparison")

    # Headers set karo, senior ke code ke jaisa
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    # Simple prompt, senior ke prompt se inspired
    prompt = """
You are an expert in text comparison. Compare two texts for semantic equivalence.
Focus on core meaning. Highlight differences with **double asterisks**.

Response Format:
json
{
  "Match": true/false,
  "Content_Diff": "Full content with differences in **double asterisks**",
  "Transcript_Diff": "Full transcript with differences in **double asterisks**"
}
"""

    # Payload banayo
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Content Text:\n{content_text}\n\nTranscript Text:\n{transcript_text}"
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "top_p": 0.5,
        "max_tokens": 1000
    }

    # Retries ke saath API call
    for attempt in range(max_retries):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            json_response = json.loads(content)
            match = json_response['Match']
            content_diff = json_response['Content_Diff']
            transcript_diff = json_response['Transcript_Diff']
            logging.info("Checkpoint 2: Comparison done")
            return match, content_diff, transcript_diff

        except Exception as e:
            logging.error(f"Attempt {attempt + 1}: Error - {e}")
            if attempt < max_retries - 1:
                time.sleep(1)

    logging.error("All retries failed")
    return None, None, None

# Main program
print("Simple Text Comparator: Enter two texts to compare (or 'exit' to stop)")
checkpoint_count = 1

while True:
    content_text = input("Enter Content Text: ")
    if content_text.lower() == "exit":
        break

    transcript_text = input("Enter Transcript Text: ")
    if transcript_text.lower() == "exit":
        break

    if not content_text.strip() or not transcript_text.strip():
        print("Error: Texts khali hain!")
        logging.error("Checkpoint: Empty input")
        continue

    # Compare karo
    match, content_diff, transcript_diff = compare_texts(content_text, transcript_text)

    if match is not None:
        # Checkpoint save karo
        checkpoint_file = f"comparison_checkpoint_{checkpoint_count}.json"
        with open(checkpoint_file, "w") as f:
            json.dump({
                "match": match,
                "content_diff": content_diff,
                "transcript_diff": transcript_diff,
                "original_content": content_text,
                "original_transcript": transcript_text
            }, f)
        logging.info(f"Checkpoint 3: Saved to {checkpoint_file}")
        print(f"Checkpoint saved to {checkpoint_file}")
        print(f"Match: {match}")
        print(f"Content Diff: {content_diff}")
        print(f"Transcript Diff: {transcript_diff}")
        checkpoint_count += 1
    else:
        print("Comparison failed after retries")

print("thankyou for vsisting")