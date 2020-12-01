"""Contact Matcher to match the specific contact"""
import re
from re import Pattern
import inspect

from wechaty_plugin_contrib.config import (
    get_logger,
    Contact,
)

from .matcher import Matcher


logger = get_logger("ContactMatcher")


class ContactMatcher(Matcher):
    async def match(self, target: Contact) -> bool:
        """match the room"""
        logger.info(f'ContactMatcher match({target})')

        for option in self.options:
            if isinstance(option, Pattern):
                re_pattern = re.compile(option)
                # match the room with regex pattern
                contact_alias = await target.alias()
                is_match = re.match(re_pattern, target.name) or re.match(re_pattern, contact_alias)
            elif isinstance(option, str):
                is_match = target.contact_id == option
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
