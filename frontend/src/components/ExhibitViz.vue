<template>
  <div class="viz-wrap" :data-viz-ready="vizReady ? '1' : '0'">
    <div ref="vizPlot" class="viz-plot"></div>
    <div ref="vizControls" class="viz-ctrls"></div>
  </div>
</template>

<script setup>
// Interactive Plotly visualizations for exhibits.
// Extracted from ExhibitView to keep the page component lean; mounts lazily
// (the parent only renders it once the explore section is near the viewport).
import { ref, watch, onBeforeUnmount, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadPlotly } from '@/utils/plotly'
import { museumViz } from '@/utils/viz'

const props = defineProps({
  topic: { type: String, required: true },
})

const { t } = useI18n()
const vizPlot = ref(null)
const vizControls = ref(null)
const vizReady = ref(false)
let vizTimer = null
let vizTopic = null

function vizLabels() {
  return {
    epsilon: t('exhibit.vizEpsilon'),
    tangent: t('exhibit.vizTangent'),
    rectangles: t('exhibit.vizRectangles'),
    harmonics: t('exhibit.vizHarmonics'),
  }
}

async function runViz() {
  clearTimeout(vizTimer)
  vizTimer = setTimeout(async () => {
    try {
      await loadPlotly()
      await nextTick()
      const el = Array.isArray(vizPlot.value) ? vizPlot.value[0] : vizPlot.value
      const ctrls = Array.isArray(vizControls.value) ? vizControls.value[0] : vizControls.value
      if (!el) { runViz(); return }
      const tp = props.topic
      if (vizTopic === tp) return
      const lbl = vizLabels()
      if (tp === 'limits') { museumViz.epsilon(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'derivatives') { museumViz.tangent(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'integrals') { museumViz.riemann(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'series') { museumViz.fourier(el, ctrls, lbl, window.Plotly) }
      else if (tp === 'multivariable') { museumViz.gradient(el, ctrls, window.Plotly) }
      vizTopic = tp
      vizReady.value = true
    } catch (e) {
      console.warn('Plotly init failed', e)
    }
  }, 120)
}

watch(() => props.topic, () => { vizTopic = null; vizReady.value = false; runViz() }, { immediate: true })
onBeforeUnmount(() => clearTimeout(vizTimer))
</script>

<style scoped>
.viz-wrap { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin: 20px 0; }
.viz-plot { width: 100%; height: 420px; }
.viz-ctrls { text-align: center; margin-top: 8px; font-size: 13px; }
</style>
