"""
Per-sample contact sheet for view selection.

For each SAMPLES entry, produces figures_final/mv_ablation_picker_test_XX.png
showing every view of every method side-by-side so the user can pick
which (idx, view_id) to freeze into make_mv_ablation_fig_final.py:SAMPLES.

Layout (per sample):
    row 0: header  Input  v0  v1  v2  v3  v4
    row 1: OREO      -    ...
    row 2: Off-Policy -   ...
    row 3: Pixel-MSE -    v0  v1  v2  (v3, v4 blank — MSE has 3 views only)
    row 4: DMD       -    v0  v1  v2  v3  v4
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).parent
OREO_ROOT = BASE_DIR / "oreo_alphaimg_new"
MSE_ROOT = BASE_DIR / "mse_alphaimg_new"
OFF_ROOT = BASE_DIR / "off_alphaimg_new"
DMD_ROOT = BASE_DIR / "dmd_alphaimg_new"

OUT_DIR = BASE_DIR.parent / "figures_final"

SAMPLES = [56, 57, 68, 71]
N_VIEWS = 5


def _test_dir(root, idx):
    return root / f"test_{idx:02d}"

def input_path(idx):
    return _test_dir(OREO_ROOT, idx) / "condition.png"

def oreo_path(idx, vid):
    return _test_dir(OREO_ROOT, idx) / f"v{vid}_student.png"

def mse_path(idx, vid):
    p = _test_dir(MSE_ROOT, idx) / f"v{vid}_student.png"
    return p if p.exists() else None

def off_path(idx, vid):
    return _test_dir(OFF_ROOT, idx) / f"v{vid}_student.png"

def dmd_path(idx, vid):
    return _test_dir(DMD_ROOT, idx) / f"v{vid}_student.png"


METHODS = [
    ("OREO",       oreo_path),
    ("Off-Policy", off_path),
    ("Pixel-MSE",  mse_path),
    ("DMD",        dmd_path),
]


CELL = 300
ROW_H = 44
COL_W = CELL
LABEL_W = 200
GAP = 8
BG = (255, 255, 255)
TEXT = (30, 30, 30)
MISSING_BG = (240, 240, 240)


BOLD_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Times New Roman Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def try_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

FONT = try_font(BOLD_FONT_PATHS, 22)


def crop_white_border(img):
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    min_x, min_y = w, h
    max_x, max_y = -1, -1
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 10 and not (r > 248 and g > 248 and b > 248):
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
    if max_x < min_x or max_y < min_y:
        return rgba
    m = 8
    return rgba.crop((max(0, min_x - m), max(0, min_y - m),
                      min(w - 1, max_x + m) + 1, min(h - 1, max_y + m) + 1))


def fit_image(path, box, crop=True):
    img = Image.open(path).convert("RGBA")
    if crop:
        img = crop_white_border(img)
    img.thumbnail((box, box), Image.LANCZOS)
    canvas = Image.new("RGBA", (box, box), (255, 255, 255, 0))
    x = (box - img.width) // 2
    y = (box - img.height) // 2
    canvas.paste(img, (x, y), img)
    return canvas.convert("RGB")


def missing_cell(size):
    tile = Image.new("RGB", (size, size), MISSING_BG)
    d = ImageDraw.Draw(tile)
    d.text((size // 2 - 20, size // 2 - 12), "n/a", font=FONT, fill=TEXT)
    return tile


def build_sheet(idx):
    n_cols = 1 + N_VIEWS   # Input + v0..v4
    n_rows = 1 + len(METHODS)  # header + methods
    W = LABEL_W + n_cols * COL_W + n_cols * GAP
    H = ROW_H + n_rows * (CELL + GAP)

    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # header
    d_y = 8
    draw.text((10, d_y), f"test_{idx:02d}", font=FONT, fill=TEXT)
    header_x = LABEL_W
    draw.text((header_x + 4, d_y), "Input", font=FONT, fill=TEXT)
    for v in range(N_VIEWS):
        x = LABEL_W + (1 + v) * (COL_W + GAP)
        draw.text((x + 4, d_y), f"v{v}", font=FONT, fill=TEXT)

    # rows
    y = ROW_H
    # Method rows: label + input(only col 0 of first row shows input) + views
    # But we want Input column across all rows to show the same reference; simpler:
    # row_i = i-th method: [method_label] [input] [v0] [v1] [v2] [v3] [v4]
    for row_idx, (mlabel, mpath) in enumerate(METHODS):
        # Label
        draw.text((10, y + CELL // 2 - 12), mlabel, font=FONT, fill=TEXT)

        # Input reference
        try:
            cond = fit_image(input_path(idx), CELL)
        except Exception:
            cond = missing_cell(CELL)
        canvas.paste(cond, (LABEL_W, y))

        for v in range(N_VIEWS):
            x = LABEL_W + (1 + v) * (COL_W + GAP)
            p = mpath(idx, v)
            if p is None or (isinstance(p, Path) and not p.exists()):
                canvas.paste(missing_cell(CELL), (x, y))
            else:
                canvas.paste(fit_image(p, CELL), (x, y))

        y += CELL + GAP

    return canvas


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for idx in SAMPLES:
        sheet = build_sheet(idx)
        out = OUT_DIR / f"mv_ablation_picker_test_{idx:02d}.png"
        sheet.save(out, dpi=(150, 150))
        print(f"Saved -> {out} ({sheet.width} x {sheet.height} px)")


if __name__ == "__main__":
    main()
