"""Room Finder to match the specific Room"""
import re
from re import Pattern
import inspect
from typing import List

from wechaty_plugin_contrib.config import (
    get_logger,
    Room,

    Wechaty
)

from .finder import Finder


logger = get_logger("RoomFinder")


class RoomFinder(Finder):
    async def match(self, wechaty: Wechaty) -> List[Room]:
        """match the room"""
        logger.info(f'RoomFinder match({Wechaty})')

        rooms: List[Room] = []

        for option in self.options:
            if isinstance(option, Pattern):

                # search from all of the friends
                # match the room with regex pattern
                all_rooms = await wechaty.Room.find_all()
                for room in all_rooms:
                    topic = await room.topic()
                    if re.match(option, topic):
                        rooms.append(room)

            elif isinstance(option, str):
                room = wechaty.Room.load(option)
                await room.ready()
                rooms.append(room)
            elif hasattr(option, '__call__'):
                """check the type of the function
                refer: https://stackoverflow.com/a/56240578/6894382
                """
                if inspect.iscoroutinefunction(option):
                    # pytype: disable=bad-return-type
                    targets = await option(wechaty)
                else:
                    targets = option(wechaty)
                if isinstance(targets, List[Room]):
                    rooms.extend(targets)
            else:
                raise ValueError(f'unknown type option: {option}')
        return rooms
