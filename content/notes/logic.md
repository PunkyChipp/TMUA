# Logic of arguments

Paper 2 tests logic in almost every sitting, usually in several questions. It is rarely hard maths:
the difficulty is reading precisely. Expect to translate English into "if … then …", decide what is
necessary or sufficient, negate statements with "all/some/at most", compare nested quantifiers,
and pick which of several statements must be true. Marks are lost through misreading, not through
lack of knowledge, so the aim is a reliable, mechanical method.

## Must-know facts

**Implication.** "If $P$ then $Q$" ($P \Rightarrow Q$) is false in exactly one case: $P$ true and $Q$ false.
If $P$ is false the implication is (vacuously) true. So $P \Rightarrow Q \equiv \neg P \lor Q$.

| $P$ | $Q$ | $P \land Q$ | $P \lor Q$ | $P \Rightarrow Q$ | $P \Leftrightarrow Q$ |
|---|---|---|---|---|---|
| T | T | T | T | T | T |
| T | F | F | T | **F** | F |
| F | T | F | T | T | F |
| F | F | F | F | T | T |

**Same meaning as $P \Rightarrow Q$:**

* if $P$, then $Q$; $\;Q$ if $P$; $\;P$ only if $Q$; $\;Q$ whenever $P$
* $P$ is sufficient for $Q$; $\;Q$ is necessary for $P$
* not $Q \Rightarrow$ not $P$ (the **contrapositive**)
* not $P$ or $Q$

**Relatives of $P \Rightarrow Q$:**

| name | form | equivalent to original? |
|---|---|---|
| converse | $Q \Rightarrow P$ | no |
| inverse | $\neg P \Rightarrow \neg Q$ | no (it is the contrapositive of the converse) |
| contrapositive | $\neg Q \Rightarrow \neg P$ | **yes** |
| negation | $P \land \neg Q$ | opposite truth value |

The negation of an implication is **not** another implication: "not (if $P$ then $Q$)" means "$P$ and not $Q$".

**"If and only if".** $P \Leftrightarrow Q$ means both $P \Rightarrow Q$ and $Q \Rightarrow P$: $P$ is necessary and sufficient for $Q$.

**"Unless".** "$A$ unless $B$" means "if not $B$ then $A$", which is the same as "$A$ or $B$".
"You will fail unless you revise" says nothing about what happens if you do revise.

**Necessary and sufficient.** "$A$ is sufficient for $B$" means $A \Rightarrow B$; "$A$ is necessary for $B$" means $B \Rightarrow A$.
Think in sets: if $S_A$ and $S_B$ are the sets where $A$ and $B$ hold, sufficient means $S_A \subseteq S_B$ and necessary means $S_B \subseteq S_A$.
For real $x$: $x > 2$ is sufficient for $x^2 > 4$, and $x^2 > 4$ is necessary for $x > 2$.

**De Morgan.** $\neg(P \land Q) \equiv \neg P \lor \neg Q$ and $\neg(P \lor Q) \equiv \neg P \land \neg Q$.
So the negation of $a < x < b$ is $x \le a$ **or** $x \ge b$.

**Quantifiers.** Negation flips each quantifier and negates the property:

* not (all $x$ have $P$) $\equiv$ some $x$ does not have $P$
* not (some $x$ has $P$) $\equiv$ no $x$ has $P$ $\equiv$ every $x$ fails $P$
* not (at most $k$) $\equiv$ at least $k+1$; not (at least $k$) $\equiv$ at most $k-1$
* "every", "each", "any" (in "any $x$ satisfies …") mean $\forall$; "some", "there exists", "at least one" mean $\exists$

**Nested quantifiers.** Order matters.

* $\forall x\ \exists y$: for each $x$ you may choose a different $y$ ($y$ can depend on $x$).
* $\exists y\ \forall x$: one single $y$ must work for every $x$. This is much stronger.

"Every lock has a key that opens it" is not "there is a key that opens every lock".
To negate, flip every quantifier in order, then negate the inside:
$$\neg(\forall x\ \exists y\ P(x,y)) \equiv \exists x\ \forall y\ \neg P(x,y).$$

## Techniques

1. **Translate to symbols first.** Name each simple statement ($P$ = "passed", $A$ = "attended every lecture"), rewrite everything as $\Rightarrow$, $\land$, $\lor$, $\neg$. Most traps disappear once "only if" and "unless" are rewritten.
2. **Rewrite implications as ORs** when checking equivalence: $P \Rightarrow Q \equiv \neg P \lor Q$. Two formulas are equivalent if their OR/AND forms match, e.g. $(P \land Q) \Rightarrow R \equiv \neg P \lor \neg Q \lor R \equiv P \Rightarrow (Q \Rightarrow R)$.
3. **Hunt for the single false row.** An implication is broken only by "hypothesis true, conclusion false". To test "must this be true?", try to build a situation where all the given statements hold and the candidate fails. If you can, it need not be true.
4. **Counterexamples.** A counterexample to "for all $x$, if $P(x)$ then $Q(x)$" must satisfy $P$ and fail $Q$. An $x$ that fails $P$ proves nothing.
5. **Necessary/sufficient questions: find the exact condition first.** Work out precisely when $B$ holds (e.g. "$f$ strictly increasing $\iff a \ge 0$"). Then sufficient conditions are subsets of that set and necessary conditions are supersets.
6. **"Must be true" with quantifiers: name a witness.** From "some violinists sing", call one of them $m$ and ask what the other statements force about $m$. Remember a universal statement can be vacuously true (nobody passed, so "every student who passed …" says nothing).
7. **Lazy witnesses.** For "there exists" claims, try $0$, $1$, $-1$, or the same variable again before anything clever: "for every integer $a$ there is $b$ with $a^2 + b^2$ a square" is true with $b = 0$.
8. **Truth tables for small counts.** With three statements there are only $8$ rows; counting rows is often faster than algebra. For "how many rows make $X \Rightarrow R$ false?", count rows with $X$ true and $R$ false.
9. **Self-referential puzzles.** Find two statements that contradict each other directly (e.g. "statement 3 is false"), split into the two cases, and check the final assignment against every statement.

## Traps

> **Trap:** Confusing the converse with the contrapositive. "If $n$ is divisible by $6$ then by $3$" is true; its converse ("divisible by $3$ then by $6$") is false. Only the contrapositive is guaranteed.

> **Trap:** Reading "only if" backwards. "$P$ only if $Q$" is $P \Rightarrow Q$, not $Q \Rightarrow P$. "You may enter only if you have a ticket" does not promise entry to ticket-holders.

> **Trap:** Swapping necessary and sufficient. The necessary condition is the one that is **implied**. $x^2 > 4$ is necessary, not sufficient, for $x > 2$.

> **Trap:** Negating "all" to "none". The negation of "all cards are red" is "at least one card is not red", not "no card is red".

> **Trap:** Forgetting the extreme cases when negating counts. "At most one is positive" negates to "at least two", which includes all three.

> **Trap:** Negating $a < x < b$ as "$x \le a$ and $x \ge b$". It must be **or**.

> **Trap:** Assuming $(P \Rightarrow R) \land (Q \Rightarrow R)$ is equivalent to $(P \land Q) \Rightarrow R$. It is actually $(P \lor Q) \Rightarrow R$.

> **Trap:** Treating a vacuous universal as giving information. "Every student who passed attended every lecture" is true when nobody passed, so it cannot tell you someone passed.

> **Tip:** In "Which of I, II, III …" questions, settle the easiest statement first and cross out options. If I is clearly false, half the options go at once.

> **Key idea:** Every logic question reduces to one question: in which situations is this statement false? Find those situations and the answer usually follows.

## Worked examples

**Example 1.** In a club, "Every member who plays chess also plays bridge" is true. Which must be true?
(a) Every bridge player plays chess. (b) Every member who does not play bridge does not play chess. (c) Some member plays chess.

<details><summary>Show solution</summary>

Write the statement as chess $\Rightarrow$ bridge.

* (a) is the converse. A member who plays only bridge is allowed, so (a) need not hold.
* (b) is "not bridge $\Rightarrow$ not chess", the contrapositive. **Must be true.**
* (c) fails if nobody plays chess: the statement is then vacuously true.

Only (b).
</details>

**Example 2.** For real $x$, is "$x^3 > x$" necessary, sufficient, both or neither for "$x > 1$"?

<details><summary>Show solution</summary>

Find the exact set: $x^3 - x = x(x-1)(x+1) > 0$ for $-1 < x < 0$ or $x > 1$.

* $x > 1 \Rightarrow x^3 > x$, since $(1, \infty)$ is inside the set. So $x^3 > x$ is **necessary** for $x > 1$.
* $x = -\tfrac12$ gives $x^3 = -\tfrac18 > -\tfrac12$ but $x \not> 1$. So it is **not sufficient**.

Necessary but not sufficient.
</details>

**Example 3.** Write down the negation of: "For every real $M$ there exists a real $x$ such that $f(x) > M$."

<details><summary>Show solution</summary>

Flip each quantifier in order and negate the inside:

$$\exists M\ \forall x:\ f(x) \le M.$$

"There is a real $M$ such that $f(x) \le M$ for all real $x$" — that is, $f$ is bounded above. This matches: the original says $f$ is unbounded above.
</details>

**Example 4.** Is $\neg P \Rightarrow (Q \lor R)$ equivalent to $(\neg Q \land \neg R) \Rightarrow P$?

<details><summary>Show solution</summary>

The contrapositive of $\neg P \Rightarrow (Q \lor R)$ is $\neg(Q \lor R) \Rightarrow P$, and by De Morgan $\neg(Q \lor R) \equiv \neg Q \land \neg R$. So yes.

Check via OR form: both are $P \lor Q \lor R$.
</details>
