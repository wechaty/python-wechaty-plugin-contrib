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

from wechaty import Wechaty

FinderOption = Union[
    str, Pattern, bool,
    Callable[[Union[Contact, Room, Message]], List[Union[Room, Contact]]],
    Callable[[Any], Coroutine[Any, Any, List[Any]]]
]


class Finder:
    """Base Abstract Finder"""
    def __init__(self, option: Union[FinderOption, List[FinderOption]], strict: bool = True):
        if isinstance(option, list):
            self.options = option
        else:
            self.options = [option]
        
        self.strict: bool = strict

    async def match(self, bot: Wechaty) -> List[Any]:
        """find the matched item, eg: Room, Contact, Message"""
        raise NotImplementedError
