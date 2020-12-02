"""daily plugin"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union, List, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler     # type: ignore
from apscheduler.schedulers.base import BaseScheduler   # type: ignore

from wechaty import Wechaty, get_logger, Room, Contact      # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore


log = get_logger('DailyPlugin')


@dataclass
class DailyPluginOptions(WechatyPluginOptions):
    """daily plugin options"""
    room_id: Optional[str] = None
    contact_id: Optional[str] = None
    trigger: Optional[str] = None
    kwargs: Optional[dict] = None
    msg: Optional[str] = None


class DailyPlugin(WechatyPlugin):
    """
    say something everyday, like `Daily Words`
    """
    def __init__(self, options: DailyPluginOptions):
        super().__init__(options)

        if options.room_id is None and options.contact_id is None:
            raise Exception('room_id and contact_id should not all be empty')
        if options.room_id is not None and options.contact_id is not None:
            raise Exception('only one of the room_id contact_id should not '
                            'be none')
        if options.trigger is None:
            raise Exception('trigger should not be none')
        if options.kwargs is None:
            raise Exception('kwargs should not be none')
        if options.msg is None:
            raise Exception('msg should not be none')

        self.options: DailyPluginOptions = options
        self.scheduler: BaseScheduler = AsyncIOScheduler()
        self._scheduler_jobs: List[Any] = []

    @property
    def name(self) -> str:
        """get the name of the plugin"""
        if self.options is None or self.options.name is None:
            return 'dayily'
        return self.options.name

    async def tick(self, msg: str):
        """tick the things """
        print(msg)
        conversation: Union[Room, Contact]
        if self.options.room_id is not None:
            conversation = self.bot.Room.load(self.options.room_id)
        elif self.options.contact_id is not None:
            conversation = self.bot.Contact.load(self.options.contact_id)
        else:
            raise Exception('room_id and contact_id should not all be empty')

        await conversation.ready()
        await conversation.say(msg)

    async def init_plugin(self, wechaty: Wechaty):
        """init plugin"""
        await super().init_plugin(wechaty)
        for job in self._scheduler_jobs:
            job(wechaty)
        self.scheduler.start()

    def add_interval_job(self, func):
        """add interval job"""

        def add_job(bot: Wechaty):
            self.scheduler.add_job(
                func,
                trigger='interval',
                seconds=5,
                kwargs={
                    'bot': bot
                }
            )
        self._scheduler_jobs.append(add_job)
