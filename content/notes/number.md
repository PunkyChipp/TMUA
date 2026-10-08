# Number, ratio & units

TMUA number questions look easy and are designed to punish careless arithmetic. Expect to: count integers or arrangements with a property, use prime factorisation, convert recurring decimals, work with bounds, standard form and compound units, handle proportion with powers, and follow growth, decay or an iterative process without a calculator. The winning habit is to look for **structure** (factorise, use multipliers, find a fixed point) rather than grinding.

## Must-know facts

* **Unique prime factorisation** is the master key. If $n=p^a q^b r^c$ then $n$ has $(a+1)(b+1)(c+1)$ positive divisors.
* $\text{HCF}(a,b)\times\text{LCM}(a,b)=ab$. HCF: minimum power of each prime; LCM: maximum power. Divisible by $m$ and by $n$ means divisible by $\operatorname{lcm}(m,n)$, **not** $mn$.
* A product of $k$ consecutive integers is divisible by $k!$.
* **Recurring decimals:** if the repeating block has length $k$, multiply by $10^k$ and subtract. $0.\dot1\dot8=\frac{18}{99}$; $0.1\dot3\dot6=\frac{136-1}{990}=\frac3{22}$.
* **Bounds:** a value given to the nearest $10$ lies in $[x-5,\,x+5)$. For $a+b$ and $ab$ use like bounds; for $a-b$ and $a/b$ use **opposite** bounds (upper of $a$ with lower of $b$ for the maximum).
* **Standard form:** $a\times10^n$ with $1\le a<10$. To square-root, make the power even first: $4.9\times10^7=49\times10^6$.
* **Proportion:** $y\propto x^n$ means $y=kx^n$; $y\propto\frac1{x^n}$ means $y=\frac{k}{x^n}$. Scaling $x$ by $s$ scales $y$ by $s^n$ (or $s^{-n}$).
* **Percentages and growth:** an increase of $r\%$ multiplies by $1+\frac r{100}$; repeated changes multiply, so after $n$ steps the multiplier is $(1+\frac r{100})^n$. Reverse a change by **dividing**.
* **Compound units:** speed $=\frac{\text{distance}}{\text{time}}$, density $=\frac{\text{mass}}{\text{volume}}$, pressure $=\frac{\text{force}}{\text{area}}$. $1\text{ m}^2=10^4\text{ cm}^2$, $1\text{ m}^3=10^6\text{ cm}^3=1000$ litres, $1$ m/s $=3.6$ km/h.
* **Product rule:** if one choice can be made in $m$ ways and then another in $n$ ways, together there are $mn$ ways.

## Techniques

**Work with multipliers.** Successive changes become products: $+20\%$ blade length in $P\propto r^2v^3$ gives $1.2^2$; $-10\%$ wind gives $0.9^3$.

**Iterative processes.** For $u_{n+1}=ru_n-c$ find the fixed point $L=\frac{c}{r-1}$; then $u_n-L=(u_0-L)r^n$, so you only need powers of $r$. Build powers by squaring ($1.2^8=(1.2^4)^2=2.0736^2\approx4.3$).

**Bounds in a formula.** Ask, for each quantity, whether making it bigger makes the answer bigger or smaller, then pick the corresponding bound. Differences in a denominator are the classic trap.

**Estimation.** Round to one significant figure and handle powers of $10$ separately.

**Factorise to find integer solutions.** $x^2-y^2=N$: $(x-y)(x+y)=N$ with both factors of the same parity. $\frac1x+\frac1y=\frac1n$: $(x-n)(y-n)=n^2$.

**Count systematically.** Fill the most restricted positions first; split into cases when restrictions interact (e.g. last digit $0$ or not, when the first digit cannot be $0$). For digit-product questions, list digit sets by largest digit, then count arrangements (divide for repeated digits).

**Compare sizes by clearing powers.** Compare $a^{1/m}$ with $b^{1/n}$ via the power $mn$; compare $2^{48}$ with $3^{32}$ as $4096^4$ against $6561^4$.

**Count by divisor structure.** The number of divisors depends only on the exponent pattern: exactly $6$ divisors means $p^5$ or $p^2q$; exactly $8$ means $p^7$, $p^3q$ or $pqr$ (distinct primes). List each pattern systematically. Counting $r\times c$ rectangle layouts of $N$ objects is counting divisors of $N$.

> **Tip:** For a counterexample, the value must satisfy the hypothesis and break the conclusion. Look for the value where the expression visibly factorises.

## Traps

> **Trap:** Adding percentages. $+25\%$ then $-20\%$ is no change; $+50\%$ length with $+25\%$ diameter in $R\propto L/d^2$ is $\frac{1.5}{1.5625}=0.96$, a $4\%$ decrease.

> **Trap:** Area conversions. $50\text{ cm}^2=0.005\text{ m}^2$, not $0.5$ or $0.05$.

> **Trap:** Bounds with a difference: the smallest $t_2-t_1$ uses the **lower** bound of $t_2$ and the **upper** bound of $t_1$.

> **Trap:** Getting the power wrong when passing from $n^k$ to $n$: $p^a\mid n^k$ gives $p^{\lceil a/k\rceil}\mid n$. So $2^3\mid n^2$ gives $4\mid n$, but $2^2\mid n^3$ gives only $2\mid n$.

* Off-by-one errors in "after how many years" questions: check the values either side of the crossing.
* "Different", "positive" and "ordered" change counts by factors of $2$.

## Worked examples

**Example 1.** Two positive integers have HCF $4$ and LCM $240$. How many unordered pairs are possible?

<details><summary>Show solution</summary>

Write them as $4p$, $4q$ with $p,q$ coprime and $pq=60=2^2\cdot3\cdot5$. Each prime power ($4$, $3$, $5$) goes wholly to $p$ or to $q$: $2^3=8$ ordered splits, so $4$ unordered pairs.

</details>

**Example 2.** A length is $8.0$ cm to 1 d.p. and a width is $2.6$ cm to 1 d.p. Find the upper bound of $\frac{\text{length}}{\text{width}}$.

<details><summary>Show solution</summary>

Maximise the numerator and minimise the denominator: $\frac{8.05}{2.55}=\frac{161}{51}\approx3.16$.

</details>

**Example 3.** A savings account adds $10\%$ interest each year, then £$300$ is withdrawn. It starts at £$2000$. Find a formula for the balance after $n$ years.

<details><summary>Show solution</summary>

$u_{n+1}=1.1u_n-300$. Fixed point $L=1.1L-300\Rightarrow L=3000$. Then $u_n-3000=(2000-3000)\times1.1^n$, so $u_n=3000-1000\times1.1^n$. The balance falls, reaching zero when $1.1^n=3$, i.e. during year $12$ ($1.1^{11}\approx2.85$, $1.1^{12}\approx3.14$).

</details>

**Example 4.** Write $0.2\dot{7}$ as a fraction.

<details><summary>Show solution</summary>

$x=0.2777\ldots$: $10x=2.777\ldots$ and $100x=27.777\ldots$, so $90x=25$ and $x=\frac{25}{90}=\frac5{18}$.

</details>
