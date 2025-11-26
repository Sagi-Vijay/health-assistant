import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def analyze_audio_file(file_path: str):
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    # Upload the file to Gemini
    audio_file = genai.upload_file(path=file_path)
    
    # Generate content
    prompt = "Listen to this audio. If it describes medical symptoms, analyze them and provide a summary. If it's a question, answer it. Do NOT provide medical advice."
    response = model.generate_content([prompt, audio_file])
    
    return response.text
