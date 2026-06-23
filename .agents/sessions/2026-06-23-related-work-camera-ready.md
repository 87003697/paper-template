# Session Handoff: Related Work Camera-Ready

## 对话 Transcript
Cursor transcript candidate:
`/Users/zhiyuanma/.cursor/projects/Users-zhiyuanma-Desktop-OREO-ECCV-paper-template/agent-transcripts/e19feed5-5d63-4519-b26a-92db0a45df02/e19feed5-5d63-4519-b26a-92db0a45df02.jsonl`

Note: `~/.claude-internal` 最新 JSONL 指向另一个项目，未作为本项目 handoff 入口。

## 前序 Session
- `.agents/sessions/2026-05-10-rebuttal-final.md` — rebuttal 最终版，记录 Reviewer #1/#2/#3 的核心 concerns 与 rebuttal 承诺。
- `.agents/sessions/2026-05-10-refine-r1-rebuttal.md` — R1 baseline / DMD / human study / overhead 相关论证来源。

## 相关 Plan
- `.agents/plan/camera-ready.md` — camera-ready 总计划；问题 1 已更新为完成状态，后续问题 2-8 仍 pending。
- `.agents/plan/problem-1-related-work.md` — 本次 Related Work 重构的细化计划、三段中英文草稿、BibTeX 状态和验证记录。

## 任务目的
完成 ECCV camera-ready 正文中 Problem 1：补充 Related Work 对 2D/3D editing pipelines 与 2D-to-3D prior transfer 的覆盖，并澄清 Magic3D / ProlificDreamer / DMD 等 baseline 与 OREO 设定的关系。

## 执行内容
- 反复讨论并收敛 Related Work 的三段结构，避免泛泛综述，改为围绕 OREO 的 fidelity gap、edited-view supervision、2D prior transfer 局限展开。
- 从 reviewer 截图中确认 Related Work 相关要求：Reviewer #2 要求补充 3D/2D generation and editing pipelines；Reviewer #1 要求澄清 Magic3D / ProlificDreamer 类 baseline 与 OREO 的设定差异。
- 检查 `main.bib` 中所有计划引用的 BibTeX：确认新增工作已存在，并修正正文 cite key 到实际 key。
- 将 `camera_ready.tex` 的 `Related Work` 重写为最终三段，并成功编译。

## 代码改动

### Commits
本 session 没有 commit。

### 文件详情

**`camera_ready.tex`** — 重写 `\section{Related Work}` 的三段内容。
- 删除旧逻辑：原先从 “optimization-based -> learning-based” 泛泛开头，并把 2D/3D editing、3D enhancement、SDS baseline 混在一起；其中还包含旧 cite key，如 `instructnerf2023`、`chen2024cvpr-gaussianeditor`、`koh2025dffsplat`。
- 新增第一段 `Learning-based 3D Generation and Generator Post-training`：直接从主流 3D-native foundations 的 feed-forward 生成切入，强调合成 3D 数据相对真实 2D 图像的规模/多样性不足导致 visual fidelity、纹理细节、realism 仍有提升空间；引出用 2D diffusion appearance prior 迁移到 3D generator，并通过 edited views 的差异进行 post-training。
- 新增第二段 `2D Image Editing for Fidelity-Enhancing Supervision`：说明高质量监督中的 edited views 应提升 visual fidelity 且保持 camera viewpoint / structure；引用 training-based editors（InstructPix2Pix、MagicBrush、Emu Edit、UltraEdit），说明其可能产生结构误差；再引用 Prompt-to-Prompt、Null-text Inversion、FlowEdit、RF-Inversion，说明 OREO 借鉴更可控的 training-free / inversion-free editing 来构造 structure-aligned edited views。
- 新增第三段 `2D Priors for 3D Editing and Generation`：覆盖 Instruct-NeRF2NeRF、DreamEditor、GaussianEditor、DFFSplat、Image Sculpting、MvDrag3D、GeoDiffusion，指出它们多为 per-scene optimization，无法摊销到可泛化 generator；再区分 DreamFusion / Magic3D / ProlificDreamer 的 optimization-based text-to-3D 设定与 OREO 的 learning-based image-to-3D generator post-training；单独说明 DMD 更接近 generator-learning，因此保留为 score-distillation ablation baseline，但仍依赖 implicit score-gradient supervision。
- 关键 cite key 已对齐 `main.bib`：`haque2023instruct`、`wang2024gaussianeditor`、`koh2026diffusion`、`yenphraphai2024image`、`chen2024mvdrag3d`、`chen2024geodiffusion` 等。

**`.agents/plan/problem-1-related-work.md`** — 更新 Problem 1 细化计划。
- 三段中英文草稿已改为最终逻辑版本。
- “待补 BibTeX 工作清单”已变成实际状态清单：所有当前引用均已存在于 `main.bib`。
- 移除了早先单独的 `## Review` 审查块，将有价值内容吸收到正文约束和最终实现摘要中。
- 新增最终验证记录：`ReadLints` 无报错，`latexmk` / `pdflatex` 成功，`camera_ready.log` 无 undefined citation/reference。

**`.agents/plan/camera-ready.md`** — 更新总计划的问题 1。
- 将问题 1 描述更新为已完成的三段 Related Work 重构。
- 记录已补充的 2D image editing、3D editing / geometry-conditioned editing、score-distillation baseline 相关工作。
- 记录已澄清 Magic3D / ProlificDreamer 不适合作为直接定量对比，DMD 作为合理消融基线。

## 调试经验
- 现象：第一次 `latexmk` 成功退出但日志里仍有新引用 undefined warnings。
  原因：`.bbl` 已生成新条目，但第一轮日志包含中间态 warning。
  解法：检查 `camera_ready.bbl` 确认新 `\bibitem` 存在，再强制跑一次 `pdflatex -interaction=nonstopmode -halt-on-error camera_ready.tex`，最终 `camera_ready.log` 无 undefined citation/reference。
- 现象：`main.bib` 中存在条目，但正文 key 可能不匹配。
  原因：用户从 Google Scholar 加入的 canonical key 与早期计划建议 key 不同。
  解法：统一正文使用 `main.bib` 实际 key，例如 `haque2023instruct` 而不是 `instructnerf2023`。

## 验证
- `ReadLints(["camera_ready.tex"])`：No linter errors。
- `latexmk -pdf -interaction=nonstopmode -halt-on-error camera_ready.tex`：成功。
- `pdflatex -interaction=nonstopmode -halt-on-error camera_ready.tex`：成功，输出 `camera_ready.pdf`。
- `rg "undefined|Undefined|Citation|There were undefined references" camera_ready.log`：无匹配。

## 未 commit
| 文件 | 改动类型 | 未提交原因 |
|------|---------|-----------|
| `.agents/plan/camera-ready.md` | 更新总计划问题 1 | 用户未要求 commit |
| `.agents/plan/problem-1-related-work.md` | 更新细化计划与验证记录 | 用户未要求 commit |
| `camera_ready.tex` | 重写 Related Work | 用户未要求 commit |
| `.agents/sessions/2026-06-23-related-work-camera-ready.md` | 新增 handoff | 用户未要求 commit |

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `camera_ready.tex` | `Related Work` | 本轮重构完成段落 |
| `main.bib` | 新增末尾条目与既有 2D/3D refs | 所有 Related Work cite key 的来源 |
| `.agents/plan/camera-ready.md` | 问题 2 起 | 后续 camera-ready 任务入口 |

## 最终方案
Related Work 采用三段防御式结构：先解释 learning-based 3D generator 的 fidelity gap，再解释 OREO 如何借助 2D editing 构造 high-fidelity 且 structure-aligned 的 supervision，最后解释已有 2D priors for 3D editing/generation 为什么不能直接满足 feed-forward generator post-training，并合理化 DMD ablation 与 Magic3D/ProlificDreamer 非直接对比。

## 下一步任务
继续推进 `.agents/plan/camera-ready.md` 中 Problem 2：在 Method 中引入 GAN loss（Adversarial Loss）及实验/附录消融说明。

## 初步方案
- 先读 `camera_ready.tex` 的 `Generator Optimization via Pseudo-GT Supervision` / Sec. 3.4 与 Algorithm 2，确认当前 loss 公式和闭环优化步骤。
- 再决定是否真的在正文加入 GAN loss。注意这是方法实质改动，需确认是否与真实训练/实验一致；若只是 camera-ready 补写，应避免引入无法支撑的 claim。
- 如果加入：正文只给最小公式和交替优化说明，Supplementary 放判别器架构、训练超参和有/无 GAN loss 定性对比。
- 风险：正文当前已编译到 17 页，后续仍需 Problem 8 控页。
