import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Render-er jonno Web Server (Bot-ke online rakhar jonno) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ᴜɴᴋɴᴏᴡɴ 〆 AI is active!"

def run_web():
    # Render default port 5000 use kore, na pele 5000 set hobe
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# --- Telegram Client Setup ---
# Environment Variables theke data nibe
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")

client = Client("unknown_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# Auto-reply message track korar jonno
sent_messages = {}

@client.on_message(filters.private & ~filters.me)
async def auto_reply(bot, message):
    try:
        me = await bot.get_me()
        
        # Jodi tumi online na thako (Offline/Last Seen)
        if me.status != "online":
            # Futuristic AI Message Style
            response_text = (
                "**SYSTEM: ᴜɴᴋɴᴏᴡɴ 〆 ᴀɪ ⚡**\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                "**sᴛᴀᴛᴜs:** `ᴜɴᴋɴᴏᴡɴ 〆 ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴏғғʟɪɴᴇ` 💤\n"
                "**ᴍᴇssᴀɢᴇ:** _Your message has been logged._\n\n"
                "**ɴᴏᴛᴇ:** ɪ ᴡɪʟʟ ɴᴏᴛɪғʏ ʜɪᴍ ᴀs sᴏᴏɴ ᴀs ʜᴇ ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ. ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ sᴇʟғ-ᴅᴇsᴛʀᴜᴄᴛᴇᴅ ᴛʜᴇɴ. 🛡️\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼"
            )
            
            # Message send korbe
            reply = await message.reply(response_text)
            # Message ID store korbe jate pore delete kora jay
            sent_messages[message.chat.id] = reply.id
            
    except Exception as e:
        print(f"Error in auto_reply: {e}")

@client.on_user_status()
async def delete_on_online(bot, update):
    try:
        me = await bot.get_me()
        # Nijer status check korbe
        if update.id == me.id:
            if update.status == "online":
                # Online houar por sob auto-replies delete hobe
                for chat_id, msg_id in list(sent_messages.items()):
                    try:
                        await bot.delete_messages(chat_id, msg_id)
                        del sent_messages[chat_id]
                    except:
                        pass
    except Exception as e:
        print(f"Error in status_update: {e}")

# --- Execution ---
if __name__ == "__main__":
    # Flask server-ke alada thread-e run kora jate Render bondho na hoy
    Thread(target=run_web).start()
    # Telegram client start
    print("Starting ᴜɴᴋɴᴏᴡɴ 〆 Userbot...")
    client.run()
