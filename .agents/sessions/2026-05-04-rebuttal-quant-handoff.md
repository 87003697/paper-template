# Session Handoff: Rebuttal 定量结果与写作风格更新

## 任务目的

本 session 继续修改 `rebuttal.tex`，重点是确定 rebuttal 开头的总述风格，并补入 Reviewer #1 / #2 关心的 human evaluation 和 public benchmark 定量结果。

## 执行内容

- 总结了当前 rebuttal 的整体风格：优先服务 R3 摇摆票，逐 reviewer Q&A，先承认问题再给解释/承诺，避免无把握的大数字承诺。
- 将开头感谢句改为更简洁的总述：强调 high-resolution visualizations、expanded related work、failure cases、editing-guidance limitations 和 computational overhead。
- 针对 Reviewer #1 的 human evaluation 要求，确定使用 pairwise preference 表格，而不是 MOS 或 overall preference。
- 写入 human evaluation 表格：OREO 相比 Trellis 在 Reference Fidelity / Texture Detail 上为 81% / 68%，相比 Photo3D 为 63% / 59%。
- 针对 Reviewer #1 / #2 的第二数据集要求，写入 full GSO dataset 定量结果：Trellis CLIP/DINO 为 0.6712 / 0.5915，OREO 为 0.6766 / 0.5972。
- 将 GSO 结果解释为 in-domain public benchmark 上的 consistent improvement，同时说明 OREO 的重点是 out-of-domain concept design images 上更大的质量缺口。
- 将 Reviewer #2 Q3 改为引用 Reviewer #1 Q1，避免重复完整 GSO 数字和解释。
- 多次用 TinyTeX 编译 `rebuttal.tex`，确认 `rebuttal.pdf` 可正常生成。

## 调试经验

- 直接运行 `latexmk -pdf rebuttal.tex` 会失败，因为 shell `PATH` 没有 TinyTeX；需要使用：
`PATH="/Users/zhiyuanma/Library/TinyTeX/bin/universal-darwin:$PATH" "/Users/zhiyuanma/Library/TinyTeX/bin/universal-darwin/latexmk" -g -synctex=1 -interaction=nonstopmode -file-line-error -pdf rebuttal.tex`
- `latexmk` 失败后可能记住上一次失败状态，需要加 `-g` 强制重编译。
- `pdflatex` 下不建议在 `.tex` 里直接写 Unicode 箭头 `→`，应使用 `$\rightarrow$`。

## 参考代码


| 文件                      | 关键位置            | 说明                                                                      |
| ----------------------- | --------------- | ----------------------------------------------------------------------- |
| `rebuttal.tex`          | 开头第 28 行        | 当前总述句已改为简洁版本，不再在开头提 public benchmark。                                   |
| `rebuttal.tex`          | Reviewer #1 Q1  | full GSO dataset 定量结果和 in-domain / out-of-domain 解释。                    |
| `rebuttal.tex`          | Reviewer #1 Q4  | human preference 表格，回应 human evaluation 要求。                             |
| `rebuttal.tex`          | Reviewer #2 Q3  | 引用 Reviewer #1 Q1 的 GSO 结果，回应 second dataset 要求。                        |
| `review/Reviewer#1.png` | Official review | 数据集、baseline、human eval、failure case、compute overhead 是主要 concern。      |
| `review/Reviewer#2.png` | Official review | related work、高清 qualitative、dataset details、second dataset 是主要 concern。 |


## 最终方案

human evaluation 使用 2x2 pairwise preference 表格，只保留 Reference Fidelity 和 Texture Detail 两个维度，直接对应概念设计图生 3D 的保真度 claim。GSO 结果只作为 public benchmark 的补充证据，不夸大提升幅度；核心解释是 GSO 多为 Trellis in-domain 的日常扫描物体，而 OREO 主要解决 out-of-domain concept design images 的保真度缺口。

## 下一步任务

明天继续修改剩余 rebuttal 内容，重点处理 Reviewer #3 的提分项，以及尚未完全落地的 compute overhead、failure cases、Qwen prompt templates、FlowEdit / negative guidance 解释和高清可视化承诺。

## 初步方案

- 优先检查 `rebuttal.tex` 是否已经超过篇幅预期，必要时压缩 R1/R2 已完成段落，为 R3 留空间。
- 完成 R3 Q1：把 high-resolution multi-view / zoom-in visualizations 的承诺写得更具体，若已有图则改成 `we have added`。
- 完成 R3 Q3：补强 Eq.~7 / negative source guidance 的解释，并与 FlowEdit intermediate-step visualization 呼应。
- 完成 R3 Q4：填入 wall-clock / VRAM profiling 数字，并补充 Qwen-Image-Edit prompt template 示例。
- 回头统一术语：Conceptual Design Dataset、full GSO dataset、Trellis、Photo3D、Qwen-Image-Edit、FlowEdit 的大小写和表达要一致。

