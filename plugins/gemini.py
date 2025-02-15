import requests
from pyrogram import filters
from pyrogram.enums import ChatAction
from ChampuMusic import app

BASE_API_URL = "https://amanshah.serv00.net/gemini?question="

async def fetch_response(user_input, message):
    try:
        api_url = f"{BASE_API_URL}{user_input}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.text
            if data:
                await message.reply_text(data, quote=True)
            else:
                await message.reply_text("No response received. Please try again.", quote=True)
        else:
            await message.reply_text(f"Error: Unable to fetch data. (Status Code: {response.status_code})", quote=True)
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Request failed: {e}", quote=True)

@app.on_message(filters.command(["gemini", "ai", "how", "ask"]))
async def command_handler(client, message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    if (
        message.text.startswith(f"/{message.command[0]}@{app.username}")
        and len(message.text.split(" ", 1)) > 1
    ):
        user_input = message.text.split(" ", 1)[1]
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await message.reply_text(
                f"ᴇxᴀᴍᴘʟᴇ :- `/{message.command[0]} who is lord ram`"
            )
            return

    await fetch_response(user_input, message)
