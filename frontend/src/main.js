import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { useToast } from '@/utils/toast'
import { useAuth } from '@/stores/auth'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(i18n)

// Learn whether the server has AI configured (so hasModel works for guests).
useAuth(pinia).loadAiConfig()

function friendlyError(err) {
  const msg = err?.message || String(err || '')
  // Suppress abort/cancel errors (user-initiated, not real failures)
  if (msg.includes('AbortError') || msg.includes('aborted')) return
  try { useToast().show('⚠️ ' + msg.slice(0, 120), 'error', 5000) } catch {}
  console.error(err)
}

app.config.errorHandler = (err, _instance, _info) => {
  friendlyError(err)
}

window.addEventListener('unhandledrejection', (e) => {
  if (e?.reason) friendlyError(e.reason)
})

app.mount('#app')
