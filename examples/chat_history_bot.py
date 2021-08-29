"""chat history plugin example"""
import asyncio
from wechaty import Wechaty  # type: ignore
from wechaty_plugin_contrib import (  # type: ignore
    ChatHistoryPluginOptions,
    ChatHistoryPlugin
)


async def run():
    chat_history_plugin = ChatHistoryPlugin(options=ChatHistoryPluginOptions(
        chat_history_path=''
    ))
    bot = Wechaty().use(chat_history_plugin)
    await bot.start()


asyncio.run(run())
