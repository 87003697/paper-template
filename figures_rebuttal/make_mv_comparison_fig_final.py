"""
Camera-ready multi-view qualitative comparison figure.

Layout per (sample, method) cluster:
    +-----------+-----+
    |           |  T1 |   <- 1x1 thumbnail
    |   HERO    +-----+
    |   2x2     |  T2 |   <- 1x1 thumbnail
    |           |     |
    +-----------+-----+
The hero cell carries a zoom inset (red border) when configured.

Overall figure:
    Sample 1 row:  [Input 1x1]   [Trellis cluster]   [Photo3D cluster]   [OREO cluster]
    Sample 2 row:  [Input 1x1]   [Trellis cluster]   [Photo3D cluster]   [OREO cluster]
    Sample 3 row:  [Input 1x1]   [Trellis cluster]   [Photo3D cluster]   [OREO cluster]

Output: figures_final/mv_comparison_final.png
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "mv_comparison"
PHOTO3D_DIR = BASE_DIR / "mv_comparison_photo3d"
OUT_PATH = BASE_DIR.parent / "figures_final" / "mv_comparison_final.png"


# Layout constants -----------------------------------------------------------
CELL = 260                              # base unit (1x1 thumbnail)
HERO = CELL * 2                         # 2x2 hero
PAD_INNER = 8                           # gap inside a cluster
PAD_THUMB = 8                           # gap between two stacked thumbs
GROUP_GAP = 40                          # gap between method clusters
INPUT_GAP = 36                          # gap between input cell and first method
SAMPLE_LABEL_W = 0                      # no rotated sample label (keep clean)
METHOD_HEADER_H = 84                    # top header row
ROW_GAP = 24                            # gap between sample rows

CLUSTER_W = HERO + PAD_INNER + CELL     # 2x2 width + gap + 1x1
CLUSTER_H = HERO                        # 2x2 height (= 2 stacked thumbs height)
INPUT_W = CELL                          # input image width
INPUT_H = HERO                          # match cluster height for visual alignment

BG = (255, 255, 255)
LINE = (210, 210, 210)
TEXT = (30, 30, 30)
INPUT_BG = (246, 246, 246)
TRELLIS_BG = (238, 242, 250)
PHOTO3D_BG = (241, 246, 239)
OREO_BG = (247, 238, 231)
ZOOM_BORDER = (210, 45, 45)
ZOOM_INSET = 110                        # bigger inset since hero is 520px


# Samples --------------------------------------------------------------------
# (sample_id, display_name, hero_view_id, thumb_view_ids[2])
# Hero choices match rebuttal narrative: zoom regions on parrot eye/beak (v3
# front) and bonsai twisted trunk (v4 front); minotaur hero = v6 back to make
# back-view color inconsistency the dominant signal.
SAMPLES = [
    ("00250", "Minotaur", 6, [4, 1]),
    ("04198", "Parrot",   3, [6, 0]),
    ("03360", "Bonsai",   4, [7, 2]),
]


# Methods --------------------------------------------------------------------
def trellis_path(sid, vid):
    return DATA_DIR / sid / f"v{vid}_teacher.png"

def photo3d_path(sid, vid):
    return PHOTO3D_DIR / f"{sid}_v{vid}_student.png"

def oreo_path(sid, vid):
    return DATA_DIR / sid / f"v{vid}_student.png"


METHODS = [
    ("Trellis",  TRELLIS_BG, trellis_path),
    ("Photo3D",  PHOTO3D_BG, photo3d_path),
    ("OREO",     OREO_BG,    oreo_path),
]


# Zoom rules: only on hero cell of certain (sample, method)
# Box coordinates are in the 520x520 hero canvas. For the parrot front view (v3)
# the head/beak occupies the upper-right area; for the bonsai courtyard (v4)
# the twisted trunk runs vertically through the right-center of the image.
PARROT_ZOOM_BOX = (260, 0, 460, 200)
BONSAI_ZOOM_BOX = (260, 130, 440, 360)
ZOOM_RULES = {
    ("04198", "Trellis"): (PARROT_ZOOM_BOX, "lower_left"),
    ("04198", "Photo3D"): (PARROT_ZOOM_BOX, "lower_left"),
    ("04198", "OREO"):    (PARROT_ZOOM_BOX, "lower_left"),
    ("03360", "Trellis"): (BONSAI_ZOOM_BOX, "lower_left"),
    ("03360", "Photo3D"): (BONSAI_ZOOM_BOX, "lower_left"),
    ("03360", "OREO"):    (BONSAI_ZOOM_BOX, "lower_left"),
}


# Fonts ----------------------------------------------------------------------
BOLD_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Times New Roman Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
REG_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/Library/Fonts/Times New Roman.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def try_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_METHOD = try_font(BOLD_FONT_PATHS, 52)
FONT_INPUT = try_font(BOLD_FONT_PATHS, 52)


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
    if position == "upper_left":
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


# Main -----------------------------------------------------------------------
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


def render_cluster(sid, mlabel, mpath_fn, hero_vid, thumb_vids):
    """Render a single sample x method cluster (HERO + 2 thumbs)."""
    cluster = Image.new("RGB", (CLUSTER_W, CLUSTER_H), BG)

    # Hero (2x2)
    hero_img = fit_image(mpath_fn(sid, hero_vid), HERO, HERO, crop=True)
    if (sid, mlabel) in ZOOM_RULES:
        crop_box, position = ZOOM_RULES[(sid, mlabel)]
        hero_img = add_zoom_inset(hero_img, crop_box, position=position)
    cluster.paste(hero_img, (0, 0))

    # Two stacked thumbs on the right
    thumb_h = (HERO - PAD_THUMB) // 2
    for i, vid in enumerate(thumb_vids):
        ty = i * (thumb_h + PAD_THUMB)
        tx = HERO + PAD_INNER
        thumb_img = fit_image(mpath_fn(sid, vid), CELL, thumb_h, crop=True)
        cluster.paste(thumb_img, (tx, ty))

    return cluster


def main():
    fig_w, fig_h = compute_geometry()
    canvas = Image.new("RGB", (fig_w, fig_h), BG)
    draw = ImageDraw.Draw(canvas)

    # X coordinates ------------------------------------------------------
    x_input = 0
    x_methods_start = INPUT_W + INPUT_GAP
    x_method_origins = [
        x_methods_start + i * (CLUSTER_W + GROUP_GAP)
        for i in range(len(METHODS))
    ]

    # Method headers (with bg tint) --------------------------------------
    draw_centered_text(
        draw, "Input",
        (x_input, 0, x_input + INPUT_W, METHOD_HEADER_H),
        FONT_INPUT,
    )
    for (label, bg, _), x_origin in zip(METHODS, x_method_origins):
        draw_centered_text(
            draw, label,
            (x_origin, 0, x_origin + CLUSTER_W, METHOD_HEADER_H),
            FONT_METHOD,
        )

    # Sample rows --------------------------------------------------------
    y_rows_start = METHOD_HEADER_H
    for row_idx, (sid, sname, hero_vid, thumb_vids) in enumerate(SAMPLES):
        y = y_rows_start + row_idx * (CLUSTER_H + ROW_GAP)

        # Input cell (vertically centered in CLUSTER_H)
        cond_path = DATA_DIR / sid / "condition.png"
        cond_img = fit_image(cond_path, INPUT_W, INPUT_H, crop=True)
        canvas.paste(cond_img, (x_input, y))

        # Method clusters
        for (mlabel, mbg, mpath_fn), x_origin in zip(METHODS, x_method_origins):
            cluster = render_cluster(sid, mlabel, mpath_fn, hero_vid, thumb_vids)
            canvas.paste(cluster, (x_origin, y))

    canvas.save(OUT_PATH, dpi=(300, 300))
    print(f"Saved -> {OUT_PATH} ({fig_w} x {fig_h} px, ratio {fig_w / fig_h:.2f}:1)")


if __name__ == "__main__":
    main()
