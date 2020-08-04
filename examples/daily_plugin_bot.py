"""daily plugin bot examples"""
import asyncio

from wechaty import Wechaty  # type: ignore
from wechaty_plugin_contrib.daily_plugin import DailyPluginOptions, DailyPlugin
from wechaty_plugin_contrib.ding_dong_plugin import DingDongPlugin


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

    eating_plugin = DailyPlugin(DailyPluginOptions(
        name='girl-friend-bot-eating',
        contact_id='some-one-id',
        trigger='cron',
        kwargs={
            'hour': 11,
            'minute': 30
        },
        msg='中午要记得好好吃饭喔～'
    ))

    ding_dong_plugin = DingDongPlugin()

    bot = Wechaty().use(morning_plugin).use(eating_plugin).use(ding_dong_plugin)
    await bot.start()

asyncio.run(run())
