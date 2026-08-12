<template>
  <div class="gaoshu-page">
    <div class="hero">
      <p class="hero-eyebrow">{{ $t('exhibit.museum') }}</p>
      <h1>{{ $t('gaoshu.title') }}</h1>
      <p class="hero-sub">{{ $t('gaoshu.subtitle') }}</p>
    </div>
    <div class="gaoshu-content">
      <h2 style="text-align:center;margin-bottom:24px;">{{ $t('gaoshu.sections') }}</h2>
      <div v-if="loading" class="loading-wrap"><div class="spinner"></div></div>
      <div v-else class="sub-grid">
        <ExhibitCard v-for="s in subtopics" :key="s.key" :to="'/exhibit/'+s.key" :title="s.label" :desc="s.question" :meta="s.historian" :accent="s.accent" :symbol="s.symbol" :chapter="s.chapter" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import ExhibitCard from '@/components/ExhibitCard.vue'
import { useLoading } from '@/utils/useLoading'

const { locale } = useI18n()
const subtopics = ref([])
// Paper-plate accent bands per chapter (muted book-cloth colors)
const bgs = [
  '#4a6b8a',
  '#8a6f3d',
  '#6b7a4a',
  '#7a5a6b',
  '#5a6b6b',
  '#8a5a4a',
  '#6b5a7a',
]
const ROMANS = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']
const exhibitKeys = ['limits','derivatives','integrals','series','multivariable','linear-algebra','probability']

const { loading, run } = useLoading(false)
onMounted(() => run(async () => {
  const r = await fetch('/api/museum/exhibits')
  const d = await r.json()
  subtopics.value = exhibitKeys.map((key, i) => {
    const ex = d.exhibits[key]
    return {
      key,
      label: locale.value === 'en' && ex.en ? ex.en : ex.zh,
      question: locale.value === 'en' && ex.big_question_en ? ex.big_question_en : ex.big_question,
      historian: ex.historian,
      accent: bgs[i],
      symbol: ex.icon || '',
      chapter: ROMANS[i],
      bg: bgs[i],
    }
  })
}).catch(e => console.warn('Failed to load exhibits', e)))
</script>

<style scoped>
.gaoshu-content { max-width:1200px; margin:0 auto; padding:36px 20px; }
.sub-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px; }
.loading-wrap { text-align:center; padding:80px 0; }
.spinner { display:inline-block; width:32px; height:32px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.6s linear infinite; }
@keyframes spin { to { transform:rotate(360deg) } }
@media(max-width:768px) { .gaoshu-hero { padding:36px 16px; } .gaoshu-hero h1 { font-size:26px; } }
</style>
