## Interactive: The Intuition Lab of Number Theory

### Try It 1: The Sieve of Eratosthenes

List the integers from 1 to 50. Cross out 1, then start at 2: **each time take the first un-crossed number (it is prime) and cross out all its multiples**. Which numbers below 50 are prime?

<svg width="360" height="210" viewBox="0 0 360 210" role="img" aria-label="Grid of 1 to 50: 1 crossed out, composites gray, primes highlighted (result of the sieve)" style="margin:12px 0;display:block;">
  <g font-size="12" text-anchor="middle" font-family="var(--font-mono)">
    <text x="26" y="34" font-size="12" fill="var(--text-muted)" text-decoration="line-through">1</text>
    <text x="58" y="34" font-weight="700" fill="var(--accent)">2</text><text x="90" y="34" font-weight="700" fill="var(--accent)">3</text>
    <text x="122" y="34" fill="var(--text-muted)">4</text><text x="154" y="34" font-weight="700" fill="var(--accent)">5</text>
    <text x="186" y="34" fill="var(--text-muted)">6</text><text x="218" y="34" font-weight="700" fill="var(--accent)">7</text>
    <text x="250" y="34" fill="var(--text-muted)">8</text><text x="282" y="34" fill="var(--text-muted)">9</text><text x="314" y="34" fill="var(--text-muted)">10</text>
    <text x="26" y="72" fill="var(--text-muted)">11</text><text x="58" y="72" fill="var(--text-muted)">12</text><text x="90" y="72" font-weight="700" fill="var(--accent)">13</text>
    <text x="122" y="72" fill="var(--text-muted)">14</text><text x="154" y="72" fill="var(--text-muted)">15</text><text x="186" y="72" fill="var(--text-muted)">16</text>
    <text x="218" y="72" font-weight="700" fill="var(--accent)">17</text><text x="250" y="72" fill="var(--text-muted)">18</text><text x="282" y="72" font-weight="700" fill="var(--accent)">19</text>
    <text x="314" y="72" fill="var(--text-muted)">20</text>
    <text x="26" y="110" fill="var(--text-muted)">21</text><text x="58" y="110" fill="var(--text-muted)">22</text><text x="90" y="110" font-weight="700" fill="var(--accent)">23</text>
    <text x="122" y="110" fill="var(--text-muted)">24</text><text x="154" y="110" fill="var(--text-muted)">25</text><text x="186" y="110" fill="var(--text-muted)">26</text>
    <text x="218" y="110" fill="var(--text-muted)">27</text><text x="250" y="110" fill="var(--text-muted)">28</text><text x="282" y="110" font-weight="700" fill="var(--accent)">29</text>
    <text x="314" y="110" fill="var(--text-muted)">30</text>
    <text x="26" y="148" fill="var(--text-muted)">31</text><text x="58" y="148" fill="var(--text-muted)">32</text><text x="90" y="148" fill="var(--text-muted)">33</text>
    <text x="122" y="148" fill="var(--text-muted)">34</text><text x="154" y="148" fill="var(--text-muted)">35</text><text x="186" y="148" fill="var(--text-muted)">36</text>
    <text x="218" y="148" font-weight="700" fill="var(--accent)">37</text><text x="250" y="148" fill="var(--text-muted)">38</text><text x="282" y="148" fill="var(--text-muted)">39</text>
    <text x="314" y="148" fill="var(--text-muted)">40</text>
    <text x="26" y="186" font-weight="700" fill="var(--accent)">41</text><text x="58" y="186" fill="var(--text-muted)">42</text><text x="90" y="186" font-weight="700" fill="var(--accent)">43</text>
    <text x="122" y="186" fill="var(--text-muted)">44</text><text x="154" y="186" fill="var(--text-muted)">45</text><text x="186" y="186" fill="var(--text-muted)">46</text>
    <text x="218" y="186" font-weight="700" fill="var(--accent)">47</text><text x="250" y="186" fill="var(--text-muted)">48</text><text x="282" y="186" fill="var(--text-muted)">49</text>
    <text x="314" y="186" fill="var(--text-muted)">50</text>
  </g>
  <text x="180" y="204" text-anchor="middle" font-size="11" fill="var(--text-muted)">highlighted = prime (15 total)</text>
</svg>

<details>
<summary>Answer</summary>
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 — 15 of them. Note: sieving up to $\sqrt{50} \approx 7$ is enough, because any composite has a factor at most its square root. This "crossing out multiples" process is the oldest primality sieve.
</details>

### Try It 2: Modular Inverses via Fermat

Fermat's little theorem says: for prime $p$ with $p \nmid a$, $a^{p-1} \equiv 1 \pmod p$, so $a \cdot a^{p-2} \equiv 1 \pmod p$, i.e. $a^{-1} \equiv a^{p-2} \pmod p$.

**Use this to find the inverse of $3$ modulo $7$.**

<details>
<summary>Answer</summary>
$3^{-1} \equiv 3^{7-2} = 3^5 = 243 \equiv 243 - 34\times 7 = 243 - 238 = 5 \pmod 7$. Check: $3 \times 5 = 15 \equiv 1 \pmod 7$ ✓. So the inverse of $3$ mod $7$ is $5$ — exactly the kind of computation RSA decryption needs.
</details>

### Try It 3: Estimate the Count of Primes

Without counting, use the prime number theorem to estimate: how many primes are less than $10^6$?

<details>
<summary>Answer</summary>
$\pi(10^6) \approx \frac{10^6}{\ln 10^6} = \frac{10^6}{6\ln 10} \approx \frac{10^6}{13.82} \approx 72{,}382$. The true value is 78,498 — off by about 8%. This "right magnitude, imperfect estimate" is exactly what an asymptotic formula means: the larger $x$, the smaller the relative error.
</details>

### Try It 4: Find a Factor of a Big Composite

$n = 143$. Using trial division — check 2, 3, 5, 7, 11… Is it composite? What is its smallest prime factor?

<details>
<summary>Answer</summary>
Trial divide up to $\sqrt{143} \approx 11.9$: 143 is not divisible by 2, 3, or 5, but $143 = 11 \times 13$. So it is composite, with smallest prime factor 11. The key is to test only up to $\sqrt{n}$ — which preserves efficiency and explains why large composites are hard to factor: their factors may lie anywhere on a vast number line.
</details>
