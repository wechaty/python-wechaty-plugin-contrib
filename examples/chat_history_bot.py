"""chat history plugin example"""
import asyncio
from wechaty import Wechaty
from wechaty_plugin_contrib import (
    ChatHistoryPluginOptions,
    ChatHistoryPlugin
)


async def run() -> None:
    """
    async run method
    chat_history_path defines the path to save message file.
    For SQlite, chat_history_database="sqlite+aiosqlite:///chathistory.db"
    For MySQL, chat_history_database="mysql+aiomysql://user:password@hostname/database"
    For PostgreSQL, chat_history_database="postgresql+asyncpg://user:password@hostname/database"
    """

    chat_history_plugin = ChatHistoryPlugin(options=ChatHistoryPluginOptions(
        chat_history_path='',
        chat_history_database=''
    ))
    bot = Wechaty().use(chat_history_plugin)
    await bot.start()


asyncio.run(run())
