<template>
  <div class="solve-area">
    <div class="problem-display">
      <div class="p-meta"><span :class="problem.difficulty">{{ diffLabel(problem.difficulty) }}</span></div>
      <div class="p-statement" v-html="renderedStatement"></div>
    </div>
    <div class="upload-zone" @click="$refs.fileInput.click()" v-if="!previewUrl">
      <div class="upload-icon">+</div>
      <p>{{ t('practice.uploadHint') }}</p>
      <input ref="fileInput" type="file" accept="image/*" @change="$emit('file-selected', $event)" hidden>
    </div>
    <div v-else class="preview">
      <img :src="previewUrl" class="preview-img">
      <button @click="$emit('reupload')">{{ t('practice.reupload') }}</button>
    </div>
    <button class="submit-btn" :disabled="!hasImage" @click="$emit('submit')">
      {{ isLoggedIn ? t('practice.submitForGrade') : '🔒 '+t('practice.loginToUse') }}
    </button>
    <div v-if="gradingProgress > 0" class="grading-progress">
      <div class="progress-bar" :style="{ width: gradingProgress + '%' }"></div>
      <span class="progress-text">{{ progressMessage }}</span>
    </div>
    <button class="btn" @click="$emit('back')">{{ t('practice.backToSelect') }}</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { renderMarkdown } from '@/utils/markdown'

const { t, locale } = useI18n()
const props = defineProps({
  problem: { type: Object, default: null },
  previewUrl: { type: String, default: null },
  hasImage: { type: Boolean, default: false },
  isLoggedIn: { type: Boolean, default: false },
  gradingProgress: { type: Number, default: 0 },
})
const emit = defineEmits(['file-selected', 'reupload', 'submit', 'back'])

const renderedStatement = computed(() => renderMarkdown(props.problem?.problem_statement || ''))

const progressMessage = computed(() => {
  const msgs = locale.value === 'en'
    ? ['Generating problem...', 'Analyzing solution...', 'Grading...', 'Preparing feedback...']
    : ['正在准备题目...', '正在分析解答...', '正在评分...', '正在生成反馈...']
  return msgs[Math.floor(props.gradingProgress / 25)] || (locale.value === 'en' ? 'Processing...' : '处理中...')
})

function diffLabel(d) {
  const labels = { basic: t('practice.diffBasic'), advanced: t('practice.diffAdvanced'), exam: t('practice.diffExam'), graduate: t('practice.diffGraduate'), phd: t('practice.diffPhd') }
  return labels[d] || d
}
</script>

<style scoped>
.solve-area { max-width:600px; margin:0 auto; }
.problem-display { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:24px; margin-bottom:16px; }
.p-meta { margin-bottom:8px; font-size:12px; }
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
.btn { padding:7px 18px; border:1px solid var(--border); border-radius:4px; background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-size:14px; text-decoration:none; transition:all 0.15s; margin-top:8px; }
</style>
