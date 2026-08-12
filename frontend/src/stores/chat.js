// Chat store — coordinates the AI tour-guide entry point between
// ExhibitView (the button) and ChatDialog (the panel). Keeps the
// guide target reactive so the dialog can react to it without props.
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', () => {
  const guideTarget = ref(null) // { key, name } | null

  function openGuide(target) {
    guideTarget.value = target
  }

  function clearGuide() {
    guideTarget.value = null
  }

  return { guideTarget, openGuide, clearGuide }
})
