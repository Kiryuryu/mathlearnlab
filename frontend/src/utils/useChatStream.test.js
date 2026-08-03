import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChatStream } from './useChatStream'

vi.mock('./api', () => ({
  apiFetch: vi.fn(),
}))

// Use the mocked apiFetch
import { apiFetch } from './api'
const mockFetch = apiFetch

vi.stubGlobal('navigator', { clipboard: { writeText: vi.fn().mockResolvedValue() } })

const makeStream = () => useChatStream({
  getApiKey: () => 'key',
  getModel: () => 'deepseek-chat',
  getLang: () => 'zh',
  getContext: () => 'context',
})

describe('useChatStream', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('addMsg pushes a rendered message', () => {
    const s = makeStream()
    const m = s.addMsg('user', 'hello')
    expect(m.role).toBe('user')
    expect(m.content).toBe('hello')
    expect(s.messages.value.length).toBe(1)
  })

  it('clear empties messages', () => {
    const s = makeStream()
    s.addMsg('user', 'a')
    s.addMsg('assistant', 'b')
    expect(s.hasMessages.value).toBe(true)
    s.clear()
    expect(s.messages.value.length).toBe(0)
    expect(s.hasMessages.value).toBe(false)
  })

  it('sendText sends user message and calls API', async () => {
    const s = makeStream()
    const mockRes = {
      ok: true,
      body: { getReader: () => ({ read: async () => ({ done: true, value: undefined }) }) },
    }
    mockFetch.mockResolvedValue(mockRes)

    await s.sendText('问题')
    expect(mockFetch).toHaveBeenCalledTimes(1)
    expect(s.messages.value[0].role).toBe('user')
    expect(s.messages.value[0].content).toBe('问题')
    expect(s.streaming.value).toBe(false)
  })

  it('sendText ignores empty text', async () => {
    const s = makeStream()
    await s.sendText('')
    expect(mockFetch).not.toHaveBeenCalled()
  })
})
