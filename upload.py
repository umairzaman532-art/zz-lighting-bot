import os
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 1. Gemini API سیٹ اپ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_lighting_script():
    prompt = "Write a short, engaging YouTube description and script about modern LED ceiling lights for ZZ LIGHTING COMPANY."
    
    # یہاں ہم خودکار طریقے سے چیک کرتے ہیں کہ کون سا ماڈل دستیاب ہے
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception:
                continue
                
    # اگر اوپر والا لوپ نہ چلے تو یہ فکسڈ ماڈل استعمال ہوگا
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 2. YouTube Upload سیٹ اپ
def upload_to_youtube(video_file_path, title, description):
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["ZZ Lighting", "LED Lights", "Modern Ceiling Lights"],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")
    
    print("Video uploaded successfully!")

if __name__ == "__main__":
    print("Generating script with Gemini...")
    script_text = generate_lighting_script()
    print("Generated Script:\n", script_text)
