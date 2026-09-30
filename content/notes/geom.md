# Geometry & measures

TMUA geometry uses GCSE and AS tools: similar shapes, circle theorems, Pythagoras in 2D and 3D,
areas and volumes, and angles in polygons. Questions reward seeing the right structure, such as
a similar triangle, a right angle hidden by a tangent, or a symmetry, rather than long
calculation. There are usually no diagrams, so draw your own quickly and label it.

## Must-know facts

* **Scale factors:** if lengths scale by $k$, areas scale by $k^2$ and volumes by $k^3$. Always return to the length factor first.
* **Polygons:** interior angles of an $n$-gon sum to $(n-2)\cdot180^\circ$; exterior angles sum to $360^\circ$. For a regular polygon, each exterior angle is $\frac{360^\circ}{n}$, so it must divide $360$.
* **Circle theorems:** the angle at the centre is twice the angle at the circumference; the angle in a semicircle is $90^\circ$; angles in the same segment are equal; opposite angles of a cyclic quadrilateral sum to $180^\circ$; a tangent is perpendicular to the radius; the two tangents from a point are equal; alternate segment theorem.
* **Volumes:** prism $=$ cross-section $\times$ length; cylinder $\pi r^2h$; cone $\frac13\pi r^2h$; pyramid $\frac13\times$ base $\times$ height; sphere $\frac43\pi r^3$. Surface areas: sphere $4\pi r^2$; curved surface of a cone $\pi rl$, where $l$ is the slant height.
* **Triangles:** equilateral of side $a$ has area $\frac{\sqrt3}{4}a^2$; inradius $r=\frac{\text{area}}{\text{semi-perimeter}}$, and for a right-angled triangle $r=\frac{a+b-c}{2}$; the circumcentre of a right-angled triangle is the midpoint of the hypotenuse.
* **Triangles sharing an angle** have areas in the ratio of the products of the enclosing sides.

## Techniques

**Coordinates for 3D.** Put a cube or cuboid on axes with a vertex at the origin. Distances are
then $\sqrt{\Delta x^2+\Delta y^2+\Delta z^2}$, and cross-sections become equations such as
$x+y+z=3$. This is quicker and safer than hunting for right-angled triangles in a sketch.

**Right pyramids and cones.** The apex is above the centre of the base, so (height)$^2$ + (centre-to-vertex distance)$^2$ = (sloping edge)$^2$. For a triangular base, the centre is $\frac23$ of the way along a median.

> **Key idea:** A tangent plane or a parallel cut creates a smaller copy of the whole figure. Find the linear scale factor and everything else follows.

**Overlapping regions.** Use inclusion–exclusion: the total area of the pieces equals the area covered plus the
overlaps counted again. It often avoids integrating or computing segments.

**Part-to-part versus part-to-whole.** Area ratios from similarity give $\frac{AD}{AB}$, but the question often asks for $\frac{AD}{DB}$. Convert at the end.

> **Tip:** In "must be true" questions, try the most symmetric case (it usually satisfies everything) and then a lopsided case (it usually breaks the false statements). One explicit counterexample settles a statement.

## Traps

> **Trap:** Using the slant height of a cone or pyramid as the perpendicular height.

> **Trap:** Using the area scale factor for volumes, or treating depth as proportional to volume in a cone of water.

> **Trap:** Assuming "all sides in proportion" means similar. It does for triangles, but not for quadrilaterals: a square and a non-square rhombus both have four equal sides.

* Forgetting the $\frac13$ for cones and pyramids, or the $\frac43$ for spheres.
* Giving the angle at the centre when the question asks for the angle at the circumference, or using the minor arc instead of the major arc.
* Halving where you should double, for example a chord is twice the half-chord.

## Worked examples

**Example 1.** A sphere of radius $3$ fits exactly inside a cylinder, touching the top, the bottom and the curved surface. What fraction of the cylinder's volume is outside the sphere?

<details><summary>Show solution</summary>

The cylinder has $r=3$ and $h=6$, so its volume is $54\pi$. The sphere's volume is $\frac43\pi\cdot27=36\pi$.
The fraction outside is $\frac{54\pi-36\pi}{54\pi}=\frac13$. In general, sphere : cylinder $=2:3$
for any size, so the answer is always $\frac13$. A cone with the same base and height gives $1:2:3$.

</details>

**Example 2.** Chords $AB$ and $CD$ of a circle meet at $X$ inside the circle, with $AX=4$, $XB=6$ and $CX=3$. Find $CD$.

<details><summary>Show solution</summary>

Angles in the same segment give angle $CAX$ = angle $BDX$ and angle $ACX$ = angle $DBX$, so
triangles $AXC$ and $DXB$ are similar. Hence $\frac{AX}{DX}=\frac{CX}{BX}$, i.e.
$AX\cdot XB=CX\cdot XD$. Then $24=3\cdot XD$, so $XD=8$ and $CD=11$.

</details>

**Example 3.** A regular polygon has interior angle $168^\circ$. How many diagonals does it have?

<details><summary>Show solution</summary>

The exterior angle is $12^\circ$, so $n=\frac{360}{12}=30$. Each vertex joins to $n-3$ others by
a diagonal, and each diagonal is counted twice: $\frac{30\cdot27}{2}=405$.

</details>
