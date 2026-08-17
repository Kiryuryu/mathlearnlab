## 探索：向量的直觉实验室

### 试试看 1：向量的线性组合

给定向量 $\mathbf{u} = (1, 2)$ 和 $\mathbf{v} = (3, 1)$，写出组合 $2\mathbf{u} - \mathbf{v}$。它的坐标是什么？

<details>
<summary>答案</summary>
$2\mathbf{u} - \mathbf{v} = (2, 4) - (3, 1) = (-1, 3)$。几何上：先沿 $\mathbf{u}$ 方向走两倍，再沿 $\mathbf{v}$ 的反方向走一步——这就是线性组合的「拼图」过程。
</details>

### 试试看 2：判断线性无关

三个向量：$\mathbf{u} = (1, 0)$，$\mathbf{v} = (0, 1)$，$\mathbf{w} = (1, 1)$。它们线性无关吗？能张成二维空间吗？

<details>
<summary>答案</summary>
$\mathbf{w} = \mathbf{u} + \mathbf{v}$，所以三个向量线性相关（$\mathbf{w}$ 是前两个的组合）。但它们仍能张成整个二维空间（只用 $\mathbf{u}, \mathbf{v}$ 就够了）。线性无关 = 没有冗余；张成 = 覆盖范围够大。两个性质独立。
</details>

### 试试看 3：内积与夹角

计算 $\mathbf{u} = (1, 0)$ 和 $\mathbf{v} = (0, 1)$ 的内积。它们正交吗？

<details>
<summary>答案</summary>
$\mathbf{u}\cdot\mathbf{v} = 1\times 0 + 0\times 1 = 0$。内积为 0 ⟺ 正交 ⟺ 夹角 90°。这里 $\mathbf{u}$ 沿 x 轴、$\mathbf{v}$ 沿 y 轴，当然垂直。
</details>

### 试试看 4：向量的投影

把向量 $\mathbf{v} = (2, 3)$ 投影到 $\mathbf{u} = (1, 0)$ 上，投影向量是什么？

<details>
<summary>答案</summary>
$\text{proj}_u(v) = \frac{v\cdot u}{u\cdot u}u = \frac{2\times 1 + 3\times 0}{1^2 + 0^2}(1, 0) = 2(1, 0) = (2, 0)$。投影把 $\mathbf{v}$ 分解成「沿 $\mathbf{u}$ 的分量 $(2,0)$」和「垂直分量 $(0,3)$」——这是最小二乘的基础。
</details>
