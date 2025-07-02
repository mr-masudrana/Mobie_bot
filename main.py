import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Load movie data from movies.json
def load_movies():
    with open('movies.json', 'r', encoding='utf-8') as f:
        return json.load(f)

movies = load_movies()

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎬 Welcome to Movie Bot!\n\nUse /search <movie name>\nUse /category to see categories")

# /search command
def search(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("❗ Usage: /search <movie name>")
        return

    query = " ".join(context.args).lower()
    result = [m for m in movies if query in m["title"].lower()]

    if not result:
        update.message.reply_text("🔍 No movie found.")
        return

    for m in result:
        update.message.reply_text(f"🎬 {m['title']} ({m['year']})\nCategory: {m['category']}\n🔗 {m['link']}")

# /category command
def category(update: Update, context: CallbackContext):
    cats = set(m['category'] for m in movies)
    cat_list = "\n".join(sorted(cats))
    update.message.reply_text(f"🎭 Available Categories:\n{cat_list}")

# Main function
def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN not found in environment.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("category", category))

    updater.start_polling()
    print("✅ Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
