from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess


def run_blog_generator():
    subprocess.run(["python", "app.py"])


scheduler = BlockingScheduler()
scheduler.add_job(run_blog_generator, "interval", hours=12)

print("🚀 Scheduler started! Running every 12 hours...")
scheduler.start()
