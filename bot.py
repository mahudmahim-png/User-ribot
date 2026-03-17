import os
import asyncio
import time
import random
from datetime import datetime
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# --- Web Server for Render ---
app = Flask(__name__)
@app.route('/')
def home():
    return "ᴜɴᴋɴᴏᴡɴ 〆 ᴀɪ is running stealthily..."

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# --- Configuration ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")

client = Client("unknown_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# AI Memory
sent_messages = {} 
replied_users = {} 

def get_wish():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "Good Morning"
    elif 12 <= hour < 18: return "Good Afternoon"
    else: return "Good Evening"

@client.on_message(filters.private & ~filters.me & ~filters.bot)
async def stealth_reply(bot: Client, message: Message):
    user_id = message.chat.id
    current_time = time.time()

    # 8-hour gap (Safe limit)
    if user_id in replied_users:
        if current_time - replied_users[user_id] < 28800:
            return 

    try:
        me = await bot.get_me()
        
        # Sudhu offline thaklei reply jabe
        if me.status != "online":
            # 1. Random delay (3 to 7 seconds) - Pattern break korar jonno
            await asyncio.sleep(random.randint(3, 7))
            
            wish = get_wish()
            name = "ᴜɴᴋɴᴏᴡɴ 〆"
            
            # Smart & Natural Text
            response_text = (
                f"{wish}! ʜᴇʟʟᴏ, ɪ ᴀᴍ {name}'s ᴀssɪsᴛᴀɴᴛ. ✨\n\n"
                "ʜᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴡᴀʏ ꜰʀᴏᴍ ʜɪs ᴘʜᴏɴᴇ. ɪ'ᴠᴇ ɴᴏᴛɪꜰɪᴇᴅ ʜɪᴍ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ. 📥\n\n"
                "ʜᴇ ᴡɪʟʟ ɢᴇᴛ ʙᴀᴄᴋ ᴛᴏ ʏᴏᴜ ᴀs sᴏᴏɴ ᴀs ʜᴇ's ᴏɴʟɪɴᴇ. ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ᴛʜᴇɴ. 🛡️"
            )

            # 2. Start "Typing" action
            await bot.send_chat_action(user_id, "typing")
            await asyncio.sleep(random.randint(2, 4)) # Simulation delay

            # 3. Send Message
            reply = await message.reply(response_text)
            
            # 4. Mark the original message as Read (Smart Move)
            await bot.read_chat_history(user_id)
            
            sent_messages[user_id] = reply.id
            replied_users[user_id] = current_time
            
    except Exception as e:
        print(f"Stealth Error: {e}")

@client.on_user_status()
async def auto_cleanup(bot: Client, update):
    try:
        me = await bot.get_me()
        if update.id == me.id and update.status == "online":
            if sent_messages:
                for chat_id, msg_id in list(sent_messages.items()):
                    try:
                        # Online houar 5 sec por delete hobe (looks natural)
                        await asyncio.sleep(5)
                        await bot.delete_messages(chat_id, msg_id)
                        del sent_messages[chat_id]
                    except: pass
    except Exception as e:
        print(f"Cleanup Error: {e}")

async def start_bot():
    await client.start()
    print(">>> ᴜɴᴋɴᴏᴡɴ 〆 ᴀɪ (Stealth Mode) Is Live <<<")
    await asyncio.Event().wait()

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
