# Graphs & transformations

TMUA rarely asks you to draw a graph, but it keeps rewarding the ability to *picture* one. Typical questions: pick the right sketch from five, say where a point or turning point goes under a transformation, count the solutions of an equation by counting intersections, decide which numbers of roots are possible, or read $f'$ from a graph of $f$. A 10-second sketch usually beats a page of algebra.

## Must-know facts

**Basic shapes (spec list: lines, quadratics, cubics, trig, exponential, log, square-root, modulus).**

* $y = a^x$ ($a > 1$): through $(0, 1)$, always positive, $x$-axis an asymptote on the left. $y = a^{-x}$ is its mirror image in the $y$-axis. $y = A - B\,a^{-x}$ rises from $A - B$ towards the asymptote $y = A$.
* $y = \ln x$: only for $x > 0$, through $(1, 0)$, $y$-axis an asymptote, increasing ever more slowly. $\ln(kx) = \ln k + \ln x$, so a horizontal stretch of $\ln x$ is also a vertical translation.
* $y = \sqrt{x}$: starts at $(0, 0)$, exists for $x \ge 0$ only. For $y = \sqrt{p - x}$ the curve exists for $x \le p$ (reflected, then moved).
* $y = a(x+b)^2 + c$: $a$ fixes which way up (and how steep), the vertex is $(-b, c)$, the $y$-intercept is $ab^2 + c$.

**Polynomials from factors.** For $y = a(x-p)^m(x-q)^n\cdots$: an odd power *crosses* the axis, an even power *touches* it; the leading coefficient fixes the ends; the $y$-intercept is a free check.

**Possible numbers of real roots.** A polynomial of degree $n$ has at most $n$ real roots, and an odd-degree one has at least one. To see which counts are possible in a family $p(x) = h(x) + k$, sketch $y = h(x)$ and slide the line $y = -k$: the count changes only at turning values. Symmetry can rule counts out (roots of an even function pair up as $\pm x$).

**Transformations of $y = f(x)$.**

| Equation | Effect |
|---|---|
| $y = f(x) + d$ | up $d$ |
| $y = f(x + c)$ | **left** $c$ |
| $y = af(x)$ | stretch parallel to $y$-axis, factor $a$ |
| $y = f(bx)$ | stretch parallel to $x$-axis, factor $\tfrac1b$ |
| $y = -f(x)$, $y = f(-x)$ | reflect in $x$-axis, $y$-axis |

Changes *outside* $f$ act on $y$ as they look; changes *inside* act on $x$ the inverse way.

**Composite functions.** $f(g(x))$ means *apply $g$ first*. Write the composite out before sketching: e.g. with $f(x) = x^2 - 4$, $g(x) = |x - 1|$, $f(g(x)) = (x-1)^2 - 4$ because $|u|^2 = u^2$.

**Modulus.** $y = |f(x)|$: reflect the parts below the $x$-axis upwards. $y = f(|x|)$: keep the part with $x \ge 0$ and reflect it in the $y$-axis (the result is always even).

**Gradient graphs.** $f$ increasing $\iff f' > 0$. A maximum or minimum of $f$ is where $f'$ is zero **and changes sign**. Where $f'$ touches the axis without changing sign, $f$ has a horizontal tangent but keeps going the same way (you only need this qualitatively; points of inflexion are not examined as such).

## Techniques

* **Where does a point go?** For $y = af(bx + c) + d$, the point $(p, q)$ moves to the $x$ solving $bx + c = p$, with $y = aq + d$. Only a negative factor $a$ swaps maxima and minima.
* **Order of transformations.** Each horizontal step *replaces $x$* in the current equation; each vertical step acts on the whole right-hand side. So "translate left 6, then stretch by $\tfrac12$" gives $f(2x + 6)$, but "stretch by $\tfrac12$, then translate left 6" gives $f(2x + 12)$; and "down 3, then reflect in the $x$-axis" gives $3 - f(x)$. Factorise the inside as $b(x - p)$: stretch and reflect for $b$, translate by $p$ last.
* **Counting solutions.** Turn $g(x) = h(x)$ into two graphs you can sketch. The count only changes when a line passes through a turning point, a corner of a modulus graph or an endpoint, or becomes tangent: test those positions.
* **Exponential versus polynomial.** Check integer points, then remember an exponential eventually overtakes any polynomial, which often gives one extra, far-off crossing. A line meets a curve that always bends the same way at most twice.
* **Picking a graph.** Eliminate with the cheapest features first: domain/endpoint, $y$-intercept, sign for large $x$, symmetry, asymptotes, one middle value.
* **Composite equations.** For $f(f(x)) = c$, solve $f(t) = c$ for $t$, then count solutions of $f(x) = t$ with horizontal lines.

## Traps

> **Trap:** $f(x - 3)$ moves the graph *right*, and $f(2x)$ *squashes* it by factor $\tfrac12$. The inside of the bracket acts the opposite way to how it looks.

> **Trap:** Dividing both sides by a factor like $x + 1$ loses the solution where that factor is zero.

> **Trap:** A line through a turning point, or tangent to a curve, gives a *repeated* root: one point, counted once.

> **Trap:** With $t = |x|$, discard negative $t$ and remember $t = 0$ gives one $x$, not two.

> **Key idea:** "How many solutions" is almost always "how many intersections" — sketch before solving.

Not examined: general rational functions such as $\dfrac{1}{x^2 - 1}$ beyond $y = \dfrac{k}{x}$ (GCSE), and questions *about* points of inflexion.

## Worked examples

**Example 1.** The curve $y = f(x)$ has a minimum at $(-2, 3)$. Find the corresponding stationary point on $y = 4 - f(2x + 6)$ and its nature.

<details><summary>Show solution</summary>

Inside: $2x + 6 = -2 \Rightarrow x = -4$. Outside: $y = 4 - 3 = 1$.

The vertical factor is $-1$, so the minimum becomes a **maximum** at $(-4, 1)$.

</details>

**Example 2.** For which values of $k$ does $|x^2 - 1| = k$ have exactly four real solutions?

<details><summary>Show solution</summary>

$y = |x^2 - 1|$ is a W with zeros at $\pm1$ and a hump of height 1 at $x = 0$. Sliding $y = k$ upwards: $k = 0$ two; $0 < k < 1$ four; $k = 1$ three; $k > 1$ two. So $0 < k < 1$.

</details>

**Example 3.** How many real solutions has $2^x = x + 3$?

<details><summary>Show solution</summary>

For $x < -3$ the line is negative, so no solutions there. At $x = -3$: $\tfrac18 > 0$; at $x = 0$: $1 < 3$, so one crossing in $(-3, 0)$. At $x = 2$: $4 < 5$; at $x = 3$: $8 > 6$, a second crossing in $(2, 3)$. As $2^x$ bends upwards everywhere, a line meets it at most twice: **2** solutions.

</details>
