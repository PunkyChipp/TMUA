"""Verification for content/questions/explog.json (originals + twins). Run: python3 content/checks/explog_check.py

Note: the checks use natural logs internally for numerics; the questions themselves never require change of base.
"""
import json
import math
import os
import re
from collections import Counter
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QL = json.load(open(os.path.join(HERE, "..", "questions", "explog.json"), encoding="utf-8"))
QS = {q["id"]: q for q in QL}
x, t = sp.symbols("x t", real=True)
L = lambda base, v: sp.log(v) / sp.log(base)
done = set()


def key(qid, values, truth):
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    hits = [i for i, v in enumerate(values) if abs(float(sp.N(v - truth, 30))) < 1e-20]
    assert hits == [q["answer"]], (qid, hits, q["answer"])
    vals = [float(sp.N(v)) for v in values]
    assert len(set(vals)) == len(vals), (qid, "options not distinct")
    done.add(qid)


def key_roman(qid, I, II, III):
    table = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4,
             (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}
    assert QS[qid]["answer"] == table[(int(I), int(II), int(III))], qid
    done.add(qid)


def key_set(qid, preds, truth, grid):
    """Option i is a predicate; exactly the keyed one must agree with truth on every grid point."""
    assert len(preds) == len(QS[qid]["options"])
    hits = [i for i, p in enumerate(preds) if all(p(v) == truth(v) for v in grid)]
    assert hits == [QS[qid]["answer"]], (qid, hits)
    done.add(qid)


def key_order(qid, orders, vals):
    """orders: list of tuples of names in claimed increasing order."""
    hits = [i for i, o in enumerate(orders) if all(vals[o[j]] < vals[o[j + 1]] for j in range(len(o) - 1))]
    assert hits == [QS[qid]["answer"]], (qid, hits)
    done.add(qid)


def lg(b, v):
    return math.log(v) / math.log(b)


# explog-01 / 01b
v = sp.simplify(sp.expand_log(3 * L(2, 6) - L(2, 27) + L(2, F(1, 32)), force=True))
key("explog-01", [-2, F(1, 4), 2, 3, 8], v)
X, Y = 3**4, 3**5
key("explog-01b", [-7, -5, -4, 2, 3], sp.log(sp.Rational(9 * X**2, Y**3), 3))

# explog-02 / 02b
sol = sp.solve(sp.Eq(9**t, 6 * 3**t), t)
assert len(sol) == 1
key("explog-02", [L(3, 2), L(3, 6) / 2, L(3, 6), L(3, 18), 6], sol[0])
sol = [s_ for s_ in sp.solve(sp.Eq(3 ** (2 * t), 4), t) if s_.is_real]
assert len(sol) == 1
key("explog-02b", [6, 8, 12, 16, 64], sp.simplify(27 ** sol[0]))

# explog-03: log2(x^2) - log2(x+6) = 1
cands = sp.solve(x**2 - 2 * (x + 6), x)
valid = [c for c in cands if c + 6 > 0 and c != 0 and abs(lg(2, float(c) ** 2) - lg(2, float(c) + 6) - 1) < 1e-12]
assert len(valid) == 2
key("explog-03", [-2, 1, 2, 3, 1 + sp.sqrt(13)], sum(valid))

# explog-03b
cands = sp.solve((x + 1) * (x + 3) - 3, x)
valid = {c for c in cands if c > -1 and abs(lg(3, float(c) + 1) + lg(3, float(c) + 3) - 1) < 1e-12}
opts = [{-4}, {0}, {-2 + sp.sqrt(2)}, {-4, 0}, set()]
assert [i for i, s_ in enumerate(opts) if s_ == valid] == [QS["explog-03b"]["answer"]]
done.add("explog-03b")

# explog-04 / 04b
y = sp.symbols("y", positive=True)
xs = [sp.log(r, 2) for r in sp.solve(y**2 - 8 * y + 12, y)]
for xv in xs:
    assert abs(float(4**xv - 2 ** (xv + 3) + 12)) < 1e-9
key("explog-04", [L(2, 6), 3, L(2, 12), 8, 12], sum(xs))
xs = [sp.log(r, 3) for r in sp.solve(y + 9 / y - 10, y)]
for xv in xs:
    assert abs(float(3**xv + 3 ** (2 - xv) - 10)) < 1e-9
key("explog-04b", [0, 2, L(3, 10), 9, 10], sum(xs))

# explog-05: 0 < a < 1 < b
pairs = [(a_, b_) for a_ in [0.1, 0.3, 0.5, 0.9] for b_ in [1.1, 2, 3, 10]]
grid = [i / 10 for i in range(-50, 51)]
I = all(sum(1 for z in grid if abs(a_**z - b_**z) < 1e-12) == 1 for a_, b_ in pairs)
I = I and all(abs(a_**z - b_**z) > 1e-12 for a_, b_ in pairs for z in grid if z != 0)
II = all(a_**z < b_**z for a_, b_ in pairs for z in grid)
III = all(a_ ** (-z) < a_ ** (-(z + 0.1)) for a_, _ in pairs for z in grid)
key_roman("explog-05", I, II, III)

# explog-05b: count sign changes of 3^x - 4 + x^2 (convex, so sign changes = roots)
h = lambda z: 3**z - 4 + z * z
zs = [i / 1000 for i in range(-10000, 10001)]
roots = sum(1 for i in range(len(zs) - 1) if h(zs[i]) * h(zs[i + 1]) < 0) + sum(1 for z in zs if h(z) == 0)
key("explog-05b", [0, 1, 2, 3, 4], roots)

# explog-06 / 06b
xs6 = [0.3, 1, 2.5, 7, 40]
I = all(abs((lg(3, z) + 2) - lg(3, 9 * z)) < 1e-12 for z in xs6)
II = True  # y = f(9x) is a stretch parallel to the x-axis, scale factor 1/9 (by definition)
III = all(abs(lg(3, z + 9) - lg(3, 9 * z)) < 1e-12 for z in xs6)
key_roman("explog-06", I, II, III)
xs6b = [-2, -0.5, 0, 1, 3]
I = True  # f(x - 2): translation +2 in x (by definition)
II = all(abs(9 * 3**z - 3 ** (z - 2)) < 1e-12 for z in xs6b)
III = all(abs(3**z / 9 - 3 ** (z - 2)) < 1e-12 for z in xs6b)
key_roman("explog-06b", I, II, III)

# explog-07
g = [k / 64 + 1 / 131 for k in range(-640, 1000)]
key_set("explog-07",
        [lambda v: v < 2 or v > 4, lambda v: 0 < v < 2 or 4 < v < 6, lambda v: 2 < v < 4, lambda v: 0 < v < 6,
         lambda v: 0 < v < 2],
        lambda v: 0 < v < 6 and lg(2, v) + lg(2, 6 - v) < 3, g)

# explog-07b
key_set("explog-07b",
        [lambda v: -2 < v < 4, lambda v: 0 < v < 4, lambda v: 2 < v < 4, lambda v: v > 4, lambda v: v < -2 or v > 4],
        lambda v: v > 2 and lg(0.5, v) + lg(0.5, v - 2) > -3, g)

# explog-08 / 08b
key_set("explog-08",
        [lambda v: v > 5, lambda v: v < 5, lambda v: 1 < v < 5, lambda v: 1 < v < 1.25, lambda v: v > 1.25],
        lambda v: v > 1 and lg(0.5, v - 1) > -2, g)
key_set("explog-08b",
        [lambda v: -1 < v < 3, lambda v: v < -1 or v > 3, lambda v: v < -3 or v > 1, lambda v: -3 < v < 1,
         lambda v: v > 3],
        lambda v: 0.5 ** (v * v - 3) < 2 ** (-2 * v), g)

# explog-09 / 09b (exact integer arithmetic)
key_roman("explog-09", 2**30 > 10**9, 3**20 > 2**30, 5**13 < 10**9)
key_roman("explog-09b", 2**100 > 10**30, 5**30 > 2**70, 3**50 < 10**24)

# explog-10 / 10b
A, b = sp.symbols("A b", positive=True)
s10 = sp.solve([A * b**2 - 16000, A * b**6 - 4000], [A, b], dict=True)[0]
T = sp.solve(sp.Eq(s10[A] * s10[b] ** t, 1000), t)
key("explog-10", [7, 8, 10, 12, 14], T[0])
s10 = sp.solve([A * b - 600, A * b**4 - 4800], [A, b], dict=True)[0]
T = sp.solve(sp.Eq(s10[A] * s10[b] ** t, 76800), t)
key("explog-10b", [4, 8, 11, 16, 20], T[0])

# explog-11: x^(log2 x) > 16 x^3, x > 0
gp = [k / 64 + 1 / 131 for k in range(1, 3000)] + [k / 1000 + 1 / 7919 for k in range(1, 1000)]
key_set("explog-11",
        [lambda v: v > 16, lambda v: 0.5 < v < 16, lambda v: 0 < v < 0.5 or v > 16, lambda v: v < -1 or v > 4,
         lambda v: 0 < v < 0.5],
        lambda v: lg(2, v) ** 2 > lg(2, 16) + 3 * lg(2, v), gp)  # log2 of both (positive) sides
for v in [0.3, 0.6, 15, 17]:  # direct check without logs
    assert (v ** lg(2, v) > 16 * v**3) == (v < 0.5 or v > 16)


# explog-11b: count positive solutions of x^(log2 x) = k x numerically for many k
def n11b(kv):
    us = [i / 500 + 1 / 7919 for i in range(-10000, 10001)]  # u = log2 x (offset avoids exact roots)
    fu = lambda u: u * u - u - math.log2(kv)
    c = sum(1 for i in range(len(us) - 1) if fu(us[i]) * fu(us[i + 1]) < 0)
    disc = 1 + 4 * math.log2(kv)
    if abs(disc) < 1e-12:
        return 1
    return c


kgrid = [k / 50 for k in range(1, 300)] + [2 ** -0.25, 2 ** -0.25 + 1e-3, 2 ** -0.25 - 1e-3, 1, 2 ** 0.25]
key_set("explog-11b",
        [lambda k: k > 0, lambda k: k > 2 ** -0.25, lambda k: k >= 2 ** -0.25, lambda k: k > 1, lambda k: k > 2 ** 0.25],
        lambda k: n11b(k) == 2 if abs(k - 2 ** -0.25) > 1e-9 else False, kgrid)
assert n11b(2 ** -0.25) == 1

# explog-12 / 12b
vals = {"a": lg(2, 3), "b": lg(3, 5), "c": lg(5, 8)}
key_order("explog-12", [("a", "b", "c"), ("b", "a", "c"), ("b", "c", "a"), ("c", "a", "b"), ("c", "b", "a")], vals)
assert 9 > 8 and 25 < 27 and 125 > 81 and 512 < 625  # benchmarks in the solution
vals = {"p": lg(2, 6), "q": lg(3, 12), "r": lg(5, 45)}
key_order("explog-12b", [("p", "q", "r"), ("p", "r", "q"), ("q", "p", "r"), ("q", "r", "p"), ("r", "q", "p")], vals)
assert 36 > 32 and 2025 < 3125 and 45**3 > 5**7 and 12**3 < 3**7


# explog-13 / 13b: parse the orders from the option strings, compare exactly
def parse_orders(qid):
    out = []
    for o in QS[qid]["options"]:
        out.append(tuple(int(bb) ** int(ee) for bb, ee in re.findall(r"(\d+)\^\{(\d+)\}", o)))
    return out


for qid in ["explog-13", "explog-13b"]:
    orders = parse_orders(qid)
    assert all(len(o) == 4 for o in orders)
    hits = [i for i, o in enumerate(orders) if all(o[j] < o[j + 1] for j in range(3))]
    assert hits == [QS[qid]["answer"]], (qid, hits)
    done.add(qid)

# explog-14 / 14b
g14 = [v for v in (k / 50 + 1 / 97 for k in range(0, 400)) if v > 0 and abs(v - 1) > 1e-9]
key_set("explog-14",
        [lambda v: v > 2, lambda v: 1 < v < 2, lambda v: 0 < v < 1 or v > 2, lambda v: 0 < v < 2 and v != 1,
         lambda v: 0 < v < 1 or 1 < v < 2],
        lambda v: lg(v, 2) < 1, g14)
key_set("explog-14b",
        [lambda v: -3 < v < 3, lambda v: 1 < v < 3, lambda v: v > 3, lambda v: 0 < v < 1 or 1 < v < 3,
         lambda v: 0 < v < 1 or v > 3],
        lambda v: lg(v, 9) > 2, g14)


# explog-15 / 15b: count positive roots y
def npos(coeffs):
    return len({rr for rr in sp.Poly(coeffs, t).real_roots() if rr > 0})


ks = [F(k, 4) for k in range(-40, 41)]
key_set("explog-15",
        [lambda k: k > 0, lambda k: k > 4, lambda k: k >= 4, lambda k: k < -4 or k > 4, lambda k: -4 < k < 4],
        lambda k: npos(t**2 - k * t + 4) == 2, ks)
ks = [F(k, 8) for k in range(-40, 41)]
key_set("explog-15b",
        [lambda k: k < 0, lambda k: k <= 0, lambda k: k == 1, lambda k: k <= 0 or k == 1, lambda k: k < 1],
        lambda k: npos(t**2 - 2 * t + k) == 1, ks)

# explog-16 / 16b
pairs16 = [(a_, b_) for a_ in [0.2, 0.5, 0.9, 1.5, 2, 5] for b_ in [0.1, 0.25, 0.3, 0.7, 1.2, 1.8, 3] if a_ > b_]
I = all(lg(0.5, a_) < lg(0.5, b_) for a_, b_ in pairs16)
II = all(0.5**a_ > 0.5**b_ for a_, b_ in pairs16)
assert sp.Rational(1, 4) ** sp.Rational(1, 4) == sp.Rational(1, 2) ** sp.Rational(1, 2)  # counterexample to III
III = False
key_roman("explog-16", I, II, III)
I = all(2 ** -a_ < 2 ** -b_ for a_, b_ in pairs16)
II = all(lg(3, 1 / a_) > lg(3, 1 / b_) for a_, b_ in pairs16)
III = all(lg(0.5, a_) - lg(0.5, b_) < 0 for a_, b_ in pairs16)
key_roman("explog-16b", I, II, III)


# explog-17 / 17b: count x-solutions via u >= 2, cross-checked by sign changes
def nsol_u(us):
    c = 0
    for u in us:
        if u.is_real:
            if u > 2:
                c += 2
            elif u == 2:
                c += 1
    return c


ks = [F(k, 8) for k in range(-80, 81)] + [F(17, 4), F(33, 8)]
key_set("explog-17",
        [lambda k: k < 4, lambda k: k <= 4, lambda k: k < F(17, 4), lambda k: 4 < k < F(17, 4), lambda k: k > 4],
        lambda k: nsol_u(sp.solve(t**2 - 3 * t + k - 2, t)) == 2, ks)
key_set("explog-17b",
        [lambda k: True, lambda k: k > 0, lambda k: k > 1, lambda k: k >= 1, lambda k: k > 2],
        lambda k: nsol_u(sp.solve(t**2 - k * t - 2, t)) == 2, ks)
zs = [i / 1000 + 1e-4 for i in range(-8000, 8001)]
for k in [-3, 0, 3.9, 4.1, 5]:
    f = lambda z: 4**z + 4**-z + k - 3 * (2**z + 2**-z)
    ch = sum(1 for i in range(len(zs) - 1) if f(zs[i]) * f(zs[i + 1]) < 0)
    assert ch == nsol_u(sp.solve(t**2 - 3 * t + F(k).limit_denominator(100) - 2, t)), k
for k in [-1, 0.5, 0.99, 1.01, 3]:
    f = lambda z: 9**z + 9**-z - k * (3**z + 3**-z)
    ch = sum(1 for i in range(len(zs) - 1) if f(zs[i]) * f(zs[i + 1]) < 0)
    assert ch == nsol_u(sp.solve(t**2 - F(k).limit_denominator(100) * t - 2, t)), k


# explog-18 / 18b
def t18(v):
    if v <= 0 or abs(v - 1) < 1e-12 or 2 * v - 1 <= 0:
        return False
    return lg(v, 2 * v - 1) > 2


def t18b(v):
    if v <= 0 or abs(v - 1) < 1e-12:
        return False
    return lg(v, v + 6) < 2


g18 = [k / 64 + 1 / 131 for k in range(-640, 640)]
key_set("explog-18",
        [lambda v: False, lambda v: 0.5 < v < 1, lambda v: v > 1, lambda v: 0.5 < v < 1 or v > 1, lambda v: 0 < v < 1],
        t18, g18)
key_set("explog-18b",
        [lambda v: v < -2 or v > 3, lambda v: v > 3, lambda v: 1 < v < 3, lambda v: 0 < v < 1 or v > 3,
         lambda v: 0 < v < 1 or 1 < v < 3],
        t18b, g18)

# ---------------- spec guard: no change of base in any question ----------------
for q in QL:
    blob = json.dumps(q, ensure_ascii=False)
    assert "\\ln" not in blob and "change of base" not in blob.lower(), q["id"]
    assert not re.search(r"\\log_\{?\d\}?\s*\\?\d*\s*\\times\s*\\log", blob), q["id"]
    assert "log_4" not in blob and "log_{a^" not in blob, q["id"]

# ---------------- metadata ----------------
assert done == set(QS), sorted(set(QS) - done)
orig = [q for q in QL if not q["id"].endswith("b")]
assert sorted(q["id"] for q in orig) == [f"explog-{i:02d}" for i in range(1, 19)]
assert sorted(Counter(q["difficulty"] for q in orig).items()) == [(2, 2), (3, 6), (4, 6), (5, 4)]
for q in orig:
    tw = QS[q["id"] + "b"]
    assert tw["difficulty"] == q["difficulty"] and tw["answer"] != q["answer"], q["id"]
    assert q["family"] == tw["family"] == q["id"]
for q in QL:
    no = len(q["options"])
    assert no == 5 or q["options"][0] == "none of them", q["id"]
    assert len(set(q["options"])) == no and 0 <= q["answer"] < no
    assert q["difficulty"] >= 2
    assert len(q["distractors"]) >= 3 and all(int(k) != q["answer"] for k in q["distractors"]), q["id"]
print("ALL OK")
