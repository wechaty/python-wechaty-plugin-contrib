from codecs import ignore_errors
import json
import os
from typing import (
    Optional, Union
)
from quart import Quart, jsonify, request

from wechaty import (
    WechatyPlugin,
    Contact,
    Room,
    Message,
    FileBox,
    MessageType,
    WechatyPluginOptions
)
from wechaty_plugin_contrib.finders.room_finder import RoomFinder
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty_plugin_contrib.utils import success


class MessageForwarderPlugin(WechatyPlugin):
    VIEW_URL = "/plugins/message_forwarder"
    def __init__(
        self,
        options: Optional[WechatyPluginOptions] = None,
        file_box_interval_seconds: int = 2
    ):
        super().__init__(options)
        self.file_box_interval_seconds: int = file_box_interval_seconds

    def get_room_finder(self) -> Optional[RoomFinder]:
        """get_room_finder with dynamic style

        Returns:
            RoomFinder: the instance of RoomFinder
        """
        # 1. init the room finder
        options = []
        for room_id in self.setting['room_ids']:
            options.append(room_id)
        if options:
            return RoomFinder(options)
        return None
    
    async def blueprint(self, app: Quart) -> None:
        @app.route(self.VIEW_URL)
        async def message_forwarder_view():
            basedir = os.path.dirname(__file__)
            with open(os.path.join(basedir, 'message_forwarder_plugin.html'), 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        
        @app.route(self.VIEW_URL + "/groups", methods=['GET'])
        async def get_message_forwarder_group_names():
            """the data structure is the following:
            {
                "group_name": {
                    "ids": [""],
                    "room_ids": [""],
                    "contact_ids": [""],
                },
                ...
            }
            """
            keys = list(self.setting.keys())
            if len(keys) == 0:
                self.setting['default'] = {}
            keys =[dict(value=key, label=key) for key in list(self.setting.keys())]
            return success(keys)
        
        @app.route(self.VIEW_URL + "/setting/<group>", methods=['GET'])
        async def get_message_forwarder_setting(group: str):
            """the data structure is the following:
            {
                "group_name": {
                    "admin_ids": [""],
                    "room_ids": [""],
                    "contact_ids": [""],
                },
                ...
            }
            """
            if self.setting[group] == 0:
                self.setting[group] = {}
            return success(self.setting[group])
            
        @app.route(self.VIEW_URL + "/setting/<group>", methods=['POST'])
        async def set_message_forwarder_setting(group: str):
            request_setting = await request.get_json()
            setting = self.setting
            setting[group] = request_setting
            self.setting = setting
            return success("ok")

    def get_admin_group(self, msg: Message) -> Optional[str]:
        """get the group_name if talker is admin

        Args:
            msg (Message): the message body

        Returns:
            Optional[str]: the name of group
        """
        conv_id = msg.conv_id(msg)
        
        for group_name, group_setting in self.setting.items():
            admin_ids = group_setting['admin_ids']
            if admin_ids == 0:
                continue
            if conv_id in admin_ids:
                return group_name
        return None

    async def forward_message(self, msg: Message, target: Union[Contact, Room]):
        """forward the message to the target conversations

        Args:
            msg (Message): the message to forward
            target (Union[Contact, Room]): the target which message to forwrad
        """
        self.logger.info(f"start to forward msg<{msg}> to target<{target}> ...")
        file_box = None
        if msg.type() in [MessageType.MESSAGE_TYPE_IMAGE, MessageType.MESSAGE_TYPE_VIDEO, MessageType.MESSAGE_TYPE_ATTACHMENT]:
            file_box = await msg.to_file_box()
            file_path = os.path.join(self.cache_dir, "files", file_box.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            await file_box.to_file(file_path, overwrite=True)
            file_box = FileBox.from_file(file_path)
            
        if file_box:
            await target.say(file_box)

        # 如果是文本的话，是需要单独来转发
        elif msg.type() == MessageType.MESSAGE_TYPE_TEXT:
            text = msg.text()
            await target.say(text)

        elif target:
            await msg.forward(target)   

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        group_name = self.get_admin_group(msg)
        if group_name is None:
            return

        # 1. forward the msg to contact_ids
        group_setting = self.setting[group_name]
        contact_ids = group_setting['contact_ids']
        if contact_ids == 0:
            contact_ids = []

        for contact_id in contact_ids:
            contact = self.bot.Contact.load(contact_id)
            await contact.ready()

            await self.forward_message(msg, contact)

        # 2. forward the msg to room_ids
        room_ids = group_setting['room_ids']
        if room_ids == 0:
            room_ids = []

        for room_id in room_ids:
            room = self.bot.Room.load(room_id)
            await room.ready()

            await self.forward_message(msg, room)