# 矩阵 — 空间的变形器

四个数字组成的矩阵，凭什么能描述旋转、拉伸、剪切——所有空间变换？因为**矩阵乘法就是空间变形**：$A$ 作用在 $\mathbf{x}$ 上，把整个坐标网格拉来拉去。理解矩阵的关键，是看它把基向量挪到了哪里。

## 矩阵乘法 = 空间变换

$$A\mathbf{x} = \mathbf{y}, \qquad \begin{bmatrix}a & b \\ c & d\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}ax+by \\ cx+dy\end{bmatrix}$$

在「3Blue1Brown」式的理解里：矩阵 $A$ 把基向量 $\mathbf{i}=(1,0)$ 挪到 $A\mathbf{i}=(a,c)$，把 $\mathbf{j}=(0,1)$ 挪到 $A\mathbf{j}=(b,d)$，其余向量跟着网格一起被搬走。**看矩阵，就是看基向量飞到了哪**。

## 三种基本变形

| 变换 | 矩阵 | 效果 |
|------|------|------|
| **旋转** | $\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$ | 绕原点转 $\theta$ |
| **缩放** | $\begin{bmatrix}s_x & 0 \\ 0 & s_y\end{bmatrix}$ | 沿轴拉伸 |
| **剪切** | $\begin{bmatrix}1 & k \\ 0 & 1\end{bmatrix}$ | 平行滑动 |

## 行列式：变形改变了多少面积

> $$\det(A) = ad - bc$$

行列式衡量 $A$ 把单位正方形变成的**平行四边形的面积**。它回答：这场变形是「放大了空间」还是「压扁了空间」？

- $\det(A) = 0$：变换把平面压成一条线（**降维**，信息丢失）
- $\det(A) > 0$：保持方向
- $\det(A) < 0$：翻转方向

行列式为 0 ⟺ 矩阵不可逆——这场变形不可逆转，有些信息找不回来了。

## 矩阵乘法与逆矩阵

- **复合**：$AB$ 表示「先做 $B$ 变换，再做 $A$ 变换」——但 $AB \neq BA$，顺序不能换
- **逆矩阵** $A^{-1}$：把 $A$ 的变形「还原」，$A^{-1}A = I$。$A$ 可逆 ⟺ $\det(A) \neq 0$
- **矩阵的秩** = 变换后空间的维数：满秩（$n$）保持维数，缺秩降维

---

**从这里出发**：[应用案例](#applications) 看矩阵如何驱动 3D 图形、压缩图像；[探索](#explore) 亲手拖动 2×2 矩阵的参数，看整个网格在屏幕上变形。

→ [继续阅读：特征值 — 不变的方向](/exhibit/eigenvalue)
