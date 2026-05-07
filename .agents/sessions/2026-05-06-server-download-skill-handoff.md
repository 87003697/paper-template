# Session Handoff: server-download skill 创建

## 任务目的

创建一个 `.agents/server-download/SKILL.md` skill，让 AI 能根据服务器名或 IP 自动解析目标主机，并生成可直接复制运行的 rsync 下载命令。

## 执行内容

- 讨论了 rsync 的断点续传机制（`-P` / `--append-verify`）
- 设计并创建了 `.agents/server-download/SKILL.md`，包含 gpucluster s1–s10、c1–c16 共 26 台服务器的名称 → IP 映射表
- 注意到 macOS 自带 rsync 2.6.9 不支持 `--append-verify`，命令模板中移除了该参数

## 参考代码

| 文件 | 关键位置 | 说明 |
|------|---------|------|
| `.agents/server-download/SKILL.md` | 全文 | 新建的下载 skill，含映射表、交互流程、命令模板 |
| `.agents/continue-session/SKILL.md` | 全文 | 参考的 skill 格式 |

## 最终方案

在 `.agents/server-download/SKILL.md` 中内嵌完整服务器名→IP映射表，AI 调用 skill 时先解析服务器名（支持简写如 `c6`），再拼装 rsync 命令（经跳板机 `10.21.21.12`，用户名固定 `zhiyuan_ma`）。


## 下一步任务

使用 `server-download` skill 从 gpucluster 服务器下载数据到本地。

## 初步方案

- 在新 session 中描述要下载的服务器名和路径，AI 会自动触发 skill
- 例如："帮我从 c6 下载 `/home/zhiyuan_ma/code/xxx`"
- AI 会查表得到 `10.21.21.185`，生成带跳板机的 rsync 命令供复制运行
