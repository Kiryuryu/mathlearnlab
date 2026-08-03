<template>
  <div class="chat-msgs" ref="scrollEl" @scroll="onScroll">
    <div v-for="m in messages" :key="m.id" :class="['msg', m.role]">
      <div class="bubble" v-html="m.html"></div>
      <div v-if="m.role === 'assistant' && !m.isStreaming" class="msg-actions">
        <button class="msg-action-btn" @click="$emit('copy', m.content)" :title="t('chat.copy')">📋</button>
        <button v-if="m.isError" class="msg-action-btn" @click="$emit('retry', m)" :title="t('chat.retry')">🔄</button>
      </div>
    </div>
    <div v-if="streaming" class="msg assistant">
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
</style>
