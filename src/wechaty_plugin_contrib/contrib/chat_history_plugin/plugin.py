"""Chat history plugin"""
import os
import aiosqlite
from typing import Optional, List
from dataclasses import dataclass, field
from wechaty_puppet import MessageType  # type: ignore
from wechaty import Message, get_logger  # type: ignore
from wechaty.plugin import WechatyPlugin, WechatyPluginOptions  # type: ignore


logger = get_logger('ChatHistoryPlugin')

SUPPORTED_MESSAGE_FILE_TYPES: List[MessageType] = [
    MessageType.MESSAGE_TYPE_ATTACHMENT,
    MessageType.MESSAGE_TYPE_IMAGE,
    MessageType.MESSAGE_TYPE_EMOTICON,
    MessageType.MESSAGE_TYPE_VIDEO,
    MessageType.MESSAGE_TYPE_AUDIO
]


@dataclass
class ChatHistoryPluginOptions(WechatyPluginOptions):
    """
    chat history plugin options
    """
    chat_history_path: str = field(default_factory=str)


class ChatHistoryPlugin(WechatyPlugin):
    """chat history plugin"""

    def __init__(self, options: Optional[ChatHistoryPluginOptions] = None):
        super().__init__(options)
        if not options.chat_history_path:
            self.chat_history_path = os.path.join(os.getcwd(), 'chathistory')
        if not os.path.exists(self.chat_history_path):
            os.makedirs(self.chat_history_path)
        self.database_path = os.path.join(
            self.chat_history_path, 'chathistory.db')

    @property
    def name(self) -> str:
        return 'chat-history'

    async def on_message(self, msg: Message):
        """listen message event"""
        msg_id = msg.message_id
        msg_date = msg.date()
        msg_talker = str(msg.talker()) if msg.payload.from_id else None
        msg_to = str(msg.to()) if msg.payload.to_id else None
        msg_room = str(msg.room()) if msg.payload.room_id else None
        msg_text = msg.text()
        msg_type = msg.type()
        message = (msg_date, msg_id, msg_type,
                   msg_talker, msg_to, msg_room, msg_text)

        conn = await aiosqlite.connect(self.database_path)
        create_database_sql = """
        CREATE TABLE IF NOT EXISTS ChatHistory(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            msg_date DATETIME DEFAULT NULL,
            msg_id VARCHAR(50) DEFAULT NULL,
            msg_type INTEGER DEFAULT NULL,
            msg_talker VARCHAR(50) DEFAULT NULL,
            msg_to VARCHAR(50) DEFAULT NULL,
            msg_room VARCHAR(50) DEFAULT NULL,
            msg_text TEXT DEFAULT NULL
        );
        """
        await conn.execute(create_database_sql)
        insert_table_sql = """
        INSERT INTO ChatHistory (msg_date, msg_id, msg_type, msg_talker, msg_to, msg_room, msg_text) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        await conn.execute(insert_table_sql, message)
        await conn.commit()
        await conn.close()

        if msg.type() in SUPPORTED_MESSAGE_FILE_TYPES:
            file_box = await msg.to_file_box()
            if file_box is not None:
                await file_box.to_file(os.path.join(self.chat_history_path, file_box.name))
