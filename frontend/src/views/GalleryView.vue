<template>
  <div class="page">
    <p class="hero-eyebrow">{{ $t('gallery.eyebrow') }}</p>
    <h1>{{ $t('gallery.title') }}</h1>
    <p class="sub">{{ $t('gallery.subtitle') }}</p>
    <div class="grid">
      <router-link v-for="g in items" :key="g.title" :to="g.to" class="card" :style="{ '--card-accent': g.accent }">
        <span class="card-accent-bar"></span>
        <div class="card-body"><p class="formula">{{ g.formula }}</p><h2>{{ g.title }}</h2><p class="desc">{{ g.desc }}</p></div>
      </router-link>
    </div>
    <BeautyVideos />
    <router-link to="/gaoshu" class="cta">{{ $t('gallery.enterExhibits') }}</router-link>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import BeautyVideos from '@/components/BeautyVideos.vue'
const { locale } = useI18n()
const rawItems = [
  { title:'欧拉恒等式', title_en:"Euler's Identity", formula:'e^(iπ) + 1 = 0', desc:'五个最重要的数学常数', desc_en:'The five most important constants united', accent:'#4a6b8a', to:'/exhibit/derivatives?tab=beauty' },
  { title:'巴塞尔问题', title_en:'Basel Problem', formula:'Σ 1/n² = π²/6', desc:'自然数倒数平方和 = π²/6', desc_en:'Sum of reciprocal squares = π²/6', accent:'#6b5a8a', to:'/exhibit/series?tab=beauty' },
  { title:'高斯积分', title_en:'Gaussian Integral', formula:'∫ e^(-x²) dx = √π', desc:'e 和 π 在积分中相遇', desc_en:'e and π meet in an integral', accent:'#5a7a6b', to:'/exhibit/integrals?tab=beauty' },
  { title:'Wallis 公式', title_en:"Wallis' Product", formula:'π/2 = 2·2/1·3 × 4·4/3·5 × ...', desc:'无穷乘积等于 π/2', desc_en:'Infinite product equals π/2', accent:'#8a5a4a', to:'/exhibit/integrals?tab=beauty' },
  { title:'Gamma 函数', title_en:'Gamma Function', formula:'Γ(n) = ∫ x^(n-1)e^(-x) dx', desc:'阶乘的连续推广', desc_en:'Continuous extension of factorial', accent:'#5a6b8a', to:'/exhibit/integrals?tab=beauty' },
  { title:'微积分基本定理', title_en:'Fundamental Theorem of Calculus', formula:'d/dx ∫ f(t)dt = f(x)', desc:'微分和积分是互逆运算', desc_en:'Differentiation and integration are inverses', accent:'#8a4a4a', to:'/exhibit/integrals?tab=beauty' },
]
const items = computed(() => rawItems.map(i => ({
  ...i,
  title: locale.value === 'en' && i.title_en ? i.title_en : i.title,
  desc: locale.value === 'en' && i.desc_en ? i.desc_en : i.desc,
})))
</script>
<style scoped>
.page { max-width:1100px; margin:0 auto; padding:48px 20px 32px; }
.page h1 { text-align:center; }
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--accent-warm);
  font-weight: 600;
  margin: 0 0 10px;
  text-align: center;
}
.page h1 { font-size:34px; margin-bottom:8px; }
.sub { color:var(--text-secondary); text-align:center; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px; padding:28px 0 12px; }
.card {
  display:block; color:var(--text-primary); text-decoration:none; border-radius:var(--radius-lg);
  overflow:hidden; min-height:190px; display:flex; flex-direction:column; justify-content:flex-end;
  background:var(--bg-card); border:1px solid var(--border); box-shadow:var(--shadow-card);
  position:relative; transition:transform 0.2s ease, box-shadow 0.25s ease, border-color 0.2s ease;
}
.card:hover {
  transform:translateY(-3px);
  border-color: color-mix(in srgb, var(--card-accent) 55%, var(--border));
  box-shadow:var(--shadow-elevated); text-decoration:none;
}
.card-accent-bar { position:absolute; top:0; left:0; right:0; height:3px; background:var(--card-accent); opacity:0.75; }
.card-body { padding:24px; }
.card-body h2 { margin:0 0 6px; font-size:19px; color:var(--text-primary); }
.formula { font-family:var(--font-mono); font-size:15px; color:var(--card-accent); margin:0 0 10px; }
.desc { font-size:12px; color:var(--text-secondary); margin:4px 0 0; }
.cta { display:block; text-align:center; padding:11px 24px; background:var(--accent); color:#fff; border-radius:var(--radius); text-decoration:none; font-weight:600; width:220px; margin:28px auto; transition:background 0.15s, transform 0.15s; }
.cta:hover { background:color-mix(in srgb, var(--accent) 85%, #000); text-decoration:none; transform:translateY(-1px); }
@media(max-width:768px){.grid{grid-template-columns:1fr;}}
</style>
