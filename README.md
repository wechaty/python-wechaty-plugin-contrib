# python-wechaty-plugin-contrib [![Python Wechaty Plugin Contrib](https://img.shields.io/badge/python--wechaty--contrib-contrib-green)](https://github.com/wechaty/python-wechaty-plugin-contrib)

 [![pypi Version](https://img.shields.io/badge/pypi-0.0.12-brightgreen)](https://pypi.org/project/wechaty-plugin-contrib/)
 [![pypi](https://img.shields.io/badge/py3.7-pass-brightgreen)](https://github.com/wechaty/python-wechaty-plugin-contrib)

Python Wechaty Plugin Contrib Package for the Community

![Wechaty Plugin](docs/images/plugin.png)

> Image Credit: [What is Plugin](https://www.computerhope.com/jargon/p/plugin.htm)

[![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://github.com/Wechaty/wechaty)
[![Python](https://img.shields.io/badge/Python-brightgreen)](https://www.python.org/)

## Introduction

When you find yourself writing repetitive code, it's time to extract it into a plugin.

Wechaty has a great support for using Plugins by calling `Wechaty.use(WechatyPlugin())`. A Wechaty Plugin is a python class that listen all the event and handle all things. 

This package is for publishing the Wechaty Plugins that are very common used by the core developer team.

## Requirements

1. Wechaty [v0.5.dev1](https://pypi.org/project/wechaty/0.5.dev1/) or above versions

## Plugins Contrib

You are welcome to send your plugin to our contrib by creating a Pull Request!

| # | Plugin | Author | Feature |
| :--- | :--- | :--- | :--- |
| 1 | DingDong | [@wj-Mcat](https://github.com/wj-Mcat) | Reply `dong` if bot receives a `ding` message. |
| 2 | DailyWords | [@wj-Mcat](https://github.com/wj-Mcat) | Say something everyday, like `Daily Words`. |
| 3 | Rasa_Rest | [@wj-Mcat](https://github.com/wj-Mcat) | Rasa server channnel connector. |
| 4 | Scheduler | [@wj-Mcat](https://github.com/wj-Mcat) | Say something everyday, like `Scheduler Words`. |
| 5 | Room_inviter | [@wj-Mcat](https://github.com/wj-Mcat) | Invite peaple to room according keywords and rules then say hello words. |
| 6 | Auto_reply | [@wj-Mcat](https://github.com/wj-Mcat) | AutoReply according keywords. |
| 7 | Chat_history | [@markoxu](https://github.com/markoxu) | Save chat history with files and database. |
| 8 | Github_webhook | [@wj-Mcat](https://github.com/wj-Mcat) | Github webhook, hook infomation to peaple or room when projects were updated. |
| 9 | GitlabEvent | [@wj-Mcat](https://github.com/wj-Mcat) | Gitlab webhook, send gitlab event infomation to peaple or room when projects were updated. |
| 10 | Finders | [@wj-Mcat](https://github.com/wj-Mcat) | Example code How to find room or contact, then do something. |


### 1 DingDong

- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Reply `dong` if bot receives a `ding` message.


```python
from wechaty_plugin_contrib import DingDongPlugin

bot.use(DingDongPlugin())
```

### 2 DailyWords
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description:Say something everyday, like `Daily Words`. 

Example code in examples folder, [daily_plugin_bot](https://github.com/wechaty/python-wechaty-plugin-contrib/blob/master/examples/daily_plugin_bot.py)

### 3 Rasa_Rest
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description:Rasa server channnel connector. 

Example code in examples folder, [rasa_plugin_bot](https://github.com/wechaty/python-wechaty-plugin-contrib/blob/master/examples/rasa_plugin_bot.py)

### 4 Scheduler
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Say something everyday, like `Scheduler Words`. 

```python
from wechaty_plugin_contrib import SchedulerPlugin, SchedulerPluginOptions
#needs more infomations and example code here.
bot.use(SchedulerPlugin())
```

### 5 Room_inviter
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Invite peaple to room according keywords and rules then say hello words.

```python
from wechaty_plugin_contrib import RoomInviterPlugin, RoomInviterOptions
from typing import Dict

rules: Dict[MessageMatcher, RoomMatcher] = {
        MessageMatcher('4群'): RoomMatcher('业主4群'),
        MessageMatcher('5群'): RoomMatcher('业主5群'),
}

room_inviter_plugin = RoomInviterPlugin(options=RoomInviterOptions(
    name='python-wechaty关键字入群插件',
    rules=rules,
    welcome = 'welcome join our group.'
))

bot.use([RoomInviterPlugin()])
```

### 6 Auto_reply
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: AutoReply according keywords. |

Example code in examples folder, [auto-reply-bot](https://github.com/wechaty/python-wechaty-plugin-contrib/blob/master/examples/auto-reply-bot.py)

### 7 Chat_history
- Author: [@markoxu](https://github.com/markoxu)
- Description: Save chat history with files and database.

Example code in examples folder, [chat_history_bot](https://github.com/wechaty/python-wechaty-plugin-contrib/blob/master/examples/chat_history_bot.py)

### 8 Github_webhook
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Github webhook, hook infomation to peaple or room when projects were updated. 

```python
# did't test, needs more infomations and example code here.
from wechaty_plugin_contrib import GithubHookItem, GithubWebhookOptions
bot.use(GithubHookItem())
```

### 9 GitlabEvent
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Gitlab webhook, send gitlab event infomation to peaple or room when projects were updated.

```python
# did't test, needs more infomations and example code here.
from wechaty_plugin_contrib import GitlabEventPlugin, GitlabEventOptions

bot.use(GitlabEventPlugin())
```

### 10 Example code How to find room or contact.
- Author: [@wj-Mcat](https://github.com/wj-Mcat)
- Description: Example code How to find room or contact, then do something.

Example code in examples folder, [Example of Finders](https://github.com/wechaty/python-wechaty-plugin-contrib/blob/master/examples/finders.py)








## Python Wechaty Plugin Directory

The Wechaty Plugin Contrib will only accept simple plugins which does not dependence very heavy NPM modules, and the SLOC (Source Line Of Code) is no more than 100.

There are many great Wechaty Plugins can not be included in the contrib because they are too powerful. They will be published as a pypi package by itself.

We are listing those powerful Wechaty Plugins outside the contrib as in the following list, and you are welcome to add your plugin below if you have published any!

[![Wechaty Plugin Contrib](https://img.shields.io/badge/Wechaty%20Plugin-Directory-brightgreen.svg)](https://github.com/wechaty/python-wechaty-plugin-contrib)

## History

### master

### v0.0.12 (Oct 2021)

The `python-wechaty-plugin-contrib` project has at least 9 plugins and 6 code examples.

It makes python-wechaty easier to use.

### v0.0.1 (Apr 2020)

The `python-wechaty-plugin-contrib` project was created. 

## Maintainers

- @wj-Mcat - [wj-Mcat](https://github.com/wj-Mcat), nlp researcher
- @huan - [Huan LI](https://github.com/huan) ([李卓桓](http://linkedin.com/in/zixia)), Tencent TVP of Chatbot

## Contributors
- @markoxu - [@markoxu](https://github.com/markoxu), Software Development Engineer at Intel Corporation.
- @lyleshaw - [@lyleshaw](https://github.com/lyleshaw), A HDU student, Author of [python-wechaty-puppet-itchat](https://github.com/wechaty/python-wechaty-puppet-itchat).

## Copyright & License

- Code & Docs © 2020 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
