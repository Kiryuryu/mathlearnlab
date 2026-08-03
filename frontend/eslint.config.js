import vue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'

const browserGlobals = {
  window: 'readonly', document: 'readonly', navigator: 'readonly', localStorage: 'readonly',
  URL: 'readonly', FileReader: 'readonly', Image: 'readonly', requestAnimationFrame: 'readonly',
  Plotly: 'readonly', setTimeout: 'readonly', clearTimeout: 'readonly', fetch: 'readonly',
  console: 'readonly', HTMLElement: 'readonly', AbortController: 'readonly', TextDecoder: 'readonly',
  Worker: 'readonly', ImageData: 'readonly', setInterval: 'readonly', clearInterval: 'readonly',
  KeyboardEvent: 'readonly', Event: 'readonly', globalThis: 'readonly',
}

export default [
  {
    ignores: ['node_modules/**', 'dist/**', 'static-spa/**'],
  },
  {
    files: ['**/*.js'],
    languageOptions: { ecmaVersion: 'latest', sourceType: 'module', globals: { ...browserGlobals, __dirname: 'readonly' } },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-undef': 'error',
    },
  },
  {
    files: ['src/workers/**/*.js'],
    languageOptions: { ecmaVersion: 'latest', sourceType: 'module', globals: { self: 'readonly', console: 'readonly' } },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-undef': 'error',
    },
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: browserGlobals,
    },
    plugins: { vue },
    processor: vue.processors['.vue'],
    rules: {
      // Vue-aware unused var check (understands script-setup macros like emit/props/defineProps)
      'vue/no-unused-vars': ['error', { ignorePattern: '^_' }],
      'no-undef': 'error',
    },
  },
]
