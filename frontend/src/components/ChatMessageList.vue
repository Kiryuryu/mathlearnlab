<template>
  <div class="chat-msgs" ref="scrollEl" @scroll="onScroll">
    <div v-for="m in messages" :key="m.id" :class="['msg', m.role]">
      <template v-if="m.role === 'assistant'">
        <div class="assistant-label">
          <span class="avatar"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>
          {{ t('chat.title') }}
        </div>
        <div class="bubble" v-html="m.html"></div>
        <div v-if="!m.isStreaming" class="msg-actions">
          <button class="msg-action-btn" @click="$emit('copy', m.content)" :title="t('chat.copy')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          </button>
          <button v-if="m.isError" class="msg-action-btn" @click="$emit('retry', m)" :title="t('chat.retry')">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          </button>
        </div>
      </template>
      <template v-else>
        <div class="bubble user-bubble" v-html="m.html"></div>
      </template>
    </div>
    <div v-if="streaming" class="msg assistant">
      <div class="assistant-label"><span class="avatar"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>{{ t('chat.title') }}</div>
      <div class="bubble" v-html="rendered(streamText)"></div>
    </div>
    <div v-if="messages.length === 0 && !streaming" class="msg hint">
      <div class="bubble">{{ t('chat.hint') }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { renderMarkdown } from '@/utils/markdown'

const { t } = useI18n()
const props = defineProps({ messages: { type: Array, default: () => [] }, streaming: { type: Boolean, default: false }, streamText: { type: String, default: '' } })
const emit = defineEmits(['copy', 'retry'])

const scrollEl = ref(null)
let userScrolledUp = false

function onScroll() {
  const el = scrollEl.value
  if (!el) return
  userScrolledUp = el.scrollHeight - el.scrollTop - el.clientHeight > 80
}

function scrollBottom() {
  if (userScrolledUp) return
  requestAnimationFrame(() => {
    const el = scrollEl.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

function rendered(text) {
  return renderMarkdown(text)
}

onMounted(() => {
  const el = scrollEl.value
  if (el) el.scrollTop = el.scrollHeight
})

watch(() => [props.messages.length, props.streamText, props.streaming], () => scrollBottom())

defineExpose({ scrollBottom })
</script>

<style scoped>
.chat-msgs { flex:1; min-height:0; overflow-y:auto; padding:16px 16px 12px; display:flex; flex-direction:column; gap:14px; }
.msg { display:flex; flex-direction:column; }
.msg.user { align-items:flex-end; }
.msg.hint { align-items:center; }
.msg.hint .bubble { background:var(--bg-nav); color:var(--text-muted); font-size:12px; text-align:center; padding:10px 16px; }
.assistant-label { display:flex; align-items:center; gap:5px; font-size:11px; color:var(--text-muted); margin-bottom:4px; font-weight:500; }
.avatar {
  width:18px; height:18px; border-radius:50%;
  background:var(--accent); color:#fff;
  display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;
}
.bubble { max-width:88%; padding:9px 14px; border-radius:14px; font-size:14px; line-height:1.65; word-wrap:break-word; }
.bubble :deep(p) { margin:4px 0; }
.bubble :deep(.katex-display) { margin:6px 0; overflow-x:auto; }
.user-bubble { background:var(--accent); color:#fff; border-radius:14px 14px 4px 14px; }
.assistant .bubble { background:var(--bg-nav); color:var(--text-primary); border-radius:4px 14px 14px 14px; border:1px solid var(--border); }
.msg-actions { display:flex; gap:4px; margin-top:6px; padding-left:2px; }
.msg-action-btn {
  background:none; border:none; cursor:pointer; opacity:0.35; padding:4px;
  color:var(--text-secondary); border-radius:6px; transition:all 0.15s;
}
.msg-action-btn:hover { opacity:1; background:var(--bg-nav); }
</style>
