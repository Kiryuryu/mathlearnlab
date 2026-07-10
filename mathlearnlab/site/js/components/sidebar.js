// Sidebar navigation

document.addEventListener('DOMContentLoaded', () => {
  renderSidebar();
  setupSidebarMobile();
});

function renderSidebar() {
  const container = document.getElementById('sidebarContent');
  if (!container) return;

  const sections = [
    {
      title: '📘 学习内容',
      items: [
        { icon: '📈', label: '极限与连续',    route: 'notebooks/01-gaoshu/01-limits' },
        { icon: '📉', label: '微分学',        route: 'notebooks/01-gaoshu/02-integration', indent: true },
        { icon: '∫',  label: '积分学',        route: 'notebooks/01-gaoshu/02-integration', indent: false },
      ],
      sub: [
        { icon: '📈', label: '极限与连续', route: 'notebooks/01-gaoshu/01-limits' },
        { icon: '📉', label: '微分学',     route: 'notebooks/01-gaoshu/01-limits' },
        { icon: '∫',  label: '积分学',     route: 'notebooks/01-gaoshu/02-integration' },
        { icon: 'Σ',  label: '无穷级数',   route: 'notebooks/01-gaoshu/03-series' },
        { icon: '🌐', label: '多元微积分',  route: 'notebooks/01-gaoshu/04-multivariable' },
      ],
    },
    {
      title: '📝 知识笔记',
      items: [
        { icon: '📐', label: '高等数学', route: 'notes/01-gaoshu' },
        { icon: '🔢', label: '线性代数', route: 'notes/02-xiandai' },
        { icon: '🎲', label: '概率论',   route: 'notes/03-gailvlun' },
      ],
    },
    {
      title: '📐 解题集',
      items: [
        { icon: '📈', label: '极限与连续', route: 'problems/01-gaoshu/limits' },
        { icon: '∫',  label: '积分学',    route: 'problems/01-gaoshu/integration' },
        { icon: 'Σ',  label: '无穷级数',  route: 'problems/01-gaoshu/series' },
        { icon: '🌐', label: '多元微积分', route: 'problems/01-gaoshu/multivariable' },
      ],
    },
    {
      title: '📋 错题本',
      items: [
        { icon: '📕', label: '高等数学', route: 'error-log/01-gaoshu' },
      ],
    },
    {
      title: '🎯 OCR 刷题',
      items: [
        { icon: '📈', label: '极限与连续', route: 'practice/limits' },
        { icon: '📉', label: '微分学',     route: 'practice/derivatives' },
        { icon: '∫',  label: '积分学',     route: 'practice/integrals' },
        { icon: 'Σ',  label: '无穷级数',   route: 'practice/series' },
        { icon: '🌐', label: '多元微积分', route: 'practice/multivariable' },
      ],
    },
  ];

  // Fix the "学习内容" section to have expanded subsections properly
  let html = '';

  // Section: 学习内容 (高等数学 notebooks)
  html += '<div class="sidebar-section">';
  html += '<div class="sidebar-section-title">📘 学习内容 · 高等数学</div>';
  const notebookItems = [
    { icon: '📈', label: '极限、连续与微分', route: 'notebooks/01-gaoshu/01-limits' },
    { icon: '∫',  label: '积分学',           route: 'notebooks/01-gaoshu/02-integration' },
    { icon: 'Σ',  label: '无穷级数',          route: 'notebooks/01-gaoshu/03-series' },
    { icon: '🌐', label: '多元微积分',         route: 'notebooks/01-gaoshu/04-multivariable' },
  ];
  notebookItems.forEach(item => {
    html += `<button class="sidebar-item" data-route="${item.route}">
      <span class="item-icon">${item.icon}</span>${item.label}
    </button>`;
  });
  html += `<div style="padding:4px 20px;font-size:11px;color:var(--text-sidebar);opacity:0.4;margin-top:4px;">线性代数 · 概率论 · 待添加</div>`;
  html += '</div>';

  // Other sections
  const otherSections = sections.slice(1);
  otherSections.forEach(section => {
    html += '<div class="sidebar-section">';
    html += `<div class="sidebar-section-title">${section.title}</div>`;
    section.items.forEach(item => {
      html += `<button class="sidebar-item" data-route="${item.route}">
        <span class="item-icon">${item.icon}</span>${item.label}
      </button>`;
    });
    html += '</div>';
  });

  container.innerHTML = html;

  // Bind click events
  container.querySelectorAll('.sidebar-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const route = btn.dataset.route;
      if (route) {
        window.location.hash = '#' + route;
        // Close sidebar on mobile
        document.getElementById('sidebar')?.classList.remove('open');
        document.getElementById('sidebarOverlay')?.setAttribute('hidden', '');
      }
    });
  });

  // Highlight active
  updateSidebarActive();
}

function updateSidebarActive() {
  const currentRoute = window.location.hash.slice(1) || 'home';
  document.querySelectorAll('.sidebar-item').forEach(btn => {
    const route = btn.dataset.route;
    btn.classList.toggle('active', route === currentRoute);
  });
}

function setupSidebarMobile() {
  const toggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (toggle) {
    toggle.addEventListener('click', () => {
      sidebar?.classList.toggle('open');
      if (sidebar?.classList.contains('open')) {
        overlay?.removeAttribute('hidden');
      } else {
        overlay?.setAttribute('hidden', '');
      }
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar?.classList.remove('open');
      overlay.setAttribute('hidden', '');
    });
  }
}
