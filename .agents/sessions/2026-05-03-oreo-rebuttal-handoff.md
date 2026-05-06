# Session Handoff: OREO Rebuttal Planning

## 任务目的

本 session 主要处理 OREO 论文的 OpenReview 评审结果，先读取三位 reviewer 的截图，整理核心问题和 rebuttal 策略，然后把旧的 `rebuttal.tex` 模板替换成 OREO 的一页文字版 rebuttal 初稿。

## 执行内容

- 确认三张 review 截图位于 `review/Reviewer#1.png`、`review/Reviewer#2.png`、`review/Reviewer#3.png`。
- 读取三位 reviewer 意见，确认分数为 `4 / 4 / 3`，其中 Reviewer #3 为 Borderline Reject 且明确表示 rebuttal 充分会考虑提高分数。
- 总结共同问题：public benchmark / dataset、stronger baselines、qualitative evidence、method clarity、computational overhead、Qwen failure cases。
- 创建并多次更新 rebuttal 计划文件：`.cursor/plans/oreo_rebuttal_plan_9b9067e6.plan.md`。
- 从 `main.tex` 确认 ECCV 2026 与 Paper ID `153`。
- 按计划改写 `rebuttal.tex`：删除旧 ScaleDreamer 图表、表格和 ASD/VSD 内容，写入 OREO 标题、metadata 和逐 reviewer Q&A。
- 搜索确认 `rebuttal.tex` 中无 `ScaleDreamer`、`ASD`、`VSD`、旧图表引用残留。
- 尝试用 LaTeX 编译，但当前环境没有 `latexmk`、`pdflatex`、`xelatex`、`lualatex` 或 `tectonic`；`ReadLints` 未发现 linter 错误。

## 调试经验

- `ReadFile` 可以直接 OCR/读取 reviewer 截图内容，但并行读取三张图片时曾被中断，后续单张或两张读取成功。
- 删除并重建 `rebuttal.tex` 后，曾出现新内容后面残留旧模板的情况；后来用 patch 删除重复旧段落，并用 `rg` 验证旧内容清理干净。
- 本机命令行环境没有可用 LaTeX 编译器，不能依赖编译结果判断 rebuttal 是否严格一页。

## 参考代码


| 文件                                                  | 关键位置              | 说明                                                                                                                                      |
| --------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `review/Reviewer#1.png`                             | 整张截图              | Reviewer #1，Borderline Accept，重点 concern 是 dataset、baseline、human eval、Qwen failure、compute。                                            |
| `review/Reviewer#2.png`                             | 整张截图              | Reviewer #2，Borderline Accept，重点 concern 是 related work、qualitative results、dataset details、figure readability。                         |
| `review/Reviewer#3.png`                             | 整张截图              | Reviewer #3，Borderline Reject，重点 concern 是 multi-view qualitative、ablation clarity、Eq. 7/negative source guidance、compute、Qwen prompts。 |
| `main.tex`                                          | ECCV package line | 包含 `\usepackage[review,year=2026,ID=153]{eccv}`，用于确认会议和 paper ID。                                                                       |
| `rebuttal.tex`                                      | 全文件               | 当前 OREO rebuttal 初稿，77 行，无图表，按 reviewer 分节。                                                                                             |
| `.cursor/plans/oreo_rebuttal_plan_9b9067e6.plan.md` | 全文件               | 当前计划与优先级记录；后续不要无故改动，除非用户要求更新计划。                                                                                                         |


## 最终方案

最终采用“一页文字版 rebuttal”策略：不放新图表，不编造尚未完成的实验数字，重点用明确的 revision 承诺回应 reviewers。结构为 Reviewer #1 四个 Q、Reviewer #2 三个 Q、Reviewer #3 四个 Q，并把 P2 次要问题合并到相关 Q 的末尾。

## 下一步任务

下个 session 需要确定实验任务优先级，尤其是在 rebuttal 时间有限、当前尚无新增实验结果的情况下，决定哪些实验最值得先做、哪些只写承诺或放 supplement。

## 初步方案

- 先围绕三类最高优先级实验排序：public benchmark/second dataset、high-resolution multi-view qualitative、Eq. 7/FlowEdit/negative source guidance 可视化。
- 明确每个实验的产出形式：rebuttal 正文一句话、revision 表格、supplement 图、或仅作为承诺。
- 评估可行性：需要多少 GPU 时间、是否已有渲染结果、是否能快速做小规模 sanity check。
- 优先服务 Reviewer #3 的提分点，同时避免 Reviewer #1/#2 觉得 dataset 和 baseline concern 被忽略。
- 如果时间很紧，建议形成 “must-run / nice-to-have / promise-only” 三档实验清单。

