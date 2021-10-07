"""
use two plugins - example code to show how to use two or more plugins.

Authors:    xinyu3ru (汝欣) <https://github.com/xinyu3ru>

2021-now @ Copyright xinyu3ru

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# pylint: disable=R0801
import asyncio, os, logging
from typing import List, Optional, Union, Dict
#os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = '2250924e-1c49-c10fb69eebc3'
#os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '192.168.1.8:8788'
#os.environ['WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_CLIENT'] = 'True'




from wechaty import (
    MessageType,
    FileBox,
    RoomMemberQueryFilter,
    Wechaty,
    Contact,
    Room,
    Message,
    Image,
    MiniProgram, 
    Friendship, 
    FriendshipType
)

from wechaty_plugin_contrib.contrib import (
    RoomInviterOptions,
    RoomInviterPlugin
)
from wechaty_plugin_contrib.matchers import (
    MessageMatcher,
    RoomMatcher
)

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions,
)

from wechaty_plugin_contrib.matchers import ContactMatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """

    def __init__(self):
        """initialization function
        """
        self.login_user: Optional[Contact] = None
        super().__init__()

    # pylint: disable=R0912,R0914,R0915
    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact: Contact = msg.talker()
        text: str = msg.text()
        room: Optional[Room] = msg.room()
        msg_type: MessageType = msg.type()
        file_box: Optional[FileBox] = None
        if text == 'ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('咚！')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)

        elif text in ['你好', '您好', 'hi', 'hello', '在吗', '在吗？', '晚上好', '中午好']:
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('你好呀，我在这里等你好久了~')

        elif text in ['晚安', '早点睡', 'good night', '我困了']:
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('晚安哟~')


        elif msg_type == MessageType.MESSAGE_TYPE_IMAGE:
            logger.info('receving image file')
            # file_box: FileBox = await msg.to_file_box()
            image: Image = msg.to_image()

            hd_file_box: FileBox = await image.hd()
            await hd_file_box.to_file('./hd-image.jpg', overwrite=True)
            #使用时需要注意保存好友名称、时间戳、分文件夹等关键信息。
            thumbnail_file_box: FileBox = await image.thumbnail()
            await thumbnail_file_box.to_file('./thumbnail-image.jpg', overwrite=True)
            artwork_file_box: FileBox = await image.artwork()
            await artwork_file_box.to_file('./artwork-image.jpg', overwrite=True)
            # reply the image
            await msg.say(hd_file_box)

        elif msg_type in [MessageType.MESSAGE_TYPE_AUDIO, MessageType.MESSAGE_TYPE_ATTACHMENT, MessageType.MESSAGE_TYPE_VIDEO]:
            logger.info('receving file ...')
            file_box = await msg.to_file_box()
            if file_box:
                await file_box.to_file(file_box.name)

        elif msg_type == MessageType.MESSAGE_TYPE_MINI_PROGRAM:
            logger.info('receving mini-program ...')
            mini_program: Optional[MiniProgram] = await msg.to_mini_program()
            if mini_program:
                await msg.say(mini_program)

        elif text == 'get room members' and room:
            logger.info('get room members ...')
            room_members: List[Contact] = await room.member_list()
            names: List[str] = [
                room_member.name for room_member in room_members]
            await msg.say('\n'.join(names))

        elif text.startswith('remove room member:'):
            logger.info('remove room member:')
            if not room:
                await msg.say('this is not room zone')
                return
            room_member_name = text[len('remove room member:') + 1:]
            room_member: Optional[Contact] = await room.member(
                query=RoomMemberQueryFilter(name=room_member_name)
            )
            if room_member:
                if self.login_user and self.login_user.contact_id in room.payload.admin_ids:
                    await room.delete(room_member)
                else:
                    await msg.say('登录用户不是该群管理员...')
            else:
                await msg.say(f'can not fine room member by name<{room_member_name}>')
        elif text.startswith('get room topic'):
            logger.info('get room topic')
            if room:
                topic: Optional[str] = await room.topic()
                if topic:
                    await msg.say(topic)

        elif text.startswith('rename room topic:'):
            logger.info('rename room topic ...')
            if room:
                new_topic = text[len('rename room topic:') + 1:]
                await msg.say(new_topic)
        elif text.startswith('add new friend:'):
            logger.info('add new friendship ...')
            identity_info = text[len('add new friend:') + 1:]
            weixin_contact: Optional[Contact] = await self.Friendship.search(weixin=identity_info)
            phone_contact: Optional[Contact] = await self.Friendship.search(phone=identity_info)
            contact: Optional[Contact] = weixin_contact or phone_contact
            if contact:
                self.Friendship.add(contact, 'hello world ...')

        elif text.startswith('at me'):
            await msg.say(self.login_user)

        else:
            pass


    async def on_friendship(self, friendship: Friendship):
        """
        处理好友请求
        """
        administrator = bot.Contact.load('admin-id')
        await administrator.ready()

        contact = friendship.contact()
        await contact.ready()

        log_msg = f' {contact.name} 请求加好友'
        await administrator.say(log_msg)

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            if friendship.hello():# == 'ding':
                # log_msg = 'accepted automatically because verify messsage is "ding"'
                log_msg = '自动通过好友'
                await asyncio.sleep(2)
                print('等待通过好友 ...')
                await friendship.accept()
                # if want to send msg, you need to delay sometimes

                print('等待发送欢迎消息 ...')
                await asyncio.sleep(3)
                await contact.say('你好')
                await contact.say('如果知道入群关键词，可以直接发我关键词哟')
                print('已经通过好友 ...')
            else:
                log_msg = 'not auto accepted, because verify message is: ' + friendship.hello()

        elif friendship.type() == FriendshipType.FRIENDSHIP_TYPE_CONFIRM:
            log_msg = 'friend ship confirmed with ' + contact.name

        print(log_msg)
        await administrator.say(log_msg)

 
    async def on_login(self, contact: Contact):
        """login event
        Args:
            contact (Contact): the account logined
        """
        logger.info('微信号<%s> 已经登录……', contact)
        self.login_user = contact



bot: Optional[MyBot] = None


async def main():
    """main() code"""
    global bot
    rules: Dict[MessageMatcher, RoomMatcher] = {
            #根据实际情况修改
            MessageMatcher('4群'): RoomMatcher('业主4群'),
            MessageMatcher('5群'): RoomMatcher('业主5群'),
    }
    room_inviter_plugin = RoomInviterPlugin(options=RoomInviterOptions(
        name='python-wechaty关键字入群插件',
        rules=rules,
        welcome = 'welcome'
    ))
    img_url = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy' \
              '/it/u=1257042014,3164688936&fm=26&gp=0.jpg'
    plugin_autoreply = AutoReplyPlugin(options=AutoReplyOptions(
        rules=[
            AutoReplyRule(keyword='dada', reply_content='dudu'),
            AutoReplyRule(keyword='七龙珠', reply_content='我爱七龙珠'),
            AutoReplyRule(
                keyword='七龙珠',
                reply_content=FileBox.from_url(img_url, name='python.png')
            ),
            AutoReplyRule(keyword='李白',reply_content='将进酒-李白，剩下的我忘了/(ㄒoㄒ)/~~'),
            AutoReplyRule(keyword='网易',reply_content='云音乐')
        ],

    ))
    bot = MyBot()
    bot.use([plugin_autoreply, room_inviter_plugin])
    await bot.start()


asyncio.run(main())
