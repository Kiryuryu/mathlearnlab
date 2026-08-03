<template>
  <div class="news-page">
    <h1>{{ $t('news.title') }}</h1>
    <p class="sub">{{ $t('news.subtitle') }}</p>

    <NewsList
      v-if="!selectedPost"
      :posts="posts"
      :loading="loading"
      @open="goToPost"
    />

    <NewsPostDetail
      v-else
      :post="selectedPost"
      :content="renderedContent"
      @back="router.push('/news')"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/utils/toast'
import { renderMarkdown } from '@/utils/markdown'
import NewsList from '@/components/NewsList.vue'
import NewsPostDetail from '@/components/NewsPostDetail.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const { show: showToast } = useToast()

const posts = ref([])
const loading = ref(false)
const selectedPost = ref(null)
const renderedContent = ref('')

async function fetchPosts() {
  loading.value = true
  try {
    const r = await fetch('/api/blog/posts')
    posts.value = (await r.json()).posts || []

    // If we're on a detail route, auto-load that post
    const slug = route.params.slug
    if (slug) {
      const post = posts.value.find(p => p.slug === slug)
      if (post) {
        selectedPost.value = post
        renderedContent.value = ''
        try {
          const cr = await fetch(`/api/blog/posts/${slug}`)
          const cd = await cr.json()
          renderedContent.value = renderMarkdown(cd.content || '')
        } catch {}
      } else {
        // Slug not in list — redirect to list view
        window.location.href = '/news'
      }
    }
  } catch(e) {
    console.warn('Failed to fetch posts', e)
    showToast(t('news.loadFail'))
  }
  loading.value = false
}

function goToPost(post) {
  window.location.href = `/news/${post.slug}`
}

onMounted(fetchPosts)
</script>

<style scoped>
.news-page { max-width:800px; margin:0 auto; padding:32px 20px 64px; }
.news-page h1 { text-align:center; font-size:28px; }
.sub { text-align:center; color:var(--text-secondary); margin-bottom:24px; }
</style>
