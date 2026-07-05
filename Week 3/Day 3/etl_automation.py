import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client using the API key from the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_cv_data(raw_text):
    """
    Sends raw, unclean CV text to OpenAI and enforces a structured JSON response.
    """
    prompt = f"Extract and clean the student CV information from the following text: {raw_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Highly cost-effective and accurate for formatting tasks
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert data assistant. Extract student details cleanly. If a field is entirely missing or unknown, use an empty string."
                },
                {"role": "user", "content": prompt}
            ],
            # Enforce a strict JSON structure matching your CSV requirements
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "student_cv_schema",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "Student ID": {"type": "string"},
                            "Full Name": {"type": "string"},
                            "Email": {"type": "string"},
                            "Phone Number": {"type": "string"},
                            "Course": {"type": "string"},
                            "Fee Paid": {"type": "string"},
                            "City": {"type": "string"},
                            "Enrolled Date": {"type": "string"}
                        },
                        "required": ["Student ID", "Full Name", "Email", "Phone Number", "Course", "Fee Paid", "City", "Enrolled Date"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        # Pyrefly Fix: Extract content and verify it's not None before parsing
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI returned an empty response.")
            
        return json.loads(content)
        
    except Exception as e:
        print(f"\n[ERROR] Failed to process row: {e}")
        # Fallback empty structure so the script doesn't crash mid-run
        return {
            "Student ID": "", "Full Name": "", "Email": "", "Phone Number": "", 
            "Course": "", "Fee Paid": "", "City": "", "Enrolled Date": ""
        }

def main():
    # File configuration updated with your exact filename
    input_file = "student_enrollment_raw.csv"  
    output_file = "student_enrollment_clean.csv"   
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Could not find the file '{input_file}'. Please check the path.")
        return

    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} rows from '{input_file}'.")

    cleaned_data_list = []
    print("\nStarting AI data cleaning process...")
    
    # Pyrefly Fix: Using native enumerate() gives a clean integer counter starting at 1
    for count, (index, row) in enumerate(df.iterrows(), start=1):
        
        # Combine row elements into a clear string for the AI to fix/clean
        raw_content = (
            f"ID: {row.get('Student_ID')}, Name: {row.get('Name')}, Email: {row.get('Email')}, "
            f"Phone: {row.get('Phone')}, Course: {row.get('Course')}, Fee: {row.get('Fee_Paid')}, "
            f"City: {row.get('City')}, Date: {row.get('Enrolled_Date')}"
        )
        
        print(f" -> Processing student {count}/{len(df)}...", end="\r")
        
        cleaned_row = clean_cv_data(raw_content)
        cleaned_data_list.append(cleaned_row)

    print("\nAI Processing complete. Structuring final dataset...")

    # Convert the list of cleaned rows into a DataFrame and save as CSV
    clean_df = pd.DataFrame(cleaned_data_list)
    clean_df.to_csv(output_file, index=False)
    
    print(f"Success! The clean file has been saved to '{output_file}'.")

if __name__ == "__main__":
    main()