"""
Generate supplement figure for ECCV 2026 rebuttal (R3 Q1).

Layout (3 rows × 10 columns):

  ┌──────────────┬───────────────┬──────┬──────┬─ … ─┬──────┐
  │  (row label) │   Reference   │ v0   │ v1   │ ... │ v7   │  ← col headers
  ├──────────────┼───────────────┼──────┼──────┼─ … ─┼──────┤
  │ OREO (Ours)  │  condition    │ v0_s │ v1_s │ ... │ v7_s │  ← OREO row
  ├──────────────┤   (spans 2   ├──────┼──────┼─ … ─┼──────┤
  │Teacher Target│    rows)      │ v0_t │ v1_t │ ... │ v7_t │  ← Teacher row
  └──────────────┴───────────────┴──────┴──────┴─ … ─┴──────┘
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).parent
OUT_PATH = BASE_DIR / "supplement_multiview.png"

N_VIEWS      = 8
CELL         = 300        # px per render cell
COND_W       = CELL + 20  # reference image column width (a bit wider)
LABEL_H      = 36         # column header row height
ROW_LABEL_W  = 160        # left row-label column width
PAD          = 8          # gap between cells
BG           = (250, 250, 250)
DIV_COLOR    = (190, 190, 190)

STRIPE_A     = (224, 230, 245)   # blue tint — OREO row
STRIPE_B     = (245, 228, 218)   # orange tint — Teacher row
STRIPES      = [STRIPE_A, STRIPE_B]

ROWS = [
    ("OREO (Ours)",    "student"),
    ("Teacher Target", "teacher"),
]

# ── font ─────────────────────────────────────────────────────────────────────
def try_font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

BOLD_PATHS = [
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
NORM_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
font_hdr  = try_font(BOLD_PATHS, 22)
font_row  = try_font(BOLD_PATHS, 20)
font_col  = try_font(NORM_PATHS, 18)

# ── helpers ──────────────────────────────────────────────────────────────────
def load_cell(path, size):
    """Load image, auto-crop whitespace, fit square cell."""
    img = Image.open(path).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    off = ((size - img.width) // 2, (size - img.height) // 2)
    canvas.paste(img, off, img)
    return canvas.convert("RGB")


def paste_label(canvas, text, x, y, w, h, font, fg=(40, 40, 40), bg=None):
    draw = ImageDraw.Draw(canvas)
    if bg:
        draw.rectangle([x, y, x + w, y + h], fill=bg)
    bx = draw.textbbox((0, 0), text, font=font)
    tw, th = bx[2] - bx[0], bx[3] - bx[1]
    draw.text((x + (w - tw) // 2, y + (h - th) // 2), text, fill=fg, font=font)


# ── compute canvas size ──────────────────────────────────────────────────────
n_rows = len(ROWS)
cond_h = n_rows * CELL + (n_rows - 1) * PAD  # reference image spans both rows

total_w = (ROW_LABEL_W + PAD
           + COND_W + PAD
           + N_VIEWS * (CELL + PAD))

total_h = LABEL_H + PAD + cond_h + PAD * 2

canvas = Image.new("RGB", (total_w, total_h), BG)
draw   = ImageDraw.Draw(canvas)

# ── stripe backgrounds ────────────────────────────────────────────────────────
for ri in range(n_rows):
    y_top = LABEL_H + PAD + ri * (CELL + PAD)
    draw.rectangle([0, y_top, total_w, y_top + CELL], fill=STRIPES[ri])

# ── column headers ────────────────────────────────────────────────────────────
# "Reference" header
paste_label(canvas, "Reference",
            ROW_LABEL_W + PAD, 0, COND_W, LABEL_H,
            font_hdr, fg=(60, 60, 60), bg=BG)

for vi in range(N_VIEWS):
    x = ROW_LABEL_W + PAD + COND_W + PAD + vi * (CELL + PAD)
    paste_label(canvas, f"View {vi}", x, 0, CELL, LABEL_H,
                font_col, fg=(80, 80, 80), bg=BG)

# ── reference image (spans both rows vertically) ─────────────────────────────
cond_path = BASE_DIR / "condition.png"
cond_img  = load_cell(cond_path, min(COND_W, cond_h))
# center in the cond column
cx = ROW_LABEL_W + PAD
cy = LABEL_H + PAD + (cond_h - cond_img.height) // 2
canvas.paste(cond_img, (cx, cy))

# thin border around reference cell
draw.rectangle(
    [cx - 1, LABEL_H + PAD - 1,
     cx + COND_W, LABEL_H + PAD + cond_h],
    outline=DIV_COLOR, width=1
)

# ── render rows ───────────────────────────────────────────────────────────────
for ri, (row_name, suffix) in enumerate(ROWS):
    y_top = LABEL_H + PAD + ri * (CELL + PAD)

    # row label
    paste_label(canvas, row_name,
                0, y_top, ROW_LABEL_W, CELL,
                font_row, fg=(30, 30, 30), bg=STRIPES[ri])

    for vi in range(N_VIEWS):
        fpath = BASE_DIR / f"v{vi}_{suffix}.png"
        if not fpath.exists():
            print(f"  [warn] missing {fpath.name}")
            continue
        cell_img = load_cell(fpath, CELL)
        x = ROW_LABEL_W + PAD + COND_W + PAD + vi * (CELL + PAD)
        canvas.paste(cell_img, (x, y_top))

        # thin cell border
        draw.rectangle([x - 1, y_top - 1, x + CELL, y_top + CELL],
                       outline=DIV_COLOR, width=1)

# ── horizontal divider between rows ──────────────────────────────────────────
y_div = LABEL_H + PAD + CELL + PAD // 2
draw.line([(ROW_LABEL_W, y_div), (total_w, y_div)], fill=(160, 160, 160), width=1)

# ── outer frame ───────────────────────────────────────────────────────────────
draw.rectangle([0, 0, total_w - 1, total_h - 1], outline=(140, 140, 140), width=2)

# ── save ─────────────────────────────────────────────────────────────────────
canvas.save(OUT_PATH, dpi=(150, 150))
print(f"Saved → {OUT_PATH}  ({total_w} × {total_h} px)")
