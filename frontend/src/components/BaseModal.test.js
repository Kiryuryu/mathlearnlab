import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModal from './BaseModal.vue'

describe('BaseModal', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('renders slot content', () => {
    const wrapper = mount(BaseModal, { slots: { default: '<p>hello</p>' } })
    expect(wrapper.text()).toContain('hello')
  })

  it('emits close on Escape key', async () => {
    const wrapper = mount(BaseModal, { slots: { default: '<button>ok</button>' } })
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close on overlay click', async () => {
    const wrapper = mount(BaseModal, { slots: { default: '<p>content</p>' } })
    await wrapper.find('.base-overlay').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('does not emit close on overlay click when closeOnOverlay=false', async () => {
    const wrapper = mount(BaseModal, { props: { closeOnOverlay: false }, slots: { default: '<p>c</p>' } })
    await wrapper.find('.base-overlay').trigger('click')
    expect(wrapper.emitted('close')).toBeFalsy()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })
})
