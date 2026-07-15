import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuth = defineStore('auth', () => {
  const token = ref(localStorage.getItem('mathlearnlab:token') || '')
  const user = ref(JSON.parse(localStorage.getItem('mathlearnlab:user') || 'null'))
  const showLogin = ref(false)
  const loginTab = ref('register')
  const apiKey = ref(localStorage.getItem('mathlearnlab:apikey') || '')
  const model = ref(localStorage.getItem('museum:model') || 'deepseek-chat')

  const isLoggedIn = computed(() => !!token.value && !!user.value)

  function openLogin(tab = 'register') {
    loginTab.value = tab
    showLogin.value = true
  }
  function closeLogin() { showLogin.value = false }

  async function doLogin(username, password) {
    const r = await fetch('/api/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    if (!r.ok) throw new Error((await r.json()).detail || 'Login failed')
    const d = await r.json()
    token.value = d.token; user.value = d.user
    localStorage.setItem('mathlearnlab:token', d.token)
    localStorage.setItem('mathlearnlab:user', JSON.stringify(d.user))
    showLogin.value = false
  }

  async function doRegister(username, password, email, m, key) {
    const r = await fetch('/api/auth/register', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, email })
    })
    if (!r.ok) throw new Error((await r.json()).detail || 'Register failed')
    const d = await r.json()
    token.value = d.token; user.value = d.user
    apiKey.value = key; model.value = m
    localStorage.setItem('mathlearnlab:token', d.token)
    localStorage.setItem('mathlearnlab:user', JSON.stringify(d.user))
    localStorage.setItem('mathlearnlab:apikey', key)
    localStorage.setItem('museum:model', m)
    showLogin.value = false
  }

  function logout() {
    localStorage.removeItem('mathlearnlab:token')
    localStorage.removeItem('mathlearnlab:user')
    token.value = ''; user.value = null
    showLogin.value = true; loginTab.value = 'register'
  }

  return { token, user, showLogin, loginTab, apiKey, model, isLoggedIn, openLogin, closeLogin, doLogin, doRegister, logout }
})
