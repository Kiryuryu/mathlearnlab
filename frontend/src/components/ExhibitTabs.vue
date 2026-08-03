<template>
  <nav class="tabs">
    <a v-for="t in tabs" :key="t.key" :href="'?tab='+t.key" :class="['tab', { active: active === t.key }]" @click.prevent="$emit('change', t.key)">{{ t('exhibit.' + t.key) }}</a>
  </nav>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
defineProps({
  tabs: { type: Array, default: () => [] },
  active: { type: String, default: 'concept' },
})
defineEmits(['change'])
</script>

<style scoped>
.tabs { display:flex; justify-content:center; gap:0; border-bottom:1px solid var(--border); background:var(--bg-nav); position:sticky; top:0; z-index:10; }
.tab { padding:12px 20px; font-size:14px; color:var(--text-secondary); text-decoration:none; border-bottom:2px solid transparent; transition:all 0.15s; }
.tab:hover { color:var(--accent); }
.tab.active { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
@media(max-width:768px) { .tabs { overflow-x:auto; justify-content:flex-start; } .tab { padding:10px 14px; font-size:13px; white-space:nowrap; } }
</style>
