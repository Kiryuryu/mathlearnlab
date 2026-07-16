<template>
  <div class="gaoshu-page">
    <div class="gaoshu-hero">
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

const { locale } = useI18n()
const subtopics = ref([])
const bgs = [
  'linear-gradient(135deg,#1a1d22,#1e2935,#2a3d54)',
  'linear-gradient(135deg,#1e1a2e,#2a2250,#3a2a60)',
  'linear-gradient(135deg,#1a2528,#1a3532,#1a4540)',
  'linear-gradient(135deg,#2a1a1e,#4a2528,#5a2a2e)',
  'linear-gradient(135deg,#1a1d22,#1e2935,#2a3d54)',
]
const exhibitKeys = ['limits','derivatives','integrals','series','multivariable']

const loading = ref(false)
onMounted(async () => {
  loading.value = true
  try {
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
  } catch(e) { console.warn('Failed to load exhibits', e) }
  loading.value = false
})
</script>

<style scoped>
.gaoshu-hero { background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460,#1a5276); color:#fff; text-align:center; padding:60px 40px 40px; }
.gaoshu-hero h1 { font-size:40px; margin:0 0 8px; }
.gaoshu-hero p { opacity:0.7; }
.gaoshu-content { max-width:1100px; margin:0 auto; padding:32px 20px; }
.sub-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }
.loading-wrap { text-align:center; padding:80px 0; }
.spinner { display:inline-block; width:32px; height:32px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.6s linear infinite; }
@keyframes spin { to { transform:rotate(360deg) } }
</style>
