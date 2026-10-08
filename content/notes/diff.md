# Differentiation

TMUA differentiation is AS-level: powers of $x$, including fractional and negative powers, and their sums. Questions rarely test the mechanics alone. They test whether you can turn a condition (a tangent through a point, a number of roots, "increasing on this interval", a quantity to optimise) into a statement about $f'$, and whether you respect the edge cases. Differentiation from first principles is not examined.

## Must-know facts

* $\dfrac{d}{dx}x^n = nx^{n-1}$ for any rational $n$. **Simplify first**: $\sqrt{x} = x^{1/2}$, $\dfrac{1}{x^2} = x^{-2}$, and $\dfrac{(x+3)^2}{x\sqrt x} = x^{1/2} + 6x^{-1/2} + 9x^{-3/2}$. Never differentiate a quotient by differentiating top and bottom separately.
* Tangent at $x=a$: $y - f(a) = f'(a)(x-a)$. Normal: gradient $-\dfrac{1}{f'(a)}$.
* **Second derivative**: $f''$ is the rate of change of the gradient. On a graph of $f'$, the *height* tells you about $f$ and the *slope* is $f''$.
* **Rates of change**: $\dfrac{dh}{dt}$ is the rate at which $h$ changes. If $s$ is a displacement, $\dfrac{ds}{dt}$ is the velocity, and the motion reverses where it changes sign.
* **Increasing / decreasing**: $f'(x) > 0$ throughout an interval makes $f$ strictly increasing there; $f'(x) < 0$ makes it strictly decreasing. Questions will state the convention they use; read it.
* Stationary point: $f'(a) = 0$. A **local maximum** has $f'$ changing $+\to-$, a **local minimum** $-\to+$.
* Second-derivative test: $f'(a)=0,\ f''(a)>0 \Rightarrow$ minimum; $f''(a)<0 \Rightarrow$ maximum. If $f''(a)=0$ the test says nothing: look at the sign of $f'$ either side ($x^4$ has a minimum at $0$ with $f''(0) = 0$).
* A cubic $ax^3+bx^2+cx+d$ has two, one or no stationary points according to whether the discriminant of $3ax^2+2bx+c$ is positive, zero or negative. For $a > 0$ the left one is the maximum. The gap between its stationary values is $\frac{|a|}{2}(\beta - \alpha)^3$.

Points of inflexion are not examined directly; you only need to know that a curve like $x^3$ can have $f' = 0$ without turning.

## Techniques

**Count roots with stationary values.** $f(x)=c$ has as many solutions as there are crossings of the horizontal line $y=c$ with the sketch. A cubic has three distinct real roots exactly when it has two stationary points and their values have opposite signs. For $|f(x)| = c$, reflect the parts below the axis first.

**Tangent from an external point.** Write the tangent at a general point $t$: $y = f'(t)(x-t) + f(t)$. Substitute the external point. Each real root $t$ is a point of contact. For a cubic you get a cubic in $t$; count its roots with its stationary values.

**A tangent meets the curve again.** Substitute the tangent into the curve: the point of contact is a **double** root, so the sum of roots gives the new point immediately.

**Optimisation.** Choose one variable, use the constraint to eliminate the others, differentiate, and check it is a maximum or minimum (sign of $f'$ or $f''$). On a closed interval also compare the endpoint values.

**Parameter conditions for increasing/decreasing.** "$f'(x) > 0$ for all $x$ in an interval" is a statement about a quadratic (or a power) on that interval. Find where its minimum on the interval occurs: the vertex if it is inside, otherwise an endpoint. An open interval does not contain its endpoints, so equality at an endpoint is allowed.

**Reading a graph of $f'$.** $x$-intercepts of $f'$ are stationary points of $f$; crossing from above to below means a maximum of $f$. Where the graph of $f'$ is above the axis, $f$ is increasing, however that graph is sloping.

> **Tip:** Distance travelled is not displacement. Split at every time where the rate changes sign and add the sizes of the changes.

## Traps

> **Trap:** $f'(a)=0$ is necessary for a turning point of a polynomial, but not sufficient. And $f''(a) > 0$ is sufficient for a minimum (with $f'(a)=0$), but not necessary.

> **Trap:** A local maximum is not the greatest value on an interval. Always check the endpoints; the curve may climb back above the local maximum.

> **Trap:** Tangent cases. When counting distinct solutions as a parameter varies, the parameter values where a line is tangent give a repeated root and so one fewer distinct solution.

> **Trap:** "Increasing on $0 < x < 4$" with $f'(x) = k - 3\sqrt x$ needs $k \ge 6$, not $k > 6$: the value $x = 4$ is not in the interval.

* The normal gradient is $-\frac{1}{m}$, not $-m$ or $\frac1m$.
* $\frac{d}{dx}(8x^{-1}) = -8x^{-2}$: the negative power brings down a negative sign.

## Worked examples

**Example 1.** Find the values of $k$ for which $f(x) = x^3 + kx^2 + 3x$ has $f'(x) > 0$ for all $x \ge 0$.

<details><summary>Show solution</summary>

$f'(x) = 3x^2 + 2kx + 3$, an upward parabola with vertex at $x = -\frac k3$.

* If $k \ge 0$ the vertex is at $x \le 0$, so on $x \ge 0$ the least value is $f'(0) = 3 > 0$. Fine.
* If $k < 0$ the vertex is inside $x>0$, with value $3 - \frac{k^2}{3}$. We need $3 - \frac{k^2}{3} > 0$, i.e. $-3 < k < 0$.

Answer: $k > -3$. The discriminant alone ($-3 < k < 3$) would wrongly exclude large positive $k$, whose roots are negative.

</details>

**Example 2.** How many tangents to $y = x^3$ pass through the point $(2, 0)$?

<details><summary>Show solution</summary>

The tangent at $t$ is $y = 3t^2(x - t) + t^3 = 3t^2x - 2t^3$.

Through $(2, 0)$: $0 = 6t^2 - 2t^3 = 2t^2(3 - t)$, so $t = 0$ or $t = 3$.

$t = 0$ gives the tangent $y=0$ and $t=3$ gives $y = 27x - 54$. Two tangents: the repeated root $t=0$ still gives just one line.

</details>

**Example 3.** Find the greatest and least values of $f(x) = x^2(3-x)$ on $0 \le x \le 4$.

<details><summary>Show solution</summary>

$f(x) = 3x^2 - x^3$, $f'(x) = 6x - 3x^2 = 3x(2 - x)$.

Stationary values: $f(0) = 0$ (min), $f(2) = 4$ (max). Endpoint: $f(4) = 48 - 64 = -16$.

Greatest value $4$, at $x = 2$. Least value $-16$, at the endpoint $x = 4$, not at the local minimum.

</details>
