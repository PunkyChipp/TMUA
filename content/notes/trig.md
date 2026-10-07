# Trigonometry

TMUA trigonometry is AS level: exact values, radians, triangles (in 2D and 3D) and trig equations
in a given interval. Most questions are not "solve this" but "how many solutions", "what is the
sum of the solutions", "what is the range" or "which of these is true". Sketching the graph and
substituting for the awkward part will crack most of them.

The specification lists the sine and cosine rules (including the ambiguous case), $\frac12ab\sin C$,
radians with arc length, sector **and** segment area, exact values, graphs with their symmetries
and periods, $\tan x=\frac{\sin x}{\cos x}$, $\sin^2x+\cos^2x=1$, and equations in an interval.
Compound-angle and double-angle formulae and the $R\cos(x-\alpha)$ form are **not** listed, so every
question can be done without them.

## Must-know facts

* **Exact values** for $0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$: $\sin$ runs $0, \frac12, \frac{\sqrt2}{2}, \frac{\sqrt3}{2}, 1$ and $\cos$ runs the other way. $\tan\frac{\pi}{6}=\frac{1}{\sqrt3}$, $\tan\frac{\pi}{4}=1$, $\tan\frac{\pi}{3}=\sqrt3$.
* **Signs by quadrant (CAST):** all positive in the first quadrant, only $\sin$ in the second, only $\tan$ in the third, only $\cos$ in the fourth.
* **Symmetries:** $\sin(\pi-x)=\sin x$, $\cos(-x)=\cos x$, $\cos(2\pi-x)=\cos x$, $\sin\left(\frac{\pi}{2}-x\right)=\cos x$, $\sin(x+\pi)=-\sin x$, $\tan(x+\pi)=\tan x$.
* **Radians:** arc length $s=r\theta$, sector area $\frac12r^2\theta=\frac12rs$, segment area $\frac12r^2(\theta-\sin\theta)$ (sector minus triangle).
* **Triangles:** $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}$; $a^2=b^2+c^2-2bc\cos A$; area $=\frac12ab\sin C$.
* **Identities:** $\sin^2x+\cos^2x=1$ and $\tan x=\dfrac{\sin x}{\cos x}$.
* **Periods:** $\sin kx$ and $\cos kx$ have period $\frac{2\pi}{k}$; $\tan kx$ and $\sin^2 kx$ have period $\frac{\pi}{k}$. A sum repeats only after a common period of all its terms.

## Techniques

**Counting solutions.** For $\sin(kx+c)=v$ on an interval, put $\theta=kx+c$ and transform the
interval the same way. Count per period: two solutions when $-1<v<1$, but only **one** when
$v=\pm1$. Then test each endpoint separately: is it a solution, and is it included?
$\sin^2\theta=\frac14$ means $\sin\theta=\pm\frac12$, so do not lose the negative root.

**Summing solutions.** Never find the messy angles. Solutions of $\sin x=c$ in one period pair up
symmetrically about $\frac{\pi}{2}$ (if $c>0$) or $\frac{3\pi}{2}$ (if $c<0$); for $\cos x=c$ they pair
about $\pi$ (or $0$). In degrees: a pair from $\sin x=\frac13$ sums to $180^\circ$, a pair from
$\sin x=-\frac13$ sums to $540^\circ$. With a substitution $\theta=2x+30^\circ$, sum the $\theta$s,
then subtract $30^\circ$ **once per solution** before halving.

**Quadratics in disguise.** Any expression in $\sin^2x$, $\cos^2x$ and $\sin x$ becomes a
quadratic in $s=\sin x$ with $-1\le s\le1$. For the range, complete the square and check the
vertex (if it lies in $[-1,1]$) **and** both endpoints. For solution counts, each $s\in(-1,1)$
gives two values of $x$ per period and $s=\pm1$ gives one. An odd count forces a root at $\pm1$.

> **Key idea:** The range of $f(\sin x)$ is the range of $f(s)$ on $[-1,1]$, not on $\mathbb{R}$. For $\frac{12}{D}$, the least value comes from the greatest positive $D$.

**Bounds without extra formulae.** $(\sin x\mp\cos x)^2\ge0$ gives $-\frac12\le\sin x\cos x\le\frac12$.
Even powers go through $p=\sin^2x\cos^2x\in[0,\frac14]$: $\sin^4x+\cos^4x=1-2p$ and
$\sin^6x+\cos^6x=1-3p$. Test the symmetric point $x=\frac{\pi}{4}$.

**Ambiguous case (SSA).** Given angle $B$, the adjacent side $c$ and the opposite side $b$, let
$h=c\sin B$. Then $b<h$: no triangle; $b=h$: one (right-angled); $h<b<c$: **two**; $b\ge c$: one.
Picture a circle centred at $A$ swinging onto the ray from $B$.

**Problems in 3D.** Find each side of the slanted triangle from a right-angled triangle lying in a
face, a vertical plane or the ground (face diagonals, $\sqrt{a^2+b^2+c^2}$), then use the cosine rule
or $\frac12ab\sin C$ in the slanted triangle. Do not assume an angle seen on the ground equals the
angle in space.

**Sectors and segments.** Overlaps of circles split along the common chord into segments,
each with its **own** radius and angle at its own centre. A region bounded by three arcs is the
inner triangle plus three segments.

**Transformations.** Each transformation replaces $x$ in the *current* equation.
A translation right by $a$ replaces $x$ by $x-a$; a stretch of factor $k$ parallel to the $x$-axis
replaces $x$ by $\frac{x}{k}$; reflection in $x=a$ replaces $x$ by $2a-x$. Check by tracking one
maximum or zero.

## Traps

> **Trap:** Dividing by $\sin x$ (or $\cos x$) loses the solutions where it is zero. Factorise instead.

> **Trap:** In a closed interval such as $0\le x\le2\pi$, solutions at both endpoints count; in an open interval they do not. Endpoints are where most counting questions are won or lost.

> **Trap:** "Translate then stretch" for $\sin x$ gives $\sin(2x-a)$, not $\sin(2(x-a))$.

* A sign slip in the cosine rule for obtuse angles: $\cos\frac{2\pi}{3}=-\frac12$, so the $-2bc\cos A$ term becomes **positive**.
* Maximising two terms separately, for example taking $\sin^2x=1$ and $\cos^2x=1$ at once.
* Applying $t+\frac1t\ge2$ to $\tan x+\frac{1}{\tan x}$ when $\tan x$ may be negative.
* Radians and degrees mixed in one calculation.

## Worked examples

**Example 1.** How many solutions does $\sin^2\left(2x+\frac{\pi}{4}\right)=\frac12$ have for $-\pi<x<\pi$?

<details><summary>Show solution</summary>

Let $\theta=2x+\frac{\pi}{4}$, so $-\frac{7\pi}{4}<\theta<\frac{9\pi}{4}$, an open interval of length $4\pi$.
$\sin\theta=\pm\frac{1}{\sqrt2}$ gives $\theta=\frac{\pi}{4}+\frac{n\pi}{2}$: four per $2\pi$, so $8$ in a
half-open interval of length $4\pi$. Both endpoints are of this form ($-\frac{7\pi}{4}=\frac{\pi}{4}-2\pi$),
and both are excluded, so the answer is $8-1=7$.

</details>

**Example 2.** Find the range of $f(x)=\sin^2x+2\cos x$.

<details><summary>Show solution</summary>

In terms of $c=\cos x\in[-1,1]$: $f=1-c^2+2c=2-(c-1)^2$. The vertex is at $c=1$, an endpoint,
giving $2$. The other endpoint $c=-1$ gives $-2$. So the range is $-2\le f(x)\le2$.

</details>

**Example 3.** Find the sum of the solutions of $2\sin^2x=\sin x+1$ for $0^\circ\le x<360^\circ$.

<details><summary>Show solution</summary>

$(2\sin x+1)(\sin x-1)=0$. $\sin x=1$ gives $90^\circ$ only (one solution at the peak).
$\sin x=-\frac12$ gives $210^\circ$ and $330^\circ$, a pair symmetric about $270^\circ$, sum $540^\circ$.
Total $630^\circ$.

</details>

**Example 4.** In triangle $ABC$, $AB=6$, angle $B=45^\circ$ and $AC=5$. How many triangles are possible?

<details><summary>Show solution</summary>

The height from $A$ to the ray from $B$ is $h=6\sin45^\circ=3\sqrt2\approx4.24$. Since
$h<5<6$, the circle centre $A$, radius $5$, crosses the ray twice: **two** triangles.

</details>
