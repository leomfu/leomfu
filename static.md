# Weyl Fu

做让日常更顺手的小东西。

## 开门亮灯

推开门，先把这盏黄铜灯点上。台上有三件正在修的东西：听得懂的视频，收得住的信，记得住的词。

![工作台上的黄铜灯、胶片轮、空白纸条、螺丝刀和扳手，下面是墨绿抽屉](assets/hero.jpg)

这一页的图片都是静止的。带回循环的版本在 [README.md](README.md)。GitHub 的 README 没有可靠的全局暂停，所以静止版单独放在这一页。

[weiliang.dev](https://weiliang.dev) 上写着「喜欢拍视频、聊科技，也喜欢做一些会发光的小东西」。那个站点用 Weiliang 这个名字。这里用 Weyl Fu。

## 工作台

这一页里的三张工作台都是静止的。

### WDub

给视频添一层听得懂的声音。实时翻译、双语字幕与 AI 配音，让外语视频更容易理解。

[![墨绿字幕放映盒，旁边是胶片轮和一盏黄铜灯](assets/wdub.jpg)](https://github.com/leomfu/wdub)

[W 声幕](https://github.com/leomfu/wdub) 是纯 JavaScript 的 Chrome 扩展。它给网页视频做实时翻译、双语字幕和 AI 配音，也支持本地视频、导入字幕、导出译文、视频总结和多角色声音。

开发和构建需要 Node.js 20 或更新版本。只把扩展加载进 Chrome 时不用装 Node。本地语音识别是可选项，用 Python，可以接 mlx-whisper、SenseVoice、FunASR 和 ffmpeg。翻译和语音可以接到外部服务。服务商不写进个人技术清单。

还没有声音克隆，也还没有把配音导出成 MP3 或视频。没有线上演示，也没有商店链接。

### gmail-classifier

把收件箱里的杂音，整理成今天真正要看的几件事。先看报告，再确认标签。

[![六格墨绿抽屉，里面是空白信封，旁边有黄铜灯和一封信](assets/gmail.jpg)](https://github.com/leomfu/gmail-classifier)

[邮件整理台](https://github.com/leomfu/gmail-classifier) 用 Python 和 uv。它通过 Gmail API 和 Google OAuth 读取邮件，用 TypeSafe 的 Jev 做分类，规则写在 YAML 里。Chrome 侧边栏连到本机服务。

先出报告，确认之后才写回标签，写回可以撤销。里面有钓鱼检测、退订分析和过滤器生成。Jev 不生成文本，只给出带概率的类型判断。发给 TypeSafe 的是主题和摘要，不是完整正文。退订分析只出清单，不会自动退订。`127.0.0.1` 上的侧边栏服务不是公开演示。

### claude-Anki

把每天学到的一点，变成明天还记得的一点。用 Markdown 记录，用 Anki 复习。

[![绿背线圈单词卡、空白词卡、铅笔和一盏黄铜灯](assets/learning.jpg)](https://github.com/leomfu/claude-Anki)

[claude-Anki](https://github.com/leomfu/claude-Anki) 是一份英语自学知识库，不是 Anki 插件，也不是可以安装的应用。笔记在 Obsidian 里，格式是 Markdown。Claude Code 整理卡片字段，AnkiConnect 建卡，复习在 Anki 里进行。卡片本体和制卡程序不在这个仓库。

内容有音标、新概念英语 1、咖啡店实用英语，还有一条雅思路线。6 到 6.5 是学习目标，不是已经拿到的成绩。

## 工具抽屉

这些名字只来自上面三个仓库的 README，分成两格。

写代码时用过的有 JavaScript、Python、Node.js、uv 和 YAML，还有 Chrome 扩展、Gmail API 和 Google OAuth。

用来把事情做完的有 Markdown、Obsidian、Anki、AnkiConnect 和 Claude Code。WDub 的可选本地识别还会用到 ffmpeg、mlx-whisper、SenseVoice 和 FunASR。

## 实验便签

铺子里已经在做的是这三件。

- 给视频做实时翻译、双语字幕和 AI 配音。
- 邮件先出报告，确认后再写标签，写回去的可以撤销。
- 用 Markdown 把当天学的记下来，用 Anki 留到明天。

下面这些还没做。

- 声音克隆。
- 把配音导出成 MP3 或视频。
- 自动退订。现在的退订分析只出清单。

## 制作记录

这是 2026-11-07 22:20（Asia/Shanghai）从 GitHub 公开提交核对的快照，不是会自己更新的图。来源是这三个公开仓库的提交列表。README 里的灯会循环，那不是正在写代码。这一页的灯是停着的。

完整的入口在 [github.com/leomfu](https://github.com/leomfu)。

- 2026-11-07 20:08，[wdub](https://github.com/leomfu/wdub/commit/ff9e4255780fefb5cde7a18c32e2fbb55e4277f1)，移除手机端代码（mobile/、extension/mobile/ 与两个打包脚本）。
- 2026-11-07 20:07，[wdub](https://github.com/leomfu/wdub/commit/0221f11df8d9c0e8ba6306a1f1c81c4fe6672656)，README 说明扩展在 Windows 和 Linux 上同样可用，只把本地识别标成 Apple 芯片限定。
- 2026-09-24 10:37，[gmail-classifier](https://github.com/leomfu/gmail-classifier/commit/223856ff7680fd9e4a9659ca51f9cba189bb286f)，发给 TypeSafe 之前遮掉验证码。
- 2026-08-31 10:52，[claude-Anki](https://github.com/leomfu/claude-Anki/commit/5c18d708cdb87ba230d41a8d0b276bb35826800c)，README 补上 Claude 制卡链路说明，并配上数据流图。

再核对一次的命令写在 [MAINTENANCE.md](MAINTENANCE.md)。这份主页不会自己去轮询。

## 门牌

信箱不放在这里。

- 网站 [weiliang.dev](https://weiliang.dev)
- GitHub [github.com/leomfu](https://github.com/leomfu)
