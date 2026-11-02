
import os
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Generating script using Gemini...")

# Initialize the updated model
model = genai.GenerativeModel('gemini-2.5-flash')

# Generate content
response = model.generate_content("Write a short, engaging description for a modern LED ceiling light from ZZ LIGHTING COMPANY.")
print(response.text)

# Add your YouTube upload logic below this line if needed
