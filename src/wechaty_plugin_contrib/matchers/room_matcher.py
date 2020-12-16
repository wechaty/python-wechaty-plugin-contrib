"""Room Matcher to match the specific room"""
import re
from re import Pattern
import inspect
from typing import List

from wechaty import Wechaty # type: ignore

from wechaty_plugin_contrib.config import (
    get_logger,
    Room,
)

from .matcher import Matcher


logger = get_logger("RoomMatcher")


class RoomMatcher(Matcher):
    async def match(self, target: Room) -> bool:
        """match the room"""
        logger.info(f'RoomMatcher match({target})')

        if not isinstance(target, Room):
            return False

        for option in self.options:

            if isinstance(option, Pattern):
                # match the room with regex pattern
                topic = await target.topic()
                is_match = re.match(option, topic) is not None
            elif isinstance(option, str):
                topic = await target.topic()
                is_match = target.room_id == option or topic == option

            # TODO: support check callback
            # elif hasattr(option, '__call__'):
            #     """check the type of the function
            #     refer: https://stackoverflow.com/a/56240578/6894382
            #     """
            #     if not inspect.isfunction(option):
            #         continue
            #     if inspect.iscoroutinefunction(option):
            #         is_match = await option(target)
            #     else:
            #         is_match = option(target)
            #
            #     if not isinstance(is_match, bool):
            #         raise ValueError('the type of result RoomMatcher function must be bool')

            elif isinstance(option, bool):
                return option

            else:
                raise ValueError(f'unknown type option: {option}')

            if is_match:
                return True
        return False

    async def find_rooms(self, bot: Wechaty) -> List[Room]:
        """find the matched rooms"""
        rooms = await bot.Room.find_all()
        matched_rooms: List[Room] = []
        for room in rooms:
            await room.ready()
            is_match: bool = await self.match(room)
            if is_match:
                matched_rooms.append(room)
        return matched_rooms
