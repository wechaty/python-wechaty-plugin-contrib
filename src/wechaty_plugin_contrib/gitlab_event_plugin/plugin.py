"""
python-wechaty-plugin-contrib - https://github.com/wechaty/python-wechaty-plugin-contrib

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
import asyncio
from wechaty import (
    Wechaty, WechatyPlugin,
)

from aiohttp import web
from wechaty_puppet import RoomQueryFilter, get_logger

from .options import GitlabHookItem, GitlabEventOptions

log = get_logger("GitlabEventPlugin")
routes = web.RouteTableDef()


@routes.get('/')
async def receive_message(request: web.Request):
    """"""
    log.info('')
    bot: Wechaty = request.app.get('bot')
    options: GitlabEventOptions = request.app.get('bot-options')

    return web.json_response(text='hello wechaty web bot')


class GitlabEventPlugin(WechatyPlugin):
    """"""

    def __init__(self, options: GitlabEventOptions):
        super().__init__(options)
        self.options = options

    @property
    def name(self) -> str:
        return 'gitlab-event-plugin'

    async def init_plugin(self, wechaty: Wechaty):
        """init the gitlab event plugin"""
        log.info('starting the server')
        self.bot = wechaty

        # start the server
        app = web.Application()
        app['bot'] = wechaty
        app['bot-options'] = self.options
        app.add_routes(routes)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, '0.0.0.0', self.options.listen_port)

        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(site.start(), loop=loop)
        log.info(
            f'the server has started ... 0.0.0.0: {self.options.listen_port}'
        )
