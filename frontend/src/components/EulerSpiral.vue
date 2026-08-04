<template>
  <div class="euler-spiral">
    <canvas ref="canvas" class="spiral-canvas" :width="W" :height="H"></canvas>
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

const W = 560
const H = 400
const canvas = ref(null)
const angle = ref(180)
const playing = ref(false)
let animId = null

const theta = computed(() => (angle.value * Math.PI) / 180)
const cosVal = computed(() => Math.cos(theta.value))
const sinVal = computed(() => Math.sin(theta.value))
const isFull = computed(() => Math.abs(angle.value - 180) < 1)

function togglePlay() {
  playing.value = !playing.value
  if (playing.value) {
    angle.value = 0
    animate()
  } else {
    window.cancelAnimationFrame(animId)
  }
}

function animate() {
  if (!playing.value) return
  angle.value += 1.5
  if (angle.value > 720) { playing.value = false; angle.value = 720; return }
  animId = window.requestAnimationFrame(animate)
}

function draw() {
  const c = canvas.value
  if (!c) return
  const ctx = c.getContext('2d')
  const dpr = window.devicePixelRatio || 1
  c.width = W * dpr
  c.height = H * dpr
  c.style.width = W + 'px'
  c.style.height = H + 'px'
  ctx.scale(dpr, dpr)

  const cx = W / 2
  const cy = H / 2
  const R = 130 // unit circle radius in px
  const ang = theta.value

  // Clear
  ctx.clearRect(0, 0, W, H)

  // --- Grid ---
  ctx.strokeStyle = 'rgba(120,140,160,0.12)'
  ctx.lineWidth = 1
  // horizontal axis (Re)
  ctx.beginPath(); ctx.moveTo(cx - R - 40, cy); ctx.lineTo(cx + R + 40, cy); ctx.stroke()
  // vertical axis (Im)
  ctx.beginPath(); ctx.moveTo(cx, cy - R - 40); ctx.lineTo(cx, cy + R + 40); ctx.stroke()

  // --- Unit circle ---
  ctx.beginPath()
  ctx.arc(cx, cy, R, 0, Math.PI * 2)
  ctx.strokeStyle = 'rgba(100,160,130,0.4)'
  ctx.lineWidth = 2
  ctx.stroke()

  // --- Spiral trace (angle sweep) ---
  if (ang > 0) {
    ctx.beginPath()
    const steps = Math.min(600, Math.floor(ang / (Math.PI * 2) * 120))
    for (let i = 0; i <= steps; i++) {
      const a = (i / steps) * ang
      const spiralR = R + (a / (Math.PI * 2)) * 22 // spiral expands outward
      const x = cx + spiralR * Math.cos(a)
      const y = cy - spiralR * Math.sin(a)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.strokeStyle = 'rgba(74,106,138,0.5)'
    ctx.lineWidth = 2
    ctx.stroke()
  }

  // --- Current spiral point ---
  const spiralR = R + (ang / (Math.PI * 2)) * 22
  const px = cx + spiralR * Math.cos(ang)
  const py = cy - spiralR * Math.sin(ang)
  ctx.beginPath()
  ctx.arc(px, py, 6, 0, Math.PI * 2)
  ctx.fillStyle = '#d06868'
  ctx.fill()
  ctx.strokeStyle = '#fff'
  ctx.lineWidth = 2
  ctx.stroke()

  // --- Projection line (spiral point → circle point) ---
  const cxP = cx + R * Math.cos(ang)
  const cyP = cy - R * Math.sin(ang)
  ctx.setLineDash([4, 4])
  ctx.beginPath()
  ctx.moveTo(px, py)
  ctx.lineTo(cxP, cyP)
  ctx.strokeStyle = 'rgba(160,104,80,0.5)'
  ctx.lineWidth = 1.5
  ctx.stroke()
  ctx.setLineDash([])

  // --- Projection line down to axis ---
  ctx.setLineDash([3, 3])
  ctx.beginPath()
  ctx.moveTo(cxP, cyP)
  ctx.lineTo(cxP, cy)
  ctx.strokeStyle = 'rgba(120,140,160,0.3)'
  ctx.lineWidth = 1
  ctx.stroke()
  ctx.beginPath()
  ctx.moveTo(cxP, cyP)
  ctx.lineTo(cx, cyP)
  ctx.stroke()
  ctx.setLineDash([])

  // --- Unit circle point ---
  ctx.beginPath()
  ctx.arc(cxP, cyP, 5, 0, Math.PI * 2)
  ctx.fillStyle = '#3d6b4f'
  ctx.fill()
  ctx.strokeStyle = '#fff'
  ctx.lineWidth = 2
  ctx.stroke()

  // --- Angle arc ---
  if (ang > 0.05) {
    const arcR = 30
    ctx.beginPath()
    ctx.arc(cx, cy, arcR, 0, -ang, true) // CCW for positive angle
    ctx.strokeStyle = 'rgba(200,160,80,0.6)'
    ctx.lineWidth = 2
    ctx.stroke()
    // angle label
    const labelA = ang / 2
    const lx = cx + (arcR + 14) * Math.cos(-labelA)
    const ly = cy + (arcR + 14) * Math.sin(-labelA)
    ctx.fillStyle = 'rgba(200,160,80,0.85)'
    ctx.font = '11px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('θ', lx, ly + 4)
  }

  // --- Axis labels ---
  ctx.fillStyle = 'rgba(120,140,160,0.7)'
  ctx.font = '12px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('Re (cos θ)', cx + R + 30, cy + 16)
  ctx.fillText('Im (sin θ)', cx, cy - R - 28)
  ctx.fillText('0', cx + 8, cy + 16)
  ctx.fillText('1', cx + R + 4, cy + 16)
  ctx.fillText('−1', cx - R - 12, cy + 16)
  ctx.fillText('i', cx + 10, cy - R - 6)
  ctx.fillText('−i', cx + 12, cy + R + 14)
}

onMounted(() => { draw() })
watch(angle, draw)
onUnmounted(() => { if (animId) window.cancelAnimationFrame(animId) })
</script>

<style scoped>
.spiral-canvas { display:block; margin:0 auto; max-width:100%; border-radius:8px; }
.spiral-ctrls { text-align:center; margin-top:10px; font-size:13px; color:var(--text-secondary); }
.ctrl-row { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; }
.ang-val { font-weight:600; color:var(--accent); min-width:40px; font-family:var(--font-mono); }
.spiral-slider { width:280px; max-width:60%; accent-color:var(--accent); }
.play-btn { background:none; border:1px solid var(--border); border-radius:6px; padding:4px 10px; cursor:pointer; font-size:14px; transition:all 0.15s; }
.play-btn:hover { background:var(--bg-card); border-color:var(--accent); }
.live-coords { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; font-family:var(--font-mono); font-size:12px; margin-top:6px; }
.coord { background:var(--bg-nav); padding:3px 10px; border-radius:12px; }
.coord.highlight { background:rgba(208,104,104,0.12); color:var(--accent); font-weight:600; }
</style>
