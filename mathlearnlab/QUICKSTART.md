# MathLearnLab — ECS 部署 + 本地开发同步

## 当前状态

- **ECS `8.137.78.250`** — Python 3.12.4 + venv + systemd + Nginx 已配置好，FastAPI 在运行
- **GitHub `Kiryuryu/mathlearnlab`** — 代码已 push (commit `e82a1a5`)
- **`.env`** — 需要你填入真实的 Anthropic API Key

## 你需要做的（1 分钟）

1. 打开 [Anthropic Console](https://console.anthropic.com/) 获取 API Key（或告诉我你的 key 我帮你填上去）
2. SSH 到 ECS：
   ```
   ssh root@8.137.78.250
   # 密码: Tickingaway997-
   ```
3. 编辑 `.env` 填入 Key：
   ```
   vi /opt/apps/mathlearnlab/.env
   # 把 ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   # 改成 ANTHROPIC_API_KEY=你的真实key
   ```
4. 重启服务：
   ```
   systemctl restart mathlearnlab
   ```
5. 浏览器打开 `http://8.137.78.250/`

## 本地开发 → ECS 同步

下次你改了代码，只需要：

```bash
# 在你的 Mac 上
cd ~/mathlearnlab
git add -A && git commit -m "updates" && git push origin main

# SSH 到 ECS
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
