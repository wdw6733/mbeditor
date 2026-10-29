<div align="center">

# MBEditor · 技术文章版

### 一句话生成专业技术文章的自托管编辑器

**说一个技术主题，AI 帮你写出一篇「有图、有准确命令代码、排版精美」的公众号技术推文。**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-一键部署-2496ED.svg)](docker-compose.yml)
[![BYOK](https://img.shields.io/badge/AI-自带模型_Key-10B981.svg)](#配置-ai-模型byok)
[![ghcr](https://img.shields.io/badge/Registry-ghcr.io-8957E5.svg)](https://github.com/users/wdw6733/packages?repo_name=mbeditor)

</div>

---

## 这是什么

本项目是 [AAAAAnson/mbeditor](https://github.com/AAAAAnson/mbeditor) 的**技术文章定制版**。

原版 MBEditor 是一个「说一句想法 → AI 流式生成排版精美推文」的自托管公众号创作工具。本定制版在其基础上，**聚焦技术干货写作**，专攻三大方向：

| 方向 | 典型选题 |
|------|---------|
| 📱 安卓手机应用 | App 逆向 / 系统优化 / 应用推荐 / 刷机玩机 |
| 🐳 容器应用 | Docker / Compose / 自托管服务 / NAS 部署 |
| 🌐 网络技术 | 内网穿透 / 反向代理 / 组网 / 网络排障 |

生成的文章对齐公众号技术干货风格：**有架构图/拓扑图、有准确可复现的命令和代码、层级清晰**。

## 相对原版，改了什么

| # | 改动 | 说明 |
|---|------|------|
| 1 | 新增「技术干货」调子 | 映射到「科技霓虹」深色科技排版 |
| 2 | 新增技术文章专用 Prompt | 专攻安卓/容器/网络，强制命令/代码准确可执行 |
| 3 | 排版器支持代码块渲染 | 原版会把代码当普通文字转义，本版正常渲染 `<pre>` 代码块 |
| 4 | 自动配图工序 | AI 标注 `[[SVG|图描述]]` → 自动生成架构图/拓扑图 SVG |
| 5 | SVG 生成改走 BYOK API | 配图与正文共用同一套模型配置，不再只认 Anthropic |
| 6 | Docker 构建走国内镜像源 | 加速镜像构建（apt/pip/playwright 均换国内源） |

## 快速开始

### 部署

镜像已推送到 `ghcr.io/wdw6733`，直接 `docker compose` 拉起即可（所有配置都写在 `docker-compose.yml` 里，无需 `.env`）：

```bash
curl -O https://raw.githubusercontent.com/wdw6733/mbeditor/main/docker-compose.yml
docker compose up -d
```

> 若镜像仍为私有，先执行一次 `docker login ghcr.io -u wdw6733`（密码填你的 Personal Access Token），公开后则无需登录。

部署完成后：

- **编辑器界面**：http://localhost:7073
- **API 接口**：http://localhost:7072/api/v1

> 要从局域网 / 手机访问（如部署在 NAS），把 `docker-compose.yml` 里两个端口的 `127.0.0.1` 改成 `0.0.0.0` 即可。

### 配置 AI 模型（BYOK）

打开 `docker-compose.yml`，找到「必填」段，填三行：

```yaml
- LLM_BASE_URL=    # 你的 API 地址
- LLM_MODEL=       # 模型名
- LLM_API_KEY=     # 你的 Key
```

**推荐模型**（针对「技术文章 + 准确代码 + SVG 配图」场景）：

| 档位 | 平台 | `LLM_BASE_URL` | `LLM_MODEL` |
|------|------|----------------|-------------|
| 🥇 首选 | DeepSeek | `https://api.deepseek.com` | `deepseek-v4-pro` |
| 🥈 省钱 | DeepSeek | `https://api.deepseek.com` | `deepseek-flash` |
| 🥉 重文笔 | 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen3.8-max` |

> 选 DeepSeek 的理由：本项目的「好看配图」是 AI 直接生成 SVG 架构图/拓扑图，**SVG 本质是代码，代码能力 = 配图能力**。DeepSeek 代码生成是国产最强档，命令准确、配图稳定、价格最低，且国内直连。

Key 只存在后端具名卷，不经过任何第三方。

### 使用

打开编辑器 → 起稿台，输入一句需求，**调子选「技术干货」**，例如：

> 给 NAS 部署一个自托管的容器应用并用 Nginx 反代，写一篇可照着敲的教程

AI 会流式生成一篇：有标题层级、有 `bash/yaml` 代码块（命令准确可复现）、有自动生成的架构图 SVG、深色科技风排版，直接复制即可粘贴进公众号。

## 镜像

| 组件 | 镜像 |
|------|------|
| 后端 | `ghcr.io/wdw6733/mbeditor-backend:latest` |
| 前端 | `ghcr.io/wdw6733/mbeditor-frontend:latest` |

## 致谢

本项目基于 [AAAAAnson/mbeditor](https://github.com/AAAAAnson/mbeditor)（MIT License）。原项目是一个功能完整的 AI 公众号创作工具——BYOK、五套排版、Agent 优先的 RESTful API、微信草稿箱推送等能力均来自原项目，本版仅在其上做技术文章方向的定制。

<a href="https://github.com/AAAAAnson">
  <img src="https://github.com/AAAAAnson.png" width="60" style="border-radius:50%;" alt="AAAAAnson" />
</a>

**[AAAAAnson](https://github.com/AAAAAnson)** — 原项目创建者与维护者

## 许可证

[MIT](LICENSE) &copy; 2025 Anson

_专注技术内容，其他交给 MBEditor。_
