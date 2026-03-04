import argparse
import os
from typing import List

import matplotlib.pyplot as plt


def parse_csv_floats(text: str) -> List[float]:
    values = [v.strip() for v in text.split(",") if v.strip()]
    return [float(v) for v in values]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot DINO Sim and Mask IoU against NFE with dual y-axes."
    )
    parser.add_argument(
        "--nfe",
        type=str,
        default="12,24,36,48",
        help="Comma-separated NFE values, e.g. 12,24,36,48",
    )
    parser.add_argument(
        "--dino",
        type=str,
        default="0.0029,0.0144,0.0311,-0.008",
        help="Comma-separated DINO Sim values, same length as --nfe",
    )
    parser.add_argument(
        "--iou",
        type=str,
        default="0.9925,0.9804,0.9397,0.6541",
        help="Comma-separated Mask IoU values, same length as --nfe",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="figures/plots/nfe_dino_iou.png",
        help="Output image path",
    )
    parser.add_argument(
        "--fig-width",
        type=float,
        default=4.8,
        help="Figure width in inches",
    )
    parser.add_argument(
        "--fig-height",
        type=float,
        default=3.0,
        help="Figure height in inches",
    )
    args = parser.parse_args()

    nfe = parse_csv_floats(args.nfe)
    dino = parse_csv_floats(args.dino)
    iou = parse_csv_floats(args.iou)

    if not (len(nfe) == len(dino) == len(iou)):
        raise ValueError(
            "Length mismatch: --nfe, --dino, and --iou must have the same number of values."
        )

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(args.fig_width, args.fig_height), dpi=160)
    ax2 = ax1.twinx()

    line1 = ax1.plot(
        nfe,
        dino,
        color="#1f77b4",
        marker="o",
        linewidth=2.2,
        markersize=5.5,
        label="DINO Sim",
    )
    line2 = ax2.plot(
        nfe,
        iou,
        color="#d62728",
        marker="s",
        linewidth=2.2,
        markersize=5.5,
        label="Mask IoU",
    )

    ax1.set_xlabel("NFE", fontsize=11)
    ax1.set_ylabel("DINO Sim", color="#1f77b4", fontsize=11)
    ax2.set_ylabel("Mask IoU", color="#d62728", fontsize=11)
    ax1.tick_params(axis="y", labelcolor="#1f77b4")
    ax2.tick_params(axis="y", labelcolor="#d62728")
    ax1.grid(True, linestyle="--", alpha=0.3)
    ax1.set_xticks(nfe)

    # Keep a compact range for easier trend comparison.
    dino_pad = max(1e-4, (max(dino) - min(dino)) * 0.2)
    iou_pad = max(1e-4, (max(iou) - min(iou)) * 0.2)
    ax1.set_ylim(min(dino) - dino_pad, max(dino) + dino_pad)
    ax2.set_ylim(min(iou) - iou_pad, max(iou) + iou_pad)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="best", frameon=False)

    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    print(f"Saved figure to: {args.out}")


if __name__ == "__main__":
    main()
