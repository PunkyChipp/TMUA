# Exponentials & logarithms

TMUA uses logs and exponentials to test algebraic care: using the laws correctly, spotting a hidden quadratic, handling inequalities where the base is less than $1$, and comparing sizes of numbers without a calculator. The domain of a log is a constant source of wrong answers.

## Must-know facts

$$\log_a x = y \iff a^y = x \qquad (a > 0,\ a \ne 1,\ x > 0).$$

* $\log_a(xy) = \log_a x + \log_a y$, $\quad\log_a\dfrac xy = \log_a x - \log_a y$, $\quad\log_a x^k = k\log_a x$.
* $\log_a 1 = 0$, $\log_a a = 1$, $a^{\log_a x} = x$.
* **Change of base:** $\log_a b = \dfrac{\log_c b}{\log_c a}$. Hence $\log_a b = \dfrac{1}{\log_b a}$ and $\log_a b\cdot\log_b c = \log_a c$.
* $\log_{a^k} x = \dfrac1k\log_a x$, so $\log_4 x = \tfrac12\log_2 x$.
* **Monotonicity:** if $a > 1$, then $a^x$ and $\log_a x$ are increasing; if $0 < a < 1$ they are decreasing.
* $\log_a x$ is negative when $x$ and $a$ lie on opposite sides of $1$.
* **Graphs:** $y = a^x$ passes through $(0, 1)$ with asymptote $y = 0$; $y = \log_a x$ passes through $(1, 0)$ with asymptote $x = 0$; they are reflections in $y = x$.
* $\log_a(kx) = \log_a k + \log_a x$: a horizontal stretch of a log graph is the same as a vertical translation.

## Techniques

* **Common base.** Write $4 = 2^2$, $27 = 3^3$, $\tfrac18 = 2^{-3}$ and equate exponents. Multiply the whole exponent: $27^{x-1} = 3^{3x-3}$.
* **Hidden quadratics.** $4^x = (2^x)^2$, $9^x = (3^x)^2$, $2^{x+1} = 2\cdot 2^x$. Substitute $y = 2^x$ and remember $y > 0$: a negative root in $y$ gives no solution, and each positive root gives exactly one $x$.
* **Reciprocal logs.** In equations with $\log_2 x$ and $\log_x 2$, put $t = \log_2 x$ so $\log_x 2 = \tfrac1t$.
* **Symmetric sums.** For $2^x + 2^{-x}$, put $u = 2^x + 2^{-x} \ge 2$; then $4^x + 4^{-x} = u^2 - 2$. Each $u > 2$ gives two values of $x$; $u = 2$ gives only $x = 0$.
* **Log inequalities.** Write the right-hand side as a log with the same base, then remove the logs, flipping the inequality if the base is less than $1$. Then intersect with the domain. With a variable base, split into base $> 1$ and $0 <$ base $< 1$.
* **Comparing sizes.** Match exponents ($3^{20} = 9^{10}$ versus $2^{30} = 8^{10}$), use $2^{10} = 1024 \approx 10^3$, or trap a log between fractional powers: $2^{3/2} = 2\sqrt2 < 3$ so $\log_2 3 > \tfrac32$.
* **Exponential models.** $V = Ab^t$: equal time steps multiply by equal factors. Divide two data points to eliminate $A$, then think in doubling or halving times rather than solving with logs.

> **Tip:** Useful benchmarks: $\log_{10}2 \approx 0.301$, $\log_{10}3 \approx 0.477$, $2^{10} = 1024$, $3^5 = 243$, $\sqrt2 \approx 1.414$, $\sqrt3 \approx 1.732$.

## Traps

> **Trap:** $\log(a + b) \ne \log a + \log b$, and $(\log a)^2 \neq \log a^2$. Also $\log_a b\cdot\log_b c$ is a *product* rule, not a sum.

> **Trap:** Not checking candidate solutions. Squaring or combining logs can introduce values where an original log has a negative or zero argument.

> **Trap:** Forgetting to flip an inequality when the base is between $0$ and $1$: $\log_{1/2}(x) > -2 \iff 0 < x < 4$.

> **Trap:** Using AM–GM on $t + \tfrac1t$ when $t = \log_a b$ could be negative.

> **Key idea:** Every log question has a hidden domain condition. Write it down first.

## Worked examples

**Example 1.** Solve $2^{2x+1} - 9\cdot 2^x + 4 = 0$.

<details><summary>Show solution</summary>

$2^{2x+1} = 2(2^x)^2$. With $y = 2^x$: $2y^2 - 9y + 4 = 0$, so $(2y - 1)(y - 4) = 0$, giving $y = \tfrac12$ or $y = 4$.

Hence $x = -1$ or $x = 2$.

</details>

**Example 2.** Solve $\log_{1/3}(2x - 1) \ge \log_{1/3}(x + 2)$.

<details><summary>Show solution</summary>

Domain: $2x - 1 > 0$ and $x + 2 > 0$, so $x > \tfrac12$.

The base is less than $1$, so the log is decreasing and the inequality flips: $2x - 1 \le x + 2$, i.e. $x \le 3$.

Answer: $\tfrac12 < x \le 3$.

</details>

**Example 3.** Put $2^{50}$, $3^{30}$ and $5^{20}$ in increasing order.

<details><summary>Show solution</summary>

Use exponent $10$: $2^{50} = 32^{10}$, $3^{30} = 27^{10}$, $5^{20} = 25^{10}$.

So $5^{20} < 3^{30} < 2^{50}$.

</details>

**Example 4.** How many real solutions does $\log_2 x = 3 - x$ have?

<details><summary>Show solution</summary>

Sketch: $y = \log_2 x$ is increasing and $y = 3 - x$ is decreasing, so they meet at most once. They do meet: at $x = 2$ both equal $1$. Exactly one solution, $x = 2$.

</details>
