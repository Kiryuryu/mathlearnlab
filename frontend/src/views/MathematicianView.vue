<template>
  <div class="page">
    <div v-if="loading" class="loading-wrap">
      <div class="spinner"></div>
    </div>
    <template v-if="m">
    <div class="hero">
      <div class="portrait">
        <img v-if="m.photo" :src="m.photo" :alt="m.name" class="photo-img" />
        <div v-else class="avatar">{{ m.icon }}</div>
      </div>
      <h1>{{ displayName }}</h1>
      <p class="years">{{ m.years }}</p>
      <p class="contrib">{{ displayContrib }}</p>
    </div>
    <div class="content">
      <blockquote>{{ m.quote }}</blockquote>

      <section v-if="displayBio">
        <h2>{{ $t('mathematicians.bio') }}</h2>
        <p class="section-text">{{ displayBio }}</p>
      </section>

      <section v-if="displayIdeas">
        <h2>{{ $t('mathematicians.ideas') }}</h2>
        <p class="section-text">{{ displayIdeas }}</p>
      </section>

      <section v-if="displayAnecdotes">
        <h2>{{ $t('mathematicians.anecdotes') }}</h2>
        <p class="section-text">{{ displayAnecdotes }}</p>
      </section>

      <section v-if="displayStory">
        <h2>{{ $t('mathematicians.story') }}</h2>
        <div class="story" v-html="displayStory.replace(/\n\n/g,'</p><p>')"></div>
      </section>

      <div class="links" v-if="m.exhibits?.length">
        <h3>{{ $t('mathematicians.relatedExhibits') }}</h3>
        <router-link v-for="ek in m.exhibits" :key="ek" :to="'/exhibit/'+ek" class="btn">→ {{ exhibitLabels[ek] || ek }}</router-link>
      </div>
      <router-link to="/mathematicians" class="back">{{ $t('mathematicians.back') }}</router-link>
    </div>
    </template>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()
const route = useRoute()
const m = ref(null)
const loading = ref(false)
const exhibitLabels = computed(() => ({
  limits: t('mathematicians.exLimit'),
  derivatives: t('mathematicians.exDerivative'),
  integrals: t('mathematicians.exIntegral'),
  series: t('mathematicians.exSeries'),
  multivariable: t('mathematicians.exMultivariable'),
}))
const displayName = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.name_en ? m.value.name_en : m.value.name
})
const displayContrib = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.contributions_en ? m.value.contributions_en : m.value.contributions
})
const displayBio = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.bio_en ? m.value.bio_en : m.value.bio
})
const displayIdeas = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.ideas_en ? m.value.ideas_en : m.value.ideas
})
const displayAnecdotes = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.anecdotes_en ? m.value.anecdotes_en : m.value.anecdotes
})
const displayStory = computed(() => {
  if (!m.value) return ''
  return locale.value === 'en' && m.value.story_en ? m.value.story_en : m.value.story
})
onMounted(async () => {
  loading.value = true
  try {
    const r = await fetch('/api/museum/exhibits')
    const d = await r.json()
    m.value = d.mathematicians[route.params.key]
  } catch(e) { console.warn('Failed to load mathematician', e) }
  loading.value = false
})
</script>
<style scoped>
.hero { background:linear-gradient(135deg,#1a1a2e,#2d1b69,#1a1a2e); color:#fff; text-align:center; padding:48px 32px 36px; }
.portrait { width:120px; height:120px; border-radius:50%; margin:0 auto 20px; overflow:hidden; border:3px solid rgba(255,255,255,0.3); background:rgba(255,255,255,0.1); display:flex; align-items:center; justify-content:center; }
.avatar { font-size:48px; font-weight:700; color:rgba(255,255,255,0.8); font-family:var(--font-heading); }
.photo-img { width:100%; height:100%; object-fit:cover; }
.hero h1 { font-size:32px; margin:0 0 8px; color:#fff; }
.years { opacity:0.5; color:#fff; }
.contrib { opacity:0.8; margin-top:8px; font-size:16px; color:#fff; }
.content { max-width:720px; margin:0 auto; padding:32px 20px 64px; }
blockquote { border-left:3px solid var(--accent-warm); padding:12px 20px; background:var(--bg-nav); border-radius:0 8px 8px 0; font-style:italic; color:var(--text-secondary); margin:20px 0; }
section { margin:28px 0; }
h2 { font-size:20px; margin:0 0 12px; padding-bottom:6px; border-bottom:1px solid var(--border); }
.section-text { font-size:15px; line-height:2; color:var(--text-primary); }
.story { font-size:15px; line-height:2; }
.links { margin:32px 0; }
.links h3 { margin-bottom:8px; font-size:15px; }
.btn { display:inline-block; padding:6px 14px; border:1px solid var(--accent); color:var(--accent); border-radius:4px; text-decoration:none; margin:4px; font-size:13px; }
.btn:hover { background:var(--accent); color:#fff; }
.back { display:block; text-align:center; margin-top:40px; color:var(--accent); text-decoration:none; font-size:14px; }
.back:hover { text-decoration:underline; }
.loading-wrap { text-align:center; padding:80px 0; }
.spinner { display:inline-block; width:32px; height:32px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.6s linear infinite; }
@keyframes spin { to { transform:rotate(360deg) } }
</style>
