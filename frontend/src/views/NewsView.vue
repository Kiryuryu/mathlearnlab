<template>
  <div class="news-page">
    <h1>数学新闻</h1>
    <p class="sub">数学界的最新动态与深度文章</p>

    <!-- Post detail -->
    <div v-if="selectedPost" class="post-detail">
      <button class="back-btn" @click="selectedPost=null">← 返回列表</button>
      <h2>{{ selectedPost.title }}</h2>
      <div class="post-meta">{{ selectedPost.date }} · {{ selectedPost.category }}</div>
      <div class="post-content" v-html="renderedContent"></div>
    </div>

    <!-- Post list -->
    <div v-else>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else class="news-list">
        <div v-for="post in posts" :key="post.slug" class="news-card" @click="openPost(post)">
          <div class="news-meta">
            <span class="news-cat">{{ post.category }}</span>
            <span class="news-date">{{ post.date }}</span>
          </div>
          <h3>{{ post.title }}</h3>
          <p class="news-summary">{{ post.summary }}</p>
        </div>
        <div v-if="!posts.length" class="empty">暂无文章</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const posts = ref([])
const loading = ref(false)
const selectedPost = ref(null)
const renderedContent = ref('')

async function fetchPosts() {
  loading.value = true
  try {
    const r = await fetch('/api/blog/posts')
    posts.value = (await r.json()).posts || []
  } catch(e) {}
  loading.value = false
}

async function openPost(post) {
  try {
    const r = await fetch(`/api/blog/posts/${post.slug}`)
    selectedPost.value = await r.json()
    // Simple markdown→HTML
    let html = selectedPost.value.content
      .replace(/^### (.+)$/gm, '<h4>$1</h4>')
      .replace(/^## (.+)$/gm, '<h3>$1</h3>')
      .replace(/^# (.+)$/gm, '<h2>$1</h2>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>')
    renderedContent.value = '<p>' + html + '</p>'
    window.scrollTo({ top: 0, behavior: 'smooth' })
    setTimeout(() => { if (window.MathJax) MathJax.typesetPromise() }, 200)
  } catch(e) {}
}

onMounted(fetchPosts)
</script>

<style scoped>
.news-page { max-width:800px; margin:0 auto; padding:32px 20px 64px; }
.news-page h1 { text-align:center; font-size:28px; }
.sub { text-align:center; color:#505560; margin-bottom:24px; }
.loading, .empty { text-align:center; padding:40px; color:#889098; }
.news-list { display:flex; flex-direction:column; gap:12px; }
.news-card { padding:20px 24px; border:1px solid #e2e5e8; border-radius:10px; background:#fff; cursor:pointer; transition:all 0.15s; }
.news-card:hover { border-color:#4a6a8a; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.news-meta { display:flex; justify-content:space-between; margin-bottom:8px; }
.news-cat { font-size:11px; color:#4a6a8a; font-weight:600; }
.news-date { font-size:11px; color:#889098; }
.news-card h3 { font-size:16px; margin:0 0 6px; }
.news-summary { font-size:13px; color:#505560; line-height:1.6; margin:0; }
.back-btn { padding:6px 14px; border:1px solid #e2e5e8; border-radius:4px; background:none; color:#4a6a8a; cursor:pointer; font-size:13px; margin-bottom:16px; }
.post-detail h2 { font-size:24px; margin:8px 0; }
.post-meta { font-size:12px; color:#889098; margin-bottom:24px; }
.post-content { font-size:15px; line-height:1.9; }
.post-content :deep(p) { margin:12px 0; }
.post-content :deep(h2), .post-content :deep(h3), .post-content :deep(h4) { margin:24px 0 12px; }
</style>
