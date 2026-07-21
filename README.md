# 数学博物馆 — 知其然，知其所以然

交互式数学学习平台。不是教你怎么做题，而是带你理解数学概念从何而来、为什么这样定义、美在哪里。

## 在线访问

https://www.mathlearnlab.cn

## 功能

### 展区
- **微积分**：极限、导数、积分、级数、多元微积分，每项 6 个 Tab（核心概念 / 应用案例 / 思想脉络 / 数学之美 / 破局心法 / 探索）
- **线性代数**：矩阵变换可视化、特征值交互探索
- **概率论**：大数定律、中心极限定理、贝叶斯

### 交互可视化
- ε-δ 极限定义滑块、泰勒展开逼近、黎曼和收敛
- 傅里叶级数方波逼近、梯度下降 3D 可视化
- 分形探索（Mandelbrot 集 / Julia 集 / Lorenz 吸引子）
- 函数工坊（2D 曲线 / 3D 曲面 / 向量场 / AI 绘图）

### AI 功能
- 智能出题（基础→进阶→考研→研究生→博士）
- 纸笔作答 → 拍照上传 → AI 批改
- 数学聊天助手（基于 DeepSeek API）

### 用户系统
- 注册审核制（管理员邮箱审批）
- MySQL / SQLite 持久化存储
- API Key 存储在浏览器 localStorage

### 安全
- HTTPS（Let's Encrypt）
- nginx 限流 + fail2ban 自动封禁
- SQL 参数化查询防注入
- ICP 备案

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + Vite + Pinia + Vue Router |
| 后端 | FastAPI (Python) |
| 数据库 | MySQL / SQLite |
| AI | DeepSeek API (OpenAI 兼容端点) |
| 数学渲染 | KaTeX + Plotly.js |
| 部署 | Alibaba Cloud ECS + nginx + systemd |

## 本地开发

```bash
# 后端
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY 和 JWT_SECRET_KEY
uvicorn server.main:app --reload

# 前端
cd frontend
npm install
npm run dev

# 数据库（可选，默认 SQLite）
# 设置环境变量 DATABASE_URL=mysql://user:pass@localhost/mathlearnlab
```

## 项目结构

```
mathlearnlab/
├── frontend/            # Vue 3 SPA
│   └── src/
│       ├── views/       # 页面组件
│       ├── components/  # 通用组件
│       └── stores/      # Pinia 状态管理
├── server/
│   ├── main.py          # FastAPI 入口
│   ├── config.py        # 配置
│   ├── routers/         # API 路由
│   ├── services/        # 业务逻辑
│   ├── models/          # 数据模型
│   └── static/          # 静态文件
├── content/             # Markdown 内容
│   ├── notebooks/       # 教材内容
│   ├── exhibits/        # 展项 Tab 内容
│   └── news/            # 博客文章
├── data/                # 运行时数据（数据库、用户文件）
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
└── LICENSE
```

## 安全配置

### 环境变量

详见 `.env.example`。生产环境**必须**设置以下变量：

| 变量 | 说明 | 是否必填 |
|------|------|---------|
| `JWT_SECRET_KEY` | JWT 签名密钥，用于防止令牌伪造 | 是 |
| `ADMIN_SECRET` | 管理后台访问密钥 | 是 |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 是 |
| `DATABASE_URL` | 数据库连接字符串 | 否（留空则用 SQLite） |
| `SMTP_*` | 邮件通知配置 | 否 |

### 密钥生成

```bash
# JWT 密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Admin 密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

> **警告**：切勿将 `.env` 文件提交到 Git。`.env` 已在 `.gitignore` 中。

## 许可

MIT License — 见 [LICENSE](LICENSE) 文件。

## 联系

- 网站：https://www.mathlearnlab.cn
- 邮箱：hilaryzhang98@163.com
