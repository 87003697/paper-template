# Session Handoff: Rebuttal Coverage Tags and R3 Refinement

## 任务目的
本 session 主要为 `rebuttal.tex` 增加临时 coverage 标记，帮助对照 `review/Reviewer#*.png` 检查每个 reviewer 的原始 bullet 是否已经被 rebuttal 覆盖。用户下一步要重点认真回答 Reviewer #3 的问题，并 refine 当前 rebuttal。

## 执行内容
- 根据 `.agents/sessions` 既有日志梳理了 rebuttal 中已处理和未充分 review 的问题，确认 R3 仍是最关键摇摆票。
- 检查并修复 LaTeX Workshop 编译问题：当前项目新增 `.vscode/settings.json`，显式使用 `/Library/TeX/texbin/latexmk`。
- 在 `rebuttal.tex` preamble 中加入 `\reviewtag{...}` 宏，用 `\showreviewtagstrue` / `\showreviewtagsfalse` 控制 PDF 中临时标记显示或隐藏。
- 按 `review/Reviewer#*.png` 的原始 bullet 编号体系为当前 11 个 rebuttal Q&A 添加 coverage tags，如 `R1-Maj1`、`R2-Sug2`、`R3-Clar1`。
- 在每个 `To Reviewer #...` 后增加 `\reviewstatus{...}` 临时状态行，显示该 reviewer 还有哪些问题未回答或需检查。
- 用户指出 `\reviewstatus` 显示和 Q 标题重叠；已改成 `\parbox{\linewidth}` 并去掉后续负间距，重新编译正常。
- 多次用 `/Library/TeX/texbin/latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf rebuttal.tex` 编译，`rebuttal.pdf` 正常生成。

## 调试经验
- `rebuttal.tex` 本身能用命令行编译；LaTeX Workshop 失败的主要原因是 Cursor GUI 环境可能找不到 TeX 工具链路径。
- 之前日志里提到的 TinyTeX 路径 `/Users/zhiyuanma/Library/TinyTeX/bin/universal-darwin/latexmk` 当前不存在；实际可用的是 `/Library/TeX/texbin/latexmk`。
- 临时状态行如果使用 `\par\vspace{-1mm}` 并紧跟 `\vspace{-2mm}`，容易和下一行 Q 标题重叠；当前用 `\parbox` 和小正间距更稳定。
- 当前 tag/status 是调试用内容，最终提交 rebuttal 前只需把 `\showreviewtagstrue` 改为 `\showreviewtagsfalse`，PDF 中的 tag 和 status 都会隐藏。

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `rebuttal.tex` | preamble 第 15--18 行 | `\reviewtag{}` 与 `\reviewstatus{}` 宏；当前开关为 `\showreviewtagstrue`。 |
| `rebuttal.tex` | Reviewer #3 Q1--Q4 | R3 相关回答当前覆盖 `R3-Qual1`、`R3-Qual2`、`R3-Clar1`、`R3-Clar2`、`R3-Clar3`、`R3-Min1`、`R3-Min2`。 |
| `review/Reviewer#3.png` | Major Weaknesses | R3 的核心 concern：qualitative evidence、ablation color issue、figure quality、Eq.7/negative guidance、VRAM、Qwen prompts、typos。 |
| `.vscode/settings.json` | LaTeX Workshop 配置 | 项目级 recipe，指向 `/Library/TeX/texbin/latexmk`。 |
| `.agents/sessions/2026-05-03-oreo-rebuttal-priority.md` | P0/P1 优先级 | 记录 R3 是摇摆票，以及 R3 Q1/Q3/Q4 的待完成重点。 |
| `.agents/sessions/2026-05-04-r3q2-rebuttal-handoff.md` | 全文件 | R3 Q2 已完成的解释逻辑和数据，不建议大改。 |

## 最终方案
采用可隐藏的 LaTeX 宏标记方案，而不是直接写死普通文本。这样当前 PDF 可以显示 coverage 信息辅助 review，最终提交时用单个开关隐藏所有标记，不需要逐处删除。原始 review bullet 编号比 rebuttal 内部 Q 编号更适合查漏补缺。

## 下一步任务
认真回答 Reviewer #3 的问题，并 refine `rebuttal.tex`，优先增强 R3 Q1、Q3、Q4 的说服力，同时保持 R3 Q2 已确定的解释逻辑。

## 初步方案
- 先集中阅读 `review/Reviewer#3.png`、当前 `rebuttal.tex` 的 R3 Q1--Q4，以及 `.agents/sessions/2026-05-03-oreo-rebuttal-priority.md` 中 P0/P1 任务。
- R3 Q1：把 multi-view / side-view / supplement 的承诺写得更具体；如果已有图或 supplement，尽量从 “we will add” 改成 “we have added”。
- R3 Q3：补强 Eq. 7 / negative source guidance 的直观解释，最好明确说明 FlowEdit intermediate-step visualization 会展示什么，而不是只说会添加 visualization。
- R3 Q4：尽量补 wall-clock / VRAM 具体数值；同时加入更具体的 Qwen-Image-Edit prompt template 示例。
- 保持 `\reviewtag{}` 和 `\reviewstatus{}` 显示开启，边改边检查是否所有 R3 tags 都被实质性回答；最终提交前再切到 `\showreviewtagsfalse`。
