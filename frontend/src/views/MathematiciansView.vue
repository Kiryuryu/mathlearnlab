<template>
  <div class="page"><h1>数学家长廊</h1><p class="sub">数学不只是公式，更是人的故事</p>
    <div class="grid">
      <router-link v-for="m in mathematicians" :key="m.key" :to="'/mathematicians/'+m.key" class="card" :style="{background:m.bg}">
        <span class="icon">{{ m.init }}</span>
        <div class="card-body"><h2>{{ m.name }}</h2><p class="years">{{ m.years }}</p><p class="contrib">{{ m.contributions }}</p></div>
      </router-link>
    </div>
  </div>
</template>
<script setup>
const mathematicians = [
  { key:'newton',init:'N',name:'艾萨克·牛顿',years:'1643–1727',contributions:'微积分、万有引力定律、光学',bg:'linear-gradient(135deg,#1a1d22,#2a3d54)' },
  { key:'leibniz',init:'L',name:'戈特弗里德·莱布尼茨',years:'1646–1716',contributions:'微积分符号、二进制',bg:'linear-gradient(135deg,#1e1a2e,#2a2250)' },
  { key:'euler',init:'E',name:'莱昂哈德·欧拉',years:'1707–1783',contributions:'e^(iπ)+1=0、图论',bg:'linear-gradient(135deg,#1a2528,#1a3532)' },
  { key:'gauss',init:'G',name:'卡尔·高斯',years:'1777–1855',contributions:'正态分布、最小二乘法',bg:'linear-gradient(135deg,#2a1a1e,#4a2528)' },
  { key:'fourier',init:'F',name:'约瑟夫·傅里叶',years:'1768–1830',contributions:'傅里叶级数、热传导',bg:'linear-gradient(135deg,#1a2d3d,#2c5f8b)' },
  { key:'ramanujan',init:'R',name:'拉马努金',years:'1887–1920',contributions:'无穷级数、π的公式',bg:'linear-gradient(135deg,#3d1a1a,#6b2a2a)' },
  { key:'cauchy_weierstrass',init:'C',name:'柯西 & 魏尔斯特拉斯',years:'1789–1857 / 1815–1897',contributions:'ε-δ极限定义、分析严密化',bg:'linear-gradient(135deg,#1a1d22,#1e2935)' },
]
</script>
<style scoped>
.page { max-width:1100px; margin:0 auto; padding:32px 20px; }
.page h1, .sub { text-align:center; }
.sub { color:#505560; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; padding:20px 0; }
.card { display:flex; align-items:flex-start; gap:16px; padding:24px; border-radius:12px; color:#fff; text-decoration:none; position:relative; overflow:hidden; transition:transform 0.25s; }
.card:hover { transform:translateY(-4px); }
.icon { font-size:40px; opacity:0.3; position:absolute; top:12px; right:16px; font-weight:700; }
.card-body h2 { margin:0 0 4px; font-size:18px; }
.years { font-size:11px; opacity:0.6; }
.contrib { font-size:13px; opacity:0.8; margin-top:6px; }
@media(max-width:768px){.grid{grid-template-columns:1fr;}}
</style>
