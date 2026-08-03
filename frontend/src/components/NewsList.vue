<template>
  <div class="news-list">
    <div v-if="loading" class="loading">{{ t('news.loading') }}</div>
    <template v-else>
      <div v-for="post in posts" :key="post.slug" class="news-card" @click="$emit('open', post)">
        <div class="news-meta">
          <span class="news-cat">{{ post.category }}</span>
          <span class="news-date">{{ post.date }}</span>
        </div>
        <h3>{{ post.title }}</h3>
        <p class="news-summary">{{ stripSummary(post.summary) }}</p>
        <button class="share-btn" @click.stop="sharePost(post)">🔗 {{ t('common.share') }}</button>
      </div>
      <div v-if="!posts.length" class="empty">{{ t('news.empty') }}</div>
    </template>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'
import { stripMarkdown } from '@/utils/markdown'

const { t } = useI18n()
const { show: showToast } = useToast()
defineProps({ posts: { type: Array, default: () => [] }, loading: { type: Boolean, default: false } })
const emit = defineEmits(['open'])

function stripSummary(s) {
  const text = stripMarkdown(s)
  return text.length > 120 ? text.slice(0, 120) + '…' : text
}

function sharePost(post) {
  const url = `${window.location.origin}/news/${post.slug}`
  if (navigator.share) {
    navigator.share({ title: post.title, url })
  } else {
    navigator.clipboard.writeText(url).then(() => {
      showToast(t('common.linkCopied') || '链接已复制')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.news-list { display:flex; flex-direction:column; gap:12px; }
.news-card { padding:20px 24px; border:1px solid var(--border); border-radius:10px; background:var(--bg-card); cursor:pointer; transition:all 0.15s; position:relative; }
.news-card:hover { border-color:var(--accent); box-shadow:var(--shadow-elevated); }
.news-meta { display:flex; justify-content:space-between; margin-bottom:8px; }
.news-cat { font-size:11px; color:var(--accent); font-weight:600; }
.news-date { font-size:11px; color:var(--text-muted); }
.news-card h3 { font-size:16px; margin:0 0 6px; color:var(--text-primary); }
.news-summary { font-size:13px; color:var(--text-secondary); line-height:1.6; margin:0; }
.share-btn { position:absolute; bottom:12px; right:12px; background:none; border:none; font-size:14px; cursor:pointer; opacity:0.4; transition:opacity 0.15s; padding:2px; }
.share-btn:hover { opacity:1; }
.loading, .empty { text-align:center; padding:40px; color:var(--text-muted); }
</style>
