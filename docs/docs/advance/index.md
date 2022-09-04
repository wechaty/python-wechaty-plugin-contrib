---
title: "进阶教程"
sidebar_label: 进阶教程
sidebar_position: 7
---

python-wechaty的插件系统初衷就拆分不同的业务到不同的插件当中，从而实现业务代码的隔离性，毕竟在wechaty当中常见的业务逻辑都是基于不同事件，如`on_message`，`on_room_join`等事件，而同一个事件下往往包含多种不同的功能，所有此时如何拆分不同的功能就成为关键。此时插件系统就是一个很好的选择。

[wechaty社区](https://github.com/wechaty/python-wechaty-plugin-contrib)包含多种插件，开发者可通过多种方式来使用和贡献自己的插件，在此将介绍三种如何贡献插件给其他开发者使用：

1. 将代码贡献给社区：[python-wechaty-plugin-contrib](github.com/wechaty/python-wechaty-plugin-contrib)，详细可见[如何将代码贡献给社区](./contribute-to-community.md)
2. 将自己的插件发布成[pypi](pypi.org/)包，详细可见[如何将插件发布成pypi包](./deploy-to-pypi.md)
3. 将自己的插件代码放在github中，其他开发者可直接clone使用，详细可见[如何在github上分享插件](share-as-repo.md)


