# Differentiation

TMUA differentiation is AS-level: polynomials and powers of $x$, including fractional and negative powers. The questions rarely test the mechanics alone. They test whether you can turn a geometric condition (a tangent through a point, a number of roots, "no turning points") into an equation about $f'$, and whether you respect the edge cases.

## Must-know facts

* $\dfrac{d}{dx}x^n = nx^{n-1}$ for any rational $n$. Rewrite first: $\sqrt{x} = x^{1/2}$, $\dfrac{1}{x^2} = x^{-2}$, $\dfrac{x^2+4}{\sqrt x} = x^{3/2} + 4x^{-1/2}$.
* Tangent at $x=a$: $y - f(a) = f'(a)(x-a)$. Normal: gradient $-\dfrac{1}{f'(a)}$.
* $f$ is increasing where $f'(x) > 0$ and decreasing where $f'(x) < 0$.
* Stationary point: $f'(a) = 0$. Its nature comes from the **sign change** of $f'$:
  $-\to+$ minimum, $+\to-$ maximum, no change: stationary point of inflection.
* Second-derivative test: $f'(a)=0,\ f''(a)>0 \Rightarrow$ minimum; $f''(a)<0 \Rightarrow$ maximum; $f''(a)=0$ tells you **nothing**.
* A cubic $ax^3+bx^2+cx+d$ has two, one or no stationary points according to whether the discriminant of $3ax^2+2bx+c$ is positive, zero or negative. Its inflection point is at $x=-\frac{b}{3a}$, exactly midway between the turning points, and the curve has half-turn symmetry about it.

## Techniques

**Count roots with stationary values.** $f(x)=c$ has as many solutions as there are crossings of the horizontal line $y=c$ with the sketch. A cubic has three real roots exactly when its local maximum and local minimum values have opposite signs.

**Tangent from an external point.** Write the tangent at a general point $t$: $y = f'(t)(x-t) + f(t)$. Substitute the external point. This gives an equation in $t$; each real root is a point of contact. For $y=x^2$ you get a quadratic in $t$, for a cubic you get a cubic in $t$.

**Optimisation.** Choose one variable, use the constraint to eliminate the others, differentiate, and check the answer is a maximum (sign of $f'$ or $f''$). On a closed interval also evaluate the endpoints.

**Reading a graph of $f'$.** $x$-intercepts of $f'$ are stationary points of $f$. Crossing the axis means a turning point; touching it means a stationary inflection. Where the graph of $f'$ is above the axis, $f$ is increasing, however the graph of $f'$ is sloping.

> **Tip:** For a positive cubic, the left stationary point is the maximum and the right one is the minimum. No second derivative needed.

## Traps

> **Trap:** "No local maximum or minimum" is not the same as "no stationary points". If the discriminant of $f'$ is zero, $f'$ has a repeated root, and the stationary point is an inflection. The boundary values are included.

> **Trap:** $f'(a)=0$ is necessary for a turning point of a polynomial, but not sufficient ($x^3$ at $0$). $f''(a)=0$ does not mean inflection either ($x^4$ at $0$ is a minimum).

> **Trap:** A local maximum is not the greatest value on an interval. Always check the endpoints.

> **Trap:** Tangent cases. When counting "distinct real solutions" as a parameter varies, the parameter values where a line is tangent give a repeated root and so one fewer distinct solution. Decide carefully whether endpoints are strict.

* The normal gradient is $-\frac{1}{m}$, not $-m$ or $\frac1m$.
* $\frac{d}{dx}(8x^{-1}) = -8x^{-2}$: the negative power brings down a negative sign.
* Never differentiate a quotient by differentiating top and bottom separately.

## Worked examples

**Example 1.** Find the values of $k$ for which $y = x^3 + kx^2 + 12x$ is increasing for all $x$.

<details><summary>Show solution</summary>

$y' = 3x^2 + 2kx + 12$. We need $y' \ge 0$ for all $x$, i.e. the quadratic never goes negative: discriminant $\le 0$.

$4k^2 - 144 \le 0 \iff -6 \le k \le 6$.

At $k = \pm 6$, $y' = 3(x \pm 2)^2$, which is zero at a single point only, so $y$ is still increasing. Both endpoints are included.

</details>

**Example 2.** How many tangents to $y = x^3$ pass through the point $(2, 0)$?

<details><summary>Show solution</summary>

The tangent at $t$ is $y = 3t^2(x - t) + t^3 = 3t^2x - 2t^3$.

Through $(2, 0)$: $0 = 6t^2 - 2t^3 = 2t^2(3 - t)$, so $t = 0$ or $t = 3$.

$t = 0$ gives the tangent $y=0$ (the $x$-axis, at the inflection point), and $t=3$ gives $y = 27x - 54$. Two tangents. The repeated root $t=0$ still gives just one line.

</details>

**Example 3.** Find the greatest and least values of $f(x) = x^2(3-x)$ on $0 \le x \le 4$.

<details><summary>Show solution</summary>

$f(x) = 3x^2 - x^3$, $f'(x) = 6x - 3x^2 = 3x(2 - x)$.

Stationary values: $f(0) = 0$ (min), $f(2) = 4$ (max). Endpoint: $f(4) = 48 - 64 = -16$.

Greatest value is $4$, at $x = 2$. Least value is $-16$, at the endpoint $x = 4$, not at the local minimum. You only know either after checking the endpoints.

</details>
