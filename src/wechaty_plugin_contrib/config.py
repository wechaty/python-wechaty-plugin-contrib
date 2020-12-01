"""import basic config from wechaty-puppet"""

from wechaty import (   # type: ignore
    Room,
    Contact,
    Message,

    Wechaty
)

from wechaty_puppet import get_logger   # type: ignore

from .version import version

__all__ = [
    'get_logger',
    'version',

    'Room',
    'Contact',
    'Message',

    'Wechaty'
]
