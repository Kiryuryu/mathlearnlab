<template>
  <div :lang="$i18n.locale">
    <a href="#main-content" class="skip-link">{{ $t('common.skipToContent') }}</a>
    <header class="app-header">
      <div class="header-left">
        <router-link to="/" class="app-brand" @click.prevent="onLogoClick">{{ $t('header.brand') }}</router-link>
        <span class="app-subtitle">{{ $t('header.subtitle') }}</span>
      </div>
      <div class="header-right">
        <button class="header-btn hamburger" @click="mobileNavOpen = !mobileNavOpen" aria-label="Menu">☰</button>
        <button class="header-btn lang-switch" @click="toggleLang" :aria-label="$t('common.switchLang')">{{ localeLabel }}</button>
        <button class="header-btn" @click="auth.openLogin()" v-if="!auth.isLoggedIn" :aria-label="$t('header.login')">{{ $t('header.login') }}</button>
        <button class="header-btn" @click="auth.openSettings()" v-if="auth.isLoggedIn" :title="$t('header.settings')" :aria-label="$t('header.settings')">⚙</button>
        <button class="header-btn" @click="auth.logout()" v-if="auth.isLoggedIn" :aria-label="auth.user?.username">{{ auth.user?.username }}</button>
        <button class="header-btn" @click="showSearch = true; $nextTick(() => searchDialogRef?.focus())" :aria-label="$t('header.search')">🔍</button>
        <button class="header-btn" @click="toggleTheme" :aria-label="$t('common.toggleTheme')">◐</button>
      </div>
    </header>
    <nav class="museum-nav" :class="{ 'nav-open': mobileNavOpen }" aria-label="Main navigation">
      <router-link to="/" @click="mobileNavOpen = false">{{ $t('nav.home') }}</router-link><span class="nav-sep">|</span>
      <router-link to="/gaoshu" @click="mobileNavOpen = false">{{ $t('nav.exhibits') }}</router-link><span class="nav-sep">|</span>
      <router-link to="/mathematicians" @click="mobileNavOpen = false">{{ $t('nav.mathematicians') }}</router-link>
      <router-link to="/workshop" @click="mobileNavOpen = false">{{ $t('nav.workshop') }}</router-link>
      <router-link to="/fractal" @click="mobileNavOpen = false">{{ $t('nav.fractal') }}</router-link>
      <router-link to="/news" @click="mobileNavOpen = false">{{ $t('nav.news') }}</router-link>
      <router-link to="/practice" @click="mobileNavOpen = false">{{ $t('nav.practice') }}</router-link>
    </nav>
    <main id="main-content"><router-view /></main>
    <footer class="site-footer" style="text-align:center">
      <a href="https://beian.miit.gov.cn" target="_blank">{{ $t('footer.beian') }}</a>
    </footer>
    <LoginDialog v-if="auth.showLogin" />
    <SettingsDialog v-if="auth.showSettings" @close="auth.closeSettings()" />
    <SearchDialog v-if="showSearch" @close="showSearch = false" ref="searchDialogRef" />
    <button class="back-top" v-show="showBackTop" @click="scrollTop" aria-label="Back to top">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
    </button>
    <div class="nav-overlay" v-show="mobileNavOpen" @click="mobileNavOpen = false"></div>
    <ChatDialog />
    <ToastNotification />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, defineAsyncComponent } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'
const LoginDialog = defineAsyncComponent(() => import('@/components/LoginDialog.vue'))
const SettingsDialog = defineAsyncComponent(() => import('@/components/SettingsDialog.vue'))
const SearchDialog = defineAsyncComponent(() => import('@/components/SearchDialog.vue'))
const ToastNotification = defineAsyncComponent(() => import('@/components/ToastNotification.vue'))
const ChatDialog = defineAsyncComponent(() => import('@/components/ChatDialog.vue'))

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuth()
const showSearch = ref(false)
const searchDialogRef = ref(null)
const showBackTop = ref(false)
const mobileNavOpen = ref(false)

const localeLabel = computed(() => locale.value === 'zh' ? 'EN' : '中')

function toggleLang() {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('mathlearnlab:lang', locale.value)
  document.documentElement.lang = locale.value
}

function toggleTheme() {
  const html = document.documentElement
  const cur = html.getAttribute('data-theme') || 'light'
  const next = cur === 'light' ? 'dark' : 'light'
  html.setAttribute('data-theme', next)
  localStorage.setItem('mathlearnlab:theme', next)
}

function onScroll() { showBackTop.value = window.scrollY > 300 }
function scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }

let logoClicks = 0, logoTimer = null
function onLogoClick() {
  logoClicks++
  clearTimeout(logoTimer)
  logoTimer = setTimeout(() => { logoClicks = 0 }, 2000)
  if (logoClicks >= 7) { logoClicks = 0; router.push('/admin') }
}

onMounted(() => {
  const saved = localStorage.getItem('mathlearnlab:theme')
  if (saved) document.documentElement.setAttribute('data-theme', saved)
  else if (window.matchMedia('(prefers-color-scheme: dark)').matches)
    document.documentElement.setAttribute('data-theme', 'dark')
  window.addEventListener('scroll', onScroll)
  if (!auth.isLoggedIn && route.name !== 'admin') setTimeout(() => auth.openLogin(), 300)
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))

watch([route, locale], () => {
  const titleKey = route.meta?.titleKey
  document.title = (titleKey ? t(titleKey) + ' — ' : '') + t('header.brand')
}, { immediate: true })
</script>

<style>
@import '@/assets/base.css';
.skip-link { position:absolute; top:-40px; left:8px; z-index:1000; background:var(--accent); color:#fff; padding:8px 16px; border-radius:0 0 6px 6px; font-size:13px; text-decoration:none; transition:top 0.2s; }
.skip-link:focus { top:0; }
.lang-switch { font-weight:600; font-size:12px; letter-spacing:0.5px; width:auto; padding:0 10px; border-color:var(--accent); color:var(--accent); }
.back-top {
  position:fixed; bottom:32px; right:32px; z-index:50;
  width:40px; height:40px; border-radius:50%;
  border:1px solid var(--border); background:var(--bg-card);
  color:var(--text-secondary); cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 2px 8px rgba(0,0,0,0.08);
  transition:all 0.2s;
}
.back-top:hover { border-color:var(--accent); color:var(--accent); transform:translateY(-2px); box-shadow:0 4px 14px rgba(0,0,0,0.12); }
.hamburger { display:none; font-size:18px; }
.nav-overlay { display:none; }
@media(max-width:768px) {
  .hamburger { display:inline-flex; }
  .museum-nav { display:none; flex-direction:column; position:absolute; top:56px; left:0; right:0; background:var(--bg-card); border-bottom:1px solid var(--border); z-index:100; padding:8px 0; }
  .museum-nav.nav-open { display:flex; }
  .museum-nav .nav-sep { display:none; }
  .museum-nav a { padding:10px 20px; border:none; border-radius:0; }
  .nav-overlay { display:block; position:fixed; inset:0; z-index:99; background:rgba(0,0,0,0.3); }
}
</style>
