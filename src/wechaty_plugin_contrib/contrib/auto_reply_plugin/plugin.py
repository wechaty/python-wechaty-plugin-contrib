"""AutoReply to someone according to keywords"""
from dataclasses import dataclass, field
from typing import Union, List, Dict

from wechaty import (  # type: ignore
    WechatyPlugin,
    WechatyPluginOptions,
    FileBox,
    Contact,
    Message,
    Room,
    MiniProgram
)

from wechaty_puppet import (    # type: ignore
    get_logger,
)

from wechaty_plugin_contrib.matchers import (
    Matcher,
    MatcherOptions,
    MatcherOption, RoomMatcher, MessageMatcher, ContactMatcher
)

from wechaty_plugin_contrib.exception import (
    WechatyPluginConfigurationError
)


@dataclass
class AutoReplyRule:
    keyword: str
    reply_content: Union[str, FileBox, Contact, Message, MiniProgram]


@dataclass
class AutoReplyOptions(WechatyPluginOptions):
    rules: List[AutoReplyRule] = field(default_factory=list)
    matchers: List[Matcher] = field(default_factory=list)

    # add rules to the specific Matcher
    matcher_rules: Dict[Matcher, List[AutoReplyRule]] = field(default_factory=dict)


logger = get_logger('AutoReplyPlugin')


class AutoReplyPlugin(WechatyPlugin):

    def __init__(self, options: AutoReplyOptions):
        super().__init__(options)

        if not options.rules and not options.matcher_rules.values():
            raise WechatyPluginConfigurationError('rules not found in rules/matcher_rules')

        # if there is no matcher, it should be apply to all of target
        if not options.matchers:
            options.matchers = [RoomMatcher(True), MessageMatcher(True), ContactMatcher(True)]

        self.rule_map: Dict[Matcher, List[AutoReplyRule]] = {}
        # 1. build rules in common data
        for rule in options.rules:
            for matcher in options.matchers:
                if matcher not in self.rule_map:
                    self.rule_map[matcher] = []
                self.rule_map[matcher].append(rule)

        # 2. build the specific rules on matcher
        for matcher, rules in options.matcher_rules.items():
            if matcher not in self.rule_map:
                self.rule_map[matcher] = []
            self.rule_map[matcher].extend(rules)

    @property
    def matcher_options(self) -> List[Matcher]:
        if not isinstance(self.options, AutoReplyOptions):
            raise TypeError(f'{self} is not AutoReplyOptions type')
        return self.options.matchers

    async def is_match(self, target: Union[Contact, Message, Room]):
        """if there is only one rule which match the target, return True"""
        for option in self.matcher_options:
            _is_match = await option.match(target)
            if _is_match:
                return True
        return False

    async def on_message(self, msg: Message):
        """check the keyword and reply to talker"""

        conversation: Union[Room, Contact] = msg.room() if msg.room() else msg.talker()
        await conversation.ready()

        text = msg.text()

        # find the match rules
        for matcher, rules in self.rule_map.items():
            is_match = await matcher.match(conversation)

            if is_match:
                for rule in rules:
                    if rule.keyword == text:
                        await conversation.say(rule.reply_content)
