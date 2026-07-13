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
    var diff = $id('diffFilter') ? $id('diffFilter').value : 'exam';
    
    $id('practiceStatus').textContent = '正在生成题目...';
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

  function setStep(phase) {
    document.querySelectorAll('.practice-step').forEach(function(s) {
      s.classList.toggle('active', s.dataset.phase === phase);
      if (s.dataset.phase === phase) s.classList.add('done');
    });
  }

  function renderProblemList(problems) {
    var list = $id('problemList');
    if (!list) return;
    if (!problems.length) { list.innerHTML = '<div class="practice-empty">暂无题目，点击「生成新题」让 AI 出一道</div>'; return; }
    var labels = {'basic':'基础','advanced':'进阶','exam':'考研','graduate':'研究生','phd':'博士'};
    list.innerHTML = problems.map(function(p) {
      var d = p.difficulty || '';
      return '<div class="practice-problem-card" onclick="PracticeV2.selectProblem(\'' + p.id + '\')" data-difficulty="' + d + '">' +
        '<span class="ppc-difficulty ppc-' + d + '">' + (labels[d] || '') + '</span>' +
        '<div class="ppc-body">' +
          '<span class="ppc-id">' + (p.id || '') + '</span>' +
          '<span class="ppc-preview">' + (p.preview || '') + '</span>' +
        '</div>' +
        '<span class="ppc-arrow">→</span>' +
      '</div>';
    }).join('');
    $id('problemCount') && ($id('problemCount').textContent = problems.length + ' 题');
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
    setStep('solve');

    var p = currentProblem;
    $id('solveContent').innerHTML =
      '<div class="practice-solve-card">' +
        '<div class="psc-meta">' +
          '<span class="ppc-difficulty ppc-' + (p.difficulty||'') + '">' + (p.difficulty||'') + '</span>' +
          '<span style="font-size:12px;color:var(--text-muted);">' + ((p.knowledge_points||[]).slice(0,3).join(' · ')) + '</span>' +
        '</div>' +
        '<div class="psc-problem">' + (p.problem_statement || '') + '</div>' +
      '</div>' +
      '<div class="practice-upload" onclick="document.getElementById(\'fileInput\').click()" id="uploadZone">' +
        '<div class="practice-upload-icon">+</div>' +
        '<p>点击拍照或上传作答图片</p>' +
        '<p style="font-size:11px;color:var(--text-muted);">支持 JPG / PNG，可直接拍照上传</p>' +
        '<input type="file" id="fileInput" accept="image/*" capture="environment" onchange="PracticeV2.handleFile(event)" style="display:none;">' +
      '</div>' +
      '<div id="imagePreview" style="display:none;text-align:center;margin:16px 0;">' +
        '<img id="previewImg" style="max-width:100%;max-height:300px;border-radius:8px;border:1px solid var(--border);">' +
        '<br><button class="btn btn-sm" onclick="PracticeV2.clearImage()" style="margin-top:8px;">重新上传</button>' +
      '</div>' +
      '<button class="btn btn-primary" id="submitBtn" disabled onclick="PracticeV2.submitGrade()" style="width:100%;padding:14px;font-size:15px;margin-top:12px;">提交批改</button>' +
      '<button class="btn" onclick="PracticeV2.goToPhase(\'select\')" style="width:100%;margin-top:8px;">返回选题</button>';

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
    setStep(p);
  }

  function escapeHtml(s) { if (!s) return ''; var d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }

  function filterProblems() {
    var filter = ($id('diffFilter') || {}).value || 'all';
    document.querySelectorAll('#problemList .practice-problem-card').forEach(function(el) {
      el.style.display = (filter === 'all' || el.dataset.difficulty === filter) ? '' : 'none';
    });
  }

  return { init:init, loadProblems:loadProblems, randomProblem:randomProblem, aiGenerate:aiGenerate, selectProblem:selectProblem, handleFile:handleFile, clearImage:clearImage, submitGrade:submitGrade, renderSolve:renderSolve, goToPhase:goToPhase, filterProblems:filterProblems };
})();
