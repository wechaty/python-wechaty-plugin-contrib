"""
Python Plugin repo - https://github.com/wechaty/python-wechaty-plugin-contrib

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

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

from wechaty import Wechaty     # type: ignore


from wechaty import (
    WechatyPlugin,
    Message,
    MessageType
)


class MessagerPlugin(WechatyPlugin):

    @property
    def name(self) -> str:
        return 'messager-plugin'

    def on_message(self, msg: Message):
        """handle the template parsing"""

        # only handle the text message type
        if msg.type() != MessageType.MESSAGE_TYPE_TEXT:
            return

        #
    async def init_plugin(self, wechaty: Wechaty):
        """初始化数据"""
        pass
