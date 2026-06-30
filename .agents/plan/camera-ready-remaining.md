---
name: camera-ready-remaining
overview: 按正文目录从前到后记录 camera-ready 还没做的主要事项。
todos:
  - id: method-symbols-flowedit-gan
    content: 第一优先级：Method 需要重新检查数学符号、FlowEdit 描述、Reinforced Editing 分支定义和 GAN 相关表述
    status: pending
  - id: experiments-redo
    content: 第二优先级：实验需要整套重做，并据新结果回填正文、表格、图和 Supplementary
    status: pending
  - id: pipeline-figure
    content: 第三优先级：方法大图暂时完成；后续需根据最终 Method 方案确认 GAN 箭头从 src 还是 tgt 指出
    status: completed
  - id: related-work-refs
    content: 第四优先级：Related Work 需要补充用户指定的参考文献，并按现有三段结构重新组织
    status: pending
isProject: false
---

# Camera-Ready Remaining Checklist

当前还没做的任务，按建议优先级排序如下：

- ❌ **1. Method**：先重新过一遍数学符号和叙述一致性，重点是 `FlowEdit` 的公式、时间步/噪声更新、Reinforced Editing 的 source/target branch 说法，以及 GAN / discriminator 是否作为最终方法的一部分。这个最优先，因为它会决定后续实验验证什么、方法大图怎么画。

- ❌ **2. Experiments**：实验需要整套重做；Method 定稿后立刻确定实验矩阵，并据新结果同步替换 main results、feedback evaluation、ablation、GSO、human study、Supplementary 细节和所有对应文字 claim。

- ✅ **3. 方法大图**：暂时完成。后续仍需要根据最终 Method 方案检查一次 GAN / discriminator 的箭头方向，尤其是箭头到底从 `x^{\texttt{src}}` 还是 `x^{\texttt{tgt}}` 指出；图注也要和最终符号一起对齐。

- ❌ **4. Related Work**：需要补你指定的参考文献；新增文献要放回现有三段脉络里，必要时重写几句承接。这个可以相对靠后，也可以和实验运行并行推进。`main.bib` 仍然不由助手直接改。

- ❌ **5. 最后收尾**：等上面四项确定后，再统一处理正文页数、`TODO`/`Placeholder` 清理、引用/交叉引用、Supplementary 独立编译和最终 PDF 检查。
