"""rasa plugin bot examples"""
from __future__ import annotations

import asyncio
from wechaty import Wechaty

from wechaty_plugin_contrib import (
    RasaRestPlugin,
    RasaRestPluginOptions
)


async def run() -> None:
    """async run method"""
    options = RasaRestPluginOptions(
        endpoint='your-endpoint',
        conversation_ids=['room-id', 'contact-id']
    )
    rasa_plugin = RasaRestPlugin(options)

    bot = Wechaty().use(rasa_plugin)
    await bot.start()


asyncio.run(run())
