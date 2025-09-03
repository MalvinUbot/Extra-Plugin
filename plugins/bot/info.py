import asyncio
import random
from time import time
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont
from pyrogram import enums, filters
from ChampuMusic import app

# Track last message timestamp & command count
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

random_photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

# Image utils
get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None,
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)
    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"downloads/userinfo_img_{user_id}.png"
    bg.save(path)
    return path

bg_path = "assets/userinfo.png"
font_path = "assets/font.ttf"

INFO_TEXT = """**
❅─────✧❅✦❅✧─────❅
            ✦ ᴜsᴇʀ ɪɴғᴏ ✦

➻ ᴜsᴇʀ ɪᴅ ‣ **`{}`
**➻ ғɪʀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ʟᴀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ᴜsᴇʀɴᴀᴍᴇ ‣ **`{}`
**➻ ᴍᴇɴᴛɪᴏɴ ‣ **{}
**➻ ʟᴀsᴛ sᴇᴇɴ ‣ **{}
**➻ ᴅᴄ ɪᴅ ‣ **{}
**➻ ʙɪᴏ ‣ **`{}`

**❅─────✧❅✦❅✧─────❅**
"""

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        status = user.status
        if status == enums.UserStatus.RECENTLY:
            return "Recently."
        elif status == enums.UserStatus.LAST_WEEK:
            return "Last week."
        elif status == enums.UserStatus.LONG_AGO:
            return "Long time ago."
        elif status == enums.UserStatus.OFFLINE:
            return "Offline."
        elif status == enums.UserStatus.ONLINE:
            return "Online."
    except:
        return "**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"

@app.on_message(
    filters.command(
        ["info", "userinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
)
async def userinfo(_, message):
    # Check if message is from a user
    if not message.from_user and not message.reply_to_message:
        await message.reply_text("⚠️ Tidak bisa mengambil info user dari pesan ini.")
        return

    # Determine which user to get info from
    user_id = message.from_user.id if message.from_user else message.reply_to_message.from_user.id

    # Spam detection
    current_time = time()
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    chat_id = message.chat.id

    try:
        user_info = await app.get_chat(user_id)
        user = await app.get_users(user_id)
        status = await userstatus(user.id)
        id = user_info.id
        dc_id = user.dc_id
        first_name = user_info.first_name
        last_name = user_info.last_name if user_info.last_name else "No last name"
        username = user_info.username if user_info.username else "No Username"
        mention = user.mention
        bio = user_info.bio if user_info.bio else "No bio set"

        # Profile photo handling
        if user.photo:
            photo = await app.download_media(user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )
        else:
            welcome_photo = random.choice(random_photo)

        await app.send_photo(
            chat_id,
            photo=welcome_photo,
            caption=INFO_TEXT.format(
                id, first_name, last_name, username, mention, status, dc_id, bio
            ),
            reply_to_message_id=message.id,
        )
    except Exception as e:
        await message.reply_text(f"⚠️ Terjadi error: {e}")

__MODULE__ = "Usᴇʀ Iɴғᴏ"
__HELP__ = """
/ɪɴғᴏ [ᴜsᴇʀ_ɪᴅ]: Gᴇᴛ ᴅᴇᴛᴀɪᴇᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜsᴇʀ.
/ᴜsᴇʀɪɴғᴏ [ᴜsᴇʀ_ɪᴅ]: Aɪᴀs ғᴏʀ /ɪɴғᴏ.
"""
