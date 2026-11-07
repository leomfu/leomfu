"""Build the profile robot from the sprite rows in this file."""

import hashlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
FRAME_MS = 180

# One character is one source pixel. "." is transparent.
# Nearest-neighbor scale keeps every edge on the grid.
COLORS = {
    "K": (109, 117, 111),
    "B": (36, 48, 44),
    "F": (62, 74, 70),
    "G": (30, 77, 58),
    "D": (168, 107, 24),
    "A": (232, 163, 23),
    "L": (255, 224, 138),
    "E": (243, 236, 223),
    "#": (212, 162, 74),
    "S": (154, 160, 156),
}

# 16 columns. "*" is the chest lamp, "e" the eyes, "h" the hand that lifts.
# rows() adds a one-pixel margin so the antenna and the hand are not flush to the edge.
BASE = (
    "...##......##...",
    "...##......##...",
    "...##..##..##...",
    "...####..####...",
    ".....##..##.....",
    "................",
    "....KKKKKKKK....",
    "...KKFFFFFFKK...",
    "...KKFEeFEeKK...",
    "...KKFEeFEeKK...",
    "...KKFFFFFFKK...",
    "....KKKKKKKK....",
    "......KKKK......",
    "...KKKKKKKKKK...",
    "..KBBBBBBBBBBK..",
    "hhKGGG**GGGGKS..",
    "..KGGG**GGGGK...",
    "..KBBBBBBBBBBK..",
    "...KKKKKKKKKK...",
    "....KKK..KKK....",
    "...KKKK..KKKK...",
)


def rows():
    grid = [list("." + row) for row in BASE]
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise SystemExit("sprite rows are not rectangular")
    grid.insert(0, ["."] * width)
    return grid


def locate(grid, char):
    return [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == char]


def frame(lamp, blink=False, wave=False):
    grid = rows()
    for x, y in locate(grid, "*"):
        grid[y][x] = lamp
    for x, y in locate(grid, "e"):
        grid[y][x] = "F" if blink else "E"
    hands = locate(grid, "h")
    for x, y in hands:
        grid[y][x] = "."
        grid[y - (1 if wave else 0)][x] = "S"
    return grid


def frames():
    # Lamp eases bright and dim. The blink and the wave each last one step.
    return (
        frame("D"),
        frame("A"),
        frame("L"),
        frame("A", blink=True),
        frame("D"),
        frame("A", wave=True),
        frame("L", wave=True),
        frame("A"),
    )


def scale_for(height):
    choices = [scale for scale in range(4, 9) if 96 <= height * scale <= 144]
    if not choices:
        raise SystemExit(f"no integer scale puts {height}px in the 96-144 range")
    return max(choices)


def to_image(grid):
    height = len(grid)
    width = len(grid[0])
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = image.load()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == ".":
                continue
            red, green, blue = COLORS[char]
            pixels[x, y] = (red, green, blue, 255)
    scale = scale_for(height)
    return image.resize((width * scale, height * scale), Image.Resampling.NEAREST)


def save_gif(images, path):
    palette = Image.new("P", (1, 1))
    flat = [0, 0, 0]
    for red, green, blue in COLORS.values():
        flat.extend((red, green, blue))
    flat.extend([0, 0, 0] * (256 - len(flat) // 3))
    palette.putpalette(flat[: 256 * 3])
    indexed = []
    for image in images:
        raw = image.convert("RGBA")
        frame = Image.new("P", raw.size)
        frame.putpalette(palette.getpalette())
        src = raw.load()
        dst = frame.load()
        color_index = {value: index + 1 for index, value in enumerate(COLORS.values())}
        for y in range(raw.size[1]):
            for x in range(raw.size[0]):
                red, green, blue, alpha = src[x, y]
                dst[x, y] = 0 if alpha == 0 else color_index[(red, green, blue)]
        indexed.append(frame)
    indexed[0].save(
        path,
        save_all=True,
        append_images=indexed[1:],
        duration=FRAME_MS,
        loop=0,
        disposal=2,
        transparency=0,
        optimize=False,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    images = [to_image(grid) for grid in frames()]
    images[0].save(OUT / "pixel-robot.png")
    save_gif(images, OUT / "pixel-robot.gif")
    digest = hashlib.sha256((OUT / "pixel-robot.gif").read_bytes()).hexdigest()[:12]
    print(f"pixel-robot.gif {images[0].size} frames={len(images)} sha={digest}")


if __name__ == "__main__":
    main()
