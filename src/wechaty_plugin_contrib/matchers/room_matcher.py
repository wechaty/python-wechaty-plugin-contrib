"""Room Matcher to match the specific room"""
import re
from re import Pattern
import inspect

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

        for option in self.options:
            if isinstance(option, Pattern):
                re_pattern = re.compile(option)
                # match the room with regex pattern
                topic = await target.topic()
                is_match = re.match(re_pattern, topic)
            elif isinstance(option, str):
                is_match = target.room_id == option
            elif hasattr(option, '__call__'):
                """check the type of the function
                refer: https://stackoverflow.com/a/56240578/6894382
                """
                if inspect.iscoroutinefunction(option):
                    # pytype: disable=bad-return-type
                    is_match = await option(target)
                else:
                    is_match = option(target)
            else:
                raise ValueError(f'unknown type option: {option}')

            if is_match:
                return True
        return False
