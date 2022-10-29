import asyncio
from typing import List
from wechaty import WechatyPlugin, Contact
from quart import Quart
from wechaty import WechatyPlugin
from wechaty_plugin_contrib.utils import success

class APIPlugin(WechatyPlugin):
    VIEW_URL = '/api/plugins/api'
    UI_DIR = "./src/plugins/views/assets"

    async def blueprint(self, app: Quart) -> None:

        @app.route(self.VIEW_URL + '/room_select')
        async def api_get_room_select():
            room_select = []
            rooms = await self.bot.Room.find_all()
            for room in rooms:
                if not room.payload.topic or not room.room_id:
                    continue
                room_select.append(dict(
                    value=room.room_id,
                    label=room.payload.topic
                ))
            
            return success(room_select)

        @app.route(self.VIEW_URL + '/contact_select')
        async def api_get_contact_select():
            contact_select = []
            contacts: List[Contact] = await self.bot.Contact.find_all()
            for contact in contacts:
                if not contact.payload.friend:
                    continue
                contact_select.append(dict(
                    value=contact.contact_id,
                    label=contact.payload.alias or contact.payload.name
                ))
            
            return success(contact_select)

        @app.route(self.VIEW_URL + '/info_select')
        async def api_get_info_select():
            room_select = []
            rooms = await self.bot.Room.find_all()
            for room in rooms:
                if not room.payload.topic or not room.room_id:
                    continue
                room_select.append(dict(
                    value=room.room_id,
                    label= "群：" + room.payload.topic
                ))

            contact_select = []
            contacts: List[Contact] = await self.bot.Contact.find_all()
            for contact in contacts:
                if not contact.payload.friend:
                    continue
                contact_select.append(dict(
                    value=contact.contact_id,
                    label="联系人：" + (contact.payload.alias or contact.payload.name)
                ))
            contact_select.extend(room_select) 
            return success(contact_select)