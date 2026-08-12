<template>
  <button v-if="!panelOpen" class="chat-fab" @click="openPanel" :aria-label="$t('chat.title')">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </button>

  <div v-if="panelOpen" class="chat-overlay" @click.self="panelOpen = false">
    <div class="chat-panel" ref="panelRef">
      <header>
        <h3>{{ $t('chat.title') }}</h3>
        <span class="chat-context" v-if="contextLabel">{{ contextLabel }}</span>
        <button v-if="chat.hasMessages" class="chat-header-btn" @click="chat.clear()" :title="$t('chat.clear')">🗑</button>
        <button class="chat-close" @click="panelOpen = false">✕</button>
      </header>
      <ChatMessageList
        :messages="chat.messages"
        :streaming="chat.streaming"
        :stream-text="chat.streamText"
        @copy="chat.copy"
        @retry="onRetry"
      />
      <form class="chat-input" @submit.prevent="onSend">
        <input v-model="input" :placeholder="$t('chat.placeholder')" :disabled="chat.streaming" @keydown.enter.prevent="onSend" />
        <button type="submit" :disabled="!input.trim() || chat.streaming" :aria-label="$t('chat.send')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
        </button>
      </form>
    </div>
  </div>

  <AiSetupGuide v-if="auth.showAiSetup" @close="auth.closeAiSetup" @proceed="finishSetup" />
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { useFocusTrap } from '@/utils/focusTrap'
import { useChatStream } from '@/utils/useChatStream'
import ChatMessageList from '@/components/ChatMessageList.vue'
import AiSetupGuide from '@/components/AiSetupGuide.vue'

const { t, locale } = useI18n()
const route = useRoute()
const auth = useAuth()
const chatStore = useChatStore()

const panelOpen = ref(false)
const input = ref('')
const panelRef = ref(null)
useFocusTrap(panelRef)

const guideActive = computed(() => !!chatStore.guideTarget)

const chat = useChatStream({
  getModel: () => auth.model,
  getLang: () => locale.value,
  getContext: () => contextLabel.value ? `${t('chat.contextPrefix')} ${contextLabel.value}` : '',
  getGuide: () => chatStore.guideTarget ? { key: chatStore.guideTarget.key, name: chatStore.guideTarget.name } : null,
})

const contextLabel = computed(() => {
  if (guideActive.value) return chatStore.guideTarget.name
  const name = route.name
  if (!name) return ''
  const labels = {
    home: t('nav.home'), subject: t('nav.exhibits'), exhibit: t('nav.exhibits'),
    workshop: t('nav.workshop'), fractal: t('nav.fractal'), gallery: t('gallery.title'),
    mathematicians: t('nav.mathematicians'), mathematician: t('nav.mathematicians'),
    practice: t('nav.practice'), news: t('nav.news'), admin: t('admin.title'),
  }
  return labels[name] || ''
})

let pendingSetup = false
function openPanel() {
  if (!auth.isLoggedIn) { auth.openLogin('login'); return }
  if (!auth.hasModel) { pendingSetup = true; auth.openAiSetup(); return }
  panelOpen.value = true
}
function finishSetup() {
  auth.closeAiSetup()
  if (pendingSetup) { pendingSetup = false; panelOpen.value = true }
}

// Opening from a guide button starts a fresh, exhibit-focused conversation.
watch(() => chatStore.guideTarget, (target) => {
  if (target) {
    chat.clear()
    openPanel()
  }
})

// Opening the FAB manually resets guide mode to a free conversation.
watch(panelOpen, (open) => {
  if (open && !chatStore.guideTarget) return
  if (!open) { chatStore.clearGuide() }
})

function onSend() {
  const text = input.value.trim()
  if (!text || chat.streaming.value) return
  input.value = ''
  chat.sendText(text)
}

function onRetry(msg) {
  chat.retry(msg, (text) => { input.value = text })
}
</script>

<style scoped>
.chat-fab {
  position:fixed; bottom:80px; right:32px; z-index:100;
  width:48px; height:48px; border-radius:50%;
  background:var(--accent); color:#fff; border:none;
  display:flex; align-items:center; justify-content:center;
  cursor:pointer; box-shadow:var(--shadow-elevated);
  transition:transform 0.2s, box-shadow 0.2s;
}
.chat-fab:hover { transform:scale(1.08); box-shadow:0 8px 26px rgba(80,70,50,0.2); }
.chat-overlay {
  position:fixed; inset:0; z-index:500;
  display:flex; align-items:flex-end; justify-content:flex-end;
  padding:16px; pointer-events:none;
}
.chat-panel {
  width:400px; max-width:calc(100vw - 32px);
  height:540px; max-height:calc(100vh - 100px);
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:16px; box-shadow:0 12px 48px rgba(0,0,0,0.18);
  display:flex; flex-direction:column; pointer-events:auto;
  animation:slideUp 0.25s;
}
@keyframes slideUp { from{transform:translateY(24px);opacity:0} to{transform:translateY(0);opacity:1} }
header {
  display:flex; align-items:center; gap:8px; padding:16px 18px;
  border-bottom:1px solid var(--border); flex-shrink:0;
}
header h3 { margin:0; font-size:15px; font-weight:600; }
.chat-context { font-size:11px; color:var(--text-muted); flex:1; text-align:right; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.chat-header-btn { background:none; border:none; font-size:14px; cursor:pointer; padding:3px 5px; opacity:0.45; transition:opacity 0.15s; }
.chat-header-btn:hover { opacity:1; }
.chat-close { background:none; border:none; font-size:16px; cursor:pointer; color:var(--text-muted); padding:4px; }
.chat-close:hover { color:var(--text-primary); }
.chat-input { display:flex; gap:8px; padding:12px 14px; border-top:1px solid var(--border); flex-shrink:0; align-items:center; }
.chat-input input {
  flex:1; padding:9px 16px; border:1px solid var(--border); border-radius:22px;
  font-size:13px; outline:none; background:var(--bg-input); color:var(--text-primary);
  transition:border-color 0.15s;
}
.chat-input input:focus { border-color:var(--accent); }
.chat-input button {
  width:38px; height:38px; flex-shrink:0; padding:0; border:none; border-radius:50%;
  background:var(--accent); color:#fff; font-size:15px; cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  transition:opacity 0.15s, transform 0.1s;
}
.chat-input button:hover { opacity:0.9; transform:scale(1.05); }
.chat-input button:disabled { opacity:0.35; cursor:not-allowed; transform:none; }
</style>
