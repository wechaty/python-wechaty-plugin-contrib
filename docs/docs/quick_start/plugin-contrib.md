---
title: "使用插件库"
sidebar_position: 1
---

# 插件库

社区插件库([python-wechaty-plugin-contrib](github.com/wechaty/python-wechaty-plugin-contrib))中包含大量常见插件，也推荐开发者优先使用仓库中内置的插件。

## Install

```shell
pip install wechaty-plugin-contrib
```

## Use Plugin

仓库中部分插件是没有相关文档，由于这些文档都是由社区开发者业余时间开发的，文档方面会有所欠缺，敬请谅解。

所以在文档中没有找到对应插件的前提下，欢迎前往[python-wechaty-plugin-contrib](https://github.com/wechaty/python-wechaty-plugin-contrib/tree/master/src/wechaty_plugin_contrib/contrib)源码中查看对应插件。

不同插件的用法基本上保持类似：

* 如果插件由对应的options类，则需要提前初始化
* 直接实例化插件并注入到插件当中

## 使用示例

在此展示如何使用插件库中的`DingDongPlugin`插件，方法也是非常简单。

```python
import asyncio
from wechaty import Wechaty
from wechaty_plugin_contrib import DingDongPlugin

async def main():
    bot = Wechaty()

    bot.use(DingDongPlugin())
    await bot.start()
    
asyncio.run(main())
```
