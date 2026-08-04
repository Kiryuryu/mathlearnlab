<template>
  <div class="euler-spiral">
    <div ref="plotEl" class="spiral-plot"></div>
    <div class="spiral-ctrls">
      <label>{{ $t('exhibit.vizAngle') }}: <span class="ang-val">{{ angle.toFixed(1) }}°</span></label>
      <input type="range" :min="0" :max="720" :step="1" v-model.number="angle" class="spiral-slider">
      <div class="live-coords">
        <span class="coord">cos θ = {{ cosVal.toFixed(4) }}</span>
        <span class="coord">sin θ = {{ sinVal.toFixed(4) }}</span>
        <span class="coord">{{ isFull ? 'e^{iπ} = -1 ✓' : '' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'

const { t } = useI18n()
const plotEl = ref(null)
const angle = ref(180) // degrees

const theta = computed(() => (angle.value * Math.PI) / 180)
const cosVal = computed(() => Math.cos(theta.value))
const sinVal = computed(() => Math.sin(theta.value))
const isFull = computed(() => Math.abs(angle.value - 180) < 0.5)

function render() {
  if (!plotEl.value || typeof Plotly === 'undefined') return
  // 3D helix: x = cos t (real), y = sin t (imag), z = t (angle)
  const N = 600
  const ts = []
  for (let i = 0; i <= N; i++) ts.push((i / N) * Math.PI * 4) // 0..4π
  const xs = ts.map(v => Math.cos(v))
  const ys = ts.map(v => Math.sin(v))
  const zs = ts

  const ang = theta.value
  // helix segment up to current angle
  const segN = Math.max(2, Math.floor((ang / (Math.PI * 4)) * N))
  const hxs = xs.slice(0, segN + 1)
  const hys = ys.slice(0, segN + 1)
  const hzs = zs.slice(0, segN + 1)

  const data = [
    // Full helix (dim)
    { x: xs, y: ys, z: zs, type: 'scatter3d', mode: 'lines', line: { color: 'rgba(120,140,160,0.25)', width: 1.5 }, showlegend: false },
    // Active segment (bright)
    { x: hxs, y: hys, z: hzs, type: 'scatter3d', mode: 'lines', line: { color: '#4a6a8a', width: 4 }, showlegend: false },
    // Current point on helix
    { x: [Math.cos(ang)], y: [Math.sin(ang)], z: [ang], type: 'scatter3d', mode: 'markers', marker: { color: '#d06868', size: 8 }, showlegend: false },
    // Projection down to complex plane (z=0): vertical dashed line
    { x: [Math.cos(ang), Math.cos(ang)], y: [Math.sin(ang), Math.sin(ang)], z: [ang, 0], type: 'scatter3d', mode: 'lines', line: { color: 'rgba(160,104,80,0.6)', width: 2, dash: 'dot' }, showlegend: false },
    // Unit circle on z=0 plane
    { x: xs, y: ys, z: Array(xs.length).fill(0), type: 'scatter3d', mode: 'lines', line: { color: 'rgba(104,160,120,0.35)', width: 2 }, showlegend: false },
    // Projected point on circle
    { x: [Math.cos(ang)], y: [Math.sin(ang)], z: [0], type: 'scatter3d', mode: 'markers', marker: { color: '#3d6b4f', size: 7 }, showlegend: false },
  ]

  const layout = {
    title: t('exhibit.vizEuler'),
    scene: {
      xaxis: { title: 'Re (cos θ)', range: [-1.4, 1.4] },
      yaxis: { title: 'Im (sin θ)', range: [-1.4, 1.4] },
      zaxis: { title: 'θ (rad)' },
      aspectmode: 'cube',
      camera: { eye: { x: 1.6, y: 1.6, z: 1.1 } },
    },
    margin: { t: 40, r: 10, b: 10, l: 10 },
    paper_bgcolor: 'rgba(0,0,0,0)',
  }
  Plotly.react(plotEl.value, data, layout, { responsive: true })
}

onMounted(async () => {
  try { await loadPlotly() } catch { return }
  render()
})

watch(angle, render)
</script>

<style scoped>
.spiral-plot { width: 100%; height: 440px; }
.spiral-ctrls { text-align: center; margin-top: 8px; font-size: 13px; color: var(--text-secondary); }
.ang-val { font-weight: 600; color: var(--accent); }
.spiral-slider { width: 320px; max-width: 90%; margin: 4px 0 8px; accent-color: var(--accent); }
.live-coords { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; font-family: var(--font-mono); font-size: 12px; }
.coord { background: var(--bg-nav); padding: 3px 10px; border-radius: 12px; }
</style>
