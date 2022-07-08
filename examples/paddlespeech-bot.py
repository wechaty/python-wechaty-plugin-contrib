"""paddlespeech bot examples"""
import asyncio
from wechaty import Wechaty
from wechaty_plugin_contrib.contrib.paddlespeech_plugin import (
    PaddleSpeechPlugin
)

async def run() -> None:
    """async run method"""
    plugin = PaddleSpeechPlugin()
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
