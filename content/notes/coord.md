# Coordinate geometry

TMUA coordinate geometry is mostly straight lines and circles, set up so that one good idea — a perpendicular distance, a symmetry, the discriminant — replaces a long calculation. Expect tangents, chords, touching circles, areas from coordinates, simple loci, and in Paper 2, statements about families of lines or conditions that are "necessary" or "sufficient".

## Must-know facts

**Lines.**

* Gradient $m = \dfrac{y_2 - y_1}{x_2 - x_1}$; line $y - y_1 = m(x - x_1)$.
* Parallel: equal gradients. Perpendicular: $m_1 m_2 = -1$ (so $ax + by = c$ is perpendicular to $bx - ay = d$).
* Midpoint $\left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$; distance $\sqrt{(\Delta x)^2 + (\Delta y)^2}$.
* Distance from $(x_0, y_0)$ to $ax + by + c = 0$ is $\dfrac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}$.

**Circles.**

* $(x-a)^2 + (y-b)^2 = r^2$. From $x^2 + y^2 + 2gx + 2fy + c = 0$: centre $(-g, -f)$, $r^2 = g^2 + f^2 - c$.
* Tangent $\perp$ radius at the point of contact. Tangent length from $P$: $\sqrt{CP^2 - r^2}$.
* The perpendicular from the centre bisects any chord, so chord length $= 2\sqrt{r^2 - d^2}$.
* Angle in a semicircle: $\angle ACB = 90^\circ$ iff $C$ is on the circle with diameter $AB$ (obtuse inside, acute outside).
* Two circles, centres distance $d$ apart, radii $r_1, r_2$: they meet twice iff $|r_1 - r_2| < d < r_1 + r_2$; touch externally iff $d = r_1 + r_2$; touch internally iff $d = |r_1 - r_2|$.

**Areas.** Triangle with one vertex at the origin and others $(x_1,y_1)$, $(x_2,y_2)$: area $\tfrac12|x_1y_2 - x_2y_1|$. Translate first to put a vertex at the origin. For polygons, use the shoelace formula or "enclosing rectangle minus corner triangles".

## Techniques

* **Line meets circle?** Either compare the distance from the centre to the line with $r$ (fast), or substitute and use the discriminant: $>0$ two points, $=0$ tangent, $<0$ none. With a parameter, expand fully — terms in $m^2$ often cancel.
* **Families of lines.** Write $k(\ldots) + (\ldots) = 0$: every member passes through the point where both brackets vanish. Check which line through that point is *missing* from the family (often the vertical one).
* **Loci.** Write the condition with $P = (x, y)$ and square distances. $PA = kPB$ with $k \ne 1$ gives a circle; $k = 1$ gives the perpendicular bisector. Check with an easy point on the line $AB$.
* **Reflection in a line.** Find the foot $F$ of the perpendicular from $P$, then $P' = 2F - P$.
* **Symmetry.** If both centres lie on a line, the figure is symmetric in that line — second intersection points are mirror images.
* **Eliminate options.** A proposed line must pass through the known point; a proposed circle must have the right centre. Test these before doing algebra.

## Traps

> **Trap:** Forgetting the second answer: a line of given gradient has *two* tangents to a circle, a triangle with given base and area can be above or below the base, $|c| = 4$ means $c = \pm4$.

> **Trap:** The distance formula for a line needs the $\sqrt{a^2 + b^2}$ divisor — $y = x + c$ is at distance $|c|/\sqrt2$ from the origin, not $|c|$.

> **Trap:** In completing the square, $x^2 + y^2 - 6x + 4y - 12 = 0$ gives $r^2 = 9 + 4 + 12$: the constant changes sign when moved across.

> **Tip:** "Sufficient" means condition $\Rightarrow$ result; "necessary" means result $\Rightarrow$ condition. To refute either, one counterexample is enough.

> **Key idea:** Most circle questions reduce to one right-angled triangle: centre, point of contact (or chord midpoint), and an external point.

## Worked examples

**Example 1.** Find the values of $k$ for which the line $y = kx$ is a tangent to the circle $(x - 5)^2 + y^2 = 9$.

<details><summary>Show solution</summary>

Distance from $(5, 0)$ to $kx - y = 0$ is $\dfrac{|5k|}{\sqrt{k^2+1}}$. Set equal to $3$:
$$25k^2 = 9k^2 + 9 \Rightarrow k^2 = \tfrac{9}{16} \Rightarrow k = \pm\tfrac34.$$

Check with a triangle: the origin is $5$ from the centre and the radius is $3$, so the tangent length is $4$, giving gradient $\tfrac34$ — and by symmetry in the $x$-axis, $-\tfrac34$ too.

</details>

**Example 2.** The circles $x^2 + y^2 = 25$ and $(x - 6)^2 + y^2 = 13$ meet at $A$ and $B$. Find $AB$.

<details><summary>Show solution</summary>

Subtract the equations to get the common chord: $x^2 - (x-6)^2 = 12 \Rightarrow 12x - 36 = 12 \Rightarrow x = 4$.

Then $y^2 = 25 - 16 = 9$, so $A, B = (4, \pm3)$ and $AB = 6$.

</details>

**Example 3.** Find the area of the triangle with vertices $(2, 1)$, $(7, 3)$, $(4, 6)$.

<details><summary>Show solution</summary>

Translate by $(-2, -1)$: the vertices become $(0,0)$, $(5, 2)$, $(2, 5)$.

Area $= \tfrac12|5 \times 5 - 2 \times 2| = \tfrac{21}{2}$.

</details>
