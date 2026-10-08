"""Verification for content/questions/trig.json. Run: python3 content/checks/trig_check.py

Every original and twin: the keyed answer is recomputed independently, and every other option is
shown to be wrong (exactly one option matches)."""
import json, math, os, random
from collections import Counter
import sympy as sp
from sympy import pi, sin, cos, tan, sqrt, Rational as R, Interval, solveset

HERE = os.path.dirname(os.path.abspath(__file__))
QL = json.load(open(os.path.join(HERE, "..", "questions", "trig.json")))
Q = {q["id"]: q for q in QL}
x = sp.symbols("x", real=True)
D = pi / 180
done = set()


def key(qid, idx):
    q = Q[qid]
    assert q["answer"] == idx, (qid, q["answer"], idx)
    assert len(set(q["options"])) == len(q["options"]), qid
    done.add(qid)


def numeric(qid, opts, truth, ascending=True):
    """opts: sympy/num values of the options in order; truth: the independently computed answer."""
    assert len(opts) == len(Q[qid]["options"]), qid
    f = [float(v) for v in opts]
    if ascending:
        assert f == sorted(f) and len(set(f)) == len(f), (qid, f)
    hits = [i for i, v in enumerate(opts) if abs(float(v) - float(truth)) < 1e-9]
    assert len(hits) == 1, (qid, hits, truth)
    key(qid, hits[0])


def sols(expr, iv):
    s = solveset(sp.Eq(expr, 0), x, iv)
    if s == sp.S.EmptySet:
        return []
    assert isinstance(s, sp.FiniteSet), s
    return sorted(s, key=float)


def combo(qid, truths):
    """truths = [I, II, III] -> index into the standard 8-option list."""
    table = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4, (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}
    assert Q[qid]["options"][7] == "I, II and III" and len(Q[qid]["options"]) == 8
    key(qid, table[tuple(int(bool(t)) for t in truths)])


def same_fn(f, g, n=200):
    random.seed(1)
    return all(abs(f(t) - g(t)) < 1e-9 for t in (random.uniform(-20, 20) for _ in range(n)))


# 01
numeric("trig-01", [-3, -1, -sqrt(3) / 3, 1, 3], (tan(5 * pi / 4) + cos(2 * pi / 3)) / sin(11 * pi / 6))
# 01b: theta in [0,360) with sin = -sqrt3/2, tan > 0
th = [t for t in range(360) if abs(math.sin(math.radians(t)) + math.sqrt(3) / 2) < 1e-12 and math.tan(math.radians(t)) > 0]
assert th == [240]
numeric("trig-01b", [-R(1, 2) - sqrt(3), -5 * sqrt(3) / 6, R(1, 2) - sqrt(3), sqrt(3) - R(1, 2), sqrt(3) + R(1, 2)],
        cos(240 * D) - tan(240 * D))

# 02: maximise sector area with perimeter 20
r = sp.symbols("r", positive=True)
A = R(1, 2) * r ** 2 * (20 - 2 * r) / r
rstar = sp.solve(sp.diff(A, r), r)[0]
numeric("trig-02", [1, pi / 2, 2, R(5, 2), pi], (20 - 2 * rstar) / rstar)
assert sp.solve(sp.diff(R(1, 2) * r * (20 - r), r), r)[0] == 10   # one-radius slip gives theta = 1
# 02b: minimise perimeter with area 9
P = 2 * r + 18 / r
rmin = sp.solve(sp.diff(P, r), r)[0]
numeric("trig-02b", [6, 6 * sqrt(2), 9, 12, 15], P.subs(r, rmin))

# 03: degrees, open interval
s3 = sols(6 * cos(x * D) ** 2 + sin(x * D) - 5, Interval.open(0, 360))
assert len(s3) == 4
numeric("trig-03", [180, 360, 540, 720, 900], sum(s3))
# 03b
s3b = sols(5 * sin(x) ** 2 + 3 * cos(x) - 3, Interval(0, 2 * pi))
assert len(s3b) == 4
numeric("trig-03b", [2 * pi, 3 * pi, 4 * pi, 5 * pi, 6 * pi], sum(s3b))

# 04: coordinates O origin, A=(5,0,0), B=(0,9,0), T=(0,0,12)
T, Av, Bv = sp.Matrix([0, 0, 12]), sp.Matrix([5, 0, 0]), sp.Matrix([0, 9, 0])
u, v = Av - T, Bv - T
numeric("trig-04", [-R(48, 65), 0, R(33, 65), R(48, 65), R(63, 65)], u.dot(v) / (u.norm() * v.norm()))
# 04b: O=(0,0,0), A=(2,0,0), C=(0,1,0), B=(2,1,0), E above A=(2,0,2)
Bb, Eb = sp.Matrix([2, 1, 0]), sp.Matrix([2, 0, 2])
numeric("trig-04b", [sqrt(2), sqrt(6), 2 * sqrt(2), sqrt(10), 2 * sqrt(6)], Bb.cross(Eb).norm() / 2)

# 05
grid = [2 * math.pi * i / 200000 for i in range(200000)]
den = lambda t: 3 * math.sin(t) ** 2 + 4 * math.cos(t) ** 2 + 2 * math.sin(t)
assert min(den(t) for t in grid) > 0.99
numeric("trig-05", [2, R(12, 5), 3, 4, 12], round(min(12 / den(t) for t in grid), 9))
den2 = lambda t: math.cos(t) ** 2 - 4 * math.sin(t) + 6
assert min(den2(t) for t in grid) > 0
numeric("trig-05b", [R(1, 11), R(1, 10), R(1, 7), R(1, 3), R(1, 2)], round(max(1 / den2(t) for t in grid), 9))

# 06: translate right pi/3 then stretch 1/2 in x
final = lambda t: math.sin(2 * t - math.pi / 3)
cands = [lambda t: math.sin(2 * t - 2 * math.pi / 3), lambda t: math.sin(2 * t - math.pi / 3),
         lambda t: math.sin(2 * t - math.pi / 6), lambda t: math.sin(t / 2 - math.pi / 3),
         lambda t: math.sin(t / 2 - math.pi / 6)]
g1 = lambda t: math.sin(t - math.pi / 3)          # after translation
assert same_fn(lambda t: g1(2 * t), final)
m = [same_fn(c, lambda t: g1(2 * t)) for c in cands]
assert m.count(True) == 1
key("trig-06", m.index(True))
# 06b: stretch sf 3 then translate left pi/2
h1 = lambda t: math.cos(t / 3)
target = lambda t: h1(t + math.pi / 2)
cands = [lambda t: math.cos(3 * t + math.pi / 2), lambda t: math.cos(3 * t + 3 * math.pi / 2),
         lambda t: math.cos(t / 3 - math.pi / 6), lambda t: math.cos(t / 3 + math.pi / 6),
         lambda t: math.cos(t / 3 + math.pi / 2)]
m = [same_fn(c, target) for c in cands]
assert m.count(True) == 1
key("trig-06b", m.index(True))

# 07
n7 = len(sols(sin(3 * x - pi / 6) ** 2 - R(1, 4), Interval.open(-pi, pi)))
numeric("trig-07", [6, 10, 11, 12, 13], n7)
n7b = len(sols(4 * cos(2 * x * D - 30 * D) ** 2 - 3, Interval(0, 360)))
numeric("trig-07b", [5, 7, 8, 9, 10], n7b)


# 08 / 08b / 15 / 15b: number of non-congruent triangles given angle at B (deg), adjacent side c, opposite side b
def ntri(c, Bdeg, b):
    B = math.radians(Bdeg)
    sC = c * math.sin(B) / b
    if sC > 1 + 1e-12:
        return 0
    if abs(sC - 1) < 1e-12:
        return 1
    C1 = math.asin(sC)
    return sum(1 for C in {C1, math.pi - C1} if C > 1e-9 and B + C < math.pi - 1e-9)


samples = [i / 100 for i in range(1, 2001)] + [5, 10]
two = {b for b in samples if ntri(10, 30, b) == 2}
sets8 = [lambda t: 0 < t < 5, lambda t: 5 < t < 10, lambda t: 5 <= t < 10, lambda t: 5 < t <= 10, lambda t: t > 5]
m = [all((b in two) == f(b) for b in samples) for f in sets8]
assert m.count(True) == 1
key("trig-08", m.index(True))
h = 4 * math.sqrt(2)
samples_b = [i / 100 for i in range(1, 2001)] + [h, 8]
one = {b for b in samples_b if ntri(8, 45, b) == 1}
eq = lambda a, b_: abs(a - b_) < 1e-12
sets8b = [lambda t: eq(t, h) or t >= 8, lambda t: t >= 8, lambda t: eq(t, h) or t > 8,
          lambda t: h - 1e-12 <= t < 8, lambda t: t > h + 1e-12]
m = [all((b in one) == f(b) for b in samples_b) for f in sets8b]
assert m.count(True) == 1
key("trig-08b", m.index(True))

# 09 / 09b identities: symbolic simplification plus a numerical counter-check
def ident(lhs, rhs):
    ok = sp.simplify(lhs - rhs) == 0
    random.seed(2)
    num = all(abs(float((lhs - rhs).subs(x, t))) < 1e-9 for t in (random.uniform(0.1, 1.4) for _ in range(5)))
    assert ok == num
    return ok


combo("trig-09", [ident((sin(x) + cos(x)) ** 2 + (sin(x) - cos(x)) ** 2, 2),
                  ident(cos(x) ** 4 - sin(x) ** 4, 1 - 2 * cos(x) ** 2),
                  ident(tan(x) + 1 / tan(x), 1 / (sin(x) * cos(x)))])
combo("trig-09b", [ident((1 - cos(x) ** 2) * (1 + tan(x) ** 2), tan(x) ** 2),
                   ident(sin(x) ** 4 - cos(x) ** 4, 2 * sin(x) ** 2 - 1),
                   ident(1 / (1 - sin(x)) + 1 / (1 + sin(x)), 2 / sin(x) ** 2)])


# 10 / 10b: exact solution counts for a sweep of k, compared with each option set
t_ = sp.symbols("t", real=True)


def count_k(poly, k):
    """Exact count of x-solutions on a half-open interval of length 2*pi ([0, 2pi) or (-pi, pi]) of
    P(u) = k, where u = sin x or cos x: each root strictly inside (-1, 1) gives two values of x,
    a root at +-1 gives one."""
    n = 0
    for root in set(sp.Poly(sp.expand(poly - k), t_).real_roots()):
        n += 2 if -1 < root < 1 else (1 if root in (-1, 1) else 0)
    return n


ks = sorted(set([R(n, 8) for n in range(-48, 33)] + [R(25, 8)]))
half = Interval.Ropen(0, 2 * pi)
c10 = {k: count_k(4 * (1 - t_ ** 2) + 4 * t_ - 1, k) for k in ks}
sets10 = [lambda k: -5 < k < 3, lambda k: -5 <= k < 3, lambda k: -5 < k < 3 or k == 4,
          lambda k: -5 < k <= 3 or k == 4, lambda k: 3 < k < 4]
m = [all((c10[k] == 2) == bool(f(k)) for k in ks) for f in sets10]
assert m.count(True) == 1
key("trig-10", m.index(True))
c10b = {k: count_k(2 * (1 - t_ ** 2) + 3 * t_, k) for k in ks}
sets10b = [lambda k: 3 < k < R(25, 8), lambda k: 3 <= k < R(25, 8), lambda k: 3 < k <= R(25, 8),
           lambda k: -3 < k < 3, lambda k: -3 < k < R(25, 8)]
ks_b = ks + [R(3) + R(1, 16)]
c10b[R(3) + R(1, 16)] = count_k(2 * (1 - t_ ** 2) + 3 * t_, R(3) + R(1, 16))
m = [all((c10b[k] == 4) == bool(f(k)) for k in ks_b) for f in sets10b]
assert m.count(True) == 1
key("trig-10b", m.index(True))

# 11: sides 3k,5k,7k, area 60 sqrt3 -> perimeter
k = sp.symbols("k", positive=True)
Cang = sp.acos(R(9 + 25 - 49, 30))
ksol = sp.solve(sp.Eq(R(1, 2) * 15 * k ** 2 * sin(Cang), 60 * sqrt(3)), k)[0]
numeric("trig-11", [30 * sqrt(2), 60, 60 * sqrt(2), 120, 240], 15 * ksol)
# 11b
a = sp.symbols("a", positive=True)
asol = [s_ for s_ in sp.solve(sp.Eq((a + 2) ** 2, (a - 2) ** 2 + a ** 2 - 2 * (a - 2) * a * cos(2 * pi / 3)), a) if s_ > 2][0]
sides = [asol - 2, asol, asol + 2]
sh = sum(sides) / 2
heron = sp.sqrt(sh * (sh - sides[0]) * (sh - sides[1]) * (sh - sides[2]))
numeric("trig-11b", [15 * sqrt(3) / 8, R(15, 4), 15 * sqrt(3) / 4, 15 * sqrt(3) / 2, 35 * sqrt(3) / 4], heron)

# 12: reflection of sin x in x = pi/3
refl = lambda t: math.sin(2 * math.pi / 3 - t)
cands = [lambda t: math.sin(math.pi / 3 - t), lambda t: math.sin(t - math.pi / 3), lambda t: math.sin(t + math.pi / 3),
         lambda t: -math.sin(t + math.pi / 3), lambda t: math.cos(t + math.pi / 3)]
m = [same_fn(c, refl) for c in cands]
assert m.count(True) == 1
key("trig-12", m.index(True))
# 12b
f12 = lambda t: math.sin(2 * t) + math.cos(t)
combo("trig-12b", [same_fn(lambda t: f12(t + 2 * math.pi), f12), same_fn(lambda t: f12(t + math.pi), f12),
                   same_fn(lambda t: f12(math.pi - t), lambda t: -f12(t))])


# 13 / 13b: lens / Reuleaux areas by exact formula and by Monte-Carlo-free grid count
def grid_area(inside, x0, x1, y0, y1, N=1500):
    cnt = 0
    for i in range(N):
        px = x0 + (x1 - x0) * (i + 0.5) / N
        for j in range(N):
            py = y0 + (y1 - y0) * (j + 0.5) / N
            cnt += inside(px, py)
    return cnt * (x1 - x0) * (y1 - y0) / N ** 2


lens = grid_area(lambda p, q: p * p + q * q <= 4 and (p - 4) ** 2 + q * q <= 12, 0, 2, -2, 2)
seg = lambda rr, th_: R(1, 2) * rr ** 2 * (th_ - sin(th_))
exact13 = seg(2, 2 * pi / 3) + seg(2 * sqrt(3), pi / 3)
assert abs(float(exact13) - lens) < 0.01
numeric("trig-13", [5 * pi / 3 - sqrt(3) - 3, 10 * pi / 3 - 4 * sqrt(3), 10 * pi / 3 - 2 * sqrt(3), 14 * pi / 3 - 4 * sqrt(3), 10 * pi / 3], exact13)
cs = [(0, 0), (2, 0), (1, math.sqrt(3))]
reul = grid_area(lambda p, q: all((p - u_) ** 2 + (q - v_) ** 2 <= 4 for u_, v_ in cs), -0.5, 2.5, -0.5, 2.1)
exact13b = sqrt(3) + 3 * seg(2, pi / 3)
assert abs(float(exact13b) - reul) < 0.01
numeric("trig-13b", [2 * pi - 3 * sqrt(3), pi - sqrt(3), 2 * pi - 2 * sqrt(3), 2 * pi - sqrt(3), 2 * pi], exact13b)

# 14 / 14b
s14 = sols(sin(2 * x - pi / 3) ** 2 - R(3, 4), Interval.open(0, 2 * pi))
assert len(s14) == 7
numeric("trig-14", [11 * pi / 3, 37 * pi / 6, 22 * pi / 3, 8 * pi, 28 * pi / 3], sum(s14))
s14b = sols(4 * cos(2 * x * D + 30 * D) ** 2 - 1, Interval.open(0, 360))
assert len(s14b) == 8
numeric("trig-14b", [660, 1320, 1410, 1440, 1560], sum(s14b))

# 15 / 15b: sufficient <=> exactly one triangle
combo("trig-15", [ntri(8, 30, b) == 1 for b in (5, 4, 10)])
assert ntri(8, 30, 5) == 2
combo("trig-15b", [ntri(6, 60, b) == 1 for b in (3 * math.sqrt(3), 5.5, 6)])
assert ntri(6, 60, 5.5) == 2

# 16 / 16b: dense grid (includes pi/4 multiples exactly)
g = [2 * math.pi * i / 80000 for i in range(80000)]
combo("trig-16", [min(math.sin(t) ** 4 + math.cos(t) ** 4 for t in g) >= 0.5 - 1e-12,
                  min(math.sin(t) ** 6 + math.cos(t) ** 6 for t in g) >= 0.5 - 1e-12,
                  min(abs(math.sin(t)) + abs(math.cos(t)) for t in g) >= 1 - 1e-12])
gd = [t for t in g if abs(math.sin(t)) > 1e-9 and abs(math.cos(t)) > 1e-9]
combo("trig-16b", [max((math.sin(t) + math.cos(t)) ** 2 for t in g) <= 2 + 1e-12,
                   min(math.sin(t) * math.cos(t) for t in g) >= -0.5 - 1e-12,
                   min(math.tan(t) + 1 / math.tan(t) for t in gd) >= 2 - 1e-9])


# 17 / 17b: sign changes on a fine offset grid (no tangencies)
def roots(F, lo, hi, N=400001):
    ts = [lo + (hi - lo) * (i + 0.37) / N for i in range(N)]
    assert all(F(t) != 0 for t in ts)
    return sum(1 for p, q in zip(ts, ts[1:]) if F(p) * F(q) < 0)


numeric("trig-17", [3, 5, 6, 7, 8], roots(lambda t: math.sin(t) - t / 10, -10.5, 10.5))
numeric("trig-17b", [3, 4, 5, 6, 7], roots(lambda t: math.cos(t) - t / 8, -8.5, 8.5))

# 18 / 18b: which option value of k gives exactly three solutions
opts18 = [-1, 0, 1, R(9, 8), R(5, 4)]
c18 = [count_k(1 - t_ ** 2 - t_, kk) for kk in opts18]
assert c18.count(3) == 1
key("trig-18", c18.index(3))
opts18b = [-3, -2, 0, 2, R(10, 3)]
c18b = [count_k(3 * (1 - t_ ** 2) - 2 * t_, kk) for kk in opts18b]
assert c18b.count(3) == 1, c18b
key("trig-18b", c18b.index(3))
# direct cross-checks with solveset at the keyed values
assert len(sols(cos(x) ** 2 - sin(x) - 1, half)) == 3
assert len(sols(3 * sin(x) ** 2 - 2 * cos(x) - 2, Interval.Lopen(-pi, pi))) == 3
assert len(sols(4 * cos(x) ** 2 + 4 * sin(x) - 1 - 4, half)) == 2
assert len(sols(4 * cos(x) ** 2 + 4 * sin(x) - 1 - 3, half)) == 3

# ---------------------------------------------------------------- structure
ids = ["trig-%02d" % i for i in range(1, 19)]
assert sorted(Q) == sorted(ids + [i + "b" for i in ids])
assert done == set(Q), set(Q) - done
orig = [Q[i] for i in ids]
assert Counter(q["difficulty"] for q in orig) == {2: 2, 3: 6, 4: 6, 5: 4}
for i in ids:
    a_, b_ = Q[i], Q[i + "b"]
    assert a_["difficulty"] == b_["difficulty"], i
    assert a_["answer"] != b_["answer"], i
    assert a_["family"] == b_["family"] == i
for q in QL:
    n = len(q["options"])
    assert n == 5 or (n == 8 and q["options"] == ["none of them", "I only", "II only", "III only", "I and II only",
                                                  "I and III only", "II and III only", "I, II and III"]), q["id"]
    assert len(q["distractors"]) >= 3, q["id"]
    for kk in q["distractors"]:
        assert int(kk) != q["answer"] and int(kk) < n, q["id"]
    assert q["difficulty"] >= 2
    if q["figure"] and "svg" in q["figure"]:
        assert "viewBox" in q["figure"]["svg"] and "currentColor" in q["figure"]["svg"]
print("ALL OK")
