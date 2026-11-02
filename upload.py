import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_automation():
    try:
        print("Generating script using ChatGPT...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are the official content creator for ZZ LIGHTING COMPANY."
                },
                {
                    "role": "user",
                    "content": "Create a catchy YouTube Short title and a 30-second script about LED lighting."
                }
            ]
        )
        ai_output = response.choices[0].message.content
        print("\n--- Generated Script ---")
        print(ai_output)
        print("------------------------\n")
        print("Automation completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    run_automation()
    
