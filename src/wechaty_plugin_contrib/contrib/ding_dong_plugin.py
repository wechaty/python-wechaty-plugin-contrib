from __future__ import annotations
from wechaty import WechatyPlugin, Message
from wechaty_plugin_contrib.message_controller import message_controller
from wechaty import WechatyPlugin

class DingDongPlugin(WechatyPlugin):
    """say something when receive ding, and you can configure it under the settings.

    setting schema: 
        {
            "ding": "dong",
            // or

            "ding": [
                "I'm alive",
                "dong"
            ]
        }
    """
    VIEW_URL = '/api/plugins/ding_dong/view'

    @message_controller.may_disable_message
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            dong = self.setting.get("ding", "dong")
            if isinstance(dong, list):
                words = []
            else:
                words = [dong]

            for word in words:
                await msg.say(word)

            message_controller.disable_all_plugins(msg)