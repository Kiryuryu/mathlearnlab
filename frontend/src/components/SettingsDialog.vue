<template>
  <BaseModal panel-class="settings-panel" @close="$emit('close')">
    <h3>{{ $t('settings.title') }}</h3>
    <p class="hint">{{ $t('settings.hint') }}</p>
    <label class="label">{{ $t('settings.model') }}</label>
    <div class="model-grid">
      <button
        :class="['model-opt', { on: selModel === 'deepseek-chat' }]"
        @click="selModel = 'deepseek-chat'"
      >
        <span class="model-name">DeepSeek V4</span>
        <span class="model-desc">{{ $t('settings.v4Desc') }}</span>
      </button>
      <button
        :class="['model-opt', { on: selModel === 'deepseek-reasoner' }]"
        @click="selModel = 'deepseek-reasoner'"
      >
        <span class="model-name">DeepSeek R1</span>
        <span class="model-desc">{{ $t('settings.r1Desc') }}</span>
      </button>
    </div>
    <label class="label">{{ $t('settings.apiKey') }}</label>
    <input v-model="selKey" type="password" class="inp" :placeholder="$t('settings.keyPlaceholder')" />
    <div class="actions">
      <button class="btn-cancel" @click="$emit('close')">{{ $t('settings.cancel') }}</button>
      <button class="btn-save" @click="save">{{ $t('settings.save') }}</button>
    </div>
    <p class="tip"><a href="https://platform.deepseek.com/api_keys" target="_blank">{{ $t('settings.getKey') }}</a></p>
  </BaseModal>
</template>
<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth'
import BaseModal from '@/components/BaseModal.vue'
const auth = useAuth()
const emit = defineEmits(['close'])
const selModel = ref(auth.model || 'deepseek-chat')
const selKey = ref(auth.apiKey || '')
function save() {
  auth.setModelConfig(selModel.value, selKey.value)
  emit('close')
}
</script>
<style scoped>
:deep(.base-panel.settings-panel) { padding:28px; width:440px; max-width:92vw; }
h3 { font-size:18px; margin:0 0 4px; }
.hint { font-size:13px; color:var(--text-muted); margin-bottom:16px; line-height:1.6; }
.label { font-size:13px; color:var(--text-secondary); display:block; margin-bottom:6px; margin-top:14px; }
.model-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.model-opt {
  display:flex; flex-direction:column; gap:4px; align-items:flex-start;
  padding:12px 14px; border:1px solid var(--border); border-radius:var(--radius);
  background:var(--bg-card); color:var(--text-primary); cursor:pointer;
  text-align:left; transition:border-color 0.15s, background 0.15s;
}
.model-opt:hover { border-color:var(--border-focus); background:var(--bg-nav); }
.model-opt.on { border-color:var(--accent); background:var(--accent-soft); }
.model-name { font-weight:600; font-size:14px; }
.model-desc { font-size:11px; color:var(--text-muted); line-height:1.5; }
.inp { width:100%; padding:10px 12px; border:1px solid var(--border); border-radius:var(--radius); font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none; font-family:monospace; }
.inp:focus { border-color:var(--accent); }
.actions { display:flex; gap:8px; margin-top:20px; }
.btn-cancel { flex:1; padding:10px; border:1px solid var(--border); border-radius:var(--radius); background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-size:14px; }
.btn-save { flex:1; padding:10px; border:none; border-radius:var(--radius); background:var(--accent); color:#fff; cursor:pointer; font-size:14px; font-weight:600; }
.tip { font-size:12px; color:var(--text-muted); margin-top:12px; text-align:center; }
.tip a { color:var(--accent); }
@media(max-width:480px) { .model-grid { grid-template-columns:1fr; } }
</style>
