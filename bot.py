import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Render-er jonno Flask Server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ᴜɴᴋɴᴏᴡɴ 〆 ᴀɪ is Synchronized!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# --- Configuration ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")

# Client Initialize
client = Client("unknown_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# Auto-reply tracking
sent_messages = {}

@client.on_message(filters.private & ~filters.me)
async def auto_reply(bot, message):
    try:
        me = await bot.get_me()
        
        # User offline thakle reply jabe
        if me.status != "online":
            name = "ᴜɴᴋɴᴏᴡɴ 〆"
            response_text = (
                f"**Greetings from {name} ᴀɪ ⚡**\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                "**ꜱᴛᴀᴛᴜꜱ:** `User is currently beyond reach` 📡\n"
                "**ʟᴏɢ:** `Message received & secured.`\n\n"
                "**ɪɴꜰᴏ:** _This AI will alert the user once he re-establishes connection. "
                "This trace will be auto-deleted soon._\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                "**ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴜɴᴋɴᴏᴡɴ ᴄᴏʀᴘ™**"
            )
            
            reply = await message.reply(response_text)
            sent_messages[message.chat.id] = reply.id
            
    except Exception as e:
        print(f"Error in reply: {e}")

@client.on_user_status()
async def delete_on_online(bot, update):
    try:
        me = await bot.get_me()
        if update.id == me.id and update.status == "online":
            # Online ashar por sob auto-reply gulo delete hobe
            for chat_id, msg_id in list(sent_messages.items()):
                try:
                    await bot.delete_messages(chat_id, msg_id)
                    del sent_messages[chat_id]
                except:
                    pass
    except Exception as e:
        print(f"Error in deletion: {e}")

# --- Python 3.14 Version Fix & Main Execution ---
async def start_bot():
    await client.start()
    print(">>> ᴜɴᴋɴᴏᴡɴ 〆 ᴀɪ ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ <<<")
    # Loop-ke active rakhar jonno
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Render-er jonno Web Thread start
    Thread(target=run_web, daemon=True).start()
    
    # Python-er version issue handle korar jonno asyncio run
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
