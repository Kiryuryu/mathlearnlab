<template>
  <div class="settings-overlay" @click.self="$emit('close')">
    <div class="settings-box">
      <h3>{{ $t('settings.title') }}</h3>
      <p class="hint">{{ $t('settings.hint') }}</p>
      <label class="label">{{ $t('settings.model') }}</label>
      <select v-model="selModel" class="inp">
        <option value="deepseek-chat">DeepSeek V4</option>
        <option value="deepseek-reasoner">DeepSeek R1</option>
      </select>
      <label class="label">{{ $t('settings.apiKey') }}</label>
      <input v-model="selKey" type="password" class="inp" :placeholder="$t('settings.keyPlaceholder')" />
      <div class="actions">
        <button class="btn-cancel" @click="$emit('close')">{{ $t('settings.cancel') }}</button>
        <button class="btn-save" @click="save">{{ $t('settings.save') }}</button>
      </div>
      <p class="tip"><a href="https://platform.deepseek.com/api_keys" target="_blank">{{ $t('settings.getKey') }}</a></p>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth'
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
.settings-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:1000; display:flex; align-items:center; justify-content:center; }
.settings-box { background:var(--bg-card); border-radius:12px; padding:28px; width:420px; max-width:92vw; box-shadow:0 8px 40px rgba(0,0,0,0.15); }
h3 { font-size:18px; margin:0 0 4px; }
.hint { font-size:13px; color:var(--text-muted); margin-bottom:16px; line-height:1.6; }
.label { font-size:13px; color:var(--text-secondary); display:block; margin-bottom:4px; margin-top:12px; }
.inp { width:100%; padding:10px 12px; border:1px solid var(--border); border-radius:6px; font-size:14px; background:var(--bg-input); color:var(--text-primary); outline:none; font-family:monospace; }
.inp:focus { border-color:var(--accent); }
select.inp { font-family:var(--font-body); }
.actions { display:flex; gap:8px; margin-top:20px; }
.btn-cancel { flex:1; padding:10px; border:1px solid var(--border); border-radius:6px; background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-size:14px; }
.btn-save { flex:1; padding:10px; border:none; border-radius:6px; background:var(--accent); color:#fff; cursor:pointer; font-size:14px; font-weight:600; }
.tip { font-size:12px; color:var(--text-muted); margin-top:12px; text-align:center; }
.tip a { color:var(--accent); }
</style>
