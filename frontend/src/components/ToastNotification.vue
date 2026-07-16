<template>
  <div class="toast-container">
    <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">{{ t.msg }}</div>
  </div>
</template>

<script setup>
import { useToast } from '@/utils/toast'
const { toasts } = useToast()
</script>

<style scoped>
.toast-container { position:fixed; top:64px; right:16px; z-index:2000; display:flex; flex-direction:column; gap:8px; pointer-events:none; }
.toast { padding:10px 18px; border-radius:8px; font-size:13px; font-weight:500; box-shadow:0 4px 16px rgba(0,0,0,0.12); animation:slideIn 0.25s; pointer-events:auto; max-width:320px; }
.toast.error { background:var(--accent-error); color:#fff; }
.toast.success { background:var(--accent-correct); color:#fff; }
@keyframes slideIn { from{transform:translateX(40px);opacity:0} to{transform:translateX(0);opacity:1} }
</style>
