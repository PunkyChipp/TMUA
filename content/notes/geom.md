# Geometry, vectors & measures

TMUA geometry uses higher GCSE tools: angles and polygons, congruence and similarity, circle
theorems, Pythagoras in 2D and 3D, bearings, plans and elevations, transformations, vectors, and
areas and volumes. Questions reward spotting the structure (a similar triangle, a right angle
hidden by a tangent, a symmetry) rather than long calculation. Diagrams are often absent, so
draw your own quickly and label it.

Formulae for the volume and surface area of spheres, cones and pyramids are **given in the
question** when needed. You still need cylinders, prisms, circles and triangles by heart.

## Must-know facts

* **Scale factors:** if lengths scale by $k$, areas scale by $k^2$ and volumes by $k^3$. Always return to the length factor first.
* **Congruence:** SSS, SAS (angle between the sides), ASA/AAS, RHS. **Not** SSA (the ambiguous case) and not AAA (that only gives similarity). Similar plus one equal length or equal area means congruent.
* **Polygons:** interior angles of an $n$-gon sum to $(n-2)\cdot180^\circ$; exterior angles of a convex polygon sum to $360^\circ$. A regular $n$-gon has exterior angle $\frac{360^\circ}{n}$, so a given exterior angle $e$ is possible only if $\frac{360}{e}$ is a whole number. A convex polygon has at most three acute angles.
* **Circle theorems:** angle at the centre is twice the angle at the circumference; angle in a semicircle is $90^\circ$; angles in the same segment are equal; opposite angles of a cyclic quadrilateral sum to $180^\circ$; tangent $\perp$ radius; equal tangents from a point; alternate segment theorem.
* **Bearings:** measured clockwise from north, three figures. The bearing of $P$ from $R$ is the bearing of $R$ from $P$ $\pm180^\circ$.
* **Enlargement** with centre $C$ and scale factor $k$: $\overrightarrow{CP'}=k\,\overrightarrow{CP}$. If $0<|k|<1$ the image is smaller; if $k<0$ the image is on the other side of $C$, rotated through $180^\circ$, and $C$ divides $PP'$ in the ratio $1:|k|$. Areas scale by $k^2$.
* **Vectors:** $\overrightarrow{AB}=\mathbf b-\mathbf a$; the point dividing $AB$ in the ratio $m:n$ is $\frac{n\mathbf a+m\mathbf b}{m+n}$. Parallel vectors are scalar multiples; $A,B,C$ are collinear when $\overrightarrow{AC}=\lambda\overrightarrow{AB}$.
* **Measures:** cylinder $\pi r^2h$; cone $\frac13\pi r^2h$, curved surface $\pi rl$; pyramid $\frac13\times$ base $\times$ height; sphere $\frac43\pi r^3$, surface $4\pi r^2$. Sector area $\frac{\theta}{360}\pi r^2$.

## Techniques

**Vector proofs and ratios.** Write the unknown point in two ways, one parameter per line, e.g.
$\mathbf a+s(\mathbf n-\mathbf a)$ and $\mathbf b+t(\mathbf m-\mathbf b)$. Because $\mathbf a$ and
$\mathbf b$ are not parallel, compare coefficients. The coefficients then give ratios along lines
and heights for area fractions: in triangle $OAB$, the triangle $O$, $p\mathbf a$, $q\mathbf b$ has
area fraction $pq$.

**Coordinates for 3D.** Put a cube or cuboid on axes with a vertex at the origin. Distances are
$\sqrt{\Delta x^2+\Delta y^2+\Delta z^2}$, and cross-sections become equations such as
$x+y+z=3$. Slanted triangles in 3D: find each side as a face diagonal first.

**Right pyramids and cones.** The apex is above the centre of the base, so
(height)$^2$ + (centre-to-vertex)$^2$ = (sloping edge)$^2$, and
(slant height of a face)$^2$ = (height)$^2$ + (centre-to-edge)$^2$. For a solid with an inscribed
sphere, volume $=\frac13\times$ (total surface area) $\times r$.

**Plans and elevations.** For stacks of cubes, each stack is capped by its column's height in the
front view and its row's height in the side view. Greatest total: every stack at the smaller of
its two caps. Least total: one cube on every square of the plan, then the fewest tall stacks,
letting one stack satisfy a row and a column at once.

**Bearings.** Draw north lines at every point. Turn each bearing into an angle inside the
triangle using back bearings, then use right-angled trigonometry or the sine/cosine rules.

> **Key idea:** A tangent plane or a parallel cut creates a smaller copy of the whole figure. Find the linear scale factor and everything else follows.

**Overlapping regions.** Inclusion–exclusion: the total area of the pieces equals the area
covered plus the overlaps counted again. Two overlapping sectors: add them, subtract the
region counted twice.

> **Tip:** In "must be true" questions, try the most symmetric case and then a lopsided one. One explicit counterexample settles a statement. For circle theorems, check whether the points can be on the same side of a chord.

## Traps

> **Trap:** Using the slant height of a cone or pyramid as the perpendicular height, or the height of a triangular face as the height of the pyramid.

> **Trap:** Using the area scale factor for volumes, or treating depth as proportional to volume in a cone of water.

> **Trap:** For a negative scale factor, the centre is **not** the midpoint of $P$ and $P'$ unless $k=-1$.

* "All sides in proportion" means similar for triangles, but not for quadrilaterals.
* Counting glued faces in the surface area of a composite solid.
* Part-to-part versus part-to-whole: similarity gives $\frac{AD}{AB}$, the question may want $\frac{AD}{DB}$.
* Giving the bearing of $R$ from $P$ when asked for $P$ from $R$.

## Worked examples

**Example 1.** In triangle $OAB$, $M$ is the midpoint of $OB$ and $N$ is on $AB$ with $AN:NB=1:2$. The lines $AM$ and $ON$ meet at $X$. Find $OX:XN$.

<details><summary>Show solution</summary>

$\overrightarrow{ON}=\frac23\mathbf a+\frac13\mathbf b$, so $\overrightarrow{OX}=\lambda\left(\frac23\mathbf a+\frac13\mathbf b\right)$.
On $AM$: $\overrightarrow{OX}=\mathbf a+\mu\left(\frac12\mathbf b-\mathbf a\right)=(1-\mu)\mathbf a+\frac{\mu}{2}\mathbf b$.
Comparing: $\frac{2\lambda}{3}=1-\mu$ and $\frac{\lambda}{3}=\frac{\mu}{2}$, so $\mu=\frac{2\lambda}{3}$ and $\lambda=\frac34$.
Hence $OX:XN=3:1$.

</details>

**Example 2.** A sphere of radius $3$ fits exactly inside a cylinder, touching the top, the bottom and the curved surface. What fraction of the cylinder's volume is outside the sphere? [Sphere: $\frac43\pi r^3$.]

<details><summary>Show solution</summary>

The cylinder has volume $\pi\cdot9\cdot6=54\pi$; the sphere $36\pi$. The fraction outside is
$\frac{18\pi}{54\pi}=\frac13$, for any size of sphere.

</details>

**Example 3.** A boat sails $5$ km on a bearing of $040^\circ$, then $12$ km on a bearing of $130^\circ$. How far is it from its start?

<details><summary>Show solution</summary>

At the turning point the back bearing to the start is $220^\circ$, and $220^\circ-130^\circ=90^\circ$, so
the path turns through a right angle. Distance $=\sqrt{5^2+12^2}=13$ km.

</details>
