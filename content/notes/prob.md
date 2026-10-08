# Probability & statistics

The TMUA tests the GCSE statistics and probability content (spec M6–M7), plus counting. The maths is not hard; the questions are set so that people who apply a rule without checking its conditions go wrong. Expect: averages that change when values are added, removed or transformed; histograms with unequal class widths; cumulative frequency and quartiles; "which conclusion is valid" questions about scatter graphs and grouped data; two-way tables, Venn and tree diagrams; conditional probability; with/without replacement; and counting arrangements and selections. Paper 2 likes "must be true" statements about averages, independence and correlation.

## Must-know facts

**Statistics**

* Mean $=\dfrac{\text{total}}{n}$. Every "a value is added/removed" question is about totals.
* Under $y=ax+b$: mean, median, mode and quartiles all become $a(\cdot)+b$; range and IQR are multiplied by $|a|$ and ignore $b$. If $a<0$ the order reverses, so the old lower quartile becomes the new upper quartile.
* Grouped data: estimate the mean with class midpoints; estimate the median and quartiles by linear interpolation within a class.
* Histograms: **area** $\propto$ frequency, and frequency density $=\dfrac{\text{frequency}}{\text{class width}}$. If the vertical scale is missing, find it from one bar.
* Cumulative frequency: read the quartiles at $\frac14n$, $\frac12n$, $\frac34n$ (the question will say which convention); IQR $=Q_3-Q_1$.
* Comparing distributions: compare a location (median/mean) **and** a spread (IQR/range), in context.
* Correlation describes association in the sample. It does not show causation, and a line of best fit should not be used outside the range of the data (extrapolation).

**Probability and counting**

* With two dice use the $36$ **ordered** outcomes.
* $P(A\cup B)=P(A)+P(B)-P(A\cap B)$; add only for mutually exclusive events.
* Independent means $P(A\cap B)=P(A)P(B)$. Mutually exclusive events with non-zero probabilities are never independent.
* $P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$.
* Expected number of successes in $n$ trials $=n\times P(\text{success})$; expected value $E(X)=\sum xP(X=x)$.
* Arrangements with repeats: $\dfrac{n!}{a!\,b!\cdots}$. Selections: $\binom nr$.

## Techniques

**Totals for averages.** Convert each mean to a total, adjust, divide by the new count. For "extreme" questions (largest possible range given mean, median and mode), write the list in order $a\le b\le\cdots$, fix the forced positions, then push the free values to the extremes. Check whether a repeat would tie with the mode.

**Histograms.** Work with areas: frequency $=$ density $\times$ width. For "how many between $25$ and $40$", take the right fraction of each partial class, assuming values are spread evenly.

**Cumulative frequency.** Interpolate: within a class from $L$ to $U$ where the cumulative frequency rises from $c_1$ to $c_2$, the value at position $p$ is $L+\dfrac{p-c_1}{c_2-c_1}(U-L)$. To compare groups, find a value on one curve and read it on the other.

**Valid conclusions.** Grouped data and summary statistics support statements about proportions and averages, not about individuals (you cannot tell who was fastest within a class). A mean above the median does not force any value above the median. To refute "must be true", build a small explicit data set.

**Expected frequencies for conditional probability.** Imagine $1000$ people and fill in a two-way table; the conditional probability is a ratio of two counts in one row or column.

**Venn diagrams with an unknown overlap.** Put $x$ in the overlap and write every region in terms of $x$; the constraints come from every region being at least $0$.

**Complement first.** "At least one", "uses every colour": subtract from the total, with inclusion–exclusion if needed.

**Restrictions in arrangements.** Together: glue into a block. Not adjacent: arrange the others and drop the restricted items into the gaps.

**Repeating games.** For "first to roll a six wins", either write $p=(\text{win now})+(\text{both miss})\,p$, or compare the players' chances within one round.

## Traps

> **Trap:** Averaging two means. Combined mean $=\dfrac{n_1\bar x_1+n_2\bar x_2}{n_1+n_2}$, not $\frac12(\bar x_1+\bar x_2)$.

> **Trap:** Reading bar height as frequency when class widths differ.

> **Trap:** Moving a value between groups can raise **both** means: it happens whenever the value lies between the two means.

> **Trap:** Confusing $P(A\mid B)$ with $P(B\mid A)$. A test that detects $90\%$ of cases does not make a positive result $90\%$ reliable.

> **Trap:** "Given at least one is red" is not "given the first is red".

> **Trap:** Adding probabilities of overlapping events: six rolls do not give $P(\text{at least one six})=1$.

> **Trap:** Correlation is not causation, and extrapolating a line of best fit can give impossible values.

## Worked examples

**Example 1.** Nine values have mean $20$. The value $28$ is removed and two equal values are added; the new mean is $19$. Find the added values.

<details><summary>Show solution</summary>

Total $180$; remove $28$: $152$ for $8$ values. New total $10\times19=190$, so the two added values total $38$: each is $19$.

</details>

**Example 2.** In a histogram, the $0$–$10$ bar is $2$ cm tall and represents $30$ people. The $10$–$40$ bar is $1$ cm tall. How many people does it represent?

<details><summary>Show solution</summary>

Areas: $10\times2=20$ units for $30$ people, so $1.5$ people per unit. The second bar has area $30\times1=30$ units: $45$ people.

</details>

**Example 3.** Two cards are drawn without replacement from $4$ red and $6$ black. Given that at least one is red, find the probability that both are red.

<details><summary>Show solution</summary>

$\binom{10}2=45$ pairs, $\binom62=15$ with no red, so $30$ contain a red. Both red: $\binom42=6$. Answer $\frac{6}{30}=\frac15$.

</details>

**Example 4.** A fair die is rolled twice. Are "first roll is $6$" and "total is $7$" independent?

<details><summary>Show solution</summary>

$P(\text{first }6)=\frac16$, $P(\text{total }7)=\frac16$ and $P(\text{both})=P((6,1))=\frac1{36}=\frac16\cdot\frac16$. Yes: whatever the first roll, exactly one second roll makes $7$.

</details>
