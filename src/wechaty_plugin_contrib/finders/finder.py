"""Base finder for finding Room/Message"""
from re import Pattern
from typing import (
    Callable,
    Optional,
    Union,
    List,
)

from wechaty_plugin_contrib.config import (
    Room,
    Contact,
    Message
)


FinderOption = Union[str, Pattern, bool, Callable[[Union[Contact, Room, Message]], List[Union[Room, Contact]]]]
FinderOptions = Union[FinderOption, List[FinderOption]]


class Finder:
    def __init__(self, option: FinderOptions):
        if isinstance(option, list):
            self.options = option
        else:
            self.options = [option]

    def match(self, target) -> bool:
        raise NotImplementedError
