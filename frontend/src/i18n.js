import { createI18n } from 'vue-i18n'
import zh from './locales/zh'
import en from './locales/en'

const savedLang = localStorage.getItem('mathlearnlab:lang') || 'zh'

export default createI18n({
  locale: savedLang,
  fallbackLocale: 'zh',
  messages: { zh, en },
})
