# Graphs & transformations

TMUA rarely asks you to draw a graph, but it constantly rewards being able to *picture* one. Typical questions: pick the right sketch from several, say where a point goes under a transformation, count the solutions of an equation by counting intersections, or read information about $f'$ from a graph of $f$ (or the other way round). A 10-second sketch usually beats a page of algebra.

## Must-know facts

**Polynomials from factors.** For $y = a(x-p)^m(x-q)^n\cdots$:

* odd power: the curve *crosses* the axis at that root; even power: it *touches* (turning point on the axis);
* a triple root is a crossing with a stationary point of inflection;
* the leading coefficient and degree fix the ends; the $y$-intercept is a free check.

**Reciprocal and rational shapes.**

* $y = \dfrac{1}{x-p} + q$: asymptotes $x = p$, $y = q$.
* $y = \dfrac{1}{g(x)}$: vertical asymptotes at roots of $g$; where $g$ has a minimum, $1/g$ has a maximum (and vice versa); $1/g$ has the same sign as $g$; large $|g|$ means $1/g$ near $0$.
* $y = \dfrac{k}{x^2}$ stays on one side of the $x$-axis; $y = \dfrac{k}{x}$ uses opposite quadrants.

**Transformations of $y = f(x)$.**

| Equation | Effect |
|---|---|
| $y = f(x) + d$ | up $d$ |
| $y = f(x + c)$ | **left** $c$ |
| $y = af(x)$ | stretch parallel to $y$-axis, factor $a$ |
| $y = f(bx)$ | stretch parallel to $x$-axis, factor $\tfrac1b$ |
| $y = -f(x)$, $y = f(-x)$ | reflect in $x$-axis, $y$-axis |

Changes *outside* $f$ act on $y$ as they look. Changes *inside* act on $x$ the inverse way.

**Modulus.** $y = |f(x)|$: reflect the parts below the $x$-axis upwards. $y = f(|x|)$: keep the part with $x \ge 0$ and reflect it in the $y$-axis (the result is always even).

**Gradient graphs.** Turning points of $f$ are where $f'$ is zero *and changes sign*; $f$ increasing $\iff f' > 0$; a stationary point of inflection of $f$ is where $f'$ touches the axis.

## Techniques

* **Where does a point go?** For $y = af(bx + c) + d$, a point $(p, q)$ on $y=f(x)$ moves to the $x$ solving $bx + c = p$, with $y = aq + d$. Don't apply transformations one at a time unless asked about order.
* **Order of transformations.** Each horizontal step *replaces $x$* in the current equation. So "translate left 6, then stretch by $\tfrac12$" gives $f(x+6) \to f(2x+6)$, whereas "stretch by $\tfrac12$, then translate left 6" gives $f(2(x+6))$. When in doubt, write the equation after each step.
* **Counting solutions.** Rearrange $g(x) = h(x)$ into two graphs you can sketch — often a curve and a line, or a curve and a horizontal line $y=k$. The count only changes when the line passes through a turning point, a corner (of a modulus graph) or an endpoint, or becomes tangent. Test those critical positions.
* **Picking a graph.** Eliminate using the cheapest features first: $y$-intercept, sign for large $x$, symmetry (even/odd), asymptotes. You rarely need more than two features to leave one option.
* **Composite equations.** For $f(f(x)) = c$, first solve $f(t) = c$ for $t$, then count solutions of $f(x) = t$ for each $t$ with horizontal lines.

## Traps

> **Trap:** $f(x - 3)$ moves the graph *right*, and $f(2x)$ *squashes* it by factor $\tfrac12$. The inside of the bracket always acts the opposite way to how it looks.

> **Trap:** Dividing both sides by a factor like $x+1$ loses the solution where that factor is zero. Factorise, then handle the zero case separately.

> **Trap:** A horizontal line through a turning point (or any line tangent to a curve) meets it at a *repeated* root — count it once, not twice.

> **Tip:** Only a negative *vertical* factor turns maxima into minima. Reflecting in the $y$-axis (a negative factor inside) keeps a maximum a maximum.

> **Key idea:** "How many solutions" is almost always "how many intersections" — sketch before solving.

## Worked examples

**Example 1.** The curve $y=f(x)$ has a minimum at $(-2, 3)$. Find the corresponding stationary point on $y = 4 - f(2x + 6)$ and its nature.

<details><summary>Show solution</summary>

Inside: $2x + 6 = -2 \Rightarrow x = -4$. Outside: $y = 4 - 3 = 1$.

The vertical factor is $-1$, so the minimum becomes a **maximum** at $(-4, 1)$. (The horizontal stretch and shift do not change its nature.)

</details>

**Example 2.** For which values of $k$ does $|x^2 - 1| = k$ have exactly four real solutions?

<details><summary>Show solution</summary>

Sketch $y = |x^2 - 1|$: a W shape with zeros at $x=\pm1$ and a reflected hump reaching $y=1$ at $x=0$.

Slide the horizontal line $y = k$ upwards:

* $k < 0$: none; $k = 0$: two ($\pm1$);
* $0 < k < 1$: four (two on the hump, two on the outer arms);
* $k = 1$: three (touches the top of the hump at $x=0$);
* $k > 1$: two.

So exactly four solutions for $0 < k < 1$.

</details>

**Example 3.** How many real solutions has $\dfrac{1}{x} = x^2 - 2$?

<details><summary>Show solution</summary>

Multiply by $x$ (note $x \ne 0$): $x^3 - 2x - 1 = 0$. Spot $x = -1$: $(x+1)(x^2 - x - 1) = 0$, giving $x = -1$ and $x = \tfrac{1\pm\sqrt5}{2}$.

None is $0$, so there are **3** solutions. A sketch shows one crossing in the first quadrant and two close together in the third — exactly the sort of pair a rough sketch can miss, so confirm with algebra when the curves are close.

</details>
