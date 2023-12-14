"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import os

from pyrogram import filters

from Amang import *
from Amang.core.decorators.permissions import adminsOnly

__MODULE__ = "Admin Miscs"
__HELP__ = """
/stchat - Change The Name Of A Group/Channel.
/setgpic - Change The PFP Of A Group/Channel.
/sutitel - Change The Administrator Title Of An Admin.
/kickme - Coba sendiri.
"""


@app.on_message(filters.command("stchat") & ~filters.private)
@adminsOnly("can_change_info")
async def set_chat_title(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n/set_chat_title NEW NAME")
    old_title = message.chat.title
    new_title = message.text.split(None, 1)[1]
    await message.chat.set_title(new_title)
    await message.reply_text(
        f"Successfully Changed Group Title From {old_title} To {new_title}"
    )


@app.on_message(filters.command("sutitel") & ~filters.private)
@adminsOnly("can_change_info")
async def set_user_title(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to user's message to set his admin title"
        )
    if not message.reply_to_message.from_user:
        return await message.reply_text(
            "I can't change admin title of an unknown entity"
        )
    chat_id = message.chat.id
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n/set_user_title NEW ADMINISTRATOR TITLE"
        )
    title = message.text.split(None, 1)[1]
    await app.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(
        f"Successfully Changed {from_user.mention}'s Admin Title To {title}"
    )

@app.on_message(filters.command(["kickme"]))
async def kickme(_, message):
    reason = None
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    try:
        await message.chat.ban_member(message.from_user.id)
        txt = f"Pengguna {message.from_user.mention} menendang dirinya sendiri. Mungkin dia sedang frustasi 😕"
        txt += f"\n<b>Alasan</b>: {reason}" if reason else "-"
        await message.reply_text(txt)
        await message.chat.unban_member(message.from_user.id)
    except RPCError as ef:
        await message.reply_text(f"Sepertinya ada error, silahkan report ke owner saya. \nERROR: {str(ef)}")
    except Exception as err:
        await message.reply(f"ERROR: {err}")


@app.on_message(filters.command("setgpic") & ~filters.private)
@adminsOnly("can_change_info")
async def set_chat_photo(_, message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text("Reply to a photo to set it as chat_photo")

    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Reply to a photo or document to set it as chat_photo"
        )

    if file.file_size > 5000000:
        return await message.reply("File size too large.")

    photo = await reply.download()
    await message.chat.set_photo(photo=photo)
    await message.reply_text("Successfully Changed Group Photo")
    os.remove(photo)
