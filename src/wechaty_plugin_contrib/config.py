"""import basic config from wechaty-puppet"""

from wechaty import (
    Room,
    Contact,
    Message,
    Wechaty
)

from wechaty_puppet import get_logger

from .version import version

__all__ = [
    'get_logger',
    'version',

    'Room',
    'Contact',
    'Message',

    'Wechaty'
]
