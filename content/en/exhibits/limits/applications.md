## Applications of Limits

### 1. Computing π

Ancient geometers used the method of exhaustion (polygons approximating a circle) — a limit in spirit:

- Liu Hui used a 3072-sided polygon to get π ≈ 3.1416
- Zu Chongzhi pushed to 12288 sides, obtaining π ≈ 3.1415926

Modern formulas for π are all limits:

$$\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$$

$$\frac{1}{\pi} = \frac{\sqrt{8}}{9801} \sum_{n=0}^\infty \frac{(4n)!(1103+26390n)}{(n!)^4 \cdot 396^{4n}}$$

Computers rely on these limit formulas to calculate π to trillions of digits.

### 2. Instantaneous Velocity

Your car's speedometer reads 60 km/h — not "60 km in the past hour," but the limit as the time interval approaches zero:

$$v(t) = \lim_{\Delta t \to 0} \frac{s(t+\Delta t) - s(t)}{\Delta t}$$

Flight control systems perform thousands of such limit calculations every second.

### 3. Continuous Compounding

"5% annual interest, compounded continuously" means money earns interest at every instant:

$$A = P \lim_{n \to \infty} \left(1 + \frac{0.05}{n}\right)^{n} = P e^{0.05}$$

This is why e exists — it's the limit of continuous growth.

### 4. Image Denoising

Digital photos taken in low light contain noise. Denoising algorithms take weighted averages over neighboring pixels — as more pixels are included, the result approaches the true clean value. A limit process.

### 5. PageRank — Google's Origin

Google's original PageRank algorithm iteratively computes: each page's importance = weighted sum of pages linking to it. After infinitely many iterations, the weight vector converges to a steady state — the mathematical foundation of search engine ranking.
