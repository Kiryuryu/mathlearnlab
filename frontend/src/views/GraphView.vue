<template>
  <div class="graph-page">
    <div class="page-head">
      <p class="hero-eyebrow">{{ $t('graph.eyebrow') }}</p>
      <h1>{{ $t('graph.title') }}</h1>
      <p class="sub">{{ $t('graph.subtitle') }}</p>
    </div>
    <div v-if="loading" class="loading-wrap"><div class="spinner"></div></div>
    <template v-else>
      <div class="graph-legend">
        <span class="legend-item"><span class="legend-dot subject"></span>{{ $t('graph.subject') }}</span>
        <span class="legend-item"><span class="legend-dot concept"></span>{{ $t('graph.concept') }}</span>
        <span class="legend-item"><span class="legend-line parent"></span>{{ $t('graph.relation') }}</span>
        <span class="legend-item"><span class="legend-line related"></span>{{ $t('graph.link') }}</span>
      </div>
      <p class="graph-hint">{{ $t('graph.focusHint') }}</p>
      <div class="graph-canvas" :class="{ 'has-focus': focused }">
        <svg viewBox="0 0 960 620" class="graph-svg">
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill="var(--border)" />
            </marker>
          </defs>
          <g class="edges">
            <line
              v-for="e in edges"
              :key="e.source + '-' + e.target + '-' + e.type"
              :x1="px(e.source)" :y1="py(e.source)"
              :x2="px(e.target)" :y2="py(e.target)"
              :class="['edge', e.type, { dim: dimmed(e.source) || dimmed(e.target) }]"
            />
          </g>
          <g class="nodes">
            <g
              v-for="n in nodes"
              :key="n.id"
              :transform="'translate(' + n.x + ',' + n.y + ')'"
              :class="['node', n.type, { focused: isFocused(n), dim: dimmed(n.id) }]"
              @click="onNodeClick(n)"
            >
              <title>{{ nodeLabel(n) }}</title>
              <circle v-if="n.type === 'subject'" :r="30" :fill="n.accent" cx="0" cy="0" class="node-shape" />
              <rect v-else :width="56" :height="38" :x="-28" :y="-19" rx="9" :fill="n.accent" class="node-shape" />
              <text class="node-icon" text-anchor="middle" dominant-baseline="central">{{ n.icon }}</text>
              <text class="node-label" text-anchor="middle" :y="n.type === 'subject' ? 48 : 34">{{ nodeLabel(n) }}</text>
            </g>
          </g>
        </svg>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { apiFetch } from '@/utils/api'
import { forceSimulation, forceLink, forceManyBody, forceCenter, forceCollide, forceX, forceY } from 'd3-force'

const { locale, t } = useI18n()
const router = useRouter()

const loading = ref(false)
const nodes = ref([])      // { id, type, parent, zh, en, icon, accent, x, y, fx, fy }
const edges = ref([])      // { source, target, type }
const focused = ref(null)  // subject id currently focused

// ── Layout: deterministic static force simulation ──
function seedPositions(nodesArr, edgesArr) {
  // Place subjects on a ring, concepts near their parent, then relax with d3-force.
  const subjects = nodesArr.filter(n => n.type === 'subject')
  const concepts = nodesArr.filter(n => n.type === 'concept')
  const cx = 480, cy = 310
  const R = 200
  subjects.forEach((n, i) => {
    const a = (i / Math.max(subjects.length, 1)) * 2 * Math.PI - Math.PI / 2
    n.x = cx + R * Math.cos(a)
    n.y = cy + R * Math.sin(a)
  })
  concepts.forEach(n => {
    const parent = nodesArr.find(p => p.id === n.parent)
    const a = Math.random() * 2 * Math.PI
    n.x = (parent ? parent.x : cx) + 110 * Math.cos(a)
    n.y = (parent ? parent.y : cy) + 70 * Math.sin(a)
  })

  const sim = forceSimulation(nodesArr)
    .force('link', forceLink(edgesArr).id(d => d.id).distance(d => d.type === 'parent' ? 80 : 110))
    .force('charge', forceManyBody().strength(-160))
    .force('center', forceCenter(cx, cy))
    .force('x', forceX(cx).strength(0.06))
    .force('y', forceY(cy).strength(0.06))
    .force('collide', forceCollide().radius(d => (d.type === 'subject' ? 42 : 38)))
  sim.stop()
  for (let i = 0; i < 500; i++) sim.tick()
  // Freeze coordinates (deterministic, no animation).
  nodesArr.forEach(n => { n.fx = n.x; n.fy = n.y })
}

async function loadGraph() {
  loading.value = true
  try {
    const r = await apiFetch('/api/graph')
    const d = await r.json()
    const n = d.nodes.map(node => ({ ...node, x: 0, y: 0, fx: null, fy: null }))
    const e = d.edges.map(edge => ({ ...edge }))
    seedPositions(n, e)
    nodes.value = n
    edges.value = e
  } catch (err) {
    console.warn('Failed to load graph', err)
  }
  loading.value = false
}

function px(id) { const n = nodes.value.find(x => x.id === id); return n ? n.x : 0 }
function py(id) { const n = nodes.value.find(x => x.id === id); return n ? n.y : 0 }
function nodeLabel(n) { return locale.value === 'en' && n.en ? n.en : n.zh }

function isFocused(n) {
  if (!focused.value) return false
  return n.type === 'subject' ? n.id === focused.value : n.parent === focused.value
}
function dimmed(id) {
  if (!focused.value) return false
  const n = nodes.value.find(x => x.id === id)
  if (!n) return true
  if (n.type === 'subject') return n.id !== focused.value
  return n.parent !== focused.value
}

function onNodeClick(n) {
  if (n.type === 'concept') {
    router.push('/exhibit/' + n.id)
    return
  }
  // subject: toggle focus
  focused.value = focused.value === n.id ? null : n.id
}

watch(locale, () => { /* labels re-render via nodeLabel */ })
onMounted(loadGraph)
</script>

<style scoped>
.graph-page { max-width: 1100px; margin: 0 auto; padding: 40px 20px 60px; }
.loading-wrap { text-align: center; padding: 80px 0; }
.spinner { display: inline-block; width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg) } }

.graph-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin: 24px 0 6px;
  font-size: 12px;
  color: var(--text-secondary);
}
.legend-item { display: inline-flex; align-items: center; gap: 6px; }
.legend-dot { width: 14px; height: 14px; border-radius: 50%; display: inline-block; }
.legend-dot.subject { background: var(--accent); }
.legend-dot.concept { background: var(--accent-soft); border: 1px solid var(--accent); }
.legend-line { width: 22px; height: 2px; display: inline-block; }
.legend-line.parent { background: var(--border-focus); }
.legend-line.related { background: transparent; border-top: 2px dashed var(--text-muted); }

.graph-hint { text-align: center; color: var(--text-muted); font-size: 12px; margin: 6px 0 16px; }

.graph-canvas {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 12px;
  overflow-x: auto;
}
.graph-svg { width: 100%; min-width: 640px; height: auto; display: block; }

.edge { stroke: var(--border); stroke-width: 1.2; }
.edge.parent { stroke: var(--border-focus); }
.edge.related { stroke-dasharray: 5 4; stroke: var(--text-muted); opacity: 0.7; }
.edge.dim { opacity: 0.08; }

.node { cursor: pointer; transition: opacity 0.2s; }
.node.dim { opacity: 0.2; }
.node-shape { stroke: var(--bg-page); stroke-width: 2.5; transition: filter 0.15s; }
.node:hover .node-shape { filter: brightness(1.12); }
.node.focused .node-shape { stroke: var(--text-primary); stroke-width: 2.5; }
.node-icon { fill: #fff; font-size: 16px; font-weight: 700; pointer-events: none; }
.node-label { fill: var(--text-primary); font-size: 12px; font-family: var(--font-heading); pointer-events: none; }

@media(max-width: 768px) {
  .graph-legend { gap: 12px; font-size: 11px; }
  .graph-svg { min-width: 520px; }
}
</style>
