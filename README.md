# python-wechaty-plugin-contrib [![Python Wechaty Plugin Contrib](https://img.shields.io/badge/python--wechaty--contrib-contrib-green)](https://github.com/wechaty/python-wechaty-plugin-contrib)

 [![pypi Version](https://img.shields.io/badge/pypi-0.0.1-brightgreen)](https://www.npmjs.com/package/wechaty-plugin-contrib)
 [![pypi](https://img.shields.io/badge/py3.7-pass-brightgreen)](https://github.com/wechaty/python-wechaty-plugin-contrib)

Python Wechaty Plugin Contrib Package for the Community

![Wechaty Plugin](docs/images/plugin.png)

> Image Credit: [What is Plugin](https://www.computerhope.com/jargon/p/plugin.htm)

[![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://github.com/Wechaty/wechaty)
[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-python-brightgreen)](https://www.python.org/)

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


### 1 DingDong

- Description: Reply `dong` if bot receives a `ding` message.
- Author: [@wj-Mcat](https://github.com/wj-Mcat)

```python
from wechaty_plugin_contrib import DingDongPlugin

bot.use(DingDongPlugin())
```


## Python Wechaty Plugin Directory

The Wechaty Plugin Contrib will only accept simple plugins which does not dependence very heavy NPM modules, and the SLOC (Source Line Of Code) is no more than 100.

There are many great Wechaty Plugins can not be included in the contrib because they are too powerful. They will be published as a pypi package by itself.

We are listing those powerful Wechaty Plugins outside the contrib as in the following list, and you are welcome to add your plugin below if you have published any!

[![Wechaty Plugin Contrib](https://img.shields.io/badge/Wechaty%20Plugin-Directory-brightgreen.svg)](https://github.com/wechaty/python-wechaty-plugin-contrib)

## History

### master


### v0.0.1 (Apr 2020)

The `python-wechaty-plugin-contrib` project was created. 

## Maintainers

- @wj-Mcat - [wj-Mcat](https://github.com/wj-Mcat), nlp researcher
- @huan - [Huan LI](https://github.com/huan) ([李卓桓](http://linkedin.com/in/zixia)), Tencent TVP of Chatbot

## Copyright & License

- Code & Docs © 2020 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
