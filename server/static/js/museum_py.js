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

  // Convert Jupyter widget code to plain Python that Pyodide can run.
  // e.g. interact(func, x=FloatSlider(value=0.5))  →  func(x=0.5)
  // e.g. interact(plot_3d, angle=Dropdown(value='30', options=['30','60']), ...)
  //       → plot_3d(angle='30')
  function adaptCode(code) {
    var lines = code.split('\n');
    var result = [];
    var merged = code; // for multiline interact()

    // Step 1: Convert multiline interact to single line
    merged = merged.replace(/interact\s*\(\s*([\s\S]*?)\)/g, function(match) {
      return match.replace(/\n\s+/g, ' ').replace(/\s+/g, ' ');
    });

    var adapted = merged.split('\n');

    for (var i = 0; i < adapted.length; i++) {
      var line = adapted[i];
      var trimmed = line.trim();
      if (!trimmed) continue;

      // Skip notebook-only lines
      if (/^\s*%matplotlib/.test(line)) continue;
      if (/from\s+ipywidgets\s+import/.test(line)) continue;
      if (/from\s+IPython/.test(line)) continue;
      if (/from\s+utils\.plot_config/.test(line)) continue;
      if (/set_style\s*\(/.test(line)) continue;
      if (/COLORS\b.*annotate_point/.test(line)) continue;
      if (/from\s+matplotlib\.animation/.test(line)) continue;
      if (/FuncAnimation/.test(line)) continue;
      if (/sys\.path\.insert/.test(line)) continue; // local path

      // Convert interact(func, param=Widget(value=X, ...)) → func(param=X)
      var interactMatch = trimmed.match(/^interact\s*\(\s*(\w+)\s*,?\s*(.+)\)\s*$/);
      if (interactMatch) {
        var funcName = interactMatch[1];
        var argsStr = interactMatch[2];

        // Extract parameter names and their default values from Widget(value=X)
        var paramExprs = [];
        var paramRegex = /(\w+)\s*=\s*(?:FloatSlider|IntSlider|Dropdown|SelectionSlider|ToggleButtons)\s*\([^)]*?value\s*=\s*([^,)\s]+)/g;
        var pm;
        while ((pm = paramRegex.exec(argsStr)) !== null) {
          paramExprs.push(pm[1] + '=' + pm[2]);
        }

        // Also handle simple parameter=widget pattern without value= keyword
        if (paramExprs.length === 0) {
          // Fallback: try to extract just simple keyword=value pairs
          var simpleRegex = /(\w+)\s*=\s*(?:FloatSlider|IntSlider|Dropdown)[^)]*?value\s*=\s*['"]?([^,'")]+)['"]?/g;
          while ((pm = simpleRegex.exec(argsStr)) !== null) {
            paramExprs.push(pm[1] + '=' + pm[2]);
          }
        }

        if (paramExprs.length > 0) {
          result.push(funcName + '(' + paramExprs.join(', ') + ')');
        } else {
          // Last resort: try to just call the function without arguments
          result.push(funcName + '()');
        }
        continue;
      }

      result.push(line);
    }

    // Deduplicate consecutive empty lines
    var final = [];
    for (var i = 0; i < result.length; i++) {
      if (result[i].trim() === '' && i > 0 && result[i-1].trim() === '') continue;
      final.push(result[i]);
    }

    return final.join('\n');
  }

  // Make all code blocks executable. First block auto-runs as setup.
  function makeExecutable() {
    var blocks = document.querySelectorAll('pre code.language-python');
    if (!blocks.length) return;

    var firstBlock = blocks[0];
    var isSetup = /^(import |from |%matplotlib|\s*$|\s*#)/m.test(firstBlock.textContent);

    blocks.forEach(function(codeBlock, idx) {
      var pre = codeBlock.closest('pre');
      if (!pre || pre.dataset.pyodideReady) return;
      pre.dataset.pyodideReady = '1';

      var wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;margin:8px 0;';

      var isFirst = (idx === 0 && isSetup);

      if (isFirst) {
        // Setup block: auto-run, compact indicator
        var status = document.createElement('span');
        status.className = 'py-setup-status';
        status.style.cssText = 'position:absolute;top:6px;right:8px;z-index:5;font-size:10px;color:var(--accent);opacity:0.7;';
        status.textContent = '⏳';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        wrapper.appendChild(status);

        // Auto-run setup on load
        (function(block, preEl, stEl) {
          var check = setInterval(function() {
            if (window._pyodideReady) {
              clearInterval(check);
              runSetup(block, preEl, stEl);
            }
          }, 300);
          // Timeout fallback: load pyodide and run
          setTimeout(function() {
            clearInterval(check);
            if (stEl.textContent === '⏳') runSetup(block, preEl, stEl);
          }, 2000);
        })(codeBlock, pre, status);
        return;
      }

      // Normal block: Run button
      var btn = document.createElement('button');
      btn.textContent = '▶ 运行';
      btn.className = 'btn btn-sm py-run-btn';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:5;font-size:11px;padding:3px 10px;';
      btn.onclick = function() { runCode(codeBlock, pre); };

      var output = document.createElement('div');
      output.className = 'py-output';
      output.style.cssText = 'background:#1a1a2e;color:#e0e0e0;padding:8px 12px;border-radius:0 0 4px 4px;font-family:monospace;font-size:12px;max-height:400px;overflow-y:auto;display:none;white-space:pre-wrap;';

      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      wrapper.appendChild(btn);
      wrapper.appendChild(output);
    });

    // Add "Run All" bar above code blocks if there are multiple
    if (blocks.length > 1 && isSetup) {
      var firstWrapper = blocks[0].closest('pre').parentNode;
      var runAllBar = document.createElement('div');
      runAllBar.className = 'py-runall-bar';
      runAllBar.style.cssText = 'display:flex;align-items:center;gap:8px;padding:4px 0;margin-bottom:4px;font-size:12px;';
      runAllBar.innerHTML = '<span style="color:var(--text-muted);">代码块:</span><button class="btn btn-sm" style="font-size:11px;" id="btnRunAll">▶ 全部运行</button>';
      firstWrapper.parentNode.insertBefore(runAllBar, firstWrapper);

      document.getElementById('btnRunAll').onclick = function() {
        var btn = document.getElementById('btnRunAll');
        btn.textContent = '⏳ 运行中...';
        btn.disabled = true;
        runAllBlocks(blocks).then(function() {
          btn.textContent = '✓ 完成';
          setTimeout(function() { btn.textContent = '▶ 全部运行'; btn.disabled = false; }, 2000);
        });
      };
    }
  }

  async function runSetup(codeBlock, pre, statusEl) {
    var py = await ensurePyodide();
    if (!py) { statusEl.textContent = '✗ 加载失败'; return; }

    try {
      py.setStdout({ batched: function(t) {} });
      py.setStderr({ batched: function(t) {} });

      var code = adaptCode(codeBlock.textContent);
      // Inject fallbacks before setup
      try {
        py.runPython('COLORS = ["#5b7b94","#b55a5a","#8b7355","#4a7c59"]\ndef annotate_point(*a,**k): pass\ndef set_style(): pass\n');
      } catch(e) {}

      await py.runPythonAsync(code);

      // Try init_printing
      try { py.runPython('import sympy as sp; sp.init_printing()'); } catch(e) {}

      statusEl.textContent = '✓ Ready';
      statusEl.style.color = 'var(--accent-correct)';
      window._pyodideReady = true;
    } catch(e) {
      statusEl.textContent = '✗ Error';
      statusEl.style.color = 'var(--accent-error)';
      statusEl.title = e.message;
    }
  }

  async function runAllBlocks(blocks) {
    for (var i = 1; i < blocks.length; i++) {
      var pre = blocks[i].closest('pre');
      var wrapper = pre.parentNode;
      var output = wrapper.querySelector('.py-output');
      if (output) {
        output.style.display = 'block';
        output.textContent = '';
      }
      await runCode(blocks[i], pre);
    }
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

      var code = adaptCode(codeBlock.textContent);

      if (!code.trim()) {
        output.textContent = '✅ 代码中无可执行内容（仅包含 notebook 配置）';
        btn.textContent = '▶ 运行';
        btn.disabled = false;
        return;
      }

      // Inject fallback for missing local utils
      try {
        py.runPython('# __FALLBACKS__\nCOLORS = ["#5b7b94","#b55a5a","#8b7355","#4a7c59"]\ndef annotate_point(*a,**k): pass\ndef set_style(): pass\n');
      } catch(e) {}

      await py.runPythonAsync(code);

      // Show printed output
      var printed = outputLines.join('');
      if (printed) {
        output.textContent = printed;
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

      // Show done message if nothing else was output
      if (!printed && output.children.length === 0) {
        output.textContent = '✅ 执行完毕';
      }

    } catch(e) {
      var msg = '错误: ' + e.message;
      if (e.message.indexOf('interact') > -1 || e.message.indexOf('FloatSlider') > -1) {
        msg += '\n\n💡 交互式组件无法在浏览器中运行。页面上的交互可视化图已可用。';
      }
      output.textContent = msg;
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
