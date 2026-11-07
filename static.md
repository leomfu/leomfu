# Weyl Fu

做让日常更顺手的小东西。

## 开门亮灯

推开门，先把这盏黄铜灯点上。台上有三件正在修的东西：听得懂的视频，收得住的信，记得住的词。

![工作台上的黄铜灯、胶片轮、空白纸条、螺丝刀和扳手，下面是墨绿抽屉](assets/hero.jpg)

这一页的画面是停着的。循环版在 [README.md](README.md)。

[weiliang.dev](https://weiliang.dev) 上写着「喜欢拍视频、聊科技，也喜欢做一些会发光的小东西」。

## 工作台

### WDub

给视频添一层听得懂的声音。实时翻译、双语字幕与 AI 配音，让外语视频更容易理解。

[![墨绿字幕放映盒，旁边是胶片轮和一盏黄铜灯](assets/wdub.jpg)](https://github.com/leomfu/wdub)

[W 声幕](https://github.com/leomfu/wdub) 放在 Chrome 里。网页视频和本地视频都能翻译，挂上双语字幕，再用现成的声音配出来。也可以导入字幕、导出译文、做个视频总结。

### gmail-classifier

把收件箱里的杂音，整理成今天真正要看的几件事。先看报告，再确认标签。

[![六格墨绿抽屉，里面是空白信封，旁边有黄铜灯和一封信](assets/gmail.jpg)](https://github.com/leomfu/gmail-classifier)

[邮件整理台](https://github.com/leomfu/gmail-classifier) 先把今天该看的理出来。确认之后才写标签，写上的可以撤销。

### claude-Anki

把每天学到的一点，变成明天还记得的一点。用 Markdown 记录，用 Anki 复习。

[![绿背线圈单词卡、空白词卡、铅笔和一盏黄铜灯](assets/learning.jpg)](https://github.com/leomfu/claude-Anki)

[claude-Anki](https://github.com/leomfu/claude-Anki) 是一份英语笔记，不是要安装的插件。音标、新概念英语 1、咖啡店实用英语，沿着一条雅思路线往下记。6 到 6.5 是学习目标。

## 工具抽屉

JavaScript 写扩展，Python 写邮件整理。邮件这边用 uv、YAML、Gmail API 和 Google OAuth。分类用 TypeSafe 的 Jev，它看的是主题和摘要。WDub 的开发和构建用 Node.js 20 或更新版本。本机识别语音时会用到 ffmpeg、mlx-whisper、SenseVoice 和 FunASR。

学习笔记是 Markdown，放在 Obsidian 里。Claude Code 整理卡片字段，AnkiConnect 把卡片放进 Anki。

## 实验便签

铺子里现在做着这三件。

- 视频能实时翻译、看双语字幕、听 AI 配音。声音是现成的，配音在浏览器里听。
- 邮件先出报告，确认后再写标签，写上的可以撤销。退订会整理成一份清单。
- 英语写在 Markdown 笔记里，再用 Anki 复习。卡片不在这个笔记仓库里。

## 制作记录

2026-11-07 22:20（Asia/Shanghai）。这几笔来自三个公开仓库的提交。入口在 [github.com/leomfu](https://github.com/leomfu)。

- 2026-11-07 20:08，[wdub](https://github.com/leomfu/wdub/commit/ff9e4255780fefb5cde7a18c32e2fbb55e4277f1)，移除手机端代码（mobile/、extension/mobile/ 与两个打包脚本）。
- 2026-11-07 20:07，[wdub](https://github.com/leomfu/wdub/commit/0221f11df8d9c0e8ba6306a1f1c81c4fe6672656)，README 说明扩展在 Windows 和 Linux 上同样可用，只把本地识别标成 Apple 芯片限定。
- 2026-09-24 10:37，[gmail-classifier](https://github.com/leomfu/gmail-classifier/commit/223856ff7680fd9e4a9659ca51f9cba189bb286f)，发给 TypeSafe 之前遮掉验证码。
- 2026-08-31 10:52，[claude-Anki](https://github.com/leomfu/claude-Anki/commit/5c18d708cdb87ba230d41a8d0b276bb35826800c)，README 补上 Claude 制卡链路说明，并配上数据流图。

## 门牌

- 网站 [weiliang.dev](https://weiliang.dev)
- GitHub [github.com/leomfu](https://github.com/leomfu)
