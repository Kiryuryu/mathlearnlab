<template>
  <div class="workshop-layout">
    <div class="sidebar">
      <h2>{{ $t('workshop.title') }}</h2>
      <div class="mode-tabs">
        <button v-for="m in modes" :key="m.key" :class="{ active: mode === m.key }" @click="mode = m.key">{{ $t(m.label) }}</button>
      </div>
      <textarea v-if="mode !== 'ai'" v-model="funcInput" :placeholder="$t('workshop.placeholder')" rows="3" class="func-input"></textarea>
      <div v-if="mode === '2d'" class="opts">
        <label>x: <input v-model.number="xMin" type="number" style="width:60px"> ~ <input v-model.number="xMax" type="number" style="width:60px"></label>
      </div>
      <textarea v-if="mode === 'ai'" v-model="aiDesc" :placeholder="$t('workshop.aiPlaceholder')" rows="3" class="func-input"></textarea>
      <button class="plot-btn" @click="plot">{{ $t('workshop.plot') }}</button>
      <div class="presets">
        <div class="preset-group" v-for="g in presets" :key="g.label">
          <div class="preset-label">{{ g.label }}</div>
          <button v-for="p in g.items" :key="p" @click="funcInput=p; if(g.setMode) mode=g.setMode" class="preset-btn">{{ p }}</button>
        </div>
      </div>
    </div>
    <div class="main">
      <div ref="plotEl" class="plot-area">
        <div class="placeholder" v-if="!plotted">{{ $t('workshop.placeholder') }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'

const { locale } = useI18n()
const mode = ref('2d')
const funcInput = ref('sin(x)')
const aiDesc = ref('')
const xMin = ref(-6), xMax = ref(6)
const plotEl = ref(null)
const plotted = ref(false)

const modes = [
  { key: '2d', label: 'workshop.mode2d' },
  { key: '3d', label: 'workshop.mode3d' },
  { key: 'vector', label: 'workshop.modeVector' },
  { key: 'ai', label: 'workshop.modeAi' },
]

const presetDefs = [
  { key: 'basic', items: ['sin(x)','x^2','x^3-3*x','1/x','exp(x)','abs(x)','sqrt(x)'] },
  { key: 'limits', items: ['(x^2-1)/(x-1)','sin(x)/x','(1+1/x)^x'] },
  { key: 'series', items: ['sin(x)\nsin(x)+sin(3*x)/3\nsin(x)+sin(3*x)/3+sin(5*x)/5'] },
  { key: '3d', items: ['x^2+y^2','x^2-y^2','sin(sqrt(x^2+y^2))','exp(-(x^2+y^2))'], setMode: '3d' },
  { key: 'vector', items: ['-y,x','x,y','-x,-y','1,0'], setMode: 'vector' },
]
const presets = computed(() => presetDefs.map(g => ({
  ...g,
  label: locale.value === 'en'
    ? ({ basic: 'Basic', limits: 'Limits', series: 'Series', '3d': '3D', vector: 'Vector Field' })[g.key] || g.key
    : ({ basic: '基础', limits: '极限', series: '级数', '3d': '3D', vector: '向量场' })[g.key] || g.key,
})))

function ev1(expr, x) {
  const s = expr.replace(/\^/g,'**').replace(/sin\(/g,'Math.sin(').replace(/cos\(/g,'Math.cos(').replace(/exp\(/g,'Math.exp(').replace(/sqrt\(/g,'Math.sqrt(').replace(/abs\(/g,'Math.abs(').replace(/pi/gi,'Math.PI').replace(/\be\b/gi,'Math.E')
  return Function('x','return '+s)(x)
}
function ev2(expr, x, y) {
  const s = expr.replace(/\^/g,'**').replace(/sin\(/g,'Math.sin(').replace(/cos\(/g,'Math.cos(').replace(/exp\(/g,'Math.exp(').replace(/sqrt\(/g,'Math.sqrt(').replace(/abs\(/g,'Math.abs(').replace(/pi/gi,'Math.PI')
  return Function('x','y','return '+s)(x, y)
}

async function plot() {
  if (!plotEl.value) return
  try { await loadPlotly() } catch { return }
  plotted.value = true
  const el = plotEl.value
  const funcs = funcInput.value.trim().split('\n').filter(Boolean)
  if (!funcs.length) return

  if (mode.value === '2d') {
    const N = 500, traces = []
    funcs.forEach(f => {
      const xs = [], ys = []
      for (let i = 0; i <= N; i++) { const xv = xMin.value + (xMax.value-xMin.value)*i/N; xs.push(xv); try { const yv = ev1(f, xv); ys.push(isFinite(yv)?yv:null) } catch(e) { ys.push(null) } }
      traces.push({ x: xs, y: ys, type: 'scatter', mode: 'lines', name: f, line: { width: 2 } })
    })
    Plotly.react(el, traces, { title: funcs.join(', '), xaxis:{title:'x'}, yaxis:{title:'y'}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)' }, { responsive: true })
  } else if (mode.value === '3d') {
    const N = 60, xs = [], ys = []
    for (let i = 0; i < N; i++) { xs.push(-5+10*i/(N-1)); ys.push(-5+10*i/(N-1)) }
    const traces = []
    funcs.forEach(f => {
      const zs = []
      for (let i = 0; i < N; i++) { const row = []; for (let j = 0; j < N; j++) { try { const z = ev2(f, xs[i], ys[j]); row.push(isFinite(z)?z:null) } catch(e) { row.push(null) } } zs.push(row) }
      traces.push({ x: xs, y: ys, z: zs, type: 'surface', colorscale: 'Viridis', showscale: true })
    })
    Plotly.react(el, traces, { title: funcs.join(', '), scene:{xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'z'}}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)' }, { responsive: true })
  } else if (mode.value === 'vector') {
    const parts = funcs[0].split(',').map(s => s.trim())
    if (parts.length < 2) return
    const [Fx, Fy] = parts, N = 20, pts = []
    for (let i = 0; i < N; i++) { for (let j = 0; j < N; j++) { const x = -5+10*i/(N-1), y = -5+10*j/(N-1); try { const u = ev2(Fx,x,y), v = ev2(Fy,x,y); if (isFinite(u)&&isFinite(v)) pts.push({ x, y, u, v, m: Math.sqrt(u*u+v*v) }) } catch(e) { console.warn('Vector eval failed', e) } } }
    const maxM = Math.max(...pts.map(p => p.m)) || 1
    Plotly.react(el, [{ x: pts.map(p => p.x), y: pts.map(p => p.y), u: pts.map(p => p.u), v: pts.map(p => p.v), type: 'scatter', mode: 'markers', marker: { size: 8, color: pts.map(p => p.m), colorscale: 'Viridis', showscale: true } }], { title: `Vector field: (${Fx}, ${Fy})`, xaxis:{range:[-5.5,5.5]}, yaxis:{range:[-5.5,5.5],scaleanchor:'x'}, margin:{t:40,r:20,b:50,l:50}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)' }, { responsive: true })
  }
}
</script>

<style scoped>
.workshop-layout { display:flex; height:calc(100vh - 90px); }
.sidebar { width:340px; min-width:340px; padding:24px 20px; overflow-y:auto; border-right:1px solid var(--border); background:var(--bg-nav); }
.main { flex:1; overflow-y:auto; padding:24px; }
.mode-tabs { display:flex; gap:0; border:1px solid var(--border); border-radius:8px; overflow:hidden; margin:12px 0; }
.mode-tabs button { flex:1; padding:8px 10px; font-size:11px; border:none; background:var(--bg-card); color:var(--text-secondary); cursor:pointer; border-right:1px solid var(--border); }
.mode-tabs button:last-child { border-right:none; }
.mode-tabs button.active { background:var(--accent); color:#fff; }
.func-input { width:100%; padding:10px; border:1px solid var(--border); border-radius:8px; font-family:monospace; font-size:13px; resize:vertical; background:var(--bg-input); color:var(--text-primary); }
.opts { margin-top:8px; font-size:12px; color:var(--text-secondary); }
.plot-btn { width:100%; padding:10px; margin-top:12px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer; }
.presets { margin-top:16px; }
.preset-label { font-size:11px; color:var(--text-muted); margin-bottom:4px; }
.preset-btn { padding:3px 9px; font-size:11px; border:1px solid var(--border); border-radius:12px; background:var(--bg-card); color:var(--text-secondary); cursor:pointer; font-family:monospace; margin:2px; }
.plot-area { min-height:500px; background:var(--bg-card); border:1px solid var(--border); border-radius:12px; position:relative; overflow:hidden; }
.placeholder { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-size:15px; }
@media(max-width:900px) { .workshop-layout { flex-direction:column; } .sidebar { width:100%; min-width:0; border-right:none; border-bottom:1px solid var(--border); max-height:50vh; } }
</style>
