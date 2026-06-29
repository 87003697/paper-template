---
name: problem-6-overhead-dataset
overview: 为 Problem 6 制定 camera-ready 补充方案：主文只加极短 dataset/overhead 指引，Supplementary 承载计算开销、数据集构建、prompts 与判别器实现细节；所有未确认数值先列为 TBD，不编造结果。
todos:
  - id: collect-tbd
    content: 收集实现前必须补齐的 profiling、dataset、prompts、discriminator 细节
    status: pending
  - id: draft-main
    content: 为 `camera_ready.tex` 草拟 1-2 句主文 dataset/overhead 指引
    status: pending
  - id: draft-supp
    content: 为 `supplementary.tex` 设计 dataset construction、prompts、overhead、adversarial details 小节结构
    status: pending
  - id: avoid-unsupported
    content: 确认所有未提供数据只保留在计划中，不写入论文正文
    status: pending
  - id: validate-after-implementation
    content: 实现后编译主文和附录，检查引用、页数与残留占位
    status: pending
isProject: false
---

# Problem 6: Computational Overhead and Dataset Details Plan

## 目标
回应 rebuttal 中关于 computational overhead 与 dataset details 的承诺，同时保持主文页数稳定。写法上避免 checklist 式的 “see Supplementary” 堆叠：主文把数据设定自然嵌入 `Setup`，把 overhead 作为训练工程实现的一句补充；Supplementary 再承载完整 profiling breakdown、数据构建说明、exact prompts、release 信息和 discriminator details。

## 关键发现
- 总计划文件是 `[.agents/plan/camera-ready.md](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/.agents/plan/camera-ready.md)`，Problem 6 当前 pending，既包含 overhead/dataset，也包含 prompts 和 discriminator details。
- `[rebuttal.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/rebuttal.tex)` 中可确认的计算开销承诺只有：9-step image editing sequentially accounts for 81% of each training iteration；async service + next-batch rollout overlap reduces effective wait to 45% on same hardware with negligible quality impact。
- `[camera_ready.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/camera_ready.tex)` 的 `Sec. 4.2 Setup` 已写入核心数据设定：over 2,000 manually collected mobile-phone images、100-example held-out Conceptual Design Dataset、no paired 3D GT、Photo3D 使用同一 Trellis backbone 和同一 training set。
- `[supplementary.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/supplementary.tex)` 的 `Implementation and Dataset Details` 仍有占位句，后面已有 Toy4K 小节与简短 Adversarial Training Details；Problem 6 应主要替换该占位并扩写实现细节。
- 当前没有可确认的 training time、inference latency、完整 VRAM、hardware spec、exact prompts、dataset release link 或筛选统计。因此这些只能作为 TBD 信息清单，不能先写成确定论文内容。

## 推荐内容分工

### 主文 `camera_ready.tex`
- 先微调 `Sec. 4.2 Setup` 的现有数据集句子，使其更完整地交代：训练集是 2,000+ manually collected mobile-phone images，经过 manual filtering 以强调 rich appearance details / realistic user scenarios；evaluation 使用 100 held-out Conceptual Design Dataset，且严格不进入训练。
- overhead 不要单独生硬插一句 “see Supplementary”。更自然的写法是在 setup 段末尾接一句：由于 editing calls 只发生在 post-training，OREO 可以把 editor 封装为 async service，并与 next-batch rollout overlap，从而降低实际等待时间；详细 profiling 放 Supplementary。
- 不在主文加表格，不写未确认的 training time / VRAM / latency 数字，以免影响页数和可信度。

### Supplementary `supplementary.tex`
- 替换 `Implementation and Dataset Details` 下的占位句，但不要写成目录式入口。直接用一段话说明这些 implementation details are used for the main experiments，并过渡到后续小节。
- 新增 `Conceptual Design Dataset Construction` 小节：写数据来源、筛选原则、训练/评估划分、无 3D GT、100 held-out evaluation split 与 release plan。
- 新增 `Editing Prompts and Evaluation Prompts` 小节：列出 Qwen-Image-Edit、NanoBanana、RE 使用的 exact prompt templates；若用户未提供 exact prompts，先只在 plan 中保留 TBD，不进入论文正文。
- 新增 `Computational Overhead` 小节：用一个紧凑表或短段落报告 confirmed profiling。当前只能确定 81% sequential editing overhead 与 async overlap 后 45% effective wait；其他字段等用户补充。
- 扩写 `Adversarial Training Details`：保留当前 DINOv3-S projected discriminator 设定，补充 frozen encoder、multi-scale trainable heads、real/fake definition、BCE objective、`gamma=1.0`、`lr=2e-5`、更新频率；如果判别器具体层数/heads 未确认，不写 PatchGAN 卷积层通道数。

## 实现前必须补齐的信息
- Profiling：GPU 型号、batch size、resolution、training iteration wall-clock、editing call latency、Trellis rollout/render time、generator update time、VRAM peak、是否启用 gradient checkpointing、async service 的 measured effective wait。
- Dataset：训练图像精确数量、来源类别是否能公开描述、筛选规则、去重/过滤流程、train/eval split、release link 或 release wording。
- Prompts：Qwen-Image-Edit original prompt、NanoBanana prompt、RE minimal prompt、是否采用 `white background` 版本，以及训练和评估是否完全一致。
- Discriminator：DINOv3-S feature layers / heads / update frequency / optimizer 参数，如没有实现级细节，只写已有可确认的 projected discriminator 高层说明。

## TeX Code Diff 草稿

### 中文说明

#### `camera_ready.tex`

主文空间很紧，但筛选标准是回应 dataset detail 的关键信息，应该用一个短语保留。核心是把 Problem 6 的数据设定自然并入 `Sec. 4.2 Main Results / Setup`：

- 原有句子已经说了 `over 2,000 manually collected mobile-phone images`、`no paired 3D GT`、`100-example held-out split`，但 `mobile-phone images` 与实际数据来源不符，需要改成线上来源的表述。
- 修改方向是压缩成一条 setup 信息：训练集有 `\texttt{TODO: number}` 张从线上来源收集的 image-only images、没有 paired 3D GT，并用一个短语说明人工筛选标准（`\texttt{TODO: filtering criteria}`）。
- 评估集继续写 `\texttt{TODO: evaluation split size}` 个 Conceptual Design Dataset 样本，但不强调 “strictly held out from training”。
- 数据来源细节、release、prompts、profiling 全部下沉 Supplementary。
- 主文不单独解释 overhead 数字，只在一句话里说 implementation details / prompts / profiling 见 Supplementary。

#### `supplementary.tex`

附录的 `Implementation and Dataset Details` 现在有一行 placeholder，需要替换成完整实现细节。建议顺序：

1. `Conceptual Design Dataset Construction`：说明训练集与 100 held-out evaluation split 的构建逻辑。
2. `Editing Prompts`：等用户提供 exact prompts 后再填；没有 exact prompts 时不要把猜测写进正文。
3. `Computational Overhead`：先放表格骨架，所有 profiling 数字和 hardware 都用 `TODO` 占位。
4. `Adversarial Training Details`：扩写已有 discriminator 段落，但 feature backbone、heads、lr、gamma、update frequency 都用 `TODO` 占位，避免写死未确认实现。

### English LaTeX Diff

下面使用真正的 unified diff / git diff 风格。Markdown 渲染时，`-` 行应显示为红色删除，`+` 行应显示为绿色新增。

#### `camera_ready.tex` (+2/-3)

中文翻译：
在主文 `Setup` 中，只保留数据集最关键的信息：训练集是 `TODO` 数量、从线上来源收集的 image-only images，没有 paired 3D GT，并经过人工筛选以满足 `TODO` 筛选标准；评估集是 `TODO` 数量的 Conceptual Design Dataset。数据来源细节、prompt 和 profiling 不在正文展开，只用一句话指向 Supplementary。

```diff
diff --git a/camera_ready.tex b/camera_ready.tex
--- a/camera_ready.tex
+++ b/camera_ready.tex
@@ -454,10 +454,9 @@ Having validated the effectiveness of Reinforced Editing in providing structure-p
 \textbf{Setup.}
 We utilize Trellis as the 3D generator backbone and Qwen-Image-Edit as the 2D editor.
-To evaluate post-training under image-only supervision without 3D ground truth, we build an in-the-wild training set with over 2,000 manually collected mobile-phone images, where no paired 3D GT is available.
-For evaluation, we use the same 100-example held-out split introduced in Sec.~\ref{4_1}, namely the \textit{Conceptual Design Dataset}.
-This benchmark contains challenging, imaginative objects (e.g., stylized characters, fantasy artifacts, and unconventional structures) with rich appearance details, and all evaluation instances are strictly held out from the training set.
+To evaluate post-training under image-only supervision without 3D ground truth, we build a training set with \texttt{TODO: number of training images} images collected from online sources, filtered for \texttt{TODO: filtering criteria}, where no paired 3D GT is available.
+For evaluation, we use the \texttt{TODO: evaluation split size}-example \textit{Conceptual Design Dataset} introduced in Sec.~\ref{4_1}.
 We compare OREO against the pre-trained baseline and Photo3D. For a fair comparison, we implement Photo3D using the same Trellis backbone and train it on the same in-the-wild training set; the Conceptual Design Dataset is used only for evaluation.
+Detailed dataset construction, editing prompts, and training-time profiling are provided in the Supplementary Material.
 
 \textbf{Quantitative Evaluation.}
```

#### `supplementary.tex` (+41/-1)

中文翻译：
在 Supplementary 的 `Implementation and Dataset Details` 下替换占位句，新增三个小节。`Conceptual Design Dataset Construction` 说明训练集数量、来源、筛选目标、排除标准、held-out split 和 release 信息，全部用 `TODO` 保留。`Editing Prompts` 列出 Reinforced Editing、Qwen-Image-Edit 和 NanoBanana 的 exact prompt 占位。`Computational Overhead` 说明后训练阶段的编辑调用开销，并放一个表格骨架，所有 step 数、sequential overhead、async wait、hardware 和备注都用 `TODO`。

```diff
diff --git a/supplementary.tex b/supplementary.tex
--- a/supplementary.tex
+++ b/supplementary.tex
@@ -120,7 +120,47 @@ Since only aggregate preference ratios are recorded, we report the descriptive pr
 
 \section{Implementation and Dataset Details}
 \label{sec:implementation_details}
-Placeholder for implementation details, prompts, and dataset statistics.
+This section provides the implementation details used in our main experiments, including dataset construction, editing prompts, computational profiling, and adversarial training settings.
+
+\subsection{Conceptual Design Dataset Construction}
+\label{sec:dataset_construction}
+We construct an in-the-wild image collection to support image-only post-training without paired 3D supervision.
+The training split contains \texttt{TODO: number of training images} images collected from online sources and filtered to emphasize \texttt{TODO: filtering goals}.
+Images with \texttt{TODO: exclusion criteria} are removed during filtering.
+For evaluation, we use a disjoint \texttt{TODO: evaluation split size}-example held-out split, referred to as the Conceptual Design Dataset in the main paper.
+This evaluation split contains \texttt{TODO: evaluation-set characteristics}, and is never used for training either OREO or the Photo3D baseline.
+\texttt{TODO: dataset release statement or stable link.}
+
+\subsection{Editing Prompts}
+\label{sec:editing_prompts}
+We use fixed editing instructions for all compared 2D feedback sources to avoid prompt-specific tuning on individual examples.
+The exact prompts are listed below:
+\begin{itemize}
+  \item Reinforced Editing: \texttt{TODO: exact RE prompt}
+  \item Qwen-Image-Edit: \texttt{TODO: exact Qwen-Image-Edit prompt}
+  \item NanoBanana: \texttt{TODO: exact NanoBanana prompt}
+\end{itemize}
+\texttt{TODO: prompt consistency statement, e.g., whether training/evaluation use the same prompt.}
+
+\subsection{Computational Overhead}
+\label{sec:computational_overhead}
+OREO introduces additional 2D editing calls during generator post-training.
+When executed sequentially, the \texttt{TODO: editing-step count}-step image editing process accounts for \texttt{TODO: sequential overhead} of each training iteration.
+In practice, we wrap the editor as \texttt{TODO: async service description} and overlap editing calls with \texttt{TODO: overlapped training component}.
+This reduces the effective waiting time to \texttt{TODO: async effective wait} on \texttt{TODO: hardware}, with \texttt{TODO: quality-impact statement}.
+
+\begin{table}[t]
+  \centering
+  \caption{Computational overhead of the editing component during OREO post-training.}
+  \label{tab:computational_overhead}
+  \begin{tabular}{@{}lccp{0.32\linewidth}@{}}
+    \toprule
+    Component & Sequential Cost & Effective Wait & Note \\
+    \midrule
+    \texttt{TODO: component} & \texttt{TODO: sequential cost} & \texttt{TODO: effective wait} & \texttt{TODO: note} \\
+    \bottomrule
+  \end{tabular}
+\end{table}
 
 \subsection{Benchmark Evaluation on Toy4K}
 \label{sec:toy4k_details}
```

#### `supplementary.tex` (+7/-3)

中文翻译：
扩写 Supplementary 中已有的 `Adversarial Training Details`，但不写死具体实现。判别器 backbone/design、encoder 是否冻结、使用哪些 feature layers、判别器更新频率、`\gamma`、判别器学习率、冻结组件和 online pairing strategy 全部用 `TODO` 占位，保留真实/伪样本定义和 adversarial branch 不需要额外 3D 监督的论述。

```diff
diff --git a/supplementary.tex b/supplementary.tex
--- a/supplementary.tex
+++ b/supplementary.tex
@@ -152,10 +192,13 @@ The degradation of the w/o Noise Update variant further supports the role of dyn
 \subsection{Adversarial Training Details}
 We implement the discriminator $D_\psi$ as a projected discriminator built on a frozen DINOv3-S image encoder.
-The encoder parameters are fixed, and lightweight trainable heads are attached to multiple intermediate feature maps for multi-scale real/fake classification.
+We implement the discriminator $D_\psi$ as \texttt{TODO: discriminator backbone/design}.
+The encoder parameters are \texttt{TODO: frozen or trainable}, and lightweight trainable heads are attached to \texttt{TODO: feature layers} for multi-scale real/fake classification.
 During discriminator training, edited pseudo-GT views $x^{\texttt{tgt}}$ are treated as real samples, while rendered predictions $x^{\texttt{src}}$ are treated as fake samples.
-We use a BCE adversarial objective for both generator and discriminator optimization.
-In our implementation, the adversarial weight is $\gamma=1.0$, and the discriminator learning rate is $2\times10^{-5}$.
+The discriminator is updated \texttt{TODO: update frequency} using the BCE objective described in the main paper.
+For the generator update, the adversarial term encourages $x^{\texttt{src}}$ to be classified as real, complementing the pixel-level pseudo-GT loss with high-frequency appearance supervision.
+In our implementation, the adversarial weight is $\gamma=\texttt{TODO: gamma}$, and the discriminator learning rate is \texttt{TODO: discriminator learning rate}.
+We keep \texttt{TODO: frozen components} frozen to reduce memory overhead and avoid overfitting the discriminator to the limited edited-view distribution.
+All real/fake pairs are formed \texttt{TODO: online pairing strategy}, so the adversarial branch does not require any additional real 3D supervision.
 
 \subsection{Qualitative Effect of Adversarial Loss}
 Placeholder for qualitative comparisons between training with and without the adversarial loss.
```

## 风险与取舍
- 如果把未确认数值写进论文，会比不写更危险；当前计划选择“先列 TBD，拿到 profiling 后再落文”。
- 主文已经接近页数上限，Problem 6 不应新增表格；所有复现性细节放 Supplementary。
- `Adversarial Training Details` 已存在一段内容，后续应扩写而不是另开重复小节，避免 Supplementary 结构松散。
- Dataset release link 如果现在没有稳定链接，建议写成 `We will release the dataset upon acceptance.`，不要伪造 URL。

## 验证
实现阶段完成后编译 `camera_ready.tex` 与 `supplementary.tex`，检查 Supplementary section refs、表格编号、overfull warnings、正文页数，以及是否仍存在占位 `Placeholder` 或 `TBD`。
