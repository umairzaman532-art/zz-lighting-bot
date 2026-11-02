
import os
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from PIL import Image, ImageDraw, ImageFont
import subprocess

# 1. Gemini API سیٹ اپ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_lighting_script():
    prompt = "Write a short, engaging YouTube description and script about modern LED ceiling lights for ZZ LIGHTING COMPANY."
    
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception:
                continue
                
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 2. اسکرپٹ سے خودکار ویڈیو (MP4) بنانے کا فنکشن
def create_video_from_script(script_text):
    print("Creating video from script...")
    
    # ایک سادہ تصویر بنانا جس پر زیڈ زی लाइٹنگ لکھا ہو
    img = Image.new('RGB', (1080, 1920), color=(15, 15, 30))
    d = ImageDraw.Draw(img)
    
    # ٹیکسٹ کو تصاویر پر سیٹ کرنا (پہلے چند جملے)
    lines = script_text.split('\n')
    text_to_show = "\n".join([line for line in lines if line.strip()][:5])
    
    d.text((50, 200), "ZZ LIGHTING COMPANY", fill=(255, 215, 0))
    d.text((50, 400), text_to_show, fill=(255, 255, 255))
    
    image_path = "temp_slide.png"
    img.save(image_path)
    
    # تصویر کو ویڈیو میں بدلنے کے لیے کمانڈ (FFmpeg کے ذریعے)
    video_path = "output_video.mp4"
    cmd = [
        "ffmpeg", "-loop", "1", "-i", image_path, 
        "-t", "10", "-pix_fmt", "yuv420p", 
        "-vf", "scale=1080:1920", video_path, "-y"
    ]
    
    subprocess.run(cmd, check=True)
    print("Video created successfully:", video_path)
    return video_path

# 3. YouTube Upload سیٹ اپ
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
    
    # ویڈیو بنانا
    video_file = create_video_from_script(script_text)
    
    # یوٹیوب پر اپ لوڈ کرنا (جب آپ کے پاس گٹ ہب سیکریٹس میں ٹوکنز ایڈ ہوں)
    # upload_to_youtube(video_file, "ZZ Lighting Company - Modern LED Lights", script_text)
