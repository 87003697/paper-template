---
name: server-download
description: 生成从 gpucluster 服务器下载文件到本地的 rsync 命令。Use when the user wants to download files from a gpucluster server (s1-s10, c1-c16) or mentions a server IP like 10.21.21.x.
---

# Server Download

根据用户提供的服务器名和远程路径，生成一条可直接复制运行的 `rsync` 下载命令。

## 服务器名 → IP 映射表

| 服务器名 | IP |
|---|---|
| gpucluster-s1 | 10.21.21.172 |
| gpucluster-s2 | 10.21.21.173 |
| gpucluster-s3 | 10.21.21.174 |
| gpucluster-s4 | 10.21.21.175 |
| gpucluster-s5 | 10.21.21.176 |
| gpucluster-s6 | 10.21.21.177 |
| gpucluster-s7 | 10.21.21.178 |
| gpucluster-s8 | 10.21.21.179 |
| gpucluster-s9 | 10.21.21.196 |
| gpucluster-s10 | 10.21.21.197 |
| gpucluster-c1 | 10.21.21.180 |
| gpucluster-c2 | 10.21.21.181 |
| gpucluster-c3 | 10.21.21.182 |
| gpucluster-c4 | 10.21.21.183 |
| gpucluster-c5 | 10.21.21.184 |
| gpucluster-c6 | 10.21.21.185 |
| gpucluster-c7 | 10.21.21.186 |
| gpucluster-c8 | 10.21.21.187 |
| gpucluster-c9 | 10.21.21.188 |
| gpucluster-c10 | 10.21.21.189 |
| gpucluster-c11 | 10.21.21.190 |
| gpucluster-c12 | 10.21.21.191 |
| gpucluster-c13 | 10.21.21.192 |
| gpucluster-c14 | 10.21.21.193 |
| gpucluster-c15 | 10.21.21.194 |
| gpucluster-c16 | 10.21.21.195 |

用户可用简写（如 `c6`、`s1`），自动补全为 `gpucluster-c6` 再查表。若用户直接提供 IP 地址（如 `10.21.21.185`），则直接使用。

## Steps

1. **解析目标服务器** — 从用户消息中提取服务器名或 IP：
   - 若为简写（如 `c6`、`s1`），补全为 `gpucluster-c6` 后查表得到 IP
   - 若已是完整服务器名（如 `gpucluster-c6`），直接查表
   - 若已是 IP 地址，直接使用
   - 若无法识别，询问用户："你想从哪台服务器下载？（如 c6、s1 或直接提供 IP）"

2. **收集远程路径** — 从用户消息中提取服务器上的完整路径；若未提供，询问："请提供服务器上的完整路径（例如 `/home/zhiyuan_ma/code/...`）"

3. **确认本地目标路径** — 若用户未指定本地路径，默认使用 `./`（无需追问，直接使用默认值，在输出命令后注明）

4. **生成命令** — 按下方模板拼装，用代码块输出，并附上参数说明

## 命令模板

```bash
rsync -avP \
  -e "ssh -J zhiyuan_ma@10.21.21.12" \
  zhiyuan_ma@<目标IP>:<远程路径>/ \
  <本地路径>/
```

输出命令后附上以下说明：
- `-avP` — archive 模式 + verbose 输出 + 断点续传进度显示
- `-e "ssh -J ..."` — 经由跳板机 `10.21.21.12` 中转连接
- 跳板机和目标机用户名均为 `zhiyuan_ma`，无需修改

## Notes

- 远程路径末尾带 `/`：只下载目录内的文件；不带 `/`：连同目录本身一起下载
- 若只需下载单个文件而非整个目录，去掉路径末尾的 `/` 即可
- 若传输中断，重新运行同一条命令即可自动续传
- 跳板机固定为 `10.21.21.12`，用户无需关心网络路由
- macOS 自带的 rsync 版本为 2.6.9，**不支持 `--append-verify`**，命令模板中不使用该参数。若需要此功能，可先执行 `brew install rsync` 升级到新版本
