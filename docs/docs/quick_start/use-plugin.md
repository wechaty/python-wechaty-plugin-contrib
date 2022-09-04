---
title: "使用插件"
sidebar_position: 1
author: wj-Mcat
---

# 使用插件

[python-wechaty-plugin-contrib](https://github.com/wechaty/python-wechaty-plugin-contrib)已经内置了常用的插件，这里将要介绍如何使用插件库中内置的插件。

## 使用内置插件

### DingDong 插件

这个是wechaty 机器人中的hello world。

```py showLineNumbers title=examples/ding-dong-bot.py {4,11}
import asyncio
from wechaty import Wechaty
from dotenv import load_dotenv
from wechaty_plugin_contrib import DingDongPlugin


async def main():
    load_dotenv()
    bot = Wechaty()

    bot.use(DingDongPlugin())

    await bot.start()
    

asyncio.run(main())
```

导入相关插件类之后，示例化一个即可通过`use`来使用此插件。

### Info Logger 插件

此插件主要是

```py title=examples/quick-start/info-logger-bot.py showLineNumbers {4,10}
import asyncio
from wechaty import Wechaty
from dotenv import load_dotenv
from wechaty_plugin_contrib import InfoLoggerPlugin

async def main():
    load_dotenv()
    bot = Wechaty()

    bot.use(InfoLoggerPlugin())

    await bot.start()

asyncio.run(main())
 
```

## 原理剖析

当插件被注册到插件内部后，机器人内部将会做以下事情：

* 将插件按照注册顺序插入到内部队列当中，一旦收到系统消息，将会按照顺序调用对应插件
* 插件将会把所有消息事件都冒泡到插件当中，如：`on_message`, `on_room_join`, `on_friendship`
* 扫描并注册blueprint中注册的http和websocket服务。
