// Theme toggle
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('themeToggle');
  if (!btn) return;

  // Apply saved theme on load
  const savedTheme = Storage.getTheme();
  applyTheme(savedTheme);

  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  });
});

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  Storage.setTheme(theme);

  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';

  // Toggle highlight.js theme
  const hljsLight = document.getElementById('hljs-light');
  const hljsDark = document.getElementById('hljs-dark');
  if (hljsLight && hljsDark) {
    hljsLight.disabled = (theme === 'dark');
    hljsDark.disabled = (theme === 'light');
  }
}
