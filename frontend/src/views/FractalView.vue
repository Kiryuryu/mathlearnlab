<template>
  <div class="fractal-page">
    <h1>{{ $t('fractal.title') }}</h1>
    <p class="sub">{{ $t('fractal.subtitle') }}</p>
    <div class="fractal-toolbar">
      <button :class="{ active: mode === 'mandelbrot' }" @click="setMode('mandelbrot')">{{ $t('fractal.mandelbrot') }}</button>
      <button :class="{ active: mode === 'julia' }" @click="setMode('julia')">{{ $t('fractal.julia') }}</button>
      <button :class="{ active: mode === 'lorenz' }" @click="setMode('lorenz')">{{ $t('fractal.lorenz') }}</button>
      <span class="hint" v-if="mode !== 'lorenz'">{{ $t('fractal.hint') }}</span>
      <button @click="resetView">{{ $t('fractal.reset') }}</button>
    </div>
    <canvas v-show="mode !== 'lorenz'" ref="canvasEl" class="fractal-canvas" @wheel="onWheel" @mousedown="onMouseDown" @click="onClick"></canvas>
    <div v-show="mode === 'lorenz'" ref="lorenzEl" class="lorenz-plot"></div>
    <div class="info" v-if="mode !== 'lorenz'">
      <span>{{ $t('fractal.center') }}: {{ cx.toFixed(6) }}+{{ cy.toFixed(6) }}i, {{ $t('fractal.range') }}: {{ range.toExponential(2) }}</span>
      <span>{{ $t('fractal.iter') }}: <input v-model.number="maxIter" @change="redraw" type="number" min="20" max="500" step="10" style="width:60px"></span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'

const { t, locale } = useI18n()

const mode = ref('mandelbrot')
const canvasEl = ref(null)
const lorenzEl = ref(null)
const maxIter = ref(100)
const cx = ref(-0.5), cy = ref(0), range = ref(3)
const juliaCx = ref(-0.7), juliaCy = ref(0.27)
let dragging = false, dragX = 0, dragY = 0, needsRedraw = false

function setMode(m) {
  mode.value = m
  if (m === 'julia') { cx.value = 0; cy.value = 0; range.value = 3 }
  nextTick(() => {
    if (m === 'lorenz') drawLorenz()
    else redraw()
  })
}

function resetView() { cx.value = -0.5; cy.value = 0; range.value = 3; redraw() }

function redraw() {
  const canvas = canvasEl.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  const w = Math.floor(rect.width) || 600
  const h = Math.min(w, 600)
  canvas.width = w; canvas.height = h
  const ctx = canvas.getContext('2d')
  const img = ctx.createImageData(w, h)
  const mi = maxIter.value

  for (let py = 0; py < h; py++) {
    for (let px = 0; px < w; px++) {
      const x0 = cx.value + (px/w - 0.5) * range.value * w/h
      const y0 = cy.value + (py/h - 0.5) * range.value
      let iter, x, y

      if (mode.value === 'mandelbrot') {
        x = 0; y = 0
        for (iter = 0; iter < mi; iter++) {
          const xt = x*x - y*y + x0; y = 2*x*y + y0; x = xt
          if (x*x + y*y > 4) break
        }
      } else {
        x = x0; y = y0
        for (iter = 0; iter < mi; iter++) {
          const xt = x*x - y*y + juliaCx.value; y = 2*x*y + juliaCy.value; x = xt
          if (x*x + y*y > 4) break
        }
      }

      const idx = (py*w + px)*4
      if (iter === mi) { img.data[idx]=15; img.data[idx+1]=10; img.data[idx+2]=30; img.data[idx+3]=255 }
      else {
        const t = iter/mi
        img.data[idx]=Math.min(255,Math.floor(9*(1-t)*t*t*t*255)+20)
        img.data[idx+1]=Math.min(255,Math.floor(15*(1-t)*(1-t)*t*t*255)+10)
        img.data[idx+2]=Math.min(255,Math.floor(8.5*(1-t)*(1-t)*(1-t)*t*255)+40)
        img.data[idx+3]=255
      }
    }
  }
  ctx.putImageData(img, 0, 0)
}

async function drawLorenz() {
  if (!lorenzEl.value) return
  try { await loadPlotly() } catch { return }
  const sigma=10, rho=28, beta=8/3, dt=0.003
  let x=0.1, y=0, z=0
  const xs=[], ys=[], zs=[]
  for(let i=0;i<15000;i++){
    x += sigma*(y-x)*dt; y += (x*(rho-z)-y)*dt; z += (x*y-beta*z)*dt
    if(i>1000){ xs.push(x); ys.push(y); zs.push(z) }
  }
  Plotly.newPlot(lorenzEl.value, [{
    x:xs, y:ys, z:zs, type:'scatter3d', mode:'lines',
    line:{width:2, color:xs.map((_,i)=>i/xs.length), colorscale:'Viridis'}
  }], {
    title: t('fractal.lorenzTitle'),
    scene:{xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'z'}},
    margin:{t:40,r:20,b:40,l:20}, paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true})
}

// Mouse events
let wheelAccum = 0
let _onMouseMove, _onMouseUp, _checkInt
onMounted(() => {
  let tries = 0
  _checkInt = setInterval(() => {
    if (canvasEl.value) { clearInterval(_checkInt); nextTick(() => redraw()); return }
    if (++tries > 25) clearInterval(_checkInt)
  }, 200)
  _onMouseMove = onMouseMove
  _onMouseUp = () => { dragging = false }
  window.addEventListener('mousemove', _onMouseMove)
  window.addEventListener('mouseup', _onMouseUp)
})
onUnmounted(() => {
  if (_checkInt) clearInterval(_checkInt)
  if (_onMouseMove) window.removeEventListener('mousemove', _onMouseMove)
  if (_onMouseUp) window.removeEventListener('mouseup', _onMouseUp)
})

function onWheel(e) {
  e.preventDefault()
  wheelAccum += e.deltaY
  if (Math.abs(wheelAccum) < (Math.abs(e.deltaY) > 50 ? 0 : 10)) return
  const zoom = wheelAccum > 0 ? 1.3 : 1/1.3
  const rect = canvasEl.value.getBoundingClientRect()
  const mx = cx.value + ((e.clientX-rect.left)/rect.width - 0.5) * range.value * rect.width/rect.height
  const my = cy.value + ((e.clientY-rect.top)/rect.height - 0.5) * range.value
  range.value *= zoom
  cx.value = mx + (cx.value - mx) * zoom
  cy.value = my + (cy.value - my) * zoom
  wheelAccum = 0
  redraw()
}

function onMouseDown(e) { if (e.target === canvasEl.value) { dragging = true; dragX = e.clientX; dragY = e.clientY } }
function onMouseMove(e) {
  if (!dragging) return
  const rect = canvasEl.value.getBoundingClientRect()
  const dx = (e.clientX - dragX)/rect.width * range.value * rect.width/rect.height
  const dy = (e.clientY - dragY)/rect.height * range.value
  cx.value -= dx; cy.value -= dy
  dragX = e.clientX; dragY = e.clientY
  if (!needsRedraw) { needsRedraw = true; requestAnimationFrame(() => { redraw(); needsRedraw = false }) }
}
function onClick(e) {
  if (Math.abs(e.clientX-dragX) > 2 || Math.abs(e.clientY-dragY) > 2) return
  if (mode.value !== 'julia') return
  const rect = canvasEl.value.getBoundingClientRect()
  juliaCx.value = cx.value + ((e.clientX-rect.left)/rect.width - 0.5) * range.value * rect.width/rect.height
  juliaCy.value = cy.value + ((e.clientY-rect.top)/rect.height - 0.5) * range.value
  redraw()
}

</script>

<style scoped>
.fractal-page { max-width:1100px; margin:0 auto; padding:32px 20px; }
.fractal-page h1 { font-size:28px; }
.sub { color:var(--text-secondary); margin-bottom:16px; }
.fractal-toolbar { display:flex; gap:8px; margin:12px 0; flex-wrap:wrap; align-items:center; }
.fractal-toolbar button { padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-size:12px; cursor:pointer; background:var(--bg-card); color:var(--text-secondary); }
.fractal-toolbar button.active { background:var(--accent); color:#fff; }
.hint { font-size:12px; color:var(--text-muted); margin-left:8px; }
.fractal-canvas { width:100%; aspect-ratio:1; max-height:600px; border:1px solid var(--border); border-radius:8px; cursor:crosshair; }
.lorenz-plot { width:100%; height:500px; border:1px solid var(--border); border-radius:8px; }
.info { margin-top:8px; font-size:12px; color:var(--text-muted); display:flex; gap:16px; align-items:center; }
</style>
