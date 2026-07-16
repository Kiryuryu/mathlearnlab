<template>
  <div class="page"><h1>{{ $t('gallery.title') }}</h1><p class="sub">{{ $t('gallery.subtitle') }}</p>
    <div class="grid">
      <router-link v-for="g in items" :key="g.title" :to="g.to" class="card" :style="{background:g.bg}">
        <div class="card-body"><h2>{{ g.title }}</h2><p class="formula">{{ g.formula }}</p><p class="desc">{{ g.desc }}</p></div>
      </router-link>
    </div>
    <router-link to="/gaoshu" class="cta">{{ $t('gallery.enterExhibits') }}</router-link>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const rawItems = [
  { title:'欧拉恒等式', title_en:"Euler's Identity", formula:'e^(iπ) + 1 = 0', desc:'五个最重要的数学常数', desc_en:'The five most important constants united', bg:'linear-gradient(135deg,#1a1d22,#2a3d54)', to:'/exhibit/derivatives?tab=beauty' },
  { title:'巴塞尔问题', title_en:'Basel Problem', formula:'Σ 1/n² = π²/6', desc:'自然数倒数平方和 = π²/6', desc_en:'Sum of reciprocal squares = π²/6', bg:'linear-gradient(135deg,#1e1a2e,#2a2250)', to:'/exhibit/series?tab=beauty' },
  { title:'高斯积分', title_en:'Gaussian Integral', formula:'∫ e^(-x²) dx = √π', desc:'e 和 π 在积分中相遇', desc_en:'e and π meet in an integral', bg:'linear-gradient(135deg,#1a2528,#1a3532)', to:'/exhibit/integrals?tab=beauty' },
  { title:'Wallis 公式', title_en:"Wallis' Product", formula:'π/2 = 2·2/1·3 × 4·4/3·5 × ...', desc:'无穷乘积等于 π/2', desc_en:'Infinite product equals π/2', bg:'linear-gradient(135deg,#2a1a1e,#4a2528)', to:'/exhibit/integrals?tab=beauty' },
  { title:'Gamma 函数', title_en:'Gamma Function', formula:'Γ(n) = ∫ x^(n-1)e^(-x) dx', desc:'阶乘的连续推广', desc_en:'Continuous extension of factorial', bg:'linear-gradient(135deg,#1a2d3d,#2c5f8b)', to:'/exhibit/integrals?tab=beauty' },
  { title:'微积分基本定理', title_en:'Fundamental Theorem of Calculus', formula:'d/dx ∫ f(t)dt = f(x)', desc:'微分和积分是互逆运算', desc_en:'Differentiation and integration are inverses', bg:'linear-gradient(135deg,#3d1a1a,#6b2a2a)', to:'/exhibit/integrals?tab=beauty' },
]
const items = computed(() => rawItems.map(i => ({
  ...i,
  title: locale.value === 'en' && i.title_en ? i.title_en : i.title,
  desc: locale.value === 'en' && i.desc_en ? i.desc_en : i.desc,
})))
</script>
<style scoped>
.page { max-width:1000px; margin:0 auto; padding:32px 20px; }
.page h1 { text-align:center; }
.sub { color:var(--text-secondary); text-align:center; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; padding:20px 0; }
.card { display:block; color:#fff; text-decoration:none; border-radius:12px; overflow:hidden; min-height:200px; display:flex; flex-direction:column; justify-content:flex-end; transition:transform 0.25s; }
.card:hover { transform:translateY(-4px); }
.card-body { padding:24px; background:linear-gradient(transparent,rgba(0,0,0,0.5)); }
.card-body h2 { margin:0 0 6px; font-size:18px; }
.formula { font-family:monospace; font-size:14px; opacity:0.9; margin:0; }
.desc { font-size:12px; opacity:0.7; margin:4px 0 0; }
.cta { display:block; text-align:center; padding:12px 24px; background:var(--accent); color:#fff; border-radius:8px; text-decoration:none; font-weight:600; width:200px; margin:24px auto; }
@media(max-width:768px){.grid{grid-template-columns:1fr;}}
</style>
