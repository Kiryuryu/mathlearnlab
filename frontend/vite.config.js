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
    // rolldown misclassifies the Plotly.react calls as pure and would drop the
    // interactive charts. Keep property side effects (so Plotly.react calls are
    // retained) without disabling tree-shaking wholesale, so unused imports and
    // dead modules can still be eliminated. Verify with a build + grep for
    // "Plotly.react" in the emitted chunks.
    rolldownOptions: {
      treeshake: {
        propertyReadSideEffects: 'always',
        propertyWriteSideEffects: true,
      },
    },
  }
})
