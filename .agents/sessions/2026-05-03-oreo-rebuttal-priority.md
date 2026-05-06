# Session Handoff: OREO Rebuttal Priority Decision

## 本 Session 目的

延续上一 session 的 rebuttal 初稿，本 session 的核心产出是**确定实验/补充材料的优先级**，以及**识别 rebuttal.tex 现有文字的风险点**，为下一 session 的具体执行做准备。

## 关键决策

### 分数与提分逻辑


| Reviewer  | 分数                    | 提分意愿                    |
| --------- | --------------------- | ----------------------- |
| R1 (Nz3M) | 4 — Borderline Accept | 未明确表态                   |
| R2        | 4 — Borderline Accept | 未明确表态                   |
| R3 (1rPv) | 3 — Borderline Reject | **明确说"rebuttal 充分会提分"** |


结论：**R3 是唯一的摇摆票**。把 R3 从 3 拉到 4，结果从 4/4/3 变成 4/4/4，accept 概率大幅提升。R1/R2 即使不改分，只要不降分也无妨。

### R3 的提分条件（原文：Weaknesses 全部条目）

R3 的关切里**没有** public benchmark——全部是：


| 编号   | 关切                                                      | 对应任务            | 是否需新实验        |
| ---- | ------------------------------------------------------- | --------------- | ------------- |
| Q1-a | 多视角结果太少，side view 太小                                    | 高清 multi-view 图 | 否，整理已有 render |
| Q1-b | Fig. 2/4 图像质量太差（压缩/非 SVG）                               | 换高质量图           | 否             |
| Q2-a | Fig. 6 第四行 w/o noise golem 颜色对齐反而更好，未解释                 | 文字澄清            | 否             |
| Q3   | Eq. 7/negative source guidance 解释混乱，需要 FlowEdit 中间步 viz | 机制图             | 小规模运行         |
| Q4-a | VRAM 开销具体是多少？                                           | 一个实测数字          | 需 profiling   |
| Q4-b | Qwen/NanoBanana 的 prompt 模板是什么？                         | 几行文字示例          | 否             |


**六件事没有一件需要大规模重新训练。**

### Public Benchmark 的风险

- R1 强烈要求在 Objaverse 上验证，R2 也提到 second dataset。
- **但 Objaverse 里大量是普通对象（椅子、车、动物），pretrained Trellis 在这类数据上已经不差，OREO 提升空间天然偏小。如果结果平淡，写进 rebuttal 反而是负分。**
- 建议策略：不在 rebuttal 中承诺具体数字，改为说明"我们选择了 [ABO / Objaverse 高细节子集]，preliminary results will be included in the revision"，等 sanity check 结果出来后再决定是否写数字。

## 优先级清单

### P0（直接对应 R3 提分，所有任务本身不依赖大规模训练）

1. **P0-A：高清多视角 qualitative 图**
  - 目标：2–3 个样例，front/side/back 三视角 + zoom-in 纹理细节
  - 产出：supplement 图；rebuttal R3 Q1 改为"we have added high-resolution multi-view visualizations in the supplementary material"
  - 前置：需从 outputs/ 或本地目录找回已有 render；若没有需小规模推理
2. **P0-B：Eq. 7 / FlowEdit 中间步 / negative source guidance 机制图**
  - 目标：一张机制对比图，含 source rendering → 中间 step t_i → target edit，以及 w/ vs w/o negative guidance 的对比
  - 产出：supplement 图或 revision Sec. 3.3 插图；rebuttal R3 Q3 加一句"we have added a step-by-step visualization"
  - 前置：在固定样例上运行 FlowEdit 并 dump 中间 x_edit 的可视化；代码改动量小
3. **P0-B'：解释 w/o noise golem 第四行颜色对齐**
  - 目标：在 rebuttal R3 Q2 里加一段有据可查的解释：noise update 稳定的是编辑轨迹的结构一致性，而非逐像素颜色匹配；某些颜色接近的样例中 w/o noise 反而颜色更像，但在纹理细节和 3D 一致性上差距更大
  - 可以引用 `tab:ablation_quantitative` 里 w/o Noise Update 的量化下降作为佐证（CLIP 0.7501→0.7235，DINO 0.7629→0.7343）
  - 产出：纯文字，不需要新实验；**零成本**
4. **P0-C：Fig. 2/4 换高质量图**
  - 目标：替换 drawio 导出的压缩 PNG，改为 SVG 或高 DPI 导出
  - 产出：revision 图；rebuttal R3 Q1 和 R2 Q2 里提及"figures have been re-exported at full resolution"
  - 前置：需找到 drawio 源文件（可能在 PaperBanana/ 或未跟踪目录）

### P1（回应 R1/R3，不依赖大规模训练）

1. **P1-A：VRAM / wall-clock 数字**
  - 一次 profiling：标准配置下单步 render + edit (9 steps) + backward 的时间和显存；与"仅 generator update"对比
  - 产出：一行数字写进 rebuttal R3 Q4 和 R1 Q4
2. **P1-B：Qwen prompt 模板 + failure 图例**
  - 整理 2–3 条具体 instruction template（如"preserve the 3D silhouette and camera perspective of the source view, enhance texture realism to match the reference image"）
  - 整理 2–4 组 typical failures（viewpoint reversion、hallucinated background、over-saturation）
  - 产出：supplement section；rebuttal R3 Q4 和 R1 Q3 中引用

### P2（有时间再做，不应影响 P0/P1 节奏）

1. Public benchmark sanity check（确认 protocol，结果出来后再决定是否写进 rebuttal）
2. Stronger baseline（carefully matched reference 承诺即可）
3. Human preference study（revision 承诺）
4. Related work 补写（R2 要求，属于纯写作，revision 承诺）

## rebuttal.tex 现有风险点


| 位置                      | 风险                                                             | 建议                                                                                |
| ----------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 第 28 行 global statement | 写了"evaluation on an additional public benchmark"，若来不及跑或结果差，会食言 | 改为"evaluation on a public benchmark subset, preliminary results will be included" |
| R3 Q1                   | 纯承诺；R3 明确说没有 supplemental material                             | 等 P0-A 完成后改为"we have added..."                                                    |
| R3 Q3                   | 文字解释仍偏绕，没有 viz 支撑时说服力不足                                        | 等 P0-B 完成后加一句"a step-by-step visualization is provided in the supplement"         |
| R3 Q4                   | VRAM/runtime 无具体数字                                             | 等 P1-A 完成后填入                                                                      |
| R1 Q4                   | 承诺了 human preference study                                     | 标注为 revision commitment，不暗示已有结果                                                   |


## 下一 Session 执行顺序

1. **找回已有 render/figure assets**（outputs/ 或 PaperBanana/ 本地目录），确认哪些可以直接用于 P0-A 和 P0-C。
2. **跑 P0-B**：固定 1–2 个样例，dump FlowEdit 中间步 x_edit 可视化；同时做 w/ vs w/o negative guidance 的对比。
3. **写 P0-B'**：用现有量化数据在 rebuttal R3 Q2 补充解释。
4. **跑 P1-A profiling**：单步计时，记录 wall-clock 和 peak VRAM。
5. **整理 P1-B**：从已有 edit 示例里挑 prompt 和 failure case。
6. 以上完成后 **更新 rebuttal.tex**，把对应段落从"we will..."改为"we have..."或"preliminary results show..."。
7. **最后**再决定 public benchmark 是否写进 rebuttal 正文。

## 参考文件


| 文件                                                    | 关键位置                             | 说明                                                                                                     |
| ----------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `review/Reviewer#1.png`                               | 整张截图                             | R1，Borderline Accept；核心要求：public benchmark、distillation baseline、human eval、Qwen failure、compute       |
| `review/Reviewer#2.png`                               | 整张截图                             | R2，Borderline Accept；核心要求：related work、qualitative+figure quality、second dataset                       |
| `review/Reviewer#3.png`                               | 整张截图                             | R3，Borderline Reject；**提分摇摆票**；核心要求：multi-view qualitative、ablation clarity、Eq.7 viz、VRAM、Qwen prompts |
| `rebuttal.tex`                                        | 全文件                              | 当前 77 行初稿，有上述风险点待修                                                                                     |
| `main.tex` L528–531                                   | `tab:ablation_quantitative`      | w/o Noise Update 量化：CLIP 0.7235、DINO 0.7343，可用于支撑 P0-B' 解释                                             |
| `main.tex` L278–281                                   | Eq. `\ref{eq:red_diff_velocity}` | 负源 guidance 的公式定义，P0-B viz 的基础                                                                         |
| `figures/plots/plot_ablation.py`                      | 全文件                              | RE ratio/steps 曲线的内嵌数据；与 R3 Q2 ablation clarity 相关                                                     |
| `.cursor/plans/rebuttal_experiments_0c5ed907.plan.md` | 全文件                              | 当前优先级计划；与本 handoff 保持一致                                                                                |


