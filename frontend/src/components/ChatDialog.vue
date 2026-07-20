<template>
  <button v-if="!panelOpen" class="chat-fab" @click="openPanel" :aria-label="$t('chat.title')">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </button>

  <div v-if="panelOpen" class="chat-overlay" @click.self="panelOpen = false">
    <div class="chat-panel" ref="panelRef">
      <header>
        <h3>{{ $t('chat.title') }}</h3>
        <span class="chat-context" v-if="contextLabel">{{ contextLabel }}</span>
        <button v-if="messages.length" class="chat-header-btn" @click="clearConversation" :title="$t('chat.clear')">🗑</button>
        <button class="chat-close" @click="panelOpen = false">✕</button>
      </header>
      <div class="chat-msgs" ref="msgList" @scroll="onScroll">
        <div v-for="m in messages" :key="m.id" :class="['msg', m.role]">
          <div class="bubble" v-html="m.html"></div>
          <div v-if="m.role === 'assistant' && !m.isStreaming" class="msg-actions">
            <button class="msg-action-btn" @click="copyContent(m.content)" :title="$t('chat.copy')">📋</button>
            <button v-if="m.isError" class="msg-action-btn" @click="retry(m)" :title="$t('chat.retry')">🔄</button>
          </div>
        </div>
        <div v-if="streaming" class="msg assistant">
          <div class="bubble" v-html="rendered(streamText)"></div>
        </div>
        <div v-if="messages.length === 0 && !streaming" class="msg hint">
          <div class="bubble">{{ $t('chat.hint') }}</div>
        </div>
      </div>
      <form class="chat-input" @submit.prevent="send">
        <input v-model="input" :placeholder="$t('chat.placeholder')" :disabled="streaming" @keydown.enter.prevent="send" />
        <button type="submit" :disabled="!input.trim() || streaming">{{ $t('chat.send') }}</button>
      </form>
    </div>
  </div>

  <AiSetupGuide v-if="auth.showAiSetup" @close="auth.closeAiSetup" @proceed="finishSetup" />
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
import { renderMarkdown } from '@/utils/markdown'
import { useFocusTrap } from '@/utils/focusTrap'

const { t } = useI18n()
const route = useRoute()
const auth = useAuth()

const panelOpen = ref(false)
const input = ref('')
const messages = ref([])
const streaming = ref(false)
const streamText = ref('')
const msgList = ref(null)
const panelRef = ref(null)
let msgId = 0
let abortCtrl = null
let userScrolledUp = false
useFocusTrap(panelRef)

const contextLabel = computed(() => {
  const name = route.name
  if (!name) return ''
  const labels = {
    home: t('nav.home'), gaoshu: t('nav.exhibits'), exhibit: t('nav.exhibits'),
    workshop: t('nav.workshop'), fractal: t('nav.fractal'), gallery: t('gallery.title'),
    mathematicians: t('nav.mathematicians'), mathematician: t('nav.mathematicians'),
    practice: t('nav.practice'), news: t('nav.news'), admin: t('admin.title'),
  }
  return labels[name] || ''
})

function onScroll() {
  const el = msgList.value
  if (!el) return
  const threshold = 80
  userScrolledUp = el.scrollHeight - el.scrollTop - el.clientHeight > threshold
}

function addMsg(role, content, opts = {}) {
  const id = ++msgId
  const m = { id, role, content, html: renderMarkdown(content), isError: !!opts.isError, isStreaming: false }
  messages.value.push(m)
  return m
}

function rendered(text) {
  return renderMarkdown(text)
}

function scrollBottom() {
  if (userScrolledUp) return
  nextTick(() => {
    const el = msgList.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

function clearConversation() {
  messages.value = []
}

function copyContent(text) {
  navigator.clipboard.writeText(text).catch(() => {})
}

function retry(msg) {
  const idx = messages.value.indexOf(msg)
  if (idx < 0) return
  const userMsg = messages.value.slice(0, idx).filter(m => m.role === 'user').pop()
  if (!userMsg) return
  messages.value.splice(idx)
  input.value = userMsg.content
  send()
}

function openPanel() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  if (!auth.hasModel) { pendingSetup.value = true; auth.openAiSetup(); return }
  doOpen()
}
let pendingSetup = false
function doOpen() {
  panelOpen.value = true
  scrollBottom()
}
function finishSetup() {
  auth.closeAiSetup()
  if (pendingSetup) { pendingSetup = false; doOpen() }
}

watch(panelOpen, (v) => {
  if (v) scrollBottom()
})

async function send() {
  const text = input.value.trim()
  if (!text || streaming.value) return
  input.value = ''
  addMsg('user', text)
  streamText.value = ''
  streaming.value = true
  scrollBottom()

  const ctx = contextLabel.value ? `${t('chat.contextPrefix')} ${contextLabel.value}` : ''
  abortCtrl = new AbortController()
  try {
    const r = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': auth.apiKey || '',
        'Authorization': `Bearer ${auth.token}`,
      },
      body: JSON.stringify({
        messages: messages.value.filter(m => m.role !== 'hint').map(m => ({ role: m.role, content: m.content })),
        model: auth.model,
        context_route: ctx,
        lang: t('chat.lang'),
      }),
      signal: abortCtrl.signal,
    })
    if (!r.ok) {
      const err = await r.json().catch(() => ({ detail: t('chat.error') }))
      addMsg('assistant', `**${t('chat.error')}** ${err.detail || t('chat.error')}`, { isError: true })
      streaming.value = false
      scrollBottom()
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
            streamText.value = `**${t('chat.error')}** ${parsed.error}`
            break
          }
        } catch {
          streamText.value += data
        }
      }
      scrollBottom()
    }
  } catch(e) {
    if (e.name !== 'AbortError') {
      addMsg('assistant', `**${t('chat.error')}** ${e.message}`, { isError: true })
    }
  }
  if (streamText.value) {
    addMsg('assistant', streamText.value)
  }
  streamText.value = ''
  streaming.value = false
  abortCtrl = null
  scrollBottom()
}
</script>

<style scoped>
.chat-fab {
  position:fixed; bottom:80px; right:32px; z-index:100;
  width:44px; height:44px; border-radius:50%;
  background:var(--accent); color:#fff; border:none;
  display:flex; align-items:center; justify-content:center;
  cursor:pointer; box-shadow:0 4px 16px rgba(0,0,0,0.2);
  transition:transform 0.2s;
}
.chat-fab:hover { transform:scale(1.08); }
.chat-overlay {
  position:fixed; inset:0; z-index:500;
  display:flex; align-items:flex-end; justify-content:flex-end;
  padding:16px; pointer-events:none;
}
.chat-panel {
  width:380px; max-width:calc(100vw - 32px);
  height:520px; max-height:calc(100vh - 100px);
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:12px; box-shadow:0 8px 40px rgba(0,0,0,0.15);
  display:flex; flex-direction:column; pointer-events:auto;
  animation:slideUp 0.2s;
}
@keyframes slideUp { from{transform:translateY(20px);opacity:0} to{transform:translateY(0);opacity:1} }
header { display:flex; align-items:center; gap:6px; padding:14px 16px; border-bottom:1px solid var(--border); flex-shrink:0; }
header h3 { margin:0; font-size:15px; }
.chat-context { font-size:11px; color:var(--text-muted); flex:1; text-align:right; }
.chat-header-btn { background:none; border:none; font-size:14px; cursor:pointer; padding:2px 4px; opacity:0.5; }
.chat-header-btn:hover { opacity:1; }
.chat-close { background:none; border:none; font-size:16px; cursor:pointer; color:var(--text-muted); padding:4px; }
.chat-msgs { flex:1; overflow-y:auto; padding:12px 16px; display:flex; flex-direction:column; gap:8px; }
.msg { display:flex; flex-direction:column; }
.msg.user { align-items:flex-end; }
.msg.hint { align-items:center; }
.msg.hint .bubble { background:var(--bg-nav); color:var(--text-muted); font-size:12px; text-align:center; }
.bubble { max-width:85%; padding:8px 14px; border-radius:12px; font-size:14px; line-height:1.6; word-wrap:break-word; }
.bubble :deep(p) { margin:4px 0; }
.bubble :deep(.katex-display) { margin:6px 0; overflow-x:auto; }
.user .bubble { background:var(--accent); color:#fff; border-radius:12px 12px 4px 12px; }
.assistant .bubble { background:var(--bg-nav); color:var(--text-primary); border-radius:12px 12px 12px 4px; }
.msg-actions { display:flex; gap:4px; margin-top:4px; padding-left:8px; }
.msg-action-btn { background:none; border:none; font-size:12px; cursor:pointer; opacity:0.4; padding:2px; }
.msg-action-btn:hover { opacity:1; }
.chat-input { display:flex; gap:8px; padding:10px 12px; border-top:1px solid var(--border); flex-shrink:0; }
.chat-input input { flex:1; padding:8px 12px; border:1px solid var(--border); border-radius:20px; font-size:13px; outline:none; background:var(--bg-input); color:var(--text-primary); }
.chat-input input:focus { border-color:var(--accent); }
.chat-input button { padding:8px 16px; border:none; border-radius:20px; background:var(--accent); color:#fff; font-size:13px; cursor:pointer; }
.chat-input button:disabled { opacity:0.4; cursor:not-allowed; }
</style>
