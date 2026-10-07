# Logic of arguments

Paper 2 tests logic in several questions every sitting. The maths is rarely hard: the difficulty is reading precisely. Expect to rewrite English as "if ..., then ...", decide whether a condition is necessary or sufficient (heavily examined since 2024), negate statements containing "every", "some" and "at most", compare nested "for every ... there is ..." statements, and decide what must, could or cannot be true. Everything in the exam is written in words. You are **not** expected to use logic symbols or fill in formal truth tables; the symbols at the end of these notes are optional shorthand.

## Must-know facts

**True and false; and, or, not.** "A and B" is true only when both are true. In mathematics "A or B" is **inclusive**: true when at least one is true, including both. "Not A" is true exactly when A is false.

**"If A, then B" is false in exactly one situation: A true and B false.** When A is false the statement makes no promise, so it counts as true. "Every member who swims also runs" is true in a club with no swimmers.

**Four ways to say the same thing:**

* if A, then B
* B if A
* A only if B
* A is sufficient for B, and B is necessary for A

"A only if B" means A cannot happen without B. "You may board only if you have a ticket" does not promise that every ticket-holder boards.

**"A if and only if B"** means both "if A, then B" and "if B, then A": A is necessary and sufficient for B.

**Converse and contrapositive of "if A, then B":**

* converse: "if B, then A". It may be true or false, independently of the original.
* contrapositive: "if not B, then not A". It is **always** true exactly when the original is true.
* Negating both parts without swapping ("if not A, then not B") is the contrapositive of the converse, so it behaves like the converse.

So a statement and its contrapositive stand or fall together; the converse must be checked separately.

**The negation of "if A, then B"** is not another "if" statement: it is "A and not B".

**Negating and/or.** "Not (A and B)" is "not A, or not B". "Not (A or B)" is "not A and not B" (neither). So the negation of "$1 < x < 3$" is "$x \le 1$ or $x \ge 3$".

**"Unless".** Questions define it; usually "A unless B" means "if not B, then A". "No refund unless you have the receipt" means "if no receipt, then no refund", i.e. "refund only if receipt".

## Necessary and sufficient

* "C is **sufficient** for P": whenever C holds, P holds.
* "C is **necessary** for P": whenever P holds, C holds (P cannot happen without C).

Think in sets. Find the **exact** set where P holds first. A sufficient condition is a set inside it; a necessary condition is a set containing it; a condition that is the same set is both.

Examples to know:

* Reals: $x^2-4x+3<0$ exactly when $1<x<3$. Then $x>0$ is necessary only; $1<x<2$ is sufficient only; $|x-2|<1$ is both.
* Integers: "divisible by $3$ and by $4$" is necessary and sufficient for divisibility by $12$; "divisible by $2$ and by $6$" is only necessary (combine using the lowest common multiple).
* Polynomials: for $x^2+bx+c=0$, two distinct real roots exactly when $b^2>4c$; $c<0$ is sufficient, not necessary.
* Functions: $x^3+ax$ is strictly increasing exactly when $a\ge 0$; $a\ge -1$ is necessary only.
* Geometry: every property of a square is necessary for being a square; "equal perpendicular diagonals" is not sufficient (a kite can have them).

To prove "not sufficient", find an example with C true and P false. To prove "not necessary", find an example with P true and C false.

## For every, for some, there exists

"Some" means **at least one** (possibly all). "There exists" means the same. "Every", "each", "all" and "any" (as in "any $x$ satisfies ...") mean for all.

**Order matters.** "For every $x$ there is a $y$ with ..." lets $y$ depend on $x$. "There is a $y$ such that for every $x$ ..." needs one single $y$ that works for all $x$, which is much stronger. "Every lock has a key that opens it" is not "there is a key that opens every lock".

**Negating quantified statements.** Swap "every" and "some", in order, and negate only the final condition:

* not (every card is red) = some card is not red
* not (some player scored in every match) = every player failed to score in at least one match
* not (at most one is positive) = at least two are positive
* not (for every $\varepsilon$ there is an $N$ such that for all $n>N$, $|a_n|<\varepsilon$) = there is an $\varepsilon$ such that for every $N$, some $n>N$ has $|a_n|\ge\varepsilon$

## Techniques

1. **Rewrite everything as "if ..., then ...".** Turn "only if", "if", "unless", "necessary", "sufficient" and "whenever" into the same form before comparing.
2. **Ask when it is false.** Each "if" statement rules out exactly one situation. Two statements are equivalent when they rule out the same situations.
3. **Must / could / cannot.** "Must be true": try to build a situation where all the facts hold and the option fails. "Could be true": build one small example where everything holds. "Cannot be true": chain the facts to show the option contradicts them.
4. **Name the witness.** From "some violinists sing", call one of them $M$ and push $M$ through every other fact.
5. **Chains.** "If A then B" and "if B then C" give "if A then C". Follow arrows forwards, or use the contrapositive; never go backwards.
6. **Counterexamples** to "for every $n$, if P then Q" must satisfy P and fail Q.
7. **Lazy witnesses** for "there exists": try $0$, $1$, or the same variable again.
8. **Self-referential puzzles**: find two statements that control each other, split into cases, and check every statement in the surviving case.

## Traps

> **Trap:** Reading "only if" backwards. "A only if B" is "if A, then B".

> **Trap:** Swapping necessary and sufficient. The necessary condition is the one that **follows**: $x^2>4$ is necessary, not sufficient, for $x>2$.

> **Trap:** Trusting the converse. "If $x^2>9$ then $x>3$" is false ($x=-4$) though its converse is true.

> **Trap:** Negating "all" to "none". The negation of "all cards are red" is "at least one card is not red".

> **Trap:** Negating "or" to "not both". The negation of "a cake or a drink" is "neither a cake nor a drink".

> **Trap:** Forgetting vacuous truth. "Every under-16 member swims" is true if there are no under-16 members.

> **Tip:** In "Which of I, II, III" questions, settle the easiest statement first and cross out options.

> **Key idea:** Almost every logic question reduces to: in which situations is this statement false?

## Optional shorthand

Some books write "if A then B" as $A \Rightarrow B$, "if and only if" as $\iff$, "and" as $\wedge$, "or" as $\vee$, "not" as $\neg$, "for all" as $\forall$ and "there exists" as $\exists$. You never need these in the exam; use them only if they help you write quickly.

## Worked examples

**Example 1.** "Every member who plays chess also plays bridge" is true. Which must be true? (a) Every bridge player plays chess. (b) Every member who does not play bridge does not play chess. (c) Some member plays chess.

<details><summary>Show solution</summary>

The statement is: if a member plays chess, then they play bridge.

* (a) is the converse. A member who plays only bridge is allowed.
* (b) is the contrapositive. **Must be true.**
* (c) fails if nobody plays chess: the statement is then true with nothing to check.

Only (b).
</details>

**Example 2.** For real $x$, is "$x^3>x$" necessary, sufficient, both or neither for "$x>1$"?

<details><summary>Show solution</summary>

Exact set: $x(x-1)(x+1)>0$ for $-1<x<0$ or $x>1$.

* Every $x>1$ is in this set, so $x^3>x$ is **necessary** for $x>1$.
* $x=-\tfrac12$ gives $-\tfrac18>-\tfrac12$ but $x$ is not greater than $1$, so it is **not sufficient**.

Necessary but not sufficient.
</details>

**Example 3.** Negate: "For every real $M$ there is a real $x$ such that $f(x)>M$."

<details><summary>Show solution</summary>

Swap each quantifier in order and negate the end: "There is a real $M$ such that for every real $x$, $f(x)\le M$." In words: $f$ is bounded above, which is indeed the opposite of "$f$ takes arbitrarily large values".
</details>
