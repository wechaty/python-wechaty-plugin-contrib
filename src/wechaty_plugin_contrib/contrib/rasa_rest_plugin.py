"""basic ding-dong bot for the wechaty plugin"""
from __future__ import annotations
from typing import List, Optional, Union
from dataclasses import dataclass, field
import requests

from wechaty import Message, Contact, Room, get_logger  # type: ignore
from wechaty.exceptions import WechatyPluginError   # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore
from wechaty_grpc.wechaty.puppet import MessageType     # type: ignore


log = get_logger('DingDongPlugin')


@dataclass
class RasaRestPluginOptions(WechatyPluginOptions):
    """Rasa Rest Connector Options
    """
    endpoint: Optional[str] = None
    conversation_ids: List[str] = field(default_factory=list)


class RasaRestPlugin(WechatyPlugin):
    """rasa server channnel connector"""
    def __init__(self, options: Optional[RasaRestPluginOptions] = None):
        super().__init__(options)
        if not options or not options.endpoint:
            raise WechatyPluginError(
                'please set the endpoint config to RasaRestPlugin, '
                'you can use RasaRestPluginOptions or kwargs'
            )
        endpoint = options.endpoint
        if not endpoint.endswith('webhooks/rest/webhook'):
            if not endpoint.endswith('/'):
                endpoint += '/'

            endpoint = f'{endpoint}webhooks/rest/webhook'
        self.endpoint = endpoint
        self.conversation_ids: List[str] = options.conversation_ids if options else []

    @property
    def name(self):
        """name of the plugin"""
        return 'rasa-rest-plugin'

    async def on_message(self, msg: Message):
        """listen message event"""
        talker = msg.talker()
        room = msg.room()

        conversation_id = room.room_id if room else talker.contact_id

        # 1. TODO: use finder to match Room/Contact
        if self.conversation_ids and conversation_id not in self.conversation_ids:
            return

        # only process the plain text message
        if msg.type() != MessageType.MESSAGE_TYPE_TEXT:
            return

        mention_self = await msg.mention_self()
        if not mention_self and room:
            return

        text: str = msg.text()

        mention_list: List[Contact] = await msg.mention_list()
        for contact in mention_list:
            await contact.ready()
            mention_text = f'@{contact.name}'
            if mention_text in text:
                text = text.replace(mention_text, '')

        text = text.strip()
        rasa_response = requests.post(
            self.endpoint,
            json=dict(
                sender=conversation_id,
                message=text
            )
        )
        messages: List[dict] = rasa_response.json()
        if len(messages) == 0:
            return

        if room:
            for message in messages:
                msg_text = message.get('text', None)
                if not msg_text:
                    continue
                await room.say(msg_text, mention_ids=[talker.contact_id])
        else:
            for message in messages:
                msg_text = message.get('text', None)
                if not msg_text:
                    continue
                await talker.say(msg_text)
