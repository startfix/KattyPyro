"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
from pyrogram import filters as filters_
from pyrogram.types import Message

from Amang import SUDOERS
from Amang import USERBOT_ID as OWNER_ID
from Amang.utils.functions import get_urls_from_text


def url(_, __, message: Message) -> bool:
    # Can't use entities to check for url because
    # monospace removes url entity

    # TODO Fix detection of those urls which
    # doesn't have schema, ex-facebook.com

    text = message.text or message.caption
    return False if not text else bool(get_urls_from_text(text))


def entities(_, __, message: Message) -> bool:
    return bool(message.entities)


def anonymous(_, __, message: Message) -> bool:
    return bool(message.sender_chat)


def sudoers(_, __, message: Message) -> bool:
    return False if not message.from_user else message.from_user.id in SUDOERS


def owner(_, __, message: Message) -> bool:
    return False if not message.from_user else message.from_user.id == OWNER_ID


class Filters:
    pass


filters = Filters
filters.url = filters_.create(url)
filters.entities = filters_.create(entities)
filters.anonymous = filters_.create(anonymous)
filters.sudoers = filters_.create(sudoers)
filters.owner = filters_.create(owner)
