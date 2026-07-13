## 多元微积分的数学之美

### 格林公式

$$\oint_C P\,dx + Q\,dy = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) dx\,dy$$

平面上沿闭合曲线的积分 = 内部区域的二重积分。一个边界和内部之间的对偶关系——"看外面就知道里面"。

### 斯托克斯公式

$$\oint_C \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F})\cdot d\mathbf{S}$$

空间曲面上沿边界曲线的环量 = 曲面上旋度的通量。格林公式和高斯公式都是它的特例——三个公式实际上是一个公式在不同维度下的表现。

### 散度定理（高斯公式）

$$\iiint_V \nabla\cdot\mathbf{F}\,dV = \oiint_S \mathbf{F}\cdot d\mathbf{S}$$

一个体积内源的"总量"等于通过其表面的通量。这解释了为什么热从热源向外扩散、为什么电流在导体中流动。

### 鞍点与马鞍面

z = x² - y² 是一个马鞍面。在原点，x 方向是上凸的，y 方向是下凸的。二阶导数 fxx·fyy - fxy² < 0 判定这个点是鞍点——不是极大也不是极小。这就像一个山口：南北方向是上坡，东西方向是下坡。

### Hairy Ball Theorem

用多元微积分可以证明：你无法在一个球面上为每一点定义一个连续不消失的切向量场。通俗地说——你无法完美地梳平一个覆盖球面的毛球，总有两个"旋"（极点处）。这和拓扑学的欧拉示性数有关。
