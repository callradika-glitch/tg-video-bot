from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
import random
import logging

# ================= CONFIG =================

BOT_TOKEN = os.getenv("BOT_TOKEN")   # SAFE for GitHub
ADMIN_ID = 7968582662
VIDEO_FILE = "videos.json"

# ===========================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_videos():
    if os.path.exists(VIDEO_FILE):
        try:
            with open(VIDEO_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"JSON error: {e}")
            return []
    return []

def save_videos(videos):
    with open(VIDEO_FILE, "w") as f:
        json.dump(videos, f)

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID and update.message.video:
        videos = load_videos()
        file_id = update.message.video.file_id

        if file_id not in videos:
            videos.append(file_id)
            save_videos(videos)
            await update.message.reply_text("Video saved automatically ✅")
        else:
            await update.message.reply_text("Video already saved.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to SS Videos Bot √")

async def videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    videos_list = load_videos()

    if videos_list:
        await update.message.reply_video(random.choice(videos_list))
    else:
        await update.message.reply_text("No videos available yet.")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.VIDEO, save_video))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("videos", videos))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
