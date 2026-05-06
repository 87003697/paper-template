# Session Handoff: TeX Rebuttal Workflow

## 任务目的
搭建 Cursor/LaTeX Workshop 可用的 TeX 即时编译环境，并为后续高频修改 `rebuttal.tex` 建立稳定的编译与预览流程。

## 执行内容
- 诊断 LaTeX Workshop 报错，确认核心问题是 Cursor 找不到 `latexmk`、`pdflatex` 和 `kpsewhich`。
- 安装用户目录版 TinyTeX 到 `/Users/zhiyuanma/Library/TinyTeX`，避免需要管理员密码。
- 为当前项目新增 `.vscode/settings.json`，让 LaTeX Workshop 使用 TinyTeX 的绝对路径和 PATH。
- 补装 `main.tex` 和 `rebuttal.tex` 编译所需宏包，包括 `aliascnt`、`silence`、`lineno`、`cite`、`caption`、`pgf`、`cleveref`、`grfext`、`enumitem` 等。
- 成功编译 `main.tex`，生成 `main.pdf`。
- 下载官方 `cvpr-org/author-kit` 的 `cvpr.sty` 到项目根目录，并将 `rebuttal.tex` 调整回 CVPR rebuttal 风格。
- 根据用户修改后的 style 重新编译 `rebuttal.tex`，成功生成最新 `rebuttal.pdf`。

## 调试经验
- Cursor GUI 环境的 `$PATH` 不包含 TinyTeX 路径，不能只依赖 shell 初始化文件；项目设置里需要写 `latexmk` 绝对路径，并给 tool 配置 `env.PATH`。
- TinyTeX 安装结束时无法写入 `/usr/local/bin` 软链接，但这不影响项目内通过绝对路径编译。
- LaTeX Workshop 预览 PDF 前必须先成功生成对应文件；之前 `rebuttal.pdf` 不存在时，预览报 `ENOENT`。
- `cvpr.sty` 不在当前 TinyTeX 源中，需要从官方 author-kit 下载到项目根目录。
- 轻量 TeX 第一次编译常逐个暴露缺包，优先根据日志中的 `File 'xxx.sty' not found` 用 `tlmgr install` 补齐。

## 参考代码
| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `.vscode/settings.json` | LaTeX Workshop tool/recipe 配置 | 当前项目的即时编译配置，指向 TinyTeX 的 `latexmk`。 |
| `rebuttal.tex` | preamble | 现在使用 `article` + `\usepackage[rebuttal]{cvpr}` 的 CVPR rebuttal 格式。 |
| `cvpr.sty` | 项目根目录 | 官方 CVPR author-kit style，本地编译 rebuttal 依赖它。 |
| `main.tex` | preamble | 主论文使用 ECCV/LNCS 模板，已验证可编译。 |

## 最终方案
采用 TinyTeX + 项目级 LaTeX Workshop 配置，而不是系统级 MacTeX 或 `/usr/local/bin` 软链接。这样不需要管理员权限，并且 Cursor、VS Code、命令行都能通过项目配置稳定编译。`rebuttal.tex` 保持 CVPR rebuttal style，因为用户偏好其格式且官方 `cvpr.sty` 已可用。

## 下一步任务
结合即时编译环境继续修改 `rebuttal.tex`，根据 reviewer comments 迭代 rebuttal 内容，并随改随编译检查版面、页数和格式。

## 初步方案
- 修改前先阅读 `rebuttal.tex`、现有 handoff/priority 文档，以及 `review/Reviewer#*.png` 中的 reviewer 意见。
- 每轮内容修改后运行项目已有 TinyTeX 编译命令，确认 `rebuttal.pdf` 成功更新且没有 fatal error。
- 优先控制 rebuttal 的篇幅和密度，CVPR rebuttal 当前输出为 2 页，应持续关注页数和压缩空间。
- 对每个 reviewer 的答复保持问题导向：先回应核心担忧，再说明 revision 中会补充的实验、图表或文本。
- 若 style 或 spacing 需要微调，优先改 `rebuttal.tex` 中局部 spacing；只有确有必要再动 `cvpr.sty`。
