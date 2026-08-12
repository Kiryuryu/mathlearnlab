<template>
  <div class="exhibit-page" v-if="exhibit">
    <nav class="crumbs" aria-label="Breadcrumb">
      <router-link to="/" class="crumb">{{ t('exhibit.crumbHome') }}</router-link>
      <span class="crumb-sep">/</span>
      <router-link to="/gaoshu" class="crumb">{{ t('exhibit.crumbExhibits') }}</router-link>
      <span class="crumb-sep">/</span>
      <span class="crumb current">{{ exhibitName }}</span>
    </nav>
    <ExhibitHero
      :name="exhibitName"
      :eyebrow="heroEyebrow"
      :chapter="chapterRoman"
      :big-q="exhibitBigQ"
      :historian="exhibit.historian"
    />
    <nav class="tabs" aria-label="Exhibit sections">
      <a
        v-for="tk in tabs"
        :key="tk.key"
        :class="['tab', { active: activeTab === tk.key }]"
        @click.prevent="changeTab(tk.key)"
      >{{ t('exhibit.' + tk.key) }}</a>
    </nav>
    <div class="tab-content">
      <div class="exhibit-actions">
        <button class="action-btn" @click="shareLink" :title="$t('common.share')">🔗</button>
        <button class="action-btn" @click="toggleBookmark" :title="isBookmarked ? $t('common.unbookmark') : $t('common.bookmark')">
          {{ isBookmarked ? '★' : '☆' }}
        </button>
      </div>
      <ol v-if="toc.length" class="toc" aria-label="On this page">
        <li class="toc-title">{{ t('exhibit.onThisPage') }}</li>
        <li v-for="h in toc" :key="h.id" class="toc-item">
          <a :href="'#' + h.id" @click.prevent="scrollToHeading(h.id)">{{ h.text }}</a>
        </li>
      </ol>
      <div v-if="loading" class="skeleton-wrap">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text short"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-block"></div>
      </div>
      <div v-else v-html="content" ref="contentEl" class="content-fade"></div>
      <div class="viz-wrap" v-if="activeTab === 'explore'" :data-viz-ready="vizReady ? '1' : '0'">
        <h4>{{ $t('exhibit.explore') }}</h4>
        <div ref="vizPlot" class="viz-plot"></div>
        <div ref="vizControls" class="viz-ctrls"></div>
        <EulerSpiral v-if="topic === 'derivatives'" />
        <ManimVideo
          v-if="manimVideo"
          :src="manimVideo.src"
          :poster="manimVideo.poster"
          :title="manimVideo.title"
          :desc="manimVideo.desc"
        />
      </div>
      <nav class="exhibit-pager" v-if="siblings.length">
        <router-link
          v-if="prevTopic"
          :to="'/exhibit/' + prevTopic"
          class="pager-link prev"
          :class="{ 'pager-text': !hasSymbol(prevTopic) }"
        ><span class="pager-label">{{ t('exhibit.prevExhibit') }}</span><span class="pager-name">{{ symbolFor(prevTopic) }} {{ nameFor(prevTopic) }}</span></router-link>
        <router-link
          v-if="nextTopic"
          :to="'/exhibit/' + nextTopic"
          class="pager-link next"
        ><span class="pager-label">{{ t('exhibit.nextExhibit') }}</span><span class="pager-name">{{ symbolFor(nextTopic) }} {{ nameFor(nextTopic) }}</span></router-link>
        <router-link to="/gaoshu" class="pager-link back">{{ t('exhibit.backToExhibits') }}</router-link>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'
import { museumViz } from '@/utils/viz'
import { renderMarkdown } from '@/utils/markdown'
import { useAuth } from '@/stores/auth'
import { useToast } from '@/utils/toast'
import { apiFetch } from '@/utils/api'
import ExhibitHero from '@/components/ExhibitHero.vue'
import EulerSpiral from '@/components/EulerSpiral.vue'
import ManimVideo from '@/components/ManimVideo.vue'

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
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
const toc = ref([])
const exhibitsMeta = ref({})

const ROMANS = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ']

// Ordered sibling exhibits within the same section (by content_data order).
const siblings = computed(() => {
  const metas = exhibitsMeta.value.exhibits || {}
  return Object.entries(metas)
    .filter(([, ex]) => ex.parent && ex.order)
    .sort((a, b) => a[1].order - b[1].order)
    .map(([key, ex]) => ({ key, ex }))
})
const idx = computed(() => siblings.value.findIndex(s => s.key === topic.value))
const prevTopic = computed(() => idx.value > 0 ? siblings.value[idx.value - 1].key : '')
const nextTopic = computed(() => idx.value >= 0 && idx.value < siblings.value.length - 1 ? siblings.value[idx.value + 1].key : '')
const chapterRoman = computed(() => {
  const ex = exhibitsMeta.value.exhibits?.[topic.value]
  return ex?.order ? ROMANS[ex.order] || '' : ''
})
function symbolFor(key) {
  return exhibitsMeta.value.exhibits?.[key]?.icon || ''
}
function hasSymbol(key) {
  return !!symbolFor(key)
}
function nameFor(key) {
  const ex = exhibitsMeta.value.exhibits?.[key]
  if (!ex) return key
  return locale.value === 'en' && ex.en ? ex.en : ex.zh
}

// Switching tabs keeps the URL in sync so links can be shared/bookmarked with the right tab.
function changeTab(tab) {
  activeTab.value = tab
  router.replace({ query: { ...route.query, tab } })
}

// Manim beauty animations embedded per exhibit (explore tab)
const manimVideo = computed(() => {
  const base = '/static/videos/'
  const V = {
    derivatives: {
      src: base + 'EulerIdentity.mp4', poster: base + 'EulerIdentity.jpg',
      title: t('exhibit.animEuler'), desc: t('exhibit.animEulerDesc'),
    },
    integrals: {
      src: base + 'RiemannSum.mp4', poster: base + 'RiemannSum.jpg',
      title: t('exhibit.animRiemann'), desc: t('exhibit.animRiemannDesc'),
    },
    series: {
      src: base + 'FourierSeries.mp4', poster: base + 'FourierSeries.jpg',
      title: t('exhibit.animFourier'), desc: t('exhibit.animFourierDesc'),
    },
  }
  return V[topic.value] || null
})

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
const heroEyebrow = computed(() => t('exhibit.museum'))
const exhibitBigQ = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.big_question_en ? exhibit.value.big_question_en : exhibit.value.big_question
})

async function loadContent() {
  loading.value = true
  try {
    // Load exhibit metadata + section ordering (for pager/chapter number)
    const er = await apiFetch('/api/museum/exhibits')
    const ed = await er.json()
    exhibitsMeta.value = ed
    exhibit.value = ed.exhibits[topic.value] || { zh: topic.value }
    // Every tab — including concept — loads its own focused short article.
    const path = `exhibits/${topic.value}/${activeTab.value}`
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
  buildToc()
}

// Build an in-page table of contents from the rendered ## headings.
function buildToc() {
  toc.value = []
  const el = contentEl.value
  if (!el) return
  const heads = el.querySelectorAll('h2')
  if (!heads.length) return
  heads.forEach((h, i) => {
    const id = 'sec-' + i
    h.id = id
    toc.value.push({ id, text: h.textContent.trim() })
  })
}

function scrollToHeading(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

watch([topic, activeTab, locale], loadContent, { immediate: true })

// Keep tab state in sync when URL changes via back/forward or direct link.
watch(() => route.query.tab, (tab) => {
  if (tab && tab !== activeTab.value) activeTab.value = tab
})

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

// Plotly viz (lazy-loaded on demand). Inlined directly (no helper function) so the
// build's tree-shaker cannot drop the Plotly.react side effects.
let vizTimer = null
let vizTopic = null
const vizReady = ref(false)
function vizLabels() {
  return { epsilon: t('exhibit.vizEpsilon'), tangent: t('exhibit.vizTangent'), rectangles: t('exhibit.vizRectangles'), harmonics: t('exhibit.vizHarmonics') }
}
async function runViz() {
  if (activeTab.value !== 'explore') return
  clearTimeout(vizTimer)
  vizTimer = setTimeout(async () => {
    try {
      await loadPlotly()
      await nextTick()
      const el = vizPlot.value
      const ctrls = vizControls.value
      if (!el) { runViz(); return }
      const tp = topic.value
      if (vizTopic === tp) return
      vizTopic = tp
      const lbl = vizLabels()
      if (tp === 'limits') { museumViz.epsilon(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'derivatives') { museumViz.tangent(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'integrals') { museumViz.riemann(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'series') { museumViz.fourier(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'multivariable') { museumViz.gradient(el, ctrls, window.Plotly) }
      vizReady.value = true
    } catch(e) { console.warn('Plotly init failed', e) }
  }, 120)
}
watch([activeTab, loading], runViz)
watch(topic, () => { vizTopic = null; runViz() })
onMounted(() => { runViz(); loadBookmarks() })
</script>

<style scoped>
.crumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  max-width: 800px;
  margin: 0 auto;
  padding: 14px 40px 0;
  font-size: 12px;
  color: var(--text-muted);
}
.crumb { color: var(--text-muted); text-decoration: none; }
.crumb:hover { color: var(--accent); text-decoration: none; }
.crumb.current { color: var(--text-secondary); }
.crumb-sep { color: var(--border); }
.tab-content { max-width:800px; margin:0 auto; padding:32px 40px; }
.tabs { display:flex; justify-content:center; gap:0; border-bottom:1px solid var(--border); background:var(--bg-nav); position:sticky; top:0; z-index:10; }
.tab { padding:12px 20px; font-size:14px; color:var(--text-secondary); text-decoration:none; border-bottom:2px solid transparent; transition:all 0.15s; cursor:pointer; }
.tab:hover { color:var(--accent); }
.tab.active { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
@media(max-width:768px) { .crumbs { padding: 12px 16px 0; } .tabs { overflow-x:auto; justify-content:flex-start; } .tab { padding:10px 14px; font-size:13px; white-space:nowrap; } }
.exhibit-actions { position:fixed; top:100px; right:20px; display:flex; flex-direction:column; gap:8px; z-index:20; }
.action-btn { width:40px; height:40px; border-radius:50%; border:1px solid var(--border); background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-size:18px; display:flex; align-items:center; justify-content:center; transition:all 0.15s; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
.action-btn:hover { border-color:var(--accent); color:var(--accent); }
.action-btn.active { color:var(--accent-warm); }

/* In-page table of contents */
.toc {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
  margin: 0 0 20px;
  padding: 12px 16px;
  background: var(--bg-nav);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 13px;
}
.toc-title { flex-basis: 100%; font-family: var(--font-heading); font-weight: 600; color: var(--text-muted); font-size: 12px; letter-spacing: 0.04em; margin-bottom: 2px; }
.toc-item a { color: var(--text-secondary); text-decoration: none; padding: 2px 8px; border-radius: 12px; border: 1px solid var(--border); background: var(--bg-card); transition: all 0.15s; }
.toc-item a:hover { color: var(--accent); border-color: var(--accent); text-decoration: none; }

/* Prev / next pager */
.exhibit-pager {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}
.pager-link {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-card);
  color: var(--text-primary);
  text-decoration: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.pager-link:hover { border-color: var(--accent); box-shadow: var(--shadow-elevated); text-decoration: none; }
.pager-link.next { text-align: right; }
.pager-label { font-size: 11px; color: var(--text-muted); letter-spacing: 0.04em; }
.pager-name { font-family: var(--font-heading); font-size: 15px; }
.pager-link.back {
  flex: none;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  font-size: 14px;
}
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
@media(max-width:768px) { .tab-content { padding:20px 16px; } .exhibit-pager { flex-direction: column; } }
</style>
