# Plan: OREO Camera-Ready Problem 2 - GAN Loss in Method

## 目标

在 `camera_ready.tex` 的 `Sec. 3.4 Generator Optimization via Pseudo-GT Supervision` 中引入 GAN / adversarial loss，使 Method 闭环从当前的

```tex
\mathcal{L}_{total} = \mathcal{L}_{sup} + \lambda \mathcal{L}_{reg}
```

扩展为：

```tex
\mathcal{L}_{total}
= \mathcal{L}_{sup}
+ \lambda \mathcal{L}_{reg}
+ \gamma \mathcal{L}_{adv}.
```

采用 **方案 4：Pseudo-GT Quality Transfer** 作为正文叙事主线：edited pseudo-GT $x^{\texttt{tgt}}$ 承载 2D editing prior 产生的高保真外观细节；MSE regression 能稳定传递整体结构和颜色，但可能削弱高频纹理；因此加入 auxiliary adversarial loss，让 rendered prediction $x^{\texttt{src}}$ 不只在 pixel space 接近 $x^{\texttt{tgt}}$，也在 appearance discriminator 下接近它。

## 关键发现（Explore 阶段）

- `camera_ready.tex` 当前 `Algorithm 2` 只计算 $\mathcal{L}_{sup}$、$\mathcal{L}_{reg}$ 并更新 generator 参数 $\theta$。
- `camera_ready.tex` 当前 `Sec. 3.4` 只包含 MSE pseudo-GT supervision 和 velocity-field regularization。
- `Sec. 4.3` 当前 ablation 只覆盖 `w/o Regularization`、`w/o Noise Update` 和 `replace MSE with DMD`，目前没有 `w/o GAN loss` 的图或定量结果。
- `edit4shape` 实现中的 discriminator 不是普通 PatchGAN，而是 `DINOv3sDiscriminator`：frozen DINOv3-S encoder + 4 个 trainable multi-scale heads，取中间 hidden states 做 projected discrimination。
- GAN loss 实现为 BCE-with-logits：edited tensor / $x^{\texttt{tgt}}$ 作为 real，rendered `comp_rgb` / $x^{\texttt{src}}$ 作为 fake。
- 当前实现超参保留 `gan=1.0`、`gan_lr=2e-5`，具体超参更适合放 Supplementary。

## 相关代码

| 文件 | 位置 | 作用 |
|------|------|------|
| `camera_ready.tex` | `Algorithm 2` | 加入 discriminator $D_\psi$ 与交替优化步骤 |
| `camera_ready.tex` | `Sec. 3.4` | 加入 pseudo-GT quality transfer 叙事、adversarial loss、discriminator loss 和总目标 |
| `camera_ready.tex` | `Sec. 4.3` | 只加入保守实验说明，不新增无数据支撑的 `w/o GAN` 表格行 |
| `supplementary.tex` | `Implementation and Dataset Details` | 加入 DINOv3-S projected discriminator 细节与后续定性对比占位 |

## 实现步骤

- [x] Step 1: 更新 `Algorithm 2 (Closed-loop Optimization)`，加入 $D_\psi$ 与交替优化步骤。
- [x] Step 2: 更新 `Sec. 3.4`，采用 pseudo-GT quality transfer 叙事，加入 DINOv3-S projected discriminator 描述、$\mathcal{L}_{adv}$、$\mathcal{L}_{disc}$ 与新的 $\mathcal{L}_{total}$。
- [x] Step 3: 更新 `Sec. 4.3` 的消融入口文字，保守说明 adversarial term 的作用边界，不新增无数据支撑的表格项。
- [x] Step 4: 更新 `supplementary.tex`，加入 adversarial training details 与定性对比占位。
- [x] Step 5: 编译 `camera_ready.tex` 与 `supplementary.tex`，检查 equation / algorithm / reference 是否正常。

## Code Diff（草案）

### `camera_ready.tex`

#### 中文修改意图

在算法里加入判别器 $D_\psi$，每轮先更新判别器，再用 $\mathcal{L}_{sup} + \lambda\mathcal{L}_{reg} + \gamma\mathcal{L}_{adv}$ 更新 generator。

#### 英文版 TeX diff

```diff
@@ Algorithm 2: Closed-loop Optimization via Dynamic Pseudo-GTs
-    \Require Generator $G_\theta$, Frozen rollout generator $G_{\theta_{pre}}$, 2D editor $\mathcal{E}_\phi$, Dataset $\mathcal{S}$, Learning rate $\eta$
+    \Require Generator $G_\theta$, Frozen rollout generator $G_{\theta_{pre}}$, 2D editor $\mathcal{E}_\phi$, discriminator $D_\psi$, Dataset $\mathcal{S}$, learning rates $\eta_G,\eta_D$
     \Ensure Optimized parameters $\theta^*$
@@
         \State Obtain $x^{\texttt{tgt}}$ via Algorithm~\ref{alg:red} from $x^{\texttt{src}}$ and $x^{\texttt{ref}}$ \Comment{\texttt{Reinforced Editing}}
+        \State Update $D_\psi$ using $x^{\texttt{tgt}}$ as real and $x^{\texttt{src}}$ as fake \Comment{\texttt{Adversarial Step}}
         \State $\mathcal{L}_{sup} = \| x^{\texttt{src}} - x^{\texttt{tgt}} \|^2$ \Comment{\texttt{Supervision}}
         \State $\mathcal{L}_{reg} = \| v_\theta(z_t) - v_{\theta_{pre}}(z_t) \|^2$ \Comment{\texttt{Regularization}}
-        \State $\theta \leftarrow \theta - \eta \nabla_\theta (\mathcal{L}_{sup} + \lambda \mathcal{L}_{reg})$ \Comment{\texttt{Update parameters}}
+        \State Compute $\mathcal{L}_{adv}$ by classifying $x^{\texttt{src}}$ as real with $D_\psi$
+        \State $\theta \leftarrow \theta - \eta_G \nabla_\theta (\mathcal{L}_{sup} + \lambda \mathcal{L}_{reg} + \gamma \mathcal{L}_{adv})$ \Comment{\texttt{Update generator}}
```

#### 中文修改意图

在 `Sec. 3.4` 使用方案 4 的叙事，并用三个短 `\textbf{...}` 块提升可读性：`\textbf{Pixel Supervision.}` 说明 $\mathcal{L}_{sup}$ 是稳定的 view-aligned 主监督；`\textbf{Adversarial Loss.}` 指出 $x^{\texttt{tgt}}$ 含有 2D editing prior 产生的高频细节，而 MSE 可能削弱这些细节，因此用 adversarial loss 做 appearance-level transfer；`\textbf{Final Objective.}` 汇总 $\mathcal{L}_{reg}$ 和最终总目标。

#### 英文版 TeX diff

```diff
@@ Generator Optimization via Pseudo-GT Supervision
+\textbf{Pixel Supervision.}
 The supervision loss is defined as
 \begin{equation}
 \mathcal{L}_{sup} = \| x^{\texttt{src}} - x^{\texttt{tgt}} \|^2
 \end{equation}
-and backpropagated through the differentiable renderer and decoder to update $\theta$.
+and is backpropagated through the differentiable renderer and decoder to update $\theta$.
+This pixel-level objective provides stable view-aligned supervision, allowing the generator to inherit the structure, color, and coarse appearance of the edited pseudo-GT.
+
+\textbf{Adversarial Loss.}
+However, the edited view $x^{\texttt{tgt}}$ also contains high-frequency texture details produced by the 2D editing prior, which may be weakened by direct regression due to the averaging effect of MSE.
+To better transfer such fine-grained appearance cues, we introduce an auxiliary adversarial loss that encourages the rendered prediction $x^{\texttt{src}}$ to be indistinguishable from $x^{\texttt{tgt}}$ under an appearance discriminator.
+We instantiate the discriminator $D_\psi$ as a projected discriminator on frozen DINOv3-S features, with lightweight trainable heads attached to multi-scale intermediate representations.
+
+The generator-side adversarial loss is
+\begin{equation}
+\mathcal{L}_{adv}(G_\theta)
+= \mathbb{E}_{x^{\texttt{src}}}
+\left[\operatorname{BCE}(D_\psi(x^{\texttt{src}}), 1)\right].
+\end{equation}
+The discriminator is optimized with edited pseudo-GTs as real samples and rendered predictions as fake samples:
+\begin{equation}
+\mathcal{L}_{disc}(D_\psi)
+= \mathbb{E}_{x^{\texttt{tgt}}}
+\left[\operatorname{BCE}(D_\psi(x^{\texttt{tgt}}), 1)\right]
++ \mathbb{E}_{x^{\texttt{src}}}
+\left[\operatorname{BCE}(D_\psi(x^{\texttt{src}}), 0)\right].
+\end{equation}
+\textbf{Final Objective.}
 To preserve geometric stability, we regularize the velocity field deviation from the pre-trained prior:
@@
 where $v_{\theta_{pre}}$ is the velocity field induced by the frozen pre-trained generator.
-The final objective is $\mathcal{L}_{total} = \mathcal{L}_{sup} + \lambda \mathcal{L}_{reg}$.
+The final objective is $\mathcal{L}_{total} = \mathcal{L}_{sup} + \lambda \mathcal{L}_{reg} + \gamma \mathcal{L}_{adv}$.
 The overall training procedure is summarized in Algorithm~\ref{alg:oreo}.
```

#### 中文修改意图

不加无数据的 `w/o GAN` 表格行，只加一句保守说明：完整 OREO 使用 adversarial appearance alignment 来更完整地转移 edited pseudo-GT 的高频细节。

#### 英文版 TeX diff

```diff
@@ Ablation Study and Analysis
 Specifically, ``w/o Regularization'' removes $\mathcal{L}_{reg}$, ``w/o Noise Update'' removes the dynamic noise update in Eq.~\ref{eq:red_dynamic_noise}, and ``replace MSE with DMD'' replaces our default direct pseudo-GT supervision with a score-distillation style objective.
+Full OREO also includes an auxiliary adversarial term to better transfer high-frequency details from the edited pseudo-GTs beyond pixel-level regression; discriminator and training details are provided in the Supplementary Material.
 As shown in Table~\ref{tab:ablation_quantitative}, all three variants underperform Full OREO, and removing regularization already causes a consistent drop across CLIP, DINO, MANIQA, and MUSIQ, validating that geometry anchoring is necessary during post-training.
```

### `supplementary.tex`

#### 中文修改意图

在附录 Implementation Details 里补 GAN 的真实实现：frozen DINOv3-S projected discriminator，只训练 multi-scale heads，BCE，real/fake 定义清楚。

#### 英文版 TeX diff

```diff
@@ Implementation and Dataset Details
 \section{Implementation and Dataset Details}
 \label{sec:implementation_details}
 Placeholder for implementation details, prompts, and dataset statistics.
+
+\subsection{Adversarial Training Details}
+We implement the discriminator $D_\psi$ as a projected discriminator built on a frozen DINOv3-S image encoder.
+The encoder parameters are fixed, and lightweight trainable heads are attached to multiple intermediate feature maps for multi-scale real/fake classification.
+During discriminator training, edited pseudo-GT views $x^{\texttt{tgt}}$ are treated as real samples, while rendered predictions $x^{\texttt{src}}$ are treated as fake samples.
+We use a BCE adversarial objective for both generator and discriminator optimization.
+In our implementation, the adversarial weight is $\gamma=1.0$, and the discriminator learning rate is $2\times10^{-5}$.
+
+\subsection{Qualitative Effect of Adversarial Loss}
+Placeholder for qualitative comparisons between training with and without the adversarial loss.
```

## 写作边界

- 不新增 `w/o GAN loss` 的定量表格行，因为目前没有对应实验指标。
- 不写具体“有 GAN 比无 GAN 提升多少”或“显著改善某一行样例”的结论，因为目前没有对应定性图。
- 正文只需要解释为什么加 GAN、GAN 如何和 pseudo-GT supervision 互补；DINOv3-S heads、BCE 和超参放 Supplementary。

## 状态

**当前阶段**: Done
