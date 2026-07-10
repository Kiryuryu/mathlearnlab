# MathLearnLab 🧮

> 考研数学复习交互式学习仓库 — 用代码辅助计算与可视化，建立数学直觉

## 概述

本仓库面向考研数学（数学一/二/三）的复习备考，核心特色是**用 Python 代码辅助计算与可视化**，帮助你直观理解高等数学、线性代数、概率论中难以建立直觉的概念。

## 仓库结构

```
mathlearnlab/
├── notebooks/          # 🔥 核心：交互式 Jupyter Notebook
│   ├── 01-gaoshu/      #   高等数学（高数）
│   ├── 02-xiandai/     #   线性代数（线代）
│   └── 03-gailvlun/    #   概率论与数理统计（概率论）
├── ocr_practice/       # 🆕 OCR 刷题 Web 应用 (Streamlit)
├── utils/              # 共享 Python 工具模块
├── notes/              # 📝 知识笔记（Markdown）
├── problems/           # 📐 解题集（Markdown）
├── error-log/          # 📋 错题本（Markdown）
└── assets/             # 静态资源
```

## 快速开始

### 1. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动 Jupyter Lab

```bash
jupyter lab
```

### 4. 打开 Notebook

在 Jupyter Lab 界面中导航到 `notebooks/01-gaoshu/`，从第一个 notebook 开始。

## 技术栈

| 用途 | 工具 |
|------|------|
| 符号计算 | SymPy |
| 数值计算 | NumPy, SciPy |
| 2D 可视化 | Matplotlib + ipywidgets |
| 3D 可视化 | Plotly |
| 交互控件 | ipywidgets |

## 学习路线建议

### 高等数学
1. ⬜ 极限、连续与微分 → `notebooks/01-gaoshu/01-limits-continuity-differentiation.ipynb`
2. ⬜ 积分学 → `notebooks/01-gaoshu/02-integration.ipynb`
3. ⬜ 无穷级数 → `notebooks/01-gaoshu/03-infinite-series.ipynb`
4. ⬜ 多元微积分 → `notebooks/01-gaoshu/04-multivariable-calculus.ipynb`

### 线性代数
> 🚧 待添加

### 概率论与数理统计
> 🚧 待添加

## 使用方式

### 📘 概念学习 (Jupyter Notebook)

每个 Notebook 包含：
- **概念解释**：中文 + LaTeX 公式，清晰定义
- **符号验证**：SymPy 代码验证数学推导
- **交互可视化**：拖动滑块、播放动画，直观感受数学概念
- **小结与自测**：关键点回顾 + 常见错误 + 练习

```bash
pip install -r requirements.txt
jupyter lab
```

### 🎯 OCR 刷题 (Streamlit Web App)

大模型出题 → 纸笔作答 → 拍照上传 → AI 批改 → 错题自动记入错题本。

```bash
pip install -r requirements_ocr.txt

# 1. 设置 API Key（二选一）
echo 'ANTHROPIC_API_KEY = "sk-ant-..."' > .streamlit/secrets.toml  # 方式一
# 或在 Web 界面中手动输入                                          # 方式二

# 2. 启动应用
streamlit run ocr_practice/app.py

# 3. 浏览器打开 http://localhost:8501
```

**刷题流程**：
1. 在首页选择科目（极限/微分/积分/级数/多元）
2. 随机抽题或从题库中选题
3. 纸笔作答，完成后拍照上传
4. Claude API 读取手写答案，与标准答案对比
5. 获得 ✅/❌/⚠️ 判定 + 详细反馈 + 按步骤评分
6. 答错的题一键加入错题本 (`error-log/`)

> 💡 首次使用前运行 `python scripts/seed_problem_bank.py` 可以调用大模型扩充题库。

## 贡献

这是一个个人学习仓库。如果你有建议或发现了错误，欢迎提 Issue。

## 许可

MIT License
