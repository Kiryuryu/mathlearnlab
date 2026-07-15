<template>
  <div class="page" v-if="m">
    <div class="hero">
      <h1>{{ m.name }}</h1>
      <p class="years">{{ m.years }}</p>
      <p class="contrib">{{ m.contributions }}</p>
    </div>
    <div class="content">
      <blockquote>{{ m.quote }}</blockquote>
      <div class="story" v-html="m.story.replace(/\n\n/g,'</p><p>')"></div>
      <div class="links" v-if="m.exhibits?.length">
        <h3>关联展区</h3>
        <router-link v-for="ek in m.exhibits" :key="ek" :to="'/exhibit/'+ek" class="btn">→ {{ ek }}</router-link>
      </div>
      <router-link to="/mathematicians" class="back">← 返回数学家长廊</router-link>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const m = ref(null)
onMounted(async () => {
  const r = await fetch('/api/museum/exhibits')
  const d = await r.json()
  // Mathematicians data is in settings, fetch from API
  // For now use hardcoded data
  const data = {
    newton:{name:'艾萨克·牛顿',name_en:'Isaac Newton',years:'1643–1727',contributions:'微积分、万有引力定律、光学',quote:'如果说我看得比别人更远，那是因为我站在巨人的肩膀上。',exhibits:['derivatives','integrals'],story:'1665年，剑桥因瘟疫关闭，23岁的牛顿回到乡下。在18个月里，他发明了微积分（他称之为"流数法"）。他还发现了万有引力定律。这18个月被称为科学史上最富有成果的"奇迹年"。'},
    leibniz:{name:'戈特弗里德·莱布尼茨',years:'1646–1716',contributions:'微积分符号系统（∫, d/dx）、二进制',quote:'∫ 是一个最美的字母，它把无穷细小的部分加总成完整的整体。',exhibits:['derivatives','integrals','series'],story:'莱布尼茨独立于牛顿发明了微积分，但他设计的符号系统优雅得多，至今仍被全世界使用。这引发了一场关于"谁先发明微积分"的激烈争论。'},
    euler:{name:'莱昂哈德·欧拉',years:'1707–1783',contributions:'e^(iπ)+1=0、图论、流体力学',quote:'数学是真实世界的语言，上帝用它书写了宇宙。',exhibits:['series','integrals','multivariable'],story:'欧拉是历史上最高产的数学家——发表了超过850篇论文。即使在双目失明的最后17年，他依然以惊人的速度产出数学成果。他发现了最美公式 e^(iπ)+1=0。'},
    gauss:{name:'卡尔·弗里德里希·高斯',years:'1777–1855',contributions:'数论、正态分布、最小二乘法',quote:'数学是科学的皇后，数论是数学的皇后。',exhibits:['integrals','multivariable','series'],story:'高斯10岁时，老师让全班算1+2+...+100，他几秒内就发现了配对法(1+100)×50=5050。他几乎在所有数学分支都做出了深远贡献。'},
    fourier:{name:'约瑟夫·傅里叶',years:'1768–1830',contributions:'傅里叶级数、傅里叶变换',quote:'对自然的深入研究是数学发现最肥沃的土壤。',exhibits:['series','derivatives'],story:'傅里叶在研究热传导时提出：任何周期函数都可以表示成正弦波的无穷和。当时被认为不严谨，今天驱动着MP3、JPEG、5G。'},
    ramanujan:{name:'拉马努金',years:'1887–1920',contributions:'无穷级数、整数分拆、π的公式',quote:'一个方程对我没有意义，除非它表达的是上帝的思想。',exhibits:['series','integrals'],story:'拉马努金出身贫困，几乎靠自学。他在笔记本上记录了近4000个公式。英国数学家哈代看后说："这些公式一定是对的，因为没有人能编造出这么复杂的东西。"'},
    cauchy_weierstrass:{name:'柯西 & 魏尔斯特拉斯',years:'1789–1857 / 1815–1897',contributions:'ε-δ极限定义、分析严密化',quote:'数学的本质不在于数字，而在于严密的逻辑推理。',exhibits:['limits'],story:'牛顿发明微积分后，"无穷小量"困扰了数学家近200年。柯西和魏尔斯特拉斯用ε-δ语言终于为微积分打下了坚实的逻辑基础。'},
  }
  m.value = data[route.params.key]
})
</script>
<style scoped>
.hero { background:linear-gradient(135deg,#1a1a2e,#2d1b69,#1a1a2e); color:#fff; text-align:center; padding:48px 32px; }
.hero h1 { font-size:32px; margin:0 0 8px; }
.years { opacity:0.5; }
.contrib { opacity:0.8; margin-top:8px; font-size:16px; }
.content { max-width:700px; margin:0 auto; padding:32px 20px; }
blockquote { border-left:3px solid #6b5e4a; padding:12px 20px; background:#f0f2f4; border-radius:0 8px 8px 0; font-style:italic; color:#505560; margin:20px 0; }
.story { font-size:15px; line-height:2; }
.links { margin:24px 0; }
.links h3 { margin-bottom:8px; }
.btn { display:inline-block; padding:6px 14px; border:1px solid #4a6a8a; color:#4a6a8a; border-radius:4px; text-decoration:none; margin:4px; }
.back { display:block; text-align:center; margin-top:32px; color:#4a6a8a; text-decoration:none; }
</style>
