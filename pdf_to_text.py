import PyPDF2
import json
import os

def pdf_to_text(pdf_path, output_path="output.txt"):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Checkpoint: JSON save
        checkpoint = {"original_pdf": pdf_path, "extracted_text_length": len(text), "output_file": output_path}
        with open("pdf_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"Text extracted to {output_path}. Checkpoint saved.")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage
if __name__ == "__main__":
    pdf_file = input("Enter PDF path: ")
    if os.path.exists(pdf_file):
        pdf_to_text(pdf_file)
    else:
        print("PDF file not found!")