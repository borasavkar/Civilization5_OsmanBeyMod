#!/usr/bin/env python3
"""
Builds every image of the mod from the public-domain Osman Gazi miniature (tools/art_src/osman.jpg):
  * diplomacy screen (1600x900) and Dawn of Man loading screen (1024x768)
  * leader icon atlas (round portrait), civilization icon atlas and alpha symbol atlas
  * preview PNGs in docs/
The civilization symbol is a stylised tree, after the tree of Osman's dream.
Requires Pillow and ImageMagick ("magick" on PATH).
"""
import math
import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
ART = os.path.join(ROOT, "Osman Bey", "Art")
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(TOOLS, "art_src", "osman.jpg")

FG = (239, 202, 85)        # gold
BG = (150, 16, 22)         # crimson
GOLD = (212, 175, 90)
FACE = (0.40, 0.31, 0.50)  # centre x, centre y, square size (fractions of the source image)
PORTRAIT_FOCUS = 0.30

MAGICK = shutil.which("magick")


def cover(img, w, h, focus_y=0.4):
    s = max(w / img.width, h / img.height)
    im = img.resize((max(w, int(img.width * s + 0.5)), max(h, int(img.height * s + 0.5))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int(max(0, min(im.height - h, (im.height - h) * focus_y)))
    return im.crop((x, y, x + w, y + h))


def vignette(w, h, strength=0.75, center=(0.5, 0.5)):
    small = Image.new("L", (w // 8, h // 8))
    px = small.load()
    cx, cy = center[0] * small.width, center[1] * small.height
    rmax = math.hypot(max(cx, small.width - cx), max(cy, small.height - cy))
    for y in range(small.height):
        for x in range(small.width):
            r = math.hypot(x - cx, y - cy) / rmax
            px[x, y] = int(255 * min(1.0, max(0.0, (r - 0.35) / 0.65)) ** 1.6 * strength)
    return small.resize((w, h), Image.BILINEAR)


def star_points(cx, cy, r_out, r_in, n, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pattern_layer(w, h, color, alpha, step=120):
    """Transparent pattern of eight-pointed stars, a common Ottoman ornament."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for row, y in enumerate(range(-step, h + step, step)):
        off = (step // 2) if row % 2 else 0
        for x in range(-step + off, w + step, step):
            d.polygon(star_points(x, y, step * 0.30, step * 0.20, 8, rot=-67.5), outline=color + (alpha,), width=2)
            d.ellipse((x - step * 0.07, y - step * 0.07, x + step * 0.07, y + step * 0.07), outline=color + (alpha,), width=2)
    return layer


def feather_mask(w, h, left=0, right=0, bottom=0, top=0):
    m = Image.new("L", (w, h), 255)
    px = m.load()
    for x in range(w):
        for y in range(h):
            v = 1.0
            if left and x < left:
                v *= x / left
            if right and x > w - right:
                v *= (w - x) / right
            if bottom and y > h - bottom:
                v *= (h - y) / bottom
            if top and y < top:
                v *= y / top
            px[x, y] = int(255 * (v ** 1.3))
    return m


def compose_scene(src, w, h, portrait_cx):
    base = Image.new("RGB", (w, h))
    bd = ImageDraw.Draw(base)
    c1 = tuple(int(v * 0.55) for v in BG)
    c2 = tuple(int(v * 0.18) for v in BG)
    for x in range(w):
        t = x / (w - 1)
        bd.line((x, 0, x, h), fill=tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)))
    blur = cover(src, w, h, PORTRAIT_FOCUS).filter(ImageFilter.GaussianBlur(max(w, h) / 30))
    base = Image.blend(base, Image.blend(blur, Image.new("RGB", (w, h), BG), 0.5), 0.22)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(pattern_layer(w, h, GOLD, 34, step=int(h / 7)))

    ph = h
    pw = int(src.width * ph / src.height)
    if pw > w * 0.62:
        pw = int(w * 0.62)
        portrait = cover(src, pw, ph, PORTRAIT_FOCUS)
    else:
        portrait = src.resize((pw, ph), Image.LANCZOS)
    mask = feather_mask(pw, ph, left=int(pw * 0.35), right=int(pw * 0.30), bottom=int(ph * 0.12), top=int(ph * 0.04))
    shadow = Image.new("RGBA", (pw + 80, ph), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (40, 0), mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    x = int(portrait_cx - pw / 2)
    canvas.alpha_composite(shadow, (x - 40, 0))
    pr = portrait.convert("RGBA")
    pr.putalpha(mask)
    canvas.alpha_composite(pr, (x, 0))

    dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dark.putalpha(vignette(w, h, 0.85, center=(portrait_cx / w, 0.42)))
    canvas.alpha_composite(dark)
    d = ImageDraw.Draw(canvas)
    m = int(h * 0.025)
    d.rectangle((m, m, w - m, h - m), outline=GOLD + (200,), width=max(2, h // 300))
    m2 = m + max(5, h // 120)
    d.rectangle((m2, m2, w - m2, h - m2), outline=GOLD + (120,), width=1)
    return canvas


def tree_mask(size):
    """The tree of Osman's dream: a trunk with branches and a crescent-shaped crown."""
    S = size
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    c = S / 2
    # crown: five round clusters
    for dx, dy, r in ((0.0, -0.20, 0.17), (-0.20, -0.08, 0.14), (0.20, -0.08, 0.14),
                      (-0.12, -0.30, 0.11), (0.12, -0.30, 0.11)):
        d.ellipse((c + S * (dx - r), c + S * (dy - r), c + S * (dx + r), c + S * (dy + r)), fill=255)
    # a crescent cut into the crown: the moon of the dream
    d.ellipse((c - S * 0.11, c - S * 0.31, c + S * 0.11, c - S * 0.09), fill=0)
    d.ellipse((c - S * 0.04, c - S * 0.34, c + S * 0.16, c - S * 0.14), fill=255)
    # trunk and roots
    d.polygon([(c - S * 0.055, c + S * 0.32), (c - S * 0.04, c - S * 0.08), (c + S * 0.04, c - S * 0.08),
               (c + S * 0.055, c + S * 0.32)], fill=255)
    d.polygon([(c - S * 0.05, c + S * 0.27), (c - S * 0.19, c + S * 0.34), (c, c + S * 0.32)], fill=255)
    d.polygon([(c + S * 0.05, c + S * 0.27), (c + S * 0.19, c + S * 0.34), (c, c + S * 0.32)], fill=255)
    return m


def civ_icon(size):
    S = 1024
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = S * 0.02
    d.ellipse((pad, pad, S - pad, S - pad), fill=BG + (255,))
    d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), outline=FG + (110,), width=int(S * 0.012))
    sym = tree_mask(int(S * 0.80))
    layer = Image.new("RGBA", sym.size, FG + (255,))
    layer.putalpha(sym)
    img.alpha_composite(layer, (int(S * 0.10), int(S * 0.12)))
    return img.resize((size, size), Image.LANCZOS)


def alpha_icon(size):
    S = 1024
    img = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    img.putalpha(tree_mask(S))
    return img.resize((size, size), Image.LANCZOS)


def leader_icon(src, size):
    S = 1024
    fx, fy, fs = FACE
    side = int(src.width * fs)
    cx, cy = int(src.width * fx), int(src.height * fy)
    x0 = max(0, min(src.width - side, cx - side // 2))
    y0 = max(0, min(src.height - side, cy - side // 2))
    face = src.crop((x0, y0, x0 + side, y0 + side)).resize((S, S), Image.LANCZOS)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), fill=255)
    img.paste(face, (0, 0), mask)
    ImageDraw.Draw(img).ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), outline=GOLD + (255,), width=int(S * 0.035))
    return img.resize((size, size), Image.LANCZOS)


def save_dds(img, path):
    """Uncompressed 32-bit (A8R8G8B8) DDS without mipmaps."""
    if MAGICK is None:
        raise SystemExit("ImageMagick (magick) not found")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    img.convert("RGBA").save(tmp)
    try:
        subprocess.check_call([MAGICK, tmp, "-alpha", "on", "-define", "dds:compression=none",
                               "-define", "dds:mipmaps=0", path])
    finally:
        os.remove(tmp)


def main():
    os.makedirs(DOCS, exist_ok=True)
    src = Image.open(SRC).convert("RGB")
    scene = compose_scene(src, 1600, 900, portrait_cx=1060)
    save_dds(scene, os.path.join(ART, "Leaders", "OB_Osman_Diplo.dds"))
    dom = compose_scene(src, 1024, 768, portrait_cx=690)
    save_dds(dom.convert("RGB").convert("RGBA"), os.path.join(ART, "Leaders", "OB_Osman_DOM.dds"))
    scene.convert("RGB").resize((800, 450), Image.LANCZOS).save(os.path.join(DOCS, "leader_osman.jpg"), quality=88)
    with open(os.path.join(ART, "Leaders", "OB_Osman_Scene.xml"), "w", encoding="utf-8") as fh:
        fh.write('<LeaderScene FallbackImage="OB_Osman_Diplo.dds"></LeaderScene>\n')

    for size in (256, 128, 80, 64, 48, 45, 32, 24, 16):
        save_dds(civ_icon(size), os.path.join(ART, "Icons", "OB_CivAtlas_%d.dds" % size))
    for size in (128, 80, 64, 48, 45, 32, 24, 16):
        save_dds(alpha_icon(size), os.path.join(ART, "Icons", "OB_CivAlphaAtlas_%d.dds" % size))
    for size in (256, 128, 80, 64, 45, 32):
        save_dds(leader_icon(src, size), os.path.join(ART, "Icons", "OB_LeaderAtlas_%d.dds" % size))

    sheet = Image.new("RGBA", (3 * 280 + 40, 300), (24, 24, 28, 255))
    sheet.alpha_composite(leader_icon(src, 256), (20, 22))
    sheet.alpha_composite(civ_icon(256), (300, 22))
    a = Image.new("RGBA", (256, 256), (60, 60, 66, 255))
    a.alpha_composite(alpha_icon(256))
    sheet.alpha_composite(a, (580, 22))
    sheet.convert("RGB").save(os.path.join(DOCS, "icons.png"))
    print("art built")


if __name__ == "__main__":
    main()
