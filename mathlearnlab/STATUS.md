# MathLearnLab — 状态总览

## ✅ 当前状态

| 项目 | 地址/状态 |
|------|----------|
| **ECS 服务器** | `http://8.137.78.250/` — 在线运行中 |
| **GitHub 仓库** | `https://github.com/Kiryuryu/mathlearnlab` |
| **SSH (个人账号)** | `git@github-personal:Kiryuryu/mathlearnlab.git` |
| **SSH 密钥** | `~/.ssh/id_ed25519_github_personal` |
| **ECS 登录** | `ssh root@8.137.78.250` (密码: Tickingaway997-) |
| **ECS 项目路径** | `/opt/apps/mathlearnlab` |

## 🔧 ECS 下次更新代码

由于 ECS 用 SSH 连 GitHub 需要额外的 deploy key 设置，目前最简单的更新方式是直接从本机 SCP：

```bash
# 修改代码后，从 Mac 上传到 ECS:
cd /Users/joycezhang/mathlearnlab
expect -c '
spawn scp -r server/ root@8.137.78.250:/opt/apps/mathlearnlab/
expect "password:" { send "Tickingaway997-\r" }
expect eof
'

# 然后重启服务:
expect /Users/joycezhang/mathlearnlab/scripts/ecs-run.exp "
find /opt/apps/mathlearnlab/server -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
systemctl restart mathlearnlab
"
```

## 📓 本地开发

```bash
cd /Users/joycezhang/mathlearnlab
source venv/bin/activate  # 或 source /path/to/python3 -m venv venv
python3 -m uvicorn server.main:app --reload
# 浏览器: http://localhost:8000
```

## 🔑 API Key

1. 点右上角「钥」按钮
2. 填入你的 Anthropic API Key (`sk-ant-api03-...`)
3. Key 仅存浏览器 localStorage
4. 没有 Key？去 https://console.anthropic.com/ 注册
