<template>
  <div>
    <div class="hero">
      <h1>数学博物馆</h1>
      <p>知其然，知其所以然。理解概念，发现数学之美。</p>
    </div>
    <div class="daily-problem" v-if="daily">
      <div class="daily-header"><span>每日一题</span><span class="daily-date">{{ today }}</span></div>
      <div class="daily-q" v-html="daily.q"></div>
      <div class="daily-actions">
        <button class="btn" @click="showHint = true" v-if="!showHint">查看提示</button>
        <div v-if="showHint" class="daily-hint" v-html="daily.answer"></div>
        <router-link to="/practice" class="btn btn-primary">去练习</router-link>
      </div>
    </div>
    <div class="card-grid">
      <ExhibitCard v-for="c in cards" :key="c.to" v-bind="c" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ExhibitCard from '@/components/ExhibitCard.vue'

const cards = [
  { to: '/gaoshu', title: '微积分的世界', desc: '极限、导数、积分、级数、多元微积分', meta: '5大主题 · 7位核心数学家', bg: 'linear-gradient(135deg,#1a1d22,#1e2935 40%,#2a3d54 70%,#3a5a7c)' },
  { to: '/exhibit/linear-algebra', title: '线性代数', desc: '矩阵变换 · 特征值 · 空间变形', meta: '凯莱、哈密顿、格拉斯曼', bg: 'linear-gradient(135deg,#1a1a2e,#2a2a4e)' },
  { to: '/exhibit/probability', title: '概率论', desc: '大数定律 · 中心极限 · 贝叶斯', meta: '帕斯卡、伯努利、柯尔莫哥洛夫', bg: 'linear-gradient(135deg,#2e1a1a,#4e2a2a)' },
  { to: '/fractal', title: '分形探索', desc: 'Mandelbrot 集 · Julia 集 · Lorenz 吸引子', meta: 'Mandelbrot · Julia', bg: 'linear-gradient(135deg,#2e1a1a,#4e2a2a)' },
  { to: '/gallery', title: '数学之美', desc: '欧拉恒等式 · 巴塞尔问题 · 高斯积分', meta: '最美的公式一览', bg: 'linear-gradient(135deg,#1d1a2e,#4a2c6e)' },
  { to: '/mathematicians', title: '数学家长廊', desc: '牛顿 · 欧拉 · 高斯 · 拉马努金', meta: '7位数学家的故事', bg: 'linear-gradient(135deg,#1e1a2e,#2a2250,#3a2a60)' },
  { to: '/workshop', title: '函数工坊', desc: '2D曲线 · 3D曲面 · 向量场 · AI绘图', meta: 'sin(x), x², eˣ, 傅里叶级数', bg: 'linear-gradient(135deg,#1a2528,#1a3532,#1a4540)' },
  { to: '/practice', title: '练习', desc: '选题 · 纸笔作答 · 拍照上传 · AI批改', meta: '基础→进阶→考研→研究生→博士', bg: 'linear-gradient(135deg,#2a1a1e,#4a2528,#5a2a2e)' },
]

const dailyProbs = [
  { q: '求极限：$\\lim_{x \\to 0} \\frac{\\sin 3x}{x}$', answer: '<strong>解答：</strong>$3$ — 因为 $\\frac{\\sin 3x}{x} = 3\\frac{\\sin 3x}{3x} \\to 3$' },
  { q: '$f(x)=x^3-3x$ 在 $x=1$ 处是极大值还是极小值？', answer: '<strong>解答：</strong>极小值点。$f\'\'(1)=6>0$' },
  { q: '计算 $\\int_0^1 x^2 dx$', answer: '<strong>解答：</strong>$\\frac{1}{3}$' },
  { q: '$\\sum_{n=0}^{\\infty} \\frac{1}{2^n} = ?$', answer: '<strong>解答：</strong>$2$ — 等比级数' },
  { q: '$e^{i\\pi} + 1 = ?$', answer: '<strong>解答：</strong>$0$ — 欧拉恒等式' },
]
const seed = new Date().toISOString().slice(0,10)
let idx = 0; for(let i=0;i<seed.length;i++) idx = (idx*31+seed.charCodeAt(i)) % dailyProbs.length
const daily = dailyProbs[idx]
const showHint = ref(false)
const today = new Date().toLocaleDateString('zh-CN')
</script>

<style scoped>
.hero { text-align:center; padding:48px 32px 24px; }
.hero h1 { font-size:32px; margin:0; }
.hero p { color:#505560; max-width:640px; margin:12px auto; font-size:15px; }
.daily-problem { max-width:640px; margin:0 auto 24px; background:var(--bg-card,#fff); border:1px solid var(--border,#e2e5e8); border-radius:12px; padding:24px; box-shadow:0 1px 2px rgba(26,29,34,0.04); }
.daily-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.daily-header span:first-child { font-size:12px; color:#4a6a8a; font-weight:600; }
.daily-date { font-size:11px; color:#889098; }
.daily-q { font-size:15px; line-height:1.8; }
.daily-actions { margin-top:12px; display:flex; gap:8px; align-items:center; }
.daily-hint { margin-top:8px; padding:10px; background:var(--bg-nav,#f0f2f4); border-radius:6px; font-size:13px; color:#505560; line-height:1.6; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; padding:32px; max-width:1400px; margin:0 auto; }
@media(max-width:768px) { .card-grid { grid-template-columns:1fr; padding:16px; } }
</style>
