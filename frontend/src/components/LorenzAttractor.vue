<template>
  <div ref="plotEl" class="lorenz-plot"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'

const { t } = useI18n()
const plotEl = ref(null)

onMounted(async () => {
  try { await loadPlotly() } catch { return }
  if (!plotEl.value || typeof Plotly === 'undefined') return
  const sigma = 10, rho = 28, beta = 8/3, dt = 0.003
  let x = 0.1, y = 0, z = 0
  const xs = [], ys = [], zs = []
  for (let i = 0; i < 15000; i++) {
    x += sigma*(y-x)*dt; y += (x*(rho-z)-y)*dt; z += (x*y-beta*z)*dt
    if (i > 1000) { xs.push(x); ys.push(y); zs.push(z) }
  }
  Plotly.newPlot(plotEl.value, [{
    x: xs, y: ys, z: zs, type: 'scatter3d', mode: 'lines',
    line: { width: 2, color: xs.map((_, i) => i / xs.length), colorscale: 'Viridis' }
  }], {
    title: t('fractal.lorenzTitle'),
    scene: { xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: 'z' } },
    margin: { t: 40, r: 20, b: 40, l: 20 },
    paper_bgcolor: 'rgba(0,0,0,0)'
  }, { responsive: true })
})
</script>

<style scoped>
.lorenz-plot { width: 100%; height: 500px; border: 1px solid var(--border); border-radius: 8px; }
</style>
