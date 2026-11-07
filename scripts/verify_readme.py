"""Check the profile page, then measure the rendered height."""

import hashlib
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

import build_robot

ROOT = Path(__file__).resolve().parents[1]
FACTS = (
    "做让日常更顺手的 AI 小工具，记录持续学习。",
    "给网页和本地视频做实时翻译、双语字幕和 AI 配音。",
    "先出报告，确认后再给 Gmail 写上标签。",
    "用 Markdown 记英语，再用 Anki 复习。这是笔记，不是插件。",
    "JavaScript · Python · Markdown · Obsidian · Anki",
    "https://github.com/leomfu/wdub",
    "https://github.com/leomfu/gmail-classifier",
    "https://github.com/leomfu/claude-Anki",
    "https://weiliang.dev",
    "https://github.com/leomfu",
)
FORBIDDEN = (
    "<script",
    "<style",
    "<img",
    "shields.io",
    "hello@",
    "example.com",
    "weylfu",
    "自动退订",
)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
failures = []


def check(ok, message):
    print(("ok  " if ok else "FAIL  ") + message)
    if not ok:
        failures.append(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rebuild_twice():
    build_robot.main()
    first = (sha256(ROOT / "assets/pixel-robot.gif"), sha256(ROOT / "assets/pixel-robot.png"))
    build_robot.main()
    second = (sha256(ROOT / "assets/pixel-robot.gif"), sha256(ROOT / "assets/pixel-robot.png"))
    check(first == second, "two builds write the same gif and png bytes")


def gif_pixels(path):
    image = Image.open(path)
    frames = []
    for index in range(image.n_frames):
        image.seek(index)
        frames.append(image.convert("RGBA"))
    return image, frames


def opaque_centroid(frame):
    total = sx = sy = 0
    pixels = frame.load()
    for y in range(frame.size[1]):
        for x in range(frame.size[0]):
            if pixels[x, y][3]:
                total += 1
                sx += x
                sy += y
    return (sx / total, sy / total) if total else (0, 0)


def block_scale(frame):
    pixels = frame.load()
    width, height = frame.size
    for scale in (8, 7, 6, 5, 4):
        if width % scale or height % scale:
            continue
        aligned = True
        for y in range(0, height, scale):
            for x in range(0, width, scale):
                color = pixels[x, y]
                for dy in range(scale):
                    for dx in range(scale):
                        if pixels[x + dx, y + dy] != color:
                            aligned = False
                            break
                    if not aligned:
                        break
                if not aligned:
                    break
            if not aligned:
                break
        if aligned:
            return scale
    return 1


def check_gif():
    path = ROOT / "assets/pixel-robot.gif"
    image, frames = gif_pixels(path)
    width, height = frames[0].size
    check(96 <= height <= 144, f"gif height {height}px is in 96-144")
    check(width <= 160, f"gif width {width}px stays clear of a banner")
    check(image.n_frames >= 6, f"gif has {image.n_frames} frames")
    check(image.info.get("loop") == 0, "gif loops")
    check(image.info.get("duration") == build_robot.FRAME_MS, "gif frame delay matches the builder")
    check(path.stat().st_size < 30_000, f"gif is {path.stat().st_size} bytes")
    steps = []
    for index, frame in enumerate(frames):
        nxt = frames[(index + 1) % len(frames)]
        changed = 0
        left = frame.load()
        right = nxt.load()
        for y in range(height):
            for x in range(width):
                if left[x, y] != right[x, y]:
                    changed += 1
        steps.append(changed)
    check(all(step > 0 for step in steps), f"consecutive frames differ {steps}")
    varying = 0
    first = frames[0].load()
    for y in range(height):
        for x in range(width):
            if any(frame.load()[x, y] != first[x, y] for frame in frames[1:]):
                varying += 1
    portion = varying / (width * height)
    check(portion < 0.2, f"moving pixels are {portion:.3f} of the canvas")
    centroids = [opaque_centroid(frame) for frame in frames]
    drift = max(
        abs(x - centroids[0][0]) + abs(y - centroids[0][1]) for x, y in centroids
    )
    check(drift < block_scale(frames[0]), f"body drift is {drift:.2f}px")
    scale = block_scale(frames[0])
    check(scale >= 4, f"pixels stay aligned at scale {scale}")
    colors = set()
    transparent = False
    for frame in frames:
        pixels = frame.load()
        for y in range(0, height, scale):
            for x in range(0, width, scale):
                red, green, blue, alpha = pixels[x, y]
                if alpha == 0:
                    transparent = True
                else:
                    colors.add((red, green, blue))
    check(transparent, "gif has transparent pixels")
    check(colors <= set(build_robot.COLORS.values()), f"gif uses only the sprite colors ({len(colors)})")
    still = Image.open(ROOT / "assets/pixel-robot.png").convert("RGBA")
    check(still.size == frames[0].size, f"png size {still.size} matches the gif")
    same = all(
        still.load()[x, y] == frames[0].load()[x, y]
        for y in range(height)
        for x in range(width)
    )
    check(same, "png matches the resting gif frame")


def inline(text):
    def link(match):
        label, href = match.group(1), match.group(2)
        return f'<a href="{href}">{label}</a>'

    return LINK_RE.sub(link, text)


def to_html(text):
    parts = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("## "):
            parts.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            parts.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("!["):
            alt, src = IMAGE_RE.match(line).groups()
            parts.append(f'<img alt="{alt}" src="file://{ROOT / src}">')
        else:
            parts.append(f"<p>{inline(line)}</p>")
    return "\n".join(parts)


def measure(text, width, padding):
    html = f"""<!doctype html><meta charset="utf-8">
<style>
html,body {{margin:0; width:{width}px}}
body {{box-sizing:border-box; width:{width}px; padding:{padding}px;
  font:16px/1.5 "WenQuanYi Micro Hei","Droid Sans Fallback",sans-serif}}
img {{display:block}}
h1 {{font-size:32px; margin:0 0 8px}}
h2 {{font-size:20px; margin:20px 0 8px}}
p {{margin:0 0 10px}}
</style>
<body>{to_html(text).replace("pixel-robot.gif", "pixel-robot.png")}</body>
<script>
const box = document.body;
const height = box.scrollHeight;
const scroll = box.scrollWidth;
const client = box.clientWidth;
const node = document.createElement("pre");
node.id = "measure";
node.style.position = "absolute";
node.textContent = [height, scroll, client].join(" ");
document.body.appendChild(node);
</script>
"""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        page = Path(directory) / "page.html"
        page.write_text(html, encoding="utf-8")
        dom = Path(directory) / "dom.html"
        handle = dom.open("w")
        process = subprocess.Popen(
            [
                "google-chrome",
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={directory}/profile",
                "--virtual-time-budget=2000",
                "--window-size=900,1400",
                "--dump-dom",
                page.as_uri(),
            ],
            stdout=handle,
            stderr=subprocess.DEVNULL,
        )
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        handle.close()
        output = dom.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r'id="measure"[^>]*>(\d+) (\d+) (\d+)', output)
    if not match:
        raise RuntimeError("chrome did not report a layout measurement")
    height, scroll_width, inner_width = (int(item) for item in match.groups())
    return height, scroll_width, inner_width


def check_pages():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    still = (ROOT / "static.md").read_text(encoding="utf-8")
    check(readme.startswith("!["), "README opens with the robot")
    check("# Weyl Fu\n" in readme and "# Weyl Fu\n" in still, "both pages title Weyl Fu")
    for fact in FACTS:
        check(fact in readme and fact in still, f"both pages say {fact}")
    for token in FORBIDDEN:
        blob = (readme + still).lower()
        check(token.lower() not in blob, f"pages omit {token}")
    readme_images = IMAGE_RE.findall(readme)
    still_images = IMAGE_RE.findall(still)
    check(readme_images == [("像素机器人，头顶是 W 形天线，胸口有一盏暖琥珀色的小灯", "assets/pixel-robot.gif")], "README has one gif")
    check(still_images == [("像素机器人，头顶是 W 形天线，胸口有一盏暖琥珀色的小灯", "assets/pixel-robot.png")], "static page has one png")
    check(".gif" not in still, "static page has no gif")
    for text, name in ((readme, "README.md"), (still, "static.md")):
        for label, target in LINK_RE.findall(text):
            if target.startswith("https://"):
                host = target.split("/")[2]
                check(host in {"github.com", "weiliang.dev"}, f"{name} link host {host}")
            else:
                check((ROOT / target).exists(), f"{name} relative target {target}")
    for width, padding, limit in ((800, 0, 900), (375, 16, 1600), (320, 16, 1600)):
        height, scroll_width, inner_width = measure(readme, width, padding)
        print(f"    layout {width}px height={height} scroll={scroll_width} inner={inner_width}")
        check(scroll_width <= inner_width, f"{width}px has no horizontal overflow")
        check(height <= limit, f"{width}px content height {height} is within {limit}")


def main():
    rebuild_twice()
    check_gif()
    check_pages()
    if failures:
        print(f"\n{len(failures)} failed")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
