"""import all contrib"""
from wechaty_plugin_contrib.ding_dong_plugin import DingDongPlugin
from wechaty_plugin_contrib.daily_plugin import (
    DailyPluginOptions,
    DailyPlugin
)

from wechaty_plugin_contrib.contrib import (
    AutoReplyRule,
    AutoReplyOptions,
    AutoReplyPlugin
)

__all__ = [
    'DingDongPlugin',

    'DailyPluginOptions',
    'DailyPlugin',

    'AutoReplyRule',
    'AutoReplyOptions',
    'AutoReplyPlugin'
]
