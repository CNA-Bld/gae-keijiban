# GAE-Keijiban

## English Version

GAE-Keijiban is a simple keijiban (揭示板 in Chinese/掲示板 in Japanese) engine running on Google App Engine. It is basically a anonymous forum where all users are identified by a random string assigned to them when they first access the website, so there is no way to know the real identity of users. Futhermore, the ID will change once the cookies is cleared, making it easy for users to change identity. A feature for users to identify themselves even if they have no fixed ID (2ch trip) is in the future feature list.

Some famous online forums having similar systems are:

* [4chan](http://www.4chan.org/) (English)
* [2chan](http://www.2chan.net/) (Japanese)
* [Komica](http://komica.org) (Traditional Chinese)
* [AC 匿名版](http://h.acfun.tv) (Simplified Chinese)

### Introduction
GAE-Keijiban is inspired by [Pixmicat!](http://pixmicat.openfoundry.org/) by Pixmicat! Development Team, [GazouBBS](http://php.s3.to/) by レッツPHP! and [futaba.php](http://www.2chan.net) by 双葉ちゃん.

The design of GAE-Keijiban's default theme is almost identical to Pixmicat! but the implementation is completely different from any of the three softwares above. As we run on different platform, there is currently no plan of supporting mods of Pixmicat! (although we look similar).

This software is still in its very early stage so it is VERY unstable. Also, the storage model is not finalized, meaning that it may change at any time without guarantee of backward compatibility.

Currently almost all site settings have to be done using GAE's app console. A UI for admin will be developed soon.

### Demo
GAE-Keijiban provides a [Demo Site](http://gae-keijiban.appspot.com) running the most recent devel version.

### Installation
After downloading the source, change `application` in `app.yaml` to your app id in Google App Engine.

    application: yourappname

After configuration, update your app using

    python appcfg.py update yourappname

Great. Now it is working, you may visit it at: http://yourappname.appspot.com

## 中文版

GAE-Keijiban 是一个 GAE 上简单的揭示板系统。这是一个自动为用户分配随机 ID 的匿名揭示板。清除 Cookies（黑话：饼干）即可重新做人。将来会提供 2ch trip 的功能。

一些常见的类似架构的网站有

* [4chan](http://www.4chan.org/) (英语)
* [2chan](http://www.2chan.net/) (日语)
* [Komica](http://komica.org) (正体中文)
* [AC 匿名版](http://h.acfun.tv) (简体中文)

### 简介
GAE-Keijiban 受到了 [Pixmicat!](http://pixmicat.openfoundry.org/) by Pixmicat! Development Team, [GazouBBS](http://php.s3.to/) by レッツPHP! 和 [futaba.php](http://www.2chan.net) by 双葉ちゃん 的启发。

GAE-Keijiban 的默认主题长得和 Pixmicat! 一样一样的但是实现完全不同。虽然我们长一样但架构没啥关系，所以暂时没有支持它的插件的计划。

这个程序依旧处在非常初期的开发阶段，极其不稳定。存储结构还没有被完全确定，时刻都可能放弃向后兼容性。

目前没有管理员用 UI，管理员几乎所有的操作都需要通过 GAE Console 完成。不过一旦稍微稳定一点就会优先开发管理员 UI。

### Demo
GAE-Keijiban 有一个 [Demo Site](http://gae-keijiban.appspot.com)。运行的是最新开发版。啊对了它完美支持 Unicode。另外目前切换语言（版面列表下面）只能在主页切换，否则就会报错，还没发现原因，看日志怀疑是页面渲染引擎的 Bug，正在寻找 Workaround。

### 安装
下载了源码后，打开`app.yaml`文件，修改`application`字段为你的GAE应用的名称：

    application: yourappname

配置完了，上传：

    python appcfg.py update yourappname

然后就可以访问：http://yourappname.appspot.com

## License
Copyright 2014 CNA_Bld @ SSHZ.ORG.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This software is a derivative work of NancyWiki by CoderZh.com licensed under Apache License, Version 2.0.
