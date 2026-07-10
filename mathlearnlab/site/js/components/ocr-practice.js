// OCR Practice component — three-phase state machine
// Phase 1: Select topic + problem
// Phase 2: View problem + upload photo
// Phase 3: View grading results

const OCRPractice = {
  // State per topic session
  state: {
    topicKey: null,
    phase: 'select',   // select | solve | results
    problem: null,
    imageDataUrl: null,
    imageBase64: null,
    result: null,
    problemBank: [],
  },

  async render(container, topicKey) {
    this.state.topicKey = topicKey;
    const topic = CONFIG.TOPICS[topicKey] || { zh: topicKey, icon: '📝' };

    // Load problem bank
    try {
      const resp = await fetch(`practice/problem_bank/${topic.json}`);
      const data = await resp.json();
      this.state.problemBank = data.problems || [];
    } catch (e) {
      this.state.problemBank = [];
    }

    if (this.state.phase === 'select' || !this.state.problem) {
      this.renderSelectPhase(container, topic);
    } else if (this.state.phase === 'solve') {
      this.renderSolvePhase(container, topic);
    } else if (this.state.phase === 'results') {
      this.renderResultsPhase(container, topic);
    }
  },

  // === Phase 1: Select Problem ===
  renderSelectPhase(container, topic) {
    const problems = this.state.problemBank;
    const stats = Storage.getGradeStats();

    let html = `<div class="practice-phase">
      <h2>${topic.icon} ${topic.zh} — OCR 刷题</h2>
      <p>选题 → 纸笔作答 → 拍照上传 → AI 批改 → 错题自动记录</p>

      <button class="btn btn-primary" onclick="OCRPractice.randomProblem()" style="margin:12px 0;">🎲 随机抽题</button>
    `;

    // Difficulty filter
    html += `<div style="margin:8px 0;">
      <label>筛选难度：</label>
      <select id="practiceDiffFilter" onchange="OCRPractice.filterProblems()">
        <option value="all">全部</option>
        <option value="easy">简单</option>
        <option value="medium">中等</option>
        <option value="hard">困难</option>
      </select>
      <span style="margin-left:16px;color:var(--text-muted);">共 ${problems.length} 道题</span>
    </div>`;

    html += '<div id="problemList">';
    problems.forEach(p => {
      const d = CONFIG.DIFFICULTY[p.difficulty] || {};
      const tags = (p.knowledge_points || []).slice(0, 3).join(' · ');
      const preview = (p.problem_statement || '').substring(0, 100).replace(/\$/g, '') + '...';
      html += `<div class="problem-list-item" onclick="OCRPractice.selectProblem('${p.id}')">
        <div>
          <strong>${d.stars || ''} ${p.id}</strong> — ${escapeHtml(preview)}
          <div style="font-size:12px;color:var(--text-muted);">${escapeHtml(tags)} · ${d.zh || ''}</div>
        </div>
        <span style="font-size:20px;">➤</span>
      </div>`;
    });
    html += '</div>';

    if (problems.length === 0) {
      html += '<p style="color:var(--text-muted);margin-top:16px;">📭 该 topic 暂无题目。请运行 <code>scripts/seed_problem_bank.py</code> 生成。</p>';
    }

    html += '</div>';
    container.innerHTML = html;
  },

  randomProblem() {
    const problems = this.state.problemBank;
    if (problems.length === 0) return;
    const idx = Math.floor(Math.random() * problems.length);
    this.selectProblem(problems[idx].id);
  },

  selectProblem(id) {
    const problem = this.state.problemBank.find(p => p.id === id);
    if (!problem) return;
    this.state.problem = problem;
    this.state.phase = 'solve';
    this.state.imageDataUrl = null;
    this.state.imageBase64 = null;
    this.state.result = null;
    this.refresh();
  },

  filterProblems() {
    const filter = document.getElementById('practiceDiffFilter')?.value || 'all';
    const container = document.getElementById('problemList');
    if (!container) return;

    const items = container.querySelectorAll('.problem-list-item');
    this.state.problemBank.forEach((p, i) => {
      if (items[i]) {
        items[i].style.display = (filter === 'all' || p.difficulty === filter) ? '' : 'none';
      }
    });
  },

  // === Phase 2: View Problem + Upload ===
  renderSolvePhase(container, topic) {
    const problem = this.state.problem;
    const d = CONFIG.DIFFICULTY[problem.difficulty] || {};
    const tags = (problem.knowledge_points || []).join(' · ');

    let html = `<div class="practice-phase">
      <button class="btn btn-secondary btn-sm" onclick="OCRPractice.goBack()">← 返回选题</button>

      <div class="problem-card">
        <div class="problem-meta">
          <span>${d.stars} ${d.zh}</span>
          <span>📌 ${escapeHtml(tags)}</span>
          <span>📝 ${problem.metadata?.problem_type || '计算题'}</span>
        </div>
        <h3>📝 ${problem.id}</h3>
        <div class="problem-statement">${problem.problem_statement || ''}</div>
      </div>

      <h3>📸 上传你的手写答案</h3>
      <div class="upload-area" id="uploadArea" onclick="document.getElementById('fileInput').click()">
        <p style="font-size:40px;">📷</p>
        <p>点击拍照或上传图片</p>
        <p style="font-size:12px;color:var(--text-muted);">支持 JPG、PNG 格式</p>
        <input type="file" id="fileInput" accept="image/*" capture="environment"
               onchange="OCRPractice.handleFileSelect(event)" style="display:none;">
      </div>

      <div id="imagePreview" style="margin:12px 0;display:none;">
        <img id="previewImg" style="max-width:100%;max-height:300px;border-radius:var(--radius);border:1px solid var(--border-color);">
        <button class="btn btn-secondary btn-sm" onclick="OCRPractice.clearImage()" style="margin-top:8px;">🗑 清除</button>
      </div>

      <button class="btn btn-primary btn-block" id="submitGradeBtn"
              onclick="OCRPractice.submitForGrading()" disabled>
        🎯 提交批改
      </button>
    </div>`;

    container.innerHTML = html;

    // Restore image if already selected
    if (this.state.imageDataUrl) {
      this.showImagePreview(this.state.imageDataUrl);
      const submitBtn = document.getElementById('submitGradeBtn');
      if (submitBtn) submitBtn.disabled = false;
    }

    // Typeset math
    typesetMath(container);
  },

  async handleFileSelect(event) {
    const file = event.target.files?.[0];
    if (!file || !ImageUtils.isImage(file)) return;

    try {
      // Show preview
      const dataUrl = await ImageUtils.readAsDataUrl(file);
      this.showImagePreview(dataUrl);
      this.state.imageDataUrl = dataUrl;

      // Compress and encode
      const compressed = await ImageUtils.compress(file);
      this.state.imageBase64 = compressed.base64;

      const submitBtn = document.getElementById('submitGradeBtn');
      if (submitBtn) submitBtn.disabled = false;
    } catch (e) {
      alert('图片处理失败: ' + e.message);
    }
  },

  showImagePreview(dataUrl) {
    const preview = document.getElementById('imagePreview');
    const img = document.getElementById('previewImg');
    if (preview && img) {
      preview.style.display = 'block';
      img.src = dataUrl;
    }
    // Update upload area style
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) uploadArea.style.borderColor = 'var(--success)';
  },

  clearImage() {
    this.state.imageDataUrl = null;
    this.state.imageBase64 = null;
    const preview = document.getElementById('imagePreview');
    if (preview) preview.style.display = 'none';
    const submitBtn = document.getElementById('submitGradeBtn');
    if (submitBtn) submitBtn.disabled = true;
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) uploadArea.style.borderColor = '';
    const fileInput = document.getElementById('fileInput');
    if (fileInput) fileInput.value = '';
  },

  async submitForGrading() {
    if (!this.state.imageBase64 || !this.state.problem) return;

    const submitBtn = document.getElementById('submitGradeBtn');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = '⏳ 正在批改... (预计 3-5 秒)';
    }

    try {
      const result = await API.gradeSubmission(this.state.problem, this.state.imageBase64);
      this.state.result = result;
      this.state.phase = 'results';

      // Save to history
      Storage.addGradeRecord({
        topicKey: this.state.topicKey,
        problemId: this.state.problem.id,
        verdict: result.verdict || 'unknown',
        score: result.score || '',
        ocrText: result.ocr_text || '',
        whatIsCorrect: result.what_is_correct || '',
        whatIsWrong: result.what_is_wrong || '',
      });

      this.refresh();
    } catch (e) {
      alert('批改失败: ' + e.message);
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🎯 提交批改';
      }
    }
  },

  // === Phase 3: Results ===
  renderResultsPhase(container, topic) {
    const problem = this.state.problem;
    const result = this.state.result;

    const verdictConfig = {
      correct: { text: '✅ 回答正确！', cls: 'verdict-correct' },
      partially_correct: { text: '⚠️ 部分正确', cls: 'verdict-partial' },
      incorrect: { text: '❌ 回答错误', cls: 'verdict-incorrect' },
    };
    const vConfig = verdictConfig[result.verdict] || { text: '❓ 无法判定', cls: 'verdict-partial' };

    let html = `<div class="practice-phase">
      <div class="verdict-banner ${vConfig.cls}">${vConfig.text}</div>
      <p style="text-align:center;color:var(--text-muted);">得分：${result.score || ''}</p>
    `;

    // OCR text
    if (result.ocr_text) {
      html += `<div class="feedback-block">
        <h4>📖 识别到的作答内容</h4>
        <pre style="white-space:pre-wrap;font-size:14px;">${escapeHtml(result.ocr_text)}</pre>
      </div>`;
    }

    // What's correct
    if (result.what_is_correct) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--success);">
        <h4>✅ 做得好的地方</h4>
        <p>${escapeHtml(result.what_is_correct)}</p>
      </div>`;
    }

    // What's wrong
    if (result.what_is_wrong) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--danger);">
        <h4>❌ 存在问题</h4>
        <p>${escapeHtml(result.what_is_wrong)}</p>
      </div>`;
    }

    // Misconception
    if (result.key_misconception) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--warning);">
        <h4>🔍 可能的概念误解</h4>
        <p>${escapeHtml(result.key_misconception)}</p>
      </div>`;
    }

    // Suggestion
    if (result.suggestion) {
      html += `<div class="feedback-block" style="border-left:3px solid var(--accent);">
        <h4>💡 改进建议</h4>
        <p>${escapeHtml(result.suggestion)}</p>
      </div>`;
    }

    // Graded steps
    const steps = result.graded_steps || [];
    if (steps.length > 0) {
      html += '<div class="feedback-block"><h4>📋 步骤批改详情</h4>';
      steps.forEach(gs => {
        const icon = { ok: '✅', wrong: '❌', missing: '⬜' }[gs.status] || '❓';
        html += `<div class="graded-step">
          <span class="step-status">${icon}</span>
          <div>
            <strong>${escapeHtml(gs.step || '')}</strong>
            <div style="font-size:13px;color:var(--text-secondary);">${escapeHtml(gs.comment || '')}</div>
          </div>
        </div>`;
      });
      html += '</div>';
    }

    // Correct solution
    const solution = problem.solution || {};
    html += `<details class="feedback-block">
      <summary><strong>📐 查看标准解答</strong></summary>
      <p><strong>方法：</strong>${escapeHtml(solution.method || '')}</p>
      <ol>`;
    (solution.steps || []).forEach(s => {
      html += `<li>${escapeHtml(s)}</li>`;
    });
    html += `</ol>`;
    if (solution.final_answer) {
      html += `<p><strong>最终答案：</strong>${escapeHtml(solution.final_answer)}</p>`;
    }
    html += '</details>';

    // Action buttons
    html += `<div style="display:flex;gap:8px;margin-top:16px;">
      <button class="btn btn-primary" onclick="OCRPractice.nextProblem()">🔄 再做一题</button>
      <button class="btn btn-secondary" onclick="OCRPractice.retryProblem()">🔁 重做此题</button>
      <button class="btn btn-secondary" onclick="OCRPractice.goToSelect()">📋 返回选题</button>
    </div>`;

    html += '</div>';
    container.innerHTML = html;

    // Auto-save to error log if incorrect
    if (result.verdict === 'incorrect' || result.verdict === 'partially_correct') {
      this.saveToErrorLog(problem, result);
    }
  },

  // === Navigation helpers ===
  goBack() { this.state.phase = 'select'; this.refresh(); },
  goToSelect() { this.state.phase = 'select'; this.state.problem = null; this.refresh(); },
  nextProblem() { this.state.phase = 'select'; this.state.problem = null; this.refresh(); },
  retryProblem() { this.state.phase = 'solve'; this.state.imageDataUrl = null; this.state.imageBase64 = null; this.state.result = null; this.refresh(); },

  refresh() {
    const container = document.getElementById('mainContent');
    const topic = CONFIG.TOPICS[this.state.topicKey] || { zh: this.state.topicKey, icon: '📝' };
    if (this.state.phase === 'select' || !this.state.problem) {
      this.renderSelectPhase(container, topic);
    } else if (this.state.phase === 'solve') {
      this.renderSolvePhase(container, topic);
    } else {
      this.renderResultsPhase(container, topic);
    }
  },

  // Save to error log (appends to localStorage + can be viewed in error-log page)
  saveToErrorLog(problem, result) {
    const errors = Storage.get('errorLog', []);
    // Avoid duplicates
    if (errors.some(e => e.problemId === problem.id && e.timestamp && Date.now() - new Date(e.timestamp).getTime() < 60000)) return;

    errors.push({
      problemId: problem.id,
      topicKey: this.state.topicKey,
      problemStatement: problem.problem_statement,
      solutionSteps: problem.solution?.steps || [],
      finalAnswer: problem.solution?.final_answer || '',
      whatIsWrong: result.what_is_wrong || '',
      suggestion: result.suggestion || '',
      misconception: result.key_misconception || '',
      timestamp: new Date().toISOString(),
    });

    // Keep last 100 errors
    if (errors.length > 100) errors.splice(0, errors.length - 100);
    Storage.set('errorLog', errors);
  },
};
