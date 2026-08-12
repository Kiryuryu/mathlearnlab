import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const backend = process.env.BACKEND_PORT ? `http://127.0.0.1:${process.env.BACKEND_PORT}` : 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: {
    proxy: {
      '/api': backend,
      '/static': backend,
      '/content': backend
    }
  },
  build: {
    outDir: '../server/static-spa',
    emptyOutDir: true,
    // rolldown misclassifies the Plotly.react calls as pure and drops the interactive charts.
    // Disable tree-shaking so the exhibit visualizations are always built in.
    rolldownOptions: {
      treeshake: {
        propertyReadSideEffects: 'always',
        propertyWriteSideEffects: true,
        annotations: false,
        moduleSideEffects: true,
      },
    },
  }
})
