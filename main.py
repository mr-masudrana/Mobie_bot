import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def load_movies():
    with open("movies.json", "r", encoding="utf-8") as f:
        return json.load(f)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎬 Welcome to Movie Bot!\n\n"
        "Use /search movie_name to find a movie.\n"
        "Use /category to see available categories."
    )

def search(update: Update, context: CallbackContext):
    query = ' '.join(context.args).lower()
    movies = load_movies()
    found = False
    for movie in movies:
        if query in movie['title'].lower():
            update.message.reply_text(
                f"🎞️ *{movie['title']}*\n"
                f"📁 Category: {movie['category']}\n"
                f"🔗 [Watch/Download]({movie['link']})",
                parse_mode="Markdown"
            )
            found = True
    if not found:
        update.message.reply_text("❌ Movie not found.")

def category(update: Update, context: CallbackContext):
    movies = load_movies()
    categories = sorted(set(m['category'] for m in movies))
    update.message.reply_text("📚 Available Categories:\n" + '\n'.join(f"• {c}" for c in categories))

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN environment variable not set.")
        return
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("category", category))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
