<template>
  <div class="bookmarks-page">
    <h1>{{ $t('bookmarks.title') }}</h1>
    <p class="sub">{{ $t('bookmarks.subtitle') }}</p>
    <div v-if="loading" class="loading">{{ $t('common.loading') }}</div>
    <div v-else-if="bookmarks.length === 0" class="empty">{{ $t('bookmarks.empty') }}</div>
    <div v-else class="bm-list">
      <div v-for="bm in bookmarks" :key="bm.id" class="bm-card">
        <router-link :to="bm.route" class="bm-link">
          <h3>{{ bm.title }}</h3>
          <span class="bm-date">{{ bm.created_at?.slice(0, 10) }}</span>
        </router-link>
        <button class="bm-remove" @click="removeBookmark(bm.id)">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'
const { t } = useI18n()
const { show: showToast } = useToast()
const bookmarks = ref([])
const loading = ref(true)

async function fetchBookmarks() {
  try {
    const r = await fetch('/api/bookmarks')
    if (r.ok) {
      const d = await r.json()
      bookmarks.value = d.bookmarks || []
    }
  } catch {}
  loading.value = false
}

async function removeBookmark(id) {
  try {
    const r = await fetch(`/api/bookmarks/${id}`, { method: 'DELETE' })
    if (r.ok) {
      bookmarks.value = bookmarks.value.filter(b => b.id !== id)
      showToast(t('common.bookmarkRemoved') || 'Removed')
    }
  } catch {}
}

onMounted(fetchBookmarks)
</script>

<style scoped>
.bookmarks-page { max-width:700px; margin:0 auto; padding:32px 20px 64px; }
.bookmarks-page h1 { text-align:center; font-size:24px; }
.sub { text-align:center; color:var(--text-secondary); margin-bottom:24px; }
.loading, .empty { text-align:center; padding:60px 20px; color:var(--text-muted); }
.bm-list { display:flex; flex-direction:column; gap:12px; }
.bm-card { display:flex; align-items:center; gap:12px; padding:16px 20px; background:var(--bg-card); border:1px solid var(--border); border-radius:10px; }
.bm-link { flex:1; text-decoration:none; color:var(--text-primary); }
.bm-link h3 { font-size:15px; margin:0 0 4px; }
.bm-date { font-size:12px; color:var(--text-muted); }
.bm-remove { background:none; border:1px solid var(--border); border-radius:6px; padding:4px 10px; cursor:pointer; color:var(--text-muted); font-size:14px; }
.bm-remove:hover { color:var(--accent-error); border-color:var(--accent-error); }
</style>
