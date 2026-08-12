<template>
  <div class="subject-page" v-if="subject">
    <div class="hero">
      <p class="hero-eyebrow">{{ $t('subject.eyebrow') }}</p>
      <h1>{{ subjectName }}</h1>
      <p class="hero-sub">{{ subjectDesc }}</p>
    </div>
    <div class="subject-content">
      <div v-if="loading" class="loading-wrap"><div class="spinner"></div></div>
      <template v-else>
        <div class="sub-grid">
          <ExhibitCard v-for="s in topics" :key="s.key" :to="'/exhibit/'+s.key" :title="s.label" :desc="s.question" :meta="s.historian" :accent="s.accent" :symbol="s.symbol" :chapter="s.chapter" />
        </div>
        <nav class="subject-pager" v-if="siblings.length">
          <router-link v-if="prevSubject" :to="'/subject/' + prevSubject" class="pager-link prev">
            <span class="pager-label">{{ $t('subject.prevSubject') }}</span>
            <span class="pager-name">{{ siblingName(prevSubject) }}</span>
          </router-link>
          <router-link v-if="nextSubject" :to="'/subject/' + nextSubject" class="pager-link next">
            <span class="pager-label">{{ $t('subject.nextSubject') }}</span>
            <span class="pager-name">{{ siblingName(nextSubject) }}</span>
          </router-link>
        </nav>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ExhibitCard from '@/components/ExhibitCard.vue'
import { useLoading } from '@/utils/useLoading'

const { locale } = useI18n()
const route = useRoute()
const subjectKey = computed(() => route.params.key)
const subjects = ref({})
const exhibits = ref({})
const topics = ref([])
const ROMANS = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']

const subject = computed(() => subjects.value[subjectKey.value] || null)
const subjectName = computed(() => {
  const s = subject.value
  return s ? (locale.value === 'en' && s.en ? s.en : s.zh) : ''
})
const subjectDesc = computed(() => {
  const s = subject.value
  return s ? (locale.value === 'en' && s.desc_en ? s.desc_en : s.desc) : ''
})

// All subjects ordered, for prev/next navigation within the subject list.
const siblings = computed(() => Object.entries(subjects.value)
  .filter(([, s]) => s.order)
  .sort((a, b) => a[1].order - b[1].order)
  .map(([key]) => key))
const idx = computed(() => siblings.value.indexOf(subjectKey.value))
const prevSubject = computed(() => idx.value > 0 ? siblings.value[idx.value - 1] : '')
const nextSubject = computed(() => idx.value >= 0 && idx.value < siblings.value.length - 1 ? siblings.value[idx.value + 1] : '')

function siblingName(key) {
  const s = subjects.value[key]
  if (!s) return key
  return locale.value === 'en' && s.en ? s.en : s.zh
}

const { loading, run } = useLoading(false)
onMounted(() => run(async () => {
  const r = await fetch('/api/museum/exhibits')
  const d = await r.json()
  subjects.value = d.subjects || {}
  exhibits.value = d.exhibits || {}
  const key = subjectKey.value
  topics.value = Object.entries(exhibits.value)
    .filter(([, ex]) => ex.parent === key && ex.order)
    .sort((a, b) => a[1].order - b[1].order)
    .map(([ek, ex], i) => ({
      key: ek,
      label: locale.value === 'en' && ex.en ? ex.en : ex.zh,
      question: locale.value === 'en' && ex.big_question_en ? ex.big_question_en : ex.big_question,
      historian: ex.historian,
      accent: ex.home_accent || '',
      symbol: ex.icon || '',
      chapter: ROMANS[i + 1] || '',
    }))
}).catch(e => console.warn('Failed to load exhibits', e)))
</script>

<style scoped>
.subject-content { max-width: 1200px; margin: 0 auto; padding: 36px 20px; }
.sub-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.loading-wrap { text-align: center; padding: 80px 0; }
.spinner { display: inline-block; width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg) } }

.subject-pager {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}
.pager-link {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-card);
  color: var(--text-primary);
  text-decoration: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.pager-link:hover { border-color: var(--accent); box-shadow: var(--shadow-elevated); text-decoration: none; }
.pager-link.next { text-align: right; }
.pager-label { font-size: 11px; color: var(--text-muted); letter-spacing: 0.04em; }
.pager-name { font-family: var(--font-heading); font-size: 15px; }
@media(max-width:768px) { .subject-pager { flex-direction: column; } }
</style>
