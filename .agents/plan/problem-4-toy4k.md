# Plan: OREO Camera-Ready Problem 4 - Toy4K Evaluation

## 目标

在 `supplementary.tex` 中补入 Toy4K 官方协议定量实验、指标含义和结果解读，回应 rebuttal 承诺；`camera_ready.tex` 只保留一句简短说明指向 Supplementary，避免新增正文表格占页。

## 关键发现（Explore 阶段）

- `camera_ready.tex` 当前 `Sec. 4.2 Main Results` 已有主结果表 `tab:main_results`，指标为 `CLIP Sim. / DINO Sim. / MANIQA / MUSIQ`，对应自建 Conceptual Design Dataset。
- `rebuttal.tex` 已有 Toy4K 数值，可直接迁移：Trellis `86.78 / 9.23 / 66.82 / 0.73`，Photo3D `86.89 / 9.09 / 76.98 / 0.70`，OREO `87.12 / 9.12 / 62.54 / 0.70`，OREO w/o noise update `86.83 / 9.39 / 67.41 / 0.72`。
- Toy4K 指标是 `CLIP`, `FD_inc`, `FD_dino`, `KD_dino`，和正文 Table 1 的指标体系不同；既然实验主体放在 Supplementary，就不应在正文新增独立 Toy4K 表。
- 当前正文已有 `tab:feedback_comparison`、`tab:main_results`、`tab:ablation_quantitative`；不新增正文表格可以避免打乱正文 Table 顺序和页数控制。
- `supplementary.tex` 当前有 `Implementation and Dataset Details` 占位，适合加入 `Benchmark Evaluation on Toy4K` 小节并放置 Toy4K 定量表。

## 相关文件

| 文件 | 位置 | 作用 |
|------|------|------|
| `camera_ready.tex` | `Sec. 4.2 Main Results` | 只加入一句 Toy4K 补充实验指引 |
| `supplementary.tex` | `Implementation and Dataset Details` | 新增 Toy4K 小节、协议说明、指标解释和定量表 |
| `rebuttal.tex` | Toy4K 表格 | Toy4K 数值来源 |
| `.agents/plan/camera-ready.md` | Problem 4 | 总计划记录，已改为 Supplementary 承载方案 |

## 推荐方案

在 `camera_ready.tex` 的 `Sec. 4.2` 定量段落末尾追加一句 cross-benchmark 指引，不放表格。这样正文仍以 Conceptual Design Dataset 为主，不引入额外表格占页，同时明确 Toy4K 标准 benchmark 结果在 Supplementary 中提供。

在 `supplementary.tex` 的 `Implementation and Dataset Details` 下新增 `Benchmark Evaluation on Toy4K` 小节，包含协议说明、指标解释、Toy4K 表格和短结果解读：

- Toy4K 是 Trellis 官方评估使用的标准 benchmark / test set，因此比 Objaverse 更适合作为补充评估。
- 指标遵循 Trellis protocol：CLIP 衡量 image-text / semantic alignment，`FD_inc` 和 `FD_dino` 衡量分布距离，`KD_dino` 衡量 kernel distance。
- Supplementary Table `tab:toy4k` 的结果显示 OREO 在 CLIP 和 `FD_dino` 上最好，在 `FD_inc` 和 `KD_dino` 上与最佳结果接近；`w/o Noise Update` 下降，作为 Toy4K 上的轻量交叉验证。

## 实施步骤

- [x] Step 1: 在 `camera_ready.tex` 的 `Sec. 4.2` 定量段落末尾加入一句 Toy4K Supplementary 指引。
- [x] Step 2: 在 `supplementary.tex` 的 `Implementation and Dataset Details` 下新增 `Benchmark Evaluation on Toy4K` 小节。
- [x] Step 3: 从 `rebuttal.tex` 迁移 Toy4K 数值，在 `supplementary.tex` 中创建表格 `tab:toy4k`。
- [x] Step 4: 检查方法命名、指标符号、表格 label、正文与 Supplementary 表述一致性。
- [x] Step 5: 编译 `camera_ready.tex` 与 `supplementary.tex`，检查引用、表格编号、overfull/underfull warning 和正文页数影响。

## Code Diff（涉及改动时必填）

#### `camera_ready.tex` (+1)

```diff
@@ Sec. 4.2 Main Results — 增加 Toy4K Supplementary 指引
 Against Photo3D, OREO achieves the best CLIP Similarity and MANIQA, while Photo3D is higher on DINO Similarity and MUSIQ.
 This result indicates a clear trade-off: Photo3D favors global feature consistency and smooth perceptual quality, whereas OREO better preserves reference-specific semantics and fine-grained texture realism.
 The trend is consistent with our design: OREO relies on on-the-fly adaptive pseudo-GT supervision from editing priors, while Photo3D is an offline pipeline without adaptive pseudo-GT updates and is therefore more dependent on fixed training targets.
+We additionally evaluate OREO on Toy4K following the official Trellis protocol; the full benchmark results and metric details are provided in the Supplementary Material.
 
 \textbf{Qualitative Evaluation.}
```

#### `supplementary.tex` (+35 左右)

```diff
@@ Implementation and Dataset Details — 新增 Toy4K benchmark 小节
 \section{Implementation and Dataset Details}
 \label{sec:implementation_details}
 Placeholder for implementation details, prompts, and dataset statistics.
+
+\subsection{Benchmark Evaluation on Toy4K}
+\label{sec:toy4k_details}
+We additionally evaluate OREO on Toy4K, a standard benchmark used by the official Trellis evaluation protocol.
+Unlike our Conceptual Design Dataset, which focuses on challenging in-the-wild user inputs, Toy4K provides a complementary benchmark for measuring whether the learned fidelity alignment transfers to a conventional test distribution.
+We follow the Trellis protocol and report CLIP, FD$_{\text{inc}}$, FD$_{\text{dino}}$, and KD$_{\text{dino}}$ in Table~\ref{tab:toy4k}.
+
+\begin{table}[t]
+  \centering
+  \caption{Evaluation on Toy4K following the official Trellis protocol.}
+  \label{tab:toy4k}
+  \scriptsize
+  \setlength{\tabcolsep}{3pt}
+  \begin{tabular}{@{}lcccc@{}}
+    \toprule
+    Method & CLIP $\uparrow$ & FD$_{\text{inc}}\downarrow$ & FD$_{\text{dino}}\downarrow$ & KD$_{\text{dino}}\downarrow$ \\
+    \midrule
+    Pretrained (Trellis) & 86.78 & 9.23 & 66.82 & 0.73 \\
+    Photo3D & 86.89 & \textbf{9.09} & 76.98 & \textbf{0.70} \\
+    OREO (Ours) & \textbf{87.12} & 9.12 & \textbf{62.54} & \textbf{0.70} \\
+    w/o Noise Update & 86.83 & 9.39 & 67.41 & 0.72 \\
+    \bottomrule
+  \end{tabular}
+\end{table}
+
+The results show that OREO improves CLIP and FD$_{\text{dino}}$ over the pretrained Trellis backbone and Photo3D, while remaining competitive on FD$_{\text{inc}}$ and KD$_{\text{dino}}$.
+The degradation of the w/o Noise Update variant further supports the role of dynamic noise update beyond the in-the-wild evaluation split.
```

## 术语与排版决策

- 使用 `Pretrained (Trellis)` 而不是 rebuttal 里的 `Trellis`，以对齐正文 Table 1 的 `Pretrained` 口径，同时保留 backbone 来源。
- 使用 `OREO (Ours)`，对齐正文 Table 1。
- 使用 `w/o Noise Update`，对齐消融表里的变体名；不写 `OREO (w/o noise update)`，避免同一个变体出现两套大小写和前缀。
- Toy4K 表只放在 Supplementary；正文不新增 Table 2，避免影响正文页数和后续消融表编号。
- 正文不写过强结论，只做短指引；详细结论留给 Supplementary。

## 验证

执行后编译 `camera_ready.tex` 与 `supplementary.tex`，检查正文 Supplementary 指引、Supplementary 中 `Table~\ref{tab:toy4k}` 引用、表格编号、overfull/underfull warning，以及正文页数是否保持稳定。

## 状态

**当前阶段**: Done
