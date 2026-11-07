"""Check the profile README, the still copy, and the generated images."""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = (
    "## 开门亮灯",
    "## 工作台",
    "## 工具抽屉",
    "## 实验便签",
    "## 制作记录",
    "## 门牌",
)
FACTS = (
    "做让日常更顺手的小东西。",
    "给视频添一层听得懂的声音。",
    "把收件箱里的杂音，整理成今天真正要看的几件事。",
    "把每天学到的一点，变成明天还记得的一点。",
    "https://github.com/leomfu/wdub",
    "https://github.com/leomfu/gmail-classifier",
    "https://github.com/leomfu/claude-Anki",
    "https://weiliang.dev",
    "https://github.com/leomfu",
    "不是已经拿到的成绩",
    "不会自动退订",
    "声音克隆",
    "127.0.0.1",
    "Asia/Shanghai",
    "2026-11-07 22:20",
    "ff9e4255780fefb5cde7a18c32e2fbb55e4277f1",
    "223856ff7680fd9e4a9659ca51f9cba189bb286f",
    "5c18d708cdb87ba230d41a8d0b276bb35826800c",
    "没有可靠的全局暂停",
)
FORBIDDEN = (
    "weylfu",
    "hello@",
    "example.com",
    "xiaohongshu",
    "xhslink",
    "shields.io",
    "github-readme-stats",
    "komarev",
    "streak-stats",
    "prefers-reduced-motion",
    "全栈",
    "260张",
    "260 张",
    "<script",
    "<style",
    "<iframe",
    "<img",
    "javascript:",
)
ALLOWED_HOSTS = {"github.com", "weiliang.dev"}
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
failures = []


def check(ok, message):
    if ok:
        print(f"ok  {message}")
    else:
        failures.append(message)
        print(f"FAIL  {message}")


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def gif_report(name, stable_box):
    path = ROOT / "assets" / name
    image = Image.open(path)
    frames = []
    for index in range(image.n_frames):
        image.seek(index)
        frames.append(np.asarray(image.convert("RGB")))
    count = len(frames)
    check(count >= 8, f"{name} has {count} frames")
    check(image.info.get("loop") == 0, f"{name} loops forever")
    check(image.info.get("duration") == 220, f"{name} frame duration is 220 ms")
    unique = len({frame.tobytes() for frame in frames})
    check(unique >= 6, f"{name} has {unique} distinct frames")
    steps = [float(np.abs(frames[i].astype(np.int16) - frames[(i + 1) % count].astype(np.int16)).mean()) for i in range(count)]
    check(all(step > 0 for step in steps), f"{name} consecutive frames all differ")
    ratio = max(steps) / sorted(steps)[count // 2]
    check(ratio < 2, f"{name} loop step ratio {ratio:.2f}")
    x0, y0, x1, y1 = stable_box
    stable = max(int(np.abs(frames[i][y0:y1, x0:x1].astype(np.int16) - frames[0][y0:y1, x0:x1].astype(np.int16)).max()) for i in range(count))
    check(stable == 0, f"{name} stable region max delta {stable}")
    identical = np.ones(frames[0].shape[:2], dtype=bool)
    for frame in frames[1:]:
        identical &= np.all(frame == frames[0], axis=2)
    fraction = float(identical.mean())
    check(fraction >= 0.75, f"{name} unchanged pixels {fraction:.2f}")
    peak = int(np.abs(frames[count // 2].astype(np.int16) - frames[0].astype(np.int16)).max())
    check(peak >= 30, f"{name} peak frame delta {peak}")
    size = path.stat().st_size
    check(size < 800_000, f"{name} is {size} bytes")
    print(f"    {name} {frames[0].shape[1]}x{frames[0].shape[0]} bytes={size} unchanged={fraction:.2f}")


def main():
    readme = read("README.md")
    still = read("static.md")
    maintenance = read("MAINTENANCE.md")
    for heading in HEADINGS:
        check(heading in readme, f"README has {heading}")
        check(heading in still, f"static.md has {heading}")
    check(readme.startswith("# Weyl Fu\n"), "README title is Weyl Fu")
    for fact in FACTS:
        check(fact in readme, f"README has {fact}")
        check(fact in still, f"static.md has {fact}")
    blob = "\n".join((readme, still, maintenance))
    lowered = blob.lower()
    for token in FORBIDDEN:
        check(token.lower() not in lowered, f"no {token}")
    check("assets/hero.gif" in readme and "assets/learning.gif" in readme, "README uses the two loops")
    check(".gif" not in still, "static.md has no GIF")
    check("python3 scripts/build_assets.py" in maintenance, "maintenance has the build command")
    check("python3 scripts/verify_readme.py" in maintenance, "maintenance has the verify command")
    for name in ("README.md", "static.md"):
        text = readme if name == "README.md" else still
        for target in IMAGE_RE.findall(text):
            check(not target.startswith(("http://", "https://")), f"{name} image is relative: {target}")
            check((ROOT / target).is_file(), f"{name} image exists: {target}")
        for target in LINK_RE.findall(text):
            if target.startswith("http://") or target.startswith("https://"):
                host = target.split("/")[2]
                check(host in ALLOWED_HOSTS, f"{name} link host {host}")
            else:
                check((ROOT / target).exists(), f"{name} relative link exists: {target}")
    for name, box in (
        ("hero.gif", (760, 0, 960, 362)),
        ("learning.gif", (0, 0, 700, 502)),
    ):
        gif_report(name, box)
    for name in ("hero.jpg", "wdub.jpg", "gmail.jpg", "learning.jpg"):
        path = ROOT / "assets" / name
        with Image.open(path) as image:
            check(image.format == "JPEG", f"{name} is JPEG {image.size}")
            check(image.size[0] == 960, f"{name} width is 960")
        check(path.stat().st_size < 250_000, f"{name} is {path.stat().st_size} bytes")
    needles = (
        "ghp_" + "[A-Za-z0-9]{20,}",
        "github_" + "pat_",
        "AK" + "IA[0-9A-Z]{16}",
        "BE" + "GIN [A-Z ]*PRIVATE KEY",
        "TYPE" + "SAFE_API_KEY=",
    )
    secret = re.compile("(" + "|".join(needles) + ")")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in {".jpg", ".gif", ".png"}:
            continue
        check(secret.search(path.read_text(encoding="utf-8", errors="ignore")) is None, f"no secret in {path.name}")
    if failures:
        print(f"\n{len(failures)} failed")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
