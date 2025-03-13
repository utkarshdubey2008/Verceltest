import telebot
from flask import Flask, request

TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot running on Vercel.")

@app.route("/")
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(debug=True)
