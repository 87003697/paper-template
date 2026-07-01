"""
Camera-ready multi-view qualitative ablation figure.

Compares four training-loss / rollout variants that all share the OREO framework
skeleton but differ in one component (see Method §3.4):
    - OREO           : full model (contrastive + on-policy)
    - Pixel-MSE      : L2 in pixel space instead of latent contrastive
    - Off-Policy     : teacher rollout instead of on-policy student rollout
    - DMD            : single-step score-distillation

Local data (all 100 x 5-view alphaimages test set unless noted):
    figures_rebuttal/oreo_alphaimg_new/test_XX/{condition,v{0..4}_student}.png
    figures_rebuttal/off_alphaimg_new/test_XX/v{0..4}_student.png
    figures_rebuttal/dmd_alphaimg_new/test_XX/v{0..4}_student.png
    figures_rebuttal/mse_alphaimg_new/test_XX/color_v{0..2}.png   # 3 views only

Because MSE only has 3 views, hero + thumbs are all restricted to v0..v2.

Layout per sample-row:
    [Input 1x1]   [OREO cluster]   [Pixel-MSE cluster]   [Off-Policy cluster]   [DMD cluster]

Cluster:
    +-----------+-----+
    |           |  T1 |
    |   HERO    +-----+
    |    2x2    |  T2 |
    |           |     |
    +-----------+-----+

Output: figures_final/mv_ablation_final.png
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# Data locations -------------------------------------------------------------
BASE_DIR = Path(__file__).parent
OREO_ROOT = BASE_DIR / "oreo_alphaimg_new"
MSE_ROOT = BASE_DIR / "mse_alphaimg_new"
OFF_ROOT = BASE_DIR / "off_alphaimg_new"
DMD_ROOT = BASE_DIR / "dmd_alphaimg_new"

OUT_PATH = BASE_DIR.parent / "figures_final" / "mv_ablation_final.png"


# Samples --------------------------------------------------------------------
# (test_index, hero_view_id, [thumb_view_id_top, thumb_view_id_bottom])
# Views restricted to v0..v2 because MSE eval only saved 3 views.
# Samples --------------------------------------------------------------------
# (test_index, view_id)
# Views restricted to v0..v2 because MSE eval only saved 3 views.
SAMPLES = [
    (56, 1),
    (57, 3),
    (71, 4),
]


# Path resolvers -------------------------------------------------------------
def _test_dir(root, idx):
    return root / f"test_{idx:02d}"

def input_path(idx):
    return _test_dir(OREO_ROOT, idx) / "condition.png"

def oreo_path(idx, vid):
    return _test_dir(OREO_ROOT, idx) / f"v{vid}_student.png"

def mse_path(idx, vid):
    return _test_dir(MSE_ROOT, idx) / f"v{vid}_student.png"

def off_path(idx, vid):
    return _test_dir(OFF_ROOT, idx) / f"v{vid}_student.png"

def dmd_path(idx, vid):
    return _test_dir(DMD_ROOT, idx) / f"v{vid}_student.png"


METHODS = [
    ("OREO (ours)",   oreo_path),
    ("w/ Off-Policy", off_path),
    ("w/ Pixel-MSE",  mse_path),
    ("w/ DMD",        dmd_path),
]


# Layout constants -----------------------------------------------------------
CELL = 520                              # square cell size for hero image
GROUP_GAP = 40                          # gap between method columns
INPUT_GAP = 36                          # gap between input cell and first method
METHOD_HEADER_H = 84                    # top header row
ROW_GAP = 24                            # gap between sample rows

CLUSTER_W = CELL
CLUSTER_H = CELL
INPUT_W = CELL
INPUT_H = CELL

BG = (255, 255, 255)
LINE = (210, 210, 210)
TEXT = (30, 30, 30)


# Optional zoom insets (empty by default). Populate as
#   ZOOM_RULES[(test_index, method_label)] = (crop_box, position)
# where crop_box is (x0,y0,x1,y1) inside the CELL x CELL canvas
# and position is one of "upper_left" / "lower_left" / "upper_right" / "lower_right".
ZOOM_RULES = {}
ZOOM_INSET = 110
ZOOM_BORDER = (210, 45, 45)


# Fonts ----------------------------------------------------------------------
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

FONT_HEADER = try_font(BOLD_FONT_PATHS, 52)


# Image helpers --------------------------------------------------------------
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


def add_zoom_inset(img, crop_box, inset_size=ZOOM_INSET, position="upper_left"):
    out = img.copy()
    draw = ImageDraw.Draw(out)
    zoom = img.crop(crop_box).resize((inset_size, inset_size), Image.LANCZOS)
    if position in ("lower_left", "upper_left"):
        inset_x = 8
    else:
        inset_x = img.width - inset_size - 8
    if position in ("upper_left", "upper_right"):
        inset_y = 8
    else:
        inset_y = img.height - inset_size - 8
    out.paste(zoom, (inset_x, inset_y))
    draw.rectangle(
        (inset_x, inset_y, inset_x + inset_size, inset_y + inset_size),
        outline=ZOOM_BORDER, width=4,
    )
    return out


def draw_centered_text(draw, text, box, font, fill=TEXT):
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - th) / 2),
              text, font=font, fill=fill)


# Rendering ------------------------------------------------------------------
def compute_geometry():
    fig_w = (
        INPUT_W
        + INPUT_GAP
        + len(METHODS) * CLUSTER_W
        + (len(METHODS) - 1) * GROUP_GAP
    )
    fig_h = (
        METHOD_HEADER_H
        + len(SAMPLES) * CLUSTER_H
        + (len(SAMPLES) - 1) * ROW_GAP
    )
    return fig_w, fig_h


def render_cluster(idx, mlabel, mpath_fn, vid):
    cell = fit_image(mpath_fn(idx, vid), CELL, CELL, crop=True)
    if (idx, mlabel) in ZOOM_RULES:
        crop_box, position = ZOOM_RULES[(idx, mlabel)]
        cell = add_zoom_inset(cell, crop_box, position=position)
    return cell


def main():
    fig_w, fig_h = compute_geometry()
    canvas = Image.new("RGB", (fig_w, fig_h), BG)
    draw = ImageDraw.Draw(canvas)

    x_input = 0
    x_methods_start = INPUT_W + INPUT_GAP
    x_method_origins = [
        x_methods_start + i * (CLUSTER_W + GROUP_GAP)
        for i in range(len(METHODS))
    ]

    # Method headers
    draw_centered_text(
        draw, "Input",
        (x_input, 0, x_input + INPUT_W, METHOD_HEADER_H),
        FONT_HEADER,
    )
    for (label, _), x_origin in zip(METHODS, x_method_origins):
        draw_centered_text(
            draw, label,
            (x_origin, 0, x_origin + CLUSTER_W, METHOD_HEADER_H),
            FONT_HEADER,
        )

    # Sample rows
    y_rows_start = METHOD_HEADER_H
    for row_idx, (idx, vid) in enumerate(SAMPLES):
        y = y_rows_start + row_idx * (CLUSTER_H + ROW_GAP)

        cond_img = fit_image(input_path(idx), INPUT_W, INPUT_H, crop=True)
        canvas.paste(cond_img, (x_input, y))

        for (mlabel, mpath_fn), x_origin in zip(METHODS, x_method_origins):
            cluster = render_cluster(idx, mlabel, mpath_fn, vid)
            canvas.paste(cluster, (x_origin, y))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PATH, dpi=(300, 300))
    print(f"Saved -> {OUT_PATH} ({fig_w} x {fig_h} px, ratio {fig_w / fig_h:.2f}:1)")


if __name__ == "__main__":
    main()
