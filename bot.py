import os
import time
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Render Port Binding (Flask) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Running!"

def run_web():
    # Render-এর জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- Bot Configuration ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")

# ক্লায়েন্ট সেটআপ
app_bot = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

# রিপ্লাই মেমোরি (যাতে স্প্যাম না হয়)
last_replied = {}

@app_bot.on_message(filters.private & ~filters.me & ~filters.bot)
async def auto_reply_handler(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    # একই মানুষকে ৫ মিনিটের মধ্যে বারবার রিপ্লাই দিবে না
    if user_id in last_replied and (current_time - last_replied[user_id] < 300):
        return

    try:
        # টাইপিং ইফেক্ট
        await client.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(2) 

        # মেসেজ টেক্সট
        reply_text = (
            "**👋 Hello! I am ᴜɴᴋɴᴏᴡɴ 〆 AI.**\n\n"
            "My owner is currently offline or busy. 📴\n"
            "Your message has been received. Please wait for a while! ⏳"
        )

        await message.reply_text(reply_text)
        last_replied[user_id] = current_time
        print(f"Successfully replied to {user_id}")

    except Exception as e:
        print(f"Error while replying: {e}")

if __name__ == "__main__":
    # ওয়েব সার্ভার চালু করা (Render-কে সজাগ রাখতে)
    Thread(target=run_web, daemon=True).start()
    
    # বট রান করা
    print(">>> ᴜɴᴋɴᴏᴡɴ 〆 AI starting now...")
    app_bot.run()
