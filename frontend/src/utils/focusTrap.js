import { onMounted, onUnmounted } from 'vue'

export function useFocusTrap(containerRef) {
  let firstFocusable, lastFocusable, previousActiveElement

  function getFocusableElements(el) {
    return Array.from(el.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ))
  }

  function handleKeydown(e) {
    if (e.key !== 'Tab') return
    const focusables = getFocusableElements(containerRef.value)
    if (focusables.length === 0) return
    firstFocusable = focusables[0]
    lastFocusable = focusables[focusables.length - 1]

    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        e.preventDefault()
        lastFocusable.focus()
      }
    } else {
      if (document.activeElement === lastFocusable) {
        e.preventDefault()
        firstFocusable.focus()
      }
    }
  }

  onMounted(() => {
    previousActiveElement = document.activeElement
    setTimeout(() => {
      const focusables = getFocusableElements(containerRef.value)
      if (focusables.length > 0) focusables[0].focus()
    }, 100)
    window.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
    if (previousActiveElement) previousActiveElement.focus()
  })
}
