from __future__ import annotations
from typing import List, Optional, Union
from dataclasses import dataclass
from wechaty import WechatyPlugin, Friendship, WechatyPluginOptions
from wechaty_plugin_contrib.message_controller import message_controller


@dataclass
class OnFriendshipPluginOptions(WechatyPluginOptions):
    auto_accept: Optional[bool] = None
    keywords: Optional[Union[str, List[str]]] = None
    first_hello: Optional[str] = None


class OnFriendshipPlugin(WechatyPlugin):
    """handle the friendship event, and can say something to new friend. you can configure it under the setting.
    
    setting schema:
        {
            "auto_accept": bool = false,
            "keyword": Union[str, List[str]] = "",
            "first_hello": str = "first hello to the new friend"
        }
    """
    def __init__(self, options: Optional[OnFriendshipPluginOptions] = None):
        super().__init__(options)

        self.options: OnFriendshipPluginOptions = self.options
        
        if not self.options.auto_accept:
            self.options.auto_accept = self.setting.get('auto_accept', False)

    @message_controller.may_disable_message
    async def on_friendship(self, friendship: Friendship) -> None:
        if self.options.auto_accept:
            await friendship.accept()
            return
        
        if not self.options.keywords:
            return
        
        if isinstance(self.options.keywords, str):
            keywords = [self.options.keywords]
        else:
            keywords = self.options.keywords

        for keyword in keywords:
            if keyword == friendship.hello():
                await friendship.accept()
                return
