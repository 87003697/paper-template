# Session Handoff: Camera-Ready Neg-Src Figure & Spacing

## 对话 Transcript
`~/.claude-internal/projects/-Users-zhiyuanma-Desktop-OREO-ECCV-paper-template/fe510cb4-0176-4fe4-9777-63c3d55c4e07.jsonl`

## 前序 Session
- `.agents/sessions/2026-06-23-related-work-camera-ready.md` — Related Work 三段重构（Problem 1 完成）。

## 相关 Plan
- `.agents/plan/camera-ready.md` — camera-ready 总计划。本 session 完成 Problem 2-5, 7；Problem 6, 8 仍 pending。
- `.agents/plan/problem-2-method.md` — GAN loss 引入计划。
- `.agents/plan/problem-3-negative-branch.md` — Negative source branch 补充说明。
- `.agents/plan/problem-4-toy4k.md` — Toy4K 评估策略（放入 Supplementary）。
- `.agents/plan/problem-5-human-study.md` — 人评协议。
- `.agents/plan/problem-7-failure-case.md` — Limitations/Failure case。

## 任务目的
为 ECCV camera-ready 版本进行多处修改：添加 Teaser 图、在 Method 中引入 GAN loss、补充 negative branch 分析、加入 Toy4K/Human study/Limitations，并将 Supplementary 从占位填充为实质内容。本次 session 额外完成了将 negative source guidance 轨迹图从 Supplementary 提升到正文 Sec. 3.3，并修复了因此导致的 Introduction 溢页问题。

## 执行内容
- 确认 rebuttal 材料中可用的可视化资源（negative source guidance 轨迹图 `comparison_grid.png`）
- 在正文 Sec. 3.3 中将原先指向 Supplementary 的红字句改为引用新 Figure
- 在 Sec. 3.3 紧跟 Eq. 7 讨论段后插入 `fig:neg_src_guidance` figure 环境
- 与用户反复讨论 caption 风格：从 4 句压缩到 2 句，去除括号引用
- 修复因新图导致 Introduction contribution 3 溢出到第 3 页的问题
- 尝试多组 vspace 方案，用户反馈"缩得太多了"后回退到温和版

## 代码改动

### Commits
无新 commit（所有改动均为 unstaged）。前序 commit `1209eab` 已包含 teaser/GAN loss/supplementary 等内容。

### 文件详情

**`camera_ready.tex`**（+11/-2 行 diff vs HEAD）— 本次 session 的增量改动

- **Teaser 图间距**（L95）：在 `\label{fig:teaser}` 后添加 `\vspace{-2mm}`，防止 Introduction contributions 列表溢出到第 3 页
- **Enumerate 间距**（L118）：`\begin{enumerate}\setlength{\itemsep}{0pt}` 进一步收紧 contribution list
- **Sec. 3.3 引用句替换**（L268）：
  - 旧：`\textcolor{red}{This auxiliary regularizing effect is further visualized in the Supplementary Material, where removing the branch leads to color over-saturation and weaker local structures such as the missing helmet mark.}`
  - 新：`\textcolor{red}{This auxiliary regularizing effect is further visualized in Fig.~\ref{fig:neg_src_guidance}, where removing the branch leads to progressive color over-saturation and degraded local structures, while our full formulation stabilizes the trajectory and preserves fine details.}`
- **Sec. 3.3 新增 Figure**（L270-277）：
  ```latex
  \begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{figures_rebuttal/comparison_grid.png}
    \caption{\textcolor{red}{\textbf{Visualization of editing trajectories with and without negative source guidance.}
    Without the negative source branch, the editing trajectory progressively exhibits color over-saturation and degraded local structures. With the branch, the trajectory remains stable and fine-grained details are well preserved.}}
    \label{fig:neg_src_guidance}
  \end{figure}
  ```

**`supplementary.tex`** — 无本次 session 改动（前序 session 已完成所有 supplementary 扩写）

## 用户决策与偏好
- Caption 必须精炼：2 句为佳（标题句 + 正文句），不要 4 句
- Caption 中不使用括号标注如 "(top row)" / "(bottom row, ours)"
- 正文引用句以 "This auxiliary regularizing effect is further visualized in Fig.~..." 开头
- 所有 camera-ready 改动必须用 `\textcolor{red}{...}` 标红
- 间距调整不要太激进——用户偏好微调而非大幅压缩

## 调试经验
- 现象：新增 `fig:neg_src_guidance` 后首次编译出现 undefined reference。
  原因：LaTeX 正常行为，新 label 需要两次编译。
  解法：运行第二次 `pdflatex` 即可。
- 现象：新图导致 Introduction 第 3 条 contribution 溢出到第 3 页。
  原因：新图占据页面空间，LaTeX 排版自动换页。
  解法：先尝试 teaser `\vspace{-2mm}` + `\vspace{-3mm}` + `\vspace{-1mm}` + itemsep——用户反馈太紧。最终方案：仅保留 teaser 底部 `\vspace{-2mm}` 和 enumerate 的 `\setlength{\itemsep}{0pt}`。用户尚未最终确认是否满意。

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `camera_ready.tex` | L460-475 | Dataset setup 段，含多个 TODO 需填入实际数字 |
| `supplementary.tex` | L119-200 | Implementation Details，大量 TODO 待填 |
| `.agents/plan/camera-ready.md` | problem-6-overhead-dataset | 下一步主要工作 |
| `.agents/plan/problem-6-compuation-and-dataset.md` | 全文 | 计算开销与数据集统计的详细计划 |

## 最终方案
将 `figures_rebuttal/comparison_grid.png` 同时保留在正文 Sec. 3.3 和 Supplementary 中。正文给出 2 句精炼 caption + 1 句引用讨论句；Supplementary 保留更详细的分析段落。通过 teaser 底部 -2mm 和 enumerate itemsep=0pt 两处微调解决页面溢出，避免过度压缩。

## 下一步任务
用户表示"接下来我们还会添加其他改动"。camera-ready plan 中仍有两个 pending 问题：
1. **Problem 6**（overhead-dataset）：填充正文与 supplementary 中的 TODO 占位（训练数据量、过滤条件、评估集大小、计算开销数据、editing prompt、判别器超参数）
2. **Problem 8**（page-limit）：将大图迁移至 supplementary、正文精简至 14 页

## 初步方案
- Problem 6 需要用户提供具体数字（训练集图片数量、GPU 型号与时间、编辑 prompt 文本等）；AI 可协助组织到 LaTeX 中
- Problem 8 需先编译确认当前页数，再决定迁移哪些图表到 supplementary
- 间距问题可能在后续改动中自然解决（如迁移大图后页面空间充裕）
- 用户可能还有额外改动需求（如新图、reviewer comment 回应等），保持灵活
