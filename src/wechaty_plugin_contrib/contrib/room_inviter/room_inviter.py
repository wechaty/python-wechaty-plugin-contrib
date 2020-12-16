"""AutoReply to someone according to keywords"""
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from typing import Union, List, Dict, Optional

from wechaty import (  # type: ignore
    WechatyPlugin,
    WechatyPluginOptions,
    FileBox,
    Contact,
    Message, Room, Wechaty
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
class RoomInviterOptions(WechatyPluginOptions):
    # add rules to the specific Matcher
    rules: Dict[MessageMatcher, Union[List[RoomMatcher], RoomMatcher]] = field(default_factory=dict)
    welcome: str = field(default_factory=str)


logger = get_logger('RoomInviterPlugin')


class RoomInviterPlugin(WechatyPlugin):

    def __init__(self, options: RoomInviterOptions):
        super().__init__(options)
        if not options or not options.rules:
            raise ValueError('options is required, please add matcher rules')

        self.rules: Dict[MessageMatcher, List[RoomMatcher]] = {}
        for matcher, room_obj in options.rules.items():
            if not room_obj:
                raise ValueError(f'matcher<{matcher}> can not match the target room')
            if isinstance(room_obj, RoomMatcher):
                self.rules[matcher] = [room_obj]
            elif isinstance(room_obj, list):
                self.rules[matcher] = room_obj
            else:
                raise ValueError(f'configuration is error')
        self.welcome_ids: Dict[str, List[str]] = defaultdict(list)
        self.welcome_words = options.welcome

    async def init_plugin(self, wechaty: Wechaty):
        """listen room-join events and say welcome"""
        async def on_room_join(room: Room, invitees: List[Contact], *args):
            if room.room_id in self.welcome_ids:
                for invited_contact in invitees:
                    if invited_contact.contact_id in self.welcome_ids[room.room_id]:
                        await room.say(
                            self.welcome_words,
                            mention_ids=[invited_contact.contact_id]
                        )
                        self.welcome_ids[room.room_id].remove(
                            invited_contact.contact_id
                        )

        wechaty.on('room-join', on_room_join)

    async def on_message(self, msg: Message):
        """check the keyword and reply to talker"""

        # don't listen in room
        if msg.room():
            return

        talker = msg.talker()

        for message_matcher, rules in self.rules.items():
            is_match = await message_matcher.match(msg)

            if is_match:
                # cache the rooms data
                rooms = []
                for rule in rules:
                    # pytype: disable=attribute-error
                    matched_rooms = await rule.find_rooms(self.bot)
                    rooms.extend(matched_rooms)

                # invite person to the room
                for room in rooms:
                    self.welcome_ids[room.room_id].append(talker.contact_id)
                    await room.add(talker)
