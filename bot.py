import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from flask import Flask
from threading import Thread

# ================= WEB SERVER =================
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)

# ================= CONFIG =================
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")

if not API_ID or not API_HASH or not SESSION:
    print("❌ Missing ENV!")
    exit()

# ================= BOT =================
app_bot = Client(
    "safe_userbot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    session_string=SESSION
)

# ================= MEMORY =================
last_replied = {}          # user_id : last_reply_time
cooldown_time = 1200        # 5 minutes
max_users_memory = 2000    # max users tracked safely

# ================= HANDLER =================
@app_bot.on_message(filters.private)
async def auto_reply(client, message):
    try:
        user_id = message.from_user.id
        now = time.time()

        print(f"📩 Message from {user_id}")

        # ===== Anti Spam Cooldown =====
        if user_id in last_replied and now - last_replied[user_id] < cooldown_time:
            print(f"⏳ Cooldown active for {user_id}, skipping...")
            return

        # ===== Human-like Delay =====
        await asyncio.sleep(2 + (user_id % 3))  # 2–4 sec delay

        # ===== Typing Action =====
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await asyncio.sleep(2)

        # ===== Pro-Level Auto Reply =====
        reply_text = (
            "👋 **আসসালামু আলাইকুম / Hello!**\n\n"
            "🤖 আমি **ᴜɴᴋɴᴏᴡɴ 〆 AI Assistant**\n\n"
            "📩 আপনার মেসেজটি সফলভাবে গ্রহণ করা হয়েছে ✅\n\n"
            "👤 Owner এই মুহূর্তে **offline / ব্যস্ত** আছেন 📴\n"
            "⏳ কিছু সময় অপেক্ষা করুন — খুব শীঘ্রই রিপ্লাই দেওয়া হবে ইনশাআল্লাহ।\n\n"
            "🙏 ধন্যবাদ আপনার ধৈর্যের জন্য ❤️"
        )

        # ===== Send Reply =====
        reply_msg = await message.reply_text(reply_text)

        # ===== Save Time =====
        last_replied[user_id] = now

        # ===== Memory Cleanup =====
        if len(last_replied) > max_users_memory:
            print("🧹 Memory cleanup: removing oldest users")
            oldest_users = sorted(last_replied.items(), key=lambda x: x[1])[:500]
            for u, _ in oldest_users:
                last_replied.pop(u)

        # ===== Check Owner Online & Delete Reply =====
        await asyncio.sleep(2)  # short delay before checking
        me = await client.get_me()
        if hasattr(me, 'status') and me.status == "online":
            try:
                await reply_msg.delete()
                print(f"✅ Reply deleted for {user_id} because owner is online")
            except Exception as e:
                print(f"⚠️ Could not delete reply: {e}")

        print(f"✅ Replied to {user_id}")

    except Exception as e:
        import traceback
        traceback.print_exc()

# ================= MAIN =================
if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    print("🚀 Safe Userbot Started (Owner Online Delete + DM Only)")
    app_bot.run()
