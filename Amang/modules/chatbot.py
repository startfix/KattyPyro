"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
from asyncio import gather, sleep

from pyrogram import enums, filters
from pyrogram.types import Message

from Amang import *
from Amang.core.decorators.errors import capture_err
from Amang.utils.dbfunctions import add_chatbot, check_chatbot, rm_chatbot
from Amang.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot"
__HELP__ = """
/chatbot [ENABLE|DISABLE] To Enable Or Disable ChatBot In Your Chat.

There's one module of this available for userbot also
check userbot module help."""


async def chat_bot_toggle(message: Message, is_userbot: bool):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    db = await check_chatbot()
    db = db["userbot"] if is_userbot else db["bot"]
    if status == "enable":
        if chat_id not in db:
            await add_chatbot(chat_id, is_userbot=is_userbot)
            text = "Chatbot Enabled!"
            return await eor(message, text=text)
        await eor(message, text="ChatBot Is Already Enabled.")
    elif status == "disable":
        if chat_id in db:
            await rm_chatbot(chat_id, is_userbot=is_userbot)
            return await eor(message, text="Chatbot Disabled!")
        await eor(message, text="ChatBot Is Already Disabled.")
    else:
        await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot"))
@capture_err
async def chatbot_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")
    await chat_bot_toggle(message, is_userbot=False)


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, enums.ChatAction.CANCEL)


@app.on_message(
    filters.text & filters.reply & ~filters.bot & ~filters.via_bot & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["bot"]:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != app.me.id:
        return
    await type_and_send(message)


# FOR USERBOT


@app2.on_message(filters.command("chatbot", prefixes=USERBOT_PREFIX) & SUDOERS)
@capture_err
async def chatbot_status_ubot(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(
            message, text=f"**Usage:**\n{USERBOT_PREFIX}chatbot [ENABLE|DISABLE]"
        )
    await chat_bot_toggle(message, is_userbot=True)


@app2.on_message(
    ~filters.me & ~filters.private & filters.text,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk_ubot(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["userbot"]:
        return
    username = f"@{str(app2.me.username)}"
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        if (
            message.reply_to_message.from_user.id != app2.me.id
            and username not in message.text
        ):
            return
    elif username not in message.text:
        return
    await type_and_send(message)


@app2.on_message(
    filters.text & filters.private & ~filters.me,
    group=(chatbot_group + 1),
)
@capture_err
async def chatbot_talk_ubot_pm(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["userbot"]:
        return
    await type_and_send(message)
