---
title: "如何将代码贡献给社区"
sidebar_label: 如何将代码贡献给社区
sidebar_position: 1
---

如果开发者愿意，社区是非常欢迎接受来自于各大开发者的贡献，从而共建开源社区的生态，让使用[python-wechaty](http://github.com/wechaty/python-wechaty)能够使用到功能更加强大插件。

## 贡献方法

开源项目的贡献方式都是基于[Pull Request](https://docs.github.com/cn/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) （简称PR）），如果新手开发者还不知道什么是PR，建议好好去了解一下，这也是一个很好的机会去实践和学习。

在这里我推荐一些学习资料，大家可以尝试去发起一个PR：

* [About Pull Request](https://docs.github.com/cn/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
* [GitHub 的 Pull Request 是指什么意思？](https://www.zhihu.com/question/21682976)
* [如何创建Pull Request](https://www.cnblogs.com/zhangjianbin/p/7774073.html)

## 插件路径

相信想尝试将插件贡献给社区的小伙伴都或多或少的看过项目的代码，在此我将简要的介绍一下：

```shell
├── contrib
│   ├── auto_reply_plugin
│   ├── chat_history_plugin
│   ├── github_webhook_plugin
│   ├── gitlab_event_plugin
│   ├── health_checker_plugin
│   ├── paddlespeech_plugin
│   └── room_inviter
├── finders
└── matchers
```

以上为目前插件库中的文件夹路径`src/wechaty_plugin_contrib`，不同的目录有如下作用：

* contrib: 防止系统插件之处
* finders: 查找`Contact`, `Room` 目标对象
* matchers: 匹配`Contact`, `Room` 目标对象

## 插件格式

故插件的代码推荐使用以下格式来编写：

* 插件以文件夹的形式存放在`src/wechaty_plugin_contrib/contrib`目录下
* 能使用单个py文件表达的尽量用一个文件
* 编写插件功能描述文档：`docs/docs/plugins`
* 编写插件单元测试代码

## 总结

欢迎各位开发者将好玩的插件贡献到社区中来，成为`wechaty contributor`，期待大家的PR。
