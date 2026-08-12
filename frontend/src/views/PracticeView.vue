<template>
  <div class="practice-page">
    <div class="header">
      <router-link to="/subject/gaoshu" class="back">← {{ $t('practice.backToExhibit') }}</router-link>
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
    <ProblemSelect
      v-if="step === 'select'"
      :topic="topic"
      :filter="filter"
      :generating="generating"
      :is-logged-in="auth.isLoggedIn"
      @update:topic="topic = $event"
      @update:filter="filter = $event"
      @generate="aiGenerate"
    />

    <!-- Phase 2: Solve -->
    <ProblemSolve
      v-if="step === 'solve' && currentProblem"
      :problem="currentProblem"
      :preview-url="previewUrl"
      :has-image="!!imageBase64"
      :is-logged-in="auth.isLoggedIn"
      :grading-progress="gradingProgress"
      @file-selected="handleFile"
      @reupload="reupload"
      @submit="submitGrade"
      @back="backToSelect"
    />

    <!-- Phase 3: Results -->
    <ProblemResult
      v-if="step === 'results' && result"
      :result="result"
      @try-another="tryAnother"
      @redo="redo"
      @export-pdf="exportPDF"
    />

    <AiSetupGuide v-if="auth.showAiSetup" @close="auth.closeAiSetup" @proceed="pendingAction?.()" />
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
import { apiFetch } from '@/utils/api'
import { useToast } from '@/utils/toast'
import { exportProblemToPDF } from '@/utils/pdfExport'
import ProblemSelect from '@/components/ProblemSelect.vue'
import ProblemSolve from '@/components/ProblemSolve.vue'
import ProblemResult from '@/components/ProblemResult.vue'
const AiSetupGuide = defineAsyncComponent(() => import('@/components/AiSetupGuide.vue'))

const { t, locale } = useI18n()
const auth = useAuth()
const { show: showToast } = useToast()
const pendingAction = ref(null)

onUnmounted(() => { pendingAction.value = null })

const topic = ref('limits')
const step = ref('select')
const filter = ref('exam')
const currentProblem = ref(null)
const previewUrl = ref(null)
const imageBase64 = ref(null)
const result = ref(null)
const generating = ref(false)
const gradingProgress = ref(0)

function backToSelect() { step.value = 'select'; currentProblem.value = null }
function reupload() { previewUrl.value = null; imageBase64.value = null }
function tryAnother() { step.value = 'select'; result.value = null }
function redo() { step.value = 'solve' }

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
    const d = await r.json().catch(() => ({}))
    if (!r.ok || !d.problem) {
      showToast(t('practice.generateFail') + ': ' + (d.detail || t('practice.emptyProblem')))
      generating.value = false
      return
    }
    currentProblem.value = d.problem
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

async function exportPDF() {
  if (!currentProblem.value) return
  const solution = result.value?.what_is_correct || result.value?.suggestion || ''
  await exportProblemToPDF(currentProblem.value, solution, locale.value)
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
</style>
