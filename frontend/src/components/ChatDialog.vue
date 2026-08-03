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
        <button type="submit" :disabled="!input.trim() || chat.streaming">{{ $t('chat.send') }}</button>
      </form>
    </div>
  </div>

  <AiSetupGuide v-if="auth.showAiSetup" @close="auth.closeAiSetup" @proceed="finishSetup" />
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/stores/auth'
import { useFocusTrap } from '@/utils/focusTrap'
import { useChatStream } from '@/utils/useChatStream'
import ChatMessageList from '@/components/ChatMessageList.vue'
import AiSetupGuide from '@/components/AiSetupGuide.vue'

const { t, locale } = useI18n()
const route = useRoute()
const auth = useAuth()

const panelOpen = ref(false)
const input = ref('')
const panelRef = ref(null)
useFocusTrap(panelRef)

const chat = useChatStream({
  getModel: () => auth.model,
  getLang: () => locale.value,
  getContext: () => contextLabel.value ? `${t('chat.contextPrefix')} ${contextLabel.value}` : '',
})

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
.chat-input { display:flex; gap:8px; padding:10px 12px; border-top:1px solid var(--border); flex-shrink:0; }
.chat-input input { flex:1; padding:8px 12px; border:1px solid var(--border); border-radius:20px; font-size:13px; outline:none; background:var(--bg-input); color:var(--text-primary); }
.chat-input input:focus { border-color:var(--accent); }
.chat-input button { padding:8px 16px; border:none; border-radius:20px; background:var(--accent); color:#fff; font-size:13px; cursor:pointer; }
.chat-input button:disabled { opacity:0.4; cursor:not-allowed; }
</style>
