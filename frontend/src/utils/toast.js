const toasts = []
let id = 0

export function useToast() {
  function show(msg, type = 'error', duration = 4000) {
    const tid = ++id
    toasts.push({ id: tid, msg, type })
    setTimeout(() => {
      const idx = toasts.findIndex(t => t.id === tid)
      if (idx !== -1) toasts.splice(idx, 1)
    }, duration)
  }
  return { toasts, show }
}
