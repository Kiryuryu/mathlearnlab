// Self-hosted (server/static/vendor/plotly.min.js) so charts work reliably in
// mainland China — public CDNs like jsdelivr can be slow or blocked there.
const PLOTLY_SRC = '/static/vendor/plotly.min.js'
let _promise = null

export function loadPlotly() {
  if (typeof window !== 'undefined' && window.Plotly) return Promise.resolve(window.Plotly)
  if (_promise) return _promise
  _promise = new Promise((resolve, reject) => {
    const s = document.createElement('script')
    s.src = PLOTLY_SRC
    s.async = true
    s.onload = () => resolve(window.Plotly)
    s.onerror = (_e) => { _promise = null; reject(new Error('Plotly failed to load')) }
    document.head.appendChild(s)
  })
  return _promise
}
