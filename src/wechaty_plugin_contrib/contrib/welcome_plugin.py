from __future__ import annotations
import asyncio
from typing import Dict, List
from dataclasses import dataclass, field
from wechaty import WechatyPlugin, Room, Contact


@dataclass
class WelcomeConfig:
    room_ids: Dict[str, str] = field(default_factory=dict)
    welcome_words: Dict[str, str] = field(default_factory=dict)


class WelcomePlugin(WechatyPlugin):
    """Welcome Plugin is for saing welcome word for some rooms when joining the Room.
    
    Examples:
        >>> plugin = WelcomePlugin()
        >>> bot.use(plugin)

    Settings:
        {
            "room_ids": {
                "first-room-id": "school-related-room",
                "second-room-id": "school-related-room",
                "third-room-id": "boy-related-room"
            },
            "welcome_words": {
                "school-related-room": "欢迎同学进入该新生群，请详细阅读群公告，修改群备注",
                "boy-related-room": "进群的都是大帅哥"
            }
        }
    """

    def get_config(self) -> WelcomeConfig:
        try:
            config: WelcomeConfig = WelcomeConfig(**self.setting)
            return config
        except:
            return {}
    
    async def on_room_join(self, room: Room, invitees: List[Contact], inviter: Contact, *args, **kwargs) -> None:
        config = self.get_config()
        
        # 1. check if the room is configured
        if room.room_id not in config.room_ids:
            return
        
        # 2. get the welcome words
        words = config.welcome_words.get(config.room_ids[room.room_id], None)
        if words is None:
            return
        
        # 3. say to the room
        for contact in invitees:
            await contact.ready()
            
            await room.say(words, mention_ids=[contact.contact_id])
            
            await asyncio.sleep(1)
 