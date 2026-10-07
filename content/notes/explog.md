# Exponentials & logarithms

TMUA uses logs and exponentials to test algebraic care: using the laws correctly, spotting a hidden quadratic, handling inequalities where the base is less than $1$, sketching $y = a^x$, and comparing sizes of numbers without a calculator. The domain of a log is a constant source of wrong answers.

> **Key idea:** The 2026 specification says questions needing the **change of base formula will not be set**. Everything can be done with the laws below and the definition $a^b = c \iff b = \log_a c$. If you find yourself converting $\log_4$ into $\log_2$, look for a more direct route.

## Must-know facts

$$\log_a x = y \iff a^y = x \qquad (a > 0,\ a \ne 1,\ x > 0).$$

* $\log_a(xy) = \log_a x + \log_a y$, $\quad\log_a\dfrac xy = \log_a x - \log_a y$, $\quad\log_a x^k = k\log_a x$.
* $\log_a\dfrac1x = -\log_a x$, $\quad\log_a 1 = 0$, $\quad\log_a a = 1$, $\quad a^{\log_a x} = x$.
* **Monotonicity:** if $a > 1$, then $a^x$ and $\log_a x$ are increasing; if $0 < a < 1$ they are decreasing.
* $\log_a x$ is negative when $x$ and $a$ lie on opposite sides of $1$ (e.g. $\log_{1/2} 8 = -3$, and $\log_x 9 < 0$ for $0 < x < 1$).
* $\log_a(x^2) = 2\log_a|x|$, defined for all $x \ne 0$; $2\log_a x$ needs $x > 0$.

## Graphs of $y = a^x$

* Every $y = a^x$ passes through $(0, 1)$, is always positive, and has asymptote $y = 0$. Increasing if $a > 1$, decreasing if $0 < a < 1$.
* For $0 < a < 1 < b$: $a^x < b^x$ when $x > 0$, but the order **reverses** when $x < 0$; the graphs meet only at $(0, 1)$.
* $a^{-x} = \left(\tfrac1a\right)^x$: reflecting in the $y$-axis swaps $a$ and $\tfrac1a$.
* $a^{x-k} = a^{-k}\cdot a^x$: for exponentials a horizontal translation is also a vertical stretch. Similarly $\log_a(kx) = \log_a k + \log_a x$: for logs a horizontal stretch is also a vertical translation.
* $y = \log_a x$ is the reflection of $y = a^x$ in $y = x$: through $(1, 0)$, asymptote $x = 0$.

## Techniques

* **Common base.** Write $9 = 3^2$, $27 = 3^3$, $\tfrac18 = 2^{-3}$ and equate exponents. Multiply the whole exponent: $27^{x-1} = 3^{3x-3}$.
* **Equations $a^x = b$.** The answer is $x = \log_a b$; leave it in that form. For $3^{2x} = 4$: $3^x = 2$ (as $3^x > 0$), so $x = \log_3 2$. Often you need a related power rather than $x$: $27^x = (3^x)^3 = 8$.
* **Hidden quadratics.** $25^x = (5^x)^2$, $2^{x+1} = 2\cdot 2^x$, $3^{2-x} = 9/3^x$. Substitute $y = 5^x$ and remember $y > 0$: a negative or zero root gives no solution, and each positive root gives exactly one $x$. For $25^x - 3\cdot 5^x + 2 = 0$: $y = 1$ or $2$, so $x = 0$ or $\log_5 2$.
* **Sum of solutions.** If the roots are $y_1, y_2$, the solutions sum to $\log_a y_1 + \log_a y_2 = \log_a(y_1y_2)$, which is the log of the product of the roots.
* **Counting solutions with a parameter.** Use the sum and product of the roots in $y$ to control their signs, and check the repeated-root and zero-root edge cases separately.
* **Symmetric sums.** For $2^x + 2^{-x}$, put $u = 2^x + 2^{-x} \ge 2$; then $4^x + 4^{-x} = u^2 - 2$. Each $u > 2$ gives two values of $x$; $u = 2$ gives only $x = 0$.
* **$x$ in the base and the exponent.** For $x^{\log_2 x}$, take $\log_2$ of both (positive) sides: $\log_2\left(x^{\log_2 x}\right) = (\log_2 x)^2$. Then it is a quadratic in $t = \log_2 x$, and **every** real $t$ is allowed.
* **Log equations and inequalities.** Write the constant as a log in the same base ($3 = \log_2 8$, $-2 = \log_{1/2} 4$), combine, remove the logs (reversing if the base is below $1$), then intersect with the domain.
* **Variable base.** For $\log_x(\ldots)$, split into $x > 1$ (increasing) and $0 < x < 1$ (decreasing), and write the right-hand side as $\log_x(x^k)$.
* **Comparing sizes.** Match exponents ($3^{20} = 9^{10}$ versus $2^{30} = 8^{10}$), use $2^{10} = 1024 > 10^3$, or trap a log between fractions: $\log_2 3 > \tfrac32 \iff 3 > 2^{3/2} \iff 9 > 8$.
* **Growth and decay models.** $V = Ab^t$: equal time steps multiply by equal factors. Divide two data points to eliminate $A$, then count doubling or halving times rather than solving with logs.

> **Tip:** Useful facts: $2^{10} = 1024$, $3^5 = 243$, $3^8 = 6561$, $5^5 = 3125$, $7^4 = 2401$.

## Traps

> **Trap:** $\log(a + b) \ne \log a + \log b$, and $(\log a)^2 \neq \log a^2$.

> **Trap:** Not checking candidate solutions. Combining logs can introduce values where an original log has a negative or zero argument. But do not over-reject: $\log_2(x^2)$ is fine for negative $x$.

> **Trap:** Forgetting to reverse an inequality when the base is between $0$ and $1$: $\log_{1/2}x > -2 \iff 0 < x < 4$.

> **Trap:** Assuming $a^x < b^x$ for all $x$ whenever $a < b$; it fails for $x < 0$. Similarly $a > b$ does not imply $a^a > b^b$: $\left(\tfrac14\right)^{1/4} = \left(\tfrac12\right)^{1/2}$.

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

The base is less than $1$, so the log is decreasing and the inequality reverses: $2x - 1 \le x + 2$, i.e. $x \le 3$.

Answer: $\tfrac12 < x \le 3$.

</details>

**Example 3.** Put $2^{50}$, $3^{30}$ and $5^{20}$ in increasing order.

<details><summary>Show solution</summary>

Use exponent $10$: $2^{50} = 32^{10}$, $3^{30} = 27^{10}$, $5^{20} = 25^{10}$.

So $5^{20} < 3^{30} < 2^{50}$.

</details>

**Example 4.** How many real solutions does $2^x = x + 2$ have?

<details><summary>Show solution</summary>

Sketch: $y = 2^x$ is convex and $y = x + 2$ is a line, so they meet at most twice. At $x = 2$ both equal $4$. At $x = -2$: $2^{-2} = \tfrac14 > 0$, and at $x = 0$: $1 < 2$, so they also cross between $-2$ and $0$. Exactly two solutions.

</details>
