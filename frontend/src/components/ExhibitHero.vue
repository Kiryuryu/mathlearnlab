<template>
  <div class="hero exhibit-hero" :style="{ borderColor: heroBorder }">
    <p class="hero-eyebrow">
      <span v-if="chapter" class="exhibit-chapter"><span class="chapter-roman">{{ chapter }}</span> {{ eyebrow }}</span>
      <span v-else>{{ eyebrow }}</span>
    </p>
    <h1>{{ name }}</h1>
    <p class="big-q">{{ bigQ }}</p>
    <p class="historian">{{ t('exhibit.historian') }}{{ historian }}</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
defineProps({
  name: { type: String, default: '' },
  eyebrow: { type: String, default: '' },
  chapter: { type: String, default: '' },
  bigQ: { type: String, default: '' },
  historian: { type: String, default: '' },
  heroBg: { type: String, default: '' },
  heroBorder: { type: String, default: '' },
})
</script>

<style scoped>
.exhibit-hero { position: relative; overflow: hidden; }
.exhibit-chapter {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--accent-warm);
  font-weight: 600;
}
.exhibit-chapter .chapter-roman { font-size: 22px; color: var(--accent); }
.exhibit-hero h1 { font-size: 38px; margin: 0 0 14px; }
.big-q { font-size: 16px; color: var(--text-secondary); margin-bottom: 10px; line-height: 1.8; }
.historian { font-size: 13px; color: var(--text-muted); margin-bottom: 18px; }
@media(max-width:768px) { .exhibit-hero h1 { font-size: 26px; } }
</style>
