"""Scheduler plugin"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, List, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler     # type: ignore
from apscheduler.schedulers.base import BaseScheduler   # type: ignore

from wechaty import Wechaty, get_logger, Room, Contact      # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore


log = get_logger('SchedulerPlugin')


@dataclass
class SchedulerPluginOptions(WechatyPluginOptions):
    """Scheduler plugin options"""


class SchedulerPlugin(WechatyPlugin):
    """
    say something everyday, like `Scheduler Words`
    """
    def __init__(self, options: Optional[SchedulerPluginOptions] = None):
        super().__init__()
        self.options = options or SchedulerPluginOptions()

        self.scheduler: BaseScheduler = AsyncIOScheduler()
        self._scheduler_jobs: List[Any] = []

    @property
    def name(self) -> str:
        """get the name of the plugin"""
        if self.options is None or self.options.name is None:
            return 'scheduler-plugin'
        return self.options.name

    async def init_plugin(self, wechaty: Wechaty):
        """init plugin"""
        await super().init_plugin(wechaty)
        for job in self._scheduler_jobs:
            job(wechaty)

        self.scheduler.start()

    def add_interval_job(self, 
            func,
            trigger="interval",
            weeks: Optional[int] = None, days: Optional[int] = None,
            hours: Optional[int] = None, minutes: Optional[int] = None,
            seconds: Optional[int] = None, 
            start_date: Optional[Union[str, datetime]] = None,
            end_date: Optional[Union[str, datetime]] = None, 
            jitter=None,
            run_date=Optional[Union[str, datetime]], 
            timezone=None,
        ):

        # add scheduler job, the params is same as APScheduler.add_job
        def add_job(bot: Wechaty):
            self.scheduler.add_job(
                func,
                trigger=trigger,
                weeks=weeks,
                days=days,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                run_date=run_date,
                timezone=timezone,
                kwargs={
                    'bot': bot
                }
            )
        self._scheduler_jobs.append(add_job)
