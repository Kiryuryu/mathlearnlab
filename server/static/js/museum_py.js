// MuseumPy — Code block handling for museum pages.
// Hides notebook Python code by default; keeps visualizations in museum_viz.js
var MuseumPy = (function() {

  function init() {
    document.querySelectorAll('pre code.language-python').forEach(function(codeBlock, i) {
      var pre = codeBlock.closest('pre');
      if (!pre || pre.dataset.pyodideHandled) return;
      pre.dataset.pyodideHandled = '1';

      // Create wrapper
      var wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;margin:8px 0;';

      // Collapse code block by default
      var toggleBtn = document.createElement('button');
      toggleBtn.className = 'btn btn-sm py-code-toggle';
      toggleBtn.style.cssText = 'font-size:11px;padding:2px 8px;display:inline-block;margin-bottom:4px;';
      toggleBtn.textContent = '📝 查看代码';
      toggleBtn.onclick = function() {
        var visible = pre.style.display !== 'none';
        pre.style.display = visible ? 'none' : '';
        toggleBtn.textContent = visible ? '📝 查看代码' : '🫥 隐藏代码';
        // Remove the full "show" button if it exists
        var showBtn = wrapper.querySelector('.py-show-btn');
        if (showBtn) showBtn.style.display = visible ? '' : 'none';
      };

      pre.style.display = 'none'; // Hidden by default

      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      wrapper.appendChild(toggleBtn);

      // If this is an "interact" block, show a small hint
      var code = codeBlock.textContent;
      if (/interact\s*\(/.test(code) && i > 0) {
        var hint = document.createElement('span');
        hint.className = 'py-show-btn';
        hint.style.cssText = 'font-size:11px;color:var(--text-muted);margin-left:8px;';
        hint.textContent = '← 互动代码';
        wrapper.appendChild(hint);
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(init, 300);
  });
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    setTimeout(init, 300);
  }

  return { init: init };
})();
