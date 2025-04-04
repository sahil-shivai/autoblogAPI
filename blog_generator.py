from google import generativeai as genai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set up your Gemini API Key
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Use Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_blog(title):
    print(f"📜 Generating content for: {title}")

    prompt = f"""
Write a detailed blog post on the topic: "{title}".
- Use an engaging and informative tone suitable for developers.
- Structure the blog with proper headings and subheadings.
- Include bullet points or code examples where helpful.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error generating blog: {e}")
        return None
