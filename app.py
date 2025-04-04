import time
import random
import threading
import subprocess
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from scrapper import get_blog_titles
from blog_generator import generate_blog
from supabase_client import save_blog, get_all_blogs  # Added get_all_blogs function

# Install Playwright dependencies (ensures browser installation)
subprocess.run(["playwright", "install", "--with-deps"], check=True)

# Keywords for blog generation
KEYWORDS = ["Python", "Web Development",
            "Scraping", "AI", "JavaScript", "Data Science"]

# Flask App
app = Flask(__name__)

# Utility: Get a random keyword


def get_random_keyword():
    return random.choice(KEYWORDS)

# Blog Generator Job


def generate_and_store_blogs():
    keyword = get_random_keyword()
    print(f"\n🔄 Using Keyword: {keyword}")

    try:
        titles = get_blog_titles(keyword)
        if not titles:
            print("❌ No blog titles found! Skipping...")
            return

        count = 0
        for title in titles:
            print(f"📝 Generating blog: {title}")
            content = generate_blog(title)
            image_url = None  # Image fetching is currently disabled

            if content:
                save_blog(title, content, keyword, image_url)
                count += 1

            time.sleep(2)  # Prevent API rate limits
            if count >= 10:
                break  # Limit to 10 blogs per run

    except Exception as e:
        print(f"⚠️ Error in blog generation: {str(e)}")

# API Route - Fetch All Blogs


@app.route("/api/blogs", methods=["GET"])
def fetch_blogs():
    try:
        blogs = get_all_blogs()
        return jsonify({"status": "success", "blogs": blogs}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Start Scheduler in Background


def start_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(generate_and_store_blogs, 'interval', hours=12)
        scheduler.start()
        print("⏳ Scheduler started. Blogs will be generated every 12 hours.")

        # Run the job immediately on startup
        generate_and_store_blogs()

    except Exception as e:
        print(f"⚠️ Error starting scheduler: {str(e)}")


# Main Entry Point
if __name__ == "__main__":
    # Run scheduler in background thread
    threading.Thread(target=start_scheduler).start()
    app.run(debug=True, port=5000)
