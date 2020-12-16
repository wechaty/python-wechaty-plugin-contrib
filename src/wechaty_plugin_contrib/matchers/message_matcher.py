"""Message Matcher to match the specific message"""
import re
from re import Pattern
import inspect
from typing import Awaitable

from wechaty_plugin_contrib.config import (
    get_logger,
    Message,
)

from .matcher import Matcher


logger = get_logger("MessageMatcher")


class MessageMatcher(Matcher):
    async def match(self, target: Message) -> bool:
        """match the room"""
        logger.info(f'MessageMatcher match({target})')

        if not isinstance(target, Message):
            return False

        for option in self.options:
            if isinstance(option, Pattern):
                # match the room with regex pattern
                topic = target.text()
                is_match = re.match(option, topic) is not None
            elif isinstance(option, str):
                await target.ready()
                is_match = target.message_id == option or target.text() == option

            # TODO: support check callback
            # elif callable(option):
            #     """check the type of the function
            #     refer: https://stackoverflow.com/a/56240578/6894382
            #     """
            #     if inspect.iscoroutinefunction(option):
            #         is_match = await option(target)
            #     else:
            #         is_match = option(target)

            elif isinstance(option, bool):
                return option

            else:
                raise ValueError(f'unknown type option: {option}')

            if is_match:
                return True
        return False
