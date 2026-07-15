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
          <button class="btn" @click="aiGenerate" :disabled="generating">
            <span v-if="generating" class="spin"></span>
            {{ generating ? '生成中...' : 'AI 出题' }}
          </button>
          <button class="btn btn-primary" @click="randomProblem">随机抽题</button>
        </div>
      </div>
      <div class="problem-list">
        <div v-if="!problems.length" class="empty">暂无题目，点击「AI 出题」生成</div>
        <div v-for="p in filteredProblems" :key="p.id" class="problem-card" @click="selectProblem(p.id)">
          <span class="diff" :class="p.difficulty">{{ diffLabel(p.difficulty) }}</span>
          <div class="p-body"><span class="p-id">{{ p.id }}</span><span class="p-preview">{{ p.preview }}</span></div>
          <span class="p-arrow">→</span>
        </div>
      </div>
    </div>

    <!-- Phase 2: Solve -->
    <div v-if="step === 'solve' && currentProblem" class="solve-area">
      <div class="problem-display">
        <div class="p-meta"><span :class="currentProblem.difficulty">{{ diffLabel(currentProblem.difficulty) }}</span></div>
        <div class="p-statement" v-html="currentProblem.problem_statement"></div>
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
      <button class="submit-btn" :disabled="!imageBase64" @click="submitGrade">提交批改</button>
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

const topic = ref('limits')
const step = ref('select')
const filter = ref('all')
const problems = ref([])
const currentProblem = ref(null)
const previewUrl = ref(null)
const imageBase64 = ref(null)
const result = ref(null)
const generating = ref(false)

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
  generating.value = true
  try {
    const key = localStorage.getItem('mathlearnlab:apikey') || ''
    const r = await fetch('/api/practice/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-API-Key': key },
      body: JSON.stringify({ topic_key: topic.value, difficulty: filter.value === 'all' ? 'exam' : filter.value })
    })
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
  const key = localStorage.getItem('mathlearnlab:apikey') || ''
  try {
    const r = await fetch('/api/grade', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-API-Key': key },
      body: JSON.stringify({ topic_key: topic.value, problem_id: currentProblem.value.id, image_base64: imageBase64.value })
    })
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
.back { font-size:13px; color:#889098; text-decoration:none; }
.steps { display:flex; align-items:center; justify-content:center; gap:8px; margin:8px 0; }
.steps span { font-size:13px; color:#889098; padding:4px 12px; border-radius:20px; }
.steps span.active { background:#4a6a8a; color:#fff; }
.steps span.done { color:#3d6b4f; }
.topic-select { display:flex; align-items:center; justify-content:center; gap:8px; margin:8px 0; font-size:13px; }
.toolbar { display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px; }
.filters { display:flex; gap:4px; }
.filters button { padding:5px 14px; border:1px solid #e2e5e8; border-radius:20px; font-size:12px; cursor:pointer; background:#fff; color:#505560; }
.filters button.active { background:#4a6a8a; color:#fff; }
.actions { display:flex; gap:8px; }
.btn { padding:7px 18px; border:1px solid #e2e5e8; border-radius:4px; background:#fff; color:#505560; cursor:pointer; font-size:14px; text-decoration:none; }
.btn-primary { border-color:#4a6a8a; color:#4a6a8a; }
.btn-primary:hover { background:#4a6a8a; color:#fff; }
.btn:disabled { opacity:0.4; }
.spin { display:inline-block; width:12px; height:12px; border:2px solid #e2e5e8; border-top-color:#4a6a8a; border-radius:50%; animation:spin 0.6s linear infinite; margin-right:4px; vertical-align:middle; }
@keyframes spin { to { transform:rotate(360deg) } }
.problem-list { display:flex; flex-direction:column; gap:4px; }
.empty { text-align:center; padding:40px; color:#889098; }
.problem-card { display:flex; align-items:center; gap:12px; padding:14px 16px; border:1px solid #e2e5e8; border-radius:8px; cursor:pointer; background:#fff; }
.problem-card:hover { border-color:#4a6a8a; }
.diff { font-size:12px; width:40px; text-align:center; }
.basic { color:#3d6b4f; } .advanced { color:#4a6a8a; } .exam { color:#6b5e4a; } .graduate, .phd { color:#a45050; }
.p-body { flex:1; }
.p-id { font-size:12px; color:#889098; }
.p-preview { font-size:14px; display:block; }
.p-arrow { font-size:18px; color:#889098; }
.solve-area { max-width:600px; margin:0 auto; }
.problem-display { background:#fff; border:1px solid #e2e5e8; border-radius:10px; padding:24px; margin-bottom:16px; }
.p-statement { font-size:16px; line-height:1.8; }
.upload-zone { border:2px dashed #e2e5e8; border-radius:12px; padding:40px 20px; text-align:center; cursor:pointer; }
.upload-icon { font-size:32px; color:#889098; margin-bottom:8px; }
.preview { text-align:center; margin:16px 0; }
.preview-img { max-width:100%; max-height:300px; border-radius:8px; border:1px solid #e2e5e8; }
.submit-btn { width:100%; padding:14px; background:#4a6a8a; color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; margin-top:12px; }
.submit-btn:disabled { opacity:0.4; }
.results { max-width:600px; margin:0 auto; }
.verdict { padding:14px 22px; border-radius:8px; text-align:center; font-size:19px; font-weight:700; margin:12px 0; }
.verdict-correct { background:#eaf4ee; color:#3d6b4f; } .verdict-partial { background:#faf3e8; color:#6b5e4a; } .verdict-incorrect { background:#f9eaea; color:#a45050; }
.feedback { background:#fff; border:1px solid #e2e5e8; border-radius:8px; padding:14px 18px; margin:8px 0; line-height:1.8; }
.result-actions { display:flex; gap:8px; margin-top:16px; }
</style>
