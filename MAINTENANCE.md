# 维护

GitHub 个人主页只渲染默认分支 `main` 上的 `README.md`。合并之前，主页仍是原来的一行标题。本仓库不部署、不改公开性，也不跑定时任务。

## 文件

```
README.md
static.md
MAINTENANCE.md
requirements.txt
assets/source/hero-workshop.jpg
assets/source/wdub.jpg
assets/source/gmail.jpg
assets/source/learning.jpg
assets/hero.jpg
assets/hero.gif
assets/wdub.jpg
assets/gmail.jpg
assets/learning.jpg
assets/learning.gif
scripts/build_assets.py
scripts/verify_readme.py
```

`README.md` 是六段正文，带两处循环。`static.md` 是同一篇正文的静止版。`assets/source/` 里是四张原创无字插画。脚本从这四张裁剪，并生成灯火和灰尘。选中的整页概念图没有放进仓库，那张图里的地址和项目句子是占位。

## 重建

在仓库根目录执行。

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_assets.py
python3 scripts/verify_readme.py
```

`verify_readme.py` 退出码 0 时，会打印每个 GIF 的帧数、体积和稳定区域。当前锁定 Pillow 13.0.0 与 numpy 1.26.4。在这个版本上，连续跑两次 `build_assets.py` 会得到相同的 GIF 字节。

图片用相对路径 `assets/...`。分支预览和合并到 `main` 之后，都指向当前提交里的文件。不要改成带分支名的 raw 地址。

## 动效

`assets/hero.gif` 是工作台开灯：灯罩和墙边的光变亮再回到原画，有五粒灰尘。`assets/learning.gif` 只有单词卡旁的灯在呼吸。放映盒和邮件抽屉是 JPEG。

GitHub 的 README 没有可靠的全局暂停。不要写成系统已经遵守减少动态的设置。看静止画面打开 `static.md`。

插画保持暖纸内景。浅色和深色主题都不会把这层颜色改掉。正文是 Markdown，字色跟着 GitHub。

## 文案

`build_assets.py` 只把 JPEG 和 GIF 写进 `assets/`。它不打开 `README.md` 和 `static.md`，所以下次重建图片不会盖掉文案。两篇访客正文要一起改。

下面这些只留在维护说明里，不写进主页：

- weiliang.dev 上的名字是 Weiliang。主页用 Weyl Fu。
- 可接入的翻译和语音服务商不写成个人技术。
- 不把声音克隆、配音文件导出、自动退订写成将要做的功能。现在的边界是：配音用现成声音，留在浏览器里。退订分析只出清单。
- 6 到 6.5 是学习目标，不是已经拿到的成绩。
- 邮件侧边栏的 `127.0.0.1` 不是公开演示。
- GitHub 的 README 没有可靠的全局暂停。主页不会自己轮询提交。

## 制作记录

上面的四条提交是 2026-11-07 22:20（Asia/Shanghai）用公开 API 读到的快照。要再核对，手动执行下面的命令，然后自己改 `README.md` 和 `static.md`。不要把它们放进 GitHub Actions，也不要轮询。

```bash
gh api "repos/leomfu/wdub/commits?per_page=3" --jq '.[] | {sha:.sha[0:7], date:.commit.author.date, msg:.commit.message|split("\n")[0]}'
gh api "repos/leomfu/gmail-classifier/commits?per_page=3" --jq '.[] | {sha:.sha[0:7], date:.commit.author.date, msg:.commit.message|split("\n")[0]}'
gh api "repos/leomfu/claude-Anki/commits?per_page=3" --jq '.[] | {sha:.sha[0:7], date:.commit.author.date, msg:.commit.message|split("\n")[0]}'
```

日期写 Asia/Shanghai（UTC+8）。只读这三个公开仓库。不要访问私有仓库。
