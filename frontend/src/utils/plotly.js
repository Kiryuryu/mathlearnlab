const PLOTLY_SRC = 'https://cdn.jsdelivr.net/npm/plotly.js@2.35.2/dist/plotly.min.js'
let _promise = null

export function loadPlotly() {
  if (typeof window !== 'undefined' && window.Plotly) return Promise.resolve(window.Plotly)
  if (_promise) return _promise
  _promise = new Promise((resolve, reject) => {
    const s = document.createElement('script')
    s.src = PLOTLY_SRC
    s.async = true
    s.onload = () => resolve(window.Plotly)
    s.onerror = (e) => { _promise = null; reject(new Error('Plotly failed to load')) }
    document.head.appendChild(s)
  })
  return _promise
}
