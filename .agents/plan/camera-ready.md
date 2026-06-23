---
name: camera ready
overview: 以 main.tex 为基线复制出 camera_ready.tex，在新文件中整理 ECCV camera-ready 正文：通过“正文精简 + 单独 supplementary + 定性大图与消退消解迁移”策略逐一解决审稿意见和 rebuttal 承诺，最后建立可独立编译的 supplementary.tex 并完成格式与控页检查。
todos:
  - id: create-supplementary-boilerplate
    content: 新建 supplementary.tex 并搭建可独立编译的 LaTeX 基础骨架
    status: completed
  - id: problem-1-related-work
    content: 在 camera_ready.tex 中补充 Related Work 并澄清 text-to-3D baseline 设定差异（使用规范 BibTeX 键名）
    status: completed
  - id: problem-2-gan-loss
    content: 在 camera_ready.tex 中引入 GAN loss（Adversarial Loss）公式与交替训练逻辑，并在 Experiments 中补充消退说明与 Supplementary 对比
    status: pending
  - id: problem-3-negative-branch
    content: 在 camera_ready.tex 中补充 negative source branch 理论解释（控制在 3-4 句），并在 supplementary.tex 中插入轨迹对比图与分析
    status: pending
  - id: problem-4-toy4k
    content: 在 camera_ready.tex 中以独立紧凑的 Table 2 插入 Toy4K 定量评估结果，并保持术语严格对齐
    status: pending
  - id: problem-5-human-study
    content: 在 camera_ready.tex 中插入人评核心结论，并在 supplementary.tex 中写入完整人评评判标准与多维度细节
    status: pending
  - id: problem-6-overhead-dataset
    content: 在 camera_ready.tex 中补充精简计算开销与数据集统计，并在 supplementary.tex 中写入详细 breakdown、prompts、以及判别器网络架构
    status: pending
  - id: problem-7-limitations
    content: 在 camera_ready.tex 中补充 Limitations 讨论，并在 supplementary.tex 中写入 Failure Cases 分析
    status: pending
  - id: problem-8-page-limit
    content: 迁移 Fig. 5（及备用 Fig. 7）至 supplementary.tex，并进行文字精简与排版微调，确保正文控制在 14 页以内
    status: pending
  - id: final-validation
    content: 联合编译并进行最终提交检查
    status: pending
isProject: false
---

# OREO Camera-Ready 计划（问题导向与人工文献管理版）

## 核心约束与原则
- **辅助文献管理**：助手绝对不修改 `main.bib` 或 any 样式、模板文件。所有文献条目的新增、修改均由助手在对话中提供 BibTeX 文本，并由用户手动写入 `main.bib`。
- **限制修改范围**：助手仅修改 `camera_ready.tex` 并创建/修改 `supplementary.tex`。其他任何已有文件（如 `main.tex`、样式文件等）均不作修改。

## 核心问题与解决方案规划

### 问题 0：创建 Supplementary 独立编译骨架 [已完成]
- **现状**：缺乏独立的 `supplementary.tex` 骨架设计，面临编译不通过或格式混乱风险。
- **目标**：建立可独立编译的 `supplementary.tex`。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：无。
  - **附录（`supplementary.tex`）**：
    - 新建 `supplementary.tex`，使用与 `camera_ready.tex` 一致的 `llncs` 样式与 packages（`graphicx`, `booktabs`, `multirow`, `eccv` 等），已去除作者与摘要，编译验证通过。
    - 将公式和图表序号的前缀重置为 `S`（`\renewcommand{\thefigure}{S\arabic{figure}}`，`\renewcommand{\thetable}{S\arabic{table}}`）。
    - 引入 `main.bib` 作为其文献引用，确保参考文献可独立解析。

---

### 问题 1：Related Work 覆盖不足与 Baseline 澄清
- **现状**：审稿人指出 Related Work 未充分覆盖 3D/2D editing pipelines；且存在关于是否需要与 text-to-3D baseline（如 Magic3D/ProlificDreamer）进行对比的疑问。
- **目标**：补充相关工作，并在不增加定量实验的前提下，清晰阐明设定差异。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - 已将 `Related Work` 重构为三段结构：
      - `Learning-based 3D Generation and Generator Post-training`：从 3D-native foundations 的 fidelity gap 出发，引出将 2D diffusion priors 的 high-fidelity appearance prior 迁移到 3D 生成模型。
      - `2D Image Editing for Fidelity-Enhancing Supervision`：说明 edited views 应提升 visual fidelity 且保持 camera viewpoint / structure；覆盖 training-based editors、training-free / inversion-based / inversion-free editing。
      - `2D Priors for 3D Editing and Generation`：覆盖 3D editing / geometry-conditioned editing 与 score-distillation 迁移路线，并澄清 OREO 与 per-scene optimization / text-to-3D baseline 的设定差异。
    - 已补充并引用 Reviewer #2 关心的 2D/3D editing 相关工作：InstructPix2Pix、MagicBrush、Emu Edit、UltraEdit、Prompt-to-Prompt、Null-text Inversion、FlowEdit、RF-Inversion、Instruct-NeRF2NeRF、DreamEditor、GaussianEditor、DFFSplat、Image Sculpting、MvDrag3D、GeoDiffusion。
    - 已明确 Magic3D / ProlificDreamer 属于 optimization-based text-to-3D，和 OREO 的 learning-based image-to-3D generator post-training 设置不同；DMD 更接近 generator-learning 范式，因此保留为 score-distillation 消融基线，但与 OREO 的 explicit edited-view pseudo-GT / online pixel-level supervision 不同。
    - **BibTeX 状态**：上述引用均已存在于 `main.bib`，正文已使用实际 key（如 `haque2023instruct`, `wang2024gaussianeditor`, `koh2026diffusion`, `yenphraphai2024image`, `chen2024mvdrag3d`, `chen2024geodiffusion`）。最终 `camera_ready.log` 无 undefined citation/reference。
  - **附录（`supplementary.tex`）**：
    - 无需此内容。

---

### 问题 2：在 Method 中引入 GAN loss（Adversarial Loss）与实验消退验证
- **现状**：现有的 Method 中仅包含基于 MSE 的 pseudo-GT 像素级监督与 $L_{\text{reg}}$ 正则化。在大尺度 3D 渲染与生成中，仅依靠 MSE 监督容易导致局部纹理过度平滑（over-smoothed），缺失高频逼真细节。
- **目标**：在 Method 的 `Generator Optimization via Pseudo-GT Supervision`（Sec. 3.4）中引入对抗损失（GAN Loss），提升纹理的高频保真度和画质，并在 Experiments 中进行论述，同时在 Supplementary 中补全定性对比，形成完整的学术闭环。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - **公式化表达**：引入一个 Discriminator $D_\psi$，以 $x^{\texttt{tgt}}$ 作为真实样本，以渲染图 $x^{\texttt{src}}$ 作为虚假样本。为了避免训练初期的梯度消失，Adversarial Loss 采用非饱和目标：
      $$\mathcal{L}_{\text{adv}}(G_\theta) = -\mathbb{E}_{x^{\texttt{src}}} \left[ \log D_\psi(x^{\texttt{src}}) \right]$$
      和 Discriminator 的训练损失 $\mathcal{L}_{\text{disc}}(D_\psi)$。
    - **总损失函数更新**：更新 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{sup}} + \lambda \mathcal{L}_{\text{reg}} + \gamma \mathcal{L}_{\text{adv}}$。
    - **文字解释与流程图/算法更新**：
      - 在正文 `Sec. 3.4` 的对应位置插入 GAN loss 的理论动机（对抗训练促使 Generator 生成高频逼真纹理）。
      - 微调 `Algorithm 2 (Closed-loop Optimization)`，补充 Discriminator $D_\psi$ 的交替优化更新步骤。
    - **消退闭环验证（实验关联）**：
      - 在正文消退分析（`Sec. 4.3`）中，使用 2-3 句文字对 GAN Loss 的高频细节增益进行论述，说明不加 GAN Loss 时的过度平滑现象。
  - **附录（`supplementary.tex`）**：
    - **判别器网络架构**：提供判别器 $D_\psi$ 的架构细节（PatchGAN 感受野、卷积层通道数等）和对抗训练超参数（$\gamma$ 权重，lr 设定等）。
    - **定性对比大图**：开辟专门章节展示有/无 GAN Loss 的高精局部渲染对比图。

---

### 问题 3：Negative Source Branch 解释与轨迹可视化
- **现状**：Reinforced Editing 中的 negative source branch 是核心创新点之一，审稿人需要更直观的可视化和原理解释。
- **目标**：在正文中进行理论澄清（极致精炼），在 Supplementary 中提供直观的轨迹对比图。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - 在 `Sec. 3.3` 的公式 `red_diff_velocity` 附近，补充对 negative source branch 物理意义的简洁文字解释。**控制在 3-4 句内**以节省篇幅：“The negative source branch pushes the latent representation away from unconditioned states, suppressing semantic hallucinations and locking the underlying geometric structure during 2D guidance.”
  - **附录（`supplementary.tex`）**：
    - 插入 `figures_rebuttal/comparison_grid.png`，并对有/无负引导的轨迹表现差异（如颜色过饱和、细节丢失、结构变化等）进行成因分析。

---

### 问题 4：Toy4K 定量评估缺失
- **现状**：rebuttal 中承诺补充在 Toy4K 数据集上的定量评估结果。
- **目标**：在正文中呈现 Toy4K 核心指标，增强实验说服力.
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - **严禁与 Table 1 合并**：因指标类型不符，明文禁止两表合并，避免表头混乱。
    - **建立独立 Table 2**：在 `Sec. 4.2 Main Results` 中加入一个独立的、紧凑的单栏表格 `Table 2`（呈现 CLIP, $FD_{\text{inc}}$, $FD_{\text{dino}}$, $KD_{\text{dino}}$ 指标）。
    - **命名严格一致**：方法名称在 Table 2、Table 1 以及主文中必须严格保持一致：`Pretrained` 或 `Pretrained (Trellis)`，`Photo3D`，`OREO (Ours)` 以及消退变体 `w/o Noise Update`。
  - **附录（`supplementary.tex`）**：
    - 无需此内容。

---

### 问题 5：Human Preference Study（人评）细节与结果
- **现状**：rebuttal 中承诺补充人评结果，但主文空间极度紧张。
- **目标**：在正文中给出人评的核心结论，并在 Supplementary 中提供完整细节。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - 用 1-2 句简短文字总结人评核心胜出率（OREO 41% vs Photo3D 36% vs Pretrained 23%），并用 `\cite` 标注完整细节见 Supplementary。
  - **附录（`supplementary.tex`）**：
    - 详尽展开人评细节：
      - 评判维度：Fidelity（多视角材质与细节）、Consistency（多视角 3D 一致性）、Identity（参考图还原度）。
      - 参与者信息：20名参与者（包括 3D 重建与图形学领域专业学者占比）。
      - 统计检验与样本划分（100个样本等）。

---

### 问题 6：计算开销（Computational Overhead）与数据集细节
- **现状**：rebuttal 承诺补充训练/推理的计算开销（VRAM、速度、异步服务等）以及数据集构建细节（2000+ 图像的筛选、划分、prompt 原文等）。
- **目标**：补充 these 实现细节，并交代判别器的设计，消除审稿人疑虑。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - **计算开销**：极力精简，仅保留一行：“The system runs efficiently on a single consumer GPU; please refer to the Supplementary Material for detailed breakdowns on training time, VRAM, and service overlapping.”，以节省空间。
    - **数据集统计**：在数据集部分补充简要的关键统计信息（2,000+ 图像、train/eval split、筛选原则）。
  - **附录（`supplementary.tex`）**：
    - **计算开销 Breakdown**：给出详细的计算开销表格（训练时间、推理延迟、VRAM 10GB with gradient checkpointing、异步服务重叠优化比例）。
    - **判别器网络架构**：在 Implementation Details 中，提供判别器 $D_\psi$ 的架构细节（PatchGAN 感受野、卷积层通道数）和对抗训练超参数（$\gamma$ 权重，lr 设定等）。
    - 给出 Qwen-Image-Edit 和 NanoBanana 的 exact prompts。
    - 说明数据集的收集与 release 计划（提供 stable link）。

---

### 问题 7：Failure Cases 与 Limitations 讨论
- **现状**：rebuttal 承诺补充对方法局限性（如 noise update 可能继承 2D 编辑器的颜色偏差）和失败案例的讨论。
- **目标**：在论文中加入客观的局限性分析，提升论文的学术严谨性。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - 在末尾补充一小段 Limitations 讨论，重点提及 noise update 在极端情况下可能继承 color bias，并导致 back views 的某些不协调。
  - **附录（`supplementary.tex`）**：
    - 提供 failure cases 的具体视觉实例与成因分析。

---

### 问题 8：正文页数超标与“双重脱水”控页备份计划
- **现状**：当前编译出的 `camera_ready.pdf` 正文部分（不含 references）为 15 页，且新加的 GAN Loss、Related Work 等内容会带来明显的 Method 膨胀，必须有稳健、极具可操作性的控页方案。
- **目标**：在其他所有问题都解决、内容全部合并后，将正文严格压缩至 14 页以内，且不添加 Appendix。
- **正文与附录分工**：
  - **正文（`camera_ready.tex`）**：
    - 进行文字精简与排版微调，删除冗余的叙述和不必要的过渡句，微调表格的 `tabcolsep` 以及图表的 `vspace` 间距。
  - **附录（`supplementary.tex`）**：
    - **第一重控页：Fig. 5 搬迁**：在 `camera_ready.tex` 中，将体积巨大的 `Fig. 5` (Qualitative ablation study on RE parameters，大约半页多空间) 整体搬迁至 `supplementary.tex`。主文中直接调用定量消退结果 `Table 3`。
    - **第二重控页（备份计划）：Fig. 7 搬迁与 Algorithm 2 压缩**：
      - 若空间依然吃紧，**将正文体积庞大、横跨双栏的消退分析大图 `Fig. 7 (Ablation overview)` 也整体搬迁至 `supplementary.tex`**，正文仅保留定量表 Table 3 的文字说明（释放近半页）。
      - 将 `Algorithm 2 (Closed-loop Optimization)` 骨架移至 Supplementary，正文仅保留最核心的 `Algorithm 1 (Reinforced Editing)`。
