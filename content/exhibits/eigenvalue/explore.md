## 探索：特征值的直觉实验室

### 试试看 1：对角矩阵的特征值

矩阵 $A = \begin{bmatrix}2 & 0 \\ 0 & 3\end{bmatrix}$。它的特征值和特征向量是什么？

<details>
<summary>答案</summary>
特征值就是对角线元素：$\lambda_1 = 2$，$\lambda_2 = 3$。对应特征向量 $(1,0)$（被放大 2 倍，方向不变）和 $(0,1)$（被放大 3 倍）。对角矩阵的特征值一眼就能读出来。
</details>

### 试试看 2：验证特征值

验证 $\lambda = 5$ 是矩阵 $A = \begin{bmatrix}4 & 1 \\ 2 & 3\end{bmatrix}$ 的一个特征值。

<details>
<summary>答案</summary>
算特征多项式 $|A - \lambda I| = \begin{vmatrix}4-\lambda & 1 \\ 2 & 3-\lambda\end{vmatrix} = (4-\lambda)(3-\lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda-5)(\lambda-2)$。所以特征值是 5 和 2。验证：$\det(A) = 12-2=10 = 5\times 2$ ✓，$\text{tr}(A) = 7 = 5+2$ ✓。
</details>

### 试试看 3：旋转矩阵的特征值

矩阵 $R = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}$（旋转 90°）的特征值是什么？

<details>
<summary>答案</summary>
$|R - \lambda I| = \lambda^2 + 1 = 0$，所以 $\lambda = \pm i$——纯虚数！旋转 90° 没有「方向不变」的实向量（任何向量都转了 90°），所以特征值是复数 $e^{\pm i\pi/2}$。这揭示了旋转的「本质」藏在复数世界里。
</details>

### 试试看 4：幂的收敛

矩阵 $A = \begin{bmatrix}0.5 & 0 \\ 0 & 0.9\end{bmatrix}$。迭代 $A^n$ 多次后，会怎样？

<details>
<summary>答案</summary>
$A^n = \begin{bmatrix}0.5^n & 0 \\ 0 & 0.9^n\end{bmatrix}$。两个特征值都 < 1，所以 $A^n \to 0$——系统收敛。特征值都小于 1 ⟺ 系统稳定衰减。这就是「特征值决定动力系统长期行为」的直观体现。
</details>
