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
      // Load commonly used packages
      await pyodide.loadPackage(['numpy', 'matplotlib', 'sympy', 'micropip']);
      // Flush pending
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

  // Find all <pre><code class="language-python"> blocks and make them executable
  function makeExecutable() {
    document.querySelectorAll('pre code.language-python, pre code.language-python, .language-python').forEach(function(codeBlock, i) {
      var pre = codeBlock.closest('pre');
      if (!pre || pre.dataset.pyodideReady) return;
      pre.dataset.pyodideReady = '1';

      // Create run button
      var btn = document.createElement('button');
      btn.textContent = '▶ 运行';
      btn.className = 'btn btn-sm py-run-btn';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:5;font-size:11px;padding:3px 10px;';
      btn.onclick = function() { runCode(codeBlock, pre); };

      // Create output area
      var output = document.createElement('div');
      output.className = 'py-output';
      output.style.cssText = 'background:#1a1a2e;color:#e0e0e0;padding:8px 12px;border-radius:0 0 4px 4px;font-family:monospace;font-size:12px;max-height:300px;overflow-y:auto;display:none;white-space:pre-wrap;';

      // Wrap pre in a container
      var wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;margin:8px 0;';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      wrapper.appendChild(btn);
      wrapper.appendChild(output);

      // Also add to viz container if exists
      addInlineWidget(pre, codeBlock);
    });
  }

  function addInlineWidget(pre, codeBlock) {
    // Check if this cell is a visualization cell
    var code = codeBlock.textContent;
    if (code.indexOf('plot_epsilon_delta') > -1 ||
        code.indexOf('plot_') > -1 ||
        code.indexOf('plt.plot') > -1 ||
        code.indexOf('fig') > -1) {
      pre.style.cursor = 'pointer';
      pre.title = '点击运行此可视化代码';
    }
  }

  async function runCode(codeBlock, pre) {
    var btn = pre.parentNode.querySelector('.py-run-btn');
    var output = pre.parentNode.querySelector('.py-output');
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
      // Capture stdout
      var outputLines = [];
      py.setStdout({ batched: function(text) { outputLines.push(text); } });
      py.setStderr({ batched: function(text) { outputLines.push('ERR: ' + text); } });

      var code = codeBlock.textContent;

      // Strip matplotlib widget magic (Pyodide doesn't support %matplotlib widget)
      code = code.replace(/%matplotlib\s+widget/g, '# %matplotlib widget (skipped in browser)');
      code = code.replace(/%matplotlib\s+inline/g, '# %matplotlib inline (skipped)');

      // Run the code
      await py.runPythonAsync(code);

      // Show output
      if (outputLines.length > 0) {
        output.textContent = outputLines.join('');
      } else {
        output.textContent = '✅ 执行完毕';
      }

      // Try to render matplotlib figure if any
      try {
        var figCode = `
import io, base64
_figs = []
try:
    import matplotlib.pyplot as _plt
    _figs = [_plt.figure(i) for i in _plt.get_fignums()]
except: pass
_figs
`;
        var figs = py.runPython(figCode);
        if (figs && figs.toJs) figs = figs.toJs();
        if (figs && figs.length > 0) {
          // Render first figure
          var imgCode = `
import io, base64
import matplotlib.pyplot as plt
buf = io.BytesIO()
plt.savefig(buf, format='svg', bbox_inches='tight')
buf.seek(0)
result = buf.getvalue().decode('utf-8')
result
`;
          try {
            var svg = py.runPython(imgCode);
            if (svg && typeof svg === 'string') {
              var imgDiv = document.createElement('div');
              imgDiv.innerHTML = svg;
              imgDiv.style.cssText = 'background:white;padding:12px;border-radius:4px;margin-top:4px;overflow-x:auto;';
              output.appendChild(imgDiv);
              // Rerun MathJax
              if (window.MathJax) MathJax.typesetPromise([imgDiv]);
            }
          } catch(e) {}
        }
      } catch(e) {}

    } catch(e) {
      output.textContent = '错误: ' + e.message;
    }

    btn.textContent = '▶ 运行';
    btn.disabled = false;

    // Rerun MathJax on any new LaTeX
    if (window.MathJax) MathJax.typesetPromise();
  }

  // Auto-detect code blocks on page load
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(makeExecutable, 500);
  });

  // Also run immediately
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    setTimeout(makeExecutable, 500);
  }

  return { makeExecutable: makeExecutable, runCode: runCode };
})();
