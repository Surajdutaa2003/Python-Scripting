import pandas as pd
import json
import os

def json_to_csv(json_path, output_path="output.csv"):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        
        checkpoint = {"original_json": json_path, "rows": len(df), "columns": len(df.columns), "output_file": output_path}
        with open("json_csv_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"CSV saved to {output_path}. Checkpoint saved.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    json_file = input("Enter JSON path: ")
    if os.path.exists(json_file):
        json_to_csv(json_file)
    else:
        print("JSON file not found!")