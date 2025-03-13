import telebot
from flask import Flask, request, jsonify
import os

TOKEN = "8017963270:AAGfnZri2gDA4By1F2LaodKYNG0ziW8CKZM"  # Replace with your bot token
WEBHOOK_URL = f"https://verceltest-psi-sable.vercel.app/{TOKEN}"  # Replace with your deployed Vercel URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Set webhook on startup
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    response = bot.set_webhook(url=WEBHOOK_URL)
    return jsonify({"webhook_set": response}), 200

# Handle incoming updates from Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"Error processing update: {e}")
        return "Error", 500

# Handle "/start" and "/hello" commands
@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot running on Vercel.")

# Default route for checking if the bot is running
@app.route("/")
def home():
    return "Bot is running!", 200

# Handle favicon.ico requests to avoid 404 errors
@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
