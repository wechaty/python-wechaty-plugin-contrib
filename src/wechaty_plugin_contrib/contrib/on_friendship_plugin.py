from __future__ import annotations
from wechaty import WechatyPlugin, Friendship


class OnFriendshipPlugin(WechatyPlugin):
    """handle the friendship event, and can say something to new friend. you can configure it under the setting.
    
    setting schema:
        {
            "accept_all": bool = false,
            "keyword": Union[str, List[str]] = "",
        }
    """
    def __init__(self):
        """init plugin"""
        super().__init__()
        self._init_setting()
    
    def _init_setting(self):
        """init default configuration"""
        default_value = {
            "accept_all": True,
            "keywords": []
        }
        default_value.update(self.setting)
        self.setting = default_value

    async def on_friendship(self, friendship: Friendship) -> None:
        if self.setting['accept_all']:
            await friendship.accept()
        else:
            hello = await friendship.hello()
            for keyword in self.setting.get("keywords", []):
                if keyword in hello:
                    await friendship.accept()
                    break