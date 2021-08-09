"""import all contrib"""

# Finder & Matcher
from wechaty_plugin_contrib.finders.finder import FinderOptions, FinderOption
from wechaty_plugin_contrib.finders.contact_finder import ContactFinder
from wechaty_plugin_contrib.finders.room_finder import RoomFinder

# Plugin List
from wechaty_plugin_contrib.contrib.ding_dong_plugin import DingDongPlugin
from wechaty_plugin_contrib.contrib.daily_plugin import (
    DailyPluginOptions,
    DailyPlugin
)
from wechaty_plugin_contrib.contrib.auto_reply_plugin import (
    AutoReplyOptions, AutoReplyPlugin,
    AutoReplyRule
)

from wechaty_plugin_contrib.contrib.github_webhook_plugin import (
    GithubHookItem,
    GithubContentType,
    GithubWebhookOptions
)

from wechaty_plugin_contrib.contrib.rasa_rest_plugin import (
    RasaRestPlugin,
    RasaRestPluginOptions
)

from wechaty_plugin_contrib.contrib.room_inviter import (
    RoomInviterOptions,
    RoomInviterPlugin
)

__all__ = [
    'FinderOptions',
    'FinderOption',

    'ContactFinder',
    'RoomFinder',

    'DingDongPlugin',

    'DailyPluginOptions',
    'DailyPlugin',

    'RasaRestPluginOptions',
    'RasaRestPlugin',

    'AutoReplyRule',
    'AutoReplyOptions',
    'AutoReplyPlugin',

    'GithubHookItem',
    'GithubContentType',
    'GithubWebhookOptions',

    'RasaRestPlugin',
    'RasaRestPluginOptions',

    'RoomInviterOptions',
    'RoomInviterPlugin'

]
