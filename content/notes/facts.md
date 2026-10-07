# Facts to know cold

Nothing here is given in the test. Each item should come back in under five seconds.

## Algebra

- $ax^2 + bx + c = 0$: $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$. Discriminant $\Delta = b^2 - 4ac$: two distinct real roots if $\Delta > 0$, one repeated root if $\Delta = 0$, none if $\Delta < 0$.
- Sum and product of roots: $\alpha + \beta = -\dfrac{b}{a}$, $\alpha\beta = \dfrac{c}{a}$. Also $\alpha^2 + \beta^2 = (\alpha+\beta)^2 - 2\alpha\beta$.
- Completing the square: $x^2 + bx + c = \left(x + \tfrac b2\right)^2 + c - \tfrac{b^2}{4}$.
- Factor theorem: $(x - a)$ is a factor of $p(x)$ exactly when $p(a) = 0$. The remainder on division by $(x - a)$ is $p(a)$.
- Indices: $a^m a^n = a^{m+n}$, $(a^m)^n = a^{mn}$, $a^{-n} = \dfrac1{a^n}$, $a^{m/n} = \left(\sqrt[n]{a}\right)^m$.
- Surds: $\dfrac{1}{\sqrt a + \sqrt b} = \dfrac{\sqrt a - \sqrt b}{a - b}$.
- $a^2 - b^2 = (a-b)(a+b)$, $a^3 - b^3 = (a-b)(a^2 + ab + b^2)$, $a^3 + b^3 = (a+b)(a^2 - ab + b^2)$.

## Exponentials and logarithms

- $\log_a x = y \iff a^y = x$ (with $a > 0$, $a \ne 1$, $x > 0$).
- $\log(xy) = \log x + \log y$, $\log\dfrac{x}{y} = \log x - \log y$, $\log x^k = k\log x$.
- Special cases: $\log_a \dfrac1x = -\log_a x$ and $\log_a a = 1$.
- The 2026 specification says no question will need the change of base formula. Work with one base at a time.
- $\log_a x$ is increasing if $a > 1$ and decreasing if $0 < a < 1$. That matters when you "take logs" of an inequality.

## Sequences and series

- Arithmetic: $u_n = a + (n-1)d$, $S_n = \dfrac n2\bigl(2a + (n-1)d\bigr) = \dfrac n2(a + l)$.
- Geometric: $u_n = ar^{n-1}$, $S_n = \dfrac{a(1 - r^n)}{1 - r}$, and $S_\infty = \dfrac{a}{1-r}$ only when $|r| < 1$.
- $\displaystyle\sum_{r=1}^n r = \frac{n(n+1)}2$.
- Binomial: $(a + b)^n = \sum_{k=0}^{n} \binom nk a^{n-k}b^k$, where $\binom nk = \dfrac{n!}{k!(n-k)!}$. The coefficients sum to $2^n$.

## Coordinate geometry

- Gradient $m = \dfrac{y_2 - y_1}{x_2 - x_1}$. Line: $y - y_1 = m(x - x_1)$. Perpendicular gradients satisfy $m_1m_2 = -1$.
- Distance $\sqrt{(x_2-x_1)^2 + (y_2 - y_1)^2}$, midpoint $\left(\tfrac{x_1+x_2}2, \tfrac{y_1+y_2}2\right)$.
- Circle: $(x-a)^2 + (y-b)^2 = r^2$. The tangent is perpendicular to the radius. A line is tangent when the distance from the centre equals $r$, or when substituting gives $\Delta = 0$.
- Distance from $(x_0, y_0)$ to $ax + by + c = 0$ is $\dfrac{|ax_0 + by_0 + c|}{\sqrt{a^2+b^2}}$.

## Trigonometry

| | $0$ | $\tfrac\pi6$ | $\tfrac\pi4$ | $\tfrac\pi3$ | $\tfrac\pi2$ |
|---|---|---|---|---|---|
| $\sin$ | $0$ | $\tfrac12$ | $\tfrac{\sqrt2}2$ | $\tfrac{\sqrt3}2$ | $1$ |
| $\cos$ | $1$ | $\tfrac{\sqrt3}2$ | $\tfrac{\sqrt2}2$ | $\tfrac12$ | $0$ |
| $\tan$ | $0$ | $\tfrac{1}{\sqrt3}$ | $1$ | $\sqrt3$ | undefined |

- $\sin^2 x + \cos^2 x = 1$, $\tan x = \dfrac{\sin x}{\cos x}$.
- $\sin(180^\circ - x) = \sin x$, $\cos(180^\circ - x) = -\cos x$, $\cos(-x) = \cos x$, $\sin(-x) = -\sin x$.
- Sine rule $\dfrac{a}{\sin A} = \dfrac{b}{\sin B}$. Cosine rule $a^2 = b^2 + c^2 - 2bc\cos A$. Area $\tfrac12 ab\sin C$.
- Radians: $\pi = 180^\circ$. Arc length $r\theta$, sector area $\tfrac12 r^2\theta$.
- Periods: $\sin kx$ and $\cos kx$ have period $\dfrac{2\pi}{k}$; $\tan x$ has period $\pi$.

## Calculus

- $\dfrac{d}{dx}x^n = nx^{n-1}$ for any real $n$. $\displaystyle\int x^n\,dx = \frac{x^{n+1}}{n+1} + c$ for $n \ne -1$.
- Tangent at $x = a$: $y - f(a) = f'(a)(x - a)$. The normal has gradient $-1/f'(a)$.
- Stationary points: $f'(x) = 0$. If $f''(x) > 0$ it's a minimum, if $f''(x) < 0$ a maximum; if $f'' = 0$, check the sign of $f'$ either side.
- $\int_a^b f(x)\,dx$ is **signed** area: regions below the axis count negatively.
- Fundamental Theorem: $\int_a^b f(x)\,dx = F(b) - F(a)$ where $F' = f$, and $\dfrac{d}{dx}\int_a^x f(t)\,dt = f(x)$.
- Combining: $\int_a^b f + \int_a^b g = \int_a^b (f+g)$, and $\int_a^b f + \int_b^c f = \int_a^c f$ (also when $c < b$). Swapping limits changes the sign.
- $\dfrac{dy}{dx} = f(x)$: integrate, then use the given point to find the constant.
- Area between $y = a(x-p)(x-q)$ and the $x$-axis: $\dfrac{|a|(q-p)^3}6$.
- Trapezium rule: overestimates when the curve is convex (bends up), underestimates when concave.
- Stationary points in the TMUA are maxima and minima; points of inflexion are not examined.

## Geometry

- Interior angles of an $n$-gon sum to $(n-2)\times 180^\circ$. Exterior angles sum to $360^\circ$.
- Similar shapes with length scale factor $k$: areas scale by $k^2$, volumes by $k^3$.
- Know cold: circle $C = 2\pi r$, $A = \pi r^2$; cylinder $V = \pi r^2 h$; prisms $V = \text{cross-section}\times\text{length}$. Sphere, cone and pyramid formulae are given in the question when needed (sphere $V = \tfrac43\pi r^3$, $A = 4\pi r^2$; cone $V = \tfrac13\pi r^2h$, curved area $\pi r l$; pyramid $V = \tfrac13\times\text{base}\times h$).
- Sector area $\tfrac12 r^2\theta$; segment area $\tfrac12 r^2(\theta - \sin\theta)$ (radians).
- Vectors: $\overrightarrow{AB} = \mathbf{b} - \mathbf{a}$; the point dividing $AB$ in ratio $m:n$ is $\dfrac{n\mathbf{a} + m\mathbf{b}}{m+n}$; parallel vectors are scalar multiples.
- Circle theorems: the angle at the centre is twice the angle at the circumference; the angle in a semicircle is $90^\circ$; angles in the same segment are equal; opposite angles of a cyclic quadrilateral sum to $180^\circ$; tangent ⟂ radius; the two tangents from a point are equal in length; alternate segment theorem.

## Number and data

- Recurring decimals: $0.\dot{a}\dot{b} = \dfrac{ab}{99}$; in general, multiply by a power of 10 and subtract.
- Bounds: a value given as 6.4 to 1 d.p. lies in $6.35 \le x < 6.45$. For a quotient, the upper bound is upper ÷ lower.
- Direct proportion $y = kx^n$; inverse proportion $y = k/x^n$.
- Frequency density = frequency ÷ class width; in a histogram, area represents frequency.
- Median and quartiles of $n$ ordered values sit at positions $\tfrac{n+1}{2}$, $\tfrac{n+1}{4}$ and $\tfrac{3(n+1)}{4}$. IQR = UQ − LQ.

## Probability and counting

- $P(A \cup B) = P(A) + P(B) - P(A \cap B)$. Independent: $P(A \cap B) = P(A)P(B)$.
- $P(\text{at least one}) = 1 - P(\text{none})$.
- Arrangements of $n$ objects with repeats $k_1, k_2, \ldots$: $\dfrac{n!}{k_1!\,k_2!\cdots}$. Choosing $r$ from $n$: $\binom nr$.

## Logic (the test uses words, never symbols)

- "If A then B" is false only when A is true and B is false.
- Its **contrapositive**, "if not B then not A", is equivalent to it. Its **converse**, "if B then A", is not.
- "A only if B" means "if A then B". "A if B" means "if B then A". "A if and only if B" means both.
- "A is sufficient for B" means "if A then B". "A is necessary for B" means "if B then A".
- "Or" is inclusive: "A or B" allows both.
- Not (for all $x$, P) = there exists an $x$ for which not P. Not (there exists $x$ with P) = for all $x$, not P.
- Not (A and B) = (not A) or (not B). Not (A or B) = (not A) and (not B). Not (if A then B) = A and not B.
- "For some" means "for at least one".
