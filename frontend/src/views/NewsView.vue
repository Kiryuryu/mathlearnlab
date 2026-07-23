<template>
  <div class="news-page">
    <h1>{{ $t('news.title') }}</h1>
    <p class="sub">{{ $t('news.subtitle') }}</p>

    <!-- Post list -->
    <div v-if="!selectedPost" class="news-list">
      <div v-if="loading" class="loading">{{ $t('news.loading') }}</div>
      <template v-else>
        <div v-for="post in posts" :key="post.slug" class="news-card" @click="goToPost(post)">
          <div class="news-meta">
            <span class="news-cat">{{ post.category }}</span>
            <span class="news-date">{{ post.date }}</span>
          </div>
          <h3>{{ post.title }}</h3>
          <p class="news-summary">{{ stripSummary(post.summary) }}</p>
          <button class="share-btn" @click.stop="sharePostById(post)">🔗 分享</button>
        </div>
        <div v-if="!posts.length" class="empty">{{ $t('news.empty') }}</div>
      </template>
    </div>

    <!-- Post detail -->
    <div v-else class="post-detail">
      <button class="back-btn" @click="$router.push('/news')">{{ $t('news.back') }}</button>
      <h2>{{ selectedPost.title }}</h2>
      <div class="post-meta">
        <span>{{ selectedPost.date }} · {{ selectedPost.category }}</span>
        <button class="share-btn" @click="sharePost(selectedPost)">🔗 分享</button>
      </div>
      <div class="post-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'
import { renderMarkdown, stripMarkdown } from '@/utils/markdown'

const route = useRoute()
const { t } = useI18n()
const { show: showToast } = useToast()

const posts = ref([])
const loading = ref(false)
const selectedPost = ref(null)
const renderedContent = ref('')

function stripSummary(s) {
  const text = stripMarkdown(s)
  return text.length > 120 ? text.slice(0, 120) + '…' : text
}

async function fetchPosts() {
  loading.value = true
  try {
    const r = await fetch('/api/blog/posts')
    posts.value = (await r.json()).posts || []
    
    // If we're on a detail route, auto-load that post
    const slug = route.params.slug
    if (slug) {
      const post = posts.value.find(p => p.slug === slug)
      if (post) {
        selectedPost.value = post
        renderedContent.value = ''
        try {
          const cr = await fetch(`/api/blog/posts/${slug}`)
          const cd = await cr.json()
          renderedContent.value = renderMarkdown(cd.content || '')
        } catch {}
      } else {
        // Slug not in list — redirect to list view
        window.location.href = '/news'
      }
    }
  } catch(e) { 
    console.warn('Failed to fetch posts', e)
    showToast(t('news.loadFail'))
  }
  loading.value = false
}

function goToPost(post) {
  window.location.href = `/news/${post.slug}`
}

function sharePost(post) {
  sharePostById(post)
}

function sharePostById(post) {
  const url = `${window.location.origin}/news/${post.slug}`
  if (navigator.share) {
    navigator.share({ title: post.title, url })
  } else {
    navigator.clipboard.writeText(url).then(() => {
      showToast(t('common.linkCopied') || '链接已复制')
    }).catch(() => {})
  }
}

onMounted(fetchPosts)
</script>

<style scoped>
.news-page { max-width:800px; margin:0 auto; padding:32px 20px 64px; }
.news-page h1 { text-align:center; font-size:28px; }
.sub { text-align:center; color:var(--text-secondary); margin-bottom:24px; }
.loading, .empty { text-align:center; padding:40px; color:var(--text-muted); }
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
.back-btn { padding:6px 14px; border:1px solid var(--border); border-radius:4px; background:none; color:var(--accent); cursor:pointer; font-size:13px; margin-bottom:16px; }
.back-btn:hover { background:var(--bg-nav); }
.post-detail h2 { font-size:24px; margin:8px 0; }
.post-meta { font-size:12px; color:var(--text-muted); margin-bottom:24px; display:flex; align-items:center; gap:12px; }
.post-content { font-size:15px; line-height:1.9; color:var(--text-primary); }
.post-content :deep(p) { margin:12px 0; }
.post-content :deep(h2), .post-content :deep(h3), .post-content :deep(h4) { margin:24px 0 12px; }
.post-content :deep(.katex-display) { margin:16px 0; overflow-x:auto; overflow-y:hidden; }
.post-content :deep(code) { background:var(--bg-nav); padding:2px 5px; border-radius:3px; }
.post-content :deep(pre) { background:var(--bg-nav); border:1px solid var(--border); border-radius:6px; padding:14px 18px; overflow-x:auto; }
</style>
