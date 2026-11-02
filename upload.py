import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def run_automation():
    try:
        print("Generating script using Gemini...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Write a catchy YouTube Short title and 30-second script for ZZ LIGHTING COMPANY modern LED lights.")
        print("\n--- Generated Script ---")
        print(response.text)
        print("------------------------\n")
        print("Automation completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    run_automation()

