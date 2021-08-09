"""Base finder for finding Room/Message"""
from re import Pattern
from typing import (
    Any,
    Callable,
    Union,
    List, Coroutine,
)
from wechaty_plugin_contrib.config import (
    Room,
    Contact,
    Message
)

from wechaty import Wechaty # type: ignore

FinderOption = Union[
    str, Pattern, bool,
    Callable[[Union[Contact, Room, Message]], List[Union[Room, Contact]]],
    Callable[[Any], Coroutine[Any, Any, List[Any]]]
]
FinderOptions = Union[FinderOption, List[FinderOption]]


class Finder:
    def __init__(self, option: FinderOptions):
        if isinstance(option, list):
            self.options = option
        else:
            self.options = [option]

    async def match(self, bot: Wechaty) -> List[Any]:
        raise NotImplementedError
