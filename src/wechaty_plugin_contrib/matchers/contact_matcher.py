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

        if not isinstance(target, Contact):
            return False

        for option in self.options:
            if isinstance(option, Pattern):
                # match the room with regex pattern
                contact_alias = await target.alias()
                is_match = re.match(option, target.name) is not None or \
                    re.match(option, contact_alias) is not None

            elif isinstance(option, str):
                # make sure that the contact is ready
                await target.ready()
                is_match = target.contact_id == option or option == target.name

            # elif hasattr(option, '__call__'):
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
