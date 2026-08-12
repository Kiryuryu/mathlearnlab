<template>
  <router-link :to="to" class="card" :style="cardStyle">
    <div class="card-accent" :style="{ background: accent }"></div>
    <span v-if="chapter" class="card-chapter chapter-roman">{{ chapter }}</span>
    <span v-if="symbol" class="card-symbol">{{ symbol }}</span>
    <div class="card-body">
      <h2>{{ title }}</h2>
      <p>{{ desc }}</p>
      <div class="card-meta">{{ meta }}</div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  to: String,
  title: String,
  desc: String,
  meta: String,
  bg: { type: String, default: '' }, // legacy gradient prop, now ignored in favor of paper style
  accent: { type: String, default: '' }, // optional muted chapter-marker color
  symbol: { type: String, default: '' }, // math symbol watermark (∞, ∆, ∫, ∑, ∂, λ, P)
  chapter: { type: String, default: '' }, // roman numeral chapter marker (Ⅰ, Ⅱ, …)
})

// Book-cloth muted accents per chapter, desaturated to fit paper palette
const ACCENTS = [
  '#8a6f3d', // ochre
  '#6b7a4a', // olive
  '#4a6b8a', // slate indigo
  '#7a5a6b', // mauve
  '#5a6b6b', // teal-gray
  '#8a5a4a', // sienna
]

const cardStyle = computed(() => ({
  '--card-accent': props.accent || ACCENTS[(props.to?.charCodeAt(1) || 0) % ACCENTS.length],
}))
</script>

<style scoped>
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 200px;
  padding: 26px 26px 22px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  text-decoration: none;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.25s ease, border-color 0.2s ease;
  box-shadow: var(--shadow-card);
}
.card::after {
  /* faint paper-grain wash on hover */
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(120% 90% at 0% 0%, color-mix(in srgb, var(--card-accent) 9%, transparent), transparent 60%);
  opacity: 0;
  transition: opacity 0.25s ease;
  pointer-events: none;
}
.card:hover {
  transform: translateY(-3px);
  border-color: color-mix(in srgb, var(--card-accent) 55%, var(--border));
  box-shadow: var(--shadow-elevated);
  text-decoration: none;
  color: var(--text-primary);
}
.card:hover::after { opacity: 1; }
.card-accent {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--card-accent);
  opacity: 0.75;
}
.card-chapter {
  position: absolute;
  top: 18px; right: 22px;
  font-size: 44px;
  font-weight: 800;
  color: var(--text-muted);
  opacity: 0.14;
  pointer-events: none;
}
.card-symbol {
  position: absolute;
  top: 26px; left: 26px;
  font-family: var(--font-mono);
  font-size: 26px;
  font-weight: 700;
  color: var(--card-accent);
  opacity: 0.85;
  pointer-events: none;
}
.card-body { position: relative; z-index: 1; }
.card-body h2 {
  font-size: 21px;
  margin: 0 0 10px;
  color: var(--text-primary);
  border: none;
  letter-spacing: 0.02em;
}
.card-body p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 6px;
  line-height: 1.7;
}
.card-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 10px;
  letter-spacing: 0.03em;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}
</style>
