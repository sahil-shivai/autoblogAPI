import time
import random
import threading
import os
import subprocess
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from scrapper import get_blog_titles
from blog_generator import generate_blog
from supabase_client import save_blog, get_all_blogs  # Add get_all_blogs function

# Install Playwright dependencies (only runs once)
subprocess.run(["playwright", "install", "--with-deps"], check=True)

# Keywords for blog generation
KEYWORDS = ["Python", "Web Development",
            "Scraping", "AI", "JavaScript", "Data Science"]


def get_random_keyword():
    """Return a random keyword from the predefined list."""
    return random.choice(KEYWORDS)


def generate_and_store_blogs():
    """Fetch blog titles and generate content using AI."""
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
        image_url = None  # Image fetching is disabled for now

        if content:
            save_blog(title, content, keyword, image_url)
            count += 1

        time.sleep(2)  # Avoid API rate limits
        if count >= 10:
            break  # Max 10 blogs per run


def start_scheduler():
    """Start the background scheduler for periodic blog generation."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_and_store_blogs, 'interval', hours=12)
    scheduler.start()
    print("⏳ Scheduler started. Blogs will be generated every 12 hours.")
    generate_and_store_blogs()  # Initial run


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.route("/api/blogs", methods=["GET"])
    def fetch_blogs():
        """Fetch all stored blogs from the database."""
        try:
            blogs = get_all_blogs()
            return jsonify({"status": "success", "blogs": blogs}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Start the scheduler in a separate thread
    threading.Thread(target=start_scheduler, daemon=True).start()

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 10000))  # Use Render's provided port
    app.run(host="0.0.0.0", port=port)
