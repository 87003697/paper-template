# Session Handoff: Figure Layout in rebuttal.tex

## 目标

在 1 页限制内，将 Figure 1 放到第一页**左栏顶部**、Figure 2 放到第一页**右栏顶部**。

## 当前状态（已解决 ✓）

- 编译为 **1 页**（`pdflatex` 输出确认）
- **Figure 1 在左栏顶部，Figure 2 在右栏顶部** — 高分辨率截图确认
- **行号正确**：左栏 001–039 在左侧，右栏 040–075 在右侧，无错位

### 解决方案

- Figure 1：`figure[H]` 在 `\appendix` 后（L35–42），强制原位放置在左栏顶部
- Figure 2：`figure[t]` 在 R3 section 内部（L95–102），LaTeX 将其浮动到右栏顶部
- 文本自然流动：R2 从左栏底部开始（Q1 在左栏），Q2 开头处自然分栏到右栏
- **行号关键**：左栏延伸到 line 039（包含 R2 Q1 和 Q2 开头），与右栏高度接近，避免 `lineno` 的 `[switch]` 模式在不平衡栏间错误分配行号

### 行号问题的根因与修复

`cvpr.sty` 使用 `\RequirePackage[switch,mathlines]{lineno}`。`[switch]` 在 twocolumn 中按栏分配行号边距（左栏→左侧，右栏→右侧）。当两栏高度严重不平衡时，底部行号会被分配到错误的边距。

修复方法：不强制分栏（不用 `\vfill\newpage`），让文本自然流动，使两栏高度接近。

### 尝试过但失败的行号修复

| 方案 | 结果 |
|------|------|
| `\makeLineNumber` 使用 `\textwidth` 双边放置 | twocolumn 中 `\textwidth` 是页面全宽，镜像数字到错误位置 |
| `\rightlinenumbers` | 左栏行号出现在 gutter 中，与右栏文字重叠 |
| `\vfill\newpage` 强制分栏 | 右栏溢出或栏高不平衡导致行号错位 |

## 尝试过的图片布局方案

| 方案 | 结果 |
|------|------|
| 两个 `figure[t]` 均声明在文档最前面 | 1 页，但两图都在左栏 |
| `figure*[t]`（双栏并排 minipage） | 2 页（LaTeX 已知 bug） |
| `\usepackage{stfloats}` + `figure*[t]` | 仍然 2 页 |
| `\usepackage{dblfloatfix}` + `figure*[t]` | 仍然 2 页 |
| `figure[H]` + `\columnbreak` | `\columnbreak` 在 twocolumn 中未定义 |
| `\setcounter{topnumber}{1}` + 两个 `figure[t]` | 两图仍在左栏（float 栏归属由声明位置决定） |
| `\vfill\newpage` + `figure[H]` 在右栏开头 | 右栏溢出到 2 页（需激进缩减间距） |
| `\enlargethispage` | 被 cvpr 模板忽略 |
| **Figure 1 `[H]` 在文档开头 + Figure 2 `[t]` 在 R3 内部** | **✓ 1 页，行号正确** |

## 当前 rebuttal.tex 结构

```latex
\appendix
\vspace{-5mm}

\begin{figure}[H]           % Figure 1，[H] 强制在左栏开头
\includegraphics[width=\linewidth]{...mv_comparison...}
\end{figure}

% 001–004: general response
\section*{To Reviewer \#1}  % 005–031: R1 Q1–Q4

\section*{To Reviewer \#2}  % 032–039: R2 Q1 + Q2 开头（左栏底部）

% === 自然分栏点 ===       % Q2 继续, Q3, Table 在右栏 (040–045)

\section*{To Reviewer \#3}  % 046–075: R3 Q1–Q4

\begin{figure}[t]           % Figure 2，[t] 浮动到右栏顶部
\includegraphics[width=\linewidth]{...view_edit_traj...}
\end{figure}
```

## 参考位置

| 文件 | 位置 | 说明 |
|------|------|------|
| `rebuttal.tex` | L35–42 | Figure 1 (`fig:mv_comparison`)，`[H]` |
| `rebuttal.tex` | L95–102 | Figure 2 (`fig:neg_src_traj`)，`[t]` |
| `rebuttal.tex` | L12 | `\usepackage{float}` |
| `cvpr.sty` | L494 | `\RequirePackage[switch,mathlines]{lineno}` |

## 下一步

1. **Refine answers**：逐条打磨 R1/R2/R3 的回复内容，确保回答精准、有说服力
2. **排版整理**：微调间距、字号、表格格式等，确保页面利用率最大化且视觉美观
3. **注意**：修改文本内容时可能影响自然分栏位置，需重新编译确认 Figure 2 仍在右栏顶部、行号仍正确、仍为 1 页
