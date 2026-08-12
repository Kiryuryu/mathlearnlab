## 探索：复分析的直觉实验室

### 试试看 1：i 的幂循环

计算 $i^0, i^1, i^2, i^3, i^4$，你发现了什么规律？

<details>
<summary>答案</summary>
$i^0 = 1$，$i^1 = i$，$i^2 = -1$，$i^3 = -i$，$i^4 = 1$。之后每 4 次循环一次：$1, i, -1, -i$。几何上，每次乘以 $i$ 就是逆时针旋转 90°——在复平面上绕单位圆转圈。这就是为什么 $i$ 的乘法"就是旋转"。
</details>

### 试试看 2：欧拉公式的取值

用 $e^{i\theta} = \cos\theta + i\sin\theta$ 计算 $e^{i\pi/2}$ 和 $e^{i\pi}$，然后验证 $e^{i\pi} + 1 = 0$。

<details>
<summary>答案</summary>
$e^{i\pi/2} = \cos(\pi/2) + i\sin(\pi/2) = 0 + i\cdot 1 = i$。所以 $e^{i\pi/2} = i$——乘以 $i$ 和 $e^{i\pi/2}$ 是同一件事（旋转 90°）。$e^{i\pi} = \cos\pi + i\sin\pi = -1 + 0i = -1$，于是 $e^{i\pi} + 1 = 0$ ✓。指数函数在复平面上就是"螺旋前进"，在 $\theta=\pi$ 时正好落在 $-1$。
</details>

### 试试看 3：1/(z−1) 的奇点

函数 $f(z) = \frac{1}{z-1}$ 在哪个点不解析？它属于什么类型的奇点？

<details>
<summary>答案</summary>
在 $z=1$ 处分母为零，$f$ 不解析。这是**简单极点**（一阶极点）：洛朗展开 $f(z) = \frac{1}{z-1}$ 中只有一个负幂项，留数 $\mathrm{Res}(f, 1) = \lim_{z\to 1}(z-1)\cdot\frac{1}{z-1} = 1$。所以 $\oint_{|z-1|=r}\frac{dz}{z-1} = 2\pi i \cdot 1 = 2\pi i$——绕极点的积分永远等于 $2\pi i$ 倍留数。
</details>

### 试试看 4：留数定理算实积分

用留数定理求 $\int_{-\infty}^{\infty} \frac{dx}{1+x^2}$。

<details>
<summary>答案</summary>
考虑上半平面围道（实轴 $[-R,R]$ + 上半圆弧）。函数 $f(z)=\frac{1}{1+z^2}=\frac{1}{(z+i)(z-i)}$ 在上半平面只有极点 $z=i$（简单极点）。留数：$\mathrm{Res}(f,i) = \lim_{z\to i}(z-i)\frac{1}{(z-i)(z+i)} = \frac{1}{2i}$。由留数定理，$\oint f = 2\pi i \cdot \frac{1}{2i} = \pi$。令 $R\to\infty$，圆弧部分趋于 0，故 $\int_{-\infty}^{\infty}\frac{dx}{1+x^2} = \pi$ ✓。一个"无穷区间"的实积分，用复平面上的一点（$z=i$）就求出来了。
</details>
