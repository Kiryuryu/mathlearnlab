## Applications of Congruence

Congruence sounds abstract, yet it works in your pocket every day: ISBNs, national ID numbers, bank cards, "enter the code" prompts… all of them do the same thing — **only the remainder matters**.

### 1. Calendars and Weekdays: The Mod-7 Timeline

A weekday is, at heart, "modulo 7". If January 1, 2024 is a Monday, what day is 100 days later? Since $100\equiv2\pmod7$, it is a Wednesday. 2024 is a leap year, and $366\equiv2\pmod7$, so New Year's Day 2025 is also a Wednesday.

- **Leap-year rule**: divisible by 4 but not by 100, or divisible by 400
- **Zeller's congruence**: one congruence computes the weekday of any date

### 2. ISBN and ID Numbers: The Remainder as a Fingerprint

How is a single mistyped digit caught instantly? Through the **check digit** — a "remainder function" of the preceding digits.

- **ISBN-13**: sum the first 12 digits weighted by $1,3,1,3,\dots$, and the check digit is $(10-S\bmod10)\bmod10$. For 978-7-302-56645 the weighted sum is $122$, and since $122\equiv2\pmod{10}$, the check digit is 8
- **Chinese national ID** (18 digits): the first 17 digits are weighted and reduced $\bmod11$; the 18th digit comes from a lookup table (it can even be an X). Mistype one digit and the check almost certainly fails
- **Credit cards** use the Luhn algorithm, another mod-10 check

### 3. RSA: Modular Arithmetic Guards the Internet

Choose large primes $p,q$, set $n=pq$, pick $e$ coprime to $\varphi(n)$, then find $d\equiv e^{-1}\pmod{\varphi(n)}$; encrypt $c=m^e\bmod n$, decrypt $m\equiv c^d\pmod n$.

Toy numbers: $p=3,q=11$ give $n=33$, $\varphi(n)=20$; take $e=3$, $d=7$ (since $3\times7\equiv1\pmod{20}$). Encrypt $m=7$: $c=7^3\equiv13\pmod{33}$; decrypt: $13^7\bmod33=7$ — the message comes back! Behind every HTTPS connection and mobile payment, this kind of modular exponentiation is running.

### 4. Pseudorandom Numbers and Hashing

- **Linear congruential generators**: $x_{n+1}=(ax_n+c)\bmod m$. Many old computer "random numbers", lotteries, and game worlds come from this sequence; with good parameters the period can reach $m$
- **Hash tables**: map arbitrary data into "buckets" from $0$ to $m-1$; bucket counts are often prime to reduce collisions

### 5. A World of Cycles

A pitch doubles in frequency every 12 semitones — **music is a mod-12 world**; clocks, stopwatches, weeks, months… a cycle is modular arithmetic.

---

**Behind all of these**: congruence folds the infinite into the finite, letting computers handle huge numbers, letting digits catch their own typos, and letting messages stay secret on public channels — this "folding" is the shared engine from calendars to cryptography.
