// Theme toggle — dark/light

(function() {
  const STORAGE_KEY = 'mathlearnlab:theme';

  function getSavedTheme() {
    try { return localStorage.getItem(STORAGE_KEY) || 'light'; }
    catch { return 'light'; }
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem(STORAGE_KEY, theme); } catch {}
    const btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '◑' : '◐';
  }

  // Apply on load
  applyTheme(getSavedTheme());

  // Toggle button
  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }
  });
})();
