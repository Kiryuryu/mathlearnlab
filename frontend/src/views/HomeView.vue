<template>
  <div>
    <div class="hero">
      <p class="hero-eyebrow">{{ $t('home.eyebrow') }}</p>
      <h1>{{ $t('home.title') }}</h1>
      <p class="hero-sub">{{ $t('home.subtitle') }}</p>
    </div>
    <div class="daily-problem" v-if="dailyQ">
      <div class="daily-header">
        <span class="daily-label">✦ {{ $t('home.daily') }}</span>
        <span class="daily-date">{{ dailySource === 'ai' ? 'AI 出题' : '' }} {{ today }}</span>
      </div>
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
import { ref, computed, onMounted } from 'vue'
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

// Static fallback bank (higher difficulty, used only if the AI API fails)
const dailyProbs = [
  // ── 极限 ──
  { q: '求极限：$\\lim_{x \\to 0} \\frac{1-\\cos x}{x^2}$', q_en: 'Evaluate: $\\lim_{x \\to 0} \\frac{1-\\cos x}{x^2}$', answer_en: '$\\frac12$ — via $\\frac{1-\\cos x}{x^2} = \\frac{2\\sin^2(x/2)}{x^2}$', answer: '$\\frac12$ — 用 $1-\\cos x = 2\\sin^2(x/2)$' },
  { q: '求极限：$\\lim_{x \\to 0} \\frac{e^x - 1 - x}{x^2}$', q_en: 'Evaluate: $\\lim_{x \\to 0} \\frac{e^x - 1 - x}{x^2}$', answer_en: '$\\frac12$ — via Taylor expansion $e^x=1+x+\\frac{x^2}{2}+\\cdots$', answer: '$\\frac12$ — 用泰勒展开 $e^x=1+x+\\frac{x^2}{2}+\\cdots$' },
  { q: '求极限：$\\lim_{x \\to 0} \\frac{\\tan x - \\sin x}{x^3}$', q_en: 'Evaluate: $\\lim_{x \\to 0} \\frac{\\tan x - \\sin x}{x^3}$', answer_en: '$\\frac12$ — expand $\\tan x, \\sin x$ to $x^3$', answer: '$\\frac12$ — 展开 $\\tan x$、$\\sin x$ 到 $x^3$ 项' },
  // ── 导数 / 极值 ──
  { q: '求 $f(x)=x^x$ 的导数', q_en: 'Find $f\'(x)$ for $f(x)=x^x$', answer_en: '$x^x(\\ln x + 1)$ — logarithmic differentiation', answer: '$x^x(\\ln x + 1)$ — 对数求导法' },
  { q: '函数 $f(x)=x^4-4x^3+6x^2$ 有几个拐点？', q_en: 'How many inflection points does $f(x)=x^4-4x^3+6x^2$ have?', answer_en: '2 — at $x=1\\pm\\frac{\\sqrt3}{3}$', answer: '2 个 — 在 $x=1\\pm\\frac{\\sqrt3}{3}$（$f\'\'=12(x^2-2x+\\frac23)$）' },
  { q: '证明 $\\arctan x + \\arctan \\frac{1}{x} = \\frac{\\pi}{2}$（$x>0$）', q_en: 'Prove $\\arctan x + \\arctan \\frac{1}{x} = \\frac{\\pi}{2}$ for $x>0$', answer_en: 'Derivative is 0, then check $x=1$', answer: '求导为 0，再代入 $x=1$ 验证常数' },
  // ── 积分 ──
  { q: '计算 $\\int_0^{\\infty} e^{-x^2} dx$', q_en: 'Compute $\\int_0^{\\infty} e^{-x^2} dx$', answer_en: '$\\frac{\\sqrt{\\pi}}{2}$ — Gaussian integral (square it & switch to polar)', answer: '$\\frac{\\sqrt{\\pi}}{2}$ — 高斯积分（平方后转极坐标）' },
  { q: '计算 $\\int_0^1 x\\ln x\\, dx$', q_en: 'Compute $\\int_0^1 x\\ln x\\, dx$', answer_en: '$-\\frac14$ — integration by parts (limit as $x\\to0^+$ is 0)', answer: '$-\\frac14$ — 分部积分（$x\\to0^+$ 的极限为 0）' },
  { q: '用对称性求 $\\int_{-\\pi}^{\\pi} x^2\\cos x\\, dx$ 与 $\\int_{-\\pi}^{\\pi} x^3\\cos x\\, dx$ 的关系', q_en: 'Relate $\\int_{-\\pi}^{\\pi} x^2\\cos x\\, dx$ and $\\int_{-\\pi}^{\\pi} x^3\\cos x\\, dx$ using symmetry', answer_en: 'Second is 0 (odd); first is $4\\pi$', answer: '第二个为 0（奇函数）；第一个为 $4\\pi$' },
  // ── 级数 / 多元 ──
  { q: '判断 $\\sum_{n=1}^{\\infty} \\frac{(-1)^n}{n}$ 的敛散性', q_en: 'Does $\\sum_{n=1}^{\\infty} \\frac{(-1)^n}{n}$ converge absolutely?', answer_en: 'Converges conditionally (alternating), not absolutely', answer: '条件收敛（交错级数），非绝对收敛' },
  { q: '求 $f(x,y)=x^2y^2$ 在约束 $x^2+y^2=1$ 下的最大值', q_en: 'Max of $f(x,y)=x^2y^2$ subject to $x^2+y^2=1$', answer_en: '$\\frac14$ — at $x^2=y^2=\\frac12$', answer: '$\\frac14$ — 在 $x^2=y^2=\\frac12$ 处' },
  { q: '$\\int_0^1 \\int_0^1 \\frac{1}{(1+xy)^2}\\, dy\\, dx$（提示：换序）', q_en: 'Compute $\\int_0^1 \\int_0^1 \\frac{1}{(1+xy)^2}\\, dy\\, dx$', answer_en: '$\\frac12$ — switch integration order', answer: '$\\frac12$ — 交换积分顺序' },
]

// Daily seed from LOCAL date (YYYY-MM-DD) so it changes at midnight local time.
function dailyIndex() {
  const d = new Date()
  const seed = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  let idx = 0
  for (let i = 0; i < seed.length; i++) idx = (idx * 31 + seed.charCodeAt(i)) % dailyProbs.length
  return idx
}

// ── Daily problem: AI-generated (via /api/daily/problem), static fallback if API fails ──
const dailyQ = ref('')
const dailyAns = ref('')
const dailySource = ref('ai') // 'ai' | 'fallback'
const showHint = ref(false)
const today = new Date().toLocaleDateString(locale.value === 'en' ? 'en-US' : 'zh-CN')

function loadDaily() {
  fetch('/api/daily/problem')
    .then(r => r.json())
    .then(d => {
      if (d.problem?.problem_statement) {
        const p = d.problem
        const steps = (p.solution?.steps || []).map((s, i) => `${i + 1}. ${s}`).join('\n\n')
        const final = p.solution?.final_answer || ''
        dailyQ.value = p.problem_statement
        dailyAns.value = steps ? `**解答思路：**\n\n${steps}${final ? `\n\n**答案：** ${final}` : ''}` : final
        dailySource.value = 'ai'
        return
      }
      // Fallback to static bank
      useStaticDaily()
    })
    .catch(() => useStaticDaily())
}

function useStaticDaily() {
  const p = dailyProbs[dailyIndex()]
  dailyQ.value = locale.value === 'en' ? p.q_en : p.q
  dailyAns.value = locale.value === 'en' ? p.answer_en : p.answer
  dailySource.value = 'fallback'
}

const renderedQ = computed(() => renderMarkdown(dailyQ.value))
const renderedAnswer = computed(() => renderMarkdown('**' + (locale.value === 'en' ? 'Answer: ' : '解答：') + '**' + dailyAns.value))

onMounted(loadDaily)
</script>

<style scoped>
.hero { text-align:center; padding:56px 32px 28px; }
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--accent-warm);
  margin: 0 0 12px;
  font-weight: 600;
}
.hero h1 { font-size: 38px; margin: 0; }
.hero-sub { color:var(--text-secondary); max-width:640px; margin:14px auto; font-size:15px; }
.daily-problem { max-width:680px; margin:0 auto 28px; background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:26px 28px; box-shadow:var(--shadow-card); }
.daily-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; }
.daily-label { font-size:12px; color:var(--accent); font-weight:600; letter-spacing:0.04em; }
.daily-date { font-size:11px; color:var(--text-muted); font-variant-numeric:tabular-nums; }
.daily-q { font-size:15px; line-height:1.9; }
.daily-actions { margin-top:14px; display:flex; gap:8px; align-items:center; }
.daily-hint { margin-top:8px; padding:10px 14px; background:var(--bg-nav); border-radius:var(--radius); font-size:13px; color:var(--text-secondary); line-height:1.7; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:22px; padding:36px; max-width:1400px; margin:0 auto; }
@media(max-width:768px) { .card-grid { grid-template-columns:1fr; padding:16px; } .hero h1 { font-size:28px; } }
</style>
