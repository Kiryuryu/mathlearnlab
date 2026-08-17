// Composable: chat message state + SSE streaming logic (testable, UI-agnostic)
import { ref, computed } from 'vue'
import { renderMarkdown } from '@/utils/markdown'
import { apiFetch } from '@/utils/api'

export function useChatStream({ getModel, getLang, getContext, getGuide }) {
  const messages = ref([])
  const streaming = ref(false)
  const streamText = ref('')
  let msgId = 0
  let abortCtrl = null

  const hasMessages = computed(() => messages.value.length > 0)

  function addMsg(role, content, opts = {}) {
    const id = ++msgId
    const m = { id, role, content, html: renderMarkdown(content), isError: !!opts.isError, isStreaming: false }
    messages.value.push(m)
    return m
  }

  function rendered(text) {
    return renderMarkdown(text)
  }

  function clear() {
    messages.value = []
  }

  function copy(text) {
    navigator.clipboard.writeText(text).catch(() => {})
  }

  function retry(msg, onInput) {
    const idx = messages.value.indexOf(msg)
    if (idx < 0) return
    const userMsg = messages.value.slice(0, idx).filter(m => m.role === 'user').pop()
    if (!userMsg) return
    messages.value.splice(idx)
    onInput(userMsg.content)
    sendText(userMsg.content)
  }

  async function sendText(text, { onScroll } = {}) {
    if (!text || streaming.value) return
    addMsg('user', text)
    streamText.value = ''
    streaming.value = true
    onScroll && onScroll()

    const ctx = getContext()
    const lang = getLang()
    const guide = getGuide ? getGuide() : null
    abortCtrl = new AbortController()
    try {
      // Send only the most recent 30 turns — matches the server-side cap and
      // keeps request bodies from growing without bound.
      const history = messages.value.filter(m => m.role !== 'hint').map(m => ({ role: m.role, content: m.content }))
      const payload = history.slice(-30)
      const r = await apiFetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: payload,
          model: getModel(),
          context_route: ctx,
          lang,
          guide_mode: guide ? true : undefined,
          exhibit_key: guide ? guide.key : undefined,
          exhibit_name: guide ? guide.name : undefined,
        }),
        signal: abortCtrl.signal,
      })
      if (!r.ok) {
        const err = await r.json().catch(() => ({ detail: lang === 'zh' ? '请求失败' : 'Request failed' }))
        addMsg('assistant', `**${lang === 'zh' ? '错误' : 'Error'}** ${err.detail || ''}`, { isError: true })
        streaming.value = false
        onScroll && onScroll()
        return
      }

      const reader = r.body.getReader()
      const decoder = new TextDecoder()
      let buf = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const lines = buf.split('\n\n')
        buf = lines.pop() || ''
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const data = line.slice(6)
          if (data === '[DONE]') break
          try {
            const parsed = JSON.parse(data)
            if (parsed.error) {
              streamText.value = `**${lang === 'zh' ? '错误' : 'Error'}** ${parsed.error}`
              break
            }
          } catch {
            streamText.value += data
          }
        }
        onScroll && onScroll()
      }
    } catch(e) {
      if (e.name !== 'AbortError') {
        addMsg('assistant', `**${lang === 'zh' ? '错误' : 'Error'}** ${e.message}`, { isError: true })
      }
    }
    if (streamText.value) {
      addMsg('assistant', streamText.value)
    }
    streamText.value = ''
    streaming.value = false
    abortCtrl = null
    onScroll && onScroll()
  }

  return { messages, streaming, streamText, hasMessages, addMsg, rendered, clear, copy, retry, sendText }
}
