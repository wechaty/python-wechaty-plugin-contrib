"""Base matcher for finding"""
from re import Pattern
from typing import (
    Callable,
    Optional,
    Union,
    List
)

from wechaty_plugin_contrib.config import (
    Room,
    Contact,
    Message
)


MatcherOption = Union[str, Pattern, bool, Callable[[Union[Contact, Room, Message]], bool]]
MatcherOptions = Union[MatcherOption, List[MatcherOption]]


class Matcher:
    def __init__(self, option: MatcherOptions):
        if isinstance(option, list):
            self.options = option
        else:
            self.options = [option]

    async def match(self, target) -> bool:
        raise NotImplementedError
