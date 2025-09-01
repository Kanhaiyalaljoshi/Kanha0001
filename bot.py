
import os
from pyrogram import Client, filters

from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

app = Client(
    "FileRenamerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.document | filters.video | filters.audio)
async def rename_file(client, message):
    user_id = message.from_user.id
    if str(user_id) != str(OWNER_ID):  # सिर्फ Owner यूज कर सके
        return await message.reply("⛔ ये बॉट सिर्फ Owner के लिए है!")

    file = message.document or message.video or message.audio
    await message.reply("✍️ नया नाम भेजो (बिना extension के)...")

    response = await client.listen(message.chat.id)  # User से नया नाम लेता है
    new_name = response.text
    file_ext = os.path.splitext(file.file_name)[1]
    new_filename = f"{new_name}{file_ext}"

    downloaded = await message.download()
    os.rename(downloaded, new_filename)

    await client.send_document(
        chat_id=message.chat.id,
        document=new_filename,
        caption=f"✅ फ़ाइल Rename की गई: **{new_filename}**"
    )

    os.remove(new_filename)


app.run
