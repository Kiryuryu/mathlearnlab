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
- 数学聊天助手（DeepSeek V4 / R1）

### 用户系统
- 注册审核制（管理员邮箱审批）
- MySQL 持久化存储
- API Key 本地加密存储

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
| AI | DeepSeek API (OpenAI 兼容) |
| 数学渲染 | MathJax 3 + Plotly.js |
| 部署 | Alibaba Cloud ECS + nginx + systemd |

## 本地开发

```bash
# 后端
pip install -r requirements.txt
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
│   └── templates/       # Jinja2 模板（旧版，逐步废弃）
├── content/             # Markdown 内容
│   ├── notebooks/       # 教材内容
│   ├── exhibits/        # 展项 Tab 内容
│   └── news/            # 博客文章
├── data/
│   └── problem_bank/    # 题库 JSON
└── requirements.txt
```

## 许可

MIT License

## 联系

- 网站：https://www.mathlearnlab.cn
- 邮箱：hilaryzhang98@163.com
