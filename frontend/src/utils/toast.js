import { ref } from 'vue'

const toasts = ref([])
let id = 0

export function useToast() {
  function show(msg, type = 'error', duration = 4000) {
    const tid = ++id
    toasts.value.push({ id: tid, msg, type })
    setTimeout(() => { toasts.value = toasts.value.filter(t => t.id !== tid) }, duration)
  }
  return { toasts, show }
}
