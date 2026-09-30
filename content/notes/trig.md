# Trigonometry

TMUA trigonometry is AS level: exact values, radians, triangles and trig equations. Most
questions are not "solve this" but "how many solutions", "what is the range" or "which of these
is true". Sketching the graph and substituting for the awkward part will crack most of them.

## Must-know facts

* **Exact values** for $0, \frac{\pi}{6}, \frac{\pi}{4}, \frac{\pi}{3}, \frac{\pi}{2}$: $\sin$ runs $0, \frac12, \frac{\sqrt2}{2}, \frac{\sqrt3}{2}, 1$ and $\cos$ runs the other way. $\tan\frac{\pi}{6}=\frac{1}{\sqrt3}$, $\tan\frac{\pi}{4}=1$, $\tan\frac{\pi}{3}=\sqrt3$.
* **Signs by quadrant (CAST):** all positive in the first quadrant, only $\sin$ in the second, only $\tan$ in the third, only $\cos$ in the fourth.
* **Symmetries:** $\sin(\pi-x)=\sin x$, $\cos(-x)=\cos x$, $\sin\left(\frac{\pi}{2}-x\right)=\cos x$, $\sin(x+\pi)=-\sin x$, $\tan(x+\pi)=\tan x$.
* **Radians:** arc length $s=r\theta$, sector area $\frac12r^2\theta=\frac12rs$, segment area $\frac12r^2(\theta-\sin\theta)$.
* **Triangles:** $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}$; $a^2=b^2+c^2-2bc\cos A$; area $=\frac12ab\sin C$.
* **Identities:** $\sin^2x+\cos^2x=1$ and $\tan x=\dfrac{\sin x}{\cos x}$.
* **Periods:** $\sin kx$ and $\cos kx$ have period $\frac{2\pi}{k}$; $\tan kx$ has period $\frac{\pi}{k}$.

## Techniques

**Counting solutions.** For $\sin(kx)=c$ on an interval, put $\theta=kx$ and stretch the interval
by $k$. Then count: each full period gives two solutions when $-1<c<1$, but only **one** when
$c=\pm1$. For $c=0$, check the endpoints individually.

> **Tip:** For a curve against a line, such as $\sin x=\frac{x}{10}$, first bound where solutions can be ($|x|\le10$), use odd or even symmetry, then go hump by hump.

**Quadratics in disguise.** Any expression in $\sin^2x$, $\cos^2x$ and $\sin x$ becomes a
quadratic in $s=\sin x$ with $-1\le s\le1$. For the range, complete the square and check the
vertex (if it lies in $[-1,1]$) **and** both endpoints. For solution counts, remember that each
$s\in(-1,1)$ gives two values of $x$ per period and $s=\pm1$ gives one. This parity argument is
often the whole question.

> **Key idea:** The range of $f(\sin x)$ is the range of $f(s)$ on $[-1,1]$, not on $\mathbb{R}$.

**Bounds without the $R$-formula.** $(\sin x-\cos x)^2\ge0$ gives $\sin x\cos x\le\frac12$, and
then $(\sin x+\cos x)^2=1+2\sin x\cos x\le2$. Also $\sin^4x+\cos^4x=1-2\sin^2x\cos^2x$.

**Ambiguous case (SSA).** You are given angle $B$, the adjacent side $c$ and the opposite side $b$. Let
$h=c\sin B$. Then $b<h$: no triangle; $b=h$: one (right-angled); $h<b<c$: **two**; $b\ge c$: one.
Picture a circle centred at $A$ swinging onto the ray from $B$.

**Transformations.** Each transformation replaces $x$ in the *current* equation.
A translation right by $a$ replaces $x$ by $x-a$. A stretch of factor $k$ parallel to the $x$-axis replaces $x$ by $\frac{x}{k}$.
Reflection in $x=a$ replaces $x$ by $2a-x$. Check your answer by tracking one maximum or zero.

**Testing identities.** In "which are identities" questions, try $x=0$ and $x=\frac{\pi}{4}$
first. One failure disproves a statement, and it takes seconds.

## Traps

> **Trap:** Dividing by $\sin x$ (or $\cos x$) loses the solutions where it is zero. Factorise instead.

> **Trap:** When the question uses a closed interval such as $0\le x\le2\pi$, solutions at both endpoints count, for example $\sin x=0$ at $0$, $\pi$ and $2\pi$.

> **Trap:** Doing transformations in the wrong order. "Translate then stretch" for $\sin x$ gives $\sin(2x-a)$, not $\sin(2(x-a))$.

* A sign slip in the cosine rule for obtuse angles: $\cos\frac{2\pi}{3}=-\frac12$, so the $-2bc\cos A$ term becomes **positive**.
* Maximising two terms separately, for example taking $\sin^2x=1$ and $\cos^2x=1$ at once.
* Radians and degrees mixed in one calculation.

## Worked examples

**Example 1.** How many solutions does $\tan 2x=-1$ have for $0\le x\le 2\pi$?

<details><summary>Show solution</summary>

Let $\theta=2x$, so $0\le\theta\le4\pi$. $\tan\theta=-1$ once per period $\pi$, at
$\theta=\frac{3\pi}{4}+n\pi$. The values in range are $\frac{3\pi}{4},\frac{7\pi}{4},\frac{11\pi}{4},\frac{15\pi}{4}$
(the next, $\frac{19\pi}{4}$, exceeds $4\pi$). **Four** solutions. Endpoints do not matter here,
since $\tan0=0\ne-1$.

</details>

**Example 2.** Find the range of $f(x)=\sin^2x+2\cos x$.

<details><summary>Show solution</summary>

In terms of $c=\cos x\in[-1,1]$: $f=1-c^2+2c=2-(c-1)^2$. The vertex is at $c=1$, an endpoint,
giving $2$. The other endpoint $c=-1$ gives $2-4=-2$. So the range is $-2\le f(x)\le2$.
Completing the square on all of $\mathbb{R}$ would suggest no lower bound, which is why the
restriction $-1\le c\le1$ matters.

</details>

**Example 3.** In triangle $ABC$, $AB=6$, angle $B=45^\circ$ and $AC=5$. How many triangles are possible?

<details><summary>Show solution</summary>

The height from $A$ to the ray from $B$ is $h=6\sin45^\circ=3\sqrt2\approx4.24$. Since
$h<5<6$, the circle centre $A$, radius $5$, crosses the ray twice: **two** triangles. With the
sine rule, $\sin C=\frac{6\sin45^\circ}{5}\approx0.85$, and both $C$ and $180^\circ-C$ give an
angle sum below $180^\circ$ with $B=45^\circ$.

</details>
