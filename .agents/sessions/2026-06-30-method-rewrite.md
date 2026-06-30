# Session Handoff: Method Sections Rewrite & Supplementary Fill

## 对话 Transcript
`~/.claude-internal/projects/-Users-zhiyuanma-Desktop-OREO-ECCV-paper-template/ed797fe1-3ce9-40d1-954c-0d6b1152e11d.jsonl`

## 前序 Session
- `.agents/sessions/2026-06-29-camera-ready-notation.md` — 同日前半 session：公式记号统一、source→unconditional、method overview 重写、pipeline 图替换
- `.agents/sessions/2026-06-29-camera-ready-edits.md` — 添加 neg-src figure 到正文、调间距

## 相关 Plan
- `.agents/plan/camera-ready-remaining.md` — camera-ready 剩余任务清单

## 任务目的
继续 ECCV camera-ready 修改：重写 Sec 3.1 Problem Formulation 和 Sec 3.3 Reinforced Editing 的叙述逻辑，替换 Figure 3 图片（SVG→PDF），添加 Sec 4.1 消融实验框架，以及填充 supplementary 中大量 TODO 占位符。

## 执行内容
1. 重写 Sec 3.1 Problem Formulation：从旧的四句话改为 pipeline-flow 风格，inline 定义符号 `x^{src} = P(G_θ(x^{ref}), π)` 和 `x^{tgt} = E_φ(x^{src}, x^{ref})`
2. 添加 FlowEdit 引用 `\cite{couairon2024flowedit}`
3. 简化 Eq. 5：去掉 `φ` 下标和 `w` guidance scale，只保留 `tgt/src` 上标
4. 完整重写 Sec 3.3 开头：新增 pipeline 角色定位→现有模型的局限（alter pose）→提出 RE→FlowEdit c^src 不存在的动机→unconditional source 分支
5. 在 Eq. 7 的 where 子句中加入 `c^ref = c^tgt` 编码说明和 Fig pipeline 引用
6. 重写 Noise Update 段落：从"reduce variance"改为"editing 可能不充分 + 随机噪声削弱效果"，引用 DNAEdit
7. 将 source branch 效果讨论（文字+figure）从 Sec 3.3 移到 Sec 4.1
8. 替换 Figure 3 图片：SVG→Chrome headless PDF→pdfcrop
9. 在 Sec 4.1 添加 Table 2 消融实验框架（Full / w/o Source Branch / w/o Noise Update），数据留 TODO
10. 在 Sec 3.3 末尾添加 Algorithm 1 引用
11. 添加 `xie2026dnaedit` bib 条目
12. 填充 supplementary：dataset construction、editing prompts、computational overhead、GSO benchmark（替换 Toy4K）、adversarial training details

## 代码改动

### Commits
无新 commit。所有改动均为 unstaged。当前 branch `main` 比 origin 多 3 commits（前序 session 提交的）。

### 文件详情

**`camera_ready.tex`**（+37/-30 行 vs HEAD）— 本次 session 核心改动

1. **Sec 3.1 Problem Formulation**（~L170-183）：
   - 删除：旧的 4 句分散定义 + 独立的 x^src/x^tgt 公式行
   - 新增：3 句 pipeline-flow 叙述，inline 定义所有符号，公式 Eq.1 不变，where 子句一句话
   - 设计选择：用户要求"在讲逻辑的同时把符号说清楚"，所以 inline 而非分离

2. **Eq. 5 FlowEdit**（~L211）：
   - `v_φ^{w_{tgt}}(x^{tgt}(t); t, c^{tgt}) - v_φ^{w_{src}}(x^{src}(t); t, c^{src})` → `v^{tgt}(x_t^{tgt}; t, c^{tgt}) - v^{src}(x_t^{src}; t, c^{src})`
   - 去掉 φ、w，因为后续讨论中 tgt 有 CFG、src 都是 uncond，不需要在 preliminary 暴露

3. **Sec 3.3 Reinforced Editing 开头**（~L250-265）：
   - 删除：旧的 2 段（generic goal + "opposite guidance scales"）
   - 新增：5 句新叙述 — pipeline 角色 → 现有 editor 的 limitation（alter pose, ref Sec 4.1）→ 提出 RE → FlowEdit c^src 不存在 → unconditional source
   - 用户关键决策："enable structure-preserving enhancement" 优于 "reinforce structure preservation"

4. **Eq. 7 where 子句**（紧接 Eq. 7 后）：
   - 新增：`v_φ` 是 velocity field、`w` 是 CFG scale（引 ho2021classifier）、`c^ref` 编码 reference image + viewpoint change text prompt（ref Fig pipeline）
   - `c^ref = c^tgt` 放在 "guide the target branch toward" 这句里而非 where 后

5. **Source branch 讨论**（从 Sec 3.3 移至 Sec 4.1，~L428-440）：
   - 原来 Sec 3.3 里 3 句冗长讨论压缩为 1 句，移入 4.1 "Effect of the Source Branch" 段
   - 新增 Figure `fig:neg_src_guidance`（用 `figures_rebuttal/comparison_grid.png`）
   - 新增对 Table 2 的定量引用

6. **Table 2 消融框架**（Sec 4.1，~L440-455）：
   - 新增 3 行表格：Full (Ours) / w/o Source Branch / w/o Noise Update
   - 指标：CLIP Sim / DINO Sim / IoU，值均为 `\texttt{TODO}`

7. **Noise Update 段**（~L261-270）：
   - 删除：旧的 "reduce stochastic variance" + 重复的 "mitigate this by"
   - 新增：editing 不充分的动机 + 随机噪声削弱效果（引 DNAEdit）+ cfg signal inject noise
   - 末尾新增 Algorithm 1 引用

8. **Figure 3**（~L356）：路径从 `figures/OREO Edit Comparison.drawiov2.png` → `figures_final/OREO_Edit_Comparisonv2_cropped.pdf`

**`main.bib`**（+9 行）：
- 新增 `xie2026dnaedit` 条目（DNAEdit, NeurIPS 2026）

**`supplementary.tex`**（+57/-48 行 vs HEAD）— 填充 TODO 占位符：
- **Sec Dataset Construction**：从 5 行 TODO 模板 → 6 句实际描述（~2000 images、filtering criteria、100 evaluation images × 5 views = 500 pairs）
- **Sec Editing Prompts**：从 itemize TODO → 具体 prompt 文本 + 说明 training/evaluation 使用同一 prompt
- **Sec Computational Overhead**：填入实际数字（22s/step baseline、81% editing cost sequential、45% async overlap、0.1s adversarial）+ 表格 Table overhead
- **Sec GSO**（替换 Toy4K）：全部重写为 GSO benchmark（77 objects, 16 views），新 Table gso（FID: Trellis 58.71, Photo3D 72.94, OREO 57.32）
- **Sec Adversarial Training Details**：填入 DINOv3-S 架构细节、hook depths {2,5,8,11}、head architecture、lr schedule、γ_adv=10^-3、R1 gradient penalty discussion

**`figures_final/`**（新目录，untracked）：
- `OREO_teaser_v0.pdf`（895KB）— teaser 图（前序 session 已有）
- `OREO_pipeline_v3.drawio.pdf`（895KB）— pipeline 图 v3（前序 session 已有）
- `OREO Edit Comparisonv2.svg`（21MB）— 原始 SVG
- `OREO_Edit_Comparisonv2.pdf`（23MB）— Chrome headless 转换的 PDF
- `OREO_Edit_Comparisonv2_cropped.pdf`（23MB）— pdfcrop 裁切白边后的最终版

**`.agents/sessions/2026-06-29-camera-ready-edits.md`** — 前序 handoff 小幅更新

## 调试经验

- 现象：SVG→PDF 转换失败链 → 原因：cairosvg 无法解析 SVG 颜色值（`ValueError: invalid literal for int() with base 16: 'ig'`），且 cairo 库存在 DYLD 路径问题 → 解法：弃用 cairosvg，改用 Chrome headless `--print-to-pdf`
- 现象：Chrome PDF 底部有文件路径和页码 → 原因：默认行为 → 解法：加 `--no-pdf-header-footer` 参数
- 现象：Chrome PDF 为 Letter 页面（612×792pt），导致 figure + 后续图全部被推到正文末尾（20 页）→ 原因：默认页面尺寸太大 → 解法：`pdfcrop` 裁切 + `width=\textwidth` 约束
- 现象：Sec 3.3 中 FlowEdit 在连续两句中重复提到 → 原因：叙述未合并 → 解法：合并为 "Different from the original FlowEdit..."

## 用户决策与偏好
- 所有 camera-ready 改动必须 `\textcolor{red}{}` 标红（反复强调）
- tex 中不使用括号做 section 引用（如 "Sec. 3.2" 而非 "(Sec. 3.2)"）
- "enable structure-preserving enhancement" 优于 "reinforce structure preservation"
- Source branch 效果讨论放 4.1 而非 method
- c^ref = c^tgt 放在 "guide the target branch toward" 叙述中而非 where 后面
- 中文逐句讨论→英文定稿工作流

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `camera_ready.tex` | ~L428-455 | Table 2 消融框架 + source branch/noise update 讨论，需填 TODO |
| `camera_ready.tex` | ~L290-340 | Sec 3.4 Optimization，尚未审查 |
| `supplementary.tex` | ~L60-80 | Sec S1 negative source guidance，需和正文 unconditional 说法统一 |

## 最终方案
Sec 3.1 采用 pipeline-flow inline 符号定义。Sec 3.3 以"pipeline 角色→editor limitation→RE proposal→FlowEdit c^src gap→unconditional source"逻辑重写。Noise Update 从 variance-reduction 改为 editing-insufficiency 动机。Source branch 讨论移至 4.1 实验。Figure 3 从 SVG 通过 Chrome→pdfcrop 链转 PDF。Supplementary 填入实际数据和架构细节。

## 下一步任务
1. **填 Table 2 TODO**：需要跑消融实验获取 Full / w/o Source Branch / w/o Noise Update 的 CLIP Sim / DINO Sim / IoU 数据
2. **页数控制**：当前 ~19 页，目标 14 页正文
3. **Sec 3.4 审查**：Optimization section 尚未过一遍
4. **Supplementary S1 统一**：negative source guidance 描述需和正文 unconditional 说法统一
5. **Related Work 补充参考文献**

## 初步方案
- Table 2：需要用户提供实验数据，或指明实验代码路径以便协助运行
- 页数：Figure 3 的 23MB PDF 可能是主要膨胀来源，考虑压缩或降低分辨率；另外可精简 experiments 文字
- Sec 3.4：读当前内容，检查符号一致性（x_t^tgt 记号、unconditional 说法），和用户逐段确认
- S1 统一：将 "negative source guidance" 改为 "unconditional source anchor" 以匹配正文
