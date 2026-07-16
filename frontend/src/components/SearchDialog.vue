<template>
  <div class="search-overlay" @click.self="$emit('close')">
    <div class="search-modal">
      <div class="search-bar">
        <input ref="inputEl" v-model="query" :placeholder="$t('search.placeholder')" @input="onInput" @keydown.escape="$emit('close')" />
        <button class="close-btn" @click="$emit('close')">{{ $t('common.close') }}</button>
      </div>
      <div class="search-hint" v-if="!query">{{ $t('search.hint') }}</div>
      <div class="search-loading" v-if="query && loading">{{ $t('search.searching') }}</div>
      <div class="search-results-wrap" v-if="query && !loading">
        <div v-if="results.length === 0" class="search-no-results">{{ $t('search.noResults') }}</div>
        <div v-for="(group, idx) in grouped" :key="idx" class="result-group">
          <div class="result-group-label">{{ group.section }}</div>
          <router-link v-for="r in group.items" :key="r.route" :to="r.route" class="search-result-item" @click="$emit('close')">
            <div class="sr-title">{{ r.title }}</div>
            <div class="sr-excerpt" v-if="r.excerpt">{{ r.excerpt }}</div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const emit = defineEmits(['close'])
const query = ref('')
const results = ref([])
const loading = ref(false)
const inputEl = ref(null)
let debounceTimer = null

const grouped = computed(() => {
  const g = {}
  for (const r of results.value) {
    const s = r.section || t('search.other')
    if (!g[s]) g[s] = []
    g[s].push(r)
  }
  return Object.entries(g).map(([section, items]) => ({ section, items }))
})

function onInput() {
  clearTimeout(debounceTimer)
  if (!query.value.trim()) { results.value = []; loading.value = false; return }
  loading.value = true
  debounceTimer = setTimeout(doSearch, 250)
}

async function doSearch() {
  if (!query.value.trim()) return
  try {
    const r = await fetch(`/api/search?q=${encodeURIComponent(query.value.trim())}`)
    const d = await r.json()
    results.value = d.results || []
  } catch { results.value = [] }
  loading.value = false
}

watch(query, () => { if (!query.value) { results.value = []; loading.value = false } })

defineExpose({ focus: () => nextTick(() => inputEl.value?.focus()) })
</script>

<style scoped>
.search-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: flex-start; justify-content: center;
  padding-top: 10vh;
  animation: fadeIn 0.15s;
}
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
.search-modal {
  width: 560px; max-width: 90vw; max-height: 70vh;
  background: var(--bg-card); border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  display: flex; flex-direction: column;
  animation: slideDown 0.2s;
}
@keyframes slideDown { from { transform:translateY(-20px); opacity:0; } to { transform:translateY(0); opacity:1; } }
.search-bar {
  display: flex; gap: 8px; padding: 16px; border-bottom: 1px solid var(--border);
}
.search-bar input {
  flex: 1; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px;
  font-size: 15px; background: var(--bg-input); color: var(--text-primary); outline: none;
}
.search-bar input:focus { border-color: var(--accent); }
.close-btn {
  background: none; border: 1px solid var(--border); border-radius: 8px;
  padding: 0 14px; cursor: pointer; color: var(--text-secondary); font-size: 13px;
}
.close-btn:hover { background: var(--bg-nav); }
.search-hint, .search-loading { padding: 32px 16px; text-align: center; color: var(--text-muted); font-size: 14px; }
.search-results-wrap { overflow-y: auto; flex: 1; padding: 8px 0; }
.search-no-results { padding: 32px 16px; text-align: center; color: var(--text-muted); font-size: 14px; }
.result-group { margin: 0; }
.result-group-label {
  padding: 6px 16px; font-size: 11px; font-weight: 600; text-transform: uppercase;
  color: var(--text-muted); letter-spacing: 0.5px;
}
.search-result-item {
  display: block; padding: 10px 16px; text-decoration: none; color: var(--text-primary);
  border-left: 2px solid transparent; transition: all 0.1s;
}
.search-result-item:hover { background: var(--bg-nav); border-left-color: var(--accent); }
.sr-title { font-weight: 600; font-size: 14px; }
.sr-excerpt { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
</style>
