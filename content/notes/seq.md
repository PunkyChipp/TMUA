# Sequences, series & binomial

TMUA rarely asks you to grind through a long sum. It tests whether you can spot structure: a sequence that repeats, a series that only converges for some values, a binomial term that is the only one that matters, or a sum that collapses by symmetry. Most questions take two or three lines once you see the right idea.

## Must-know facts

**Arithmetic** (first term $a$, common difference $d$):
$$u_n = a + (n-1)d, \qquad S_n = \frac n2\big(2a + (n-1)d\big) = \frac n2(\text{first} + \text{last}).$$

**Geometric** (first term $a$, common ratio $r$):
$$u_n = ar^{n-1}, \qquad S_n = \frac{a(1 - r^n)}{1 - r}, \qquad S_\infty = \frac{a}{1-r} \text{ only if } |r| < 1.$$

**Sigma:** $\sum_{r=1}^n r = \tfrac12 n(n+1)$, and $\sum_{r=1}^n c = nc$ (the constant appears $n$ times). Check how many terms there are: $\sum_{r=0}^{n}$ has $n+1$.

**From sums to terms:** $u_n = S_n - S_{n-1}$ for $n \ge 2$, but $u_1 = S_1$.

**Binomial** (positive integer $n$):
$$(a + b)^n = \sum_{r=0}^{n}\binom nr a^{n-r}b^r, \qquad \binom nr = \binom n{n-r}, \qquad \sum_{r=0}^n\binom nr = 2^n.$$

**Recurrences** $u_{n+1} = f(u_n)$: a fixed point solves $f(L) = L$; if the sequence converges, it converges to a fixed point (the converse is false).

## Techniques

* **General term first.** For a coefficient or constant term, write the general term as a single power of $x$, e.g. $\binom6r(-2)^r x^{12-3r}$, then choose $r$. Put the sign inside the bracket: $(2 - x)^7$ has terms $\binom7r2^{7-r}(-x)^r$.
* **Pair up products.** $(1+x)^6(1-x)^4 = (1-x^2)^4(1+x)^2$ is far quicker than two full expansions. More generally, you only need the terms up to the power you want.
* **Substitute special values.** With $f(x) = \sum a_k x^k$: $f(1)$ is the sum of the coefficients, $f(-1)$ is the alternating sum, and $\tfrac12\big(f(1) + f(-1)\big)$ is the sum of the even-power coefficients.
* **Centre an arithmetic sequence.** If you know a middle term $m$, write the terms around it as $m \pm kd$. Then $S_{2k+1} = (2k+1)m$ and products of symmetric terms are differences of squares.
* **Generate terms of a recurrence.** Write down four or five terms before doing any algebra. Many TMUA recurrences are periodic, e.g. $u_{n+1} = \frac{1}{1-u_n}$ has period $3$.
* **Convergence is a condition, not an afterthought.** For a series with a variable ratio, first solve $|r| < 1$, then work inside that interval.
* **Symmetry for sums of binomial coefficients.** $\sum r\binom nr = n2^{n-1}$: pair $r$ with $n-r$ so each pair averages to $n/2$.
* **Linear recurrences** $u_{n+1} = pu_n + q$: the fixed point is $L = \frac{q}{1-p}$, and $u_n - L$ is geometric with ratio $p$.

> **Tip:** When options are numbers, eliminate with a rough size or sign check before computing. The sign of a binomial coefficient is fixed by $(-1)^r$, which often removes half the options.

## Traps

> **Trap:** Using $S_\infty = \dfrac{a}{1-r}$ without checking $|r| < 1$. The formula happily returns a number for $r = 2$, but that series diverges.

> **Trap:** Off-by-one errors. $u_n$ has $(n-1)$ steps of $d$; $\sum_{r=0}^{20}$ has $21$ terms; the $r$th term of a binomial expansion uses $\binom n{r-1}$.

> **Trap:** Confusing the first negative *term* of a series with the first negative *sum*. The sum only turns negative after the positive terms have been cancelled, roughly twice as far along.

> **Trap:** Treating $u_n = S_n - S_{n-1}$ as valid for $n = 1$. Always check $u_1 = S_1$ separately.

> **Trap:** "Bounded" does not mean "convergent". A recurrence can stay trapped in an interval and still cycle forever.

> **Key idea:** Logs turn geometric sequences into arithmetic ones (and $2^{u_n}$ turns arithmetic into geometric). That link appears in both topics.

## Worked examples

**Example 1.** Find the constant term in $\left(2x - \dfrac{1}{x^2}\right)^9$.

<details><summary>Show solution</summary>

The general term is $\binom9r(2x)^{9-r}\left(-x^{-2}\right)^r = \binom9r 2^{9-r}(-1)^r x^{9 - 3r}$.

The power is zero when $r = 3$: $\binom93 \cdot 2^6 \cdot (-1)^3 = 84 \cdot 64 \cdot (-1) = -5376$.

</details>

**Example 2.** For which values of $x$ does $\displaystyle\sum_{n=0}^{\infty}\left(\frac{x}{x+1}\right)^n$ converge, and what is its sum?

<details><summary>Show solution</summary>

Need $\left|\dfrac{x}{x+1}\right| < 1$, i.e. $|x| < |x + 1|$, i.e. $x$ is closer to $0$ than to $-1$: $x > -\tfrac12$.

Then $S = \dfrac{1}{1 - \frac{x}{x+1}} = \dfrac{x+1}{1} = x + 1$.

</details>

**Example 3.** $u_1 = 3$ and $u_{n+1} = \dfrac{u_n - 1}{u_n}$. Find $u_{2026}$.

<details><summary>Show solution</summary>

$u_1 = 3$, $u_2 = \tfrac23$, $u_3 = \dfrac{-1/3}{2/3} = -\tfrac12$, $u_4 = \dfrac{-3/2}{-1/2} = 3$.

Period $3$. Since $2026 = 3 \times 675 + 1$, $u_{2026} = u_1 = 3$.

</details>

**Example 4.** Find the coefficient of $x^3$ in $(1 + 2x)^5(1 - x)^3$.

<details><summary>Show solution</summary>

$(1+2x)^5 = 1 + 10x + 40x^2 + 80x^3 + \cdots$ and $(1-x)^3 = 1 - 3x + 3x^2 - x^3$.

Collect the $x^3$ terms: $80 - 3\cdot 40 + 3\cdot 10 - 1 = 80 - 120 + 30 - 1 = -11$.

</details>
