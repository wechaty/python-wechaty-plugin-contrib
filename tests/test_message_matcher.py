"""unit test for message matcher"""
import re

from tests.fake_message import FakeMessage
from wechaty_plugin_contrib.matchers import MessageMatcher


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



