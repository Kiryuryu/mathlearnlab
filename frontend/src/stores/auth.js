import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuth = defineStore('auth', () => {
  const token = ref(localStorage.getItem('mathlearnlab:token') || '')
  const user = ref(JSON.parse(localStorage.getItem('mathlearnlab:user') || 'null'))
  const showLogin = ref(false)
  const loginTab = ref('register')
  const showSettings = ref(false)
  const showAiSetup = ref(false)
  const apiKey = ref(localStorage.getItem('mathlearnlab:apikey') || '')
  const model = ref(localStorage.getItem('mathlearnlab:model') || 'deepseek-chat')

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const hasModel = computed(() => !!apiKey.value && !!model.value)

  function openLogin(tab = 'register') {
    loginTab.value = tab
    showLogin.value = true
  }
  function closeLogin() { showLogin.value = false }
  function openSettings() { showSettings.value = true }
  function closeSettings() { showSettings.value = false }
  function openAiSetup() { showAiSetup.value = true }
  function closeAiSetup() { showAiSetup.value = false }

  async function doLogin(username, password) {
    const r = await fetch('/api/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    if (!r.ok) {
      let detail = 'Login failed'
      try { detail = (await r.json()).detail || detail } catch {}
      throw new Error(detail)
    }
    const d = await r.json()
    token.value = d.token; user.value = d.user
    localStorage.setItem('mathlearnlab:token', d.token)
    localStorage.setItem('mathlearnlab:user', JSON.stringify(d.user))
    showLogin.value = false
  }

  async function doRegister(username, password, email) {
    const r = await fetch('/api/auth/register', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, email })
    })
    let d
    try { d = await r.json() } catch { d = {} }
    if (!r.ok) throw new Error(d.detail || 'Register failed')
    showLogin.value = false
    return d.message || '注册成功，等待审核'
  }

  function logout() {
    localStorage.removeItem('mathlearnlab:token')
    localStorage.removeItem('mathlearnlab:user')
    token.value = ''; user.value = null
    showLogin.value = true; loginTab.value = 'register'
  }

  function setModelConfig(m, key) {
    model.value = m; apiKey.value = key
    localStorage.setItem('mathlearnlab:model', m)
    localStorage.setItem('mathlearnlab:apikey', key)
  }

  return { token, user, showLogin, loginTab, showSettings, showAiSetup, apiKey, model, isLoggedIn, hasModel, openLogin, closeLogin, openSettings, closeSettings, openAiSetup, closeAiSetup, doLogin, doRegister, setModelConfig, logout }
})
