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
    <section id="exhibits" class="exhibit-grid" aria-label="Subjects">
      <h2 class="section-title">{{ $t('home.subjectsTitle') }}</h2>
      <div v-if="loading" class="loading-wrap"><div class="spinner"></div></div>
      <div v-else class="card-grid">
        <ExhibitCard v-for="c in exhibitCards" :key="c.to" v-bind="c" />
      </div>
    </section>
    <nav class="side-halls" aria-label="More halls">
      <router-link v-for="h in sideHalls" :key="h.to" :to="h.to" class="hall-item">
        <span class="hall-num chapter-roman">{{ h.num }}</span>
        <span class="hall-name">{{ h.label }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import ExhibitCard from '@/components/ExhibitCard.vue'
import { renderMarkdown } from '@/utils/markdown'

const { locale, t } = useI18n()

const ROMANS = ['', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ']
const loading = ref(false)
const exhibitCards = ref([])

const sideHalls = computed(() => [
  { to: '/mathematicians', num: 'A', label: locale.value === 'en' ? 'Mathematicians' : '数学家长廊' },
  { to: '/gallery', num: 'B', label: locale.value === 'en' ? 'Mathematical Beauty' : '数学之美' },
  { to: '/fractal', num: 'C', label: locale.value === 'en' ? 'Fractals' : '分形' },
  { to: '/workshop', num: 'D', label: locale.value === 'en' ? 'Function Lab' : '函数工坊' },
  { to: '/practice', num: 'E', label: locale.value === 'en' ? 'Practice' : '练习' },
  { to: '/graph', num: 'F', label: locale.value === 'en' ? 'Knowledge Graph' : '知识图谱' },
])

// Direct-to-subject cards: the three subjects (高数/线代/概率), ordered.
async function loadSubjects() {
  loading.value = true
  try {
    const r = await fetch('/api/museum/exhibits')
    const d = await r.json()
    const ex = d.exhibits || {}
    exhibitCards.value = Object.entries(d.subjects || {})
      .filter(([, s]) => s.order)
      .sort((a, b) => a[1].order - b[1].order)
      .map(([key, s]) => {
        const count = Object.values(ex).filter(e => e.parent === key && e.order).length
        return {
          to: '/subject/' + key,
          title: locale.value === 'en' && s.en ? s.en : s.zh,
          desc: locale.value === 'en' && s.desc_en ? s.desc_en : s.desc,
          meta: count + ' ' + t('home.subjectCount'),
          symbol: s.icon || '',
          chapter: ROMANS[s.order] || '',
          accent: s.accent || '',
        }
      })
  } catch (e) {
    console.warn('Failed to load subjects', e)
  }
  loading.value = false
}

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

onMounted(() => { loadDaily(); loadSubjects() })
</script>

<style scoped>
.exhibit-grid { max-width: 1400px; margin: 0 auto; padding: 0 20px; }
.section-title {
  font-size: 15px;
  font-family: var(--font-heading);
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-align: center;
  margin: 36px 0 18px;
}
.loading-wrap { text-align: center; padding: 60px 0; }
.spinner { display: inline-block; width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg) } }
.side-halls {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  max-width: 900px;
  margin: 28px auto 40px;
  padding: 0 20px;
}
.hall-item {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 9px 18px 9px 12px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: var(--bg-card);
  box-shadow: var(--shadow-card);
  color: var(--text-primary);
  text-decoration: none;
  font-size: 13px;
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}
.hall-item:hover {
  border-color: var(--accent);
  box-shadow: var(--shadow-elevated);
  transform: translateY(-1px);
  text-decoration: none;
}
.hall-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px; height: 26px;
  border-radius: 50%;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 14px;
  flex-shrink: 0;
}
.hall-name { letter-spacing: 0.03em; }
.daily-problem { max-width:680px; margin:24px auto 28px; background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:26px 28px; box-shadow:var(--shadow-card); }.daily-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; }
.daily-label { font-size:12px; color:var(--accent); font-weight:600; letter-spacing:0.04em; }
.daily-date { font-size:11px; color:var(--text-muted); font-variant-numeric:tabular-nums; }
.daily-q { font-size:15px; line-height:1.9; }
.daily-actions { margin-top:14px; display:flex; gap:8px; align-items:center; }
.daily-hint { margin-top:8px; padding:10px 14px; background:var(--bg-nav); border-radius:var(--radius); font-size:13px; color:var(--text-secondary); line-height:1.7; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:22px; padding:36px; max-width:1400px; margin:0 auto; }
@media(max-width:768px) { .card-grid { grid-template-columns:1fr; padding:16px; } .hero h1 { font-size:28px; } .daily-problem { margin-left:16px; margin-right:16px; padding:20px; } }
</style>
