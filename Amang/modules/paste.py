"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import os
import re

import aiofiles
from pyrogram import filters
from pyrogram.types import Message

from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.core.keyboard import ikb
from Amang.utils.pastebin import paste

__MODULE__ = "Paste"
__HELP__ = "/paste - To Paste Replied Text Or Document To A Pastebin"
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@app2.on_message(filters.command("paste", prefixes=USERBOT_PREFIX) & SUDOERS)
@app.on_message(filters.command("paste"))
@capture_err
async def paste_func(_, message: Message):
    if not message.reply_to_message:
        return await eor(message, text="Reply To A Message With /paste")
    r = message.reply_to_message

    if not r.text and not r.document:
        return await eor(message, text="Only text and documents are supported.")

    m = await eor(message, text="Pasting...")

    if r.text:
        content = str(r.text)
    else:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")

        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")

        doc = await message.reply_to_message.download()

        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await paste(content)
    kb = ikb({"Paste Link": link})
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"**Paste Link:** [Here]({link})",
            )
        await m.delete()
    except Exception:
        await m.edit("Here's your paste", reply_markup=kb)
