
              
import os
from flask import Flask, jsonify, request
import openai
import urllib.parse

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "ZZ LIGHTING COMPANY Complete YouTube Automation Bot is Active!"

@app.route('/run-complete-automation', methods=['POST'])
def run_automation():
    try:
        # Step 1: ChatGPT se script generate karwana
        response = openai.ChatCompletion.create(
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
        
        return jsonify({
            "status": "success",
            "brand": "ZZ LIGHTING COMPANY",
            "generated_script": ai_output
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
