<template>
  <div class="beauty-videos">
    <h2>{{ $t('gallery.videos') }}</h2>
    <div class="video-grid">
      <figure v-for="v in videos" :key="v.src" class="video-card">
        <div class="video-wrap">
          <video :src="v.src" loop muted playsinline preload="metadata" :poster="v.poster" @mouseenter="$event.target.play()" @mouseleave="$event.target.pause()"></video>
          <span class="play-hint">▶ {{ $t('gallery.hoverPlay') }}</span>
        </div>
        <figcaption>
          <span class="video-title">{{ v.title }}</span>
          <span class="video-desc">{{ v.desc }}</span>
        </figcaption>
      </figure>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const base = '/static/videos/'
const videos = [
  { src: base + 'EulerIdentity.mp4', poster: base + 'EulerIdentity.jpg', title: () => locale.value === 'en' ? "Euler's Identity" : '欧拉恒等式', desc: () => locale.value === 'en' ? 'e^(iπ) + 1 = 0 — rotating on the unit circle' : 'e^(iπ)+1=0 —— 单位圆上的旋转' },
  { src: base + 'FourierSeries.mp4', poster: base + 'FourierSeries.jpg', title: () => locale.value === 'en' ? 'Fourier Series' : '傅里叶级数', desc: () => locale.value === 'en' ? 'Square wave from sines' : '用正弦波拼出方波' },
  { src: base + 'RiemannSum.mp4', poster: base + 'RiemannSum.jpg', title: () => locale.value === 'en' ? 'Riemann Sum' : '黎曼和', desc: () => locale.value === 'en' ? 'Rectangles → integral' : '矩形逼近 → 定积分' },
  { src: base + 'FractalZoom.mp4', poster: base + 'FractalZoom.jpg', title: () => locale.value === 'en' ? 'Self-Similarity' : '自相似', desc: () => locale.value === 'en' ? 'Fractal zoom' : '分形缩放' },
]
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
}
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
.video-card:hover .play-hint { opacity: 0.2; }
figcaption { padding: 14px 16px; }
.video-title { display: block; font-weight: 600; font-size: 15px; color: var(--text-primary); font-family: var(--font-heading); }
.video-desc { display: block; font-size: 12px; color: var(--text-muted); margin-top: 4px; }
</style>
