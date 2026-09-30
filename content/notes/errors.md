# Finding errors in proofs

Paper 2 regularly shows an argument laid out as numbered lines (I), (II), … and asks "In which line does the first error occur?" or "Which one of the following best describes the proof?". Your job is to test each line against the lines before it, not to judge the final answer. Often the answer is "the proof is correct", and sometimes the conclusion is true even though the reasoning is broken.

## Must-know facts

A line is an error if it does **not follow** from the assumptions and earlier lines. It does not matter whether the line happens to be true, and a false-looking line may be fine inside a proof by contradiction.

The classic errors:

- **Dividing by something that may be zero.** $x(x-2)=3x\Rightarrow x-2=3$ loses $x=0$.
- **Squaring both sides of an equation.** Valid as an implication, but not reversible: it can create extra roots, so candidates must be checked.
- **Squaring an inequality.** Valid only when both sides are known to be non-negative.
- **Taking square roots.** $\sqrt{x^2}=|x|$, so $x^2=y^2$ only gives $x=\pm y$.
- **Multiplying or dividing an inequality by an expression of unknown sign.** The inequality flips when the expression is negative.
- **Misused laws.** $\log(a+b)\ne\log a+\log b$; $(a^m)^n=a^{mn}$ with fractional powers needs $a>0$; $\sqrt{a+b}\ne\sqrt a+\sqrt b$.
- **Proving the converse.** Assuming the conclusion and deriving the hypothesis proves "if $Q$ then $P$", not "if $P$ then $Q$".
- **Assuming what is to be proved.** Starting from the claim and reaching something true proves nothing, unless every step is reversible.
- **Missing cases.** A proof by cases that omits a residue, a sign, or a boundary case is incomplete.
- **Special case only.** "Without loss of generality" that actually loses generality, or an unjustified "$a+b\ge0$".
- **Treating something undefined as a number.** For example $S=1+2+4+\cdots$, which has no sum.
- **Illegitimate divisibility steps.** $k\mid n^2\Rightarrow k\mid n$ is true for prime $k$, false for $k=4,8,12,\dots$

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

Line (I) divides by $x$, which could be $0$. Correctly, $x^2-4x=0\Rightarrow x(x-4)=0$, so $x=0$ or $x=4$. The first error is in (I); the root $x=0$ is lost. (Line (II) is also false, but it follows from (I), so it is not the *first* error.)

</details>

**Example 2.** Claim: if $a>b$ then $a^2>b^2$. Proof: (I) $a>b$. (II) Multiplying by $a$: $a^2>ab$. (III) Multiplying $a>b$ by $b$: $ab>b^2$. (IV) So $a^2>ab>b^2$. Evaluate.

<details><summary>Show solution</summary>

(II) multiplies an inequality by $a$, valid only if $a>0$; (III) needs $b>0$. So the first error is (II). The claim is false: $a=1,b=-2$ gives $1<4$.

If the claim were "if $a>b>0$ then $a^2>b^2$", exactly the same proof would be correct, since then both $a$ and $b$ are positive.

</details>

**Example 3.** Claim: $\sqrt 8$ is irrational. Proof: suppose $\sqrt8=\frac pq$ in lowest terms; then $p^2=8q^2$, so $8\mid p^2$, hence $8\mid p$; … so $8\mid q$, contradiction. Evaluate.

<details><summary>Show solution</summary>

"$8\mid p^2\Rightarrow 8\mid p$" is false ($p=4$: $8\mid16$ but $8\nmid4$). So the proof is invalid at that step. The claim is still true: use $2\mid p^2\Rightarrow2\mid p$ with the prime $2$, then $p=2r$ gives $4r^2=8q^2$, $r^2=2q^2$, so $r$ is even; $r=2s$ gives $q^2=2s^2$, so $q$ is even too, contradicting lowest terms. True conclusion, invalid reasoning.

</details>
