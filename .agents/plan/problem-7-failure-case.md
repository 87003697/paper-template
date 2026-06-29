---
name: problem-7-failure-case
overview: 为 Problem 7 制定 camera-ready 修改方案：正文补充极短、诚实的 limitations 段落，Supplementary 重点分析 face-like objects 的 viewpoint drift failure case，并补充 color/style bias 与 weakly constrained views 的原因分析。
todos:
  - id: main-limitations
    content: 在 `camera_ready.tex` 的 Conclusion 后加入极短 Limitations 段落
    status: completed
  - id: supp-failure-analysis
    content: 替换 `supplementary.tex` 的 Limitations/Failure Cases placeholder
    status: completed
  - id: figure-decision
    content: 确认是否加入 face-orientation failure-case figure，默认无可靠图则不加
    status: completed
  - id: plan-status
    content: 执行后更新 Problem 7 计划状态与编译检查
    status: completed
isProject: false
---

# Problem 7 Failure Cases and Limitations Plan

## 目标
回应 rebuttal 中关于 failure cases 与 editing-guidance limitations 的承诺，在不明显增加正文页数的前提下，补充一段客观局限性讨论，并在 Supplementary 中重点展开“人像/角色面部在编辑后朝向镜头，而不是保持原本 3D 朝向”的 failure case。

## 关键发现
- 总计划位于 `[.agents/plan/camera-ready.md](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/.agents/plan/camera-ready.md)`，Problem 7 当前要求：`camera_ready.tex` 加 Limitations，`supplementary.tex` 写 Failure Cases。
- `[rebuttal.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/rebuttal.tex)` 明确承诺补充 failure cases，并给出核心局限：noise update 会加强与 2D editor prior 的对齐，但在 golem 等样例上可能继承 color bias。
- `[camera_ready.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/camera_ready.tex)` 目前没有单独 Limitations；最自然位置是 `Conclusion` 后、`Future Work` 前，新增一个很短的 `\textbf{Limitations.}` 段落。
- `[supplementary.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/supplementary.tex)` 已有 `\section{Limitations and Failure Cases}` 和 `\label{sec:limitations_failure}`，但内容仍是 placeholder，正好替换。
- 用户补充的关键 failure case：当编辑人像或角色类对象时，2D editor 可能倾向 canonical portrait composition，把面部转向当前相机，而不是保持 3D 对象“朝前”的原始方向。这会造成局部面部细节变好，但跨视角面部朝向不一致。
- 当前仓库没有命名为 failure/bias 的图像文件；`figures_rebuttal/` 有大量 multi-view comparison 图，但需要实施前确认哪一个样例可作为 face-orientation failure-case 图，避免把正常 qualitative comparison 强行解释成 failure。

## 推荐正文策略
- 不新增独立 `\section{Limitations}`，避免正文结构膨胀；在 `Conclusion` 后新增 3-4 句 `\textbf{Limitations.}`。
- 内容只写确定且审稿相关的限制：
  - OREO 依赖 2D editing prior，极端情况下会继承 editor 的 compositional / viewpoint bias。
  - 对 face-like objects 或 characters，2D editor 可能把面部转向相机，而不是保持源 3D 视角方向。
  - 复杂材质上仍可能继承 color/style bias；弱约束背面视角也可能出现局部纹理不一致。
  - 失败案例与原因分析见 Supplementary。
- 保留已有 `Future Work`，但可轻微压缩其第一句，避免新增段落导致页数压力。

## 推荐 Supplementary 策略
- 替换 `[supplementary.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/supplementary.tex)` 中 `Limitations and Failure Cases` 的 placeholder。
- 建议写成 2-3 个短小类目，而不是泛泛自我批评：
  - `Viewpoint Drift for Face-like Objects`：2D editor 可能把人脸/角色正面转向当前相机，提升面部局部细节但破坏 3D 朝向一致性。
  - `Inherited Color and Style Bias`：noise update 将 pseudo-GT 拉向 2D editor prior，在 golem/stone/metallic 等材质上可能引入色调偏移。
  - `Weakly Constrained Views and Fine Structures`：单视角或局部视角编辑反馈可能无法完全约束背面与细结构，导致 back views 的纹理密度、局部装饰或细长结构不一致。
- 如果用户提供或指定 face-orientation failure 图，再加入一个紧凑 figure；如果没有可靠图，不强行放图，只写文字分析。

## 实现步骤
1. 在 `[camera_ready.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/camera_ready.tex)` 的 `Conclusion` 后插入 `\textbf{Limitations.}`，控制在一个短段落。
2. 在正文 limitations 末尾加一句指向 Supplementary 的 `Limitations and Failure Cases`，复用已有 `sec:limitations_failure` label。
3. 替换 `[supplementary.tex](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/supplementary.tex)` 的 placeholder，写成上述三类 failure analysis，并把 face-like viewpoint drift 放在第一类。
4. 若有确认的 face-orientation failure-case 图像，增加 `figure` 环境和 caption；若没有，则保持文字版，不添加 unsupported visual claim。
5. 更新 `[.agents/plan/camera-ready.md](/Users/zhiyuanma/Desktop/OREO_ECCV/paper-template/.agents/plan/camera-ready.md)` 中 Problem 7 的完成状态，并可新建/补充 `problem-7-failure-case.md` 执行记录。
6. 编译 `camera_ready.tex` 与 `supplementary.tex`，检查 undefined reference、页数和是否仍有 `Placeholder`。

## TeX Code Diff 草稿

### 中文说明

#### `camera_ready.tex`

主文只新增一个紧凑的 `\textbf{Limitations.}` 段落，放在 `Conclusion` 和 `Future Work` 之间。这个位置比另开 section 更省空间，也不会破坏现有 ECCV 正文结构。段落重点回应 2D editor prior 的 compositional / viewpoint bias：在人像或角色类对象上，editor 可能把面部转向相机而不是保持 3D 物体原本朝向。

#### `supplementary.tex`

附录直接替换 `Limitations and Failure Cases` 下的 placeholder。默认不插图，因为当前没有明确命名的 face-orientation failure-case 图像；如果用户之后指定对应图片，再按可选 diff 加 `figure`。

### English LaTeX Diff

#### `camera_ready.tex` (+5/-0)

中文翻译：
在 `Conclusion` 后插入一个短 limitations 段落：OREO 的收益来自 2D editor prior，因此极端情况下可能继承 editor 的构图/视角偏差；当编辑人脸或角色类对象时，2D editor 可能把面部转向当前相机，而不是保持原本 3D 朝向；更多失败分析见 Supplementary。

```diff
diff --git a/camera_ready.tex b/camera_ready.tex
--- a/camera_ready.tex
+++ b/camera_ready.tex
@@ -569,10 +569,15 @@ This analysis suggests that, in the post-training setting where structure-preser
 \section{Conclusion}
 This paper proposes \textbf{OREO}, a fidelity alignment framework for 3D generation.
 Addressing the lack of visual realism in existing 3D models, we introduce an on-the-fly optimization loop that leverages 2D diffusion priors.
 At its core, we propose Reinforced Editing to generate structure-preserving pseudo-GTs, which serve as dynamic supervision targets.
 Experimental results demonstrate that OREO effectively enhances the visual fidelity and texture details of 3D generators while maintaining geometric integrity, offering a scalable solution to bridge the gap between 3D geometry and 2D visual realism.
 
+\textbf{Limitations.}
+OREO inherits its appearance guidance from 2D editing priors, and thus may also inherit their compositional or viewpoint biases in rare cases.
+For face-like objects or characters, the 2D editor may rotate the face toward the camera instead of preserving the intended 3D-facing direction, leading to view-dependent orientation inconsistency.
+Similar biases can also appear as color/style shifts on unusual materials or weakly constrained back views.
+We provide additional failure-case analysis in the Supplementary Material.
+
 \textbf{Future Work.} Although OREO performs well, there is still room for further exploration. First, the current FlowEdit process has high inference costs; future work could explore more efficient distillation strategies (e.g., one-step editing). Second, we will attempt to extend OREO to more complex scene generation tasks, utilizing panoramic editing models to optimize large-scale 3D environments. Finally, combining with Large Multimodal Models (LMM) for more fine-grained interactive editing is also an exciting direction.
 
 \clearpage
```

#### `supplementary.tex` (+20/-1)

中文翻译：
把附录的 placeholder 替换成三类 failure analysis。第一类重点解释 face-like objects 的 viewpoint drift：editor 可能把人脸朝向镜头，造成面部局部更清晰但 3D 朝向不一致；第二类解释 inherited color/style bias，承接 rebuttal 里 golem color bias；第三类合并 back views 与细结构弱约束问题。最后用一段总结说明未来需要 multi-view-aware editor 或 3D-consistent feedback。

```diff
diff --git a/supplementary.tex b/supplementary.tex
--- a/supplementary.tex
+++ b/supplementary.tex
@@ -206,7 +206,26 @@ Placeholder for qualitative comparisons between training with and without the ad
 \section{Limitations and Failure Cases}
 \label{sec:limitations_failure}
-Placeholder for limitations and failure cases.
+While OREO improves visual fidelity in most cases, its feedback signal is still derived from 2D editing priors rather than explicit 3D supervision.
+This section discusses representative limitations observed during post-training.
+
+\textbf{Viewpoint drift for face-like objects.}
+When the rendered object contains a face or character-like front side, the 2D editor may prefer a canonical portrait composition.
+As a result, the edited pseudo-GT can rotate or reorient the face toward the camera instead of preserving the intended forward-facing direction of the 3D object.
+If such pseudo-GTs are repeatedly used during post-training, OREO may improve local facial details while introducing inconsistent face orientation across views.
+This failure is caused by a mismatch between 2D portrait priors and the 3D view-consistency requirement.
+
+\textbf{Inherited color and style bias.}
+The dynamic noise update encourages the editing trajectory to follow the 2D editor's appearance prior more closely.
+This generally improves texture richness and perceptual quality, but it can also inherit editor-specific color or style bias.
+For objects with unusual materials, such as stone-like creatures, metallic surfaces, or highly stylized designs, the edited pseudo-GT may shift the intended hue or over-emphasize a dominant color tone.
+When such biased pseudo-GTs are repeatedly used for generator optimization, the final 3D output may preserve the geometry but deviate in color distribution.
+
+\textbf{Weakly constrained views and fine structures.}
+OREO optimizes rendered views with online pseudo-GTs, but each editing query still observes a limited camera view.
+Regions that are rarely visible or only weakly constrained, such as back views, occluded surfaces, thin structures, and sharp material boundaries, can show slightly mismatched texture density or local decorative details.
+In such cases, OREO can improve the overall appearance while still leaving small artifacts around boundaries, appendages, or high-frequency ornaments.
+
+These failure cases suggest that future work could incorporate stronger multi-view consistency constraints, 3D-aware editing models, or uncertainty-aware filtering of pseudo-GTs before they are used for generator updates.
 
 % ---------------------------------------------------------------
 % References
```

#### 可选：`supplementary.tex` 加 face-orientation failure-case figure（需要用户指定图片）

中文说明：
如果用户指定一张可靠的 face-orientation failure-case 图，例如 source render、edited pseudo-GT、optimized multi-view 的拼图，就在 `Viewpoint drift for face-like objects` 段落后插入下面的 figure。若没有指定图片，不执行这个 diff。

```diff
diff --git a/supplementary.tex b/supplementary.tex
--- a/supplementary.tex
+++ b/supplementary.tex
@@ -214,6 +214,17 @@ This failure is caused by a mismatch between 2D portrait priors and the 3D view-
+
+\begin{figure}[t]
+  \centering
+  \includegraphics[width=0.95\linewidth]{\texttt{TODO: failure-case figure path}}
+  \caption{
+  Representative viewpoint-drift failure case for a face-like object.
+  The 2D editor improves local facial details but reorients the face toward the camera, causing the pseudo-GT to conflict with the intended 3D-facing direction and producing view-dependent orientation inconsistency after optimization.
+  }
+  \label{fig:failure_case_face_orientation}
+\end{figure}
 
 \textbf{Inherited color and style bias.}
 The dynamic noise update encourages the editing trajectory to follow the 2D editor's appearance prior more closely.
```

## 需要确认的信息
- 是否有指定的 face-orientation failure-case 图片，最好包含 source render、edited pseudo-GT、optimized 3D render / multi-view。默认方案是不新增图，只写文字分析。
- 是否还要保留 rebuttal 里提到的 golem color bias 作为第二个文字案例。默认保留，不放图。
- 是否允许我在执行 Problem 7 时顺手清理 Supplementary 里与 Problem 6 相关的残留 `TODO`/重复 discriminator 句子。默认不处理，避免混入 Problem 7 范围。

## 风险与取舍
- 主文页数已经接近上限，正文 limitations 必须短，详细讨论下沉 Supplementary。
- 没有可靠 face-orientation 失败图时，文字分析比硬放图更稳妥；camera-ready 版本里 unsupported visual claim 风险更高。
- Problem 7 与 Problem 8 控页相关，若新增段落造成页数超限，后续应由 Problem 8 统一压缩，而不是在 Problem 7 阶段牺牲内容清晰度。
