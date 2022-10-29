from __future__ import annotations
import asyncio
import os
from typing import List
from wechaty import WechatyPlugin, Room, Contact
from quart import Quart, request



class WelcomePlugin(WechatyPlugin):
    VIEW_URL = "/plugins/welcome/view"

    """Welcome Plugin is for saing welcome word for some rooms when invited into the Room.
    
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

    async def blueprint(self, app: Quart) -> None:
        @app.route(WelcomePlugin.VIEW_URL)
        async def room_join_view():
            basedir = os.path.dirname(__file__)
            with open(os.path.join(basedir, 'on_room_join_plugin.html'), 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace("{{view_url}}", WelcomePlugin.VIEW_URL)
            return content
        
        @app.route(WelcomePlugin.VIEW_URL + "/<room_id>", methods=['GET'])
        async def get_welcome_words(room_id: str):
            words = self.setting.get(room_id, None)
            if isinstance(words, int):
                words = ""
            return str(words)
        
        @app.route(WelcomePlugin.VIEW_URL + "/<room_id>", methods=['POST'])
        async def set_welcome_words(room_id: str):
            json_data = await request.get_json(force=True)
            text = json_data.get("text", None)
            setting = self.setting

            setting[room_id] = text
            self.setting = setting

            return "ok"
    
    async def on_room_join(self, room: Room, invitees: List[Contact], inviter: Contact, *args, **kwargs) -> None:
       
        if room.room_id not in self.setting:
            return
        
        words = self.setting[room.room_id]
        if isinstance(words, int):
            return
        
        for contact in invitees:
            await contact.ready()
            
            await room.say(words, mention_ids=[contact.contact_id])
            
            await asyncio.sleep(0.5)
            