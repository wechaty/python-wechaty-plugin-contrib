"""Example of Finders"""
from __future__ import annotations
from typing import List
from wechaty import Wechaty     # type: ignore
from wechaty.user.contact import Contact    # type: ignore
from wechaty.user.room import Room  # type: ignore
from wechaty_puppet.schemas.room import RoomQueryFilter     # type: ignore
from wechaty_plugin_contrib import (
    RoomFinder,
    FinderOption,
    ContactFinder
)


async def find_wechaty_rooms(bot: Wechaty) -> List[Room]:
    """call back function for RoomFinder"""
    return await bot.Room.find_all(RoomQueryFilter(topic='Wechaty Room 1'))


async def room_finders(bot: Wechaty) -> List[Room]:
    """Room Finder Example Code"""
    room_finder_options: List[FinderOption] = [
        # 通过room-id来筛选指定群聊
        'room-id',
        # 通过Pattern（正则化表达式）来筛选群聊
        r'(Wechaty)',
        # 通过回调函数来检索房间
        find_wechaty_rooms
    ]
    room_finder = RoomFinder(room_finder_options)
    rooms: List[Room] = await room_finder.match(bot)
    return rooms


async def find_wechaty_contacts(bot: Wechaty) -> List[Contact]:
    """call back function for ContactFinder"""
    contacts: List[Contact] = await bot.Contact.find_all('Baby')
    return contacts


async def contact_finders(bot: Wechaty) -> List[Contact]:
    """Contact Finder Example Code"""
    options: List[FinderOption] = [
        # 通过contact-id来筛选指定联系人
        'contact-id',
        # 通过Pattern（正则化表达式）来筛选群聊
        r'Baby-\d',
        # 通过回调函数来检索房间
        find_wechaty_contacts
    ]
    contact_finder = ContactFinder(options)
    contacts: List[Contact] = await contact_finder.match(bot)
    return contacts
