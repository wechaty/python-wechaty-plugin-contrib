"""daily plugin bot examples"""
import asyncio
from datetime import datetime
from typing import List

from wechaty import Wechaty  # type: ignore
from wechaty_puppet import RoomQueryFilter  # type: ignore

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions
)


def get_rules() -> List[AutoReplyRule]:
    return [
        AutoReplyRule(keyword='ding', reply_content='dong'),
        AutoReplyRule(keyword='wechaty', reply_content='hello-wechaty')
    ]


async def run():
    """async run method"""

    plugin = AutoReplyPlugin(AutoReplyOptions(rules=get_rules()))
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
