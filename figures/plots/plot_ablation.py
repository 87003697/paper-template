import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns

# Set style
# sns.set_theme(style="whitegrid")
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12

# Data aggregated from eval_metrics_full-rndm_steps-*_cfg-4_src-0_prompt_v15/
# guidance_similarity.csv (deduped by test+view, n=501).

# Data for Effect of Editing Ratio (Fixed N=12)
# Ratio: 0.25, 0.50, 0.75, 1.00
# Steps: 3|12, 6|12, 9|12, 12|12
ratios = [0.25, 0.50, 0.75, 1.00]
ratio_clip_delta = [0.0024, 0.0040, 0.0379, -0.0416]
ratio_dino_delta = [0.0012, 0.0065, 0.0299, -0.0628]
ratio_iou        = [0.9933, 0.9869, 0.9520,  0.6891]

# Data for Effect of Absolute Steps (Fixed Ratio ~0.75)
# Steps: 6|8, 9|12, 15|20, 30|40
# Editing steps N_e: 6, 9, 15, 30
steps_N = [6, 9, 15, 30]
steps_clip_delta = [0.0226, 0.0379, 0.0496, 0.0614]
steps_dino_delta = [0.0171, 0.0299, 0.0358, 0.0450]
steps_iou        = [0.9666, 0.9520, 0.9360, 0.9205]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# --- Plot 1: Effect of Editing Ratio ---
color_sem = 'tab:blue'
color_geo = 'tab:red'

# Left Y-axis: Semantic Improvement (CLIP/DINO)
ax1.set_xlabel('Editing Ratio ($N_e/N$)', fontsize=14)
ax1.set_ylabel('Semantic Improvement ($\Delta$)', color=color_sem, fontsize=14)
l1 = ax1.plot(ratios, ratio_clip_delta, marker='o', linestyle='-', color=color_sem, label='CLIP Sim $\Delta$', linewidth=2, markersize=8)
l2 = ax1.plot(ratios, ratio_dino_delta, marker='s', linestyle='--', color='tab:cyan', label='DINO Sim $\Delta$', linewidth=2, markersize=8)
ax1.tick_params(axis='y', labelcolor=color_sem)
ax1.grid(True, linestyle='--', alpha=0.7)

# Right Y-axis: Geometric Consistency (IoU)
ax1_right = ax1.twinx()
ax1_right.set_ylabel('Geometric Consistency (Mask IoU)', color=color_geo, fontsize=14)
l3 = ax1_right.plot(ratios, ratio_iou, marker='^', linestyle='-', color=color_geo, label='Mask IoU', linewidth=2, markersize=8)
ax1_right.tick_params(axis='y', labelcolor=color_geo)
ax1_right.set_ylim(0.5, 1.05)  # Adjust ylim for IoU to show drop clearly

# Combine legends
lines1 = l1 + l2 + l3
labels1 = [l.get_label() for l in lines1]
ax1.legend(lines1, labels1, loc='center left', frameon=True, framealpha=0.9)
ax1.set_title('(a) Effect of Editing Ratio (Fixed $N=12$)', fontsize=16, pad=15)
ax1.set_xticks(ratios)

# --- Plot 2: Effect of Absolute Steps ---
# Left Y-axis: Semantic Improvement
ax2.set_xlabel('Editing Steps ($N_e$)', fontsize=14)
ax2.set_ylabel('Semantic Improvement ($\Delta$)', color=color_sem, fontsize=14)
l4 = ax2.plot(steps_N, steps_clip_delta, marker='o', linestyle='-', color=color_sem, label='CLIP Sim $\Delta$', linewidth=2, markersize=8)
l5 = ax2.plot(steps_N, steps_dino_delta, marker='s', linestyle='--', color='tab:cyan', label='DINO Sim $\Delta$', linewidth=2, markersize=8)
ax2.tick_params(axis='y', labelcolor=color_sem)
ax2.grid(True, linestyle='--', alpha=0.7)

# Right Y-axis: Geometric Consistency
ax2_right = ax2.twinx()
ax2_right.set_ylabel('Geometric Consistency (Mask IoU)', color=color_geo, fontsize=14)
l6 = ax2_right.plot(steps_N, steps_iou, marker='^', linestyle='-', color=color_geo, label='Mask IoU', linewidth=2, markersize=8)
ax2_right.tick_params(axis='y', labelcolor=color_geo)
ax2_right.set_ylim(0.85, 1.01) # Zoom in for IoU since changes are smaller here

# Combine legends
lines2 = l4 + l5 + l6
labels2 = [l.get_label() for l in lines2]
ax2.legend(lines2, labels2, loc='center right', frameon=True, framealpha=0.9)
ax2.set_title('(b) Effect of Absolute Steps (Fixed Ratio $\\approx 0.75$)', fontsize=16, pad=15)
ax2.set_xticks(steps_N)

plt.tight_layout()
plt.savefig('figures_final/ablation_ratio_steps.png', dpi=300, bbox_inches='tight')
print("Plot saved to figures_final/ablation_ratio_steps.png")
