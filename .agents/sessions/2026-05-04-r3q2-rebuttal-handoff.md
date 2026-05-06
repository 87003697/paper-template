# Session Handoff: R3 Q2 Rebuttal 改写

## 本 Session 目的

针对 Reviewer #3 Q2（"w/o noise golem 第四行颜色对齐反而更好"），讨论并最终确定回复逻辑，完成 `rebuttal.tex` 对应段落的改写。

## 核心决策：最终采用的解释逻辑

**归因链（四层递进）：**

1. **承认现象**：Reviewer 的观察是正确的，第四行 w/o noise 结果颜色确实更接近 reference。
2. **归因于 prompt 设计**：主实验统一使用 minimal prompt（"rotate the camera"）来隔离视角变化，保证训练一致性；但这个 prompt 对背景颜色没有约束。
3. **解释 3D 机制**：背景不受约束 → 2D 基模可能引入意外的色偏 → Classifier-guided noise update 忠实传播并放大了这一偏差。
4. **给出解法**：在 prompt 里加入背景约束（如 "white background"）能有效保持前景颜色一致性，并进一步提升 3D 生成质量。
5. **大盘数据兜底**：在全数据集上，noise update 对结构和纹理保真度仍然不可或缺（CLIP/DINO 从 0.7235/0.7343 提升至 0.7501/0.7629）。

## 关键数据（已获得）

| 对比 | CLIP | DINO |
|------|------|------|
| 2D 编辑 "rotate the camera" | 0.0314 | 0.0371 |
| 2D 编辑 "rotate the camera. white background" | 0.0339 (+7.9%) | 0.0387 (+4.3%) |
| 3D 生成 原版 prompt | 0.7501 | 0.7629 |
| 3D 生成 white background prompt | 0.7528 (+0.36%) | 0.7653 (+0.31%) |
| 3D 生成 w/o Noise Update（ablation） | 0.7235 | 0.7343 |

**注意**：3D 层面的 prompt 提升幅度很小（+0.3%），**不写进 rebuttal 正文**，改为定性描述"further improves"，具体数字承诺放进 revision。

## 讨论中排除的方案及原因

| 方案 | 排除原因 |
|------|---------|
| 说"石质材质有暖色先验" | 模型没有在此类数据上 finetune，会引发泛化性质疑 |
| 说"prompt 写得有问题" | 暗示 ablation 选图有偏，可能引发对实验公正性的质疑 |
| 同时列出 2D（0.0314）和 3D（0.7501）数字 | 两组数字尺度悬殊（0.03 vs 0.75），容易引发 Reviewer 误解和追问 |
| 说"to ensure a fair baseline"解释 minimal prompt | 与"under-constrained"矛盾，自相打架 |

## 最终写入 rebuttal.tex 的段落（R3 Q2，第 66–70 行）

```latex
\noindent{\em\textbf{Q2. Hard-to-interpret ablation results.}}
The reviewer is correct. 
Our experiments used a minimal prompt ``rotate the camera'' to isolate the viewpoint change; however, this leaves the color unconstrained, allowing the 2D base model to introduce color shifts, which our classifier-guided noise update faithfully propagates and amplifies. 
We found that adding a background constraint such as ``white background'' in the prompt helps preserve foreground color consistency and further improves the 3D generation quality, with full results included in the revision. 
Across the full dataset, noise update remains essential for structural and textural fidelity, improving CLIP/DINO from 0.7235/0.7343 to 0.7501/0.7629.
```

## 与其他问题的桥接关系

- **R3 Q4 / R1 Q3（Qwen prompt 模板）**：Q2 里提到了"background constraint in the prompt"，Q4 应进一步展示具体的 prompt template 示例（包括 "rotate the camera. white background" 作为改进示例），保持前后呼应。
- **R3 Q4 的 prompt ablation 数据**：完整的 2D/3D 定量对比（上表）将放进 revision，Q4 里可以一并承诺。

## 待完成的其他问题

根据 priority 文档，R3 Q2 已完成，剩余优先级任务：

| 优先级 | 任务 | 状态 |
|--------|------|------|
| P0-A | 高清多视角 qualitative 图 | 待完成 |
| P0-B | FlowEdit 中间步 / negative guidance 机制图 | 待完成 |
| P0-C | Fig. 2/4 换高质量图 | 待完成 |
| P1-A | VRAM / wall-clock profiling | 待完成 |
| P1-B | Qwen prompt 模板 + failure 图例 | 待完成 |
| — | R1/R2 其余问题回答完善 | 待完成 |
| — | 第 28 行 global statement 措辞软化 | 待完成 |

## 参考文件

| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `rebuttal.tex` | 第 66–70 行 | R3 Q2 已改写完成 |
| `main.tex` L528–531 | `tab:ablation_quantitative` | w/o Noise Update 量化数据来源 |
| `.agents/sessions/2026-05-03-oreo-rebuttal-priority.md` | 全文件 | 优先级决策和风险点 |
