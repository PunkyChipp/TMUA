# Probability & counting

TMUA probability is GCSE/AS level but set to trap people who apply rules without checking the conditions. Expect sample-space questions with dice and coins, tree diagrams (especially without replacement and conditional probability), "at least one", counting arrangements and selections with restrictions, and the occasional area-based (geometric) probability. Paper 2 likes asking whether statements about independence and mutual exclusivity must hold, or where an argument goes wrong.

## Must-know facts

* Equally likely outcomes: $P(E)=\dfrac{\text{favourable}}{\text{total}}$. With two dice, use the $36$ **ordered** outcomes.
* $P(A\cup B)=P(A)+P(B)-P(A\cap B)$. Add probabilities only for **mutually exclusive** events.
* $A$, $B$ **independent** means $P(A\cap B)=P(A)P(B)$. Multiply only for independent events (or use conditional probabilities along a tree).
* Mutually exclusive events with non-zero probabilities are never independent.
* Conditional probability: $P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$.
* $P(\text{at least one})=1-P(\text{none})$.
* Expected value: $E(X)=\sum x\,P(X=x)$.
* Arrangements of $n$ objects with repeats $a,b,\dots$: $\dfrac{n!}{a!\,b!\cdots}$. Selections: $\binom nr=\dfrac{n!}{r!(n-r)!}$.
* Choosing $k$ from $n$ with no two consecutive: $\binom{n-k+1}{k}$.

## Techniques

**Count, don't multiply, when unsure.** Probability $=$ (number of favourable selections)/(number of selections), e.g. $P(\text{two reds from }5R,3B)=\binom52/\binom82$. This avoids ordering mistakes on trees.

**Complement first.** "At least one", "not all the same", "at least one woman on the committee" are usually one subtraction away.

**Natural frequencies for conditional probability.** Imagine $1000$ people and follow them down the tree; then the conditional probability is a ratio of counts. This makes "given a positive test" questions quick.

**Restrictions in arrangements.**

* *Must be together:* glue them into a block, then multiply by internal arrangements.
* *Must not be together:* arrange the others, then place the restricted items in the gaps; or subtract "together" from the total.
* *A before B:* by symmetry exactly half of all arrangements.

**Inclusion–exclusion** for "none of these happen" (no couple together, no letter in its place): add singles, subtract pairs, add triples. Do not stop early.

**Recursive games.** For "first to roll a six wins", write $p=\frac16+\frac{25}{36}p$: either you win now, or the game resets.

**Geometric probability** is a ratio of lengths or areas. Sketch the region and use the complement if it is simpler.

> **Tip:** Check that your categories add up to the total. If you classified $20$ triangles into shapes, the counts must sum to $20$.

## Traps

> **Trap:** Adding probabilities of overlapping events. "Six rolls, each with $\frac16$ chance of a six, so $P(\text{at least one})=1$" is wrong because two rolls can both be sixes.

> **Trap:** Unordered outcomes are not equally likely. Getting a $2$ and a $6$ has probability $\frac2{36}$, not $\frac1{36}$.

> **Trap:** Confusing $P(A\mid B)$ with $P(B\mid A)$. A test that detects $90\%$ of cases does not mean a positive result is $90\%$ reliable.

> **Trap:** "Given at least one is red" is not "given the first is red". The conditioning event is larger, so the answer changes.

> **Trap:** Overcounting with "choose one of the required type, then any others". This counts committees with several women more than once.

## Worked examples

**Example 1.** Two cards are drawn without replacement from $4$ red and $6$ black. Given that at least one is red, find the probability that both are red.

<details><summary>Show solution</summary>

Count pairs: $\binom{10}2=45$ in total, $\binom62=15$ with no red, so $30$ contain a red. Both red: $\binom42=6$. Answer $\frac{6}{30}=\frac15$.

</details>

**Example 2.** How many arrangements of the letters of SUCCESS have no two S's adjacent?

<details><summary>Show solution</summary>

Arrange U, C, C, E: $\frac{4!}{2!}=12$ ways, creating $5$ gaps. Put the three identical S's in $3$ different gaps: $\binom53=10$. Total $120$.

</details>

**Example 3.** A fair coin is tossed until the first head. Find the probability that this takes an odd number of tosses.

<details><summary>Show solution</summary>

Let $p$ be the probability. Either the first toss is a head ($\frac12$), or the first two are tails ($\frac14$) and we restart: $p=\frac12+\frac14p$, so $p=\frac23$.

</details>

**Example 4.** A fair die is rolled twice. Are "first roll is $6$" and "total is $7$" independent?

<details><summary>Show solution</summary>

$P(\text{first }6)=\frac16$, $P(\text{total }7)=\frac16$, and $P(\text{both})=P((6,1))=\frac1{36}=\frac16\cdot\frac16$. Yes, they are independent: whatever the first roll, exactly one second roll makes $7$.

</details>
