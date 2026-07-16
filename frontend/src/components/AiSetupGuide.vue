<template>
  <div class="setup-overlay" @click.self="$emit('close')">
    <div class="setup-modal">
      <div class="setup-steps">
        <span v-for="s in steps" :key="s.key" :class="['step-dot', { active: s.key === step, done: stepIdx > s.idx }]">
          <span v-if="stepIdx > s.idx">✓</span><span v-else>{{ s.idx + 1 }}</span>
        </span>
      </div>

      <!-- Step 1: Welcome -->
      <div v-if="step === 'intro'" class="step-content">
        <h2>{{ $t('setup.welcome') }}</h2>
        <p>{{ $t('setup.welcomeDesc') }}</p>
        <button class="btn btn-primary" @click="step = 'model'">{{ $t('setup.next') }}</button>
        <button class="btn btn-ghost" @click="$emit('close')">{{ $t('setup.skip') }}</button>
      </div>

      <!-- Step 2: Select Model -->
      <div v-if="step === 'model'" class="step-content">
        <h2>{{ $t('setup.selectModel') }}</h2>
        <div class="model-options">
          <div v-for="m in models" :key="m.id" :class="['model-card', { active: selectedModel === m.id }]" @click="selectedModel = m.id">
            <div class="model-name">{{ m.name }}</div>
            <div class="model-desc">{{ locale === 'en' ? m.desc_en : m.desc_zh }}</div>
          </div>
        </div>
        <div class="step-actions">
          <button class="btn" @click="step = 'intro'">{{ $t('setup.back') }}</button>
          <button class="btn btn-primary" @click="step = 'key'">{{ $t('setup.next') }}</button>
        </div>
      </div>

      <!-- Step 3: Enter API Key -->
      <div v-if="step === 'key'" class="step-content">
        <h2>{{ $t('setup.enterKey') }}</h2>
        <p>{{ $t('setup.keyDesc') }}</p>
        <input v-model="apiKeyInput" :placeholder="$t('setup.keyPlaceholder')" class="setup-input" />
        <p class="setup-hint">
          <a href="https://platform.deepseek.com" target="_blank">{{ $t('setup.getKey') }}</a>
        </p>
        <div class="step-actions">
          <button class="btn" @click="step = 'model'">{{ $t('setup.back') }}</button>
          <button class="btn btn-primary" :disabled="!apiKeyInput.trim()" @click="saveAndProceed">{{ $t('setup.done') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'

const { locale } = useI18n()
const emit = defineEmits(['close', 'proceed'])
const auth = useAuth()

const step = ref('intro')
const steps = [
  { key: 'intro', idx: 0 },
  { key: 'model', idx: 1 },
  { key: 'key', idx: 2 },
]
const stepIdx = computed(() => steps.find(s => s.key === step.value)?.idx ?? 0)

const selectedModel = ref('deepseek-chat')
const apiKeyInput = ref('')

const models = [
  { id: 'deepseek-chat', name: 'DeepSeek Chat', desc_zh: '通用模型，适合出题和批改', desc_en: 'General-purpose model, suitable for problem generation and grading' },
  { id: 'deepseek-reasoner', name: 'DeepSeek Reasoner', desc_zh: '推理增强，适合复杂批改', desc_en: 'Enhanced reasoning, suitable for complex grading' },
]

function saveAndProceed() {
  auth.setModelConfig(selectedModel.value, apiKeyInput.value.trim())
  emit('proceed')
}
</script>

<style scoped>
.setup-overlay {
  position:fixed; inset:0; z-index:1000;
  background:rgba(0,0,0,0.5);
  display:flex; align-items:center; justify-content:center;
}
.setup-modal {
  width:420px; max-width:90vw;
  background:var(--bg-card); border-radius:12px;
  padding:32px; box-shadow:0 20px 60px rgba(0,0,0,0.3);
  animation:slideUp 0.25s;
}
@keyframes slideUp { from{transform:translateY(30px);opacity:0} to{transform:translateY(0);opacity:1} }
.setup-steps { display:flex; justify-content:center; gap:8px; margin-bottom:28px; }
.step-dot {
  width:28px; height:28px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:12px; font-weight:600;
  background:var(--bg-nav); color:var(--text-muted); transition:all 0.2s;
}
.step-dot.active { background:var(--accent); color:#fff; }
.step-dot.done { background:var(--accent-correct); color:#fff; }
.step-content { text-align:center; }
.step-content h2 { font-size:20px; margin:0 0 12px; }
.step-content p { font-size:14px; color:var(--text-secondary); line-height:1.6; margin:0 0 20px; }
.model-options { display:flex; flex-direction:column; gap:10px; margin-bottom:20px; }
.model-card {
  padding:14px 18px; border:1px solid var(--border); border-radius:8px;
  cursor:pointer; text-align:left; transition:all 0.15s;
}
.model-card:hover { border-color:var(--border-focus); }
.model-card.active { border-color:var(--accent); background:rgba(74,106,138,0.08); }
.model-name { font-size:15px; font-weight:600; color:var(--text-primary); }
.model-desc { font-size:12px; color:var(--text-muted); margin-top:2px; }
.step-actions { display:flex; gap:8px; justify-content:center; margin-top:8px; }
.btn { padding:8px 20px; border:1px solid var(--border); border-radius:6px; font-size:14px; cursor:pointer; background:var(--bg-card); color:var(--text-primary); transition:all 0.15s; text-decoration:none; }
.btn-primary { background:var(--accent); color:#fff; border-color:var(--accent); }
.btn-primary:hover { opacity:0.9; }
.btn-primary:disabled { opacity:0.4; cursor:not-allowed; }
.btn-ghost { background:none; border-color:transparent; color:var(--text-muted); }
.btn-ghost:hover { color:var(--text-secondary); }
.setup-input { width:100%; padding:10px 14px; border:1px solid var(--border); border-radius:8px; font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none; margin-bottom:8px; }
.setup-input:focus { border-color:var(--accent); }
.setup-hint { font-size:12px; color:var(--text-muted); margin-bottom:16px; }
.setup-hint a { color:var(--accent); }
</style>
