## 破局心法：解同余问题的工具箱

### 1. 先学会"折叠"：模运算四则

- 加减乘都可"先取模再算"：$(a+b)\bmod m=((a\bmod m)+(b\bmod m))\bmod m$——**永远让数字保持小**
- 负数也在环里：$-1\equiv m-1\pmod m$
- 除法铁律：从 $ac\equiv bc\pmod m$ 推 $a\equiv b$，必须 $\gcd(c,m)=1$

### 2. 解线性同余方程 $ax\equiv b\pmod m$

记 $d=\gcd(a,m)$：有解 $\iff d\mid b$。约简：两边与模数同除 $d$，得 $a'x\equiv b'\pmod{m'}$（互素），再求逆：$x\equiv a'^{-1}b'\pmod{m'}$；解的个数恰为 $d$。

例：$3x\equiv4\pmod7$，$3^{-1}\equiv5$，故 $x\equiv6$ ✓。再例：$4x\equiv8\pmod{12}$，$d=4\mid8$，约简 $x\equiv2\pmod3$，得 4 个解 $2,5,8,11$。

### 3. 求模逆元三武器

- **扩展欧几里得**：解 $ax+my=1$，$x$ 即逆元
- **费马小定理**（$p$ 素数）：$a^{-1}\equiv a^{p-2}\pmod p$
- **欧拉定理**（$\gcd(a,n)=1$）：$a^{-1}\equiv a^{\varphi(n)-1}\pmod n$

例：$13=2\times5+3$，$5=3+2$，$3=2+1$，回代得 $1=2\times13-5\times5$，故 $5^{-1}\equiv8\pmod{13}$ ✓。

### 4. 中国剩余定理：化整为零

$m_1,m_2$ 互素时，$x\equiv a_1\pmod{m_1}$、$x\equiv a_2\pmod{m_2}$ 有唯一解模 $m_1m_2$：

$$x\equiv a_1M_1M_1^{-1}+a_2M_2M_2^{-1}\pmod M, \qquad M=m_1m_2$$

其中 $M_i=M/m_i$，$M_i^{-1}$ 为其模 $m_i$ 的逆元。思想：拆成小问题再拼回。例：$x\equiv2\pmod3$、$x\equiv3\pmod5$：$5^{-1}\equiv2\pmod3$、$3^{-1}\equiv2\pmod5$，故 $x\equiv8\pmod{15}$ ✓。

### 5. 快速幂取模：平方-乘算法

把指数写成二进制，反复平方、按需相乘，每步取模，复杂度仅 $O(\log e)$。例：$3^{13}\bmod7$，$13=1101_2$，故 $3^{13}=3^8\cdot3^4\cdot3^1\equiv2\cdot4\cdot3=24\equiv3\pmod7$ ✓。

### 常见陷阱

1. 不查有解性：$\gcd(a,m)\nmid b$ 时无解
2. 约分不查互质：$ac\equiv bc$ 直接约 $c$，$\gcd(c,m)>1$ 时错
3. 费马小定理滥用：$p$ 必须素数且 $p\nmid a$
4. CRT 忘互素：不互素时先拆成素数幂
5. 快速幂不取模：中间数字变大等于白算
