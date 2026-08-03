import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { useToast } from '@/utils/toast'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

function friendlyError(err) {
  const msg = err?.message || String(err || '')
  // Suppress abort/cancel errors (user-initiated, not real failures)
  if (msg.includes('AbortError') || msg.includes('aborted')) return
  try { useToast().show('⚠️ ' + msg.slice(0, 120), 'error', 5000) } catch {}
  console.error(err)
}

app.config.errorHandler = (err, instance, info) => {
  friendlyError(err)
}

window.addEventListener('unhandledrejection', (e) => {
  if (e?.reason) friendlyError(e.reason)
})

app.mount('#app')
