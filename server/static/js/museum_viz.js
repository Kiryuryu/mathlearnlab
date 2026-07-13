// MuseumViz — Interactive mathematical visualizations using Plotly.js
var MuseumViz = (function() {

  // ── Epsilon-Delta Slider (Limits) ──
  function epsilonDelta(container) {
    var x0 = 1, L = 2; // f(x) = (x^2-1)/(x-1) = x+1, limit at x=1 is 2
    var epsilon = 0.5;

    function plot() {
      var xs = [], ys = [], fx = [];
      var margin = Math.max(3 * epsilon, 1.5);
      for (var i = 0; i <= 200; i++) {
        var x = x0 - margin + (2 * margin * i / 200);
        xs.push(x);
        fx.push(x === x0 ? null : x + 1); // removable discontinuity
      }

      var trace1 = { x: xs, y: fx, type: 'scatter', mode: 'lines', name: 'f(x)',         line: { color: '#4a6a8a', width: 2 } };
      var trace2 = { x: [x0], y: [L], type: 'scatter', mode: 'markers', name: 'x=1, 极限=2', marker: { color: '#a45050', size: 10, symbol: 'x' } };
      // Epsilon band
      var trace3 = { x: [x0 - margin, x0 + margin], y: [L + epsilon, L + epsilon], type: 'scatter', mode: 'lines', name: 'L+ε', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } };
      var trace4 = { x: [x0 - margin, x0 + margin], y: [L - epsilon, L - epsilon], type: 'scatter', mode: 'lines', name: 'L-ε', line: { color: 'rgba(61,107,79,0.5)', dash: 'dash' } };
      // Delta band
      var delta = epsilon; // linear function, delta = epsilon
      var trace5 = { x: [x0 - delta, x0 - delta], y: [L - epsilon - 0.5, L + epsilon + 0.5], type: 'scatter', mode: 'lines', name: 'x-δ', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } };
      var trace6 = { x: [x0 + delta, x0 + delta], y: [L - epsilon - 0.5, L + epsilon + 0.5], type: 'scatter', mode: 'lines', name: 'x+δ', line: { color: 'rgba(107,94,74,0.5)', dash: 'dot' } };

      var layout = {
        title: 'ε-δ 极限定义: ε=' + epsilon.toFixed(2) + ', δ=' + delta.toFixed(2),
        xaxis: { title: 'x', zeroline: false },
        yaxis: { title: 'f(x)', zeroline: false },
        showlegend: false,
        margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2, trace3, trace4, trace5, trace6], layout, { responsive: true });
    }

    // Slider control
    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>拖动 ε: <span id="epsVal">0.50</span></label><br>' +
      '<input type="range" id="epsSlider" min="0.05" max="1.5" step="0.05" value="0.5" style="width:200px;" ' +
      'oninput="var v=parseFloat(this.value);document.getElementById(\'epsVal\').textContent=v.toFixed(2);MuseumViz._epsVal=v;MuseumViz._replot();">';
    plot();
  }

  // ── Tangent Line Animation (Derivatives) ──
  function tangentLine(container) {
    var a = 0; // point of tangency
    function f(x) { return x*x; }
    function fp(x) { return 2*x; }

    function plot() {
      var xs = [], ys = [];
      for (var i = 0; i <= 200; i++) { var x = -3 + 6*i/200; xs.push(x); ys.push(f(x)); }
      var trace1 = { x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'f(x)=x²', line: { color: '#4a6a8a', width: 2 } };
      // Tangent line: y = f(a) + f'(a)(x-a)
      var tx = [a - 1.5, a + 1.5];
      var ty = [f(a) + fp(a)*(-1.5), f(a) + fp(a)*(1.5)];
      var trace2 = { x: tx, y: ty, type: 'scatter', mode: 'lines', name: '切线', line: { color: '#a45050', width: 2, dash: 'dash' } };
      var trace3 = { x: [a], y: [f(a)], type: 'scatter', mode: 'markers', name: '切点', marker: { color: '#a45050', size: 10 } };

      var layout = {
        title: '导数 = 切线斜率: f\'(x)=' + fp(a).toFixed(1) + ' at x=' + a.toFixed(1),
        xaxis: { range: [-3, 3], zeroline: true }, yaxis: { zeroline: true },
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2, trace3], layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>切点 x = <span id="tanVal">0.0</span></label><br>' +
      '<input type="range" id="tanSlider" min="-2.5" max="2.5" step="0.1" value="0" style="width:200px;" ' +
      'oninput="var v=parseFloat(this.value);document.getElementById(\'tanVal\').textContent=v.toFixed(1);MuseumViz._tanA=v;MuseumViz._replotTan();">';
    plot();

    container.parentElement.addEventListener('mousemove', function(e) {
      var rect = container.getBoundingClientRect();
      var xRel = (e.clientX - rect.left) / rect.width * 6 - 3;
      a = Math.max(-2.5, Math.min(2.5, xRel));
      var slider = document.getElementById('tanSlider');
      if (slider) slider.value = a;
      var label = document.getElementById('tanVal');
      if (label) label.textContent = a.toFixed(1);
      plot();
    });
  }

  // ── Riemann Sum Visualization (Integrals) ──
  function riemannSum(container) {
    var n = 10;
    function f(x) { return x*x; }
    function plot() {
      var xs = [], ys = [];
      var a = 0, b = 2, dx = (b-a)/n, area = 0;
      for (var i = 0; i <= 200; i++) { var x = a - 0.5 + (b - a + 1)*i/200; xs.push(x); ys.push(f(x)); }
      var traces = [{ x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'f(x)=x²', fill: 'tozeroy', fillcolor: 'rgba(74,106,138,0.1)', line: { color: '#4a6a8a', width: 2 } }];
      var rx = [], ry = [];
      for (var i = 0; i < n; i++) {
        var xL = a + i*dx, xR = xL + dx, yH = f(xL);
        area += dx * yH;
        rx.push(xL, xR, xR, xL, xL, null);
        ry.push(0, 0, yH, yH, 0, null);
      }
      traces.push({ x: rx, y: ry, type: 'scatter', mode: 'lines', name: '黎曼和', fill: 'toself', fillcolor: 'rgba(107,94,74,0.3)', line: { color: '#6b5e4a', width: 1 } });

      var layout = {
        title: '黎曼和 (左端点): n=' + n + ' 矩形, 面积≈' + area.toFixed(3) + ', 精确值=' + (8/3).toFixed(3),
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, traces, layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>矩形数量 n = <span id="nVal">10</span></label><br>' +
      '<input type="range" id="nSlider" min="2" max="100" step="1" value="10" style="width:200px;" ' +
      'oninput="var v=parseInt(this.value);document.getElementById(\'nVal\').textContent=v;MuseumViz._riemN=v;MuseumViz._replotRiem();">';
    plot();
  }

  // ── Fourier Series (Series) ──
  function fourierSeries(container) {
    var N = 3;
    function squareWave(x, n) {
      var s = 0;
      for (var k = 1; k <= n; k++) { s += Math.sin((2*k-1)*x) / (2*k-1); }
      return 4/Math.PI * s;
    }
    function plot() {
      var xs = [], sw = [];
      for (var i = 0; i <= 400; i++) { var x = -2*Math.PI + 4*Math.PI*i/400; xs.push(x); sw.push(squareWave(x, N)); }
      var traces = [
        { x: xs, y: sw, type: 'scatter', mode: 'lines', name: 'N='+N+' 项近似', line: { color: '#4a6a8a', width: 2 } },
      ];
      var harmonicsInfo = '';
      for (var k = 1; k <= N; k++) { if (k>1) harmonicsInfo += ' + '; harmonicsInfo += 'sin('+(2*k-1)+'x)/'+(2*k-1); }
      var layout = {
        title: '傅里叶级数逼近方波: N=' + N + ' 项',
        xaxis: { title: 'x' }, yaxis: { range: [-1.8, 1.8] },
        showlegend: false, margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, traces, layout, { responsive: true });
    }

    var controls = document.getElementById('vizControls');
    controls.innerHTML = '<label>谐波数量 N = <span id="nFourier">3</span></label><br>' +
      '<input type="range" id="fourierSlider" min="1" max="20" step="1" value="3" style="width:200px;" ' +
      'oninput="var v=parseInt(this.value);document.getElementById(\'nFourier\').textContent=v;MuseumViz._fourierN=v;MuseumViz._replotFourier();">';
    plot();
  }

  // ── Gradient Descent (Multivariable) ──
  function gradientDescent(container) {
    function f(x, y) { return x*x + 2*y*y; }
    function plot() {
      var xs = [], ys = [], zs = [];
      for (var i = 0; i <= 50; i++) {
        var row = [];
        xs.push(-3 + 6*i/50);
        ys.push(-3 + 6*i/50);
      }
      var zGrid = [];
      for (var i = 0; i < xs.length; i++) {
        var row = [];
        for (var j = 0; j < ys.length; j++) { row.push(f(xs[i], ys[j])); }
        zGrid.push(row);
      }
      var trace1 = { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.8, showscale: false };

      // Gradient descent path
      var px = [2.5], py = [2.5], lr = 0.1;
      for (var i = 0; i < 20; i++) {
        var x = px[px.length-1], y = py[py.length-1];
        px.push(x - lr * 2*x); py.push(y - lr * 4*y);
      }
      var pz = px.map(function(_,i) { return f(px[i], py[i]) + 0.2; });
      var trace2 = { x: px, y: py, z: pz, type: 'scatter3d', mode: 'lines+markers', marker: { size: 3, color: '#a45050' }, line: { color: '#a45050', width: 4 } };

      var layout = {
        title: '梯度下降: f(x,y) = x² + 2y², 从 (2.5, 2.5) 开始',
        scene: { xaxis: { title: 'x' }, yaxis: { title: 'y' }, zaxis: { title: 'f(x,y)' } },
        margin: { t: 40, r: 20, b: 40, l: 40 },
        paper_bgcolor: 'rgba(0,0,0,0)',
      };
      Plotly.react(container, [trace1, trace2], layout, { responsive: true });
    }
    plot();
  }

  // State for replot callbacks
  var _epsVal = 0.5, _tanA = 0, _riemN = 10, _fourierN = 3;

  function _replot() {
    var c = document.getElementById('vizPlot'); if (c) epsilonDelta(c);
  }
  function _replotTan() {
    var c = document.getElementById('vizPlot'); if (c) { var old = _tanA; _tanA = MuseumViz._tanA; tangentLine(c); }
  }
  function _replotRiem() {
    var c = document.getElementById('vizPlot'); if (c) { var old = _riemN; _riemN = MuseumViz._riemN; riemannSum(c); }
  }
  function _replotFourier() {
    var c = document.getElementById('vizPlot'); if (c) { var old = _fourierN; _fourierN = MuseumViz._fourierN; fourierSeries(c); }
  }

  return {
    epsilonDelta: epsilonDelta, tangentLine: tangentLine, riemannSum: riemannSum,
    fourierSeries: fourierSeries, gradientDescent: gradientDescent,
    _epsVal: _epsVal, _tanA: _tanA, _riemN: _riemN, _fourierN: _fourierN,
    _replot: _replot, _replotTan: _replotTan, _replotRiem: _replotRiem, _replotFourier: _replotFourier,
  };
})();

// Re-export to global for inline callbacks
window.MuseumViz = MuseumViz;
