<template>
  <div class="base-overlay" :class="{ 'base-overlay-top': alignTop }" @click.self="onOverlayClick">
    <div class="base-panel" :class="panelClass" ref="panelRef">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useFocusTrap } from '@/utils/focusTrap'

const props = defineProps({
  // Optional alignment/width variant applied to the panel
  panelClass: { type: String, default: '' },
  // If true, clicking the overlay also emits close (default modal behavior)
  closeOnOverlay: { type: Boolean, default: true },
  // Align panel near the top instead of centered
  alignTop: { type: Boolean, default: false },
})
const emit = defineEmits(['close'])

const panelRef = ref(null)
useFocusTrap(panelRef)

function onOverlayClick() {
  if (props.closeOnOverlay) emit('close')
}

function onKeydown(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.base-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  animation: baseFadeIn 0.15s;
}
.base-overlay-top { align-items: flex-start; padding-top: 10vh; }
@keyframes baseFadeIn { from { opacity: 0; } to { opacity: 1; } }
.base-panel {
  background: var(--bg-card); border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  animation: baseSlideIn 0.2s;
}
@keyframes baseSlideIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
