# MathLearnLab — 状态总览

## ✅ 当前状态

| 项目 | 地址/状态 |
|------|----------|
| **ECS 服务器** | `http://8.137.78.250/` — 在线运行中（https://www.mathlearnlab.cn） |
| **GitHub 仓库** | `https://github.com/Kiryuryu/mathlearnlab` |
| **SSH (个人账号)** | `git@github-personal:Kiryuryu/mathlearnlab.git` |
| **SSH 密钥** | `~/.ssh/id_ed25519_github_personal` |
| **ECS 登录** | `ssh root@8.137.78.250` (密码: 见环境变量/密码管理器，勿提交到 git) |
| **CI 部署密钥** | `~/.ssh/mathlearnlab_deploy`（公钥已安装到 ECS `~/.ssh/authorized_keys`） |
| **ECS 项目路径** | `/opt/apps/mathlearnlab` |

## 🚀 部署方式（推荐）

统一使用 `scripts/ci_deploy.py`（本地与 CI 共用，支持 SSH 密钥或密码）：

```bash
cd /Users/joycezhang/mathlearnlab
export DEPLOY_HOST=8.137.78.250 DEPLOY_USER=root
export DEPLOY_SSH_KEY="$HOME/.ssh/mathlearnlab_deploy"   # 推荐：密钥
# 或 export DEPLOY_PASS='<你的密码>'
python deploy.py          # 本地入口（gitignore 中，仅本机可用）
# 或 python scripts/ci_deploy.py
```

脚本会全量同步 `server/`（routers/services/models/middleware）、`content/`、`static-spa/`
与 requirements，自动重启 systemd 服务；若远程 `.env` 缺 `ADMIN_SECRET` 会自动生成并打印。

## 🤖 CI 自动部署

GitHub Actions（`.github/workflows/ci.yml`）在 push 到 main 且测试通过后自动部署。
需要一次性在 GitHub 仓库 Settings → Secrets and variables → Actions 里配置：

| Secret | 值 |
|--------|-----|
| `DEPLOY_HOST` | `8.137.78.250` |
| `DEPLOY_USER` | `root` |
| `DEPLOY_SSH_KEY` | `~/.ssh/mathlearnlab_deploy` 的**内容**（私钥全文） |

## ⚙️ 生产环境变量（ECS `/opt/apps/mathlearnlab/.env`）

| 变量 | 说明 | 必填 |
|------|------|------|
| `JWT_SECRET_KEY` | JWT 签名密钥 | 是（缺失拒绝启动） |
| `ADMIN_SECRET` | 管理后台密钥（`Authorization: Bearer <secret>` 头） | 是（缺失拒绝启动） |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥（生产只信任此服务端 Key） | 是 |
| `DATABASE_URL` | MySQL 连接串；留空用 SQLite | 否 |
| `AI_DAILY_LIMIT` | 每用户每日 AI 调用配额（默认 60） | 否 |
| `MAX_IMAGE_BYTES` | 批改图片大小上限（默认 5MB） | 否 |
| `SMTP_*` / `ADMIN_EMAIL` | 邮件通知 + 密码重置 | 否 |

## 📓 本地开发

```bash
cd /Users/joycezhang/mathlearnlab
source venv/bin/activate
DEBUG=true python3 -m uvicorn server.main:app --reload
# 前端: cd frontend && npm run dev（Vite :5173 代理 /api 到后端）
```

## 🔑 API Key 说明

1. 生产环境：AI 功能（出题/批改/聊天）使用服务端 `DEEPSEEK_API_KEY`，用户无需自备 Key
2. 开发环境（DEBUG=true）：前端可在设置中填自己的 DeepSeek Key
3. 每位用户每日有 AI 调用配额（`AI_DAILY_LIMIT`），持久化在数据库
