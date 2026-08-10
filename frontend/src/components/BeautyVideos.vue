<template>
  <div class="beauty-videos">
    <h2>{{ $t('gallery.videos') }}</h2>
    <div class="video-grid">
      <figure v-for="v in videos" :key="v.src" class="video-card" @click="open(v)">
        <div class="video-wrap">
          <video :src="v.src" loop muted playsinline preload="metadata" :poster="v.poster" @mouseenter="$event.target.play()" @mouseleave="$event.target.pause()" @click.stop="open(v)"></video>
          <span class="play-hint">▶ {{ $t('gallery.hoverPlay') }}</span>
          <span class="zoom-hint">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
          </span>
        </div>
        <figcaption>
          <span class="video-title">{{ v.title }}</span>
          <span class="video-desc">{{ v.desc }}</span>
        </figcaption>
      </figure>
    </div>

    <!-- Fullscreen preview -->
    <div v-if="active" class="lightbox" @click.self="close">
      <div class="lightbox-inner" @click.stop>
        <video :src="active.src" loop controls autoplay playsinline></video>
        <div class="lightbox-meta">
          <span class="lightbox-title">{{ active.title }}</span>
          <span class="lightbox-desc">{{ active.desc }}</span>
        </div>
        <button class="close-btn" @click="close" :aria-label="$t('gallery.close')">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const base = '/static/videos/'
const videos = [
  { src: base + 'EulerIdentity.mp4', poster: base + 'EulerIdentity.jpg', title: () => locale.value === 'en' ? "Euler's Identity" : '欧拉恒等式', desc: () => locale.value === 'en' ? 'e^(iπ) + 1 = 0 — rotating on the unit circle' : 'e^(iπ)+1=0 —— 单位圆上的旋转' },
  { src: base + 'FourierSeries.mp4', poster: base + 'FourierSeries.jpg', title: () => locale.value === 'en' ? 'Fourier Series' : '傅里叶级数', desc: () => locale.value === 'en' ? 'Square wave from sines' : '用正弦波拼出方波' },
  { src: base + 'RiemannSum.mp4', poster: base + 'RiemannSum.jpg', title: () => locale.value === 'en' ? 'Riemann Sum' : '黎曼和', desc: () => locale.value === 'en' ? 'Rectangles → integral' : '矩形逼近 → 定积分' },
  { src: base + 'FractalZoom.mp4', poster: base + 'FractalZoom.jpg', title: () => locale.value === 'en' ? 'Self-Similarity' : '自相似', desc: () => locale.value === 'en' ? 'Fractal zoom' : '分形缩放' },
]
const active = ref(null)
function open(v) { active.value = v }
function close() { active.value = null }
</script>

<style scoped>
.beauty-videos { margin-top: 40px; }
.beauty-videos h2 {
  text-align: center;
  font-size: 22px;
  margin-bottom: 20px;
  color: var(--text-primary);
}
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.video-card {
  margin: 0;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  cursor: zoom-in;
  transition: transform 0.2s ease, box-shadow 0.25s ease;
}
.video-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-elevated); }
.video-wrap { position: relative; background: #111; aspect-ratio: 16/9; }
.video-wrap video { width: 100%; height: 100%; object-fit: cover; display: block; }
.play-hint {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.85); font-size: 15px;
  background: rgba(0,0,0,0.25);
  pointer-events: none;
  transition: opacity 0.2s;
}
.zoom-hint {
  position: absolute; top: 10px; right: 10px;
  width: 32px; height: 32px;
  border-radius: 50%;
  background: rgba(0,0,0,0.55);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}
.video-card:hover .zoom-hint { opacity: 1; }
.video-card:hover .play-hint { opacity: 0.2; }
figcaption { padding: 14px 16px; }
.video-title { display: block; font-weight: 600; font-size: 15px; color: var(--text-primary); font-family: var(--font-heading); }
.video-desc { display: block; font-size: 12px; color: var(--text-muted); margin-top: 4px; }

/* Lightbox */
.lightbox {
  position: fixed; inset: 0; z-index: 1200;
  background: rgba(0,0,0,0.88);
  display: flex; align-items: center; justify-content: center;
  padding: 24px;
  animation: lbFade 0.2s;
}
@keyframes lbFade { from { opacity: 0; } to { opacity: 1; } }
.lightbox-inner { position: relative; max-width: 96vw; width: 100%; }
.lightbox-inner video {
  width: 100%;
  max-height: 82vh;
  border-radius: 8px;
  background: #000;
  display: block;
}
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
