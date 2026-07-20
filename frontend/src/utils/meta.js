import { useHead } from '@vueuse/head'

const metaTags = {
  home: {
    title: '数学博物馆 — 知其然，知其所以然',
    description: '交互式探索微积分、线性代数、概率论的数学之美',
    ogType: 'website',
  },
  gaoshu: {
    title: '微积分的世界 — 数学博物馆',
    description: '极限、导数、积分、级数、多元微积分',
    ogType: 'website',
  },
  exhibit: {
    title: '展区 — 数学博物馆',
    description: '交互式数学展览',
    ogType: 'article',
  },
  fractal: {
    title: '分形探索 — 数学博物馆',
    description: 'Mandelbrot 集、Julia 集、Lorenz 吸引子',
    ogType: 'website',
  },
  gallery: {
    title: '数学之美 — 数学博物馆',
    description: '欧拉恒等式、巴塞尔问题、高斯积分',
    ogType: 'website',
  },
  mathematicians: {
    title: '数学家长廊 — 数学博物馆',
    description: '伟大数学家的故事',
    ogType: 'website',
  },
  workshop: {
    title: '函数工坊 — 数学博物馆',
    description: '2D曲线、3D曲面、向量场、AI绘图',
    ogType: 'website',
  },
  practice: {
    title: '练习 — 数学博物馆',
    description: 'AI 出题与批改',
    ogType: 'website',
  },
  news: {
    title: '数学新闻 — 数学博物馆',
    description: '最新的数学界动态',
    ogType: 'website',
  },
  admin: {
    title: '管理后台 — 数学博物馆',
    description: '用户管理',
    ogType: 'website',
  },
  'not-found': {
    title: '404 — 页面未找到',
    description: '抱歉，您访问的页面不存在',
    ogType: 'website',
  },
}

export function useMeta(titleKey) {
  const config = metaTags[titleKey] || { title: '数学博物馆', description: '', ogType: 'website' }
  useHead({
    title: config.title,
    meta: [
      { name: 'description', content: config.description },
      { property: 'og:title', content: config.title },
      { property: 'og:description', content: config.description },
      { property: 'og:type', content: config.ogType },
    ],
  })
}
