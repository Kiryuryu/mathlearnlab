<template>
  <div class="exhibit-page" v-if="exhibit">
    <nav class="crumbs" aria-label="Breadcrumb">
      <router-link to="/" class="crumb">{{ t('exhibit.crumbHome') }}</router-link>
      <span class="crumb-sep">/</span>
      <router-link :to="subjectKey ? '/subject/' + subjectKey : '/#exhibits'" class="crumb">{{ subjectName }}</router-link>
      <span class="crumb-sep">/</span>
      <span class="crumb current">{{ exhibitName }}</span>
    </nav>
    <ExhibitHero
      :name="exhibitName"
      :eyebrow="heroEyebrow"
      :chapter="chapterRoman"
      :big-q="exhibitBigQ"
      :historian="exhibit.historian"
      :mathematicians="mathematicianLinks"
    />
    <nav class="section-nav" aria-label="Sections">
      <a
        v-for="s in SECTIONS"
        :key="s"
        :class="['section-link', { active: activeSection === s }]"
        :href="'#' + s"
        @click.prevent="goToSection(s)"
      >{{ t('exhibit.' + s) }}</a>
    </nav>
    <div class="exhibit-actions">
      <button class="action-btn" @click="openGuide" :title="$t('chat.tourGuide')">🎧</button>
      <button class="action-btn" @click="shareLink" :title="$t('common.share')">🔗</button>
      <button class="action-btn" @click="toggleBookmark" :title="isBookmarked ? $t('common.unbookmark') : $t('common.bookmark')">
        {{ isBookmarked ? '★' : '☆' }}
      </button>
    </div>
    <div class="page-body">
      <section
        v-for="s in SECTIONS"
        :id="s"
        :key="s"
        class="exhibit-section"
        :ref="el => setSectionEl(s, el)"
      >
        <h2 class="section-heading">{{ t('exhibit.' + s) }}</h2>
        <div v-if="loading && !loadedSections[s]" class="skeleton-wrap">
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-text short"></div>
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-block"></div>
        </div>
        <div v-else v-html="sections[s]" class="content-fade"></div>

        <!-- Interactive block lives at the end of the explore section -->
        <div v-if="s === 'explore' && lazyViz" class="viz-wrap" :data-viz-ready="vizReady ? '1' : '0'">
          <EulerSpiral v-if="topic === 'derivatives'" />
          <ManimVideo
            v-if="manimVideo"
            :src="manimVideo.src"
            :poster="manimVideo.poster"
            :title="manimVideo.title"
            :desc="manimVideo.desc"
          />
          <div ref="vizPlot" class="viz-plot"></div>
          <div ref="vizControls" class="viz-ctrls"></div>        </div>
      </section>

      <!-- Narrative "up next" card -->
      <div v-if="nextNote" class="next-note">
        <span class="next-note-label">{{ t('exhibit.nextNoteLabel') }}</span>
        <router-link v-if="nextTopic" :to="'/exhibit/' + nextTopic" class="next-note-body">{{ nextNote }}</router-link>
      </div>

      <nav class="exhibit-pager" v-if="siblings.length">
        <router-link
          v-if="prevTopic"
          :to="'/exhibit/' + prevTopic"
          class="pager-link prev"
        ><span class="pager-label">{{ t('exhibit.prevExhibit') }}</span><span class="pager-name">{{ symbolFor(prevTopic) }} {{ nameFor(prevTopic) }}</span></router-link>
        <router-link
          v-if="nextTopic"
          :to="'/exhibit/' + nextTopic"
          class="pager-link next"
        ><span class="pager-label">{{ t('exhibit.nextExhibit') }}</span><span class="pager-name">{{ symbolFor(nextTopic) }} {{ nameFor(nextTopic) }}</span></router-link>
        <router-link :to="subjectKey ? '/subject/' + subjectKey : '/#exhibits'" class="pager-link back">{{ t('exhibit.backToExhibits') }}</router-link>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'
import { museumViz } from '@/utils/viz'
import { renderMarkdown } from '@/utils/markdown'
import { useAuth } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { useToast } from '@/utils/toast'
import { apiFetch } from '@/utils/api'
import ExhibitHero from '@/components/ExhibitHero.vue'
import EulerSpiral from '@/components/EulerSpiral.vue'
import ManimVideo from '@/components/ManimVideo.vue'

const SECTIONS = ['concept', 'applications', 'history', 'beauty', 'method', 'explore']

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuth()
const chatStore = useChatStore()
const { show: showToast } = useToast()
const topic = computed(() => route.params.topic)
const exhibit = ref(null)
const exhibitsMeta = ref({})
const sections = ref({})
const loadedSections = ref({})
const loading = ref(false)
const isBookmarked = ref(false)

const vizPlot = ref(null)
const vizControls = ref(null)
const vizReady = ref(false)
const lazyViz = ref(false)
const activeSection = ref('concept')
const sectionEls = {}

const ROMANS = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ']

function setSectionEl(s, el) {
  if (el) sectionEls[s] = el
}

// ── Exhibits metadata → chapter, siblings (within same subject), names, links ──
const subjectKey = computed(() => exhibitsMeta.value.exhibits?.[topic.value]?.parent || '')
const subjectName = computed(() => {
  const s = exhibitsMeta.value.subjects?.[subjectKey.value]
  if (!s) return t('exhibit.crumbExhibits')
  return locale.value === 'en' && s.en ? s.en : s.zh
})
const siblings = computed(() => {
  const metas = exhibitsMeta.value.exhibits || {}
  const parent = subjectKey.value
  return Object.entries(metas)
    .filter(([, ex]) => ex.parent === parent && ex.order)
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
const nextNote = computed(() => {
  const ex = exhibitsMeta.value.exhibits?.[topic.value]
  if (!ex) return ''
  return locale.value === 'en' && ex.next_note_en ? ex.next_note_en : ex.next_note || ''
})
function symbolFor(key) {
  return exhibitsMeta.value.exhibits?.[key]?.icon || ''
}
function nameFor(key) {
  const ex = exhibitsMeta.value.exhibits?.[key]
  if (!ex) return key
  return locale.value === 'en' && ex.en ? ex.en : ex.zh
}

const exhibitName = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.en ? exhibit.value.en : exhibit.value.zh
})
const heroEyebrow = computed(() => t('exhibit.museum'))
const exhibitBigQ = computed(() => {
  if (!exhibit.value) return ''
  return locale.value === 'en' && exhibit.value.big_question_en ? exhibit.value.big_question_en : exhibit.value.big_question
})
const mathematicianLinks = computed(() => {
  const keys = exhibit.value?.mathematicians || []
  const all = exhibitsMeta.value.mathematicians || {}
  return keys
    .filter(k => all[k])
    .map(k => ({ key: k, name: all[k].name, name_en: all[k].name_en }))
})

// Manim beauty animations embedded per exhibit (explore section)
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

// ── Load all six section articles in one pass ──
async function loadContent() {
  loading.value = true
  try {
    const er = await apiFetch('/api/museum/exhibits')
    const ed = await er.json()
    exhibitsMeta.value = ed
    exhibit.value = ed.exhibits[topic.value] || { zh: topic.value }
    const lang = locale.value === 'en' ? 'en' : 'zh'
    const results = await Promise.all(SECTIONS.map(async (s) => {
      try {
        const cr = await apiFetch(`/api/content/exhibits/${topic.value}/${s}?lang=${lang}`)
        const cd = await cr.json()
        return [s, cd.error ? '<p>' + cd.error + '</p>' : renderMarkdown(cd.content || '')]
      } catch {
        return [s, '<p>' + t('exhibit.loadFail') + '</p>']
      }
    }))
    sections.value = Object.fromEntries(results)
    loadedSections.value = Object.fromEntries(SECTIONS.map(s => [s, true]))
  } catch (e) {
    // metadata fetch failed — at least try content
    const lang = locale.value === 'en' ? 'en' : 'zh'
    const results = await Promise.all(SECTIONS.map(async (s) => {
      try {
        const cr = await apiFetch(`/api/content/exhibits/${topic.value}/${s}?lang=${lang}`)
        const cd = await cr.json()
        return [s, cd.error ? '<p>' + cd.error + '</p>' : renderMarkdown(cd.content || '')]
      } catch {
        return [s, '<p>' + t('exhibit.loadFail') + '</p>']
      }
    }))
    sections.value = Object.fromEntries(results)
    loadedSections.value = Object.fromEntries(SECTIONS.map(s => [s, true]))
  }
  loading.value = false
  await nextTick()
  setupScrollTracking()
  handleHashOrQuery()
}

// ── Section navigation: scroll + URL hash ──
function goToSection(s) {
  if (s === activeSection.value && isAtSection(s)) return
  const el = document.getElementById(s)
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  // Push the hash without bouncing; observer will keep activeSection in sync.
  if (route.hash !== '#' + s) {
    router.replace({ hash: '#' + s }).catch(() => {})
  }
  suppressActive = true
  setTimeout(() => { suppressActive = false }, 350)
}
function isAtSection(s) {
  const el = sectionEls[s]
  if (!el) return true
  const r = el.getBoundingClientRect()
  return Math.abs(r.top) < 8
}

// ── URL support: #anchor deep link, plus legacy ?tab= compat ──
function handleHashOrQuery() {
  const q = route.query.tab
  if (q && SECTIONS.includes(q)) {
    // Legacy tab link — drop the query, scroll to the section.
    router.replace({ query: {} }).catch(() => {})
    scrollToId(q)
    return
  }
  const h = (route.hash || '').replace(/^#/, '')
  if (h && SECTIONS.includes(h)) {
    scrollToId(h)
  }
}
function scrollToId(id) {
  nextTick(() => {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'auto', block: 'start' })
  })
}

// ── Scroll highlight + lazy viz via scroll position (IO not reliable in all embeds) ──
let scrollHandler = null
let suppressActive = false
const NAV_OFFSET = 96

function setupScrollTracking() {
  if (scrollHandler) window.removeEventListener('scroll', scrollHandler)
  scrollHandler = () => onScroll()
  window.addEventListener('scroll', scrollHandler, { passive: true })
  onScroll()
}

function onScroll() {
  // Lazy-init the interactive section when it approaches the viewport.
  if (!lazyViz.value) {
    const exploreEl = document.getElementById('explore')
    if (exploreEl && exploreEl.getBoundingClientRect().top < window.innerHeight + 300) {
      lazyViz.value = true
    }
  }
  // Highlight the section currently at the top of the reading column.
  if (suppressActive) return
  const anchor = NAV_OFFSET + 80
  let current = SECTIONS[0]
  for (const s of SECTIONS) {
    const el = document.getElementById(s)
    if (!el) continue
    const top = el.getBoundingClientRect().top
    if (top <= anchor) current = s
    else break
  }
  if (current !== activeSection.value) activeSection.value = current
}

// ── Plotly viz (lazy, tree-shaking-safe: inlined side effects must stay) ──
let vizTimer = null
let vizTopic = null
function vizLabels() {
  return { epsilon: t('exhibit.vizEpsilon'), tangent: t('exhibit.vizTangent'), rectangles: t('exhibit.vizRectangles'), harmonics: t('exhibit.vizHarmonics') }
}
async function runViz() {
  if (!lazyViz.value) return
  clearTimeout(vizTimer)
  vizTimer = setTimeout(async () => {
    try {
      await loadPlotly()
      await nextTick()
      const el = Array.isArray(vizPlot.value) ? vizPlot.value[0] : vizPlot.value
      const ctrls = Array.isArray(vizControls.value) ? vizControls.value[0] : vizControls.value
      if (!el) { runViz(); return }
      const tp = topic.value
      if (vizTopic === tp) return
      const lbl = vizLabels()
      if (tp === 'limits') { museumViz.epsilon(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'derivatives') { museumViz.tangent(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'integrals') { museumViz.riemann(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'series') { museumViz.fourier(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'multivariable') { museumViz.gradient(el, ctrls, window.Plotly) }
      vizTopic = tp
      vizReady.value = true
    } catch(e) { console.warn('Plotly init failed', e) }
  }, 120)
}
watch(lazyViz, (v) => { if (v) runViz() })
watch(topic, () => { vizTopic = null; lazyViz.value = false; vizReady.value = false; loadContent() })
watch(locale, () => { if (exhibit.value) loadContent() })

// ── Bookmarks ──
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

function openGuide() {
  chatStore.openGuide({ key: topic.value, name: exhibitName.value || topic.value })
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

// ── Init ──
loadContent()
onMounted(loadBookmarks)
onBeforeUnmount(() => {
  if (scrollHandler) window.removeEventListener('scroll', scrollHandler)
  clearTimeout(vizTimer)
})
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

.section-nav {
  display: flex;
  justify-content: center;
  gap: 0;
  border-bottom: 1px solid var(--border);
  border-top: 1px solid var(--border);
  background: var(--bg-nav);
  position: sticky;
  top: 0;
  z-index: 10;
}
.section-link {
  padding: 12px 20px;
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.15s;
  cursor: pointer;
}
.section-link:hover { color: var(--accent); text-decoration: none; }
.section-link.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
@media(max-width:768px) {
  .crumbs { padding: 12px 16px 0; }
  .section-nav { overflow-x: auto; justify-content: flex-start; -webkit-overflow-scrolling: touch; }
  .section-link { padding: 10px 14px; font-size: 13px; white-space: nowrap; }
}

.exhibit-actions { position: fixed; top: 100px; right: 20px; display: flex; flex-direction: column; gap: 8px; z-index: 20; }
.action-btn { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--border); background: var(--bg-card); color: var(--text-secondary); cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; transition: all 0.15s; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.action-btn:hover { border-color: var(--accent); color: var(--accent); }

.page-body { max-width: 800px; margin: 0 auto; padding: 0 40px 32px; }
.exhibit-section {
  scroll-margin-top: 96px;
  padding: 36px 0 8px;
  border-bottom: 1px solid var(--border);
}
.exhibit-section:last-of-type { border-bottom: none; }
.section-heading {
  font-size: 22px;
  margin: 0 0 8px;
  padding-bottom: 8px;
  border-bottom: 3px double var(--border);
  font-family: var(--font-heading);
}

.content-fade :deep(.katex-display) { margin: 16px 0; overflow-x: auto; overflow-y: hidden; }
.content-fade :deep(table) { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.content-fade :deep(th), .content-fade :deep(td) { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
.content-fade :deep(th) { background: var(--bg-nav); font-weight: 600; }
.content-fade :deep(tr:nth-child(even)) { background: var(--bg-even); }
.content-fade :deep(tr:hover) { background: var(--bg-hover); }
.content-fade :deep(blockquote) { border-left: 3px solid var(--accent); margin: 16px 0; padding: 8px 16px; background: var(--bg-nav); border-radius: 0 var(--radius) var(--radius) 0; color: var(--text-secondary); }
.content-fade :deep(code) { font-family: var(--font-mono); font-size: 0.9em; background: var(--bg-nav); padding: 2px 5px; border-radius: 3px; }
.content-fade :deep(pre) { background: #1a1d22; border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; overflow-x: auto; margin: 16px 0; }
.content-fade :deep(pre code) { background: none; padding: 0; color: var(--text-muted); }
.content-fade :deep(details) { border: 1px solid var(--border); border-radius: var(--radius); padding: 10px 14px; margin: 12px 0; background: var(--bg-card); }
.content-fade :deep(details summary) { cursor: pointer; font-weight: 600; font-family: var(--font-heading); }
.content-fade :deep(h3) { font-size: 18px; margin: 24px 0 10px; }
.content-fade :deep(p) { margin: 10px 0; }

.viz-wrap { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin: 20px 0; }
.viz-plot { width: 100%; height: 420px; }
.viz-ctrls { text-align: center; margin-top: 8px; font-size: 13px; }

/* Narrative "up next" card */
.next-note {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 32px;
  padding: 18px 20px;
  background: var(--accent-soft);
  border: 1px solid color-mix(in srgb, var(--accent) 30%, var(--border));
  border-radius: var(--radius);
}
.next-note-label {
  flex-shrink: 0;
  font-family: var(--font-heading);
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--accent);
  font-weight: 700;
  padding: 3px 10px;
  border: 1px solid var(--accent);
  border-radius: 12px;
}
.next-note-body { color: var(--text-primary); font-size: 14px; text-decoration: none; line-height: 1.7; }
.next-note-body:hover { color: var(--accent); text-decoration: none; }

.exhibit-pager {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 24px;
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
@media(max-width:768px) { .page-body { padding: 0 16px 24px; } .exhibit-pager { flex-direction: column; } }
</style>
