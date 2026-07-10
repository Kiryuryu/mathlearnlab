# 解题集 — 高等数学

> 📐 按题型分类，含详细解答（可折叠）

## 第一章：极限与连续

### 题型一：求极限

**1. 求 $\lim_{x\to 0}\frac{\tan x - \sin x}{x^3}$**

<details>
<summary>点击查看解答</summary>

**解**：用泰勒展开。
- $\tan x = x + \frac{x^3}{3} + O(x^5)$
- $\sin x = x - \frac{x^3}{6} + O(x^5)$
- $\tan x - \sin x = \frac{x^3}{3} + \frac{x^3}{6} + O(x^5) = \frac{x^3}{2} + O(x^5)$

故 $\lim_{x\to 0}\frac{\tan x - \sin x}{x^3} = \frac{1}{2}$

> 💡 注意：泰勒展开是求极限的最强工具，比反复使用洛必达更高效。
</details>

---

**2. 求 $\lim_{x\to 0}(1+x^2)^{1/(x\sin x)}$**

<details>
<summary>点击查看解答</summary>

**解**：$1^\infty$ 型，用重要极限。

$\lim_{x\to 0}(1+x^2)^{\frac{1}{x\sin x}} = \exp\left(\lim_{x\to 0}\frac{x^2}{x\sin x}\right) = \exp\left(\lim_{x\to 0}\frac{x}{\sin x}\right) = e^1 = e$

> 💡 $1^\infty$ 型的标准处理：$\lim f^g = \exp(\lim g(f-1))$（当 $f\to 1$）
</details>

---

### 题型二：无穷小比较

> 🚧 待添加

### 题型三：间断点与连续性

> 🚧 待添加

---

## 第二章：微分学

> 🚧 待添加

## 第三章：积分学

> 🚧 待添加

## 更多章节

> 🚧 待添加
