"""daily plugin bot examples"""
import asyncio
from datetime import datetime

from wechaty import Wechaty  # type: ignore
from wechaty_puppet import RoomQueryFilter  # type: ignore

from wechaty_plugin_contrib import (
    DailyPluginOptions,
    DailyPlugin,
    DingDongPlugin
)


async def say_hello(bot: Wechaty):
    """say hello to the room"""
    room = await bot.Room.find(query=RoomQueryFilter(topic='小群，小群1'))
    if room:
        await room.say(f'hello bupt ... {datetime.now()}')


async def run():
    """async run method"""
    morning_plugin = DailyPlugin(DailyPluginOptions(
        name='girl-friend-bot-morning',
        contact_id='some-one-id',
        trigger='cron',
        kwargs={
            'hour': 8,
            'minute': 0
        },
        msg='宝贝，早安，爱你哟～'
    ))
    morning_plugin.add_interval_job(say_hello)

    ding_dong_plugin = DingDongPlugin()

    bot = Wechaty().use(morning_plugin).use(ding_dong_plugin)
    await bot.start()

asyncio.run(run())
