---
title: "自定义插件"
sidebar_position: 2
---

# 自定义插件

## 插件介绍

export const Green = ({children}) => (
  <span
    style={{
      backgroundColor: "#25c2a0",
      borderRadius: '2px',
      color: '#fff',
      padding: '0.2rem',
    }}>
    {children}
  </span>
)


export const Blue = ({children}) => (
  <span
    style={{
      backgroundColor: "#eeeeee",
      borderRadius: '2px',
      color: '#000',
      padding: '0.2rem',
      fontWeight: 500
    }}>
    {children}
  </span>
)

export const Gray = ({children}) => (
  <span
    style={{
      backgroundColor: "#eeeeee",
      borderRadius: '2px',
      color: '#000',
      padding: '0.2rem',
      fontWeight: 500
    }}>
    {children}
  </span>
)

python-wechaty 支持自定义插件，将<Gray>部分业务功能封装到一个插件</Gray>当中，实现<Gray>业务上的隔离性</Gray>，比如：自动通过好友申请这个功能封装成一个插件中，通过关键字拉人入群的功能封装成一个插件等，这样做有如下好处：

* 功能模块化，代码更简洁；
* 插件化之后，扩展性更高；
* 插件内置[scheduler](https://apscheduler.readthedocs.io/)、[web server](https://github.com/pallets/quart)等，可玩性更高；
* 插件适合分享，也适合共享到社区中来；
* ...

以上是使用插件系统的种种优点，也是推荐给位开发者能够基于插件系统开发出自己的业务机器人，主要在于机器人能够实现所有Wechaty类中的功能，比如所有消息事件、主动发送消息等，同时还可通过[Quart](https://github.com/pallets/quart)启动Web Service，支持Http和WebSocket协议，可在不同的插件当中开发出不同的功能。

以下我将介绍一些简单的插件，并如何自定义插件。

## DingDongPlugin 示例

```py 

from wechaty import WechatyPlugin, Message

class DingDongPlugin(WechatyPlugin):
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            await msg.say('dong')
```

在此插件中实现了一个最简单的功能：收到一个`ding`，回复一个`dong`；这个就是机器人开发中的`hello world`，说明机器人能够正常运行，实现接受消息和发送消息这个流程。

:::tip 关键点
在这个插件中值得注意的是：

* 重写`on_message`方法，并可通过此方法接受到群内发送的所有消息。
* 在插件中可实现消息的自定义回复
:::

## 使用插件

python-wechaty中有仓库内置的插件，详细可见：[插件列表](/python-wechaty-plugin-contrib/plugins)，同时也是支持自定义插件的，使用方法就是：

* 导入相关插件类，有时候需要对应options来初始化插件
* 实例化插件
* 调用Wechaty实例的`use`方法来注册插件


```py showLineNumbers {4}
async def main():
    bot = Wechaty()
    plugin = DingDongPlugin()
    bot.use(plugin)
    await bot.start()
```

## 使用配置项

在python-wechaty插件中可通过`setting`属性来获取已经修改setting配置项，而加载和保存修改的这个过程插件内部已经做了完整的实现，开发者不需要做任何额外的开发工作，使用方法是如下所示：

```py showLineNumbers {6}
from wechaty import WechatyPlugin, Message

class DingDongPlugin(WechatyPlugin):
    async def on_message(self, msg: Message) -> None:
        if msg.text() == "ding":
            dong = self.setting.get("ding", "dong")
            await msg.say(word)
```

:::info 配置项
在以上的代码中，通过`self.setting`可获取到插件配置项，为字典数据类型。

开发者也可在本地直接修改插件配置文件，配置文件路径默认为：`.wechaty/{PluginName}/setting.json`路径。
:::

此外，开发者使用最新版本的wechaty可直接通过wechaty-ui实现在线插件配置，非常的方便。

