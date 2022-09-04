---
title: 通过Http的方式发送消息
---

# 使用Http的方式发送消息

在社区中有很多小伙伴都想要一个功能：能否通过 restful api的方式来让机器发送消息。

在此章节当中将展示如何通过浏览器、[curl](https://curl.se/)或者[python requests](https://pypi.org/project/requests/)等方式让机器人主动发送消息。

## 实现方式

在最新版本[python-wechaty](https://pypi.org/project/wechaty/#history)中已经基于[Quart](https://pypi.org/project/quart/)内置了Http服务的能力。

而在插件中使用HTTP服务的方式非常简单，只需要在`blueprint`函数中注册路由函数即可。

:::tip
[Quart](https://pypi.org/project/quart/)是Flask的协程版本，作者也是Flask的原班人马，从简单易用的角度出发，故选用此框架。
:::

## 代码实践

```py title=examples/http-bpt.py showLineNumbers {8-12}
from __future__ import annotations

from quart import Quart
from wechaty import WechatyPlugin, Contact


class HttpBotPlugin(WechatyPlugin):
    async def blueprint(self, app: Quart) -> None:
        @app.route("/api/plugins/http_bot/say/<something>")
        async def say_something(something: str) -> None:
            contact: Contact = self.bot.Contact.load('<some-contact-id>')
            await contact.say(something)
```

核心代码，仅仅是以上高亮部分，核心还是路由注册的代码。

## 消息发送

通过以上代码即可暴露出`/api/plugins/http_bot/say/<something>`路由，可通过http get的方式来调用。

例如通过curl的方式来发送文本消息：

```shell
curl http://localhost:5000/api/plugins/http_bot/say/你在干嘛呢？
```
