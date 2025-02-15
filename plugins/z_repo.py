import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ChampuMusic import app
from ChampuMusic.utils.database import add_served_chat, get_assistant


start_txt = """**
✪ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗦𝗵𝗮𝗵𝗶𝗹 𝗥𝗲𝗽𝗼𝘀 ✪


➲ ᴇᴀsʏ ʜᴇʀᴏᴋᴜ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ✰  
➲ ɴᴏ ʙᴀɴ ɪssᴜᴇs ✰  
➲ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs ✰  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ ✰

► sᴇɴᴅ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍs!
**"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=true")
        ],
        [
          InlineKeyboardButton("Shahil", url="https://t.me/Shahil440"),
          InlineKeyboardButton("𓆩 ˹𝖲𝗁𝖺𝗁𝗂𝗅 ✘ 𝖡𝗈𝗍𝗌˼ 𓆪", url="https://t.me/ShahilBotsList"),
          ],
               [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/shahil440"),

],[
              InlineKeyboardButton("ᴍᴜsɪᴄ", url=f"https://github.com/Shahilali5/ShahilxMusic"),
              InlineKeyboardButton("ՏTᖇIᑎᘜ ᙭ ᕼᗩᑕKᗴᖇ 🧑🏻‍💻", url=f"https://github.com/Shahilali5/STRING-HACK"),
              ],
[
              InlineKeyboardButton("𓆩˹𝖴𝗇𝗄𝗇𝗈𝗐𝗇 ✘ ChatBot˼ 𓆪", url=f"https://github.com/Shahil440/CHATBOTV2")
              ],
              [
              InlineKeyboardButton("ᴍᴀɴᴀɢᴍᴇɴᴛ", url=f"https://github.com/Shahilali5/ShahilxMange")
]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo=config.START_IMG_URL,
        caption=start_txt,
        reply_markup=reply_markup
    )


