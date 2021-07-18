"""fake Message Target"""
from __future__ import annotations
from wechaty import Message


class FakeMessage(Message):
    """Fake Message for unit test"""
    def __init__(self, message: str = 'wechaty', message_id: str = 'fake-id'):
        self.message = message
        self.message_id = message_id

    def text(self) -> str:
        """return fake message"""
        return self.message

    async def ready(self):
        pass
