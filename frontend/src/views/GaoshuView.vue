<template>
  <div class="gaoshu-page">
    <div class="gaoshu-hero">
      <p class="hero-eyebrow">{{ $t('exhibit.museum') }}</p>
      <h1>{{ $t('gaoshu.title') }}</h1>
      <p>{{ $t('gaoshu.subtitle') }}</p>
    </div>
    <div class="gaoshu-content">
      <h2 style="text-align:center;margin-bottom:24px;">{{ $t('gaoshu.sections') }}</h2>
      <div v-if="loading" class="loading-wrap"><div class="spinner"></div></div>
      <div v-else class="sub-grid">
        <ExhibitCard v-for="s in subtopics" :key="s.key" :to="'/exhibit/'+s.key" :title="s.label" :desc="s.question" :meta="s.historian" :bg="s.bg" />
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
]
const exhibitKeys = ['limits','derivatives','integrals','series','multivariable']

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
      bg: bgs[i],
    }
  })
}).catch(e => console.warn('Failed to load exhibits', e)))
</script>

<style scoped>
.gaoshu-hero {
  background: radial-gradient(90% 70% at 50% 0%, #eef0f4 0%, transparent 70%), linear-gradient(180deg, #f1efe7 0%, #f6f3ec 100%);
  color: var(--text-primary);
  text-align: center;
  padding: 56px 40px 44px;
  border-bottom: 1px solid var(--border);
}
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--accent-warm);
  font-weight: 600;
  margin: 0 0 12px;
}
.gaoshu-hero h1 { font-size: 38px; margin: 0 0 10px; }
.gaoshu-hero p:not(.hero-eyebrow) { color: var(--text-secondary); }
.gaoshu-content { max-width:1200px; margin:0 auto; padding:36px 20px; }
.sub-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px; }
.loading-wrap { text-align:center; padding:80px 0; }
.spinner { display:inline-block; width:32px; height:32px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.6s linear infinite; }
@keyframes spin { to { transform:rotate(360deg) } }
@media(max-width:768px) { .gaoshu-hero { padding:36px 16px; } .gaoshu-hero h1 { font-size:26px; } }
</style>
