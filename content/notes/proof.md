# Mathematical proof

Paper 2 tests whether you can follow, build and judge proofs, not grind algebra. The specification lists: direct proof, proof by cases, proof by contradiction and disproof by counterexample (Prf1); deducing what follows from given statements (Prf2); making a conjecture from small cases and then justifying it (Prf3); putting the lines of a proof in the right order (Prf4); and problems needing a longer chain of reasoning (Prf5). Everything is in words: you will not be asked to use logic symbols or truth tables.

## Must-know facts

- **Counterexample.** To disprove "for every $x$, if $P(x)$ then $Q(x)$", you need one $x$ for which $P(x)$ is true **and** $Q(x)$ is false. A value where $P$ is false is not a counterexample.
- **Negations.** Not "for every $x$, $P$" is "there is an $x$ with not $P$". Not "there are no $x$ with $P$" is "there is an $x$ with $P$". Not "if $P$ then $Q$" is "$P$ and not $Q$". Not "$A$ or $B$" is "not $A$ and not $B$".
- **Contrapositive.** "If $P$ then $Q$" is equivalent to "if not $Q$ then not $P$". The **converse**, "if $Q$ then $P$", is a different statement.
- **"$A$ only if $B$"** means "if $A$ then $B$".
- **Divisibility.** Among $k$ consecutive integers one is divisible by $k$; so $n(n+1)$ is even and $(n-1)n(n+1)$ is divisible by $6$. Two consecutive even numbers include a multiple of $4$, so their product is a multiple of $8$. If $a$ and $b$ have no common factor and both divide $N$, then $ab$ divides $N$.
- **Squares and remainders.** On division by $3$: $0,1$. By $4$: $0,1$. By $5$: $0,1,4$. By $7$: $0,1,2,4$. Odd squares leave remainder $1$ on division by $8$.
- **Primes.** If a prime $p$ divides $ab$ then $p$ divides $a$ or $b$; so if $p$ divides $n^2$ then $p$ divides $n$. This fails for divisors with a repeated factor: $12$ divides $36$ but not $6$.

## Techniques

**Direct proof.** Start from what you know and move forwards. For "odd times odd is odd", write $2a+1$, $2b+1$ and expand. Use different letters for different unknowns.

**Proof by cases.** Split into finitely many cases that cover everything: parity, remainders on division by $m$, sign of $x$. Every case must be handled.

**Proof by contradiction.** Assume the negation and derive something impossible. Know both parts: *what is assumed* (for "there are no integers with …", assume there **are** some) and *what the contradiction is* (two facts about the same object that cannot both hold, such as "$a^2$ is a multiple of $4$" and "$a^2=4b+2$").

**Deducing from given statements (Prf2).** Chain "every" statements forwards, and use their contrapositives backwards. "Every" statements never create objects; only "at least one" statements do. To show something is **not** forced, build a small situation where all the given facts hold and it fails.

**Conjecture, then justify (Prf3).** Several patterns can fit the first few cases ($n(n+1)(n+2)(n+3)+1$ gives $5^2,11^2,19^2,29^2$: squares of primes for $n\le5$, but $n=6$ gives $55^2$). Test each candidate a little beyond the data, then look for an identity or a case split that proves the survivor. A list of checked cases is never a proof of a "for every" statement.

**Ordering a proof (Prf4).** For each line ask what it uses. A line may only use the assumption and lines above it. The line that introduces the letters comes first; the contradiction or conclusion comes last.

**Invariants (Prf5).** In process or game questions, look for something a move cannot change, such as the parity of a total. It rules outcomes out; then construct examples for the outcomes that remain.

> **Key idea:** A proof must run from what is known to what is claimed. Deducing something true *from* the claim proves nothing.

## Traps

> **Trap:** Choosing a value that makes the hypothesis false as a "counterexample". For "if $n$ is prime then …", non-primes are irrelevant.

> **Trap:** Negating "there are no $a,b$ with …" as "for every $a,b$ …". The correct negation is "there are some $a,b$ with …".

> **Trap:** Testing one example inside a proof by contradiction. The assumed object is unknown; you must argue about it in general.

> **Trap:** Thinking Euclid's number $p_1\cdots p_n+1$ is always prime. $2\cdot3\cdot5\cdot7\cdot11\cdot13+1=30031=59\times509$. What is guaranteed is a *new prime factor*.

> **Tip:** In "which of I, II, III" questions, hunt for a quick counterexample to each statement before trying to prove any of them. Always try the smallest allowed value: $n^4+4$ is composite for $n\ge2$ but equals $5$ at $n=1$.

## Worked examples

**Example 1.** Which of these are true for every integer $n$? I: $n^2-n$ is even. II: $n^4-1$ is divisible by $5$. III: $n^2+1$ is never divisible by $3$.

<details><summary>Show solution</summary>

I: $n^2-n=n(n-1)$, two consecutive integers, so even. True.

II: $n=5$ gives $624$, not divisible by $5$. False (it holds only when $5$ does not divide $n$).

III: squares leave remainder $0$ or $1$ on division by $3$, so $n^2+1$ leaves $1$ or $2$. True.

Answer: I and III only.

</details>

**Example 2.** Facts: every member who plays chess plays go; no member who plays go plays tennis; at least one member plays tennis. Must some member not play chess?

<details><summary>Show solution</summary>

Take the tennis player. They do not play go (second fact), so by the contrapositive of the first fact they do not play chess. Yes, it must be true. Note that "some member plays go" is **not** forced: a club of tennis players only satisfies all three facts.

</details>

**Example 3.** Find the smallest $N$ such that checking $N$, $N+1$, $N+2$, together with "if $n=3a+5b$ then $n+3=3(a+1)+5b$", proves that every $n\ge N$ is of the form $3a+5b$ ($a,b\ge0$).

<details><summary>Show solution</summary>

The amounts that cannot be made are $1,2,4,7$. We need three consecutive amounts that can be made: $8=3+5$, $9=3\cdot3$, $10=5\cdot2$. So $N=8$. Any $N\le7$ has a failing base case.

</details>
