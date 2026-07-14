## 交互探索：线性变换可视化

拖动下面的矩阵元素，观察标准基向量 (1,0) 和 (0,1) 如何被变换，以及整个坐标网格如何变形。

<div id="linTransform" style="width:100%;height:500px;border:1px solid var(--border);border-radius:8px;margin:16px 0;"></div>

<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:12px 0;">
  <span style="font-size:13px;">矩阵 A = </span>
  <input type="number" id="m00" value="1" step="0.1" style="width:60px;padding:4px;border:1px solid var(--border);border-radius:4px;text-align:center;font-size:13px;background:var(--bg-input);color:var(--text-primary);" onchange="updateTransform()">
  <input type="number" id="m01" value="0" step="0.1" style="width:60px;padding:4px;border:1px solid var(--border);border-radius:4px;text-align:center;font-size:13px;background:var(--bg-input);color:var(--text-primary);" onchange="updateTransform()">
  <br>
  <input type="number" id="m10" value="0" step="0.1" style="width:60px;padding:4px;border:1px solid var(--border);border-radius:4px;text-align:center;font-size:13px;background:var(--bg-input);color:var(--text-primary);" onchange="updateTransform()">
  <input type="number" id="m11" value="1" step="0.1" style="width:60px;padding:4px;border:1px solid var(--border);border-radius:4px;text-align:center;font-size:13px;background:var(--bg-input);color:var(--text-primary);" onchange="updateTransform()">
  <span style="font-size:13px;color:var(--text-muted);margin-left:8px;">det(A) = <span id="detVal">1.00</span></span>
  <button class="btn btn-sm" onclick="resetTransform()">重置</button>
</div>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin:8px 0;">
  <button class="btn btn-sm" onclick="presetTransform(1,0,0,1)">单位矩阵</button>
  <button class="btn btn-sm" onclick="presetTransform(2,0,0,1)">水平拉伸</button>
  <button class="btn btn-sm" onclick="presetTransform(0,-1,1,0)">旋转90°</button>
  <button class="btn btn-sm" onclick="presetTransform(1,1,0,1)">剪切</button>
  <button class="btn btn-sm" onclick="presetTransform(0,0,0,0)">零矩阵</button>
  <button class="btn btn-sm" onclick="presetTransform(-1,0,0,1)">镜像</button>
</div>

<script>
function updateTransform() {
  var a=parseFloat(document.getElementById('m00').value)||0;
  var b=parseFloat(document.getElementById('m01').value)||0;
  var c=parseFloat(document.getElementById('m10').value)||0;
  var d=parseFloat(document.getElementById('m11').value)||0;
  document.getElementById('detVal').textContent = (a*d-b*c).toFixed(2);
  drawTransform(a,b,c,d);
}
function presetTransform(a,b,c,d) {
  document.getElementById('m00').value=a; document.getElementById('m01').value=b;
  document.getElementById('m10').value=c; document.getElementById('m11').value=d;
  updateTransform();
}
function resetTransform(){ presetTransform(1,0,0,1); }
function drawTransform(a,b,c,d) {
  var N=11; var xs=[],ys=[],us=[],vs=[];
  for(var i=0;i<N;i++){for(var j=0;j<N;j++){
    var x=-1+2*i/(N-1), y=-1+2*j/(N-1);
    xs.push(x); ys.push(y); us.push(a*x+b*y-x); vs.push(c*x+d*y-y);
  }}
  // Grid lines
  var gridX=[],gridY=[];
  for(var k=0;k<N;k++){
    var t=-1+2*k/(N-1);
    gridX.push(a*t+b*(-1),a*t+b*1); gridY.push(c*t+d*(-1),c*t+d*1);
    gridX.push(a*(-1)+b*t,a*1+b*t); gridY.push(c*(-1)+d*t,c*1+d*t);
  }
  var layout={title:'线性变换: Ax',xaxis:{range:[-3,3]},yaxis:{range:[-3,3],scaleanchor:'x'},
    margin:{t:40,r:20,b:40,l:40},paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',showlegend:false};
  Plotly.react('linTransform',[
    {x:xs,y:ys,type:'scatter',mode:'markers',marker:{size:3,color:'#4a6a8a'},name:'grid'},
    {x:us.map(function(_,i){return [xs[i],xs[i]+us[i]*0.8,null]}).flat(),
     y:us.map(function(_,i){return [ys[i],ys[i]+vs[i]*0.8,null]}).flat(),
     type:'scatter',mode:'lines',line:{color:'#a45050',width:1.5},hoverinfo:'none'},
    {x:[0,a],y:[0,c],type:'scatter',mode:'lines+markers',line:{color:'#4a6a8a',width:3},marker:{size:8,color:'#4a6a8a'},name:'e1'},
    {x:[0,b],y:[0,d],type:'scatter',mode:'lines+markers',line:{color:'#6b5e4a',width:3},marker:{size:8,color:'#6b5e4a'},name:'e2'}
  ],layout,{responsive:true});
}
if(window.Plotly) setTimeout(function(){ updateTransform(); },500);
else { var chk=setInterval(function(){ if(window.Plotly){clearInterval(chk);updateTransform();} },200); }
</script>
