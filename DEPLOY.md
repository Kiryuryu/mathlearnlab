# MathLearnLab — 阿里云 ECS 完整部署指南

> 服务器信息
> - 内网 IP: 192.168.31.15
> - 公网 IP: 8.137.78.250
> - 系统: Alibaba Cloud Linux / CentOS 兼容

---

## 第一步：服务器基础环境

SSH 登录你的 ECS 后，逐条执行：

### 1.1 安装 Python 3.12

```bash
# 安装依赖
yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel readline-devel sqlite-devel

# 下载并编译 Python 3.12
cd /tmp
wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz
tar xzf Python-3.12.4.tgz
cd Python-3.12.4
./configure --enable-optimizations --prefix=/usr/local/python3.12
make -j$(nproc)
make install

# 添加到 PATH
echo 'export PATH="/usr/local/python3.12/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
python3.12 --version
```

### 1.2 安装 Nginx

```bash
yum install -y nginx
systemctl enable nginx
systemctl start nginx
```

---

## 第二步：部署项目

### 2.1 推送代码到 GitHub

在你本地 Mac 上：

```bash
cd /Users/joycezhang/mathlearnlab

# 确保所有文件都已提交
git add -A
git commit -m "FastAPI server with 静逸书卷 design"
git push origin main
```

### 2.2 在 ECS 上拉取代码

```bash
# SSH 到 ECS 后
mkdir -p /opt/apps
cd /opt/apps
git clone https://github.com/joycezhang/mathlearnlab.git
cd mathlearnlab
```

### 2.3 创建虚拟环境

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 配置环境变量

```bash
cp .env.example .env
vi .env
```

编辑 `.env`，填入你的 Anthropic API Key：

```
ANTHROPIC_API_KEY=sk-ant-api03-你的真实key
DEBUG=false
CONTENT_DIR=content
DATA_DIR=data
```

### 2.5 测试启动

```bash
source venv/bin/activate
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

应该看到：
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

`Ctrl+C` 停止测试。

---

## 第三步：配置 systemd 服务

### 3.1 创建服务文件

项目中已有 `mathlearnlab.service`，复制到系统目录：

```bash
cp /opt/apps/mathlearnlab/mathlearnlab.service /etc/systemd/system/
```

### 3.2 编辑确认路径正确

```bash
cat /etc/systemd/system/mathlearnlab.service
```

确认内容：
```ini
[Unit]
Description=MathLearnLab FastAPI
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/apps/mathlearnlab
ExecStart=/opt/apps/mathlearnlab/venv/bin/uvicorn server.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5
EnvironmentFile=/opt/apps/mathlearnlab/.env

[Install]
WantedBy=multi-user.target
```

### 3.3 启动服务

```bash
systemctl daemon-reload
systemctl enable mathlearnlab
systemctl start mathlearnlab
systemctl status mathlearnlab
```

应该显示 `active (running)` 绿灯。

---

## 第四步：配置 Nginx

### 4.1 复制配置文件

```bash
cp /opt/apps/mathlearnlab/nginx.conf /etc/nginx/conf.d/mathlearnlab.conf
```

### 4.2 修改域名/监听

如果你的 ECS 有公网 IP 可以直接访问，保持 `server_name _;`（匹配所有）。

如果你要绑定域名（如 mathlearnlab.cn），修改：

```nginx
server_name mathlearnlab.cn;
```

### 4.3 测试并重启 Nginx

```bash
nginx -t                      # 测试配置语法
systemctl restart nginx       # 重启
```

---

## 第五步：配置安全组（阿里云控制台）

在阿里云 ECS 控制台 → 安全组 → 入方向添加规则：

| 端口 | 协议 | 来源 | 说明 |
|------|------|------|------|
| 80 | TCP | 0.0.0.0/0 | HTTP |
| 443 | TCP | 0.0.0.0/0 | HTTPS (如果需要) |
| 22 | TCP | 0.0.0.0/0 | SSH |

---

## 第六步：验证部署

```bash
# 1. 确认 FastAPI 在运行
curl http://127.0.0.1:8000/api/health
# 应返回: {"status":"ok","app":"MathLearnLab"}

# 2. 确认 Nginx 代理
curl http://127.0.0.1/api/health
# 也应返回相同内容

# 3. 测试页面
curl -s http://127.0.0.1/ | head -5
# 应返回 HTML 页面内容
```

从你本地浏览器访问：
- `http://10.67.99.90/` — 首页
- `http://10.67.99.90/practice/integrals` — 刷题页

---

## 第七步：（可选）配置 HTTPS

如果你有域名并解析到了 ECS：

```bash
# 安装 certbot（CentOS/RHEL）
yum install -y epel-release
yum install -y certbot python3-certbot-nginx

# 自动配置 SSL
certbot --nginx -d mathlearnlab.cn

# 测试自动续期
certbot renew --dry-run
```

---

## 日常更新

修改代码推送到 GitHub 后，在 ECS 上执行：

```bash
cd /opt/apps/mathlearnlab
bash scripts/deploy.sh
```

或手动：

```bash
cd /opt/apps/mathlearnlab
git pull origin main
source venv/bin/activate
pip install -r requirements.txt -q
systemctl restart mathlearnlab
```

---

## 排查问题

```bash
# 查看 FastAPI 日志
journalctl -u mathlearnlab -f

# 查看 Nginx 日志
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# 检查端口监听
ss -tlnp | grep 8000
ss -tlnp | grep 80

# 手动启动测试（不通过 systemd）
cd /opt/apps/mathlearnlab
source venv/bin/activate
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```
