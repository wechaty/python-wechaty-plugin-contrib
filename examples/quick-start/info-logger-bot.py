import asyncio
from wechaty import Wechaty
from dotenv import load_dotenv
from wechaty_plugin_contrib import InfoLoggerPlugin

async def main():
    load_dotenv()
    bot = Wechaty()

    bot.use(InfoLoggerPlugin())

    await bot.start()

asyncio.run(main())
 