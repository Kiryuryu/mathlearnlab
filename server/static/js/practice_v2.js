// Practice v2 — AI-powered problem generation + refresh
var PracticeV2 = (function() {
  var currentTopic = '';
  var currentProblem = null;
  var imageBase64 = null;
  var result = null;

  function init(topic) {
    currentTopic = topic;
  }

  function $id(id) { return document.getElementById(id); }

  async function loadProblems() {
    try {
      var resp = await fetch('/api/practice/' + currentTopic + '/problems');
      var data = await resp.json();
      renderProblemList(data.problems || []);
    } catch(e) { alert('加载失败: ' + e.message); }
  }

  async function randomProblem() {
    $id('practiceStatus').textContent = '加载中...';
    try {
      var resp = await fetch('/api/practice/' + currentTopic + '/problems/random');
      var data = await resp.json();
      currentProblem = data.problem;
      renderSolve();
    } catch(e) { alert('加载失败: ' + e.message); }
    $id('practiceStatus').textContent = '';
  }

  async function aiGenerate() {
    var diff = $id('diffFilter') ? $id('diffFilter').value : 'medium';
    $id('practiceStatus').textContent = 'AI 正在生成新题目...';
    try {
      var apiKey = '';
      try { apiKey = localStorage.getItem('mathlearnlab:apikey') || ''; } catch(e) {}
      var resp = await fetch('/api/practice/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
        body: JSON.stringify({ topic_key: currentTopic, difficulty: diff }),
      });
      if (!resp.ok) throw new Error((await resp.json()).detail || '生成失败');
      var data = await resp.json();
      currentProblem = data.problem;
      renderSolve();
    } catch(e) { alert('AI 生成失败: ' + e.message); }
    $id('practiceStatus').textContent = '';
  }

  function renderProblemList(problems) {
    var list = $id('problemList');
    if (!list) return;
    if (!problems.length) { list.innerHTML = '<p style="color:var(--text-muted);">暂无题目，点击"AI 出题"</p>'; return; }
    list.innerHTML = problems.map(function(p) {
      return '<div class="problem-list-item" onclick="PracticeV2.selectProblem(\'' + p.id + '\')" data-difficulty="' + (p.difficulty || '') + '">' +
        '<div><strong>' + (p.id || '?') + '</strong> — ' + (p.preview || '') + '</div>' +
        '<span style="font-size:18px;color:var(--text-muted);">→</span></div>';
    }).join('');
  }

  async function selectProblem(id) {
    try {
      var resp = await fetch('/api/practice/' + currentTopic + '/problems/' + id);
      var data = await resp.json();
      currentProblem = data.problem;
      renderSolve();
    } catch(e) { alert('加载失败: ' + e.message); }
  }

  function renderSolve() {
    if (!currentProblem) return;
    $id('phaseSelect').style.display = 'none';
    $id('phaseResults').style.display = 'none';
    $id('phaseSolve').style.display = 'block';

    var p = currentProblem;
    $id('solveContent').innerHTML =
      '<div class="problem-card">' +
        '<div class="problem-meta"><span>' + (p.difficulty || '') + '</span><span>' + ((p.knowledge_points || []).slice(0,3).join(' · ')) + '</span></div>' +
        '<h3>' + (p.id || '') + '</h3>' +
        '<div>' + (p.problem_statement || '') + '</div>' +
      '</div>' +
      '<div class="upload-area" onclick="document.getElementById(\'fileInput\').click()">' +
        '<p>点击拍照或上传图片</p><p style="font-size:12px;color:var(--text-muted);">JPG / PNG</p>' +
        '<input type="file" id="fileInput" accept="image/*" capture="environment" onchange="PracticeV2.handleFile(event)" style="display:none;">' +
      '</div>' +
      '<div id="imagePreview" style="display:none;margin:12px 0;">' +
        '<img id="previewImg" style="max-width:100%;max-height:300px;border-radius:8px;border:1px solid var(--border);">' +
        '<button class="btn btn-sm" onclick="PracticeV2.clearImage()" style="margin-top:6px;">清除</button>' +
      '</div>' +
      '<button class="btn btn-primary btn-block" id="submitBtn" disabled onclick="PracticeV2.submitGrade()">提交批改</button>';

    if (window.MathJax) MathJax.typesetPromise();
  }

  async function handleFile(event) {
    var file = event.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(e) {
      $id('imagePreview').style.display = 'block';
      $id('previewImg').src = e.target.result;
    };
    reader.readAsDataURL(file);
    imageBase64 = await compressImage(file);
    $id('submitBtn').disabled = false;
  }

  function compressImage(file, maxDim, quality) {
    maxDim = maxDim || 1200; quality = quality || 0.8;
    return new Promise(function(resolve) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var img = new Image();
        img.onload = function() {
          var w = img.width, h = img.height;
          if (w > maxDim || h > maxDim) { var s = maxDim / Math.max(w, h); w = Math.round(w * s); h = Math.round(h * s); }
          var canvas = document.createElement('canvas');
          canvas.width = w; canvas.height = h;
          canvas.getContext('2d').drawImage(img, 0, 0, w, h);
          resolve(canvas.toDataURL('image/jpeg', quality).split(',')[1]);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  function clearImage() { imageBase64 = null; $id('imagePreview').style.display = 'none'; $id('submitBtn').disabled = true; $id('fileInput').value = ''; }

  async function submitGrade() {
    if (!imageBase64 || !currentProblem) return;
    var btn = $id('submitBtn'); btn.disabled = true; btn.textContent = '批改中...';
    var apiKey = ''; try { apiKey = localStorage.getItem('mathlearnlab:apikey') || ''; } catch(e) {}
    if (!apiKey) { alert('请先设置 API Key'); btn.disabled = false; btn.textContent = '提交批改'; return; }
    try {
      var resp = await fetch('/api/grade', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
        body: JSON.stringify({ topic_key: currentTopic, problem_id: currentProblem.id, image_base64: imageBase64 }),
      });
      if (!resp.ok) throw new Error((await resp.json()).detail || '批改失败');
      result = await resp.json();
      renderResults();
    } catch(e) { alert('批改失败: ' + e.message); btn.disabled = false; btn.textContent = '提交批改'; }
  }

  function renderResults() {
    $id('phaseSolve').style.display = 'none';
    $id('phaseResults').style.display = 'block';
    var r = result;
    var verdicts = { correct:'回答正确', partially_correct:'部分正确', incorrect:'回答有误' };
    var v = verdicts[r.verdict] || '未知';

    var html = '<div class="verdict-banner verdict-' + (r.verdict || 'incorrect') + '">' + v + '</div>';
    if (r.score) html += '<p style="text-align:center;color:var(--text-muted);">' + r.score + '</p>';
    if (r.ocr_text) html += '<div class="feedback-block"><h4>识别的作答</h4><pre style="white-space:pre-wrap;font-size:13px;">' + escapeHtml(r.ocr_text) + '</pre></div>';
    if (r.what_is_correct) html += '<div class="feedback-block" style="border-left:3px solid var(--accent-correct);"><h4>正确的部分</h4><p>' + escapeHtml(r.what_is_correct) + '</p></div>';
    if (r.what_is_wrong) html += '<div class="feedback-block" style="border-left:3px solid var(--accent-error);"><h4>存在的问题</h4><p>' + escapeHtml(r.what_is_wrong) + '</p></div>';
    if (r.suggestion) html += '<div class="feedback-block" style="border-left:3px solid var(--accent);"><h4>改进建议</h4><p>' + escapeHtml(r.suggestion) + '</p></div>';
    html += '<div style="display:flex;gap:8px;margin-top:16px;"><button class="btn btn-primary" onclick="PracticeV2.goToPhase(\'select\')">再做一题</button><button class="btn" onclick="PracticeV2.renderSolve()">重做此题</button></div>';
    $id('resultsContent').innerHTML = html;
    if (window.MathJax) MathJax.typesetPromise();
  }

  function goToPhase(p) {
    if (p === 'select') { currentProblem = null; imageBase64 = null; result = null; $id('phaseSelect').style.display = 'block'; $id('phaseSolve').style.display = 'none'; $id('phaseResults').style.display = 'none'; loadProblems(); }
  }

  function escapeHtml(s) { if (!s) return ''; var d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }

  function filterProblems() {
    var filter = ($id('diffFilter') || {}).value || 'all';
    document.querySelectorAll('#problemList .problem-list-item').forEach(function(el) {
      el.style.display = (filter === 'all' || el.dataset.difficulty === filter) ? '' : 'none';
    });
  }

  return { init:init, loadProblems:loadProblems, randomProblem:randomProblem, aiGenerate:aiGenerate, selectProblem:selectProblem, handleFile:handleFile, clearImage:clearImage, submitGrade:submitGrade, renderSolve:renderSolve, goToPhase:goToPhase, filterProblems:filterProblems };
})();
