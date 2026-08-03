<template>
  <div class="results">
    <div :class="'verdict verdict-'+(result.verdict==='partially_correct'?'partial':result.verdict)">
      {{ result.verdict === 'correct' ? '✓ '+t('practice.correct') : result.verdict === 'partially_correct' ? '≈ '+t('practice.partial') : '✗ '+t('practice.incorrect') }}
    </div>
    <div class="feedback">
      <div v-if="result.what_is_correct"><strong>{{ t('practice.whatIsCorrect') }}</strong>{{ result.what_is_correct }}</div>
      <div v-if="result.what_is_wrong"><strong>{{ t('practice.whatIsWrong') }}</strong>{{ result.what_is_wrong }}</div>
      <div v-if="result.suggestion"><strong>{{ t('practice.suggestion') }}</strong>{{ result.suggestion }}</div>
    </div>
    <div class="result-actions">
      <button class="btn btn-primary" @click="$emit('try-another')">{{ t('practice.tryAnother') }}</button>
      <button class="btn" @click="$emit('redo')">{{ t('practice.redo') }}</button>
      <button class="btn" @click="$emit('export-pdf')">📄 PDF</button>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
defineProps({ result: { type: Object, default: null } })
defineEmits(['try-another', 'redo', 'export-pdf'])
</script>

<style scoped>
.results { max-width:600px; margin:0 auto; }
.verdict { padding:14px 22px; border-radius:8px; text-align:center; font-size:19px; font-weight:700; margin:12px 0; }
.verdict-correct { background:#eaf4ee; color:var(--accent-correct); } .verdict-partial { background:#faf3e8; color:var(--accent-warm); } .verdict-incorrect { background:#f9eaea; color:var(--accent-error); }
[data-theme="dark"] .verdict-correct { background:#1a2e20; color:#8cc9a0; } [data-theme="dark"] .verdict-partial { background:#2e2418; color:#d4b87a; } [data-theme="dark"] .verdict-incorrect { background:#2e1a1a; color:#d49a9a; }
.feedback { background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:8px 0; line-height:1.8; color:var(--text-primary); }
.result-actions { display:flex; gap:8px; margin-top:16px; }
.btn { padding:7px 18px; border:1px solid var(--border); border-radius:4px; background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-size:14px; text-decoration:none; transition:all 0.15s; }
.btn-primary { border-color:var(--accent); color:var(--accent); }
.btn-primary:hover { background:var(--accent); color:#fff; }
</style>
