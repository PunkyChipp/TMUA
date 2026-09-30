# Integration

TMUA integration is AS-level: integrate powers of $x$, evaluate definite integrals, and find areas. The interesting questions are about what an integral *means*: signed area, what happens under shifts and stretches, what symmetry tells you, and when the trapezium rule over- or underestimates. Many can be done with almost no integration at all if you picture the area.

## Must-know facts

* $\displaystyle\int x^n\,dx = \frac{x^{n+1}}{n+1} + c$ for $n \ne -1$. Rewrite roots and fractions as powers first: $\displaystyle\int \frac{x^2-4}{x^2}\,dx = \int (1 - 4x^{-2})\,dx = x + \frac4x + c$.
* $\displaystyle\int_a^b f(x)\,dx$ is the **signed** area: regions below the $x$-axis count negatively.
* Area between curves: $\displaystyle\int_p^q (\text{top} - \text{bottom})\,dx$. Where the curves cross inside the interval, split.
* Parabola and chord: if $y = x^2 + \dots$ meets a line at $x = p$ and $x = q$, the area between them is $\dfrac{(q-p)^3}{6}$. For leading coefficient $a$, multiply by $|a|$.
* $\dfrac{d}{da}\displaystyle\int_0^a f(x)\,dx = f(a)$.

## Techniques

**Transformations.** Think of the picture:

* $\displaystyle\int_{a+h}^{b+h} f(x - h)\,dx = \int_a^b f(x)\,dx$ (shift the graph, shift the limits).
* $\displaystyle\int_a^b k f(x)\,dx = k\int_a^b f(x)\,dx$ (vertical stretch).
* $\displaystyle\int_a^b \big(f(x) + c\big)\,dx = \int_a^b f(x)\,dx + c(b-a)$: a constant adds a rectangle of width $b - a$.

**Symmetry.**

* $f$ odd ($f(-x) = -f(x)$): $\displaystyle\int_{-a}^a f = 0$.
* $f$ even ($f(-x) = f(x)$): $\displaystyle\int_{-a}^a f = 2\int_0^a f$.
* even $\times$ odd is odd; odd $\times$ odd is even.
* $f(c - x) = f(x)$ means the graph is symmetric in $x = \frac c2$, so the area splits equally either side.

**Unknown limits.** $\displaystyle\int_1^k f(x)\,dx = A$ is an equation in $k$. Check which roots satisfy the conditions given. If a question says "between $x = 1$ and $x = k$", $k$ could be on either side of $1$.

**Trapezium rule.** Each trapezium's top edge is a chord. If the curve is convex ($f'' > 0$, U-shaped) the chords lie above it: **overestimate**. Concave ($f''<0$): **underestimate**. If the concavity changes, no general conclusion; the errors may even cancel.

> **Key idea:** Before integrating, ask whether a sketch plus symmetry gives the answer. Odd parts vanish, shifts move limits, and constants add rectangles.

## Traps

> **Trap:** "Find the area" when the curve crosses the axis. $\int_0^3 (x-1)(x-3)\,dx = 0$, but the area is $\frac83$. Find the roots first and split.

> **Trap:** Two curves crossing three times (e.g. $y=x^3$ and $y=4x$). Integrating top minus bottom across the whole range cancels the two regions.

> **Trap:** $\int f = 3$ says nothing exact about $\int |f|$; only $\int|f| \ge 3$.

* Integrating a constant: $\int_1^4 3\,dx = 9$, not $3$.
* Dividing by a negative new power flips the sign: $\int -4x^{-2}\,dx = +4x^{-1}$.
* Never integrate numerator and denominator separately.
* An integral being $\ge 0$ does not make the integrand $\ge 0$ everywhere, but an integrand $\ge 0$ everywhere does make the integral $\ge 0$.

## Worked examples

**Example 1.** Given $\displaystyle\int_0^2 f(x)\,dx = 3$, find $\displaystyle\int_{-1}^{1} \big(4 - f(x+1)\big)\,dx$.

<details><summary>Show solution</summary>

$y = f(x+1)$ is $y=f(x)$ shifted left by $1$, so $\int_{-1}^1 f(x+1)\,dx = \int_0^2 f(x)\,dx = 3$.

$\int_{-1}^1 4\,dx = 4 \times 2 = 8$.

Answer: $8 - 3 = 5$.

</details>

**Example 2.** Find the area enclosed between $y = x^2$ and $y = 2 - x^2$.

<details><summary>Show solution</summary>

They meet where $x^2 = 2 - x^2$, i.e. $x = \pm 1$. The top curve is $2 - x^2$, so

$$\int_{-1}^1 (2 - 2x^2)\,dx = 2\int_0^1 (2 - 2x^2)\,dx = 2\left(2 - \tfrac23\right) = \tfrac83.$$

Check with the chord formula: $(2 - 2x^2)$ has leading coefficient $-2$ and roots $\pm1$, so area $= 2 \times \frac{2^3}{6} = \frac83$.

</details>

**Example 3.** For which of $x^3$ on $[0, 1]$ and $x^3$ on $[-1, 1]$ does the trapezium rule with two equal strips give an overestimate?

<details><summary>Show solution</summary>

On $[0,1]$, $x^3$ is convex ($f'' = 6x \ge 0$): overestimate. The rule gives $\frac14(0 + 2\cdot\frac18 + 1) = \frac{5}{16} > \frac14$.

On $[-1,1]$ the function is odd and the strips are symmetric about $0$, so the rule gives exactly $0$, which is the true value. Neither over nor under.

</details>
