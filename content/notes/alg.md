# Algebra & functions

Algebra underpins almost every TMUA question, but questions set purely on it tend to test a few things over and over. These are conditions on the roots of a quadratic involving a parameter, inequalities where one lost case costs you the mark, hidden quadratics ($u=2^x$, $u=x^2$), the factor and remainder theorems, and careful reasoning about domains and inverses. The algebra itself is rarely long. The difficulty is in not missing a case.

## Must-know facts

* **Indices:** $a^m a^n=a^{m+n}$, $(a^m)^n=a^{mn}$, $a^{-n}=\frac1{a^n}$, $a^{p/q}=(\sqrt[q]a)^p$. Put everything into one base (usually 2 or 3) before simplifying.
* **Surds:** $\frac{1}{\sqrt a-\sqrt b}=\frac{\sqrt a+\sqrt b}{a-b}$. Multiplying by the conjugate gives a difference of two squares.
* **Completing the square:** $ax^2+bx+c=a\left(x+\frac{b}{2a}\right)^2+c-\frac{b^2}{4a}$. Take out the factor $a$ *before* halving $b$.
* **Discriminant** $\Delta=b^2-4ac$: two distinct real roots if $\Delta>0$, a repeated root if $\Delta=0$, no real roots if $\Delta<0$. A curve is always above the $x$-axis when $a>0$ and $\Delta<0$.
* **Roots:** for $ax^2+bx+c=0$, $\alpha+\beta=-\frac ba$ and $\alpha\beta=\frac ca$. For a cubic $x^3+px^2+qx+r$: $\sum\alpha=-p$, $\sum\alpha\beta=q$, $\alpha\beta\gamma=-r$.
* **Symmetric expressions:** $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta$ and $\alpha^3+\beta^3=(\alpha+\beta)^3-3\alpha\beta(\alpha+\beta)$.
* **Factor/remainder theorem:** the remainder when $p(x)$ is divided by $(x-c)$ is $p(c)$. Dividing by $(ax-b)$ leaves remainder $p(b/a)$.
* **Functions:** $fg(x)=f(g(x))$, so $g$ is applied first. The range of $f$ is the domain of $f^{-1}$. $f^{-1}$ exists only if $f$ is one-to-one on its domain.

## Techniques

* **Line meets curve:** substitute the linear equation into the quadratic, then use the discriminant of the resulting quadratic to count the intersections (0, 1 tangent, or 2).
* **Signs of the roots from sum and product:** both roots positive $\iff \Delta\ge0$, sum $>0$, product $>0$. If the product is $<0$, the roots have opposite signs, and you don't need to check $\Delta$.
* **Hidden quadratics:** $4^x=(2^x)^2$, $x^4=(x^2)^2$, $x-5\sqrt x+6=0$. Set $u=\ldots$, solve, then **keep only the valid $u$**: $u=2^x$ must be $>0$, and $u=x^2$ must be $\ge0$. Each positive $u=x^2$ gives two $x$ values and $u=0$ gives one.
* **Quadratic inequalities:** find the roots and sketch the parabola, then read off the answer. Don't try to reason it out without the sketch.
* **Inequalities with $x$ in a denominator:** multiply by $x^2$ (which is positive), not by $x$, then draw a sign diagram for the resulting cubic.
* **Polynomial with given values:** if $p(1)=1$, $p(2)=2$, ... then $p(x)-x$ has known roots. Write it in factor form.
* **$f=f^{-1}$:** for an *increasing* $f$, the two graphs can only meet on $y=x$, so solve $f(x)=x$ and then check the domain.
* **Self-inverse:** $\frac{ax+b}{cx-a}$ is its own inverse. To find its range, rewrite it as a constant plus a fraction: $\frac{2x+1}{x-2}=2+\frac5{x-2}$.

> **Tip:** Test special values. Put $k=0$, $x=0$ or $x=\pm1$ into every option and cross off the ones that fail. With 6-8 options, two quick tests often leave only one.

> **Key idea:** "Two distinct real roots" for an upward parabola is the same as "the parabola is negative somewhere". So $f(0)<0$ (that is, $c<0$), or $f(1)<0$, or any $f(t)<0$ is enough on its own.

## Traps

> **Trap:** When the $x^2$ coefficient contains the parameter, e.g. $kx^2+4x+k-3=0$, the equation is linear when $k=0$. Exclude that value, or treat it separately.

> **Trap:** Multiplying an inequality by an expression whose sign you don't know. $\frac6x>x-1$ is **not** equivalent to $6>x^2-x$.

> **Trap:** Taking only the positive square root. $(1+m)^2=16$ gives $m=3$ **or** $m=-5$.

* In a hidden quadratic, one of the $u$-roots is often negative or zero. Rejecting $u=0$ doesn't reject the other root.
* When completing the square for $2x^2-12x$, you get $2(x-3)^2-18$, not $-9$.
* Sufficient and necessary are different. "$m>3$" can be sufficient for two intersections without being necessary.
* $\alpha^3+\beta^3\ne(\alpha+\beta)(\alpha^2+\beta^2)$. You need the $-\alpha\beta$ term.
* The domain of $f^{-1}$ is the **range** of $f$, not the domain of $f$.

## Worked examples

**1.** Find the complete set of values of $k$ for which $x^2-2kx+k+6=0$ has two distinct positive roots.

<details><summary>Show solution</summary>

Need $\Delta>0$: $4k^2-4(k+6)>0\iff(k-3)(k+2)>0\iff k<-2$ or $k>3$.

Sum $2k>0\Rightarrow k>0$. Product $k+6>0\Rightarrow k>-6$.

All three together: $k>3$. A quick check with $k=4$ gives $x^2-8x+10$, whose roots $4\pm\sqrt6$ are both positive.

</details>

**2.** How many real solutions does $x^4-3x^2-4=0$ have?

<details><summary>Show solution</summary>

Put $u=x^2$: $u^2-3u-4=(u-4)(u+1)=0$, so $u=4$ or $u=-1$. Only $u=4$ is allowed, which gives $x=\pm2$. So there are **2** real solutions, not 4. The product of the $u$-roots is $-4<0$, which already tells you exactly one of them is positive.

</details>

**3.** When $p(x)$ is divided by $(x-1)$ the remainder is $3$, and when it is divided by $(x+2)$ the remainder is $-3$. Find the remainder when $p(x)$ is divided by $(x-1)(x+2)$.

<details><summary>Show solution</summary>

The remainder on division by a quadratic is linear: $p(x)=(x-1)(x+2)q(x)+ax+b$.

$p(1)=a+b=3$ and $p(-2)=-2a+b=-3$, so $a=2$ and $b=1$. The remainder is $2x+1$.

</details>
