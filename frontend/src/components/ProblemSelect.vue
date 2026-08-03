<template>
  <div class="select-area">
    <div class="topic-select">
      <label>{{ t('practice.topic') }}</label>
      <select :value="topic" @change="$emit('update:topic', $event.target.value)">
        <option v-for="s in displaySubtopics" :key="s.key" :value="s.key">{{ s.label }}</option>
      </select>
    </div>
    <div class="difficulty-select">
      <label>{{ t('practice.difficulty') }}</label>
      <div class="filters">
        <button v-for="d in displayDifficulties" :key="d.key" :class="{ active: filter === d.key }" @click="$emit('update:filter', d.key)">{{ d.label }}</button>
      </div>
    </div>
    <button class="btn btn-primary btn-lg" @click="$emit('generate')" :disabled="generating">
      <span v-if="generating" class="spin"></span>
      {{ generating ? t('practice.generating') : (isLoggedIn ? t('practice.aiGenerate') : '🔒 '+t('practice.loginToUse')) }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const props = defineProps({
  topic: { type: String, default: 'limits' },
  filter: { type: String, default: 'exam' },
  generating: { type: Boolean, default: false },
  isLoggedIn: { type: Boolean, default: false },
})
const emit = defineEmits(['generate', 'update:topic', 'update:filter'])

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
</script>

<style scoped>
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
</style>
