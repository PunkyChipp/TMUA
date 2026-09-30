"""Verification for content/questions/trig.json. Run: python3 content/checks/trig_check.py"""
import json, math, os, random
import sympy as sp
from sympy import pi, sin, cos, tan, sqrt, Rational as R, Interval, solveset, S

HERE = os.path.dirname(os.path.abspath(__file__))
Q = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "trig.json")))}
x = sp.symbols("x", real=True)


def key(qid, expected_index):
    q = Q[qid]
    assert q["answer"] == expected_index, (qid, q["answer"], expected_index)
    assert len(set(q["options"])) == len(q["options"]), qid
    assert 4 <= len(q["options"]) <= 8, qid


def nsols(expr, lo, hi, left_closed=True, right_closed=True):
    iv = Interval(lo, hi, not left_closed, not right_closed)
    sol = solveset(sp.Eq(expr, 0), x, iv)
    assert isinstance(sol, sp.FiniteSet), sol
    return sorted(sol, key=float)


def ascending(vals):
    f = [float(v) for v in vals]
    assert f == sorted(f) and len(set(f)) == len(f), f


# 01
v = tan(4 * pi / 3) * cos(7 * pi / 6)
opts = [-R(3, 2), -sqrt(3) / 2, -R(1, 2), R(1, 2), R(3, 2)]
ascending(opts)
assert sp.simplify(v - opts[0]) == 0
key("trig-01", 0)

# 02
r = sp.symbols("r", positive=True)
rv = sp.solve(sp.Eq(R(1, 2) * r * 6, 15), r)[0]
theta = 6 / rv
opts = [R(3, 5), R(5, 6), R(6, 5), R(5, 3), R(12, 5)]
ascending(opts)
assert theta == opts[2]
key("trig-02", 2)

# 03
s3 = nsols(2 * cos(x) ** 2 - sin(x) - 1, 0, 2 * pi)
assert len(s3) == 3, s3
key("trig-03", 2)

# 04
c2 = 3 ** 2 + 5 ** 2 - 2 * 3 * 5 * cos(2 * pi / 3)
opts = [4, sqrt(19), sqrt(34), 7, 8]
ascending(opts)
assert sp.sqrt(c2) == 7
key("trig-04", 3)

# 05
f5 = lambda t: 3 * math.sin(t) ** 2 - 4 * math.cos(t) ** 2 + 2
mx = max(f5(2 * math.pi * i / 100000) for i in range(100000))
assert abs(mx - 5) < 1e-9
key("trig-05", 3)

# 06
g = lambda t: math.sin(t - math.pi / 3)       # after translation
final = lambda t: g(2 * t)                     # stretch sf 1/2 parallel to x-axis
cands = [lambda t: math.sin(2 * t - 2 * math.pi / 3), lambda t: math.sin(2 * t - math.pi / 3),
         lambda t: math.sin(2 * t - math.pi / 6), lambda t: math.sin(t / 2 - math.pi / 3),
         lambda t: math.sin(t / 2 - math.pi / 6), lambda t: math.sin(2 * t + math.pi / 3)]
pts = [random.uniform(-10, 10) for _ in range(50)]
match = [all(abs(c(t) - final(t)) < 1e-12 for t in pts) for c in cands]
assert match == [False, True, False, False, False, False], match
key("trig-06", 1)

# 07
s7 = nsols(2 * sin(2 * x) ** 2 - sin(2 * x), 0, 2 * pi)
assert len(s7) == 9, s7
assert Q["trig-07"]["options"][5] == "$9$"
key("trig-07", 5)


# 08 & 15: count non-congruent triangles given angle B, adjacent side c, opposite side b
def ntri(c, Bdeg, b):
    B = math.radians(Bdeg)
    sC = c * math.sin(B) / b
    if sC > 1 + 1e-12:
        return 0
    if abs(sC - 1) < 1e-12:
        return 1
    C1 = math.asin(sC)
    return sum(1 for C in {C1, math.pi - C1} if C > 1e-12 and B + C < math.pi - 1e-12)


samples = [i / 100 for i in range(1, 2001)]
two = [b for b in samples if ntri(10, 30, b) == 2]
assert all(5 < b < 10 for b in two) and len(two) == len([b for b in samples if 5 < b < 10])
assert ntri(10, 30, 5) == 1 and ntri(10, 30, 10) == 1 and ntri(10, 30, 12) == 1
key("trig-08", 1)

# 09
I = (sin(x) + cos(x)) ** 2 + (sin(x) - cos(x)) ** 2 - 2
II = cos(x) ** 4 - sin(x) ** 4 - (1 - 2 * cos(x) ** 2)
III = tan(x) + 1 / tan(x) - 1 / (sin(x) * cos(x))
truth = [sp.simplify(I) == 0, sp.simplify(II) == 0, sp.simplify(III) == 0]
assert II.subs(x, 0) != 0
assert truth == [True, False, True], truth
key("trig-09", 5)  # I and III only

# 10
s = sp.symbols("s", real=True)
h = 4 * (1 - s ** 2) + 4 * s - 1
vals = [h.subs(s, v) for v in (-1, 1, R(1, 2))]
assert (min(vals), max(vals)) == (-5, 4)
key("trig-10", 1)

# 11
a, b, c = 6, 10, 14
sper = R(a + b + c, 2)
area = sp.sqrt(sper * (sper - a) * (sper - b) * (sper - c))
opts = [15 * sqrt(3) / 2, 15, 15 * sqrt(3), 30, 30 * sqrt(3)]
ascending(opts)
assert sp.simplify(area - 15 * sqrt(3)) == 0
key("trig-11", 2)

# 12
refl = lambda t: math.sin(math.pi / 2 - t)
cands = [math.cos, lambda t: -math.cos(t), lambda t: -math.sin(t), lambda t: math.sin(t - math.pi / 4),
         lambda t: math.sin(t + math.pi / 4), lambda t: math.sin(math.pi / 4 - t)]
match = [all(abs(cf(t) - refl(t)) < 1e-12 for t in pts) for cf in cands]
assert match == [True] + [False] * 5, match
key("trig-12", 0)

# 13: standard lens formula for two circles radius r, centre distance d
rr, d = 2, 2
lens = 2 * rr ** 2 * sp.acos(sp.Rational(d, 2 * rr)) - sp.Rational(d, 2) * sp.sqrt(4 * rr ** 2 - d ** 2)
opts = [4 * pi / 3 - 2 * sqrt(3), 8 * pi / 3 - 4 * sqrt(3), 4 * pi / 3 - sqrt(3), 8 * pi / 3 - 2 * sqrt(3), 8 * pi / 3]
ascending(opts)
assert sp.simplify(lens - opts[3]) == 0
key("trig-13", 3)

# 14
s14 = nsols(sin(2 * x - pi / 3) - sqrt(3) / 2, 0, 2 * pi)
assert len(s14) == 4 and sp.simplify(sum(s14) - 11 * pi / 3) == 0, s14
opts = [5 * pi / 6, 11 * pi / 6, 3 * pi, 10 * pi / 3, 11 * pi / 3, 4 * pi]
ascending(opts)
key("trig-14", 4)

# 15
assert ntri(8, 30, 5) == 2 and ntri(8, 30, 4) == 1 and ntri(8, 30, 10) == 1
key("trig-15", 6)  # II and III only

# 16
grid = [2 * math.pi * i / 200000 for i in range(200000)]
assert max(math.sin(t) + math.cos(t) for t in grid) <= math.sqrt(2) + 1e-12
assert max(math.sin(t) * math.cos(t) for t in grid) <= 0.5 + 1e-12
assert min(math.sin(t) ** 4 + math.cos(t) ** 4 for t in grid) < 0.75
key("trig-16", 4)  # I and II only

# 17: sign changes of sin x - x/10 on [-10.5, 10.5] (no tangencies; offset grid avoids 0 exactly)
F = lambda t: math.sin(t) - t / 10
N = 400001
ts = [-10.5 + 21 * (i + 0.37) / N for i in range(N)]
changes = sum(1 for p, q in zip(ts, ts[1:]) if F(p) * F(q) < 0)
assert changes == 7, changes
assert all(F(t) != 0 for t in ts)
key("trig-17", 3)

# 18
counts = {}
for kv in [-1, 0, 1, R(9, 8), R(5, 4)]:
    counts[kv] = len(nsols(cos(x) ** 2 - sin(x) - kv, 0, 2 * pi, True, False))
assert counts == {-1: 1, 0: 2, 1: 3, R(9, 8): 4, R(5, 4): 2}, counts
key("trig-18", 2)

# structural checks
from collections import Counter
assert sorted(Q) == ["trig-%02d" % i for i in range(1, 19)]
assert Counter(q["difficulty"] for q in Q.values()) == {1: 2, 2: 4, 3: 6, 4: 4, 5: 2}
for q in Q.values():
    assert 0 <= q["answer"] < len(q["options"])
    for k in q["distractors"]:
        assert int(k) != q["answer"] and int(k) < len(q["options"]), q["id"]
print("ALL OK")
