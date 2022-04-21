"""Room Finder to match the specific Room"""
from __future__ import annotations

from uuid import uuid4
import re
from re import L, Pattern
from typing import Dict, List
import inspect

from wechaty_plugin_contrib.config import (
    get_logger,
    Room,
    Wechaty
)

from .finder import Finder


logger = get_logger("RoomFinder")


async def _is_match_with_str(room: Room, option: str, strict: bool = True) -> bool:
    """check if the room id/topic/alias match the option with the following fields:
    
    * contact_id
    * room topic

    Examples:
        >>> is_match = _is_match_with_str(room, 'room_id', True)

    Args:
        room (Room): the room object
        option (str): the option to match the room
        strict (bool, optional): whether to match the room name exactly. Defaults to True.

    Returns:
        Boolean: if the option match the room
    """
    await room.ready()
    if room.room_id == option:
        return True

    if strict:
        return room.payload.topic == option

    return room.payload.topic.startswith(option)


class RoomFinder(Finder):
    """Room Finder can find rooms"""

    async def match(self, bot: Wechaty) -> List[Room]:
        """match the rooms with options

        Args:
            bot (Wechaty): the wechaty bot instance

        Returns:
            List[Room]: the rooms list
        """        
        logger.info(f'RoomFinder match({Wechaty})')

        room_map: Dict[str, Room] = {}
        # 1. load all of room data
        all_rooms: List[Room] = await bot.Room.find_all()
        for room in all_rooms:
            await room.ready()        

        # 2. search rooms with options
        for option in self.options:
            if isinstance(option, Pattern):

                # search from all of the friends
                # match the room with regex pattern
                all_rooms = await bot.Room.find_all()
                for room in all_rooms:
                    topic = await room.topic()
                    if re.match(option, topic):
                        room_map[room.room_id] = room

            elif isinstance(option, str):
                for room in all_rooms:
                    is_match = await _is_match_with_str(room, option, self.strict)
                    if is_match:
                        room_map[room.room_id] = room
            elif inspect.isfunction(option):

                # check the type of the function refer: https://stackoverflow.com/a/56240578/6894382
                if inspect.iscoroutinefunction(option):
                    # pytype: disable=bad-return-type
                    rooms = await option(bot)
                else:
                    rooms = option(bot)

                if isinstance(rooms, Room):
                    rooms = [rooms]

                for room in rooms:
                    room_map[room.room_id] = room

            else:
                raise ValueError(f'unknown type option: {option}')
        return list(room_map.values())
