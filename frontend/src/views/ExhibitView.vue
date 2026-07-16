<template>
  <div class="exhibit-page" v-if="exhibit">
    <div class="exhibit-hero" :style="{background: heroBg}">
      <h1>{{ exhibitName }}</h1>
      <p class="big-q">{{ exhibitBigQ }}</p>
      <p class="historian">{{ $t('exhibit.historian') }}{{ exhibit.historian }}</p>
      <p class="beauty">{{ exhibitBeauty }}</p>
    </div>
    <nav class="tabs">
      <a v-for="t in tabs" :key="t.key" :href="'?tab='+t.key" :class="['tab', { active: activeTab === t.key }]" @click.prevent="activeTab = t.key">{{ $t('exhibit.' + t.key) }}</a>
    </nav>
    <div class="tab-content">
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
        <div ref="vizPlot" class="viz-plot"></div>
        <div ref="vizControls" class="viz-ctrls"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'
import { renderMarkdown } from '@/utils/markdown'

const { t, locale } = useI18n()
const route = useRoute()
const topic = computed(() => route.params.topic)
const activeTab = ref(route.query.tab || 'concept')
const exhibit = ref(null)
const content = ref('')
const loading = ref(false)
const vizPlot = ref(null)
const vizControls = ref(null)
const contentEl = ref(null)

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
}
const heroBg = computed(() => heroBgs[topic.value] || 'linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)')

async function loadContent() {
  loading.value = true
  try {
    // Load exhibit info
    const er = await fetch('/api/museum/exhibits')
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
    const cr = await fetch(`/api/content/${path}?lang=${lang}`)
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
  if (t === 'limits') MuseumVizEpsilon(el)
  else if (t === 'derivatives') MuseumVizTangent(el)
  else if (t === 'integrals') MuseumVizRiemann(el)
  else if (t === 'series') MuseumVizFourier(el)
  else if (t === 'multivariable') MuseumVizGradient(el)
}

// Inline viz functions (ported from museum_viz.js)
function MuseumVizEpsilon(el) {
  let epsVal = 0.5
  function render() {
    const eps = epsVal, x0 = 1, L = 2, delta = eps, margin = Math.max(3*eps, 1.5)
    const xs = [], fx = []
    for (let i = 0; i <= 200; i++) { const x = x0 - margin + 2*margin*i/200; xs.push(x); fx.push(x === x0 ? null : x+1) }
    Plotly.react(el, [
      { x: xs, y: fx, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } },
      { x: [x0], y: [L], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10, symbol: 'x' } },
      { x: [x0-margin,x0+margin], y: [L+eps,L+eps], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } },
      { x: [x0-margin,x0+margin], y: [L-eps,L-eps], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } },
      { x: [x0-delta,x0-delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } },
      { x: [x0+delta,x0+delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } },
    ], { title: 'ε-δ: ε='+eps.toFixed(2)+', δ='+delta.toFixed(2), margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  const ctrls = vizControls.value
  if (ctrls) ctrls.innerHTML = (locale.value === 'en'
    ? '<label>Drag ε: <span id="epsVal">0.50</span></label><br><input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="0.5" style="width:260px">'
    : '<label>拖动 ε: <span id="epsVal">0.50</span></label><br><input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="0.5" style="width:260px">')
  setTimeout(() => {
    const s = document.getElementById('epsSlider')
    if (s) s.oninput = function() { epsVal = parseFloat(this.value); document.getElementById('epsVal').textContent = epsVal.toFixed(2); render() }
  }, 100)
  render()
}
function MuseumVizTangent(el) {
  let tanA = 0
  function f(x) { return x*x }; function fp(x) { return 2*x }
  function render() {
    const a = tanA, xs = [], ys = []
    for (let i = 0; i <= 200; i++) { const x = -3 + 6*i/200; xs.push(x); ys.push(f(x)) }
    Plotly.react(el, [
      { x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } },
      { x: [a-1.5,a+1.5], y: [f(a)+fp(a)*(-1.5), f(a)+fp(a)*1.5], type: 'scatter', mode: 'lines', line: { color: '#a45050', width: 2, dash: 'dash' } },
      { x: [a], y: [f(a)], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10 } },
    ], { title: 'f\'(x)='+fp(a).toFixed(1)+' at x='+a.toFixed(1), xaxis:{range:[-3,3]}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  const ctrls = vizControls.value
  if (ctrls) ctrls.innerHTML = (locale.value === 'en'
    ? '<label>Tangent x = <span id="tanVal">0.0</span></label><br><input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="0" style="width:260px">'
    : '<label>切点 x = <span id="tanVal">0.0</span></label><br><input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="0" style="width:260px">')
  setTimeout(() => {
    const s = document.getElementById('tanSlider')
    if (s) s.oninput = function() { tanA = parseFloat(this.value); document.getElementById('tanVal').textContent = tanA.toFixed(1); render() }
  }, 100)
  render()
}
function MuseumVizRiemann(el) {
  let riemN = 10
  function f(x) { return x*x }
  function render() {
    const n = riemN, a = 0, b = 2, dx = (b-a)/n
    let area = 0
    const xs = [], ys = [], rx = [], ry = []
    for (let i = 0; i <= 200; i++) { const x = a-0.5+(b-a+1)*i/200; xs.push(x); ys.push(f(x)) }
    for (let i = 0; i < n; i++) { const xL = a+i*dx, xR = xL+dx, yH = f(xL); area += dx*yH; rx.push(xL,xR,xR,xL,xL,null); ry.push(0,0,yH,yH,0,null) }
    Plotly.react(el, [
      { x: xs, y: ys, type: 'scatter', mode: 'lines', fill: 'tozeroy', fillcolor: 'rgba(74,106,138,0.1)', line: { color: '#4a6a8a', width: 2 } },
      { x: rx, y: ry, type: 'scatter', mode: 'lines', fill: 'toself', fillcolor: 'rgba(107,94,74,0.3)', line: { color: '#6b5e4a', width: 1 } },
    ], { title: 'Riemann: n='+n+', ≈'+area.toFixed(3)+' (exact:'+(8/3).toFixed(3)+')', margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  const ctrls = vizControls.value
  if (ctrls) ctrls.innerHTML = (locale.value === 'en'
    ? '<label>Rectangles n = <span id="nVal">10</span></label><br><input type="range" id="nSlider" min="2" max="100" step="1" value="10" style="width:260px">'
    : '<label>矩形数 n = <span id="nVal">10</span></label><br><input type="range" id="nSlider" min="2" max="100" step="1" value="10" style="width:260px">')
  setTimeout(() => {
    const s = document.getElementById('nSlider')
    if (s) s.oninput = function() { riemN = parseInt(this.value); document.getElementById('nVal').textContent = riemN; render() }
  }, 100)
  render()
}
function MuseumVizFourier(el) {
  let fN = 3
  function render() {
    const N = fN, xs = [], ys = []
    for (let i = 0; i <= 400; i++) { const x = -2*Math.PI+4*Math.PI*i/400; let s = 0; for (let k = 1; k <= N; k++) s += Math.sin((2*k-1)*x)/(2*k-1); xs.push(x); ys.push(4/Math.PI*s) }
    Plotly.react(el, [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } }], { title: 'Fourier: N='+N+' harmonics', xaxis:{title:'x'}, yaxis:{range:[-1.8,1.8]}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  const ctrls = vizControls.value
  if (ctrls) ctrls.innerHTML = (locale.value === 'en'
    ? '<label>Harmonics N = <span id="nFourier">3</span></label><br><input type="range" id="fourierSlider" min="1" max="20" step="1" value="3" style="width:260px">'
    : '<label>谐波数 N = <span id="nFourier">3</span></label><br><input type="range" id="fourierSlider" min="1" max="20" step="1" value="3" style="width:260px">')
  setTimeout(() => {
    const s = document.getElementById('fourierSlider')
    if (s) s.oninput = function() { fN = parseInt(this.value); document.getElementById('nFourier').textContent = fN; render() }
  }, 100)
  render()
}
function MuseumVizGradient(el) {
  function f(x,y) { return x*x + 2*y*y }
  const N = 50, xs = [], ys = [], zGrid = []
  for (let i = 0; i <= N; i++) { xs.push(-3+6*i/N); ys.push(-3+6*i/N) }
  for (let i = 0; i < xs.length; i++) { const row = []; for (let j = 0; j < ys.length; j++) row.push(f(xs[i], ys[j])); zGrid.push(row) }
  const px = [2.5], py = [2.5]
  for (let i = 0; i < 20; i++) { const x = px[px.length-1], y = py[py.length-1]; px.push(x-0.1*2*x); py.push(y-0.1*4*y) }
  const pz = px.map((_,i) => f(px[i], py[i]) + 0.2)
  Plotly.react(el, [
    { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.8, showscale: false },
    { x: px, y: py, z: pz, type: 'scatter3d', mode: 'lines+markers', marker: { size: 3, color: '#a45050' }, line: { color: '#a45050', width: 4 } }
  ], { title: 'Gradient descent: f(x,y)=x²+2y²', scene:{xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'f'}}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)' }, { responsive: true })
}
</script>

<style scoped>
.exhibit-hero { color:#fff; text-align:center; padding:60px 40px 40px; }
.exhibit-hero h1 { font-size:36px; margin:0 0 12px; }
.big-q { font-size:17px; opacity:0.8; margin-bottom:8px; }
.historian { font-size:13px; opacity:0.5; margin-bottom:16px; }
.beauty { font-size:14px; padding:10px 24px; background:rgba(255,255,255,0.1); border-radius:20px; display:inline-block; }
.tabs { display:flex; justify-content:center; gap:0; border-bottom:1px solid var(--border); background:var(--bg-nav); position:sticky; top:0; z-index:10; }
.tab { padding:12px 20px; font-size:14px; color:var(--text-secondary); text-decoration:none; border-bottom:2px solid transparent; transition:all 0.15s; }
.tab:hover { color:var(--accent); }
.tab.active { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
.tab-content { max-width:800px; margin:0 auto; padding:32px 40px; }
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
@media(max-width:768px) { .tabs { overflow-x:auto; justify-content:flex-start; } .tab { padding:10px 14px; font-size:13px; white-space:nowrap; } .tab-content { padding:20px 16px; } .exhibit-hero { padding:32px 16px; } .exhibit-hero h1 { font-size:24px; } }
</style>
