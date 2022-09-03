"""daily plugin bot examples"""
import asyncio

from wechaty import Wechaty

from wechaty_puppet import (
    FileBox
)

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions,
)

from wechaty_plugin_contrib.matchers import ContactMatcher


async def run() -> None:
    """async run method"""
    img_url = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy' \
              '/it/u=1257042014,3164688936&fm=26&gp=0.jpg'
    plugin = AutoReplyPlugin(options=AutoReplyOptions(
        rules=[
            AutoReplyRule(keyword='ding', reply_content='dong'),
            AutoReplyRule(keyword='七龙珠', reply_content='七龙珠'),
            AutoReplyRule(
                keyword='七龙珠',
                reply_content=FileBox.from_url(img_url, name='python.png')
            ),
            AutoReplyRule(
                keyword='wechaty-icon',
                reply_content=FileBox.from_url(img_url, name='python.png')
            )
        ],
        matchers=[
            ContactMatcher('秋客'),
        ]
    ))
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
