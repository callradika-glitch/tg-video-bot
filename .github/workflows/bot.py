import json
import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

VIDEO_FILE = "videos.json"

def load_videos():
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, "r") as f:
            return json.load(f)
    return []

def save_videos(videos):
    with open(VIDEO_FILE, "w") as f:
        json.dump(videos, f)

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video and update.message.from_user.id == ADMIN_ID:
        videos = load_videos()
        file_id = update.message.video.file_id

        if file_id not in videos:
            videos.append(file_id)
            save_videos(videos)
            await update.message.reply_text("Video saved ✅")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to SS Videos Bot √")

async def videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    videos_list = load_videos()

    if not videos_list:
        await update.message.reply_text("No videos available.")
        return

    await update.message.reply_video(random.choice(videos_list))

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("videos", videos))
    app.add_handler(MessageHandler(filters.VIDEO, save_video))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
