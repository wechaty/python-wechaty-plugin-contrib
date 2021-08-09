"""basic ding-dong bot for the wechaty plugin"""
from typing import List, Optional, Union
from dataclasses import dataclass, field
from wechaty import Message, Contact, Room, get_logger  # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore


log = get_logger('DingDongPlugin')


@dataclass
class DingDongPluginOptions(WechatyPluginOptions):
    """
    conversation_id can be contact_id and room_id.

    only one of [include_conversation_ids,exclude_conversation_ids] can be empty
    """
    include_conversation_ids: List[str] = field(default_factory=list)
    exclude_conversation_ids: List[str] = field(default_factory=list)


class DingDongPlugin(WechatyPlugin):
    """basic ding-dong plugin"""
    def __init__(self, options: Optional[DingDongPluginOptions] = None):
        super().__init__(options)

        if options is not None:
            if options.include_conversation_ids is not None and \
                    options.exclude_conversation_ids is not None:
                log.info('only one of [include_conversation_ids, '
                         'exclude_conversation_ids] can be empty ')

        self.options = options

    @property
    def name(self):
        """name of the plugin"""
        return 'ding-dong'

    def can_send_dong(self, conversation_id: str):
        """check if the bot can send dong message"""
        if self.options is None:
            return True
        if self.options.include_conversation_ids is not None:
            if not isinstance(self.options.include_conversation_ids, list):
                log.error('include_conversation_ids should be a list')
            elif conversation_id in self.options.include_conversation_ids:
                return True
        if self.options.exclude_conversation_ids is not None:
            if not isinstance(self.options.exclude_conversation_ids, list):
                log.error('exclude_conversation_ids should be a list')
            elif conversation_id not in self.options.exclude_conversation_ids:
                return True
        return False

    async def on_message(self, msg: Message):
        """listen message event"""
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '#ding':
            conversation: Union[Room, Contact] = from_contact if room is None else room
            conversation_id = from_contact.contact_id if room is None \
                else room.room_id
            if self.can_send_dong(conversation_id):
                await conversation.ready()
                await conversation.say('dong')
