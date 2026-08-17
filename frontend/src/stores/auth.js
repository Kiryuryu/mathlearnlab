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
  // Whether the server has its own DeepSeek key configured (production).
  // When true, AI features work without the user providing a key.
  const serverAi = ref(false)
  const aiDailyLimit = ref(60)

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  // In production the server key powers AI, so a personal key is optional.
  const hasModel = computed(() => serverAi.value || (!!apiKey.value && !!model.value))

  // Probe /api/config/ai to learn whether server-side AI is available.
  // Runs once per app load; safe to call even when not logged in.
  let aiConfigPromise = null
  function loadAiConfig() {
    if (!aiConfigPromise) {
      aiConfigPromise = fetch('/api/config/ai')
        .then(r => r.ok ? r.json() : null)
        .then(cfg => {
          if (cfg) {
            serverAi.value = !!cfg.server_ai
            if (cfg.ai_daily_limit) aiDailyLimit.value = cfg.ai_daily_limit
          }
        })
        .catch(() => {})
        .finally(() => {})
    }
    return aiConfigPromise
  }

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
      // Attach the HTTP status so the dialog can show a friendly message.
      const err = new Error(detail)
      err.status = r.status
      throw err
    }
    const d = await r.json()
    setToken(d.token, d.user)
    showLogin.value = false
  }

  function setToken(newToken, newUser) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('mathlearnlab:token', newToken)
    localStorage.setItem('mathlearnlab:user', JSON.stringify(newUser))
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

  return { token, user, showLogin, loginTab, showSettings, showAiSetup, apiKey, model, serverAi, aiDailyLimit, isLoggedIn, hasModel, loadAiConfig, openLogin, closeLogin, openSettings, closeSettings, openAiSetup, closeAiSetup, doLogin, doRegister, setToken, setModelConfig, logout }
})
