<template>
  <div class="news-page">
    <h1>数学新闻</h1>
    <p class="sub">来自 arXiv 的最新数学论文与动态</p>
    <div class="filters">
      <button v-for="c in cats" :key="c.key" :class="{ active: activeCat === c.key }" @click="activeCat = c.key; fetchNews()">{{ c.label }}</button>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="news-list">
      <a v-for="item in news" :key="item.id" :href="item.link" target="_blank" class="news-card">
        <div class="news-meta">
          <span class="news-cat">{{ catLabel(item.cat) }}</span>
          <span class="news-date">{{ item.date }}</span>
        </div>
        <h3>{{ item.title }}</h3>
        <p class="news-authors">{{ item.authors }}</p>
        <p class="news-abstract">{{ item.summary }}</p>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cats = [
  { key: 'math.HO', label: '历史与概述' },
  { key: 'math.CA', label: '经典分析' },
  { key: 'math.DS', label: '动力系统' },
  { key: 'math.NT', label: '数论' },
  { key: 'math.PR', label: '概率论' },
  { key: 'math.NA', label: '数值分析' },
  { key: 'math.AG', label: '代数几何' },
  { key: 'math.GT', label: '几何拓扑' },
]

const activeCat = ref('math.HO')
const news = ref([])
const loading = ref(false)

function catLabel(key) {
  return cats.find(c => c.key === key)?.label || key
}

async function fetchNews() {
  loading.value = true
  try {
    const r = await fetch(`https://export.arxiv.org/api/query?search_query=cat:${activeCat.value}&sortBy=submittedDate&sortOrder=descending&max_results=15`)
    const text = await r.text()
    const parser = new DOMParser()
    const xml = parser.parseFromString(text, 'text/xml')
    const entries = xml.querySelectorAll('entry')
    news.value = Array.from(entries).map(e => ({
      id: e.querySelector('id')?.textContent?.split('/abs/').pop() || '',
      title: e.querySelector('title')?.textContent?.replace(/\n/g,' ').trim() || '',
      summary: (e.querySelector('summary')?.textContent || '').replace(/\n/g,' ').substring(0, 300) + '...',
      authors: Array.from(e.querySelectorAll('author name')).map(a => a.textContent).join(', '),
      link: e.querySelector('id')?.textContent || '',
      date: new Date(e.querySelector('published')?.textContent || '').toLocaleDateString('zh-CN'),
      cat: activeCat.value,
    }))
  } catch(e) {
    news.value = []
  }
  loading.value = false
}

onMounted(fetchNews)
</script>

<style scoped>
.news-page { max-width:900px; margin:0 auto; padding:32px 20px 64px; }
.news-page h1 { text-align:center; font-size:28px; }
.sub { text-align:center; color:#505560; margin-bottom:24px; }
.filters { display:flex; justify-content:center; flex-wrap:wrap; gap:6px; margin-bottom:24px; }
.filters button { padding:6px 16px; border:1px solid #e2e5e8; border-radius:20px; font-size:13px; background:#fff; color:#505560; cursor:pointer; transition:all 0.15s; }
.filters button:hover { border-color:#4a6a8a; color:#4a6a8a; }
.filters button.active { background:#4a6a8a; color:#fff; border-color:#4a6a8a; }
.loading { text-align:center; padding:40px; color:#889098; }
.news-list { display:flex; flex-direction:column; gap:12px; }
.news-card { display:block; padding:20px 24px; border:1px solid #e2e5e8; border-radius:10px; background:#fff; text-decoration:none; color:inherit; transition:all 0.15s; }
.news-card:hover { border-color:#4a6a8a; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.news-meta { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.news-cat { font-size:11px; color:#4a6a8a; font-weight:600; }
.news-date { font-size:11px; color:#889098; }
.news-card h3 { font-size:16px; margin:0 0 6px; line-height:1.4; }
.news-authors { font-size:12px; color:#889098; margin:0 0 8px; }
.news-abstract { font-size:13px; color:#505560; line-height:1.6; margin:0; }
@media(max-width:768px){ .news-card{padding:16px;} }
</style>
