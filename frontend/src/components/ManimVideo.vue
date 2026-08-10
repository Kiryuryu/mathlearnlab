<template>
  <div class="manim-video">
    <div class="mv-wrap" @click="open">
      <video :src="src" loop muted playsinline preload="metadata" :poster="poster" @mouseenter="$event.target.play()" @mouseleave="$event.target.pause()" @click.stop="open"></video>
      <span class="mv-play">▶ {{ $t('gallery.hoverPlay') }}</span>
      <span class="mv-zoom">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      </span>
    </div>
    <div v-if="active" class="lightbox" @click.self="close">
      <div class="lightbox-inner" @click.stop>
        <video :src="src" loop controls autoplay playsinline></video>
        <div class="lightbox-meta">
          <span class="lightbox-title">{{ title }}</span>
          <span class="lightbox-desc">{{ desc }}</span>
        </div>
        <button class="close-btn" @click="close" :aria-label="$t('gallery.close')">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
defineProps({ src: String, poster: String, title: String, desc: String })
const active = ref(false)
function open() { active.value = true }
function close() { active.value = false }
</script>

<style scoped>
.manim-video { margin: 16px 0; }
.mv-wrap {
  position: relative;
  background: #111;
  aspect-ratio: 16/9;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
  cursor: zoom-in;
  box-shadow: var(--shadow-card);
}
.mv-wrap video { width: 100%; height: 100%; object-fit: cover; display: block; }
.mv-play {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.85); font-size: 14px;
  background: rgba(0,0,0,0.25);
  pointer-events: none;
  transition: opacity 0.2s;
}
.mv-zoom {
  position: absolute; top: 10px; right: 10px;
  width: 30px; height: 30px; border-radius: 50%;
  background: rgba(0,0,0,0.55); color: #fff;
  display: flex; align-items: center; justify-content: center;
  pointer-events: none; opacity: 0; transition: opacity 0.2s;
}
.mv-wrap:hover .mv-zoom { opacity: 1; }
.mv-wrap:hover .mv-play { opacity: 0.2; }

.lightbox {
  position: fixed; inset: 0; z-index: 1200;
  background: rgba(0,0,0,0.88);
  display: flex; align-items: center; justify-content: center;
  padding: 24px; animation: lbFade 0.2s;
}
@keyframes lbFade { from { opacity: 0; } to { opacity: 1; } }
.lightbox-inner { position: relative; max-width: 96vw; width: 100%; }
.lightbox-inner video { width: 100%; max-height: 82vh; border-radius: 8px; background: #000; display: block; }
.lightbox-meta { margin-top: 12px; color: #fff; }
.lightbox-title { font-size: 17px; font-weight: 600; font-family: var(--font-heading); }
.lightbox-desc { display: block; font-size: 13px; color: rgba(255,255,255,0.7); margin-top: 4px; }
.close-btn {
  position: absolute; top: -14px; right: -14px;
  width: 36px; height: 36px; border-radius: 50%;
  border: none; background: var(--accent); color: #fff;
  font-size: 15px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.close-btn:hover { background: var(--accent-error); }
</style>
