"""
Create a SV3D-style multi-view comparison figure for rebuttal R3-Qual1.

Rows:
  Input / Trellis / OREO

Columns:
  00250: three selected novel views
  04198: three selected novel views
  03360: three selected novel views

The selected views are intentionally object-specific because the v0-v7 camera
indices do not correspond to the same semantic direction for every object.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "mv_comparison"
OUT_PATH = BASE_DIR / "mv_comparison_00250_04198_03360.png"

CELL = 220
PAD = 8
ROW_LABEL_W = 130
SAMPLE_HEADER_H = 34
VIEW_HEADER_H = 28
ROW_H = CELL
BG = (255, 255, 255)
LINE = (205, 205, 205)
TEXT = (30, 30, 30)
SUBTEXT = (85, 85, 85)
INPUT_BG = (246, 246, 246)
TRELLIS_BG = (238, 242, 250)
OREO_BG = (247, 238, 231)

# sample_id, display_name, [(semantic view, view index), ...]
SAMPLES = [
    ("00250", "00250", [("View 1", 4), ("View 2", 6), ("View 3", 1)]),
    ("04198", "04198", [("View 1", 3), ("View 2", 6), ("View 3", 0)]),
    ("03360", "03360", [("View 1", 4), ("View 2", 7), ("View 3", 2)]),
]

ROWS = [
    ("Input", INPUT_BG),
    ("Trellis", TRELLIS_BG),
    ("OREO", OREO_BG),
]


def try_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


BOLD_FONT_PATHS = [
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
REG_FONT_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

FONT_SAMPLE = try_font(BOLD_FONT_PATHS, 20)
FONT_VIEW = try_font(REG_FONT_PATHS, 15)
FONT_ROW = try_font(BOLD_FONT_PATHS, 18)


def crop_white_border(img):
    """Crop near-white borders while preserving object content."""
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size

    min_x, min_y = w, h
    max_x, max_y = -1, -1
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 10 and not (r > 248 and g > 248 and b > 248):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x < min_x or max_y < min_y:
        return rgba

    margin = 8
    min_x = max(0, min_x - margin)
    min_y = max(0, min_y - margin)
    max_x = min(w - 1, max_x + margin)
    max_y = min(h - 1, max_y + margin)
    return rgba.crop((min_x, min_y, max_x + 1, max_y + 1))


def fit_image(path, box_w, box_h, crop=True):
    img = Image.open(path).convert("RGBA")
    if crop:
        img = crop_white_border(img)
    img.thumbnail((box_w, box_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (box_w, box_h), (255, 255, 255, 0))
    x = (box_w - img.width) // 2
    y = (box_h - img.height) // 2
    canvas.paste(img, (x, y), img)
    return canvas.convert("RGB")


def draw_centered_text(draw, text, box, font, fill=TEXT):
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - th) / 2),
              text, font=font, fill=fill)


def main():
    n_groups = len(SAMPLES)
    n_views = 3
    group_w = n_views * CELL + (n_views - 1) * PAD
    fig_w = ROW_LABEL_W + PAD + n_groups * group_w + (n_groups - 1) * (PAD * 2)
    fig_h = SAMPLE_HEADER_H + VIEW_HEADER_H + PAD + len(ROWS) * ROW_H + (len(ROWS) - 1) * PAD

    canvas = Image.new("RGB", (fig_w, fig_h), BG)
    draw = ImageDraw.Draw(canvas)

    y_sample_header = 0
    y_view_header = SAMPLE_HEADER_H
    y_rows = SAMPLE_HEADER_H + VIEW_HEADER_H + PAD

    # Row backgrounds and labels.
    for row_idx, (row_name, row_bg) in enumerate(ROWS):
        y = y_rows + row_idx * (ROW_H + PAD)
        draw.rectangle((0, y, fig_w, y + ROW_H), fill=row_bg)
        draw_centered_text(draw, row_name, (0, y, ROW_LABEL_W, y + ROW_H), FONT_ROW)

    # Sample headers, view headers, and cells.
    x = ROW_LABEL_W + PAD
    for sample_id, sample_name, views in SAMPLES:
        sample_dir = DATA_DIR / sample_id
        draw_centered_text(
            draw,
            sample_name,
            (x, y_sample_header, x + group_w, y_sample_header + SAMPLE_HEADER_H),
            FONT_SAMPLE,
        )

        # View labels.
        for view_idx, (view_name, _) in enumerate(views):
            vx = x + view_idx * (CELL + PAD)
            draw_centered_text(
                draw,
                view_name,
                (vx, y_view_header, vx + CELL, y_view_header + VIEW_HEADER_H),
                FONT_VIEW,
                fill=SUBTEXT,
            )

        # Input row: condition image centered across the three-view group.
        input_y = y_rows
        input_img = fit_image(sample_dir / "condition.png", group_w, ROW_H, crop=True)
        canvas.paste(input_img, (x, input_y))
        draw.rectangle((x, input_y, x + group_w, input_y + ROW_H), outline=LINE, width=1)

        # Trellis and OREO rows use paired single-view renders.
        for view_idx, (_, view_id) in enumerate(views):
            vx = x + view_idx * (CELL + PAD)

            trellis_y = y_rows + 1 * (ROW_H + PAD)
            trellis_img = fit_image(sample_dir / f"v{view_id}_teacher.png", CELL, ROW_H, crop=True)
            canvas.paste(trellis_img, (vx, trellis_y))
            draw.rectangle((vx, trellis_y, vx + CELL, trellis_y + ROW_H), outline=LINE, width=1)

            oreo_y = y_rows + 2 * (ROW_H + PAD)
            oreo_img = fit_image(sample_dir / f"v{view_id}_student.png", CELL, ROW_H, crop=True)
            canvas.paste(oreo_img, (vx, oreo_y))
            draw.rectangle((vx, oreo_y, vx + CELL, oreo_y + ROW_H), outline=LINE, width=1)

        # Group divider.
        draw.rectangle((x, y_rows, x + group_w, fig_h - 1), outline=(170, 170, 170), width=2)
        x += group_w + PAD * 2

    canvas.save(OUT_PATH, dpi=(300, 300))
    print(f"Saved -> {OUT_PATH} ({fig_w} x {fig_h} px)")


if __name__ == "__main__":
    main()
