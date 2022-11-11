from __future__ import annotations
import os
from quart import Quart, request, jsonify
from wechaty import WechatyPlugin, Message, UrlLink
from wechaty.user.url_link import UrlLinkPayload
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty import WechatyPlugin


class SendUrlLinkPlugin(WechatyPlugin):
    """say something when receive ding, and you can configure it under the settings.
    """
    VIEW_URL = '/api/plugins/send_url_link/'

    async def blueprint(self, app: Quart) -> None:
        @app.route(self.VIEW_URL)
        def send_url_link_view():
            basedir = os.path.dirname(__file__)
            with open(os.path.join(basedir, 'view.html'), 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        
        def get_ids(value):
            if not value:
                return []
            if isinstance(value, str):
                return [value]
            return value
        
        @app.route(self.VIEW_URL + "/send", methods=['POST'])
        async def send_url_link_api():
            json_data = await request.get_json()
            url_link = json_data.pop("url_link")
            room_ids = get_ids(json_data.pop("room_ids", None))
            contact_ids = get_ids(json_data.pop('contact_ids', None))

            url_link = UrlLink(payload=UrlLinkPayload(**url_link))
            for room_id in room_ids:
                room = self.bot.Room.load(room_id)
                await room.say(url_link)
            
            for contact_id in contact_ids:
                contact = self.bot.Contact.load(contact_id)
                await contact.say(url_link)
            
            return "ok"