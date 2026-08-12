<template>
  <div class="page">
    <div class="page-head">
      <p class="hero-eyebrow">{{ $t('mathematicians.eyebrow') }}</p>
      <h1>{{ $t('mathematicians.title') }}</h1>
      <p class="sub">{{ $t('mathematicians.subtitle') }}</p>
    </div>
    <div class="grid">
      <router-link v-for="m in mathematicians" :key="m.key" :to="'/mathematicians/'+m.key" class="card" :style="{ '--card-accent': m.accent }">
        <span class="card-accent-bar"></span>
        <span class="icon">{{ m.init }}</span>
        <div class="card-body"><h2>{{ locale === 'en' && m.name_en ? m.name_en : m.name }}</h2><p class="years">{{ m.years }}</p><p class="contrib">{{ m.contributions }}</p></div>
      </router-link>
    </div>
  </div>
</template>
<script setup>
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const mathematicians = [
  { key:'newton',init:'N',name:'艾萨克·牛顿',name_en:'Isaac Newton',years:'1643–1727',contributions:'微积分、万有引力定律、光学',accent:'#4a6b8a' },
  { key:'leibniz',init:'L',name:'戈特弗里德·莱布尼茨',name_en:'Gottfried Leibniz',years:'1646–1716',contributions:'微积分符号、二进制',accent:'#6b5a8a' },
  { key:'euler',init:'E',name:'莱昂哈德·欧拉',name_en:'Leonhard Euler',years:'1707–1783',contributions:'e^(iπ)+1=0、图论',accent:'#5a7a6b' },
  { key:'gauss',init:'G',name:'卡尔·高斯',name_en:'Carl Friedrich Gauss',years:'1777–1855',contributions:'正态分布、最小二乘法',accent:'#8a5a4a' },
  { key:'fourier',init:'F',name:'约瑟夫·傅里叶',name_en:'Joseph Fourier',years:'1768–1830',contributions:'傅里叶级数、热传导',accent:'#5a6b8a' },
  { key:'ramanujan',init:'R',name:'拉马努金',name_en:'Srinivasa Ramanujan',years:'1887–1920',contributions:'无穷级数、π的公式',accent:'#8a4a4a' },
  { key:'cauchy_weierstrass',init:'C',name:'柯西 & 魏尔斯特拉斯',name_en:'Cauchy & Weierstrass',years:'1789–1857 / 1815–1897',contributions:'ε-δ极限定义、分析严密化',accent:'#6b6b5a' },
  { key:'fermat',init:'Fp',name:'皮埃尔·德·费马',name_en:'Pierre de Fermat',years:'1607–1665',contributions:'费马大定理、解析几何、概率论',accent:'#7a5a8a' },
]
</script>
<style scoped>
.page { max-width:1200px; margin:0 auto; padding:48px 20px 32px; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px; padding:28px 0 12px; }
.card {
  display:flex; align-items:flex-start; gap:16px; padding:24px 24px 20px;
  border-radius:var(--radius-lg); color:var(--text-primary); text-decoration:none;
  position:relative; overflow:hidden; background:var(--bg-card);
  border:1px solid var(--border); box-shadow:var(--shadow-card);
  transition:transform 0.2s ease, box-shadow 0.25s ease, border-color 0.2s ease;
}
.card:hover {
  transform:translateY(-3px);
  border-color: color-mix(in srgb, var(--card-accent) 55%, var(--border));
  box-shadow:var(--shadow-elevated); text-decoration:none;
}
.card-accent-bar { position:absolute; top:0; left:0; right:0; height:3px; background:var(--card-accent); opacity:0.75; }
.icon {
  font-size:26px; font-weight:700; color:var(--card-accent);
  width:48px; height:48px; border-radius:var(--radius);
  background: color-mix(in srgb, var(--card-accent) 12%, var(--bg-card));
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  font-family:var(--font-heading);
}
.card-body h2 { margin:0 0 4px; font-size:18px; color:var(--text-primary); border-bottom:none; }
.years { font-size:11px; color:var(--text-muted); font-variant-numeric:tabular-nums; }
.contrib { font-size:13px; color:var(--text-secondary); margin-top:6px; line-height:1.6; }
@media(max-width:768px){.grid{grid-template-columns:1fr;}}
</style>
