# 维护

`python3 scripts/build_robot.py` 用本文件旁边的像素表生成 `assets/pixel-robot.gif` 和 `assets/pixel-robot.png`。脚本不改这两篇正文。

`python3 scripts/verify_readme.py` 会再生成两次，并检查帧、尺寸、链接和页面高度。

连续两次生成的 GIF 和 PNG 字节相同。GitHub 的 README 不能全局暂停，所以静止画面单独放在 `static.md`。

图片用相对路径。分支预览和合并到 `main` 之后，都指向当前提交里的文件。
