import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Error]', err, info)
}

window.addEventListener('unhandledrejection', (e) => {
  console.error('[Unhandled Promise]', e.reason)
})

app.mount('#app')
