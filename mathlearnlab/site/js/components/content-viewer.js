// Content viewer — loads and renders markdown content

const ContentViewer = {
  async render(route) {
    const container = document.getElementById('mainContent');
    if (!container) return;

    // Show loading
    container.innerHTML = '<div class="content-loading">⏳ 加载中...</div>';

    if (route === 'home') {
      container.innerHTML = await this.renderHome();
      await typesetMath(container);
      return;
    }

    const filePath = CONFIG.ROUTES[route];
    if (!filePath) {
      container.innerHTML = `<div class="content-loading">
        <h3>🔍 页面未找到</h3>
        <p>路由 "${escapeHtml(route)}" 没有对应的内容。</p>
      </div>`;
      return;
    }

    // Check if it's a practice route
    if (filePath.startsWith('practice:')) {
      const topicKey = filePath.split(':')[1];
      OCRPractice.render(container, topicKey);
      return;
    }

    // Load and render markdown
    const html = await loadAndRenderMarkdown(filePath);
    container.innerHTML = `<div class="content-page">${html}</div>`;

    // Re-render MathJax
    await typesetMath(container);

    // Highlight code blocks
    if (typeof hljs !== 'undefined') {
      container.querySelectorAll('pre code').forEach(block => {
        hljs.highlightElement(block);
      });
    }
  },

  async renderHome() {
    const stats = Storage.getGradeStats();
    const totalProblems = Object.values(CONFIG.TOPICS).reduce((sum, t) => sum + 0, 0); // We'll count from session

    return `
      <div class="content-page">
        <h1>🧮 欢迎来到 MathLearnLab</h1>
        <p>考研数学复习一站式平台 — 概念学习 + 交互可视化 + AI 答疑 + OCR 刷题</p>

        <h2>📊 学习概览</h2>
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-value">${stats.total}</div>
            <div class="stat-label">总答题数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">${stats.accuracy}%</div>
            <div class="stat-label">正确率</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">✅ ${stats.correct}</div>
            <div class="stat-label">正确</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">❌ ${stats.incorrect}</div>
            <div class="stat-label">需复习</div>
          </div>
        </div>

        <h2>📘 高等数学</h2>
        <div class="home-grid">
          <div class="home-card" data-route="notebooks/01-gaoshu/01-limits">
            <div class="card-icon">📈</div>
            <h3>极限、连续与微分</h3>
            <p>ε-δ 定义、中值定理、泰勒展开、洛必达法则</p>
            <div class="card-meta">🖥 交互可视化 + 📝 笔记 + 📐 解题</div>
          </div>
          <div class="home-card" data-route="notebooks/01-gaoshu/02-integration">
            <div class="card-icon">∫</div>
            <h3>积分学</h3>
            <p>黎曼和、换元法、分部积分、旋转体体积、反常积分</p>
            <div class="card-meta">🖥 3D 旋转体可视化 + 📝 笔记 + 📐 解题</div>
          </div>
          <div class="home-card" data-route="notebooks/01-gaoshu/03-series">
            <div class="card-icon">Σ</div>
            <h3>无穷级数</h3>
            <p>审敛法、幂级数、泰勒级数、傅里叶级数、吉布斯现象</p>
            <div class="card-meta">🖥 谐波叠加动画 + 📝 笔记 + 📐 解题</div>
          </div>
          <div class="home-card" data-route="notebooks/01-gaoshu/04-multivariable">
            <div class="card-icon">🌐</div>
            <h3>多元微积分</h3>
            <p>偏导数、梯度下降、拉格朗日乘数、二重积分、线积分</p>
            <div class="card-meta">🖥 3D 梯度下降可视化 + 📝 笔记 + 📐 解题</div>
          </div>
        </div>

        <h2>🎯 快速入口</h2>
        <div class="home-grid">
          <div class="home-card" data-route="practice/integrals">
            <div class="card-icon">📸</div>
            <h3>OCR 刷题 — 积分学</h3>
            <p>拍照上传手写答案 → AI 自动批改 → 错题自动记录</p>
            <div class="card-meta">👆 点击开始刷题</div>
          </div>
          <div class="home-card" data-route="error-log/01-gaoshu">
            <div class="card-icon">📋</div>
            <h3>错题本</h3>
            <p>查看所有答错的题目和分析，针对性复习</p>
            <div class="card-meta">👆 点击查看错题</div>
          </div>
        </div>

        <h2>💡 使用提示</h2>
        <ul>
          <li>📘 <strong>左侧导航</strong>选择学习内容或刷题</li>
          <li>🤖 <strong>右侧 AI 助手</strong>随时提问（华里士公式？格林公式？）</li>
          <li>📸 <strong>OCR 刷题</strong>：纸笔作答 → 拍照上传 → AI 批改</li>
          <li>🖥 <strong>交互可视化</strong>：部分内容引用了 Jupyter Notebook，建议本地运行 <code>jupyter lab</code> 获取完整体验</li>
        </ul>
      </div>
    `;
  },
};

// Make clickable cards on home page
document.addEventListener('click', (e) => {
  const card = e.target.closest('.home-card');
  if (card && card.dataset.route) {
    window.location.hash = '#' + card.dataset.route;
  }
});
