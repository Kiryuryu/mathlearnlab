<template>
  <div class="practice-page">
    <div class="header">
      <router-link to="/gaoshu" class="back">← 展区</router-link>
      <h1>练习</h1>
      <div class="steps">
        <span :class="{ active: step === 'select', done: step !== 'select' }">选题</span>
        <span>—</span>
        <span :class="{ active: step === 'solve', done: step === 'results' }">作答</span>
        <span>—</span>
        <span :class="{ active: step === 'results' }">批改</span>
      </div>
      <div class="topic-select">
        <span>主题：</span>
        <select v-model="topic" @change="loadProblems">
          <option v-for="s in subtopics" :key="s.key" :value="s.key">{{ s.label }}</option>
        </select>
      </div>
    </div>

    <!-- Phase 1: Select -->
    <div v-if="step === 'select'">
      <div class="toolbar">
        <div class="filters">
          <button v-for="d in difficulties" :key="d.key" :class="{ active: filter === d.key }" @click="filter = d.key">{{ d.label }}</button>
        </div>
        <div class="actions">
          <button class="btn" @click="aiGenerate" :disabled="generating" :title="auth.isLoggedIn ? '' : '登录后使用'">
            <span v-if="generating" class="spin"></span>
            {{ generating ? '生成中...' : (auth.isLoggedIn ? 'AI 出题' : '🔒 AI 出题') }}
          </button>
          <button class="btn btn-primary" @click="randomProblem">随机抽题</button>
        </div>
      </div>
      <div class="problem-list">
        <div v-if="!problems.length" class="empty">暂无题目，点击「AI 出题」生成</div>
        <div v-for="p in filteredProblems" :key="p.id" class="problem-card" @click="selectProblem(p.id)">
          <span class="diff" :class="p.difficulty">{{ diffLabel(p.difficulty) }}</span>
          <div class="p-body"><span class="p-id">{{ p.id }}</span><span class="p-preview" v-html="renderMarkdown(p.preview)"></span></div>
          <span class="p-arrow">→</span>
        </div>
      </div>
    </div>

    <!-- Phase 2: Solve -->
    <div v-if="step === 'solve' && currentProblem" class="solve-area">
      <div class="problem-display">
        <div class="p-meta"><span :class="currentProblem.difficulty">{{ diffLabel(currentProblem.difficulty) }}</span></div>
        <div class="p-statement" v-html="renderedStatement"></div>
      </div>
      <div class="upload-zone" @click="$refs.fileInput.click()" v-if="!previewUrl">
        <div class="upload-icon">+</div>
        <p>点击拍照或上传作答图片</p>
        <input ref="fileInput" type="file" accept="image/*" @change="handleFile" hidden>
      </div>
      <div v-else class="preview">
        <img :src="previewUrl" class="preview-img">
        <button @click="previewUrl=null;imageBase64=null">重新上传</button>
      </div>
      <button class="submit-btn" :disabled="!imageBase64" @click="submitGrade">
        {{ auth.isLoggedIn ? '提交批改' : '🔒 登录后批改' }}
      </button>
      <button class="btn" @click="step='select';currentProblem=null">返回选题</button>
    </div>

    <!-- Phase 3: Results -->
    <div v-if="step === 'results' && result" class="results">
      <div :class="'verdict verdict-'+result.verdict">{{ result.verdict === 'correct' ? '✓ 正确' : result.verdict === 'partial' ? '≈ 部分正确' : '✗ 错误' }}</div>
      <div class="feedback">
        <div v-if="result.what_is_correct"><strong>做对的地方：</strong>{{ result.what_is_correct }}</div>
        <div v-if="result.what_is_wrong"><strong>需要改进：</strong>{{ result.what_is_wrong }}</div>
        <div v-if="result.suggestion"><strong>建议：</strong>{{ result.suggestion }}</div>
      </div>
      <div class="result-actions">
        <button class="btn btn-primary" @click="step='select';result=null">再做一题</button>
        <button class="btn" @click="step='solve'">重做此题</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { renderMarkdown } from '@/utils/markdown'
import { useAuth } from '@/stores/auth'
import { apiFetch } from '@/utils/api'

const auth = useAuth()

const topic = ref('limits')
const step = ref('select')
const filter = ref('all')
const problems = ref([])
const currentProblem = ref(null)
const previewUrl = ref(null)
const imageBase64 = ref(null)
const result = ref(null)
const generating = ref(false)

const renderedStatement = computed(() => renderMarkdown(currentProblem.value?.problem_statement || ''))

const subtopics = [
  { key: 'limits', label: '极限 — 无限逼近的艺术' },
  { key: 'derivatives', label: '导数 — 瞬间的变化率' },
  { key: 'integrals', label: '积分 — 和的极限' },
  { key: 'series', label: '无穷级数 — 无限的拼图' },
  { key: 'multivariable', label: '多元微积分 — 从平面到空间' },
]

const difficulties = [
  { key: 'all', label: '全部' },
  { key: 'basic', label: '基础' },
  { key: 'advanced', label: '进阶' },
  { key: 'exam', label: '考研' },
  { key: 'graduate', label: '研究生' },
  { key: 'phd', label: '博士' },
]

const labels = { basic:'基础', advanced:'进阶', exam:'考研', graduate:'研究生', phd:'博士' }
function diffLabel(d) { return labels[d] || d }

const filteredProblems = computed(() => {
  if (filter.value === 'all') return problems.value
  return problems.value.filter(p => p.difficulty === filter.value)
})

async function loadProblems() {
  try {
    const r = await fetch(`/api/practice/${topic.value}/problems`)
    problems.value = (await r.json()).problems || []
  } catch(e) {}
}
async function randomProblem() {
  try {
    const r = await fetch(`/api/practice/${topic.value}/problems/random`)
    currentProblem.value = (await r.json()).problem
    step.value = 'solve'
  } catch(e) {}
}
async function selectProblem(id) {
  try {
    const r = await fetch(`/api/practice/${topic.value}/problems/${id}`)
    currentProblem.value = (await r.json()).problem
    step.value = 'solve'
  } catch(e) {}
}
async function aiGenerate() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  generating.value = true
  try {
    const r = await apiFetch('/api/practice/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic_key: topic.value, difficulty: filter.value === 'all' ? 'exam' : filter.value })
    })
    if (r.status === 401) { auth.openLogin('login'); generating.value = false; return }
    currentProblem.value = (await r.json()).problem
    step.value = 'solve'
  } catch(e) { alert('生成失败: '+e.message) }
  generating.value = false
}

async function handleFile(e) {
  const file = e.target.files[0]
  if (!file) return
  previewUrl.value = URL.createObjectURL(file)
  const reader = new FileReader()
  reader.onload = ev => {
    const img = new Image()
    img.onload = () => {
      const c = document.createElement('canvas')
      const s = Math.min(img.width, img.height, 1200) / Math.max(img.width, img.height)
      c.width = Math.round(img.width * s); c.height = Math.round(img.height * s)
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height)
      imageBase64.value = c.toDataURL('image/jpeg', 0.8).split(',')[1]
    }
    img.src = ev.target.result
  }
  reader.readAsDataURL(file)
}

async function submitGrade() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  try {
    const r = await apiFetch('/api/grade', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic_key: topic.value, problem_id: currentProblem.value.id, image_base64: imageBase64.value })
    })
    if (r.status === 401) { auth.openLogin('login'); return }
    result.value = await r.json()
    step.value = 'results'
  } catch(e) { alert('批改失败: '+e.message) }
}

onMounted(loadProblems)
</script>

<style scoped>
.practice-page { max-width:780px; margin:0 auto; padding:32px 20px 64px; }
.header { text-align:center; margin-bottom:32px; }
.header h1 { font-size:24px; }
.back { font-size:13px; color:var(--text-muted); text-decoration:none; }
.steps { display:flex; align-items:center; justify-content:center; gap:8px; margin:8px 0; }
.steps span { font-size:13px; color:var(--text-muted); padding:4px 12px; border-radius:20px; }
.steps span.active { background:var(--accent); color:#fff; }
.steps span.done { color:var(--accent-correct); }
.topic-select { display:flex; align-items:center; justify-content:center; gap:8px; margin:8px 0; font-size:13px; color:var(--text-secondary); }
.topic-select select { background:var(--bg-input); color:var(--text-primary); border:1px solid var(--border); border-radius:4px; padding:3px 8px; }
.toolbar { display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px; }
.filters { display:flex; gap:4px; }
.filters button { padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-size:12px; cursor:pointer; background:var(--bg-card); color:var(--text-secondary); }
.filters button.active { background:var(--accent); color:#fff; border-color:var(--accent); }
.actions { display:flex; gap:8px; }
.btn { padding:7px 18px; border:1px solid var(--border); border-radius:4px; background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-size:14px; text-decoration:none; }
.btn-primary { border-color:var(--accent); color:var(--accent); }
.btn-primary:hover { background:var(--accent); color:#fff; }
.btn:disabled { opacity:0.4; }
.spin { display:inline-block; width:12px; height:12px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.6s linear infinite; margin-right:4px; vertical-align:middle; }
@keyframes spin { to { transform:rotate(360deg) } }
.problem-list { display:flex; flex-direction:column; gap:4px; }
.empty { text-align:center; padding:40px; color:var(--text-muted); }
.problem-card { display:flex; align-items:center; gap:12px; padding:14px 16px; border:1px solid var(--border); border-radius:8px; cursor:pointer; background:var(--bg-card); }
.problem-card:hover { border-color:var(--accent); }
.diff { font-size:12px; width:40px; text-align:center; }
.basic { color:var(--accent-correct); } .advanced { color:var(--accent); } .exam { color:var(--accent-warm); } .graduate, .phd { color:var(--accent-error); }
.p-body { flex:1; }
.p-id { font-size:12px; color:var(--text-muted); }
.p-preview { font-size:14px; display:block; color:var(--text-primary); }
.p-preview :deep(.katex) { font-size:1em; }
.p-arrow { font-size:18px; color:var(--text-muted); }
.solve-area { max-width:600px; margin:0 auto; }
.problem-display { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:24px; margin-bottom:16px; }
.p-statement { font-size:16px; line-height:1.8; color:var(--text-primary); }
.p-statement :deep(.katex-display) { margin:16px 0; overflow-x:auto; overflow-y:hidden; }
.upload-zone { border:2px dashed var(--border); border-radius:12px; padding:40px 20px; text-align:center; cursor:pointer; background:var(--bg-card); }
.upload-zone:hover { border-color:var(--accent); }
.upload-icon { font-size:32px; color:var(--text-muted); margin-bottom:8px; }
.preview { text-align:center; margin:16px 0; }
.preview-img { max-width:100%; max-height:300px; border-radius:8px; border:1px solid var(--border); }
.submit-btn { width:100%; padding:14px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; margin-top:12px; }
.submit-btn:disabled { opacity:0.4; }
.results { max-width:600px; margin:0 auto; }
.verdict { padding:14px 22px; border-radius:8px; text-align:center; font-size:19px; font-weight:700; margin:12px 0; }
.verdict-correct { background:#eaf4ee; color:var(--accent-correct); } .verdict-partial { background:#faf3e8; color:var(--accent-warm); } .verdict-incorrect { background:#f9eaea; color:var(--accent-error); }
[data-theme="dark"] .verdict-correct { background:#1a2e20; color:#8cc9a0; } [data-theme="dark"] .verdict-partial { background:#2e2418; color:#d4b87a; } [data-theme="dark"] .verdict-incorrect { background:#2e1a1a; color:#d49a9a; }
.feedback { background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:8px 0; line-height:1.8; color:var(--text-primary); }
.result-actions { display:flex; gap:8px; margin-top:16px; }
</style>
