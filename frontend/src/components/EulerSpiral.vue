<template>
  <div class="euler-spiral">
    <div v-if="webglOk === false" class="no-webgl">⚠ WebGL 不可用，3D 可视化需要浏览器支持 WebGL</div>
    <div ref="plotEl" class="spiral-plot"></div>
    <div class="spiral-ctrls">
      <div class="ctrl-row">
        <button class="play-btn" @click="togglePlay">{{ playing ? '⏸' : '▶' }}</button>
        <label>{{ $t('exhibit.vizAngle') }}:</label>
        <input type="range" :min="0" :max="720" :step="1" v-model.number="angle" class="spiral-slider">
        <span class="ang-val">{{ angle.toFixed(0) }}°</span>
      </div>
      <div class="live-coords">
        <span class="coord">cos θ = {{ cosVal.toFixed(4) }}</span>
        <span class="coord">sin θ = {{ sinVal.toFixed(4) }}</span>
        <span v-if="isFull" class="coord highlight">e<sup>iπ</sup> = −1</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const plotEl = ref(null)
const angle = ref(180)
const playing = ref(false)
const webglOk = ref(null)
let animId = null
let plotlyLoaded = false

const theta = computed(() => (angle.value * Math.PI) / 180)
const cosVal = computed(() => Math.cos(theta.value))
const sinVal = computed(() => Math.sin(theta.value))
const isFull = computed(() => Math.abs(angle.value - 180) < 1)

function checkWebGL() {
  try {
    const c = document.createElement('canvas')
    return !!(c.getContext('webgl') || c.getContext('experimental-webgl'))
  } catch { return false }
}

function togglePlay() {
  playing.value = !playing.value
  if (playing.value) { angle.value = 0; animate() }
  else { window.cancelAnimationFrame(animId) }
}
function animate() {
  if (!playing.value) return
  angle.value += 1.2
  if (angle.value > 720) { playing.value = false; angle.value = 720; return }
  animId = window.requestAnimationFrame(animate)
}

function buildTraces(ang) {
  const N = 800
  const maxAngle = Math.PI * 4
  const ts = Array.from({ length: N + 1 }, (_, i) => (i / N) * maxAngle)
  const xs = ts.map(v => Math.cos(v))
  const ys = ts.map(v => Math.sin(v))
  const zs = ts

  const segN = Math.max(2, Math.floor((ang / maxAngle) * N))
  const hxs = xs.slice(0, segN + 1)
  const hys = ys.slice(0, segN + 1)
  const hzs = zs.slice(0, segN + 1)

  const cx = Math.cos(ang), sy = Math.sin(ang)
  return [
    // Full helix (dim)
    { x: xs, y: ys, z: zs, type: 'scatter3d', mode: 'lines',
      line: { color: 'rgba(120,140,160,0.2)', width: 1.5 }, showlegend: false },
    // Active segment (bright)
    { x: hxs, y: hys, z: hzs, type: 'scatter3d', mode: 'lines',
      line: { color: '#4a6a8a', width: 5 }, showlegend: false },
    // Current point on helix
    { x: [cx], y: [sy], z: [ang], type: 'scatter3d', mode: 'markers',
      marker: { color: '#d06868', size: 8 }, showlegend: false },
    // Projection line: helix point → circle point
    { x: [cx, cx], y: [sy, sy], z: [ang, 0], type: 'scatter3d', mode: 'lines',
      line: { color: 'rgba(160,104,80,0.5)', width: 2, dash: 'dot' }, showlegend: false },
    // Unit circle on z=0
    { x: xs, y: ys, z: Array(N + 1).fill(0), type: 'scatter3d', mode: 'lines',
      line: { color: 'rgba(104,160,120,0.3)', width: 2 }, showlegend: false },
    // Projected point on circle
    { x: [cx], y: [sy], z: [0], type: 'scatter3d', mode: 'markers',
      marker: { color: '#3d6b4f', size: 7 }, showlegend: false },
    // Re axis line
    { x: [-1.5, 1.5], y: [0, 0], z: [0, 0], type: 'scatter3d', mode: 'lines',
      line: { color: 'rgba(180,60,60,0.25)', width: 1.5 }, showlegend: false },
    // Im axis line
    { x: [0, 0], y: [-1.5, 1.5], z: [0, 0], type: 'scatter3d', mode: 'lines',
      line: { color: 'rgba(60,120,180,0.25)', width: 1.5 }, showlegend: false },
  ]
}

function render() {
  if (!plotEl.value || typeof Plotly === 'undefined') return
  const data = buildTraces(theta.value)
  const layout = {
    scene: {
      xaxis: { title: 'Re (cos θ)', range: [-1.5, 1.5], gridcolor: 'rgba(120,140,160,0.12)' },
      yaxis: { title: 'Im (sin θ)', range: [-1.5, 1.5], gridcolor: 'rgba(120,140,160,0.12)' },
      zaxis: { title: 'θ (rad)', gridcolor: 'rgba(120,140,160,0.12)' },
      aspectmode: 'cube',
      camera: { eye: { x: 1.8, y: 1.8, z: 1.2 } },
    },
    margin: { t: 10, r: 10, b: 10, l: 10 },
    paper_bgcolor: 'rgba(0,0,0,0)',
  }
  Plotly.react(plotEl.value, data, layout, { responsive: true })
}

onMounted(async () => {
  webglOk.value = checkWebGL()
  if (!webglOk.value) return
  try {
    const { loadPlotly } = await import('@/utils/plotly')
    await loadPlotly()
    plotlyLoaded = true
    await new Promise(r => setTimeout(r, 50))
    render()
  } catch (e) {
    console.warn('Plotly load failed:', e)
    webglOk.value = false
  }
})

watch(angle, () => { if (plotlyLoaded) render() })
onUnmounted(() => { if (animId) window.cancelAnimationFrame(animId) })
</script>

<style scoped>
.spiral-plot { width: 100%; height: 460px; }
.no-webgl { text-align:center; padding:20px; color:var(--text-muted); font-size:13px; background:var(--bg-nav); border-radius:8px; margin-bottom:8px; }
.spiral-ctrls { text-align:center; margin-top:8px; font-size:13px; color:var(--text-secondary); }
.ctrl-row { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; }
.ang-val { font-weight:600; color:var(--accent); min-width:40px; font-family:var(--font-mono); }
.spiral-slider { width:280px; max-width:60%; accent-color:var(--accent); }
.play-btn { background:none; border:1px solid var(--border); border-radius:6px; padding:4px 10px; cursor:pointer; font-size:14px; transition:all 0.15s; }
.play-btn:hover { background:var(--bg-card); border-color:var(--accent); }
.live-coords { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; font-family:var(--font-mono); font-size:12px; margin-top:6px; }
.coord { background:var(--bg-nav); padding:3px 10px; border-radius:12px; }
.coord.highlight { background:rgba(208,104,104,0.12); color:var(--accent); font-weight:600; }
</style>
