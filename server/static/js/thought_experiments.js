/**
 * ThoughtExperiments — Interactive exploration framework for math concepts.
 * Provides lightweight Plotly-based "thought experiments" that guide
 * users to discover mathematical truths through interaction.
 */
var ThoughtExperiments = (function() {

  // ── Experiment definitions per topic ──
  var topics = {};

  function register(topic, experiments) {
    topics[topic] = experiments;
  }

  // ── Render experiments for a topic ──
  function render(topic, container) {
    var exps = topics[topic] || [];
    if (!exps.length) return;

    exps.forEach(function(exp, i) {
      var card = document.createElement('div');
      card.className = 'te-card';
      card.id = 'te-' + exp.id;

      var header = document.createElement('div');
      header.className = 'te-header';
      header.innerHTML = '<span class="te-number">' + (i+1) + '</span><div><h4>' + exp.title + '</h4><p>' + exp.prompt + '</p></div>';
      card.appendChild(header);

      var plotDiv = document.createElement('div');
      plotDiv.className = 'te-plot';
      plotDiv.id = 'te-plot-' + exp.id;
      card.appendChild(plotDiv);

      var controls = document.createElement('div');
      controls.className = 'te-controls';
      controls.id = 'te-controls-' + exp.id;
      card.appendChild(controls);

      var reveal = document.createElement('div');
      reveal.className = 'te-reveal';
      reveal.innerHTML = '<button class="btn btn-sm" onclick="ThoughtExperiments.reveal(\'' + exp.id + '\')">💡 揭示答案</button><div class="te-explanation" style="display:none;">' + exp.explanation + '</div>';
      card.appendChild(reveal);

      container.appendChild(card);

      // Build controls and initial plot
      setupExperiment(exp);
    });
  }

  function setupExperiment(exp) {
    var controlsDiv = document.getElementById('te-controls-' + exp.id);
    var state = {};

    (exp.controls || []).forEach(function(ctrl) {
      state[ctrl.id] = ctrl.value;
      if (ctrl.type === 'slider') {
        var label = document.createElement('label');
        label.innerHTML = ctrl.label + ': <span id="te-val-' + exp.id + '-' + ctrl.id + '">' + ctrl.value + '</span>';
        controlsDiv.appendChild(label);

        var input = document.createElement('input');
        input.type = 'range';
        input.min = ctrl.min;
        input.max = ctrl.max;
        input.step = ctrl.step || 0.1;
        input.value = ctrl.value;
        input.style.width = '180px';
        input.style.margin = '0 8px';
        input.oninput = function() {
          state[ctrl.id] = parseFloat(this.value);
          document.getElementById('te-val-' + exp.id + '-' + ctrl.id).textContent = state[ctrl.id];
          redrawPlot(exp, state);
        };
        controlsDiv.appendChild(input);
      } else if (ctrl.type === 'select') {
        var sel = document.createElement('select');
        sel.id = 'te-sel-' + exp.id + '-' + ctrl.id;
        (ctrl.options || []).forEach(function(opt) {
          var o = document.createElement('option');
          o.value = opt.value; o.textContent = opt.label;
          if (opt.value === ctrl.value) o.selected = true;
          sel.appendChild(o);
        });
        sel.onchange = function() {
          state[ctrl.id] = parseFloat(this.value);
          redrawPlot(exp, state);
        };
        controlsDiv.appendChild(sel);
      }
    });

    redrawPlot(exp, state);
  }

  function redrawPlot(exp, state) {
    var plotDiv = document.getElementById('te-plot-' + exp.id);
    if (!plotDiv || !window.Plotly) return;
    var result = exp.plot(plotDiv, state);
    Plotly.react(plotDiv, result.traces || result.data || [], result.layout || {}, { responsive: true });
  }

  function reveal(id) {
    var card = document.getElementById('te-' + id);
    if (!card) return;
    var explanation = card.querySelector('.te-explanation');
    var btn = card.querySelector('.te-reveal button');
    if (explanation) {
      explanation.style.display = 'block';
      explanation.classList.add('te-explanation-visible');
    }
    if (btn) {
      btn.textContent = '✓ 已揭示';
      btn.disabled = true;
    }
  }

  // ── Exhibit-level thought experiments ──
  (function() {
    // Limits
    register('limits', [
      {
        id: 'guess_limit_sinx',
        title: '猜猜极限是多少？',
        prompt: 'f(x) = sin(x)/x。当 x 趋近于 0 时，f(x)趋近于多少？拖动 x 一点点靠近 0，观察函数值的变化。',
        controls: [
          { type: 'slider', id: 'xval', min: 0.01, max: 2, step: 0.01, value: 1, label: 'x → 0' }
        ],
        plot: function(el, s) {
          var xv = s.xval, xs = [], ys = [];
          for (var i = 0; i <= 200; i++) {
            var x = -6 + 12*i/200;
            xs.push(x);
            ys.push(x === 0 ? null : Math.sin(x)/x);
          }
          return {
            traces: [
              { x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'sin(x)/x', line: {color:'#5b7b94',width:2} },
              { x: [xv], y: [Math.sin(xv)/xv], type: 'scatter', mode: 'markers', marker: {color:'#b55a5a',size:12}, name: 'x='+xv.toFixed(2)+', y='+(Math.sin(xv)/xv).toFixed(4) }
            ],
            layout: { title: 'sin(x)/x, 当前值: '+(Math.sin(xv)/xv).toFixed(4), margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }
          };
        },
        explanation: '<p>当 x→0 时，sin(x)/x → <strong>1</strong>。</p><p>这是微积分中最重要极限之一。直觉理解：在非常小的角度下，sin(x) ≈ x（弧度制下）。所以 sin(x)/x ≈ 1。</p><p>这个极限是推导导数公式 sin\'(x) = cos(x) 的关键。</p>'
      }
    ]);

    // Derivatives
    register('derivatives', [
      {
        id: 'taylor_magic',
        title: '泰勒展开的魔法',
        prompt: '用多项式逼近 sin(x)。增加阶数，看多项式如何越来越高精度地贴合 sin(x)。',
        controls: [
          { type: 'slider', id: 'order', min: 1, max: 15, step: 2, value: 3, label: '泰勒阶数' }
        ],
        plot: function(el, s) {
          var n = s.order, xs = [], ys_sin = [], ys_poly = [];
          for (var i = 0; i <= 300; i++) {
            var x = -2*Math.PI + 4*Math.PI*i/300;
            xs.push(x);
            ys_sin.push(Math.sin(x));
            var poly = 0, fact = 1;
            for (var k = 0; k <= n; k++) {
              if (k > 0) fact *= (2*k) * (2*k+1);
              var term = (k%2===0?1:-1) * Math.pow(x, 2*k+1) / (fact || 1);
              poly += term;
            }
            ys_poly.push(poly);
          }
          return {
            traces: [
              { x: xs, y: ys_sin, type: 'scatter', mode: 'lines', name: 'sin(x)', line: {color:'#5b7b94',width:2} },
              { x: xs, y: ys_poly, type: 'scatter', mode: 'lines', name: 'N='+n, line: {color:'#b55a5a',width:2,dash:'dash'} }
            ],
            layout: { title: 'sin(x) ≈ x - x³/3! + x⁵/5! - ... (到x^'+ (2*n+1) +')', margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)' }
          };
        },
        explanation: '<p>泰勒展开的核心思想：<strong>任何光滑函数都可以用多项式逼近</strong>。</p><p>N=1 时只取了 x 项（一阶近似）<br>N=3 时取了 x - x³/3!（在原点附近已经很准）<br>N=13 时几乎完全重合</p><p>这就是为什么物理学家经常用\"小角度近似\" sin(x)≈x——它其实是泰勒展开的一阶项！</p>'
      }
    ]);

    // Integrals
    register('integrals', [
      {
        id: 'ftc_visual',
        title: '微积分基本定理（FTC）— 微分和积分是逆运算',
        prompt: '上方是 f(x)=sin(x)，下方是以 0 为起点的积分函数 F(x)=∫₀ˣ sin(t)dt。拖动 x，观察两个函数的关系——这\"巧合\"是数学史上最伟大的发现。',
        controls: [
          { type: 'slider', id: 'xpos', min: -3.14, max: 3.14, step: 0.1, value: 1, label: 'x 位置' }
        ],
        plot: function(el, s) {
          var xp = s.xpos, xs = [], ys_sin = [], ys_int = [];
          var N = 200;
          for (var i = 0; i <= N; i++) {
            var x = -3.14 + 6.28*i/N;
            xs.push(x);
            ys_sin.push(Math.sin(x));
            ys_int.push(-Math.cos(x) + 1); // ∫₀ˣ sin(t)dt = -cos(x)+1
          }
          return {
            traces: [
              { x: xs, y: ys_sin, type: 'scatter', mode: 'lines', name: 'f(x)=sin(x)', line: {color:'#5b7b94',width:2} },
              { x: xs, y: ys_int, type: 'scatter', mode: 'lines', name: 'F(x)=∫₀ˣ sin(t)dt', line: {color:'#8b7355',width:2} },
              { x: [xp,xp], y: [-2,2], type: 'scatter', mode: 'lines', line: {color:'#b55a5a',width:1,dash:'dot'} },
              { x: [xp], y: [Math.sin(xp)], type: 'scatter', mode: 'markers', marker: {color:'#5b7b94',size:10} },
              { x: [xp], y: [-Math.cos(xp)+1], type: 'scatter', mode: 'markers', marker: {color:'#8b7355',size:10} }
            ],
            layout: { title: 'F\'(x) = f(x)! F\'('+xp.toFixed(1)+')='+Math.sin(xp).toFixed(3)+', f('+xp.toFixed(1)+')='+Math.sin(xp).toFixed(3), margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:true, legend:{font:{size:11}} }
          };
        },
        explanation: '<p><strong>微积分基本定理（FTC）</strong>：</p><p>1. <strong>F\'(x) = f(x)</strong> — 对积分函数求导，得到原函数<br>2. <strong>∫ₐᵇ f(x)dx = F(b)-F(a)</strong> — 定积分 = 原函数的差值</p><p>这意味着<strong>微分和积分是互逆运算</strong>——就像加法和减法、乘法和除法一样。这是牛顿和莱布尼茨最伟大的发现。</p>'
      }
    ]);

    // Series
    register('series', [
      {
        id: 'harmonic_divergence',
        title: '调和级数 — 无穷多个数的和也可以是无穷大！',
        prompt: '1 + 1/2 + 1/3 + 1/4 + ... 虽然每一项都在变小，但加起来却是无穷大。增加项数，观察它如何慢慢但坚定地攀升——没有任何上限。',
        controls: [
          { type: 'slider', id: 'terms', min: 10, max: 500, step: 10, value: 50, label: '项数 N' }
        ],
        plot: function(el, s) {
          var N = s.terms, sums = [], partial = 0;
          for (var k = 1; k <= N; k++) { partial += 1/k; sums.push(partial); }
          return {
            traces: [{ y: sums, type: 'scatter', mode: 'lines', name: '调和级数部分和', fill:'tozeroy', fillcolor:'rgba(91,123,148,0.08)', line:{color:'#5b7b94',width:2}, marker:{size:3} }],
            layout: { title: '调和级数前'+N+'项和 = '+partial.toFixed(3)+' (还在涨...)', xaxis:{title:'项数'}, yaxis:{title:'部分和'}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }
          };
        },
        explanation: '<p>调和级数是<strong>发散</strong>的——虽然每一项都趋近于 0，但和却是无穷大。</p><p>证明思路：1/3+1/4 > 1/2, 1/5+1/6+1/7+1/8 > 1/2... 可以把级数分成无穷多组，每组都大于 1/2。</p><p>对比：1+1/4+1/9+1/16+... = π²/6 ≈ 1.645（收敛！）这就是为什么\"项趋近于0\"不是级数收敛的充分条件。</p>'
      }
    ]);

    // Multivariable
    register('multivariable', [
      {
        id: 'contour_explorer',
        title: '等高线 — 用二维地图表示三维信息',
        prompt: '考察函数 f(x,y) = x² + 2y²。移动 x 和 y，观察你在三维碗形曲面上所处的位置——以及它对应的等高线位置。',
        controls: [
          { type: 'slider', id: 'px', min: -2.5, max: 2.5, step: 0.1, value: 1, label: 'x' },
          { type: 'slider', id: 'py', min: -2.5, max: 2.5, step: 0.1, value: 0.5, label: 'y' }
        ],
        plot: function(el, s) {
          var px = s.px, py = s.py, N = 40;
          var xs = [], ys = [], zs = [];
          for (var i = 0; i < N; i++) {
            xs.push(-3 + 6*i/(N-1));
            ys.push(-3 + 6*i/(N-1));
          }
          var zGrid = [];
          for (var i = 0; i < N; i++) { var row = []; for (var j = 0; j < N; j++) row.push(xs[i]*xs[i] + 2*ys[j]*ys[j]); zGrid.push(row); }
          return {
            traces: [
              { x: xs, y: ys, z: zGrid, type: 'surface', colorscale: 'YlGnBu', opacity: 0.7, showscale: false },
              { x: [px], y: [py], z: [px*px+2*py*py+0.5], type: 'scatter3d', mode: 'markers', marker: {color:'#b55a5a',size:8} }
            ],
            layout: { title: 'f('+px.toFixed(1)+','+py.toFixed(1)+') = '+(px*px+2*py*py).toFixed(2), scene:{xaxis:{title:'x'},yaxis:{title:'y'},zaxis:{title:'f'}}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)' }
          };
        },
        explanation: '<p>f(x,y) = x² + 2y² 的<strong>等高线</strong>是一些<strong>椭圆</strong>——因为 z = 常数 意味着 x² + 2y² = C。</p><p>因为 y² 的系数 (2) 比 x² 的系数 (1) 大，所以曲面在 y 方向上更\"陡\"。梯度的方向是 (2x, 4y)，指向函数增长最快的方向。</p>'
      }
    ]);
  })();

  // ── Mathematician thought recreations ──
  function renderMathematician(key, container) {
    var recreations = {
      'newton': [
        {
          id: 'newton_fluxion',
          title: '流数法 — 牛顿如何发现导数',
          prompt: '牛顿把运动看作\"流动的量\"（fluent），把变化率看作\"流数\"（fluxion）。拖动 x 坐标，观察切线斜率如何变化——这就是牛顿眼中\"瞬间的变化速度\"。',
          controls: [
            { type: 'slider', id: 'xpos', min: -2.5, max: 2.5, step: 0.1, value: 1, label: '切点 x' }
          ],
          plot: function(el, s) {
            var xs = [], ys = [];
            for (var i = 0; i <= 200; i++) { var x = -3 + 6*i/200; xs.push(x); ys.push(x*x); }
            var x0 = s.xpos;
            var tx = [x0 - 1.2, x0 + 1.2];
            var ty = [x0*x0 + 2*x0*(-1.2), x0*x0 + 2*x0*(1.2)];
            return {
              traces: [
                { x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'f(x)=x²', line: { color: '#5b7b94', width: 2 } },
                { x: tx, y: ty, type: 'scatter', mode: 'lines', name: '切线', line: { color: '#b55a5a', width: 2, dash: 'dash' } },
                { x: [x0], y: [x0*x0], type: 'scatter', mode: 'markers', marker: { size: 8, color: '#b55a5a' } }
              ],
              layout: { title: 'f(x)=x², 切点 x=' + x0.toFixed(1) + ', 斜率=' + (2*x0).toFixed(1), margin: { t:40,r:20,b:40,l:40 }, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)' }
            };
          },
          explanation: '<p>牛顿把函数看作\"流动的量\"。他在《自然哲学的数学原理》中写道：<em>\"我把量看成是逐渐增加的，就像它们在相等时间内被产生的样子。\"</em></p><p>🎯 <strong>核心思想</strong>：导数不是抽象的公式，而是<em>变化的速度</em>。x² 在 x=2 处的导数是 4 —— 这意味着当 x 在 2 附近微小变化时，x² 的变化大约是位移的 4 倍。</p>'
        }
      ],
      'leibniz': [
        {
          id: 'leibniz_symbol',
          title: '∫ 和 d/dx — 为什么莱布尼茨的符号赢了？',
          prompt: '莱布尼茨用 ∫（summa的拉长S）表示积分，用 d/dx 表示微分。拖动矩形数量，观察 ∫ 符号的真正含义——把无穷多个微小量\\"加总\\"。',
          controls: [
            { type: 'slider', id: 'nrect', min: 2, max: 50, step: 1, value: 5, label: '矩形数量 n' }
          ],
          plot: function(el, s) {
            var n = s.nrect;
            function f(x) { return x*x; }
            var a = 0, b = 2, dx = (b-a)/n, area = 0;
            var xs = [], ys = [];
            for (var i = 0; i <= 200; i++) { var x = a + (b-a)*i/200; xs.push(x); ys.push(f(x)); }
            var rx = [], ry = [];
            for (var i = 0; i < n; i++) {
              var xL = a+i*dx, xR = xL+dx, yH = f(xL);
              area += dx*yH;
              rx.push(xL,xR,xR,xL,xL,null);
              ry.push(0,0,yH,yH,0,null);
            }
            return {
              traces: [
                { x: xs, y: ys, type: 'scatter', mode: 'lines', fill:'tozeroy', fillcolor:'rgba(91,123,148,0.08)', line:{color:'#5b7b94',width:2} },
                { x: rx, y: ry, type: 'scatter', mode: 'lines', fill:'toself', fillcolor:'rgba(139,115,85,0.25)', line:{color:'#8b7355',width:1} }
              ],
              layout: { title: '∫₀² x² dx ≈ '+area.toFixed(3)+' (精确: '+(8/3).toFixed(3)+')', margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend: false }
            };
          },
          explanation: '<p>莱布尼茨的符号系统之所以胜出，是因为它<strong>承载了直觉</strong>：</p><ul><li><strong>∫</strong> 是拉长的 S，代表 Sum（求和）—— 把无穷小的矩形面积加起来</li><li><strong>dx</strong> 中的 d 代表 difference（差）—— 无限小的变化量</li><li>牛顿用 ẋ、ẏ 表示流数，但不如 dy/dx 直观</li></ul><p>莱布尼茨深知符号的力量。他说过：<em>\"好的符号就像一个设备正确的天平——它们替我们思考。\"</em></p>'
        }
      ],
      'euler': [
        {
          id: 'euler_basel',
          title: '巴塞尔问题 — 自然数的平方和 = π²/6 ？！',
          prompt: '1 + 1/4 + 1/9 + 1/16 + ... 这个看起来和圆周率毫无关系的无穷和，竟然等于 π²/6。增加项数，观察部分和如何奇妙地趋近 π²/6。',
          controls: [
            { type: 'slider', id: 'terms', min: 1, max: 100, step: 1, value: 5, label: '项数 N' }
          ],
          plot: function(el, s) {
            var N = s.terms, sums = [], partial = 0;
            for (var k = 1; k <= N; k++) { partial += 1/(k*k); sums.push(partial); }
            var target = Math.PI*Math.PI/6;
            var line = Array(N).fill(target);
            return {
              traces: [
                { y: sums, type: 'scatter', mode: 'lines+markers', name: '部分和', line: {color:'#5b7b94',width:2}, marker:{size:4} },
                { y: line, type: 'scatter', mode: 'lines', name: 'π²/6 ≈ '+target.toFixed(4), line: {color:'#b55a5a',width:1,dash:'dash'} }
              ],
              layout: { title: '前N项和 → π²/6 = '+target.toFixed(4), xaxis:{title:'项数'}, yaxis:{title:'部分和'}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)' }
            };
          },
          explanation: '<p>1735年，28岁的欧拉解决了困扰数学界近一个世纪的巴塞尔问题。</p><p>他的证明是天才般的——把 sin(x) 写成一个无穷乘积（就像多项式因式分解），然后比较系数。这个想法在当时非常大但，但结果是正确的。</p><p>欧拉晚年回忆：<em>\"我花了7年时间，反复试验不同的方法，直到最后一刻，它如此优雅地出现。\"</em></p>'
        }
      ],
      'fourier': [
        {
          id: 'fourier_harmonics',
          title: '任何声音都是一堆正弦波的叠加',
          prompt: '傅里叶在1822年断言：<em>任何</em>周期函数都可以表示成正弦波的和。当时几乎所有数学家都说这不可能。拖动滑块加谐波，看方波如何从一堆正弦波中浮现。',
          controls: [
            { type: 'slider', id: 'harmonics', min: 1, max: 20, step: 1, value: 3, label: '谐波数 N' }
          ],
          plot: function(el, s) {
            var N = s.harmonics, xs = [], ys = [];
            for (var i = 0; i <= 400; i++) {
              var x = -2*Math.PI + 4*Math.PI*i/400;
              xs.push(x);
              var val = 0;
              for (var k = 1; k <= N; k++) { val += Math.sin((2*k-1)*x)/(2*k-1); }
              ys.push(4/Math.PI * val);
            }
            return {
              traces: [{ x: xs, y: ys, type: 'scatter', mode: 'lines', name: 'N='+N, line: {color:'#5b7b94',width:2} }],
              layout: { title: '方波的傅里叶级数逼近 (N='+N+')', xaxis:{title:'x'}, yaxis:{range:[-1.8,1.8]}, margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend:false }
            };
          },
          explanation: '<p>傅里叶在研究热传导时发现了这个惊人的事实。他写道：<em>\"对自然的深入研究是数学发现最肥沃的土壤。\"</em></p><p>今天：<strong>MP3音频</strong>用傅里叶变换压缩声音、<strong>JPEG图片</strong>用离散余弦变换压缩图像、<strong>5G通信</strong>用正交频分复用（OFDM）——全是傅里叶变换。</p><p>一个被当时数学家嘲笑\"不严谨\"的想法，200年后改变了整个世界。</p>'
        }
      ],
      'cauchy_weierstrass': [
        {
          id: 'cauchy_epsilon',
          title: 'ε-δ — 一道200年的难题终于被解决',
          prompt: '从牛顿1687年发表《原理》到柯西1821年给出严密定义，数学家们争论了134年：\"无穷小量\"到底是零还是不是零？拖动 ε，观察需要多大的 δ 才能让函数值落在 (L-ε, L+ε) 范围内。',
          controls: [
            { type: 'slider', id: 'eps', min: 0.05, max: 1.5, step: 0.05, value: 0.5, label: 'ε (容许误差)' }
          ],
          plot: function(el, s) {
            var eps = s.eps, x0 = 1, L = 2, delta = eps;
            var margin = Math.max(3*eps, 1.5);
            var xs = [], fxs = [];
            for (var i = 0; i <= 200; i++) { var x = x0-margin+2*margin*i/200; xs.push(x); fxs.push(x===x0 ? null : x+1); }
            return {
              traces: [
                { x: xs, y: fxs, type: 'scatter', mode: 'lines', name: 'f(x)', line: {color:'#5b7b94',width:2} },
                { x: [x0], y: [L], type: 'scatter', mode: 'markers', marker: {color:'#b55a5a',size:10,symbol:'x'} },
                { x: [x0-margin,x0+margin], y: [L+eps,L+eps], type: 'scatter', mode: 'lines', line: {color:'rgba(74,124,89,0.4)',dash:'dash'} },
                { x: [x0-margin,x0+margin], y: [L-eps,L-eps], type: 'scatter', mode: 'lines', line: {color:'rgba(74,124,89,0.4)',dash:'dash'} },
                { x: [x0-delta,x0-delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: {color:'rgba(139,115,85,0.4)',dash:'dot'} },
                { x: [x0+delta,x0+delta], y: [L-eps-0.5,L+eps+0.5], type: 'scatter', mode: 'lines', line: {color:'rgba(139,115,85,0.4)',dash:'dot'} }
              ],
              layout: { title: 'ε='+eps.toFixed(2)+' → δ='+delta.toFixed(2), margin:{t:40,r:20,b:40,l:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', showlegend: false }
            };
          },
          explanation: '<p><strong>这可能是数学史上最重要的一段话</strong>——柯西在1821年写道：</p><blockquote style=\"font-size:13px;\">\"当变量依次取的值无限趋近一个固定值，使得它们之间的差变得任意小——这时我们说该变量有极限。\"</blockquote><p>魏尔斯特拉斯后来用更精确的 ε-δ 语言表达：</p><blockquote style=\"font-size:13px;\">\"对任意 ε>0，存在 δ>0，使得当 0<|x-x₀|<δ 时，|f(x)-L|<ε。\"</blockquote><p>这56个符号，终结了200年来关于\"无穷小\"的争论。微积分终于不再依赖\"直觉\"，而是建立在严密的逻辑之上。</p>'
        }
      ]
    };

    var recs = recreations[key] || [];
    if (!recs.length) return;

    recs.forEach(function(exp, i) {
      var card = document.createElement('div');
      card.className = 'te-card';
      card.id = 'thr-' + exp.id;

      var header = document.createElement('div');
      header.className = 'te-header';
      header.innerHTML = '<span class="te-number thr-number">' + (i+1) + '</span><div><h4>' + exp.title + '</h4><p>' + exp.prompt + '</p></div>';
      card.appendChild(header);

      var plotDiv = document.createElement('div');
      plotDiv.className = 'te-plot';
      plotDiv.id = 'te-plot-' + exp.id;
      card.appendChild(plotDiv);

      var controls = document.createElement('div');
      controls.className = 'te-controls';
      controls.id = 'te-controls-' + exp.id;
      card.appendChild(controls);

      var reveal = document.createElement('div');
      reveal.className = 'te-reveal';
      reveal.innerHTML = '<button class="btn btn-sm" onclick="ThoughtExperiments.reveal(\'' + exp.id + '\')">💡 揭示答案</button><div class="te-explanation" style="display:none;">' + exp.explanation + '</div>';
      card.appendChild(reveal);

      container.appendChild(card);

      setupExperiment(exp);
    });
  }

  return { register, render, reveal, renderMathematician };
})();
