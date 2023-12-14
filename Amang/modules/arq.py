"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
from pyrogram import filters

from Amang import *
from Amang.core.sections import section


@app.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        return await message.reply_text(data.result)
    server = data.result
    nlp = server.spam_protection

    body = {
        "Uptime": server.uptime,
        "Requests Since Uptime": server.requests,
        "CPU": server.cpu,
        "Memory": server.memory.server,
        "Platform": server.platform,
        "Python": server.python,
        "Spam/Ham Ratio": f"{nlp.spam_messages}/{nlp.ham_messages}",
        "Users": server.users,
        "Bot": [server.bot],
    }
    text = section("A.R.Q", body)
    await message.reply_text(text)
