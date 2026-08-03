// Interactive Plotly visualizations for exhibits.
// Each takes (el, controlsEl, labels) where labels provides i18n strings.

export function museumVizEpsilon(el, controlsEl, labels) {
  let epsVal = 0.5
  function render() {
    const eps = epsVal, x0 = 1, L = 2, delta = eps, margin = Math.max(3*eps, 1.5)
    const xs = [], fx = []
    for (let i = 0; i <= 200; i++) { const x = x0 - margin + 2*margin*i/200; xs.push(x); fx.push(x === x0 ? null : x+1) }
    Plotly.react(el, [
      { x: xs, y: fx, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } },
      { x: [x0], y: [L], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10, symbol: 'x' } },
      { x: [x0-margin,x0+margin], y: [L+eps,L+eps], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } },
      { x: [x0-margin,x0+margin], y: [L-eps,L-eps], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } },
      { x: [x0-delta,x0-delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } },
      { x: [x0+delta,x0+delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } },
    ], { title: 'ε-δ: ε='+eps.toFixed(2)+', δ='+delta.toFixed(2), margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  if (controlsEl) controlsEl.innerHTML = `<label>${labels.epsilon} <span id="epsVal">0.50</span></label><br><input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="0.5" style="width:260px">`
  setTimeout(() => {
    const s = document.getElementById('epsSlider')
    if (s) s.oninput = function() { epsVal = parseFloat(this.value); document.getElementById('epsVal').textContent = epsVal.toFixed(2); render() }
  }, 100)
  render()
}

export function museumVizTangent(el, controlsEl, labels) {
  let tanA = 0
  function f(x) { return x*x }; function fp(x) { return 2*x }
  function render() {
    const a = tanA, xs = [], ys = []
    for (let i = 0; i <= 200; i++) { const x = -3 + 6*i/200; xs.push(x); ys.push(f(x)) }
    Plotly.react(el, [
      { x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } },
      { x: [a-1.5,a+1.5], y: [f(a)+fp(a)*(-1.5), f(a)+fp(a)*1.5], type: 'scatter', mode: 'lines', line: { color: '#a45050', width: 2, dash: 'dash' } },
      { x: [a], y: [f(a)], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10 } },
    ], { title: 'f\'(x)='+fp(a).toFixed(1)+' at x='+a.toFixed(1), xaxis:{range:[-3,3]}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  if (controlsEl) controlsEl.innerHTML = `<label>${labels.tangent} <span id="tanVal">0.0</span></label><br><input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="0" style="width:260px">`
  setTimeout(() => {
    const s = document.getElementById('tanSlider')
    if (s) s.oninput = function() { tanA = parseFloat(this.value); document.getElementById('tanVal').textContent = tanA.toFixed(1); render() }
  }, 100)
  render()
}

export function museumVizRiemann(el, controlsEl, labels) {
  let riemN = 10
  function f(x) { return x*x }
  function render() {
    const n = riemN, a = 0, b = 2, dx = (b-a)/n
    let area = 0
    const xs = [], ys = [], rx = [], ry = []
    for (let i = 0; i <= 200; i++) { const x = a-0.5+(b-a+1)*i/200; xs.push(x); ys.push(f(x)) }
    for (let i = 0; i < n; i++) { const xL = a+i*dx, xR = xL+dx, yH = f(xL); area += dx*yH; rx.push(xL,xR,xR,xL,xL,null); ry.push(0,0,yH,yH,0,null) }
    Plotly.react(el, [
      { x: xs, y: ys, type: 'scatter', mode: 'lines', fill: 'tozeroy', fillcolor: 'rgba(74,106,138,0.1)', line: { color: '#4a6a8a', width: 2 } },
      { x: rx, y: ry, type: 'scatter', mode: 'lines', fill: 'toself', fillcolor: 'rgba(107,94,74,0.3)', line: { color: '#6b5e4a', width: 1 } },
    ], { title: 'Riemann: n='+n+', ≈'+area.toFixed(3)+' (exact:'+(8/3).toFixed(3)+')', margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  if (controlsEl) controlsEl.innerHTML = `<label>${labels.rectangles} <span id="nVal">10</span></label><br><input type="range" id="nSlider" min="2" max="100" step="1" value="10" style="width:260px">`
  setTimeout(() => {
    const s = document.getElementById('nSlider')
    if (s) s.oninput = function() { riemN = parseInt(this.value); document.getElementById('nVal').textContent = riemN; render() }
  }, 100)
  render()
}

export function museumVizFourier(el, controlsEl, labels) {
  let fN = 3
  function render() {
    const N = fN, xs = [], ys = []
    for (let i = 0; i <= 400; i++) { const x = -2*Math.PI+4*Math.PI*i/400; let s = 0; for (let k = 1; k <= N; k++) s += Math.sin((2*k-1)*x)/(2*k-1); xs.push(x); ys.push(4/Math.PI*s) }
    Plotly.react(el, [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 } }], { title: 'Fourier: N='+N+' harmonics', xaxis:{title:'x'}, yaxis:{range:[-1.8,1.8]}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }, { responsive: true })
  }
  if (controlsEl) controlsEl.innerHTML = `<label>${labels.harmonics} <span id="nFourier">3</span></label><br><input type="range" id="fourierSlider" min="1" max="20" step="1" value="3" style="width:260px">`
  setTimeout(() => {
    const s = document.getElementById('fourierSlider')
    if (s) s.oninput = function() { fN = parseInt(this.value); document.getElementById('nFourier').textContent = fN; render() }
  }, 100)
  render()
}

export function museumVizGradient(el, controlsEl) {
  function f(x,y) { return x*x + 2*y*y }
  const N = 50, xs = [], ys = [], zGrid = []
  for (let i = 0; i <= N; i++) { xs.push(-3+6*i/N); ys.push(-3+6*i/N) }
  for (let i = 0; i < xs.length; i++) { const row = []; for (let j = 0; j < ys.length; j++) row.push(f(xs[i], ys[j])); zGrid.push(row) }
  const px = [2.5], py = [2.5]
  for (let i = 0; i < 20; i++) { const x = px[px.length-1], y = py[py.length-1]; px.push(x-0.1*2*x); py.push(y-0.1*4*y) }
  const pz = px.map((_,i) => f(px[i], py[i]) + 0.2)
  Plotly.react(el, [
    { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.8, showscale: false },
    { x: px, y: py, z: pz, type: 'scatter3d', mode: 'lines+markers', marker: { size: 3, color: '#a45050' }, line: { color: '#a45050', width: 4 } }
  ], { title: 'Gradient descent: f(x,y)=x²+2y²', scene:{xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'f'}}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)' }, { responsive: true })
}

export const museumViz = {
  epsilon: museumVizEpsilon,
  tangent: museumVizTangent,
  riemann: museumVizRiemann,
  fourier: museumVizFourier,
  gradient: museumVizGradient,
}
