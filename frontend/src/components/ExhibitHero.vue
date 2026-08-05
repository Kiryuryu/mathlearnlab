<template>
  <div class="exhibit-hero" :style="{ background: heroBg, borderColor: heroBorder }">
    <p class="hero-eyebrow">{{ eyebrow }}</p>
    <h1>{{ name }}</h1>
    <p class="big-q">{{ bigQ }}</p>
    <p class="historian">{{ t('exhibit.historian') }}{{ historian }}</p>
    <p class="beauty">{{ beauty }}</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
defineProps({
  name: { type: String, default: '' },
  eyebrow: { type: String, default: '' },
  bigQ: { type: String, default: '' },
  historian: { type: String, default: '' },
  beauty: { type: String, default: '' },
  heroBg: { type: String, default: '' },
  heroBorder: { type: String, default: '' },
})
</script>

<style scoped>
.exhibit-hero {
  color: var(--text-primary);
  text-align: center;
  padding: 56px 40px 44px;
  border-bottom: 1px solid var(--border);
  position: relative;
}
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--accent-warm);
  font-weight: 600;
  margin: 0 0 12px;
}
.exhibit-hero h1 { font-size: 38px; margin: 0 0 14px; }
.big-q { font-size: 16px; color: var(--text-secondary); margin-bottom: 10px; line-height: 1.8; }
.historian { font-size: 13px; color: var(--text-muted); margin-bottom: 18px; }
.beauty {
  font-size: 13px;
  padding: 8px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: inline-block;
  color: var(--text-secondary);
}
@media(max-width:768px) { .exhibit-hero { padding: 36px 16px; } .exhibit-hero h1 { font-size: 26px; } }
</style>
