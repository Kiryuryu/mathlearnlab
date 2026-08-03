# MathLearnLab — ECS 部署 + 本地开发同步

## 当前状态

- **ECS `8.137.78.250`** — Python + venv + systemd + Nginx 已配置好，FastAPI 在运行
- **GitHub `Kiryuryu/mathlearnlab`** — 代码已 push
- **`.env`** — 需要你填入真实的 DeepSeek API Key（生产环境还需 `JWT_SECRET_KEY`、`ADMIN_SECRET`）

## 环境变量

部署与远程检查脚本（`deploy.py`、`check_config.py`、`scripts/*`）均从环境变量读取凭据，**切勿把密码硬编码进仓库**：

```bash
export DEPLOY_HOST=8.137.78.250
export DEPLOY_USER=root
export DEPLOY_PASS='<你的密码>'
```

## 本地开发 → ECS 同步

```bash
# 在你的 Mac 上
cd ~/mathlearnlab
git add -A && git commit -m "updates" && git push origin main

# SSH 到 ECS（密码见环境变量/密码管理器）
ssh root@8.137.78.250
cd /opt/apps/mathlearnlab
git pull origin main
systemctl restart mathlearnlab
```

## ECS 上的快速命令

| 命令 | 作用 |
|------|------|
| `systemctl status mathlearnlab` | 看服务状态 |
| `journalctl -u mathlearnlab -f` | 看实时日志 |
| `systemctl restart mathlearnlab` | 重启 |
| `curl localhost:8000/api/health` | 健康检查 |
| `nginx -t` | 检查 Nginx 配置 |
