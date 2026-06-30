# Session Handoff: Camera-Ready 公式记号 & Method Overview 重写

## 对话 Transcript
`~/.claude-internal/projects/-Users-zhiyuanma-Desktop-OREO-ECCV-paper-template/ed797fe1-3ce9-40d1-954c-0d6b1152e11d.jsonl`

## 前序 Session
- `.agents/sessions/2026-06-29-camera-ready-edits.md` — 同日较早 session：添加 neg-src figure 到正文、调间距
- `.agents/sessions/2026-06-23-related-work-camera-ready.md` — Related Work 三段重构

## 相关 Plan
- `.agents/plan/camera-ready-remaining.md` — camera-ready 剩余任务清单（Method 符号、实验重做、Related Work 补充）

## 任务目的
为 ECCV camera-ready 做多项修改：公式记号统一（`x^{tgt}(t)` → `x_t^{tgt}`）、source 分支改为 unconditional、Figure 2 替换为新 pipeline 图并裁白边、Figure 1 caption 去重、method overview 段落重写为 high-level 叙述、添加通讯作者标记和 project page URL。

## 执行内容
- 添加通讯作者 `†` 标记（Wenbo Hu + Lei Zhang），用 `\textsuperscript{\dag}` + `\let\thefootnote\relax\footnotetext`
- 在 abstract 末尾添加 project page URL（`https://theericma.github.io/oreo/`）
- 去掉 institute 中的 `\email{}`，改换行格式
- 将 Eq. 5/6/7/8 和 Algorithm 1 中所有 `x^{tgt}(t)` → `x_t^{tgt}`、`x^{src}(t)` → `x_t^{src}` 并标红
- 将 Algorithm 1 中 source 分支从 `v_φ^{-w}(x_t^{src}; t, c^{ref})` 改为 `v_φ(x_t^{src}; t, ∅)`（unconditional）并标红
- 相应修改 Eq. 7 和 Sec. 3.3 正文描述
- 替换 Figure 2 为 `figures_final/OREO_pipeline_v3.drawio.pdf`，添加 `trim=80 0 80 0,clip` 裁白边
- 修复 Figure 1/2 caption 重复问题（Figure 1 改为 "Teaser"，Figure 2 保持 "Overview of OREO"）
- 将 teaser 图宽度改为 `0.95\textwidth`
- 重写 method overview 段（L155-161）为 4 句 high-level 叙述，不含数学符号，引用相应 section，中文反复讨论后定稿并标红
- 更新 Figure 2 caption 中的 source 分支描述为 "a positive guidance term with an unconditional source anchor"

## 代码改动

### Commits
无新 commit。所有改动均为 unstaged。前序 commit `1209eab` 为上次 session 的提交。

### 文件详情

**`camera_ready.tex`**（+37/-30 行 diff vs HEAD）— 本次 session 全部改动

1. **通讯作者标记**（L55-56, L69-70）：
   - `Wenbo Hu\inst{2}\textsuperscript{\dag}`、`Lei Zhang\inst{1}\textsuperscript{\dag}`
   - 删除 `\email{}`，在 `\maketitle` 后加 `\let\thefootnote\relax\footnotetext{\textsuperscript{\dag}Corresponding authors}`
   - 经历多次尝试（`\thanks{}` 不兼容 LLNCS → `$^*$` 风格不统一 → `†` 脚注符号不匹配），最终用 `\textsuperscript{\dag}` + 手动 footnotetext 解决

2. **Project page URL**（L80）：在 abstract 末尾 `\keywords` 前加 `Our project page is at \url{https://theericma.github.io/oreo/}.`

3. **Teaser 图**（L94-97）：宽度 → `0.95\textwidth`，caption "Overview of OREO" → "Teaser"，加 `\vspace{-2mm}`

4. **Method overview 重写**（L157-161）：
   - 删除旧的 8 句详细描述（含数学符号、变量名、ODE rollout 等细节）
   - 新增 4 句 high-level 叙述（全部标红），结构：idea → on-policy sampling → reinforced editing → distillation
   - 不含任何数学符号，用自然语言引用 section（如 "Sec.~\ref{sec:preliminaries}"）
   - 用户在中文讨论中逐句确认并调整措辞

5. **Figure 2 替换**（L165）：
   - 旧：`figures/OREO_pipeline_v2.drawio.png`
   - 新：`figures_final/OREO_pipeline_v3.drawio.pdf`，加 `trim=80 0 80 0,clip` 裁白边
   - Caption 更新：`coupling positive and negative guidance terms` → `coupling a positive guidance term with an unconditional source anchor`

6. **公式记号统一**（Eq. 5/6/7/8 + Algorithm 1，约 L215-290）：
   - `x^{tgt}(t)` → `\textcolor{red}{x_t^{tgt}}`，`x^{src}(t)` → `\textcolor{red}{x_t^{src}}`
   - 涉及 Eq. 5（FlowEdit 原始公式）、Eq. 6（source/target 构造）、Eq. 7（Reinforced Editing）、Eq. 8（noise update）和 Algorithm 1 的多处
   - 用户提示后补充对 Eq. 6、Algorithm 1、Eq. 8 的遗漏

7. **Source 分支 unconditional 改动**（Sec. 3.3 正文 + Eq. 7 + Algorithm 1）：
   - Eq. 7：`v_φ^{-w}(x_t^{src}; t, c^{ref})` → `v_φ(x_t^{src}; t, ∅)`
   - Algorithm 1 对应行同步更新
   - Sec. 3.3 正文两段描述重写（标红）：从 "opposite guidance scales" 改为 "replace source branch with unconditional prediction"

## 调试经验
- 现象：LLNCS `\author{}` 中使用 `\thanks{}` 报错 → 原因：LLNCS 不支持 `\thanks` 在 author 环境 → 解法：用 `\textsuperscript{\dag}` + `\let\thefootnote\relax\footnotetext{}`
- 现象：用户说"figure 2能不缩小吗"，被误解为"能不能缩小" → 原因：中文歧义 → 解法：用户实际意思是"能不缩小？"（有白边即使满宽度），改用 `trim=80 0 80 0,clip` 裁切
- 现象：只修改了 Eq. 5 的 subscript 记号 → 原因：遗漏其他公式 → 解法：用户提醒后补全 Eq. 6、Algorithm 1、Eq. 8
- 现象：修改公式后忘记标红 → 原因：camera-ready 规则 → 解法：用户两次提醒后补上 `\textcolor{red}{}`

## 用户决策与偏好
- 所有 camera-ready 改动必须 `\textcolor{red}{}` 标红（反复强调）
- Method overview 段不要数学符号（因为还没 formulation）
- Section 引用不要括号（如 "Sec. 3.2" 而非 "(Sec. 3.2)"）
- Caption 精炼、2 句为佳
- 中文逐句讨论→英文定稿的工作流
- Source 分支不需要 CFG，直接用 unconditional（算法核心改动）

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `camera_ready.tex` | L155-161 | 新 method overview，用户可能继续调整 |
| `camera_ready.tex` | L190-230 | Sec. 3.1 Preliminaries + FlowEdit formulation，用户觉得"不通顺" |
| `camera_ready.tex` | L255-280 | Sec. 3.3 Reinforced Editing，刚改完 source→unconditional |
| `camera_ready.tex` | L165-175 | Figure 2 caption，可能需要更新以匹配 v3 pipeline 图 |
| `supplementary.tex` | L62-78 | Negative source guidance 分析，可能需要和正文统一 |

## 最终方案
将公式记号从函数式 `x^{tgt}(t)` 统一改为下标式 `x_t^{tgt}` 并标红。Source 分支从 negative CFG (`v^{-w}`) 改为 unconditional (`v(x;t,∅)`)。Method overview 从详细技术描述重写为 4 句 high-level 叙述。所有改动用 `\textcolor{red}{}` 标记。

## 下一步任务
用户刚提出："你有没有觉得3.1开头讲的很不通顺"——Sec. 3.1 的开头段落需要重写/调整通顺度。

此外 camera-ready 仍有多项 pending：
1. **Sec. 3.1 通顺度调整**（用户刚提出）
2. **Source 分支 unconditional 改动的全文一致性检查**（用户曾说"应该有很多内容需要调整"但未完全展开）
3. **Problem 6**（overhead/dataset TODO 填充）
4. **Problem 8**（页数限制 14 页）
5. **实验重做**（camera-ready-remaining.md 中的最高优先级未完成项）
6. **Related Work 补充参考文献**

## 初步方案
- Sec. 3.1 开头：读当前内容，识别不通顺之处（可能是 Preliminaries 的 problem setup 部分叙述跳跃），和用户逐句调整
- Source→unconditional 全文检查：grep `w_{\texttt{src}}` 和 `c^{\texttt{src}}` 确认无遗留旧说法
- Supplementary Sec. S1 中的 negative source guidance 描述可能也需要同步更新
