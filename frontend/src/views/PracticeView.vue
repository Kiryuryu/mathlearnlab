<template>
  <div class="practice-page">
    <div class="header">
      <router-link to="/gaoshu" class="back">← {{ $t('practice.backToExhibit') }}</router-link>
      <h1>{{ $t('practice.title') }}</h1>
      <div class="steps">
        <span :class="{ active: step === 'select', done: step !== 'select' }">{{ $t('practice.select') }}</span>
        <span>—</span>
        <span :class="{ active: step === 'solve', done: step === 'results' }">{{ $t('practice.solve') }}</span>
        <span>—</span>
        <span :class="{ active: step === 'results' }">{{ $t('practice.grade') }}</span>
      </div>
    </div>

    <!-- Phase 1: Select -->
    <div v-if="step === 'select'">
      <div class="select-area">
        <div class="topic-select">
          <label>{{ $t('practice.topic') }}</label>
          <select v-model="topic">
            <option v-for="s in displaySubtopics" :key="s.key" :value="s.key">{{ s.label }}</option>
          </select>
        </div>
        <div class="difficulty-select">
          <label>{{ $t('practice.difficulty') }}</label>
          <div class="filters">
            <button v-for="d in displayDifficulties" :key="d.key" :class="{ active: filter === d.key }" @click="filter = d.key">{{ d.label }}</button>
          </div>
        </div>
        <button class="btn btn-primary btn-lg" @click="aiGenerate" :disabled="generating">
          <span v-if="generating" class="spin"></span>
          {{ generating ? $t('practice.generating') : (auth.isLoggedIn ? $t('practice.aiGenerate') : '🔒 '+$t('practice.loginToUse')) }}
        </button>
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
        <p>{{ $t('practice.uploadHint') }}</p>
        <input ref="fileInput" type="file" accept="image/*" @change="handleFile" hidden>
      </div>
      <div v-else class="preview">
        <img :src="previewUrl" class="preview-img">
        <button @click="previewUrl=null;imageBase64=null">{{ $t('practice.reupload') }}</button>
      </div>
      <button class="submit-btn" :disabled="!imageBase64" @click="submitGrade">
        {{ auth.isLoggedIn ? $t('practice.submitForGrade') : '🔒 '+$t('practice.loginToUse') }}
      </button>
      <div v-if="gradingProgress > 0" class="grading-progress">
        <div class="progress-bar" :style="{ width: gradingProgress + '%' }"></div>
        <span class="progress-text">{{ gradingMessages[Math.floor(gradingProgress / 25)] || '处理中...' }}</span>
      </div>
      <button class="btn" @click="step='select';currentProblem=null">{{ $t('practice.backToSelect') }}</button>
    </div>

    <!-- Phase 3: Results -->
    <div v-if="step === 'results' && result" class="results">
      <div :class="'verdict verdict-'+result.verdict">{{ result.verdict === 'correct' ? '✓ '+$t('practice.correct') : result.verdict === 'partial' ? '≈ '+$t('practice.partial') : '✗ '+$t('practice.incorrect') }}</div>
      <div class="feedback">
        <div v-if="result.what_is_correct"><strong>{{ $t('practice.whatIsCorrect') }}</strong>{{ result.what_is_correct }}</div>
        <div v-if="result.what_is_wrong"><strong>{{ $t('practice.whatIsWrong') }}</strong>{{ result.what_is_wrong }}</div>
        <div v-if="result.suggestion"><strong>{{ $t('practice.suggestion') }}</strong>{{ result.suggestion }}</div>
      </div>
      <div class="result-actions">
        <button class="btn btn-primary" @click="step='select';result=null">{{ $t('practice.tryAnother') }}</button>
        <button class="btn" @click="step='solve'">{{ $t('practice.redo') }}</button>
        <button class="btn" @click="exportPDF">📄 PDF</button>
      </div>
    </div>
    <AiSetupGuide v-if="auth.showAiSetup" @close="auth.closeAiSetup" @proceed="pendingAction?.()" />
  </div>
</template>

<script setup>
import { ref, computed, defineAsyncComponent } from 'vue'
import { useI18n } from 'vue-i18n'
import { renderMarkdown } from '@/utils/markdown'
import { useAuth } from '@/stores/auth'
import { apiFetch } from '@/utils/api'
import { useToast } from '@/utils/toast'
import { exportProblemToPDF } from '@/utils/pdfExport'
const AiSetupGuide = defineAsyncComponent(() => import('@/components/AiSetupGuide.vue'))

const { t, locale } = useI18n()
const auth = useAuth()
const { show: showToast } = useToast()
const pendingAction = ref(null)

const topic = ref('limits')
const step = ref('select')
const filter = ref('exam')
const currentProblem = ref(null)
const previewUrl = ref(null)
const imageBase64 = ref(null)
const result = ref(null)
const generating = ref(false)
const gradingProgress = ref(0)
const gradingMessages = ['正在准备题目...', '正在分析解答...', '正在评分...', '正在生成反馈...']

const renderedStatement = computed(() => renderMarkdown(currentProblem.value?.problem_statement || ''))

const subtopics = [
  { key: 'limits', label: '极限 — 无限逼近的艺术', label_en: 'Limits — The Art of Infinite Approximation' },
  { key: 'derivatives', label: '导数 — 瞬间的变化率', label_en: 'Derivatives — Instantaneous Rate of Change' },
  { key: 'integrals', label: '积分 — 和的极限', label_en: 'Integrals — The Limit of Sums' },
  { key: 'series', label: '无穷级数 — 无限的拼图', label_en: 'Infinite Series — The Puzzle of Infinity' },
  { key: 'multivariable', label: '多元微积分 — 从平面到空间', label_en: 'Multivariable Calculus — From Plane to Space' },
]
const displaySubtopics = computed(() => subtopics.map(s => ({ ...s, label: locale.value === 'en' && s.label_en ? s.label_en : s.label })))

const difficulties = [
  { key: 'basic', label: '基础', label_en: 'Basic' },
  { key: 'advanced', label: '进阶', label_en: 'Advanced' },
  { key: 'exam', label: '考研', label_en: 'Exam Prep' },
  { key: 'graduate', label: '研究生', label_en: 'Graduate' },
  { key: 'phd', label: '博士', label_en: 'PhD' },
]
const displayDifficulties = computed(() => difficulties.map(d => ({ ...d, label: locale.value === 'en' && d.label_en ? d.label_en : d.label })))

function diffLabel(d) {
  const labels = { basic: t('practice.diffBasic'), advanced: t('practice.diffAdvanced'), exam: t('practice.diffExam'), graduate: t('practice.diffGraduate'), phd: t('practice.diffPhd') }
  return labels[d] || d
}

async function aiGenerate() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  if (!auth.hasModel) { pendingAction.value = aiGenerateWithModel; auth.openAiSetup(); return }
  await aiGenerateWithModel()
}
async function aiGenerateWithModel() {
  generating.value = true
  try {
    const r = await apiFetch('/api/practice/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic_key: topic.value, difficulty: filter.value })
    })
    if (r.status === 401) { auth.openLogin('login'); generating.value = false; return }
    currentProblem.value = (await r.json()).problem
    step.value = 'solve'
  } catch(e) { showToast(t('practice.generateFail')+': '+e.message) }
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
  if (!auth.hasModel) { pendingAction.value = submitGradeWithModel; auth.openAiSetup(); return }
  await submitGradeWithModel()
}
async function submitGradeWithModel() {
  try {
    gradingProgress.value = 25
    const r = await apiFetch('/api/grade', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic_key: topic.value, problem_id: currentProblem.value.id, image_base64: imageBase64.value })
    })
    gradingProgress.value = 60
    if (r.status === 401) { auth.openLogin('login'); return }
    result.value = await r.json()
    gradingProgress.value = 100
    step.value = 'results'
  } catch(e) { showToast(t('practice.gradeFail')+': '+e.message) }
}

function exportPDF() {
  if (!currentProblem.value) return
  const solution = result.value?.what_is_correct || result.value?.suggestion || ''
  exportProblemToPDF(currentProblem.value, solution)
}
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

.select-area { display:flex; flex-direction:column; align-items:center; gap:16px; padding:32px 0; }
.topic-select, .difficulty-select { display:flex; align-items:center; gap:8px; font-size:14px; color:var(--text-secondary); }
.topic-select select { background:var(--bg-input); color:var(--text-primary); border:1px solid var(--border); border-radius:4px; padding:6px 10px; font-size:14px; }
.filters { display:flex; gap:4px; }
.filters button { padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-size:12px; cursor:pointer; background:var(--bg-card); color:var(--text-secondary); transition:all 0.15s; }
.filters button.active { background:var(--accent); color:#fff; border-color:var(--accent); }
.btn-lg { padding:12px 32px; font-size:16px; font-weight:600; border-radius:8px; }

.btn { padding:7px 18px; border:1px solid var(--border); border-radius:4px; background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-size:14px; text-decoration:none; transition:all 0.15s; }
.btn-primary { border-color:var(--accent); color:var(--accent); }
.btn-primary:hover { background:var(--accent); color:#fff; }
.btn:disabled { opacity:0.4; cursor:not-allowed; }
.spin { display:inline-block; width:14px; height:14px; border:2px solid var(--border); border-top-color:#fff; border-radius:50%; animation:spin 0.6s linear infinite; margin-right:6px; vertical-align:middle; }
@keyframes spin { to { transform:rotate(360deg) } }

.solve-area { max-width:600px; margin:0 auto; }
.problem-display { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:24px; margin-bottom:16px; }
.p-meta { margin-bottom:8px; font-size:12px; }
.diff { font-size:12px; }
.basic { color:var(--accent-correct); } .advanced { color:var(--accent); } .exam { color:var(--accent-warm); } .graduate, .phd { color:var(--accent-error); }
.p-statement { font-size:16px; line-height:1.8; color:var(--text-primary); }
.p-statement :deep(.katex-display) { margin:16px 0; overflow-x:auto; overflow-y:hidden; }
.upload-zone { border:2px dashed var(--border); border-radius:12px; padding:40px 20px; text-align:center; cursor:pointer; background:var(--bg-card); transition:all 0.15s; }
.upload-zone:hover { border-color:var(--accent); }
.upload-icon { font-size:32px; color:var(--text-muted); margin-bottom:8px; }
.preview { text-align:center; margin:16px 0; }
.preview-img { max-width:100%; max-height:300px; border-radius:8px; border:1px solid var(--border); }
.submit-btn { width:100%; padding:14px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; margin-top:12px; }
.submit-btn:disabled { opacity:0.4; }
.grading-progress { margin-top:12px; position:relative; }
.progress-bar { height:4px; background:var(--accent); border-radius:2px; transition:width 0.3s; }
.progress-text { font-size:12px; color:var(--text-muted); margin-top:4px; display:block; text-align:center; }
.results { max-width:600px; margin:0 auto; }
.verdict { padding:14px 22px; border-radius:8px; text-align:center; font-size:19px; font-weight:700; margin:12px 0; }
.verdict-correct { background:#eaf4ee; color:var(--accent-correct); } .verdict-partial { background:#faf3e8; color:var(--accent-warm); } .verdict-incorrect { background:#f9eaea; color:var(--accent-error); }
[data-theme="dark"] .verdict-correct { background:#1a2e20; color:#8cc9a0; } [data-theme="dark"] .verdict-partial { background:#2e2418; color:#d4b87a; } [data-theme="dark"] .verdict-incorrect { background:#2e1a1a; color:#d49a9a; }
.feedback { background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:8px 0; line-height:1.8; color:var(--text-primary); }
.result-actions { display:flex; gap:8px; margin-top:16px; }
</style>
