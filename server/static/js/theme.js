// Theme toggle — dark/light, auto-detect system preference
(function() {
  const STORAGE_KEY = 'mathlearnlab:theme';

  function systemPrefersDark() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function getSavedTheme() {
    try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
  }

  function resolveTheme() {
    var saved = getSavedTheme();
    if (saved === 'dark' || saved === 'light') return saved;
    return systemPrefersDark() ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem(STORAGE_KEY, theme); } catch {}
    var btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '◑' : '◐';
  }

  // Apply on load
  applyTheme(resolveTheme());

  // Toggle button
  document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', function() {
        var current = document.documentElement.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }
  });

  // Listen for system preference changes (when user hasn't set manual preference)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
    if (!getSavedTheme()) applyTheme(systemPrefersDark() ? 'dark' : 'light');
  });
})();
