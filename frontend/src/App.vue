<template>
  <div>
    <header class="app-header">
      <div class="header-left">
        <router-link to="/" class="app-brand">数学博物馆</router-link>
        <span class="app-subtitle">知其然，知其所以然</span>
      </div>
      <div class="header-right">
        <button class="header-btn" @click="auth.openLogin()" v-if="!auth.isLoggedIn">登录</button>
        <button class="header-btn" @click="auth.logout()" v-else>{{ auth.user?.username }}</button>
        <button class="header-btn" @click="searchOpen = !searchOpen">🔍</button>
        <button class="header-btn" @click="toggleTheme">◐</button>
      </div>
    </header>
    <nav class="museum-nav">
      <router-link to="/">大厅</router-link><span class="nav-sep">|</span>
      <router-link to="/gaoshu">展区</router-link><span class="nav-sep">|</span>
      <router-link to="/mathematicians">数学家长廊</router-link>
      <router-link to="/workshop">函数工坊</router-link>
      <router-link to="/fractal">分形</router-link>
      <router-link to="/practice">练习</router-link>
    </nav>
    <main><router-view /></main>
    <footer class="site-footer">
      <a href="https://beian.miit.gov.cn" target="_blank">蜀ICP备2026039520号</a>
    </footer>
    <LoginDialog v-if="auth.showLogin" />
    <button class="back-top" v-show="showBackTop" @click="scrollTop">↑</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuth } from '@/stores/auth'
import LoginDialog from '@/components/LoginDialog.vue'

const auth = useAuth()
const searchOpen = ref(false)
const showBackTop = ref(false)

function toggleTheme() {
  const html = document.documentElement
  const cur = html.getAttribute('data-theme') || 'light'
  const next = cur === 'light' ? 'dark' : 'light'
  html.setAttribute('data-theme', next)
  localStorage.setItem('mathlearnlab:theme', next)
}

function onScroll() { showBackTop.value = window.scrollY > 300 }
function scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }

onMounted(() => {
  const saved = localStorage.getItem('mathlearnlab:theme')
  if (saved) document.documentElement.setAttribute('data-theme', saved)
  else if (window.matchMedia('(prefers-color-scheme: dark)').matches)
    document.documentElement.setAttribute('data-theme', 'dark')
  window.addEventListener('scroll', onScroll)
  if (!auth.isLoggedIn) setTimeout(() => auth.openLogin(), 300)
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style>
@import '@/assets/base.css';
</style>
