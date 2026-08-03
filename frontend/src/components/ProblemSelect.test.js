import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import ProblemSelect from './ProblemSelect.vue'

const i18n = createI18n({
  legacy: true,
  locale: 'zh',
  messages: {
    zh: {
      practice: {
        topic: '主题', difficulty: '难度', generating: '生成中', aiGenerate: 'AI 出题',
        loginToUse: '登录后使用', select: '选题', solve: '作答', grade: '批改',
      },
    },
  },
})

const mountSelect = (props = {}) => mount(ProblemSelect, {
  props,
  global: { plugins: [i18n] },
})

describe('ProblemSelect', () => {
  it('renders topic options', () => {
    const wrapper = mountSelect({ isLoggedIn: true })
    const opts = wrapper.findAll('option')
    expect(opts.length).toBe(5) // 5 subtopics
  })

  it('emits generate on button click', async () => {
    const wrapper = mountSelect({ isLoggedIn: true })
    await wrapper.find('.btn-lg').trigger('click')
    expect(wrapper.emitted('generate')).toBeTruthy()
  })

  it('emits update:filter when difficulty clicked', async () => {
    const wrapper = mountSelect({ isLoggedIn: true, filter: 'basic' })
    const filters = wrapper.findAll('.filters button')
    await filters[2].trigger('click') // exam
    expect(wrapper.emitted('update:filter')[0]).toEqual(['exam'])
  })

  it('shows lock label when not logged in', () => {
    const wrapper = mountSelect({ isLoggedIn: false })
    expect(wrapper.text()).toContain('登录后使用')
  })
})
