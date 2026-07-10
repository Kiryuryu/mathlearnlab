// OCR Practice — three-phase state machine

const Practice = {
  topic: '',
  problem: null,
  imageBase64: null,
  result: null,

  init(topic) {
    this.topic = topic;
  },

  async randomProblem() {
    try {
      const resp = await fetch(`/api/practice/${this.topic}/problems/random`);
      if (!resp.ok) throw new Error('No problems');
      const data = await resp.json();
      this.problem = data.problem;
      this.imageBase64 = null;
      this.result = null;
      this.showSolve();
    } catch (e) {
      alert('获取题目失败: ' + e.message);
    }
  },

  async selectProblem(id) {
    try {
      const resp = await fetch(`/api/practice/${this.topic}/problems/${id}`);
      if (!resp.ok) throw new Error('Not found');
      const data = await resp.json();
      this.problem = data.problem;
      this.imageBase64 = null;
      this.result = null;
      this.showSolve();
    } catch (e) {
      alert('获取题目失败: ' + e.message);
    }
  },

  showSolve() {
    if (!this.problem) return;
    const p = this.problem;
    const diff = window.PRACTICE_SETTINGS?.difficulty || {};
    const d = diff[p.difficulty] || {};

    document.getElementById('phaseSelect').style.display = 'none';
    document.getElementById('phaseResults').style.display = 'none';
    document.getElementById('phaseSolve').style.display = 'block';

    document.getElementById('solveContent').innerHTML = `
      <div class="problem-card">
        <div class="problem-meta">
          <span>${d.stars || ''} ${d.zh || ''}</span>
          <span>${(p.knowledge_points || []).slice(0,3).join(' · ')}</span>
          <span>${(p.metadata || {}).problem_type || '计算题'}</span>
        </div>
        <h3>${p.id}</h3>
        <div>${p.problem_statement || ''}</div>
      </div>

      <div class="upload-area" onclick="document.getElementById('fileInput').click()">
        <p>点击拍照或上传图片</p>
        <p style="font-size:12px;color:var(--text-muted);">JPG / PNG</p>
        <input type="file" id="fileInput" accept="image/*" capture="environment"
               onchange="Practice.handleFile(event)" style="display:none;">
      </div>

      <div id="imagePreview" style="display:none;margin:12px 0;">
        <img id="previewImg" style="max-width:100%;max-height:300px;border-radius:var(--radius);border:1px solid var(--border);">
        <button class="btn btn-sm" onclick="Practice.clearImage()" style="margin-top:6px;">清除</button>
      </div>

      <button class="btn btn-primary btn-block" id="submitBtn" disabled
              onclick="Practice.submitGrade()">提交批改</button>
    `;

    if (window.MathJax) MathJax.typesetPromise();
  },

  async handleFile(event) {
    const file = event.target.files?.[0];
    if (!file || !file.type.startsWith('image/')) return;

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
      document.getElementById('imagePreview').style.display = 'block';
      document.getElementById('previewImg').src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Compress via canvas
    this.imageBase64 = await this.compressImage(file);
    document.getElementById('submitBtn').disabled = false;

    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) uploadArea.style.borderColor = 'var(--accent-correct)';
  },

  compressImage(file, maxDim = 1200, quality = 0.8) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          let w = img.width, h = img.height;
          if (w > maxDim || h > maxDim) {
            const s = maxDim / Math.max(w, h);
            w = Math.round(w * s); h = Math.round(h * s);
          }
          const canvas = document.createElement('canvas');
          canvas.width = w; canvas.height = h;
          canvas.getContext('2d').drawImage(img, 0, 0, w, h);
          resolve(canvas.toDataURL('image/jpeg', quality).split(',')[1]);
        };
        img.onerror = reject;
        img.src = e.target.result;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  },

  clearImage() {
    this.imageBase64 = null;
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('fileInput').value = '';
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) uploadArea.style.borderColor = '';
  },

  async submitGrade() {
    if (!this.imageBase64 || !this.problem) return;
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.textContent = '批改中...';

    const apiKey = (() => {
      try { return localStorage.getItem('mathlearnlab:apikey') || ''; } catch { return ''; }
    })();
    if (!apiKey) { alert('请先设置 API Key'); btn.disabled = false; btn.textContent = '提交批改'; return; }

    try {
      const resp = await fetch('/api/grade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
        body: JSON.stringify({
          topic_key: this.topic,
          problem_id: this.problem.id,
          image_base64: this.imageBase64,
        }),
      });
      if (!resp.ok) throw new Error((await resp.json()).detail || 'Grading failed');
      this.result = await resp.json();
      this.showResults();
    } catch (e) {
      alert('批改失败: ' + e.message);
      btn.disabled = false;
      btn.textContent = '提交批改';
    }
  },

  showResults() {
    const r = this.result;
    const verdicts = {
      correct: { text: '回答正确', cls: 'verdict-correct' },
      partially_correct: { text: '部分正确', cls: 'verdict-partial' },
      incorrect: { text: '回答有误', cls: 'verdict-incorrect' },
    };
    const v = verdicts[r.verdict] || verdicts.incorrect;

    document.getElementById('phaseSolve').style.display = 'none';
    document.getElementById('phaseResults').style.display = 'block';

    let html = `
      <div class="verdict-banner ${v.cls}">${v.text}</div>
      <p style="text-align:center;color:var(--text-muted);">${r.score || ''}</p>
    `;

    if (r.ocr_text) {
      html += `<div class="feedback-block">
        <h4>识别的作答</h4>
        <pre style="white-space:pre-wrap;font-size:13px;">${this.escape(r.ocr_text)}</pre>
      </div>`;
    }
    if (r.what_is_correct) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--accent-correct);">
        <h4>正确的部分</h4><p>${this.escape(r.what_is_correct)}</p></div>`;
    }
    if (r.what_is_wrong) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--accent-error);">
        <h4>存在的问题</h4><p>${this.escape(r.what_is_wrong)}</p></div>`;
    }
    if (r.key_misconception) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--accent-warm);">
        <h4>概念误解</h4><p>${this.escape(r.key_misconception)}</p></div>`;
    }
    if (r.suggestion) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--accent);">
        <h4>改进建议</h4><p>${this.escape(r.suggestion)}</p></div>`;
    }

    const steps = r.graded_steps || [];
    if (steps.length > 0) {
      html += '<div class="feedback-block"><h4>步骤详情</h4>';
      steps.forEach(s => {
        const icon = { ok: '✓', wrong: '✗', missing: '—' }[s.status] || '?';
        html += `<div class="graded-step"><span class="step-status">${icon}</span>
          <div><strong>${this.escape(s.step||'')}</strong>
          <div style="font-size:12px;color:var(--text-secondary);">${this.escape(s.comment||'')}</div></div></div>`;
      });
      html += '</div>';
    }

    // Solution
    const sol = this.problem?.solution || {};
    html += `<details class="feedback-block">
      <summary><strong>标准解答</strong></summary>
      <p>${this.escape(sol.method||'')}</p>`;
    if (sol.steps) sol.steps.forEach((s,i) => { html += `<p>${i+1}. ${this.escape(s)}</p>`; });
    if (sol.final_answer) html += `<p><strong>答案：</strong>${this.escape(sol.final_answer)}</p>`;
    html += `</details>`;

    html += `<div style="display:flex;gap:8px;margin-top:16px;">
      <button class="btn btn-primary" onclick="Practice.goToPhase('select')">再做一题</button>
      <button class="btn" onclick="Practice.showSolve()">重做此题</button>
    </div>`;

    document.getElementById('resultsContent').innerHTML = html;
    if (window.MathJax) MathJax.typesetPromise();
  },

  goToPhase(phase) {
    if (phase === 'select') {
      this.problem = null; this.imageBase64 = null; this.result = null;
      document.getElementById('phaseSelect').style.display = 'block';
      document.getElementById('phaseSolve').style.display = 'none';
      document.getElementById('phaseResults').style.display = 'none';
    }
  },

  filterProblems() {
    const filter = document.getElementById('diffFilter')?.value || 'all';
    document.querySelectorAll('#problemList .problem-list-item').forEach(el => {
      el.style.display = (filter === 'all' || el.dataset.difficulty === filter) ? '' : 'none';
    });
  },

  escape(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = String(str);
    return div.innerHTML;
  },
};

// Init on page load
document.addEventListener('DOMContentLoaded', () => {
  if (window.PRACTICE_TOPIC) Practice.init(window.PRACTICE_TOPIC);
});
