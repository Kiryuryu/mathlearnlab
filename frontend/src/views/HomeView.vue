<template>
  <div>
    <div class="hero">
      <h1>{{ $t('home.title') }}</h1>
      <p>{{ $t('home.subtitle') }}</p>
    </div>
    <div class="daily-problem" v-if="daily">
      <div class="daily-header"><span>{{ $t('home.daily') }}</span><span class="daily-date">{{ today }}</span></div>
      <div class="daily-q" v-html="renderedQ"></div>
      <div class="daily-actions">
        <button class="btn" @click="showHint = true" v-if="!showHint">{{ $t('home.showHint') }}</button>
        <div v-if="showHint" class="daily-hint" v-html="renderedAnswer"></div>
        <router-link to="/practice" class="btn btn-primary">{{ $t('home.goPractice') }}</router-link>
      </div>
    </div>
    <div class="card-grid">
      <ExhibitCard v-for="c in displayCards" :key="c.to" v-bind="c" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ExhibitCard from '@/components/ExhibitCard.vue'
import { renderMarkdown } from '@/utils/markdown'

const { locale } = useI18n()

const cards = [
  { to: '/gaoshu', title: '微积分的世界', title_en: 'Calculus World', desc: '极限、导数、积分、级数、多元微积分', desc_en: 'Limits, Derivatives, Integrals, Series, Multivariable', meta: '5大主题 · 7位核心数学家', meta_en: '5 Topics · 7 Key Mathematicians', bg: 'linear-gradient(135deg,#1a1d22,#1e2935 40%,#2a3d54 70%,#3a5a7c)' },
  { to: '/fractal', title: '分形探索', title_en: 'Fractal Explorer', desc: 'Mandelbrot 集 · Julia 集 · Lorenz 吸引子', desc_en: 'Mandelbrot · Julia · Lorenz Attractor', meta: 'Mandelbrot · Julia', bg: 'linear-gradient(135deg,#2e1a1a,#4e2a2a)' },
  { to: '/gallery', title: '数学之美', title_en: 'Mathematical Beauty', desc: '欧拉恒等式 · 巴塞尔问题 · 高斯积分', desc_en: "Euler's Identity · Basel Problem · Gaussian Integral", meta: '最美的公式一览', meta_en: 'The Most Beautiful Formulas', bg: 'linear-gradient(135deg,#1d1a2e,#4a2c6e)' },
  { to: '/mathematicians', title: '数学家长廊', title_en: 'Mathematicians', desc: '牛顿 · 欧拉 · 高斯 · 拉马努金', desc_en: 'Newton · Euler · Gauss · Ramanujan', meta: '7位数学家的故事', meta_en: 'Stories of 7 Mathematicians', bg: 'linear-gradient(135deg,#1e1a2e,#2a2250,#3a2a60)' },
  { to: '/workshop', title: '函数工坊', title_en: 'Function Lab', desc: '2D曲线 · 3D曲面 · 向量场 · AI绘图', desc_en: '2D Curves · 3D Surfaces · Vector Fields · AI Plots', meta: 'sin(x), x², eˣ, 傅里叶级数', meta_en: 'sin(x), x², eˣ, Fourier Series', bg: 'linear-gradient(135deg,#1a2528,#1a3532,#1a4540)' },
  { to: '/practice', title: '练习', title_en: 'Practice', desc: '选题 · 纸笔作答 · 拍照上传 · AI批改', desc_en: 'Select Topics · Solve · Submit Photos · AI Grading', meta: '基础→进阶→考研→研究生→博士', meta_en: 'Basic → Advanced → Grad School → PhD', bg: 'linear-gradient(135deg,#2a1a1e,#4a2528,#5a2a2e)' },
]

const displayCards = computed(() => cards.map(c => ({
  ...c,
  title: locale.value === 'en' && c.title_en ? c.title_en : c.title,
  desc: locale.value === 'en' && c.desc_en ? c.desc_en : c.desc,
  meta: locale.value === 'en' && c.meta_en ? c.meta_en : c.meta,
})))

const dailyProbs = [
  // ── 极限 ──
  { q: '求极限：$\\lim_{x \\to 0} \\frac{\\sin 3x}{x}$', q_en: 'Evaluate: $\\lim_{x \\to 0} \\frac{\\sin 3x}{x}$', answer_en: '3 — because $\\frac{\\sin 3x}{x} = 3\\frac{\\sin 3x}{3x} \\to 3$', answer: '3 — 因为 $\\frac{\\sin 3x}{x} = 3\\frac{\\sin 3x}{3x} \\to 3$' },
  { q: '求极限：$\\lim_{x \\to \\infty} \\left(1 + \\frac{1}{x}\\right)^x$', q_en: 'Evaluate: $\\lim_{x \\to \\infty} \\left(1 + \\frac{1}{x}\\right)^x$', answer_en: '$e$ — the definition of Euler\'s number', answer: '$e$ — 这就是自然常数 $e$ 的定义' },
  { q: '判断 $f(x)=\\frac{\\sin x}{x}$ 在 $x=0$ 处如何定义才连续', q_en: 'How to define $f(x)=\\frac{\\sin x}{x}$ at $x=0$ to make it continuous?', answer_en: '$f(0)=1$', answer: '$f(0)=1$（因为 $\\lim_{x\\to0}\\frac{\\sin x}{x}=1$）' },
  { q: '求极限：$\\lim_{x \\to 0} \\frac{1-\\cos x}{x^2}$', q_en: 'Evaluate: $\\lim_{x \\to 0} \\frac{1-\\cos x}{x^2}$', answer_en: '$\\frac12$ — via $\\frac{1-\\cos x}{x^2} = \\frac{2\\sin^2(x/2)}{x^2} \\to \\frac12$', answer: '$\\frac12$ — 用 $1-\\cos x = 2\\sin^2(x/2)$' },
  // ── 导数 ──
  { q: '$f(x)=x^3-3x$ 在 $x=1$ 处是极大值还是极小值？', q_en: '$f(x)=x^3-3x$ at $x=1$: max or min?', answer_en: 'Local minimum. $f\'\'(1)=6>0$', answer: '极小值点。$f\'\'(1)=6>0$' },
  { q: '求 $f(x)=x\\ln x$ 的导数', q_en: 'Find the derivative of $f(x)=x\\ln x$', answer_en: '$\\ln x + 1$ (product rule)', answer: '$\\ln x + 1$（乘积法则）' },
  { q: '求 $y=e^{2x}\\cos x$ 的导数', q_en: 'Find $y\'$ for $y=e^{2x}\\cos x$', answer_en: '$e^{2x}(2\\cos x - \\sin x)$', answer: '$e^{2x}(2\\cos x - \\sin x)$（乘积+链式法则）' },
  { q: '函数 $f(x)=x^4-2x^2$ 有几个驻点？', q_en: 'How many critical points does $f(x)=x^4-2x^2$ have?', answer_en: '3 — at $x=0,\\pm 1$', answer: '3 个 — 在 $x=0,\\pm 1$（$f\'=4x^3-4x=4x(x^2-1)$）' },
  // ── 积分 ──
  { q: '计算 $\\int_0^1 x^2 dx$', q_en: 'Compute $\\int_0^1 x^2 dx$', answer_en: '1/3', answer: '$\\frac13$' },
  { q: '计算 $\\int \\frac{1}{x} dx$', q_en: 'Compute $\\int \\frac{1}{x} dx$', answer_en: '$\\ln|x| + C$', answer: '$\\ln|x| + C$' },
  { q: '利用对称性求 $\\int_{-1}^{1} x^3 dx$', q_en: 'Use symmetry to find $\\int_{-1}^{1} x^3 dx$', answer_en: '0 — odd function over symmetric interval', answer: '$0$ — 奇函数在对称区间上积分为零' },
  { q: '求曲线 $y=\\sin x$ 在 $[0,\\pi]$ 与 $x$ 轴围成的面积', q_en: 'Area between $y=\\sin x$ and the $x$-axis on $[0,\\pi]$', answer_en: '$2$', answer: '$2$（$\\int_0^\\pi \\sin x\\, dx = 2$）' },
  // ── 级数 ──
  { q: '$\\sum_{n=0}^{\\infty} \\frac{1}{2^n} = ?$', q_en: '$\\sum_{n=0}^{\\infty} \\frac{1}{2^n} = ?$', answer_en: '2 — geometric series', answer: '2 — 等比级数' },
  { q: '判断 $\\sum_{n=1}^{\\infty} \\frac{1}{n}$ 是否收敛', q_en: 'Does $\\sum_{n=1}^{\\infty} \\frac{1}{n}$ converge?', answer_en: 'No — the harmonic series diverges', answer: '发散 — 调和级数' },
  { q: '$\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = ?$（巴塞尔问题）', q_en: '$\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = ?$ (Basel problem)', answer_en: '$\\pi^2/6$ — Euler\'s famous result', answer: '$\\frac{\\pi^2}{6}$ — 欧拉的著名结果' },
  { q: '$1+2+4+8+\\cdots$ 收敛吗？', q_en: 'Does $1+2+4+8+\\cdots$ converge?', answer_en: 'No — ratio $r=2>1$, diverges', answer: '不收敛 — 公比 $r=2>1$' },
  // ── 多元 / 综合 ──
  { q: '$e^{i\\pi} + 1 = ?$', q_en: '$e^{i\\pi} + 1 = ?$', answer_en: '0 — Euler identity', answer: '0 — 欧拉恒等式' },
  { q: '求 $f(x,y)=x^2+y^2$ 在 $(1,2)$ 处的梯度', q_en: 'Gradient of $f(x,y)=x^2+y^2$ at $(1,2)$', answer_en: '$(2, 4)$', answer: '$(2, 4)$（$\\nabla f=(2x, 2y)$）' },
  { q: '判断 $f(x)=x^3$ 在 $x=0$ 是否有极值', q_en: 'Does $f(x)=x^3$ have an extremum at $x=0$?', answer_en: 'No — inflection point ($f\'$ does not change sign)', answer: '没有 — 是拐点（$f\'=3x^2$ 不改变符号）' },
  { q: '$\\int_0^{\\infty} e^{-x} dx = ?$', q_en: '$\\int_0^{\\infty} e^{-x} dx = ?$', answer_en: '$1$ — improper integral', answer: '$1$ — 反常积分' },
]

// Daily seed from LOCAL date (YYYY-MM-DD) so it changes at midnight local time.
function dailyIndex() {
  const d = new Date()
  const seed = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  let idx = 0
  for (let i = 0; i < seed.length; i++) idx = (idx * 31 + seed.charCodeAt(i)) % dailyProbs.length
  return idx
}

const daily = computed(() => dailyProbs[dailyIndex()])
const showHint = ref(false)
const today = new Date().toLocaleDateString(locale.value === 'en' ? 'en-US' : 'zh-CN')
const renderedQ = computed(() => renderMarkdown(locale.value === 'en' ? daily.value.q_en : daily.value.q))
const renderedAnswer = computed(() => {
  const ans = locale.value === 'en' ? daily.value.answer_en : daily.value.answer
  return renderMarkdown('**' + (locale.value === 'en' ? 'Answer: ' : '解答：') + '**' + ans)
})
</script>

<style scoped>
.hero { text-align:center; padding:48px 32px 24px; }
.hero h1 { font-size:32px; margin:0; }
.hero p { color:var(--text-secondary); max-width:640px; margin:12px auto; font-size:15px; }
.daily-problem { max-width:640px; margin:0 auto 24px; background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:24px; box-shadow:0 1px 2px rgba(26,29,34,0.04); }
.daily-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.daily-header span:first-child { font-size:12px; color:var(--accent); font-weight:600; }
.daily-date { font-size:11px; color:var(--text-muted); }
.daily-q { font-size:15px; line-height:1.8; }
.daily-actions { margin-top:12px; display:flex; gap:8px; align-items:center; }
.daily-hint { margin-top:8px; padding:10px; background:var(--bg-nav); border-radius:6px; font-size:13px; color:var(--text-secondary); line-height:1.6; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; padding:32px; max-width:1400px; margin:0 auto; }
@media(max-width:768px) { .card-grid { grid-template-columns:1fr; padding:16px; } }
</style>
