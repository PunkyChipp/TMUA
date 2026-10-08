# Coordinate geometry

TMUA coordinate geometry is straight lines and circles, set up so that one good idea — a perpendicular distance, a circle theorem, a symmetry, the discriminant — replaces a long calculation. Expect tangents, chords, touching circles, the circle theorems used with coordinates, families of lines with a parameter, simple loci and regions, and (in Paper 2) "necessary" or "sufficient" conditions.

## Must-know facts

**Lines.**

* Both forms: $y = mx + c$ and $ax + by + c = 0$ (gradient $-\tfrac ab$; the second form also covers vertical lines).
* $a_1x + b_1y + c_1 = 0$ and $a_2x + b_2y + c_2 = 0$ are **parallel** iff $a_1b_2 = a_2b_1$ (and distinct iff they are not multiples of each other), **perpendicular** iff $a_1a_2 + b_1b_2 = 0$.
* Midpoint $\left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$; distance $\sqrt{(\Delta x)^2 + (\Delta y)^2}$.
* Distance from $(x_0, y_0)$ to $ax + by + c = 0$: $\dfrac{|ax_0 + by_0 + c|}{\sqrt{a^2 + b^2}}$.

**Circles.**

* Both forms: $(x-a)^2 + (y-b)^2 = r^2$, and $x^2 + y^2 + 2gx + 2fy + c = 0$ with centre $(-g, -f)$, $r^2 = g^2 + f^2 - c$ (must be positive).
* Substituting a point into $x^2 + y^2 + 2gx + 2fy + c$ gives a positive value outside, zero on, negative inside the circle.
* Two circles, centres $d$ apart: meet twice iff $|r_1 - r_2| < d < r_1 + r_2$; touch at either end.

**Circle properties (spec a–g), in coordinate form.**

1. The perpendicular from the centre to a chord bisects it: chord $= 2\sqrt{r^2 - d^2}$.
2. Tangent $\perp$ radius: tangent gradient is $-1/(\text{radius gradient})$; tangent length from $P$ is $\sqrt{CP^2 - r^2}$.
3. Angle at the centre is twice the angle at the circumference.
4. Angle in a semicircle is $90^\circ$: $\angle ACB = 90^\circ$ iff $C$ is on the circle with diameter $AB$ (obtuse inside, acute outside).
5. Angles in the same segment are equal: the points seeing $AB$ at a fixed angle form an arc.
6. Opposite angles of a cyclic quadrilateral add to $180^\circ$.
7. Alternate segment: the tangent–chord angle equals the angle in the alternate segment.

## Techniques

* **Line meets circle?** Compare the distance from the centre with $r$ (fast), or substitute and use the discriminant. With a parameter, expand fully — terms in $m^2$ often cancel.
* **Families of lines.** Write $k(\ldots) + (\ldots) = 0$: every member passes through the point where both brackets vanish, and exactly one line through that point is *missing* (the first bracket). Check whether that missing line is the one a statement needs.
* **Use the theorems to pick a convenient point.** For an angle subtended by a chord, choose the point of the circle that makes it easy (often the end of a diameter, giving a right angle).
* **Loci.** Write the condition with $P = (x, y)$ and square distances: $PA = kPB$ ($k \ne 1$) is a circle. A fixed angle $\angle APB = \theta$ is an arc of a circle whose centre sees $AB$ at $2\theta$; "angle at least $\theta$" is the inside.
* **Regions.** Sketch every boundary, find the corners, then use rectangles, triangles or the shoelace formula; for a circle cut by a chord use sector minus triangle.
* **Reflection in a line.** Foot of the perpendicular $F$, then $P' = 2F - P$.

## Traps

> **Trap:** Forgetting a second answer: a direction has *two* tangents to a circle; a triangle of given area can be on either side of its base.

> **Trap:** $\le$ versus $<$: a tangent meets a circle once, so "two distinct points" needs a strict inequality.

> **Trap:** In $x^2 + y^2 - 6x + 4y - 12 = 0$, $r^2 = 9 + 4 + 12$: the constant changes sign.

> **Tip:** "Sufficient" means condition $\Rightarrow$ result; "necessary" means result $\Rightarrow$ condition. Find the exact condition first, then compare sets.

> **Key idea:** Most circle questions reduce to one right-angled triangle: centre, point of contact (or chord midpoint), and an external point.

## Worked examples

**Example 1.** For which $k$ is the line $y = kx$ a tangent to $(x - 5)^2 + y^2 = 9$?

<details><summary>Show solution</summary>

Distance from $(5, 0)$ to $kx - y = 0$ is $\dfrac{|5k|}{\sqrt{k^2+1}} = 3$, so $16k^2 = 9$ and $k = \pm\tfrac34$. (Tangent length from the origin is $\sqrt{25 - 9} = 4$, giving gradient $\tfrac34$, and $-\tfrac34$ by symmetry.)

</details>

**Example 2.** $A(0, 0)$, $B(4, 0)$ and $C(0, 2)$ lie on a circle. Find the other point where the circle meets the line $y = x$.

<details><summary>Show solution</summary>

$\angle AOC$... here the right angle at $A$ between $AB$ and $AC$ means $BC$ is a diameter (angle in a semicircle): centre $(2, 1)$, $r^2 = 5$. On $y = x$: $(t-2)^2 + (t-1)^2 = 5 \Rightarrow 2t^2 - 6t = 0$, so $t = 3$: the point $(3, 3)$.

</details>

**Example 3.** The lines $(k+1)x + 2y = 3$ and $3x + (k-4)y = 1$ are parallel. Find $k$.

<details><summary>Show solution</summary>

$a_1b_2 = a_2b_1$: $(k+1)(k-4) = 6 \Rightarrow k^2 - 3k - 10 = 0 \Rightarrow k = 5$ or $k = -2$. Check they are distinct: $k = 5$ gives $6x + 2y = 3$ and $3x + y = 1$ (parallel, distinct); $k = -2$ gives $-x + 2y = 3$ and $3x - 6y = 1$ (parallel, distinct). Both work.

</details>
