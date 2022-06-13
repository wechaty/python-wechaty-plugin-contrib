"""basic ding-dong bot for the wechaty plugin"""
import os
from typing import Optional

from wechaty import FileBox, Message, MessageType, WechatyPluginOptions, WechatyPlugin
from wechaty_puppet import get_logger


class VoiceRepeaterPlugin(WechatyPlugin):
    """Voice Repeater Plugin"""
    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        super().__init__(options)
        self.cache_dir = f'.wechaty/{self.name}'
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = get_logger(self.name, f'{self.cache_dir}/log.log')

    async def on_message(self, msg: Message) -> None:
        """listen message event"""
        if msg.room():
            return

        if msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
            file_box = await msg.to_file_box()
            saved_file = os.path.join(self.cache_dir, file_box.name)
            await file_box.to_file(saved_file)
            new_audio_file = FileBox.from_file(saved_file)
            await msg.talker().say(new_audio_file)
