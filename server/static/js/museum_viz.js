// MuseumViz — Interactive mathematical visualizations using Plotly.js
var MuseumViz = (function() {

  // Shared state (read by functions on replot)
  var _epsVal = 0.5, _tanA = 0, _riemN = 10, _fourierN = 3;

  // ── Epsilon-Delta Slider (Limits) ──
  function epsilonDelta(container) {
    var x0 = 1, L = 2;

    function plot() {
      var epsilon = MuseumViz._epsVal;
      var xs = [], fx = [];
      var margin = Math.max(3 * epsilon, 1.5);
      for (var i = 0; i <= 200; i++) {
        var x = x0 - margin + (2 * margin * i / 200);
        xs.push(x);
        fx.push(x === x0 ? null : x + 1);
      }

      var delta = epsilon;
      var trace1 = { x: xs, y: fx, type: 'scatter', mode: 'lines', name: 'f(x)', line: { color: '#4a6a8a', width: 2 } };
      var trace2 = { x: [x0], y: [L], type: 'scatter', mode: 'markers', name: 'x=1, limit=2', marker: { color: '#a45050', size: 10, symbol: 'x' } };
      var trace3 = { x: [x0 - margin, x0 + margin], y: [L + epsilon, L + epsilon], type: 'scatter', mode: 'lines', name: 'L+ε', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } };
      var trace4 = { x: [x0 - margin, x0 + margin], y: [L - epsilon, L - epsilon], type: 'scatter', mode: 'lines', name: 'L-ε', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } };
      var trace5 = { x: [x0 - delta, x0 - delta], y: [L - epsilon - 0.5, L + epsilon + 0.5], type: 'scatter', mode: 'lines', name: 'x-δ', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } };
      var trace6 = { x: [x0 + delta, x0 + delta], y: [L - epsilon - 0.5, L + epsilon + 0.5], type: 'scatter', mode: 'lines', name: 'x+δ', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } };

      var layout = {
        title: 'ε-δ: ε=' + epsilon.toFixed(2) + ', δ=' + delta.toFixed(2),
        xaxis: { title: 'x', zeroline: false }, yaxis: { title: 'f(x)', zeroline: false },
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2, trace3, trace4, trace5, trace6], layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>拖动 ε: <span id="epsVal">' + MuseumViz._epsVal.toFixed(2) + '</span></label><br>' +
      '<input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="' + MuseumViz._epsVal + '" style="width:260px;" ' +
      'oninput="var v=parseFloat(this.value);document.getElementById(\'epsVal\').textContent=v.toFixed(2);MuseumViz._epsVal=v;MuseumViz._replot();">';
    plot();
  }

  // ── Tangent Line (Derivatives) ──
  function tangentLine(container) {
    function f(x) { return x*x; }
    function fp(x) { return 2*x; }

    function plot() {
      var a = MuseumViz._tanA;
      var xs = [], ys = [];
      for (var i = 0; i <= 200; i++) { var x = -3 + 6*i/200; xs.push(x); ys.push(f(x)); }
      var tx = [a - 1.5, a + 1.5];
      var ty = [f(a) + fp(a)*(-1.5), f(a) + fp(a)*(1.5)];
      var trace1 = { x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'f(x)=x²', line: { color: '#4a6a8a', width: 2 } };
      var trace2 = { x: tx, y: ty, type: 'scatter', mode: 'lines', name: 'tangent', line: { color: '#a45050', width: 2, dash: 'dash' } };
      var trace3 = { x: [a], y: [f(a)], type: 'scatter', mode: 'markers', name: 'point', marker: { color: '#a45050', size: 10 } };
      var layout = {
        title: 'f\'(x)=' + fp(a).toFixed(1) + ' at x=' + a.toFixed(1),
        xaxis: { range: [-3, 3], zeroline: true }, yaxis: { zeroline: true },
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2, trace3], layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>切点 x = <span id="tanVal">' + MuseumViz._tanA.toFixed(1) + '</span></label><br>' +
      '<input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="' + MuseumViz._tanA + '" style="width:260px;" ' +
      'oninput="var v=parseFloat(this.value);document.getElementById(\'tanVal\').textContent=v.toFixed(1);MuseumViz._tanA=v;MuseumViz._replotTan();">';
    plot();

    container.parentElement.addEventListener('mousemove', function(e) {
      var rect = container.getBoundingClientRect();
      var xRel = (e.clientX - rect.left) / rect.width * 6 - 3;
      MuseumViz._tanA = Math.max(-2.5, Math.min(2.5, xRel));
      var slider = document.getElementById('tanSlider');
      if (slider) slider.value = MuseumViz._tanA;
      var label = document.getElementById('tanVal');
      if (label) label.textContent = MuseumViz._tanA.toFixed(1);
      plot();
    });
  }

  // ── Riemann Sum (Integrals) ──
  function riemannSum(container) {
    function f(x) { return x*x; }

    function plot() {
      var n = MuseumViz._riemN;
      var a = 0, b = 2, dx = (b-a)/n, area = 0;
      var xs = [], ys = [];
      for (var i = 0; i <= 200; i++) { var x = a - 0.5 + (b - a + 1)*i/200; xs.push(x); ys.push(f(x)); }
      var traces = [{ x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'f(x)=x²', fill: 'tozeroy', fillcolor: 'rgba(74,106,138,0.1)', line: { color: '#4a6a8a', width: 2 } }];
      var rx = [], ry = [];
      for (var i = 0; i < n; i++) {
        var xL = a + i*dx, xR = xL + dx, yH = f(xL);
        area += dx * yH;
        rx.push(xL, xR, xR, xL, xL, null);
        ry.push(0, 0, yH, yH, 0, null);
      }
      traces.push({ x: rx, y: ry, type: 'scatter', mode: 'lines', name: 'Riemann', fill: 'toself', fillcolor: 'rgba(107,94,74,0.3)', line: { color: '#6b5e4a', width: 1 } });
      var layout = {
        title: 'Riemann sum: n=' + n + ', ≈' + area.toFixed(3) + ' (exact: ' + (8/3).toFixed(3) + ')',
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, traces, layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>矩形数 n = <span id="nVal">' + MuseumViz._riemN + '</span></label><br>' +
      '<input type="range" id="nSlider" min="2" max="100" step="1" value="' + MuseumViz._riemN + '" style="width:260px;" ' +
      'oninput="var v=parseInt(this.value);document.getElementById(\'nVal\').textContent=v;MuseumViz._riemN=v;MuseumViz._replotRiem();">';
    plot();
  }

  // ── Fourier Series (Series) ──
  function fourierSeries(container) {
    function squareWave(x, n) {
      var s = 0;
      for (var k = 1; k <= n; k++) { s += Math.sin((2*k-1)*x) / (2*k-1); }
      return 4/Math.PI * s;
    }

    function plot() {
      var N = MuseumViz._fourierN;
      var xs = [], sw = [];
      for (var i = 0; i <= 400; i++) { var x = -2*Math.PI + 4*Math.PI*i/400; xs.push(x); sw.push(squareWave(x, N)); }
      var traces = [{ x: xs, y: sw, type: 'scatter', mode: 'lines', name: 'N='+N, line: { color: '#4a6a8a', width: 2 } }];
      var layout = {
        title: 'Fourier: N=' + N + ' harmonics',
        xaxis: { title: 'x' }, yaxis: { range: [-1.8, 1.8] },
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, traces, layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>谐波数 N = <span id="nFourier">' + MuseumViz._fourierN + '</span></label><br>' +
      '<input type="range" id="fourierSlider" min="1" max="20" step="1" value="' + MuseumViz._fourierN + '" style="width:260px;" ' +
      'oninput="var v=parseInt(this.value);document.getElementById(\'nFourier\').textContent=v;MuseumViz._fourierN=v;MuseumViz._replotFourier();">';
    plot();
  }

  // ── Gradient Descent (Multivariable) ──
  function gradientDescent(container) {
    function f(x, y) { return x*x + 2*y*y; }
    function plot() {
      var N = 50;
      var xs = [], ys = [], zGrid = [];
      for (var i = 0; i <= N; i++) { xs.push(-3 + 6*i/N); ys.push(-3 + 6*i/N); }
      for (var i = 0; i < xs.length; i++) { var row = []; for (var j = 0; j < ys.length; j++) row.push(f(xs[i], ys[j])); zGrid.push(row); }
      var trace1 = { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.8, showscale: false };
      var px = [2.5], py = [2.5], lr = 0.1;
      for (var i = 0; i < 20; i++) {
        var xv = px[px.length-1], yv = py[py.length-1];
        px.push(xv - lr*2*xv); py.push(yv - lr*4*yv);
      }
      var pz = px.map(function(_,i) { return f(px[i], py[i]) + 0.2; });
      var trace2 = { x: px, y: py, z: pz, type: 'scatter3d', mode: 'lines+markers', marker: { size: 3, color: '#a45050' }, line: { color: '#a45050', width: 4 } };
      var layout = {
        title: 'Gradient descent: f(x,y) = x² + 2y²',
        scene: { xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: 'f' } },
        margin: { t: 40, r: 20, b: 40, l: 40 }, paper_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2], layout, { responsive: true });
    }
    plot();
  }

  function _replot()     { var c = document.getElementById('vizPlot'); if (c) epsilonDelta(c); }
  function _replotTan()   { var c = document.getElementById('vizPlot'); if (c) tangentLine(c); }
  function _replotRiem()  { var c = document.getElementById('vizPlot'); if (c) riemannSum(c); }
  function _replotFourier(){ var c = document.getElementById('vizPlot'); if (c) fourierSeries(c); }

  return {
    epsilonDelta: epsilonDelta, tangentLine: tangentLine, riemannSum: riemannSum,
    fourierSeries: fourierSeries, gradientDescent: gradientDescent,
    _epsVal: _epsVal, _tanA: _tanA, _riemN: _riemN, _fourierN: _fourierN,
    _replot: _replot, _replotTan: _replotTan, _replotRiem: _replotRiem, _replotFourier: _replotFourier,
  };
})();

window.MuseumViz = MuseumViz;
