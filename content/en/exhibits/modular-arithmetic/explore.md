## Interactive: The Intuition Lab of Modular Arithmetic

### Try It 1: Powers on a Clock — The Cycle of $a^k \bmod n$

Fix a modulus $n$ and a base $a$, compute $a^1, a^2, a^3, \dots$ reduced mod $n$ in turn, and watch when the sequence starts repeating. First, look at the powers of 3 in the mod-7 world:

<svg width="320" height="240" viewBox="0 0 320 240" role="img" aria-label="The cycle of powers of 3 mod 7: 3→2→6→4→5→1→3" style="margin:12px 0;display:block;">
  <defs>
    <marker id="arrPow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><polygon points="0 0, 9 4.5, 0 9" fill="var(--accent)" /></marker>
  </defs>
  <g stroke="var(--accent)" stroke-width="2" fill="none" marker-end="url(#arrPow)">
    <line x1="177.3" y1="60.1" x2="202.7" y2="74.9" />
    <line x1="220" y1="105" x2="220" y2="135" />
    <line x1="202.7" y1="165.1" x2="177.3" y2="179.9" />
    <line x1="142.6" y1="180" x2="116.4" y2="165" />
    <line x1="99" y1="135" x2="99" y2="105" />
    <line x1="116.4" y1="75" x2="142.6" y2="60" />
  </g>
  <g font-size="11" fill="var(--text-muted)" text-anchor="middle">
    <text x="188" y="58">×3</text>
    <text x="230" y="116">×3</text>
    <text x="197" y="183">×3</text>
    <text x="122" y="183">×3</text>
    <text x="89" y="116">×3</text>
    <text x="122" y="58">×3</text>
  </g>
  <g font-family="var(--font-mono)" font-size="15" font-weight="700" text-anchor="middle">
    <circle cx="160" cy="50" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="160" y="55" fill="var(--text-primary)">3</text>
    <circle cx="220" cy="85" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="220" y="90" fill="var(--text-primary)">2</text>
    <circle cx="220" cy="155" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="220" y="160" fill="var(--text-primary)">6</text>
    <circle cx="160" cy="190" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="160" y="195" fill="var(--text-primary)">4</text>
    <circle cx="99" cy="155" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="99" y="160" fill="var(--text-primary)">5</text>
    <circle cx="99" cy="85" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="99" y="90" fill="var(--text-primary)">1</text>
  </g>
  <text x="160" y="228" text-anchor="middle" font-size="11" fill="var(--text-muted)">Each step multiplies by 3 (mod 7): 3→2→6→4→5→1→3</text>
</svg>

The sequence is $3, 2, 6, 4, 5, 1, 3, \dots$ — **period 6**: it visits every nonzero remainder and returns to the start.

**Now try it yourself:**

1. $n = 5, a = 2$: what is the sequence? What is its period?
2. $n = 8, a = 2$: what happens to the sequence? Why?
3. Under what conditions does the sequence visit every nonzero remainder?

<details>
<summary>Answers</summary>
1. $2, 4, 3, 1, 2, \dots$, period 4 — it visits all nonzero remainders; 2 is a primitive root mod 5.<br>
2. $2, 4, 0, 0, 0, \dots$ — once it hits 0 it is stuck forever. Because $\gcd(2, 8) = 2 > 1$, the factors of 8 eventually "swallow" the powers of 2: once $2^k$ is divisible by 8 ($k \ge 3$), the remainder is 0 forever.<br>
3. You need $\gcd(a, n) = 1$ (to avoid collapsing), and $a$ must be a **primitive root** of $n$; for prime $n$, a primitive root always exists. Mod 7, 3 is a primitive root, 2 is not.
</details>

### Try It 2: Be a "Master Sun" — The Unknown Number of Things

Solve the system of congruences: $x \equiv 2 \pmod 3$, $x \equiv 3 \pmod 5$, $x \equiv 2 \pmod 7$. Use the Chinese remainder theorem (see [Key Insights](#method)) or patient enumeration to find the smallest positive solution.

<details>
<summary>Answer</summary>
$x = 23$. Check: $23 \bmod 3 = 2$ ✓, $23 \bmod 5 = 3$ ✓, $23 \bmod 7 = 2$ ✓. This is the classic answer to the "unknown number of things" problem in the *Sunzi Suanjing*. Using CRT: merge the first two congruences to get $x \equiv 8 \pmod{15}$, then merge with $x \equiv 2 \pmod 7$ to obtain $x \equiv 23 \pmod{105}$ — the smallest positive solution is 23.
</details>

### Try It 3: Fast Exponentiation in Your Head

Using square-and-multiply or Fermat's little theorem, compute mentally: $2^{10} \bmod 13$ and $3^{1000} \bmod 7$.

<details>
<summary>Answer</summary>
$2^{10} = 1024 = 78 \times 13 + 10$, so $2^{10} \equiv 10 \pmod{13}$. For $3^{1000} \bmod 7$: Fermat's little theorem says $3^6 \equiv 1 \pmod 7$, and $1000 = 6 \times 166 + 4$, so $3^{1000} \equiv 3^4 = 81 \equiv 4 \pmod 7$ — divide the exponent by the period first, then take the remainder. That is the power of congruence.
</details>

### Try It 4: Be a Check-Digit Detective

The first 12 digits of an ISBN-13 are `978-7-302-56645`. What is the 13th check digit? Rule: multiply the first 12 digits by alternating weights $1, 3, 1, 3, \dots$, sum to get $S$, then the check digit is $(10 - S \bmod 10) \bmod 10$.

<details>
<summary>Answer</summary>
The weighted sum is $S = 9+21+8+21+3+0+2+15+6+18+4+15 = 122$, so $S \bmod 10 = 2$ and the check digit is $10 - 2 = 8$. The complete number is 978-7-302-56645-8. Now change any single digit and recompute — the check almost certainly fails. A string of digits' "remainder fingerprint" leaves typos nowhere to hide.
</details>

### Think Further

- What other "moduli" surround you? Weeks are mod 7, months mod 12, zodiac signs mod 12, stopwatches mod 60… find a cycle in your daily life and name its modulus
- Draw the cycle of $a^k \bmod n$: what distinguishes sequences with long periods from those that "collapse" to 0? Hint: look at $\gcd(a, n)$
- Why is a clock 12 hours? If humans had 10 fingers, would clock faces have 10 hours? Try designing your own "mod-10 clock"
