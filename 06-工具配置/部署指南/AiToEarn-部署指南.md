# AiToEarn 本地部署指南（Docker 方式）

## 前置要求

- **Git** — 用于克隆代码
- **Docker Desktop** — 包含 Docker 和 Docker Compose
  - macOS / Windows：下载 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Linux：安装 docker.io + docker-compose-plugin

## 第一步：克隆项目

```bash
git clone https://github.com/yikart/AiToEarn.git
cd AiToEarn
```

## 第二步：一键启动所有服务

```bash
docker compose up -d
```

这条命令会自动拉取镜像并启动以下服务（无需手动安装 MongoDB、Redis 等）：

| 服务 | 说明 |
|------|------|
| MongoDB | 数据库 |
| Redis | 缓存 |
| RustFS | 对象存储 |
| aitoearn-server | 后端 API |
| aitoearn-ai | AI 服务 |
| aitoearn-web | Next.js 前端 |
| Nginx | 反向代理 |

首次启动需要拉取镜像，可能需要几分钟，请耐心等待。

## 第三步：访问应用

启动完成后，打开浏览器访问：

| 服务 | 地址 | 说明 |
|------|------|------|
| Web 前端 | http://localhost:8080 | 主界面 |
| 后端 API | http://localhost:8080/api | API 接口 |
| RustFS 控制台 | http://localhost:9001 | 对象存储管理 |

## 常用命令

```bash
# 查看所有服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 查看某个服务的日志
docker compose logs -f aitoearn-web

# 停止所有服务
docker compose down

# 停止并清除数据卷（完全重置）
docker compose down -v

# 重新构建并启动
docker compose up -d --build
```

## 高级配置

如需自定义 API 密钥、数据库密码等，编辑以下文件：

- `docker-compose.yml` — 环境变量（数据库密码、API Key 等）
- `config/aitoearn-ai.config.js` — AI 服务配置
- `config/aitoearn-server.config.js` — 后端服务配置

### 配置 AI 功能（可选）

在 `docker-compose.yml` 中找到 `aitoearn-ai` 服务，替换占位符：

```yaml
OPENAI_API_KEY: sk-your-real-key
ANTHROPIC_API_KEY: sk-your-real-key
```

## 故障排查

**端口冲突：** 如果 8080 或 27017 等端口被占用，修改 `docker-compose.yml` 中的端口映射。

**服务未就绪：** 运行 `docker compose ps` 检查各服务状态，确保都是 healthy。

**重置环境：** 运行 `docker compose down -v && docker compose up -d` 完全重置。
