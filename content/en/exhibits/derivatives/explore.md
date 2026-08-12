## Explore Derivatives

### Try It 1: Which Way Is Up?

You're on a hill with height function h(x) = -x² + 4x (x is horizontal position). You're at x = 1. Which direction gives the steepest climb?

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="Parabola h=-x²+4x with a positively-sloped tangent at x=1 pointing uphill" style="margin:12px 0;display:block;">
  <g transform="translate(20,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="60" y1="0" x2="60" y2="170" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,78 C 15,88 30,108 45,138 M 60,150 L 65,142 L 75,122 C 90,92 105,72 120,58 C 135,48 150,42 165,38 L 180,35" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <line x1="0" y1="48" x2="90" y2="228" stroke="var(--accent-error)" stroke-width="2" />
    <circle cx="45" cy="138" r="4.5" fill="var(--accent-error)" />
    <text x="38" y="128" font-size="11" fill="var(--accent-error)">x=1</text>
    <text x="96" y="180" font-size="11" fill="var(--accent-error)">go right, uphill ↑</text>
    <text x="120" y="24" font-size="11" fill="var(--accent)">h(x)=-x²+4x</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
h'(x) = -2x + 4. At x = 1, h'(1) = 2 > 0, so moving forward (increasing x) goes uphill. Positive derivative → function is increasing.
</details>

### Try It 2: When Does It Stop?

A car's displacement s(t) = t³ - 6t² + 9t. When does it come to a stop (velocity = 0)?

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="Cubic s=t³-6t²+9t with horizontal tangents at t=1 and t=3 (velocity zero)" style="margin:12px 0;display:block;">
  <g transform="translate(20,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="60" y1="0" x2="60" y2="170" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,150 C 25,140 50,100 62,96 C 75,92 90,120 105,130 C 120,138 140,145 165,152 L 175,154" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <line x1="40" y1="96" x2="85" y2="96" stroke="var(--accent-error)" stroke-width="2" />
    <line x1="90" y1="130" x2="120" y2="130" stroke="var(--accent-error)" stroke-width="2" />
    <circle cx="62" cy="96" r="4.5" fill="var(--accent-error)" />
    <circle cx="105" cy="130" r="4.5" fill="var(--accent-error)" />
    <text x="55" y="86" font-size="11" fill="var(--accent-error)">t=1</text>
    <text x="108" y="122" font-size="11" fill="var(--accent-error)">t=3</text>
    <text x="140" y="30" font-size="11" fill="var(--accent)">s(t)=t³-6t²+9t</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
v(t) = s'(t) = 3t² - 12t + 9 = 3(t² - 4t + 3) = 3(t-1)(t-3). Velocity is 0 at t = 1 and t = 3.
Notice: around t = 1, velocity goes from positive to positive (a pause); around t = 3, velocity goes from negative to positive (a U-turn).
</details>

### Try It 3: Guess the Rate

What's the derivative of f(x) = x³ at x = 2? (Guess intuitively before using the formula.)

<details>
<summary>Answer</summary>
f'(x) = 3x², so f'(2) = 12.
Intuition check: f(2) = 8, f(2.01) ≈ (2.01)³ ≈ 8.1206, an increase of ~0.1206. Rate ≈ 0.1206/0.01 = 12.06 ≈ 12.
</details>

### Try It 4: The Mean Value Theorem

You drive 120 km from A to B in 1 hour. Was there a moment when your instantaneous speed was exactly 120 km/h?

<details>
<summary>Answer</summary>
Yes! The Mean Value Theorem: if s(t) is continuous and differentiable, then there exists some c such that s'(c) = (s(1)-s(0))/(1-0) = 120/1 = 120.
At least one instant, your speed exactly equals your average speed. This is the math behind speeding tickets.
</details>
