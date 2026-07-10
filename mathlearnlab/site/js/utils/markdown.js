// Markdown rendering with marked.js

let _markedReady = false;

function ensureMarked() {
  if (_markedReady) return;
  if (typeof marked === 'undefined') {
    console.warn('marked.js not loaded yet');
    return;
  }
  // Configure marked
  marked.setOptions({
    breaks: true,
    gfm: true,
  });
  // Set up highlight.js if available
  if (typeof hljs !== 'undefined') {
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value;
        }
        return code;
      }
    });
  }
  _markedReady = true;
}

async function renderMarkdown(mdText) {
  ensureMarked();
  if (typeof marked === 'undefined') {
    return `<pre>${escapeHtml(mdText)}</pre>`;
  }
  try {
    let html = marked.parse(mdText);
    return html;
  } catch (e) {
    console.error('Markdown parse error:', e);
    return `<pre>${escapeHtml(mdText)}</pre>`;
  }
}

async function loadAndRenderMarkdown(path) {
  try {
    const resp = await fetch(path);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const md = await resp.text();
    return await renderMarkdown(md);
  } catch (e) {
    console.error('Failed to load markdown:', path, e);
    return `<div class="content-error">
      <h3>⚠️ 内容加载失败</h3>
      <p>无法加载: ${escapeHtml(path)}</p>
      <p>请确认内容文件存在。</p>
    </div>`;
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// MathJax re-render after content changes
async function typesetMath(element) {
  if (window.MathJax && window.MathJax.typesetPromise) {
    try {
      await MathJax.typesetPromise([element]);
    } catch (e) {
      // MathJax may not be ready yet — retry once
      setTimeout(() => {
        if (window.MathJax && window.MathJax.typesetPromise) {
          MathJax.typesetPromise([element]).catch(() => {});
        }
      }, 500);
    }
  }
}
