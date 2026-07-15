import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/gaoshu', name: 'gaoshu', component: () => import('@/views/GaoshuView.vue') },
  { path: '/exhibit/:topic', name: 'exhibit', component: () => import('@/views/ExhibitView.vue') },
  { path: '/workshop', name: 'workshop', component: () => import('@/views/WorkshopView.vue') },
  { path: '/fractal', name: 'fractal', component: () => import('@/views/FractalView.vue') },
  { path: '/gallery', name: 'gallery', component: () => import('@/views/GalleryView.vue') },
  { path: '/mathematicians', name: 'mathematicians', component: () => import('@/views/MathematiciansView.vue') },
  { path: '/mathematicians/:key', name: 'mathematician', component: () => import('@/views/MathematicianView.vue') },
  { path: '/practice/:topic?', name: 'practice', component: () => import('@/views/PracticeView.vue') },
  { path: '/:path(.*)', redirect: '/' }
]

export default createRouter({ history: createWebHistory(), routes })
