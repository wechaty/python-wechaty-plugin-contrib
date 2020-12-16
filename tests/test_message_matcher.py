"""unit test for message matcher"""
import re

from wechaty import Message

from wechaty_plugin_contrib.matchers import MessageMatcher


class FakeMessage(Message):
    """Fake Message for unit test"""
    def __init__(self, message: str = 'wechaty', message_id: str = 'fake-id'):
        self.message = message
        self.message_id = message_id

    def text(self) -> str:
        """return fake message"""
        return self.message


async def test_message_matcher_with_str():
    # 1. define the matcher

    matcher = MessageMatcher('wechaty')

    # 2. true test
    msg = FakeMessage(
        message='wechaty'
    )
    assert await matcher.match(msg)

    # 3. fake test
    msg = FakeMessage(
        message='python-wechaty'
    )
    assert not await matcher.match(msg)


async def test_message_matcher_with_patten():
    # 1. define the matcher
    matcher = MessageMatcher(re.compile(r'^wechaty$'))

    # 2. true test
    msg = FakeMessage(
        message='wechaty'
    )
    assert await matcher.match(msg)

    msg = FakeMessage(
        message='python-wechaty'
    )
    assert not await matcher.match(msg)

    # 3. fake test
    msg = FakeMessage(
        message='wechat'
    )
    assert not await matcher.match(msg)



