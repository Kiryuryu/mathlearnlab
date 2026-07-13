// MuseumPy — Run Python code cells via Pyodide (in-browser Python)
var MuseumPy = (function() {
  var pyodide = null;
  var loading = false;
  var pending = [];

  async function ensurePyodide() {
    if (pyodide) return pyodide;
    if (loading) {
      return new Promise(function(resolve) { pending.push(resolve); });
    }
    loading = true;
    try {
      pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
      });
      await pyodide.loadPackage(['numpy', 'matplotlib', 'sympy', 'micropip']);
      pending.forEach(function(r) { r(pyodide); });
      pending = [];
      return pyodide;
    } catch(e) {
      console.error('Pyodide load failed:', e);
      return null;
    } finally {
      loading = false;
    }
  }

  // Detects whether a code block requires Jupyter (uses ipywidgets, interact, etc.)
  function isNotebookOnly(code) {
    return /ipywidgets|interact\s*\(|FloatSlider|IntSlider|Play\b|jslink|VBox\b|HBox\b|IPython\.display|%matplotlib\s+widget|Output\(|clear_output|FuncAnimation/.test(code);
  }

  // Strip notebook-only lines from code
  function stripNotebookCode(code) {
    return code.split('\n').filter(function(line) {
      var trimmed = line.trim();
      if (!trimmed) return false; // skip empty lines
      if (/^\s*%matplotlib/.test(line)) return false;
      if (/from\s+ipywidgets\s+import/.test(line)) return false;
      if (/from\s+IPython/.test(line)) return false;
      if (/interact\s*\(/.test(line)) return false;
      if (/from\s+utils\.plot_config/.test(line)) return false;
      if (/set_style\s*\(/.test(line)) return false;
      if (/COLORS\b.*annotate_point/.test(line)) return false;
      if (/FuncAnimation/.test(line)) return false;
      if (/from\s+matplotlib\.animation/.test(line)) return false;
      return true;
    }).join('\n');
  }

  // Make code blocks executable
  function makeExecutable() {
    document.querySelectorAll('pre code.language-python').forEach(function(codeBlock, i) {
      var pre = codeBlock.closest('pre');
      if (!pre || pre.dataset.pyodideReady) return;
      pre.dataset.pyodideReady = '1';

      var code = codeBlock.textContent;
      var isNotebook = isNotebookOnly(code);

      // Create wrapper
      var wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;margin:8px 0;';

      // Detect if it's a simple import/setup block (often first cell)
      var isSetup = /^(import |from |%matplotlib|\s*$|\s*#)/m.test(code) && code.split('\n').filter(function(l){return l.trim();}).length <= 10;

      if (isNotebook) {
        // Notebook-only block: show info button
        var btn = document.createElement('button');
        btn.textContent = '📓 Jupyter 查看';
        btn.className = 'btn btn-sm py-run-btn py-jupyter-btn';
        btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:5;font-size:11px;padding:3px 10px;opacity:0.6;';
        btn.title = '此代码使用 ipywidgets 交互组件，需要在本地 Jupyter 中运行';
        btn.onclick = function() {
          // Show a hint panel
          var existing = wrapper.querySelector('.py-jupyter-hint');
          if (existing) { existing.remove(); return; }
          var hint = document.createElement('div');
          hint.className = 'py-jupyter-hint';
          hint.style.cssText = 'background:var(--bg-nav);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin-top:4px;font-size:13px;color:var(--text-secondary);line-height:1.7;';
          hint.innerHTML = '<strong>📓 此代码需要本地 Jupyter 环境</strong><br>它使用了 <code>ipywidgets</code> 交互组件（滑块、下拉菜单等），这些在浏览器中无法运行。<br><br>👉 运行 <code>jupyter lab</code> 启动本地环境，打开对应的 <code>.ipynb</code> 文件即可体验完整交互。';
          wrapper.appendChild(hint);
        };
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        wrapper.appendChild(btn);
        return; // Don't add output area for notebook blocks
      }

      // Executable block
      var btn = document.createElement('button');
      btn.textContent = '▶ 运行';
      btn.className = 'btn btn-sm py-run-btn';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:5;font-size:11px;padding:3px 10px;';
      btn.onclick = function() { runCode(codeBlock, pre); };

      var output = document.createElement('div');
      output.className = 'py-output';
      output.style.cssText = 'background:#1a1a2e;color:#e0e0e0;padding:8px 12px;border-radius:0 0 4px 4px;font-family:monospace;font-size:12px;max-height:300px;overflow-y:auto;display:none;white-space:pre-wrap;';

      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      wrapper.appendChild(btn);
      wrapper.appendChild(output);

      // Skip auto-run for setup blocks
      if (isSetup) {
        pre.style.cursor = 'default';
      }
    });
  }

  async function runCode(codeBlock, pre) {
    var wrapper = pre.parentNode;
    var btn = wrapper.querySelector('.py-run-btn');
    var output = wrapper.querySelector('.py-output');
    if (!btn || !output) return;

    btn.textContent = '⏳ 加载中...';
    btn.disabled = true;
    output.style.display = 'block';
    output.textContent = '';

    var py = await ensurePyodide();
    if (!py) {
      output.textContent = 'Pyodide 加载失败，请刷新页面重试';
      btn.textContent = '▶ 运行';
      btn.disabled = false;
      return;
    }

    btn.textContent = '⏳ 运行中...';

    try {
      var outputLines = [];
      py.setStdout({ batched: function(text) { outputLines.push(text); } });
      py.setStderr({ batched: function(text) { outputLines.push('ERR: ' + text); } });

      var code = codeBlock.textContent;
      code = stripNotebookCode(code);

      if (!code.trim()) {
        output.textContent = 'ℹ️ 此代码仅包含 Jupyter 特定组件，请在本地 Jupyter 中运行完整笔记本。';
        btn.textContent = '▶ 运行';
        btn.disabled = false;
        return;
      }

      // Inject fallback for missing utils
      try {
        py.runPython('COLORS = ["#5b7b94","#b55a5a","#8b7355","#4a7c59"]\ndef annotate_point(*a,**k): pass\n');
      } catch(e) {}

      await py.runPythonAsync(code);

      if (outputLines.length > 0) {
        output.textContent = outputLines.join('');
      } else {
        output.textContent = '✅ 执行完毕';
      }

      // Render matplotlib figure
      try {
        var hasFig = py.runPython("import matplotlib.pyplot as _plt; len(_plt.get_fignums()) > 0");
        if (hasFig) {
          var svg = py.runPython(`
import io, base64, matplotlib.pyplot as plt
buf = io.BytesIO()
plt.savefig(buf, format='svg', bbox_inches='tight')
buf.seek(0)
buf.getvalue().decode('utf-8')
`);
          if (svg && typeof svg === 'string') {
            var imgDiv = document.createElement('div');
            imgDiv.innerHTML = svg;
            imgDiv.style.cssText = 'background:white;padding:12px;border-radius:4px;margin-top:4px;overflow-x:auto;';
            output.appendChild(imgDiv);
            if (window.MathJax) MathJax.typesetPromise([imgDiv]);
          }
        }
      } catch(e) {}

    } catch(e) {
      output.textContent = '错误: ' + e.message;
      if (e.message.indexOf('interact') > -1) {
        output.textContent += '\n\n💡 此代码需要在本地 Jupyter 中运行。运行 jupyter lab 打开对应的 .ipynb 文件。';
      }
    }

    btn.textContent = '▶ 运行';
    btn.disabled = false;
    if (window.MathJax) MathJax.typesetPromise();
  }

  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(makeExecutable, 500);
  });
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    setTimeout(makeExecutable, 500);
  }

  return { makeExecutable: makeExecutable, runCode: runCode };
})();
