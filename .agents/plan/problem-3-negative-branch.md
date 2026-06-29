---
name: problem-3-negative-branch
overview: 为 camera-ready 的 Problem 3 制定改动计划：沿用 rebuttal 中对 negative source branch 的保守解释口径，在正文精炼说明其 auxiliary regularizer 作用，并在 Supplementary 中加入轨迹对比图和对应分析。
todos:
  - id: main-negative-explanation
    content: 在 `camera_ready.tex` 的 `Eq.~\ref{eq:red_diff_velocity}` 后保留原解释并追加 1 句 negative source branch / Supplementary visualization 说明
    status: completed
  - id: supp-negative-section
    content: 在 `supplementary.tex` 新增 negative source guidance 轨迹分析小节与 `comparison_grid.png` 图
    status: completed
  - id: overview-and-plan-update
    content: 更新 Supplementary overview 与 `.agents/plan/camera-ready.md` 中 Problem 3 的落地状态说明
    status: completed
  - id: compile-check
    content: 编译主文和附录，检查新增引用、图路径与编号
    status: completed
isProject: false
---

# Problem 3: Negative Source Branch 改动计划

## 目标

补强 Reinforced Editing 中 negative source branch 的可解释性：正文只在 [camera_ready.tex](camera_ready.tex) 的 `Sec. 3.3` 公式附近保留原有解释并追加 1 句机制说明，沿用 rebuttal 的核心口径，即 negative source branch acts as an auxiliary regularizer for stabilizing reference-guided editing；附录在 [supplementary.tex](supplementary.tex) 中加入 `figures_rebuttal/comparison_grid.png` 的轨迹对比图与分析，回应审稿人对该分支作用的直观性疑问。

## 关键发现

- [camera_ready.tex](camera_ready.tex) 的落点已经存在：`Constructing On-the-fly Pseudo-GTs via Reinforced Editing` 中 `Eq.~\ref{eq:red_diff_velocity}` 后目前只有一句解释：

```tex
By pushing away from the unconditional score via $-w$ and pulling towards the reference-conditioned score via $w$, this mechanism effectively reinforces the visual details of $c^{\texttt{ref}}$ while neutralizing structural drift, ensuring the editing variable $x^{\texttt{edit}}$ remains geometrically aligned with $x^{\texttt{src}}$.
```

- [supplementary.tex](supplementary.tex) 当前只有 `Overview`、`Human Preference Study Protocols`、`Implementation and Dataset Details`、`Limitations and Failure Cases`，尚无 Reinforced Editing / negative branch 的附录小节。
- `figures_rebuttal/comparison_grid.png` 已存在，内容是 `w/o neg src guidance` 与 `w/ neg src guidance (Ours)` 在 `t=0,3,6,8,t_final` 的轨迹对比，可直接作为 Problem 3 的核心可视化素材。
- [rebuttal.tex](rebuttal.tex) 中 R3 Q3 的最终解释是：“The negative source branch in Eq.~7 acts as an auxiliary regularizer, stabilizing reference-guided editing.” 图像分析只指出移除它会导致 color over-saturation、insufficient structural changes，以及 helmet 上的 “A” 缺失。
- 之前的 R3 Q3 handoff 明确记录：不要写成 “avoid copying source appearance”，也不宜使用过长的 push-away / pull-toward 公式解释、pose/viewpoint drift、over-align 或 local optimum 等说法；更稳的分析是 unstable global color changes and weaker local structures。
- 图像放置决策：`figures_rebuttal/comparison_grid.png` 放在 Supplementary，而不是正文。理由是该图主要服务 Eq.~7 / negative source branch 的机制解释，不是 end-to-end 主结果；正文页数已经紧张，Problem 3 正文只需追加 1 句强引用指向 Supplementary，既能兑现 rebuttal 中 “expand Sec.~3.3 with this visualization” 的承诺，也能把正文空间留给 Toy4K、人评、limitations 和最终控页。
- 约束：不改 `main.bib`、不动模板文件；正文空间紧张，正文解释必须克制，详细分析放 Supplementary。

## 实施步骤（含论文 TeX code diff）

1. 更新 [camera_ready.tex](camera_ready.tex) 的 `Sec. 3.3` negative branch 解释。

   保留 `Eq.~\ref{eq:red_diff_velocity}` 后现有的一句解释，只在其后追加 1 句更清楚但保守的英文说明，重点覆盖：
   - 不重写已有 push-away / pull-toward 解释，减少 Method 文本扰动；
   - 追加句把现有机制解释和 Supplementary 轨迹图连接起来；
   - 追加句只点出 rebuttal 中已经使用过的现象：removing the branch leads to color over-saturation and weaker local structures；
   - 避免写 “copy source appearance”、over-align、local optimum、semantic hallucination 或过强 pose/viewpoint drift 归因。

   **中文修改意图**：正文保留 `Eq.~\ref{eq:red_diff_velocity}` 后的原句，只追加一句引用 Supplementary 轨迹图。这样既不推翻已有 Method 解释，又能对齐 rebuttal：negative source branch 的辅助正则化效果可以通过附录中的 color over-saturation / weaker local structures 现象来直观看到。

   **英文版 TeX diff（GitHub 红绿风格：`-` 为删除，`+` 为新增）**：

   ```diff
   @@ Constructing On-the-fly Pseudo-GTs via Reinforced Editing — append Supplementary visualization sentence after Eq.~\ref{eq:red_diff_velocity}
    \begin{equation}
        \label{eq:red_diff_velocity}
        \tilde{v} = v_\phi^{w}(x^{\texttt{tgt}}(t); t, c^{\texttt{ref}}) - v_\phi^{-w}(x^{\texttt{src}}(t); t, c^{\texttt{ref}}),
    \end{equation}
    By pushing away from the unconditional score via $-w$ and pulling towards the reference-conditioned score via $w$, this mechanism effectively reinforces the visual details of $c^{\texttt{ref}}$ while neutralizing structural drift, ensuring the editing variable $x^{\texttt{edit}}$ remains geometrically aligned with $x^{\texttt{src}}$.
   +This auxiliary regularizing effect is further visualized in the Supplementary Material, where removing the branch leads to color over-saturation and weaker local structures such as the missing helmet mark.
    
    
    \textbf{Noise Update.}
   ```

2. 在 [supplementary.tex](supplementary.tex) 新增 Reinforced Editing 可视化小节。

   建议放在 `Overview` 之后、`Human Preference Study Protocols` 之前，新增：
   - `\section{Analysis of Negative Source Guidance}`
   - `\label{sec:negative_source_guidance}`
   - 一个 `figure*` 或普通 `figure`，引用 `figures_rebuttal/comparison_grid.png`。
   - 不在正文放图；正文只通过 `as visualized in the Supplementary Material` 进行交叉引用。

   **中文修改意图**：Supplementary 先在 `Overview` 里增加新小节入口，然后在 `Overview` 后新增 `Analysis of Negative Source Guidance`。这里放 rebuttal 已经使用过的 `comparison_grid.png`，完整展示有/无 negative source guidance 的 intermediate trajectory。

   **英文版 TeX diff（Overview 入口，GitHub 红绿风格：`-` 为删除，`+` 为新增）**：

   ```diff
   @@ Overview — add negative source guidance section to supplementary overview
    \section{Overview}
    In this supplementary material, we provide:
    \begin{itemize}
   +  \item Section~\ref{sec:negative_source_guidance}: Trajectory visualization and analysis of negative source guidance in Reinforced Editing.
      \item Section~\ref{sec:human_study_details}: Comprehensive protocols and setup for our human preference study.
      \item Section~\ref{sec:implementation_details}: Detailed training/inference computational overhead, prompts, and dataset statistics.
      \item Section~\ref{sec:limitations_failure}: Additional discussion on failure cases and limitations.
    \end{itemize}
   ```

   **英文版 TeX diff（新增小节与图，GitHub 红绿风格：`-` 为删除，`+` 为新增）**：

   ```diff
   @@ Supplementary body — insert negative source guidance analysis before human study protocols
    \end{itemize}
    
    % ---------------------------------------------------------------
   +\section{Analysis of Negative Source Guidance}
   +\label{sec:negative_source_guidance}
   +
   +\begin{figure}[t]
   +  \centering
   +  \includegraphics[width=\linewidth]{figures_rebuttal/comparison_grid.png}
   +  \caption{\textbf{Editing trajectories with and without negative source guidance.}
   +  Starting from the same rendered source view $x^{\texttt{src}}$ and reference image $x^{\texttt{ref}}$, we visualize intermediate editing states and the final output.
   +  Without negative source guidance, the trajectory exhibits unstable global color changes and weaker local structures.
   +  With negative source guidance, Reinforced Editing stabilizes the reference-guided trajectory while preserving local details such as the helmet mark.}
   +  \label{fig:negative_source_guidance}
   +\end{figure}
   +
   +Fig.~\ref{fig:negative_source_guidance} illustrates the role of the negative source branch in the Reinforced Editing differential velocity defined in the main paper.
   +When the branch is removed, the editing trajectory becomes less stable: colors are rapidly over-saturated, and local structures become weaker, as shown by the missing ``A'' on the helmet.
   +With the negative source branch, the reference-guided enhancement proceeds more smoothly and maintains more stable local markings throughout the trajectory.
   +This supports our use of the branch as an auxiliary regularizer for producing reliable pseudo-GTs during closed-loop 3D optimization.
   +
   +% ---------------------------------------------------------------
    \section{Human Preference Study Protocols}
    \label{sec:human_study_details}
    Placeholder for human study protocols.
   ```

3. 为附录图写 caption 与正文分析。

   Caption 需要明确列含义：`x^{\texttt{src}}`、`x^{\texttt{ref}}`、intermediate editing steps、final output；行含义：without negative source guidance vs with negative source guidance。分析文字控制在一段左右，和 rebuttal 保持一致：无 negative source guidance 时，轨迹出现 unstable global color changes / color over-saturation，并削弱局部结构，例如 helmet 上的 “A” 未能稳定形成；加入 negative source guidance 后，reference-guided editing 更稳定，局部标识和整体颜色变化更受控。不要把图解读为统计性提升，也不要扩展到当前图无法支撑的 viewpoint / pose drift 结论。

4. 更新 [supplementary.tex](supplementary.tex) 的 `Overview` 列表。

   增加一项指向新小节，例如：`Section~\ref{sec:negative_source_guidance}: trajectory visualization and analysis of negative source guidance in Reinforced Editing.`

5. 更新 [camera-ready.md](.agents/plan/camera-ready.md) 的 Problem 3 状态说明。

   如果你确认执行，实施后把 Problem 3 的正文/附录分工从粗略描述更新为已落地内容，并将 todo `problem-3-negative-branch` 从 `pending` 改为 `completed`。注意只改该 plan 文件对应条目，不顺手改其他问题。

   **中文修改意图**：执行完成后，把总计划中 Problem 3 的 todo 改为 completed，并把 Problem 3 的正文/附录分工从粗略承诺更新为已落地描述。这里不改其他 Problem，也不重写整份 camera-ready 总计划。

   **英文版 Markdown diff（GitHub 红绿风格：`-` 为删除，`+` 为新增）**：

   ```diff
   @@ frontmatter todos — mark Problem 3 completed after implementation
      - id: problem-3-negative-branch
        content: 在 camera_ready.tex 中补充 negative source branch 理论解释（追加 1 句），并在 supplementary.tex 中插入轨迹对比图与分析
   -    status: pending
   +    status: completed
    
   @@ 问题 3：Negative Source Branch 解释与轨迹可视化
    - **正文与附录分工**：
      - **正文（`camera_ready.tex`）**：
   -    - 在 `Sec. 3.3` 的公式 `red_diff_velocity` 附近，补充对 negative source branch 物理意义的简洁文字解释。**控制在 3-4 句内**以节省篇幅：“The negative source branch pushes the latent representation away from unconditioned states, suppressing semantic hallucinations and locking the underlying geometric structure during 2D guidance.”
   +    - 已在 `Sec. 3.3` 的公式 `red_diff_velocity` 后保留原解释并追加 1 句说明：negative source branch 的 auxiliary regularizing effect 可在 Supplementary 轨迹图中直观看到；移除该分支会出现 color over-saturation / weaker local structures。
      - **附录（`supplementary.tex`）**：
   -    - 插入 `figures_rebuttal/comparison_grid.png`，并对有/无负引导的轨迹表现差异（如颜色过饱和、细节丢失、结构变化等）进行成因分析。
   +    - 已新增 `Analysis of Negative Source Guidance` 小节，插入 `figures_rebuttal/comparison_grid.png`，分析有/无 negative source guidance 的 intermediate editing trajectory，重点解释 color over-saturation、unstable global color changes、weaker local structures，以及 helmet “A” 缺失。
   ```

6. 验证。

   编译 `camera_ready.tex` 与 `supplementary.tex`，检查：
   - `Eq.~\ref{eq:red_diff_velocity}` 周边无语法错误；
   - 新增 `Fig.~\ref{fig:negative_source_guidance}` 引用正常；
   - Supplementary 不直接引用主文公式 label，避免独立编译时 undefined reference；
   - `comparison_grid.png` 路径可被 LaTeX 找到；
   - Supplementary 的 section / figure 编号保持 `S` 前缀。

## 预期改动范围

- [camera_ready.tex](camera_ready.tex)：约 +1 行净增长，保留已有解释并追加一句 Supplementary visualization 引用，不新增图表。
- [supplementary.tex](supplementary.tex)：约 +18 到 +28 行，新增小节、图和一段分析。
- [.agents/plan/camera-ready.md](.agents/plan/camera-ready.md)：约 +4 到 +8 行说明变更，并更新 Problem 3 todo 状态。

## 风险与取舍

- 正文若写得太长会加剧 14 页压力，所以正文只追加一句机制/附录引用，不放可视化图。
- 如果正文直接放 `comparison_grid.png`，R3 的直觉解释会更显眼，但会占用接近半栏到一栏空间，并与后续 Toy4K table、人评结论、limitations 和最终控页计划竞争版面。当前更稳的取舍是：正文强引用 Supplementary，附录放完整图。
- 附录图只展示一个样例轨迹，适合解释机制，但不应过度声称统计性提升；文字中应使用 qualitative / illustrates / tends to，而不是 claims broad quantitative gains。
- 不需要新增引用，也不需要改 `main.bib`。
