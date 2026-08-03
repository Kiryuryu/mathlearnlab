<template>
  <div class="exhibit-hero" :style="{ background: heroBg }">
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
  bigQ: { type: String, default: '' },
  historian: { type: String, default: '' },
  beauty: { type: String, default: '' },
  heroBg: { type: String, default: '' },
})
</script>

<style scoped>
.exhibit-hero { color:#fff; text-align:center; padding:60px 40px 40px; }
.exhibit-hero h1 { font-size:36px; margin:0 0 12px; }
.big-q { font-size:17px; opacity:0.8; margin-bottom:8px; }
.historian { font-size:13px; opacity:0.5; margin-bottom:16px; }
.beauty { font-size:14px; padding:10px 24px; background:rgba(255,255,255,0.1); border-radius:20px; display:inline-block; }
@media(max-width:768px) { .exhibit-hero { padding:32px 16px; } .exhibit-hero h1 { font-size:24px; } }
</style>
