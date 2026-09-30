# Number & arithmetic

TMUA number questions look easy and are designed to punish careless arithmetic. Typical questions ask you to count integers with a property, find a remainder or last digit, compare huge numbers without a calculator, or handle percentages and averages. The winning habit is to look for **structure** (factorise, work with totals or multipliers, find a cycle) rather than computing.

## Must-know facts

* **Prime factorisation** is the master key. If $n=p^a q^b r^c$ then $n$ has $(a+1)(b+1)(c+1)$ positive divisors.
* $\text{HCF}(a,b)\times\text{LCM}(a,b)=ab$. For the HCF take the minimum power of each prime; for the LCM take the maximum.
* Divisible by $m$ and by $n$ means divisible by $\operatorname{lcm}(m,n)$, **not** $mn$ (e.g. divisible by $4$ and $6$ means divisible by $12$, not $24$).
* A product of $k$ consecutive integers is divisible by $k!$. So $n(n+1)$ is even, and $(n-1)n(n+1)$ is divisible by $6$.
* Last digits of powers cycle with period dividing $4$: $2\to2,4,8,6$; $3\to3,9,7,1$; $7\to7,9,3,1$; $8\to8,4,2,6$; $4$ and $9$ have period $2$; $0,1,5,6$ are fixed.
* Divisibility tests: $3$ and $9$ (digit sum), $4$ (last two digits), $8$ (last three), $11$ (alternating digit sum).
* Trailing zeros of $n!$: $\lfloor n/5\rfloor+\lfloor n/25\rfloor+\lfloor n/125\rfloor+\cdots$.
* Percentages: an increase of $r\%$ is multiplication by $1+\frac{r}{100}$. Successive changes multiply. To reverse a change, **divide** by the multiplier.
* Means: total $=$ mean $\times$ count. Adding a value above the mean raises the mean; below lowers it.

## Techniques

**Work with totals and multipliers.** Averages questions become subtraction of totals. Percentage chains become products like $1.25\times0.8=1$.

**Reduce modulo something small.** For last digits work mod $10$; for remainders find when the powers cycle (e.g. $10^6\equiv1\pmod 7$, $2^3\equiv1\pmod7$), then reduce the exponent modulo the cycle length.

**Factorise to find integer solutions.** Rearrange into (bracket)(bracket) $=$ constant, then count factor pairs. Two standard forms:

* $x^2-y^2=N$: $(x-y)(x+y)=N$, and the two factors must have the same parity.
* $\frac1x+\frac1y=\frac1n$: $(x-n)(y-n)=n^2$.

Remember negative factor pairs, and whether the question wants ordered pairs.

**Compare sizes by clearing roots and powers.** To compare $a^{1/m}$ with $b^{1/n}$, raise both to the power $mn$. To compare $2^{100}$ with $3^{60}$, write both as 20th powers: $32^{20}$ vs $27^{20}$. Logs are rarely needed.

**Count with complements and Venn diagrams.** "Divisible by $3$ or $5$" is $\lfloor N/3\rfloor+\lfloor N/5\rfloor-\lfloor N/15\rfloor$.

**Test small values, then prove.** For "must be true" statements about all integers, try $n=1,2,3$ and a negative value first. One failure kills a statement; if nothing fails, look for a factorisation that proves it.

> **Tip:** In a counterexample question, the answer is usually the value where the expression visibly factorises: $n^2+n+41$ at $n=40$ is $41^2$.

## Traps

> **Trap:** Adding percentages. $+25\%$ then $-20\%$ is no change, not $+5\%$.

> **Trap:** Reverse percentages. If £68 is the price after a $15\%$ cut, the original is $68\div0.85$, not $68\times1.15$.

> **Trap:** Forgetting the conditions in "different", "positive" or "ordered". These change counts by factors of $2$ and cause off-by-one errors.

> **Trap:** Assuming a pattern continues. $n^4-n^2$ is always divisible by $12$ but not by $24$ ($n=2$ gives $12$).

> **Trap:** Getting the power wrong when passing from $n^k$ back to $n$. Exponents of primes in $n^k$ are multiples of $k$, so $p^a\mid n^k$ gives $p^{\lceil a/k\rceil}\mid n$. For example $2^3\mid n^2$ gives $2^2\mid n$ (not just $2\mid n$), while $2\mid n^3$ gives only $2\mid n$.

## Worked examples

**Example 1.** Two positive integers have HCF $4$ and LCM $240$. How many unordered pairs are possible?

<details><summary>Show solution</summary>

Write them as $4p$, $4q$ with $p,q$ coprime and $pq=240/4=60=2^2\cdot3\cdot5$. Each prime power ($4$, $3$, $5$) goes wholly to $p$ or wholly to $q$: $2^3=8$ ordered splits, so $4$ unordered pairs: $(4,240),(16,60),(12,80),(20,48)$.

</details>

**Example 2.** What is the remainder when $3^{2026}$ is divided by $7$?

<details><summary>Show solution</summary>

Powers of $3$ mod $7$: $3,2,6,4,5,1$, so $3^6\equiv1$. Since $2026=6\times337+4$, $3^{2026}\equiv3^4=81\equiv4\pmod7$. The remainder is $4$.

</details>

**Example 3.** The mean of $8$ numbers is $15$. Two numbers with mean $9$ are removed. What is the new mean?

<details><summary>Show solution</summary>

Totals: $8\times15=120$, removed $2\times9=18$, leaving $102$ over $6$ numbers. The new mean is $17$.

</details>

**Example 4.** Which is larger, $2^{300}$ or $3^{200}$?

<details><summary>Show solution</summary>

Write both as $100$th powers: $2^{300}=8^{100}$ and $3^{200}=9^{100}$. So $3^{200}$ is larger.

</details>
