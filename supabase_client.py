from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_blog(title, content, word, image_url):
    data = {
        "title": title,
        "content": content,
        "word": word,
        "image_url": image_url
    }

    response = supabase.table("blogs").insert(data).execute()

    if response.data:
        print(f"✅ Saved: {title}")
    else:
        print(f"❌ Error: {response.error}")


def get_all_blogs(limit=10):
    response = supabase.table("blogs").select(
        "*").order("created_at", desc=True).limit(limit).execute()
    return response.data


if __name__ == "__main__":
    save_blog("Test Blog", "This is a test content.",
              "Python", "https://testimage.jpg")
