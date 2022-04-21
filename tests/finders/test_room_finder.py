"""Room Finder Unit Test"""
from typing import List
from uuid import uuid4
import re
import pytest
from faker import Faker

from wechaty import Room, Wechaty, WechatyOptions
from wechaty_puppet import Puppet, PuppetOptions, RoomPayload

from wechaty_plugin_contrib.finders.room_finder import RoomFinder
from ..conftest import FakePuppet


def _construct_room_payload_width_topic(topic: str) -> RoomPayload:
    return RoomPayload(
        id=str(uuid4()),
        topic=topic,
        owner_id='wechaty_user',
        member_ids=['wechaty_user', 'fake_user', 'test_user'],
        admin_ids=['wechaty_user'],
        avatar=''
    )


@pytest.fixture
def fake_puppet() -> Puppet:
    """create fake puppet to test room finder"""
    puppet = FakePuppet(options=PuppetOptions())

    # 1. add wechaty room
    for index in range(100):
        puppet.add_room(
            _construct_room_payload_width_topic(f'Wechaty Chatroom #{index}')
        )
    # 2. add random string room
    faker: Faker = Faker()
    for _ in range(20):
        puppet.add_room(
            _construct_room_payload_width_topic(
                faker.name()
            )
        )
    return puppet


@pytest.fixture
@pytest.mark.asyncio
async def bot(fake_puppet: Puppet) -> Wechaty:
    """bot with fake puppet"""
    wechaty_bot = Wechaty(options=WechatyOptions(puppet=fake_puppet))
    await wechaty_bot.init_puppet()
    return wechaty_bot


@pytest.mark.asyncio
async def test_simple_room_finder(bot: Wechaty) -> None:
    """test simple room finder"""
    rooms: List[Room] = await bot.Room.find_all()
    assert len(rooms) == 120


@pytest.mark.asyncio
async def test_room_finder_with_pattern(bot: Wechaty) -> None:
    """test room finder"""
    option = re.compile(r'^Wechaty Chatroom #(\d+)$')
    room_finder: RoomFinder = RoomFinder(option)
    rooms: List[Room] = await room_finder.match(bot)
    assert len(rooms) == 100


@pytest.mark.asyncio
async def test_room_finder_with_string(bot: Wechaty) -> None:
    """test room finder"""
    room_finder: RoomFinder = RoomFinder('Wechaty Chatroom #1')
    rooms: List[Room] = await room_finder.match(bot)
    assert len(rooms) == 1
