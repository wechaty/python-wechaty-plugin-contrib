---
title: "如何将插件发布成pypi包"
sidebar_label: 如何将插件发布成pypi包
sidebar_position: 2
---

在此还比较推荐各位开发者将插件发布成属于作者自己的[pypi](https://pypi.org/)包，每个包的更新迭代由开发者自行控制。

## 构建wechaty-plugin repo

在此，[@wj-Mcat](https://github.com/wj-Mcat)给大家提供了一个插件模板repo: [python-wechaty-plugin-template](https://github.com/wj-Mcat/python-wechaty-plugin-template)，各位开发者只需要按照以下步骤即可发布属于自己的pypi插件包。

### 创建pypi账号

要想发布pypi包，首先就需要创建对应的账号获取到token，然后通过[Github Action](https://docs.github.com/cn/actions)实现自动化包测试、发布等过程。

创建账号的方法大家可自行google，最后需要拿到`name`和`token`这两个信息。

### fork repo & rename repo

各位开发者可fork [python-wechaty-plugin-template](https://github.com/wj-Mcat/python-wechaty-plugin-template)仓库，在forke的过程中需要修改项目名称，比如插件名称为：foo，故repo的名称推荐为: `python-wechaty-plugin-foo`。

然后对repo中的相关文件稍作修改即可实现插件的自动化发布，在模板代码设置了多个占位符：

* <foo\>：插件名称（小写）
* <Foo\>: 插件名称（大写）
* <author\>: github_id
* <author_email\>: github email

以上占位符需要替换成作者自己的信息，推荐使用IDE进行全局占位符替换，从而最大程度上减小工作量

### 设置repo token

此时假设项目代码基本已完成，此时需要配置Github Action CD 的相关`name`和`token`，这也是在上个小节当中保存下来的。

* 修改`.github/workflows/pypi.yml` 的 `TWINE_USERNAME`字段
* 添加action secret token：`settings` -> `Secrets` -> `Actions` -> `New Repository secret`，并将键设置为`PYPI_TOKEN`。 

## 注册插件

开发者发布好自己的插件后推荐在社区注册对应的插件，这样其他开发者可看到相关插件（提高曝光度）。

如何注册：
* 在[python-wechaty-plugin-template](https://github.com/wj-Mcat/python-wechaty-plugin-template)仓库中的`docs/docs/plugins`目录下添加对应插件的介绍信息
* 在[python-wechaty-plugin-template](https://github.com/wj-Mcat/python-wechaty-plugin-template)仓库中的`docs/docs/plugins/index.md`的插件列表中添加插件简要描述信息。

## 总结

这种方式也是最为推荐的方式，也欢迎各位开发者能够参与到插件生态的建设当中来。
