# Session Handoff: Refine Reviewer #1 Rebuttal

## 任务目的

对 `rebuttal.tex` 中 Reviewer #1 的四个问题进行润色与加强。

## 本次执行内容（2026-05-10 下午）

本 session 完成了 R1 Q1–Q4 的全面改写，具体如下：

### R1 Q1（小规模数据集评估）
- 直接指出 Objaverse 是 Trellis 的训练集，用于评估会产生不公平优势
- 改为使用 Toy4K（Trellis 官方测试集），引用 `Table~\ref{tab:toy4k}` 和 Reviewer #2 Q3
- 结尾说明 margin 较小的原因（in-distribution），并强调 OREO 目标是 out-of-domain

### R1 Q2（缺少 distillation baseline 对比）
- 标题改为 "Comparison with distillation baselines."
- 明确指出 Magic3D / ProlificDreamer 是 text-to-3D、optimization-based，与 OREO 的 image-to-3D learning-based 设定不可直接对比
- 引用正文 Sec. 4.3 / Fig. 5 中的 DMD ablation，说明 score distillation 在此设定下效果更差

### R1 Q3（Human evaluation）
- 原 Q3（failure case）内容删除，改为 human preference study 结果
- 20名参与者，100个测试样本，评估多视角一致性与输入保真度
- OREO 42%，Photo3D 36%，Trellis 22%

### R1 Q4（计算开销）
- 原 Q4 拆分：human study 移到 Q3，计算开销单独成 Q4
- 9-step image editing 占每个 training iteration 的 81%
- 解决方案：async service（vllm-omni）+ 与 next-batch rollout 重叠，降至 45%，性能基本不变

### 其他
- `\showreviewtagsfalse`：关闭了 PDF 中的红字/蓝字 tag 显示
- 始终保持 2 页编译成功

## 参考位置

| 文件 | 位置 | 说明 |
|------|------|------|
| `rebuttal.tex` | L40–L51 | R1 Q1–Q4 全部回答 |
| `rebuttal.tex` | L17 | `\showreviewtagsfalse` 开关 |
| `main.tex` | L500, L535–540 | DMD ablation 描述（Sec. 4.3） |

## 下一步任务

用户将从头过一遍三个 reviewer 的 rebuttal 全文，检查内容是否一致、逻辑是否通顺，然后进行排版调整。

重点关注：
- R1 Q3 的 failure case 问题是否需要在某处补一句（目前只在 general response 提及）
- R3 Q4 的 prompt 描述与 R1 Q2 的 DMD 说明是否存在矛盾或重复
- `\showreviewtagstrue/false` 在提交前确认开关状态（提交时建议关闭）
