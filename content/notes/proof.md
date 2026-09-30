# Mathematical proof

Paper 2 tests whether you can recognise, build and judge proofs rather than grind algebra. Expect: picking a counterexample, stating what a proof by contradiction assumes, choosing the step or order that completes a proof, deciding which of several arguments is valid, and parity/divisibility arguments. The maths is rarely beyond GCSE; the difficulty is in the logic.

## Must-know facts

- **Counterexample.** To disprove "for all $x$, if $P(x)$ then $Q(x)$", you need one $x$ with $P(x)$ true **and** $Q(x)$ false. A value where $P$ is false is not a counterexample.
- **Negations.** Not (for all $x$, $P$) = there is an $x$ with not $P$. Not (if $P$ then $Q$) = $P$ and not $Q$. Not ($A$ or $B$) = not $A$ and not $B$.
- **Contrapositive.** "If $P$ then $Q$" is equivalent to "if not $Q$ then not $P$". The **converse** "if $Q$ then $P$" is a different statement.
- **Quantifier order matters.** "For every $x$ there is a $y$ with $y>x$" is true; "there is a $y$ such that for every $x$, $y>x$" is false. In the first, $y$ may depend on $x$.
- **Standard divisibility facts.** Among $k$ consecutive integers one is divisible by $k$; so $n(n+1)$ is even and $(n-1)n(n+1)$ is divisible by $6$. If coprime $a,b$ both divide $N$, then $ab\mid N$.
- **Squares mod small numbers.** mod 3: $0,1$. mod 4: $0,1$. mod 8 (odd squares): $1$. mod 5: $0,1,4$.
- **Prime divisibility.** If a prime $p$ divides $ab$ then $p\mid a$ or $p\mid b$; in particular $p\mid n^2\Rightarrow p\mid n$. This fails for composite $p$ with a repeated factor ($12\mid 36$ but $12\nmid 6$).

## Techniques

**Direct proof.** Start from what you know and move forwards. For "odd $\times$ odd is odd", write $n=2a+1$, $m=2b+1$ and expand. Use *different* letters for different unknowns.

**Proof by contradiction.** Assume the negation of the statement and derive something impossible. For irrationality: assume $\sqrt k=\frac pq$ in lowest terms and find a common factor. For "infinitely many": assume a complete finite list and build something outside it.

**Contrapositive.** When the hypothesis is awkward ("if $n^2$ is even") prove "if $n$ is odd then $n^2$ is odd" instead.

**Proof by cases / exhaustion.** Split into finitely many cases that cover everything: parity, residues mod $m$, sign of $x$. The cases must be exhaustive; missing one breaks the proof.

**Finding counterexamples fast.**

- Try small values, $0$, $1$, negatives, and a fraction between $0$ and $1$.
- For "is prime for all $n$", choose $n$ that makes the expression factorise (e.g. $n=41$ or $40$ in $n^2+n+41$).
- For "divisible by $k$", try $n=2$ first.

**Judging a "proof".** Read each line and ask: does this follow from the assumptions and earlier lines alone? A valid line may use only what has already been established.

> **Key idea:** A proof must run from what is known to what is claimed. Deducing something true *from* the claim proves nothing.

## Traps

> **Trap:** Choosing a value that makes the hypothesis false as a "counterexample". For "if $n$ is odd then …", even $n$ are irrelevant.

> **Trap:** Negating "if $P$ then $Q$" as "if $P$ then not $Q$" or "not $P$ and not $Q$". It is "$P$ and not $Q$".

> **Trap:** Checking several cases and declaring the result proved. Examples support a conjecture; only a general argument (or an exhaustive check of finitely many cases) proves it.

> **Trap:** Thinking Euclid's number $p_1\cdots p_n+1$ is always prime. $2\cdot3\cdot5\cdot7\cdot11\cdot13+1=30031=59\times509$. What is guaranteed is a *new prime factor*.

> **Tip:** In "which of I, II, III" questions, hunt for a quick counterexample to each statement before trying to prove any of them. A single counterexample removes several options at once.

## Worked examples

**Example 1.** Which of these are true for every integer $n$? I: $n^2-n$ is even. II: $n^4-1$ is divisible by $5$. III: $n^2+1$ is never divisible by $3$.

<details><summary>Show solution</summary>

I: $n^2-n=n(n-1)$, two consecutive integers, so even. True.

II: $n=5$ gives $624$, not divisible by $5$. False (it holds only when $5\nmid n$).

III: squares mod 3 are $0$ or $1$, so $n^2+1\equiv1$ or $2\pmod 3$. True.

Answer: I and III only.

</details>

**Example 2.** A proof by contradiction that $\log_2 3$ is irrational begins "Suppose $\log_2 3=\frac pq$ with $p,q$ positive integers." Complete it.

<details><summary>Show solution</summary>

Then $2^{p/q}=3$, so $2^p=3^q$. The left side is even (since $p\ge1$) and the right side is odd: contradiction. Hence $\log_2 3$ is irrational.

Note the assumption $p,q>0$ is justified because $\log_2 3>0$. Lowest terms are not needed here: parity alone gives the contradiction.

</details>

**Example 3.** Find the smallest $N$ such that checking $N$, $N+1$ and $N+2$, together with "if $n=3a+5b$ then $n+3=3(a+1)+5b$", proves that every $n\ge N$ is of the form $3a+5b$ ($a,b\ge0$).

<details><summary>Show solution</summary>

Non-representable numbers are $1,2,4,7$. We need three consecutive representable values to start from: $8=3+5$, $9=3\cdot3$, $10=5\cdot2$. So $N=8$. Any $N\le7$ includes $7$ among the base cases, which fails.

</details>
