"""Rebuild cropped stills and looping GIFs from assets/source."""

import math
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source"
OUT = ROOT / "assets"
TARGET_W = 960
FRAMES = 12
DURATION_MS = 220

# Crops are (left, top, right, bottom) on the 1280x720 source paintings.
HERO = {
    "source": "hero-workshop.jpg",
    "still": "hero.jpg",
    "gif": "hero.gif",
    "crop": (0, 230, 1280, 712),
    "lamp": (268, 408, 86, 68),
    "halo": (300, 360, 190, 150),
    "pool": (300, 548, 180, 32),
    "dust": ((390, 270), (460, 330), (340, 240), (510, 390), (430, 450)),
}
LEARN = {
    "source": "learning.jpg",
    "still": "learning.jpg",
    "gif": "learning.gif",
    "crop": (80, 72, 1220, 668),
    "lamp": (1048, 318, 78, 70),
    "halo": (1048, 300, 100, 90),
    "pool": (1040, 478, 120, 22),
    "dust": (),
}
STILLS = (
    {"source": "wdub.jpg", "still": "wdub.jpg", "crop": (150, 96, 1160, 640)},
    {"source": "gmail.jpg", "still": "gmail.jpg", "crop": (145, 48, 1165, 672)},
)


def crop_resize(path, crop):
    image = Image.open(path).convert("RGB")
    left, top, right, bottom = crop
    cropped = image.crop((left, top, right, bottom))
    scale = TARGET_W / cropped.width
    height = int(round(cropped.height * scale))
    if height % 2:
        height += 1
    resized = cropped.resize((TARGET_W, height), Image.Resampling.LANCZOS)
    return np.asarray(resized).astype(np.float32), scale


def place(x, y, crop, scale):
    return (x - crop[0]) * scale, (y - crop[1]) * scale


def ellipse(h, w, cx, cy, rx, ry):
    yy, xx = np.ogrid[:h, :w]
    field = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    mask = np.clip(1.0 - field, 0.0, 1.0)
    mask *= mask
    mask[field >= 1] = 0
    return mask


def apply_light(base, spec, crop, scale, amount):
    if amount <= 0:
        return base
    height, width = base.shape[:2]
    lx, ly = place(spec["lamp"][0], spec["lamp"][1], crop, scale)
    lamp = ellipse(height, width, lx, ly, spec["lamp"][2] * scale, spec["lamp"][3] * scale)
    hx, hy = place(spec["halo"][0], spec["halo"][1], crop, scale)
    halo = ellipse(height, width, hx, hy, spec["halo"][2] * scale, spec["halo"][3] * scale)
    px, py = place(spec["pool"][0], spec["pool"][1], crop, scale)
    pool = ellipse(height, width, px, py, spec["pool"][2] * scale, spec["pool"][3] * scale)
    out = base.copy()
    luma = out.mean(axis=2, keepdims=True) / 255.0
    # The shade is already near white, so the breath lives on the wall and the wood.
    ink_safe = np.clip((luma - 0.5) / 0.35, 0, 1)
    out *= 1 + lamp[..., None] * amount * 0.16 * ink_safe
    ring = np.clip(halo - lamp, 0, 1)
    out += ring[..., None] * amount * np.array([26.0, 12.0, -4.0])
    out += pool[..., None] * amount * np.array([16.0, 7.0, 0.0])
    return np.clip(out, 0, 255)


def apply_dust(base, spec, crop, scale, phase):
    if not spec["dust"]:
        return base
    out = base.copy()
    height, width = out.shape[:2]
    color = np.array([168.0, 132.0, 86.0], dtype=np.float32)
    for index, (sx, sy) in enumerate(spec["dust"]):
        cx, cy = place(sx, sy, crop, scale)
        cx += math.sin(phase + index * 1.2) * 11
        cy += math.cos(phase * 0.85 + index) * 5
        alpha = 0.36 + 0.22 * math.sin(phase + index * 0.7)
        radius = 2.3 + (index % 3) * 0.4
        reach = int(math.ceil(radius * 3))
        x0 = max(0, int(math.floor(cx)) - reach)
        y0 = max(0, int(math.floor(cy)) - reach)
        x1 = min(width, int(math.floor(cx)) + reach + 1)
        y1 = min(height, int(math.floor(cy)) + reach + 1)
        if x0 >= x1 or y0 >= y1:
            continue
        yy, xx = np.ogrid[y0:y1, x0:x1]
        blob = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * radius * radius)) * alpha
        blob[blob < 0.02] = 0
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - blob[..., None]) + color * blob[..., None]
    return np.clip(out, 0, 255)


def frames_for(base, spec, crop, scale):
    frames = []
    for index in range(FRAMES):
        phase = 2 * math.pi * index / FRAMES
        breath = (1 - math.cos(phase)) / 2
        image = apply_light(base, spec, crop, scale, breath)
        image = apply_dust(image, spec, crop, scale, phase)
        frames.append(Image.fromarray(image.round().astype(np.uint8), "RGB"))
    return frames


def shared_palette(frames):
    strip = Image.fromarray(np.concatenate([np.asarray(frame) for frame in frames], axis=0), "RGB")
    return strip.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def save_gif(frames, path):
    palette = shared_palette(frames)
    quantized = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )


def save_still(array, path):
    Image.fromarray(array.round().astype(np.uint8), "RGB").save(path, quality=90, optimize=True)


def build_animated(spec):
    base, scale = crop_resize(SOURCE / spec["source"], spec["crop"])
    save_still(base, OUT / spec["still"])
    frames = frames_for(base, spec, spec["crop"], scale)
    save_gif(frames, OUT / spec["gif"])
    print(f"{spec['gif']} {frames[0].size} frames={len(frames)} bytes={ (OUT / spec['gif']).stat().st_size }")


def build_still(spec):
    base, _scale = crop_resize(SOURCE / spec["source"], spec["crop"])
    save_still(base, OUT / spec["still"])
    print(f"{spec['still']} {base.shape[1]}x{base.shape[0]} bytes={(OUT / spec['still']).stat().st_size}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_animated(HERO)
    build_animated(LEARN)
    for spec in STILLS:
        build_still(spec)


if __name__ == "__main__":
    main()
