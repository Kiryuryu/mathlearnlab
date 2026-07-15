<template>
  <div class="gaoshu-page">
    <div class="gaoshu-hero">
      <h1>展区</h1>
      <p>从微积分到线性代数，探索数学的核心概念</p>
    </div>
    <div class="gaoshu-content">
      <h2 style="text-align:center;margin-bottom:24px;">五大展区</h2>
      <div class="sub-grid">
        <ExhibitCard v-for="s in subtopics" :key="s.key" :to="'/exhibit/'+s.key" :title="s.label" :desc="s.question" :meta="s.historian" :bg="s.bg" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ExhibitCard from '@/components/ExhibitCard.vue'
const bgs = [
  'linear-gradient(135deg,#1a1d22,#1e2935,#2a3d54)',
  'linear-gradient(135deg,#1e1a2e,#2a2250,#3a2a60)',
  'linear-gradient(135deg,#1a2528,#1a3532,#1a4540)',
  'linear-gradient(135deg,#2a1a1e,#4a2528,#5a2a2e)',
  'linear-gradient(135deg,#1a1d22,#1e2935,#2a3d54)',
]
const subtopics = [
  { key:'limits', label:'极限 — 无限逼近的艺术', question:'如何用数学语言精确描述"无限接近"', historian:'柯西、魏尔斯特拉斯', bg:bgs[0] },
  { key:'derivatives', label:'导数 — 瞬间的变化率', question:'如何在某一瞬间测量变化？', historian:'费马、牛顿、莱布尼茨', bg:bgs[1] },
  { key:'integrals', label:'积分 — 和的极限', question:'如何求一个曲线下方不规则图形的面积？', historian:'阿基米德、黎曼、勒贝格', bg:bgs[2] },
  { key:'series', label:'无穷级数 — 无限的拼图', question:'无穷多个数加起来可以是有限的吗？', historian:'欧拉、傅里叶', bg:bgs[3] },
  { key:'multivariable', label:'多元微积分 — 从平面到空间', question:'如何在多维世界中理解变化和流动？', historian:'拉格朗日、高斯、格林', bg:bgs[4] },
]
</script>

<style scoped>
.gaoshu-hero { background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460,#1a5276); color:#fff; text-align:center; padding:60px 40px 40px; }
.gaoshu-hero h1 { font-size:40px; margin:0 0 8px; }
.gaoshu-hero p { opacity:0.7; }
.gaoshu-content { max-width:1100px; margin:0 auto; padding:32px 20px; }
.sub-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }
</style>
