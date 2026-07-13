// MuseumViz — Interactive mathematical visualizations using Plotly.js
var MuseumViz = (function() {

  var _epsVal = 0.5, _tanA = 0, _riemN = 10, _fourierN = 3;
  var _rafId = null;

  // ── Epsilon-Delta Slider (Limits) ──
  function epsilonDelta(container) {
    var x0 = 1, L = 2;

    function buildTraces() {
      var epsilon = MuseumViz._epsVal, delta = epsilon;
      var margin = Math.max(3 * epsilon, 1.5);
      var xs = [], fx = [];
      for (var i = 0; i <= 200; i++) {
        var x = x0 - margin + 2*margin*i/200;
        xs.push(x); fx.push(x === x0 ? null : x + 1);
      }
      return [
        { x: xs, y: fx, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 }, name: 'f(x)' },
        { x: [x0], y: [L], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10, symbol: 'x' }, name: 'limit' },
        { x: [x0-margin, x0+margin], y: [L+epsilon, L+epsilon], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' }, name: 'L+ε' },
        { x: [x0-margin, x0+margin], y: [L-epsilon, L-epsilon], type: 'scatter', mode: 'lines', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' }, name: 'L-ε' },
        { x: [x0-delta, x0-delta], y: [L-epsilon-0.5, L+epsilon+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' }, name: 'x-δ' },
        { x: [x0+delta, x0+delta], y: [L-epsilon-0.5, L+epsilon+0.5], type: 'scatter', mode: 'lines', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' }, name: 'x+δ' }
      ];
    }

    function render() {
      var epsilon = MuseumViz._epsVal;
      var layout = {
        title: 'ε-δ: ε=' + epsilon.toFixed(2) + ', δ=' + epsilon.toFixed(2),
        xaxis: { title: 'x' }, yaxis: { title: 'f(x)' },
        showlegend: false, margin: { t:40, r:20, b:40, l:40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, buildTraces(), layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>拖动 ε: <span id="epsVal">' + MuseumViz._epsVal.toFixed(2) + '</span></label><br>' +
      '<input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="' + MuseumViz._epsVal + '" style="width:260px;">';
    document.getElementById('epsSlider').oninput = function() {
      var v = parseFloat(this.value);
      document.getElementById('epsVal').textContent = v.toFixed(2);
      MuseumViz._epsVal = v;
      cancelAnimationFrame(_rafId);
      _rafId = requestAnimationFrame(render);
    };
    render();
  }

  // ── Tangent Line (Derivatives) ──
  function tangentLine(container) {
    function f(x) { return x*x; }
    function fp(x) { return 2*x; }

    function buildTraces() {
      var a = MuseumViz._tanA;
      var xs = [], ys = [];
      for (var i = 0; i <= 200; i++) { var x = -3 + 6*i/200; xs.push(x); ys.push(f(x)); }
      return [
        { x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 }, name: 'f(x)=x²' },
        { x: [a-1.5, a+1.5], y: [f(a)+fp(a)*(-1.5), f(a)+fp(a)*1.5], type: 'scatter', mode: 'lines', line: { color: '#a45050', width: 2, dash: 'dash' }, name: 'tangent' },
        { x: [a], y: [f(a)], type: 'scatter', mode: 'markers', marker: { color: '#a45050', size: 10 }, name: 'point' }
      ];
    }

    function render() {
      var a = MuseumViz._tanA;
      var layout = {
        title: 'f\'(x)=' + fp(a).toFixed(1) + ' at x=' + a.toFixed(1),
        xaxis: { range: [-3,3] }, yaxis: {},
        showlegend: false, margin: { t:40, r:20, b:40, l:40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, buildTraces(), layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>切点 x = <span id="tanVal">0.0</span></label><br>' +
      '<input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="0" style="width:260px;">';
    var slider = document.getElementById('tanSlider');
    var label = document.getElementById('tanVal');
    slider.oninput = function() {
      var v = parseFloat(this.value);
      label.textContent = v.toFixed(1);
      MuseumViz._tanA = v;
      cancelAnimationFrame(_rafId);
      _rafId = requestAnimationFrame(render);
    };

    container.parentElement.addEventListener('mousemove', function(e) {
      var rect = container.getBoundingClientRect();
      var xRel = (e.clientX - rect.left) / rect.width * 6 - 3;
      var a = Math.max(-2.5, Math.min(2.5, Math.round(xRel*10)/10));
      MuseumViz._tanA = a;
      slider.value = a;
      label.textContent = a.toFixed(1);
      cancelAnimationFrame(_rafId);
      _rafId = requestAnimationFrame(render);
    });
    render();
  }

  // ── Riemann Sum (Integrals) ──
  function riemannSum(container) {
    function f(x) { return x*x; }

    function buildTraces() {
      var n = MuseumViz._riemN, a = 0, b = 2, dx = (b-a)/n, area = 0;
      var xs = [], ys = [];
      for (var i = 0; i <= 200; i++) { var x = a - 0.5 + (b-a+1)*i/200; xs.push(x); ys.push(f(x)); }
      var rx = [], ry = [];
      for (var i = 0; i < n; i++) {
        var xL = a+i*dx, xR = xL+dx, yH = f(xL); area += dx*yH;
        rx.push(xL, xR, xR, xL, xL, null); ry.push(0, 0, yH, yH, 0, null);
      }
      return [
        { x: xs, y: ys, type: 'scatter', mode: 'lines', fill: 'tozeroy', fillcolor: 'rgba(74,106,138,0.1)', line: { color: '#4a6a8a', width: 2 }, name: 'f(x)' },
        { x: rx, y: ry, type: 'scatter', mode: 'lines', fill: 'toself', fillcolor: 'rgba(107,94,74,0.3)', line: { color: '#6b5e4a', width: 1 }, name: 'Riemann' }
      ];
    }

    function render() {
      var n = MuseumViz._riemN, a = 0, b = 2, dx = (b-a)/n, area = 0;
      for (var i = 0; i < n; i++) area += dx * f(a+i*dx);
      var layout = {
        title: 'Riemann sum: n=' + n + ', ≈' + area.toFixed(3) + ' (exact: ' + (8/3).toFixed(3) + ')',
        showlegend: false, margin: { t:40, r:20, b:40, l:40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, buildTraces(), layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>矩形数 n = <span id="nVal">10</span></label><br>' +
      '<input type="range" id="nSlider" min="2" max="100" step="1" value="10" style="width:260px;">';
    document.getElementById('nSlider').oninput = function() {
      var v = parseInt(this.value);
      document.getElementById('nVal').textContent = v;
      MuseumViz._riemN = v;
      cancelAnimationFrame(_rafId);
      _rafId = requestAnimationFrame(render);
    };
    render();
  }

  // ── Fourier Series (Series) ──
  function fourierSeries(container) {
    function buildTraces() {
      var N = MuseumViz._fourierN, xs = [], ys = [];
      for (var i = 0; i <= 400; i++) {
        var x = -2*Math.PI + 4*Math.PI*i/400, s = 0;
        for (var k = 1; k <= N; k++) s += Math.sin((2*k-1)*x)/(2*k-1);
        xs.push(x); ys.push(4/Math.PI * s);
      }
      return [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { color: '#4a6a8a', width: 2 }, name: 'N='+N }];
    }

    function render() {
      var N = MuseumViz._fourierN;
      var layout = {
        title: 'Fourier: N=' + N + ' harmonics',
        xaxis: { title: 'x' }, yaxis: { range: [-1.8, 1.8] },
        showlegend: false, margin: { t:40, r:20, b:40, l:40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, buildTraces(), layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>谐波数 N = <span id="nFourier">3</span></label><br>' +
      '<input type="range" id="fourierSlider" min="1" max="20" step="1" value="3" style="width:260px;">';
    document.getElementById('fourierSlider').oninput = function() {
      var v = parseInt(this.value);
      document.getElementById('nFourier').textContent = v;
      MuseumViz._fourierN = v;
      cancelAnimationFrame(_rafId);
      _rafId = requestAnimationFrame(render);
    };
    render();
  }

  // ── Gradient Descent (Multivariable) ──
  function gradientDescent(container) {
    function f(x, y) { return x*x + 2*y*y; }
    var N = 50, xs = [], ys = [], zGrid = [];
    for (var i = 0; i <= N; i++) { xs.push(-3 + 6*i/N); ys.push(-3 + 6*i/N); }
    for (var i = 0; i < xs.length; i++) { var row = []; for (var j = 0; j < ys.length; j++) row.push(f(xs[i], ys[j])); zGrid.push(row); }
    var px = [2.5], py = [2.5], lr = 0.1;
    for (var i = 0; i < 20; i++) { var xv = px[px.length-1], yv = py[py.length-1]; px.push(xv - lr*2*xv); py.push(yv - lr*4*yv); }
    var pz = px.map(function(_,i) { return f(px[i], py[i]) + 0.2; });

    var traces = [
      { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.8, showscale: false },
      { x: px, y: py, z: pz, type: 'scatter3d', mode: 'lines+markers', marker: { size: 3, color: '#a45050' }, line: { color: '#a45050', width: 4 } }
    ];
    var layout = {
      title: 'Gradient descent: f(x,y) = x² + 2y²',
      scene: { xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: 'f' } },
      margin: { t:40, r:20, b:40, l:40 }, paper_bgcolor: 'rgba(0,0,0,0)',
    };
    Plotly.react(container, traces, layout, { responsive: true });
  }

  return {
    epsilonDelta: epsilonDelta, tangentLine: tangentLine, riemannSum: riemannSum,
    fourierSeries: fourierSeries, gradientDescent: gradientDescent,
    _epsVal: _epsVal, _tanA: _tanA, _riemN: _riemN, _fourierN: _fourierN,
  };
})();

window.MuseumViz = MuseumViz;
