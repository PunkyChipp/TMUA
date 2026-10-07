# Finding errors in proofs

Paper 2 regularly shows an argument laid out as numbered lines (I), (II), … and asks "In which line does the first error occur?" or "Which one of the following best describes the proof?". Your job is to test each line against the lines before it, not to judge the final answer. Often the answer is "the proof is correct", and sometimes the conclusion is true even though the reasoning is broken.

## Must-know facts

A line is an error if it does **not follow** from the assumptions and earlier lines. It does not matter whether the line happens to be true, and a false-looking line may be fine inside a proof by contradiction.

The classic errors:

The two errors named in the specification:

- **"If $ab=ac$ then $b=c$."** Valid only when $a\ne0$. Cancelling a factor that might be zero is division by zero: from $x(x-2)=3x$ you may not conclude $x-2=3$, which loses $x=0$. Factorise instead: $x(x-5)=0$.
- **"If $\sin A=\sin B$ then $A=B$."** False: $\sin A=\sin B$ also when $A=180^\circ-B$ (and when angles differ by $360^\circ$). In a triangle this is the ambiguous case of the sine rule: $\sin B=\frac{\sqrt3}2$ allows $B=60^\circ$ or $120^\circ$. Similarly $\sin2A=\sin2B$ allows $A+B=90^\circ$, a right angle at $C$.

Other classic errors:

- **Squaring both sides of an equation.** Valid as a step forwards, but not reversible: it can create extra roots, so candidates must be checked.
- **Squaring an inequality.** Valid only when both sides are known to be non-negative.
- **Taking square roots and losing $\pm$.** $\sqrt{x^2}=|x|$, so $A^2=B^2$ only gives $A=B$ or $A=-B$; similarly $\sin^2A=\cos^2B$ gives $\sin A=\pm\cos B$.
- **Multiplying or dividing an inequality by an expression of unknown sign.** The inequality flips when the expression is negative.
- **Misused laws.** $\log(a+b)\ne\log a+\log b$; $\sqrt{a+b}\ne\sqrt a+\sqrt b$.
- **Proving the converse.** Assuming the conclusion and deriving the hypothesis proves "if $Q$ then $P$", not "if $P$ then $Q$".
- **Circular reasoning.** Starting from the claim and reaching something true proves nothing. It can be repaired only if every step reverses (adding terms reverses; multiplying by $x$ of unknown sign does not).
- **Checking only examples.** Examples never prove a "for every" statement about infinitely many cases. But checking **all** cases of a finite statement is a proof, and one example does prove a "there exists" statement or disprove a "for every" statement.
- **Missing cases.** A proof by cases that omits a remainder, a sign or a boundary case is incomplete, and the missing case may be exactly where the claim fails.
- **Special case only.** "Without loss of generality" that actually loses generality (the symmetry must leave the whole statement unchanged), or an unjustified "$a+b\ge0$".
- **Treating something undefined as a number.** For example $S=1+2+4+\cdots$, which has no sum.
- **Illegitimate divisibility steps.** "$k$ divides $n^2$, so $k$ divides $n$" is true for prime $k$, false for $k=4,8,12,\dots$

## Techniques

**Go line by line.** For each line ask: "Given only what came before, must this be true?" Stop at the first "no". Later lines may also be wrong, but questions ask for the *first* error.

**Test a specific value.** Put a number into the line in question. If the earlier lines hold for that number and this line fails, you have found the error. Negative numbers, $0$ and $1$ are the best tests.

**Separate "claim true?" from "proof valid?".** Many options read "incorrect, and the claim is false" versus "incorrect, but the claim is true". Decide these separately: find the faulty line, then look for a counterexample to the claim.

**Identify the structure.** Is the argument direct, contrapositive, contradiction or cases? Check it proves the right statement (not the converse) and that contradiction arguments negate correctly.

> **Key idea:** Judge each line by whether it follows, not by whether it is true. Inside a proof by contradiction you expect to deduce false things; that is the point.

## Traps

> **Trap:** Blaming the squaring line in an equation. Squaring is a valid step forwards; the error is usually the later line that claims all candidates are solutions.

> **Trap:** Declaring a proof wrong because its conclusion is surprising, or right because its conclusion is true. A correct conclusion can come from bad reasoning (e.g. proving the converse of a true statement).

> **Trap:** Rejecting a correct proof because it looks too short. Contrapositive proofs and clean factorisations often are short. Expect at least one "the proof is correct" per paper.

> **Tip:** When the options pair the same line with different reasons, the reason matters: "divides by zero" versus "loses a negative case" can both point at the same line, and only one is right.

## Worked examples

**Example 1.** A student solves $x^2=4x$: (I) divide by $x$: $x=4$. (II) So the only solution is $x=4$. Which line contains the first error, and what is lost?

<details><summary>Show solution</summary>

Line (I) divides by $x$, which could be $0$. Correctly, $x^2-4x=0$ gives $x(x-4)=0$, so $x=0$ or $x=4$. The first error is in (I); the root $x=0$ is lost. (Line (II) is also false, but it follows from (I), so it is not the *first* error.)

</details>

**Example 2.** Claim: if $a>b$ then $a^2>b^2$. Proof: (I) $a>b$. (II) Multiplying by $a$: $a^2>ab$. (III) Multiplying $a>b$ by $b$: $ab>b^2$. (IV) So $a^2>ab>b^2$. Evaluate.

<details><summary>Show solution</summary>

(II) multiplies an inequality by $a$, valid only if $a>0$; (III) needs $b>0$. So the first error is (II). The claim is false: $a=1,b=-2$ gives $1<4$.

If the claim were "if $a>b>0$ then $a^2>b^2$", exactly the same proof would be correct, since then both $a$ and $b$ are positive.

</details>

**Example 3.** Claim: $\sqrt 8$ is irrational. Proof: suppose $\sqrt8=\frac pq$ in lowest terms; then $p^2=8q^2$, so $8\mid p^2$, hence $8\mid p$; … so $8\mid q$, contradiction. Evaluate.

<details><summary>Show solution</summary>

"$8$ divides $p^2$, so $8$ divides $p$" is false ($p=4$: $8\mid16$ but $8\nmid4$). So the proof is invalid at that step. The claim is still true: use the prime $2$ ($2\mid p^2$ gives $2\mid p$), then $p=2r$ gives $4r^2=8q^2$, $r^2=2q^2$, so $r$ is even; $r=2s$ gives $q^2=2s^2$, so $q$ is even too, contradicting lowest terms. True conclusion, invalid reasoning.

</details>
