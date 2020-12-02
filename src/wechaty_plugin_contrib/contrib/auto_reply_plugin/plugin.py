"""AutoReply to someone according to keywords"""
from dataclasses import dataclass, field
from typing import Union, List, Dict

from wechaty import (   # type: ignore
    WechatyPlugin,
    WechatyPluginOptions,
    FileBox,
    Contact,
    Message
)

from wechaty_puppet import (    # type: ignore
    get_logger
)


@dataclass
class AutoReplyRule:
    keyword: str
    reply_content: Union[str, FileBox, Contact]


@dataclass
class AutoReplyOptions(WechatyPluginOptions):
    rules: List[AutoReplyRule] = field(default_factory=list)


logger = get_logger('AutoReplyPlugin')


class AutoReplyPlugin(WechatyPlugin):

    def __init__(self, options: AutoReplyOptions):
        super().__init__(options)

        self.rule_map: Dict[str, AutoReplyRule] = {}
        if options.rules:
            self.rule_map = {rule.keyword: rule for rule in options.rules}

    async def on_message(self, msg: Message):
        """check the keyword and reply to talker"""
        text = msg.text()

        if text in self.rule_map:
            room = msg.room()
            if room:
                await room.ready()
                await room.say(self.rule_map[text])
            else:
                talker = msg.talker()
                await talker.ready()
                await talker.say(self.rule_map[text])
