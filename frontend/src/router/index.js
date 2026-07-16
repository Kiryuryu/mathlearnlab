import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', meta: { titleKey: 'nav.home' }, component: () => import('@/views/HomeView.vue') },
  { path: '/gaoshu', name: 'gaoshu', meta: { titleKey: 'nav.exhibits' }, component: () => import('@/views/GaoshuView.vue') },
  { path: '/exhibit/:topic', name: 'exhibit', meta: { titleKey: 'nav.exhibits' }, component: () => import('@/views/ExhibitView.vue') },
  { path: '/workshop', name: 'workshop', meta: { titleKey: 'nav.workshop' }, component: () => import('@/views/WorkshopView.vue') },
  { path: '/fractal', name: 'fractal', meta: { titleKey: 'nav.fractal' }, component: () => import('@/views/FractalView.vue') },
  { path: '/gallery', name: 'gallery', meta: { titleKey: 'gallery.title' }, component: () => import('@/views/GalleryView.vue') },
  { path: '/mathematicians', name: 'mathematicians', meta: { titleKey: 'nav.mathematicians' }, component: () => import('@/views/MathematiciansView.vue') },
  { path: '/mathematicians/:key', name: 'mathematician', meta: { titleKey: 'nav.mathematicians' }, component: () => import('@/views/MathematicianView.vue') },
  { path: '/practice/:topic?', name: 'practice', meta: { titleKey: 'nav.practice' }, component: () => import('@/views/PracticeView.vue') },
  { path: '/news', name: 'news', meta: { titleKey: 'nav.news' }, component: () => import('@/views/NewsView.vue') },
  { path: '/admin', name: 'admin', meta: { titleKey: 'admin.title' }, component: () => import('@/views/AdminView.vue') },
  { path: '/:path(.*)', name: 'not-found', meta: { titleKey: 'notFound.title' }, component: () => import('@/views/NotFoundView.vue') }
]

export default createRouter({ history: createWebHistory(), routes })
