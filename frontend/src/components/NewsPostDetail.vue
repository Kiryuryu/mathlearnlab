<template>
  <div class="post-detail">
    <button class="back-btn" @click="$emit('back')">{{ t('news.back') }}</button>
    <h2>{{ post.title }}</h2>
    <div class="post-meta">
      <span>{{ post.date }} · {{ post.category }}</span>
      <button class="share-btn" @click="sharePost">🔗 {{ t('common.share') }}</button>
    </div>
    <div class="post-content" v-html="content"></div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'

const { t } = useI18n()
const { show: showToast } = useToast()
const props = defineProps({ post: { type: Object, default: null }, content: { type: String, default: '' } })
const emit = defineEmits(['back'])

function sharePost() {
  if (!props.post) return
  const url = `${window.location.origin}/news/${props.post.slug}`
  if (navigator.share) {
    navigator.share({ title: props.post.title, url })
  } else {
    navigator.clipboard.writeText(url).then(() => {
      showToast(t('common.linkCopied') || '链接已复制')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.back-btn { padding:6px 14px; border:1px solid var(--border); border-radius:4px; background:none; color:var(--accent); cursor:pointer; font-size:13px; margin-bottom:16px; }
.back-btn:hover { background:var(--bg-nav); }
.post-detail h2 { font-size:24px; margin:8px 0; }
.post-meta { font-size:12px; color:var(--text-muted); margin-bottom:24px; display:flex; align-items:center; gap:12px; }
.share-btn { background:none; border:none; font-size:14px; cursor:pointer; opacity:0.4; transition:opacity 0.15s; padding:2px; }
.share-btn:hover { opacity:1; }
.post-content { font-size:15px; line-height:1.9; color:var(--text-primary); }
.post-content :deep(p) { margin:12px 0; }
.post-content :deep(h2), .post-content :deep(h3), .post-content :deep(h4) { margin:24px 0 12px; }
.post-content :deep(.katex-display) { margin:16px 0; overflow-x:auto; overflow-y:hidden; }
.post-content :deep(code) { background:var(--bg-nav); padding:2px 5px; border-radius:3px; }
.post-content :deep(pre) { background:var(--bg-nav); border:1px solid var(--border); border-radius:6px; padding:14px 18px; overflow-x:auto; }
</style>
