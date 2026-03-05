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

# Data for Effect of Editing Ratio (Fixed N=12)
# Ratio: 0.25, 0.50, 0.75, 1.00
# Steps: 3|12, 6|12, 9|12, 12|12
ratios = [0.25, 0.50, 0.75, 1.00]
ratio_clip_delta = [0.0034, 0.0031, 0.0123, -0.0738]
ratio_dino_delta = [0.0029, 0.0144, 0.0311, -0.0080]
ratio_iou = [0.9925, 0.9804, 0.9397, 0.6541]

# Data for Effect of Absolute Steps (Fixed Ratio ~0.75)
# Steps: 6|8, 9|12, 15|20, 30|40
# Total Steps N: 8, 12, 20, 40
steps_N = [6, 9, 15, 30]
steps_clip_delta = [0.0061, 0.0123, 0.0177, 0.0216]
steps_dino_delta = [0.0240, 0.0311, 0.0398, 0.0474]
steps_iou = [0.9489, 0.9397, 0.9280, 0.9159]

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
plt.savefig('figures/plots/ablation_ratio_steps.png', dpi=300, bbox_inches='tight')
print("Plot saved to figures/plots/ablation_ratio_steps.png")
