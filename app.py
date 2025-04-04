import time
import random
import threading
from flask import Flask, jsonify
# Use background scheduler for Flask
from apscheduler.schedulers.background import BackgroundScheduler
from scrapper import get_blog_titles
from blog_generator import generate_blog
# from image_fetcher import fetch_image  # Disabled for now
from supabase_client import save_blog, get_all_blogs  # Add get_all_blogs function

# Keywords for generation
KEYWORDS = ["Python", "Web Development",
            "Scraping", "AI", "JavaScript", "Data Science"]

# Flask App
app = Flask(__name__)

# Utility: Random keyword


def get_random_keyword():
    return random.choice(KEYWORDS)

# Blog Generator Job


def generate_and_store_blogs():
    keyword = get_random_keyword()
    print(f"\n🔄 Using Keyword: {keyword}")

    titles = get_blog_titles(keyword)
    if not titles:
        print("❌ No titles found!")
        return

    count = 0
    for title in titles:
        print(f"📝 Generating blog: {title}")
        content = generate_blog(title)
        image_url = None  # Temporarily disabled

        if content:
            save_blog(title, content, keyword, image_url)
            count += 1

        time.sleep(2)  # Avoid API rate limits
        if count >= 10:
            break  # Max 10 blogs per run

# API Route


@app.route("/api/blogs", methods=["GET"])
def fetch_blogs():
    try:
        blogs = get_all_blogs()
        return jsonify({"status": "success", "blogs": blogs}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Start scheduler in background thread


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_and_store_blogs, 'interval', hours=12)
    scheduler.start()
    print("⏳ Scheduler started. Blogs will be generated every 12 hours.")
    generate_and_store_blogs()  # Initial run


# Main
if __name__ == "__main__":
    # Run scheduler in background
    threading.Thread(target=start_scheduler).start()
    app.run(debug=True, port=5000)
