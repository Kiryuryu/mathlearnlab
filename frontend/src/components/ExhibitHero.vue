<template>
  <div class="hero exhibit-hero" :style="{ borderColor: heroBorder }">
    <p class="hero-eyebrow">
      <span v-if="chapter" class="exhibit-chapter"><span class="chapter-roman">{{ chapter }}</span> {{ eyebrow }}</span>
      <span v-else>{{ eyebrow }}</span>
    </p>
    <h1>{{ name }}</h1>
    <p class="big-q">{{ bigQ }}</p>
    <p class="historian">{{ t('exhibit.historian') }}
      <template v-if="mathematicianLinks.length">
        <router-link
          v-for="ml in mathematicianLinks"
          :key="ml.key"
          :to="'/mathematicians/' + ml.key"
          class="historian-link"
        >{{ ml.name }}</router-link>
      </template>
      <template v-else>{{ historian }}</template>
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const props = defineProps({
  name: { type: String, default: '' },
  eyebrow: { type: String, default: '' },
  chapter: { type: String, default: '' },
  bigQ: { type: String, default: '' },
  historian: { type: String, default: '' },
  mathematicians: { type: Array, default: () => [] }, // [{ key, name, name_en }]
  heroBg: { type: String, default: '' },
  heroBorder: { type: String, default: '' },
})

const mathematicianLinks = computed(() => props.mathematicians.map(m => ({
  key: m.key,
  name: locale.value === 'en' && m.name_en ? m.name_en : m.name,
})))
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
.historian-link {
  color: var(--accent);
  text-decoration: none;
  margin-right: 6px;
  border-bottom: 1px dashed color-mix(in srgb, var(--accent) 40%, transparent);
  transition: border-color 0.15s;
}
.historian-link:hover { border-bottom-color: var(--accent); text-decoration: none; }
@media(max-width:768px) { .exhibit-hero h1 { font-size: 26px; } }
</style>
