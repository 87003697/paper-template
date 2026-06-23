# Plan: OREO Camera-Ready Problem 1 - Related Work & Baseline Clarification

## 目标
重构 Related Work 章节为更清晰、说服力更强的“三段论”结构，全面引入 **optimization-based** 与 **learning-based** 的术语对比。在补充 3D/2D editing pipelines 讨论（引用 Instruct-NeRF2NeRF, GaussianEditor, DreamEditor）的同时，保留并整合 3D foundation models 与对齐工作的全部文献引用，深刻澄清 OREO 与传统 optimization-based 蒸馏基线（如 Magic3D, ProlificDreamer）的场景差异，并论证 DMD 作为合理消融对照的充分性。

## 关键发现（Explore 阶段）
- **相关文件**：
  - `camera_ready.tex` (修改 Related Work 章节，将原本的两大加粗小段扩展为结构更严密的三个加粗小段)
  - `main.bib` (由用户手动录入 BibTeX 文献条目，助手不修改)
- **约束条件与决策**：
  - 助手不直接修改 `main.bib`，所有 BibTeX 条目均在对话中向用户提供，并引导其手动录入。
  - **引用策略调整**：用户确认不需要对 3D 预训练模型和对齐工作做复杂的两组细分（“原生派” vs “解耦派”），而是秉持最直截了当、清晰的逻辑，直接将全部 10 篇 3D-native 预训练/对齐模型（`xiang2025structured,zhao2025hunyuan3d,ye2025hi3dgen,li2025triposg,guo2025hyper3d,yushi2025gaussiananything,chen20253dtopia,lin2025diffsplat,li2025step1x,zhang2025bang`）进行一并保留，放置于最主流的 3D-native foundations 部分，从而实现大一统。
  - **BibTeX 风险**：`DMD` 对应的 `yin2024onestep` 已存在于 `main.bib`，不需要重复新增；但新增的 2D/3D editing 与 3D prior-transfer 文献必须由用户手动录入，并确保正文 `\cite{...}` 键名与 `main.bib` 完全一致，否则会在 PDF 中出现未定义引用 `[?]`。
  - **核心逻辑澄清**：OREO 不是在推理时直接使用 2D editor 精修单个结果，而是在 generator post-training 的动态闭环中，利用 high-fidelity 且 structure-aligned 的 edited views 作为 pseudo-GT / online supervision 来训练 3D 生成器。

## 逻辑架构设计（三段论）

### 第一段：Learning-based 3D Generation and Generator Post-training
*   **中文草稿**：目前主流的 learning-based 3D 生成方法通常在隐空间中训练 3D-native foundations，以前向方式生成 3D 资产（此处并列引用 10 篇 3D-native 大模型文献）。这些方法依赖 Objaverse 等合成 3D 数据进行训练，其数据规模与多样性仍远弱于真实世界 2D 图像数据。因此，它们生成的 3D 资产在 visual fidelity、纹理细节和真实感上仍存在明显提升空间。相比之下，预训练 2D diffusion priors 从大规模真实图像中学习了更丰富的 appearance prior。因此，一个可行方向是将 2D diffusion priors 中蕴含的高保真 appearance prior 迁移到 3D 生成模型中，用以弥补 3D 数据在纹理细节与真实感上的不足。OREO 沿着这一方向，通过 2D 图像编辑将生成器渲染出的不完美视图转化为更高保真且结构保持的 edited views，并利用编辑前后的视图差异构造在线监督信号，对 3D 生成器进行 post-training。
*   **英文草稿**：State-of-the-art learning-based 3D generation methods typically train 3D-native foundations in latent spaces to synthesize 3D assets in a feed-forward manner. These methods are predominantly trained on synthetic 3D datasets such as Objaverse, whose scale and diversity remain limited compared with real-world 2D image data. As a result, the generated 3D assets still leave significant room for improvement in visual fidelity, texture details, and realism. In contrast, pretrained 2D diffusion priors capture richer appearance priors from large-scale real images. Therefore, a feasible direction is to transfer the high-fidelity appearance prior encoded in 2D diffusion priors to 3D generative models, compensating for the limitations of 3D data in texture detail and realism. Following this direction, OREO leverages 2D image editing to transform imperfect rendered views from a 3D generator into higher-fidelity, structure-preserving edited views, and uses the discrepancy between the original and edited views as online supervision for generator post-training.

### 第二段：2D Image Editing for Fidelity-Enhancing Supervision
*   **中文草稿**：为了得到高质量的监督信号，edited views 相较于原始 rendered views 应提升视觉保真度，同时保持一致的相机视角与结构信息。为此，我们从现有 2D 图像编辑方法中获得启发。近年来，基于训练的图像编辑模型通常以输入图像和文本指令为条件，学习生成符合编辑目标的输出图像，并已展现出较强的外观改写与细节增强能力。然而，这类方法不显式约束输出图像保持输入图像的相机视角、物体姿态或整体布局，编辑后的图像会产生结构误差，从而提供错误的编辑信号。为了减少上述结构误差，我们进一步考虑在这些强大的 image editors 上结合 training-free editing 方法，对编辑过程进行更可控的约束。已有一些 inversion-based editing 方法通过先将输入图像反演到噪声或隐空间，再在反演轨迹上进行编辑，但反演误差仍可能影响结构保持。相比之下，inversion-free editing 方法不需要显式反演输入图像，而是通过耦合源图像与目标编辑方向的生成轨迹来实现编辑，更适合作为 OREO 构造结构对齐 edited views 的基础。
*   **英文草稿**：To obtain high-quality supervision signals, edited views should enhance the visual fidelity of the original rendered views while preserving their camera viewpoints and structural information. To this end, we draw inspiration from existing 2D image editing methods. Recent training-based image editors typically take an input image and a text instruction as conditions, learning to generate outputs that satisfy the desired edit while demonstrating strong appearance modification and detail enhancement capabilities. However, these methods do not explicitly constrain the output to preserve the input camera viewpoint, object pose, or overall layout, so the edited images may introduce structural errors and provide incorrect editing signals. To reduce such structural errors, we further consider combining these powerful image editors with training-free editing methods to impose more controllable constraints on the editing process. Some inversion-based editing methods first invert the input image into the noise or latent space and then perform editing along the inverted trajectory, but inversion errors may still affect structure preservation. In contrast, inversion-free editing methods avoid explicit image inversion and edit images by coupling the generation trajectories of the source image and the target direction, making them a better fit for constructing structure-aligned edited views in OREO.

### 第三段：2D Priors for 3D Editing and Generation
*   **中文草稿**：虽然 2D priors 已被用于 3D editing 和 generation，现有方法仍难以直接满足后训练 feed-forward 3D 生成器的需求。一方面，Instruct-NeRF2NeRF、DreamEditor、GaussianEditor、DFFSplat 以及 Image Sculpting、MvDrag3D、GeoDiffusion 等 3D editing / geometry-conditioned editing 方法主要面向单个实例或场景，通常依赖 per-scene optimization，因此无法将 fidelity-enhancing prior 摊销到可泛化的 3D 生成器中。另一方面，DreamFusion、Magic3D、ProlificDreamer 等 score-distillation 方法属于 optimization-based text-to-3D，输入设定和推理流程与 OREO 的 learning-based image-to-3D generator post-training 不同，不适合作为直接定量对比对象。DMD 更接近生成器学习范式，因此可作为合理的 score-distillation 消融基线；但它仍依赖隐式 score-gradient supervision。相比之下，OREO 显式构造 high-fidelity 且 structure-aligned 的 edited views 作为 pseudo-GT，用稳定的 online pixel-level supervision 后训练 3D 生成器。
*   **英文草稿**：Although 2D priors have been explored for 3D editing and generation, existing methods do not directly meet the goal of post-training a feed-forward 3D generator. On the one hand, 3D editing and geometry-conditioned editing methods, such as Instruct-NeRF2NeRF, DreamEditor, GaussianEditor, DFFSplat, Image Sculpting, MvDrag3D, and GeoDiffusion, mainly target individual instances or scenes and typically rely on per-scene optimization, making it difficult to amortize the fidelity-enhancing prior into a generalizable 3D generator. On the other hand, score-distillation methods such as DreamFusion, Magic3D, and ProlificDreamer are optimization-based text-to-3D methods whose input setting and inference pipeline differ from OREO's learning-based image-to-3D generator post-training, making them unsuitable for direct quantitative comparison. DMD is closer to a generator-learning paradigm and is therefore retained as a reasonable score-distillation ablation baseline; however, it still relies on implicit score-gradient supervision. In contrast, OREO explicitly constructs high-fidelity, structure-aligned edited views as pseudo-GT and uses stable online pixel-level supervision to post-train the 3D generator.

## 相关代码
| 文件 | 位置 | 作用 |
|------|---------|------|
| `camera_ready.tex` | Related Work (Sec. 2) | 全面重写 Related Work 章节，重组为结构严密、辩护力极强的三个段落。 |

## 待补 BibTeX 工作清单

### 第一段：3D-native foundations / learning-based 3D generators
- ✅ `xiang2025structured` — Trellis / Structured 3D Latents（`main.bib` 已存在）
- ✅ `zhao2025hunyuan3d` — Hunyuan3D（`main.bib` 已存在）
- ✅ `ye2025hi3dgen` — Hi3DGen（`main.bib` 已存在）
- ✅ `li2025triposg` — TripoSG（`main.bib` 已存在）
- ✅ `guo2025hyper3d` — Hyper3D（`main.bib` 已存在）
- ✅ `yushi2025gaussiananything` — GaussianAnything（`main.bib` 已存在）
- ✅ `chen20253dtopia` — 3DTopia（`main.bib` 已存在）
- ✅ `lin2025diffsplat` — DiffSplat（`main.bib` 已存在）
- ✅ `li2025step1x` — Step1X-3D（`main.bib` 已存在）
- ✅ `zhang2025bang` — BANG（`main.bib` 已存在）

### 第二段：2D image editing
- ✅ InstructPix2Pix — `brooks2023instructpix2pix` 已存在；另有 `brooks2022instructpix2pix` arXiv 版本，正文建议统一用一个键名。
- ✅ Emu Edit — `sheynin2023emu` 已存在。
- ✅ Prompt-to-Prompt — `hertz2022prompt` 已存在（如需 attention control 代表作可引用）。
- ✅ Null-text Inversion — `mokady2023null` 已存在。
- ✅ FlowEdit — `couairon2024flowedit` 已存在。
- ✅ RF-Inversion — `zhang2024rfinversion` 已存在。
- ✅ MagicBrush — `zhang2023magicbrush` 已存在。
- ✅ UltraEdit — `zhao2024ultraedit` 已存在。

### 第三段：2D priors for 3D editing / geometry-conditioned editing
- ✅ Instruct-NeRF2NeRF — `haque2023instruct` 已存在；注意当前草稿/正文若使用 `instructnerf2023` 需要改成实际 key。
- ✅ DreamEditor — `zhuang2023dreameditor` 已存在。
- ✅ GaussianEditor — `wang2024gaussianeditor` 已存在；注意当前草稿/正文若使用 `chen2024cvpr-gaussianeditor` 需要改成实际 key。
- ✅ DFFSplat / Diffusion Feature Field for Text-based 3D Editing with Gaussian Splatting — `koh2026diffusion` 已存在；注意当前草稿/正文若使用 `koh2025dffsplat` 需要改成实际 key。
- ✅ Image Sculpting — `yenphraphai2024image` 已存在。
- ✅ MvDrag3D — `chen2024mvdrag3d` 已存在。
- ✅ GeoDiffusion — `chen2024geodiffusion` 已存在。
- ✅ **正文 key 已对齐**：`camera_ready.tex` 已统一使用 `haque2023instruct`、`wang2024gaussianeditor`、`koh2026diffusion` 等 `main.bib` 实际 key；最终编译日志无 undefined citation/reference。

### 第三段：2D-to-3D prior transfer / baseline clarification
- ✅ DreamFusion — `poole2022dreamfusion` 与 `poole2023dreamfusion` 都存在；正文建议统一用一个键名，优先用当前正文已有键名。
- ✅ Magic3D — `lin2023magic3d` 已存在。
- ✅ ProlificDreamer — `wang2024prolificdreamer` 已存在。
- ✅ DMD — `yin2024onestep` 已存在，不需要重复新增。
- ✅ Photo3D — `liang2026photo3d` 已存在。

## 实现步骤
- [x] Step 1: 在对话中向用户提供新增 2D/3D editing、3D prior-transfer 与 baseline 文献的标准 BibTeX 文本，并引导其手动录入 `main.bib`；特别注意 `yin2024onestep` 已存在，其他新增键名必须与正文引用完全一致。
- [x] Step 2: 对 `camera_ready.tex` 中的 Related Work 章节进行三段式重构：第一段说明 3D-native generator 的 fidelity gap，第二段说明如何构造 high-fidelity 且 structure-aligned 的 edited views，第三段说明 2D priors 在 3D editing / generation 中的已有迁移方式及其局限。
- [x] Step 3: 进行编译检查，确保没有引入 LaTeX 语法错误。

## 最终实现摘要

#### `camera_ready.tex` Related Work
- **第一段**：改为从 learning-based 3D-native foundations 切入，强调合成 3D 数据相对真实 2D 图像在规模与多样性上的不足，进而引出 visual fidelity / texture / realism 的提升空间。
- **第二段**：聚焦 `2D Image Editing for Fidelity-Enhancing Supervision`，说明 high-quality edited views 既要提升 visual fidelity，也要保持 camera viewpoint / structure；training-based editors 提供外观增强但可能引入结构误差，inversion-free editing 更适合作为构造 structure-aligned edited views 的基础。
- **第三段**：聚焦 `2D Priors for 3D Editing and Generation`，用 3D editing / geometry-conditioned editing 说明已有方法多为 per-scene optimization；用 DreamFusion / Magic3D / ProlificDreamer / DMD 说明 score-distillation 路线，并区分 DMD 的合理消融地位与 OREO 的 explicit pseudo-GT / online pixel-level supervision。
- **引用 key**：全部使用 `main.bib` 实际存在的 key，例如 `haque2023instruct`、`wang2024gaussianeditor`、`koh2026diffusion`、`yenphraphai2024image`、`chen2024mvdrag3d`、`chen2024geodiffusion`。

## 验证
- `ReadLints(camera_ready.tex)`：无 linter errors。
- `latexmk -pdf -interaction=nonstopmode -halt-on-error camera_ready.tex`：成功。
- `pdflatex -interaction=nonstopmode -halt-on-error camera_ready.tex`：最终 pass 成功。
- `camera_ready.log`：无 undefined citation / undefined reference。

## 状态
**当前阶段**: Done (Related Work Consolidatively Merged and defensive logic closed-loop)
