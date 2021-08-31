"""Chat history plugin"""
import os
from typing import Optional, List
from dataclasses import dataclass, field
from wechaty_puppet import MessageType  # type: ignore
from wechaty import Message, get_logger  # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (  # type: ignore
    Column,
    Integer,
    DateTime,
    VARCHAR,
    Text
)

logger = get_logger('ChatHistoryPlugin')

SUPPORTED_MESSAGE_FILE_TYPES: List[MessageType] = [
    MessageType.MESSAGE_TYPE_ATTACHMENT,
    MessageType.MESSAGE_TYPE_IMAGE,
    MessageType.MESSAGE_TYPE_EMOTICON,
    MessageType.MESSAGE_TYPE_VIDEO,
    MessageType.MESSAGE_TYPE_AUDIO
]

Base = declarative_base()


class ChatHistory(Base):
    """ChatHistory"""
    __tablename__ = 'ChatHistory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    msg_id = Column(Integer, default=None)
    msg_date = Column(DateTime, default=None)
    msg_type = Column(Integer, default=None)
    msg_room = Column(VARCHAR(50), default=None)
    msg_talker = Column(VARCHAR(50), default=None)
    msg_receiver = Column(VARCHAR(50), default=None)
    msg_text = Column(Text, default=None)


@dataclass
class ChatHistoryPluginOptions(WechatyPluginOptions):
    """
    chat history plugin options
    """
    chat_history_path: str = field(default_factory=str)
    chat_history_database: str = field(default_factory=str)


class ChatHistoryPlugin(WechatyPlugin):
    """chat history plugin"""

    def __init__(self, options: Optional[ChatHistoryPluginOptions] = None):
        super().__init__(options)
        if not options.chat_history_path:
            self.chat_history_path = os.path.join(os.getcwd(), 'chathistory')
        if not os.path.exists(self.chat_history_path):
            os.makedirs(self.chat_history_path)
        if not options.chat_history_database:
            self.chat_history_database = 'sqlite+aiosqlite:///chathistory.db'
        else:
            self.chat_history_database = options.chat_history_database

    @property
    def name(self) -> str:
        return 'chat-history'

    async def on_message(self, msg: Message):
        """listen message event"""
        async_engine = create_async_engine(self.chat_history_database)
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async_session = sessionmaker(async_engine,
                                     expire_on_commit=False,
                                     class_=AsyncSession)
        async with async_session() as session:
            async with session.begin():
                chathistroy = ChatHistory(
                    msg_id=msg.message_id,
                    msg_date=msg.date(),
                    msg_type=msg.type(),
                    msg_room=str(msg.room()) if msg.payload.room_id else None,
                    msg_talker=str(
                        msg.talker()) if msg.payload.from_id else None,
                    msg_receiver=str(msg.to()) if msg.payload.to_id else None,
                    msg_text=msg.text()
                )
                session.add(chathistroy)
            await session.commit()
        await async_engine.dispose()

        if msg.type() in SUPPORTED_MESSAGE_FILE_TYPES:
            file_box = await msg.to_file_box()
            if file_box is not None:
                await file_box.to_file(os.path.join(self.chat_history_path, file_box.name))
