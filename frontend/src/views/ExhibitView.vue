<template>
  <div class="exhibit-page" v-if="exhibit">
    <ExhibitHero
      :name="exhibitName"
      :big-q="exhibitBigQ"
      :historian="exhibit.historian"
      :beauty="exhibitBeauty"
      :hero-bg="heroBg"
    />
    <ExhibitTabs :tabs="tabs" :active="activeTab" @change="activeTab = $event" />
    <div class="tab-content">
      <div class="exhibit-actions">
        <button class="action-btn" @click="shareLink" :title="$t('common.share')">🔗</button>
        <button class="action-btn" @click="toggleBookmark" :title="isBookmarked ? $t('common.unbookmark') : $t('common.bookmark')">
          {{ isBookmarked ? '★' : '☆' }}
        </button>
      </div>
      <div v-if="loading" class="skeleton-wrap">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text short"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-block"></div>
      </div>
      <div v-else v-html="content" ref="contentEl" class="content-fade"></div>
      <div class="viz-wrap" v-if="activeTab === 'concept' || activeTab === 'explore'">
        <h4>{{ $t('exhibit.explore') }}</h4>
        <EulerSpiral v-if="topic === 'derivatives' && activeTab === 'explore'" />
        <template v-else>
          <div ref="vizPlot" class="viz-plot"></div>
          <div ref="vizControls" class="viz-ctrls"></div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'
import { museumViz } from '@/utils/viz'
import { renderMarkdown } from '@/utils/markdown'
import { useAuth } from '@/stores/auth'
import { useToast } from '@/utils/toast'
import { apiFetch } from '@/utils/api'
import ExhibitHero from '@/components/ExhibitHero.vue'
import ExhibitTabs from '@/components/ExhibitTabs.vue'
import EulerSpiral from '@/components/EulerSpiral.vue'

const { t, locale } = useI18n()
const route = useRoute()
const auth = useAuth()
const { show: showToast } = useToast()
const topic = computed(() => route.params.topic)
const activeTab = ref(route.query.tab || 'concept')
const exhibit = ref(null)
const content = ref('')
const loading = ref(false)
const vizPlot = ref(null)
const vizControls = ref(null)
const contentEl = ref(null)
const isBookmarked = ref(false)

const tabs = [
  { key: 'concept' },
  { key: 'applications' },
  { key: 'history' },
  { key: 'beauty' },
  { key: 'method' },
  { key: 'explore' },
]

const exhibitName = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.en ? exhibit.value.en : exhibit.value.zh
})
const exhibitBigQ = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.big_question_en ? exhibit.value.big_question_en : exhibit.value.big_question
})
const exhibitBeauty = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.beauty_en ? exhibit.value.beauty_en : exhibit.value.beauty
})

const heroBgs = {
  limits: 'linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)',
  derivatives: 'linear-gradient(135deg,#2d1b69,#5b2c8e)',
  integrals: 'linear-gradient(135deg,#0d3b3b,#1a6b5a)',
  series: 'linear-gradient(135deg,#3d1a1a,#8b3a3a)',
  multivariable: 'linear-gradient(135deg,#1a2d3d,#2c5f8b)',
  'linear-algebra': 'linear-gradient(135deg,#1a1a2e,#2a2a4e)',
  probability: 'linear-gradient(135deg,#2e1a1a,#4e2a2a)',
}
const heroBg = computed(() => heroBgs[topic.value] || 'linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)')

async function loadContent() {
  loading.value = true
  try {
    // Load exhibit info
    const er = await apiFetch('/api/museum/exhibits')
    const ed = await er.json()
    exhibit.value = ed.exhibits[topic.value] || { zh: topic.value }
    // Load tab content — notebook only for concept tab
    let path
    if (activeTab.value === 'concept' && ed.exhibits[topic.value]?.notebook) {
      path = ed.exhibits[topic.value].notebook
    } else {
      path = `exhibits/${topic.value}/${activeTab.value}`
    }
    const lang = locale.value === 'en' ? 'en' : 'zh'
    const cr = await apiFetch(`/api/content/${path}?lang=${lang}`)
    const cd = await cr.json()
    if (cd.error) {
      content.value = '<p>' + cd.error + '</p>'
    } else {
      content.value = renderMarkdown(cd.content || '')
    }
  } catch(e) {
    content.value = '<p>' + t('exhibit.loadFail') + '</p>'
  }
  loading.value = false
  await nextTick()
}

watch([topic, activeTab, locale], loadContent, { immediate: true })

async function loadBookmarks() {
  if (!auth.isLoggedIn) return
  try {
    const r = await apiFetch('/api/bookmarks')
    if (r.ok) {
      const d = await r.json()
      const bm = d.bookmarks || []
      isBookmarked.value = bm.some(b => b.route === `/exhibit/${topic.value}`)
    }
  } catch {}
}

async function toggleBookmark() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  try {
    const r = await apiFetch('/api/bookmarks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        route: `/exhibit/${topic.value}`,
        title: exhibitName.value || topic.value,
      })
    })
    if (r.ok) {
      isBookmarked.value = !isBookmarked.value
      showToast(isBookmarked.value ? t('common.bookmarkAdded') : t('common.bookmarkRemoved'))
    }
  } catch {}
}

function shareLink() {
  const url = window.location.href
  if (navigator.share) {
    navigator.share({ title: exhibitName.value || topic.value, url })
  } else {
    navigator.clipboard.writeText(url).then(() => {
      showToast(t('common.linkCopied'))
    }).catch(() => {
      window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(exhibitName.value || topic.value)}`, '_blank')
    })
  }
}

// Plotly viz (lazy-loaded on demand)
let vizInited = false
onMounted(async () => {
  try {
    await loadPlotly()
    await nextTick()
    if (!vizInited && vizPlot.value) { vizInited = true; initViz() }
  } catch(e) { console.warn('Plotly init failed', e) }
})

function initViz() {
  if (typeof Plotly === 'undefined' || !vizPlot.value) return
  const t = topic.value
  const el = vizPlot.value
  const ctrls = vizControls.value
  const labels = { epsilon: t('exhibit.vizEpsilon'), tangent: t('exhibit.vizTangent'), rectangles: t('exhibit.vizRectangles'), harmonics: t('exhibit.vizHarmonics') }
  if (t === 'limits') museumViz.epsilon(el, ctrls, labels)
  else if (t === 'derivatives') museumViz.tangent(el, ctrls, labels)
  else if (t === 'integrals') museumViz.riemann(el, ctrls, labels)
  else if (t === 'series') museumViz.fourier(el, ctrls, labels)
  else if (t === 'multivariable') museumViz.gradient(el, ctrls)
}
</script>

<style scoped>
.tab-content { max-width:800px; margin:0 auto; padding:32px 40px; }
.exhibit-actions { position:fixed; top:100px; right:20px; display:flex; flex-direction:column; gap:8px; z-index:20; }
.action-btn { width:40px; height:40px; border-radius:50%; border:1px solid var(--border); background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-size:18px; display:flex; align-items:center; justify-content:center; transition:all 0.15s; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
.action-btn:hover { border-color:var(--accent); color:var(--accent); }
.action-btn.active { color:var(--accent-warm); }
.tab-content :deep(.katex-display) { margin:16px 0; overflow-x:auto; overflow-y:hidden; }
.tab-content :deep(table) { width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; }
.tab-content :deep(th), .tab-content :deep(td) { border:1px solid var(--border); padding:8px 12px; text-align:left; }
.tab-content :deep(th) { background:var(--bg-nav); font-weight:600; }
.tab-content :deep(tr:nth-child(even)) { background:var(--bg-even); }
.tab-content :deep(tr:hover) { background:var(--bg-hover); }
.tab-content :deep(blockquote) { border-left:3px solid var(--accent); margin:16px 0; padding:8px 16px; background:var(--bg-nav); border-radius:0 var(--radius) var(--radius) 0; color:var(--text-secondary); }
.tab-content :deep(code) { font-family:var(--font-mono); font-size:0.9em; background:var(--bg-nav); padding:2px 5px; border-radius:3px; }
.tab-content :deep(pre) { background:#1a1d22; border:1px solid var(--border); border-radius:8px; padding:16px 20px; overflow-x:auto; margin:16px 0; }
.tab-content :deep(pre code) { background:none; padding:0; color:var(--text-muted); }
.viz-wrap { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:20px; margin:16px 0; }
.viz-wrap h4 { margin-bottom:12px; }
.viz-plot { width:100%; height:420px; }
.viz-ctrls { text-align:center; margin-top:8px; font-size:13px; }
@media(max-width:768px) { .tab-content { padding:20px 16px; } }
</style>
