from __future__ import annotations
from selectors import DefaultSelector
import feedparser
from typing import Optional, List
from dataclasses import dataclass
from wechaty import WechatyPlugin, Message, Wechaty, WechatyPluginOptions, UrlLink
from wechaty.user.url_link import UrlLinkPayload
from wechaty import WechatyPlugin


@dataclass
class FeedNews:
    id: str
    title: str
    url: str
    description: str

    def to_url_link(self) -> UrlLink:
        # thumbnailUrl: Optional[str] = None
        return UrlLink(
            payload=UrlLinkPayload(
                url=self.url,
                title=self.title,
                description=self.description,
            )
        )


def parse(url) -> List[FeedNews]:
    result = feedparser.parse(url)
    news = []
    for entry in result.get("entries", []):
        news.append(FeedNews(
            id=entry['id'],
            url=entry['link'],
            title=entry['title'],
            description=entry['summary']
        ))
    return news


class RSSPlugin(WechatyPlugin):
    """rss plugins which can push rss news into Contact & Rooms

        examples:
            >>> plugin = RSSPlugin()
            >>> plugin.setting['url'] = 'your-own-feed-url'
            >>> plugin.settings['room_ids'] = ["your-room-ids"]
            >>> bot.use(plugin)

    """
    VIEW_URL = '/api/plugins/rss/view'

    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        """_summary_

        Args:
            options (Optional[WechatyPluginOptions], optional): _description_. Defaults to None.
        """
        super().__init__(options)
        self._init_default_setting()
    
    def _init_default_setting(self):
        default_setting = {
            # 每天早上九点钟推送消息
            "hour": 9,
            "max_news": 3,
            "contact_ids": [],
            "room_ids": [],
            "url": "feed-url"
        }
        default_setting.update(self.setting)
        self.setting = default_setting

    async def init_plugin(self, wechaty: Wechaty) -> None:
        self.add_daily_job(
            hour=self.setting['hour'],
            handler=self.fetch_news
        )
    
    async def push_news(self, new: FeedNews):
        for contact_id in self.setting.get("contact_ids", []):
            contact = self.bot.Contact.load(contact_id)
            await contact.ready()
            await contact.say(new.to_url_link())
        
        for room_id in self.setting.get("room_ids", []):
            room = self.bot.Room.load(room_id)
            await room.ready()
            await room.say(new.to_url_link())
    
    async def fetch_news(self):
        news:List[FeedNews] = parse(self.setting['url'])
        sended_news_count = 0
        for new in news:
            if new.id in self.setting:
                continue
            if sended_news_count > self.setting['max_news']:
                break
            sended_news_count += 1

            self.setting[new.id] = True
            
            await self.push_news(new)
