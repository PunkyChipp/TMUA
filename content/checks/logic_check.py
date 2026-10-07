"""Verification for content/questions/logic.json (24 originals + 24 twins).

* Pure-logic questions: every truth assignment is enumerated, or (for quantified
  statements about a group) every "world" = every set of member types is enumerated,
  so "must / could / cannot be true" and "is the negation of" are decided exactly.
* Mathematical claims: brute force over sensible domains (rational grids, integer
  ranges, lattice quadrilaterals / triangles), with explicit witnesses and
  counterexamples for the infinite parts.
For every question we compute the full list of options that satisfy the criterion
and assert it is exactly [keyed answer], so every distractor is also shown wrong.
"""
import json
import os
import random
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import isqrt

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QLIST = json.load(open(os.path.join(HERE, "..", "questions", "logic.json"), encoding="utf-8"))
QS = {q["id"]: q for q in QLIST}
III_OPTS = ["none of them", "I only", "II only", "III only", "I and II only",
            "I and III only", "II and III only", "I, II and III"]
STD = {frozenset(): 0, frozenset("1"): 1, frozenset("2"): 2, frozenset("3"): 3,
       frozenset("12"): 4, frozenset("13"): 5, frozenset("23"): 6, frozenset("123"): 7}
CHECKED = set()


def imp(a, b):
    return (not a) or b


def rows(n):
    return list(product([False, True], repeat=n))


def equiv(f, g, n):
    return all(bool(f(*r)) == bool(g(*r)) for r in rows(n))


def entails(premises, concl, n):
    return all(concl(*r) for r in rows(n) if all(p(*r) for p in premises))


def exactly(ok, qid):
    q = QS[qid]
    assert len(ok) == len(q["options"]), (qid, len(ok))
    good = [i for i, v in enumerate(ok) if v]
    assert good == [q["answer"]], (qid, good, q["answer"])
    CHECKED.add(qid)


def check_std(qid, true_set):
    """I/II/III question: true_set is the set of statement numbers ('1','2','3') that hold."""
    q = QS[qid]
    assert q["options"] == III_OPTS, qid
    exactly([i == STD[frozenset(true_set)] for i in range(8)], qid)


def worlds(ntypes_attrs):
    """All worlds: every set of member types, each type a tuple of booleans."""
    types = rows(ntypes_attrs)
    for mask in range(1 << len(types)):
        yield [types[i] for i in range(len(types)) if mask >> i & 1]


def ns(dom, A, B):
    """(necessary, sufficient) for condition A relative to property B over dom."""
    return all(A(x) for x in dom if B(x)), all(B(x) for x in dom if A(x))


NEC_ONLY, SUF_ONLY, BOTH, NEITHER = (True, False), (False, True), (True, True), (False, False)

GRID = sorted({F(i, 8) for i in range(-80, 81)} | {F(i) for i in range(-30, 31)})

# ===================================================================== 01 / 01b
for qid, opts in [
    ("logic-01", [lambda w: all(imp(v, h) for h, v in w), lambda w: all(imp(not h, not v) for h, v in w),
                  lambda w: all(imp(not v, not h) for h, v in w), lambda w: any(h for h, v in w),
                  lambda w: any(h and not v for h, v in w)]),
    # (h, v) = (wind above 50, warning issued)
    ("logic-01b", [lambda w: all(imp(not v, not h) for h, v in w), lambda w: all(imp(v, h) for h, v in w),
                   lambda w: all(imp(not h, not v) for h, v in w), lambda w: any(h for h, v in w),
                   lambda w: any(h and not v for h, v in w)])]:
    prem_worlds = [w for w in worlds(2) if all(imp(h, v) for h, v in w)]
    exactly([all(o(w) for w in prem_worlds) for o in opts], qid)

# ===================================================================== 02
box_types = [b for k in range(1, 4) for b in product("RB", repeat=k)]
box_worlds = [w for k in range(1, 4) for w in product(box_types, repeat=k)]
orig = lambda w: all(any(c == "R" for c in b) for b in w)
opts = [lambda w: all(not any(c == "R" for c in b) for b in w),
        lambda w: all(any(c != "R" for c in b) for b in w),
        lambda w: any(any(c != "R" for c in b) for b in w),
        lambda w: any(not any(c == "R" for c in b) for b in w),
        lambda w: any(all(c == "R" for c in b) for b in w)]
exactly([all(o(w) == (not orig(w)) for w in box_worlds) for o in opts], "logic-02")

# ===================================================================== 02b  (players x matches score matrix)
mats = [tuple(tuple(bits[i * m:(i + 1) * m]) for i in range(p))
        for p in range(1, 4) for m in range(1, 4) for bits in product([False, True], repeat=p * m)]
orig = lambda M: any(all(r) for r in M)
opts = [lambda M: not any(any(r) for r in M),
        lambda M: all(any(not x for x in r) for r in M),
        lambda M: any(all(not x for x in r) for r in M),
        lambda M: any(any(not x for x in r) for r in M),
        lambda M: all(any(not M[i][j] for i in range(len(M))) for j in range(len(M[0])))]
exactly([all(o(M) == (not orig(M)) for M in mats) for o in opts], "logic-02b")

# ===================================================================== 03 / 03b
B = lambda x: x * x - 4 * x + 3 < 0
opts = [lambda x: 1 < x < 2, lambda x: 2 < x < 4, lambda x: abs(x - 2) < 1, lambda x: x * x < 4, lambda x: x > 0]
exactly([ns(GRID, o, B) == NEC_ONLY for o in opts], "logic-03")
assert [ns(GRID, o, B) for o in opts] == [SUF_ONLY, NEITHER, BOTH, NEITHER, NEC_ONLY]

B = lambda x: x ** 3 > 4 * x
opts = [lambda x: x > 0, lambda x: x > 3, lambda x: x * x > 4, lambda x: x < 0, lambda x: x > -2]
exactly([ns(GRID, o, B) == SUF_ONLY for o in opts], "logic-03b")
assert [ns(GRID, o, B) for o in opts] == [NEITHER, SUF_ONLY, NEITHER, NEITHER, NEC_ONLY]

# ===================================================================== 04 / 04b
# 04: O = offered a job, P = passed interview; rule "O only if P" = if O then P.
# III "P is necessary for O" = if O then P (definition of necessary).
rule = lambda O, P: imp(O, P)
c = {"1": lambda O, P: imp(P, O), "2": lambda O, P: imp(not P, not O), "3": lambda O, P: imp(O, P)}
check_std("logic-04", {k for k, f in c.items() if equiv(f, rule, 2)})
# 04b: R = Rhea goes, S = Sam goes; "R if S" = if S then R.
rule = lambda R, S: imp(S, R)
c = {"1": lambda R, S: imp(not R, not S), "2": lambda R, S: imp(S, R), "3": lambda R, S: imp(R, S)}
check_std("logic-04b", {k for k, f in c.items() if equiv(f, rule, 2)})

# ===================================================================== 05 / 05b
cx = lambda n: sp.isprime(n) and not sp.isprime(2 ** n - 1)
exactly([cx(n) for n in [2, 4, 7, 9, 11]], "logic-05")
assert 2 ** 11 - 1 == 23 * 89 and sp.isprime(127)
cx = lambda n: n % 2 == 1 and not sp.isprime(n * n + 4)
exactly([cx(n) for n in [2, 3, 6, 9, 13]], "logic-05b")
assert 85 == 5 * 17 and sp.isprime(173)

# ===================================================================== 06 (orders: sandwich, cake, drink)
W = list(worlds(3))
orig = lambda w: all(imp(s, c or d) for s, c, d in w)
opts = [lambda w: all(imp(s, not (c or d)) for s, c, d in w),
        lambda w: any(s and not c and not d for s, c, d in w),
        lambda w: any(c and d and not s for s, c, d in w),
        lambda w: any(s and not (c and d) for s, c, d in w),
        lambda w: any(s and c and not d for s, c, d in w)]
exactly([all(o(w) == (not orig(w)) for w in W) for o in opts], "logic-06")

# ===================================================================== 06b (flats: balcony, view)
W = list(worlds(2))
orig = lambda w: any(b and v for b, v in w)
opts = [lambda w: all(not b and not v for b, v in w),
        lambda w: any(not b and not v for b, v in w),
        lambda w: any(not b or not v for b, v in w),
        lambda w: all(imp(b, not v) for b, v in w),
        lambda w: all(imp(not b, v) for b, v in w)]
exactly([all(o(w) == (not orig(w)) for w in W) for o in opts], "logic-06b")

# ===================================================================== 07
t = set()
if all(imp(x * x > 9, x > 3) for x in GRID): t.add("1")
if all(imp(x > 3, x * x > 9) for x in GRID): t.add("2")
if all(imp(x <= 3, x * x <= 9) for x in GRID): t.add("3")
check_std("logic-07", t)

# ===================================================================== lattice quadrilaterals (07b, 11)
PTS = [(x, y) for x in range(5) for y in range(5)]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


QUADS = []
for A in PTS:
    for Bq in PTS:
        if Bq == A:
            continue
        for C in PTS:
            if C in (A, Bq):
                continue
            for D in PTS:
                if D in (A, Bq, C):
                    continue
                P4 = (A, Bq, C, D)
                cr = [cross(sub(P4[(i + 1) % 4], P4[i]), sub(P4[(i + 2) % 4], P4[(i + 1) % 4])) for i in range(4)]
                if all(z > 0 for z in cr) or all(z < 0 for z in cr):
                    QUADS.append(P4)


def qinfo(P4):
    A, Bq, C, D = P4
    sides = [dot(sub(P4[(i + 1) % 4], P4[i]), sub(P4[(i + 1) % 4], P4[i])) for i in range(4)]
    angles_right = [dot(sub(P4[i - 1], P4[i]), sub(P4[(i + 1) % 4], P4[i])) == 0 for i in range(4)]
    d1, d2 = sub(C, A), sub(D, Bq)
    return {
        "rect": all(angles_right),
        "square": all(angles_right) and len(set(sides)) == 1,
        "deq": dot(d1, d1) == dot(d2, d2),
        "perp": dot(d1, d2) == 0,
        "bisect": (A[0] + C[0], A[1] + C[1]) == (Bq[0] + D[0], Bq[1] + D[1]),
        "sides_eq": len(set(sides)) == 1,
        "one_right": any(angles_right),
    }


QI = [qinfo(P4) for P4 in QUADS]

# 07b: S = rectangle -> equal diagonals
t = set()
if all(imp(i["rect"], i["deq"]) for i in QI): t.add("1")
if all(imp(i["deq"], i["rect"]) for i in QI): t.add("2")
if all(imp(not i["deq"], not i["rect"]) for i in QI): t.add("3")
check_std("logic-07b", t)
assert qinfo(((0, 0), (4, 0), (3, 2), (1, 2)))["deq"] and not qinfo(((0, 0), (4, 0), (3, 2), (1, 2)))["rect"]

# 11: necessary and sufficient for a square
conds = {"1": lambda i: i["deq"] and i["perp"],
         "2": lambda i: i["deq"] and i["perp"] and i["bisect"],
         "3": lambda i: i["sides_eq"] and i["one_right"]}
assert sum(i["square"] for i in QI) > 20  # includes tilted squares
check_std("logic-11", {k for k, f in conds.items() if ns(QI, f, lambda i: i["square"]) == BOTH})
assert all(ns(QI, f, lambda i: i["square"])[0] for f in conds.values())  # all necessary
kite = qinfo(((0, 1), (2, 0), (4, 1), (2, 4)))
assert kite["deq"] and kite["perp"] and not kite["square"]

# ===================================================================== 11b: lattice triangles, right angle at C
P6 = [(x, y) for x in range(6) for y in range(6)]
TRI = [(A, Bt, C) for A in P6 for Bt in P6 for C in P6 if cross(sub(Bt, A), sub(C, A)) != 0]


def tri_conds(T):
    A, Bt, C = T
    a2, b2, c2 = dot(sub(Bt, C), sub(Bt, C)), dot(sub(A, C), sub(A, C)), dot(sub(A, Bt), sub(A, Bt))
    m2 = (2 * C[0] - A[0] - Bt[0], 2 * C[1] - A[1] - Bt[1])
    return {"right": dot(sub(A, C), sub(Bt, C)) == 0, "1": a2 + b2 == c2,
            "2": dot(m2, m2) == c2, "3": c2 > a2 and c2 > b2}


TC = [tri_conds(T) for T in TRI]
assert sum(i["right"] for i in TC) > 100
check_std("logic-11b", {k for k in "123" if ns(TC, lambda i: i[k], lambda i: i["right"]) == BOTH})
assert ns(TC, lambda i: i["3"], lambda i: i["right"]) == NEC_ONLY

# ===================================================================== 08 / 08b
orig = lambda O, Fn: imp(not Fn, O)
opts = [lambda O, Fn: imp(Fn, not O), lambda O, Fn: imp(not Fn, not O), lambda O, Fn: imp(not O, Fn),
        lambda O, Fn: imp(O, not Fn), lambda O, Fn: Fn and not O]
exactly([equiv(o, orig, 2) for o in opts], "logic-08")
# Rf = refund, Rc = receipt; "no refund unless receipt" = if not Rc then not Rf
orig = lambda Rf, Rc: imp(not Rc, not Rf)
opts = [lambda Rf, Rc: imp(Rc, Rf), lambda Rf, Rc: imp(Rf, Rc), lambda Rf, Rc: imp(not Rf, not Rc),
        lambda Rf, Rc: imp(Rc, not Rf), lambda Rf, Rc: Rf or Rc]
exactly([equiv(o, orig, 2) for o in opts], "logic-08b")

# ===================================================================== 09 / 09b (nested quantifiers on reals)
t = set()
if all((x * x + 1) > x * x for x in GRID): t.add("1")                  # witness y = x^2 + 1
if any(all(y > x * x for x in GRID + [abs(y) + 1]) for y in GRID): t.add("2")  # x = |y|+1 defeats each y
if all(y * y >= 0 for y in GRID): t.add("3")                            # witness x = 0
check_std("logic-09", t)


def pool(x):
    extra = {1 - x} | ({1 / x} if x != 0 else set())
    return GRID + sorted(extra)


t = set()
if all(any(x * y == 1 for y in pool(x)) for x in GRID): t.add("1")   # fails at x = 0 (0*y = 0 for all y)
if all(any(x + y == 1 for y in pool(x)) for x in GRID): t.add("2")
if any(all(x * y == 0 for x in GRID) for y in GRID): t.add("3")
check_std("logic-09b", t)

# ===================================================================== 10 (swim, run, cycle, u16)
W10 = [w for w in worlds(4)
       if all(imp(s, r) for s, r, c, u in w) and any(c and not r for s, r, c, u in w)
       and all(imp(r, not u) for s, r, c, u in w)]
opts = [lambda w: any(c and s for s, r, c, u in w),
        lambda w: all(imp(r, s) for s, r, c, u in w),
        lambda w: all(imp(u, c and s) for s, r, c, u in w),
        lambda w: any(s and u for s, r, c, u in w),
        lambda w: any(c and u for s, r, c, u in w)]
exactly([not any(o(w) for w in W10) for o in opts], "logic-10")  # "cannot be true"

# ===================================================================== 10b (flat, dog, walk)
W10b = [w for w in worlds(3)
        if all(imp(f, not d) for f, d, k in w) and all(imp(d, k) for f, d, k in w)
        and any(k and f for f, d, k in w)]
opts = [lambda w: any(d and f for f, d, k in w),
        lambda w: all(imp(f, not k) for f, d, k in w),
        lambda w: all(imp(k, d) for f, d, k in w),
        lambda w: all(imp(k, f) for f, d, k in w) and any(d for f, d, k in w),
        lambda w: all(imp(k, f) for f, d, k in w)]
exactly([any(o(w) for w in W10b) for o in opts], "logic-10b")  # "could be true"

# ===================================================================== 12 / 12b
N = range(1, 20001)
B12 = lambda n: n % 12 == 0
conds = {"1": lambda n: n % 3 == 0 and n % 4 == 0, "2": lambda n: n % 2 == 0 and n % 6 == 0,
         "3": lambda n: (n * n) % 48 == 0}
check_std("logic-12", {k for k, f in conds.items() if ns(N, f, B12) == BOTH})

B12b = lambda n: (n * n - 1) % 24 == 0
conds = {"1": lambda n: n % 2 == 1, "2": lambda n: sp.isprime(n) and n > 3,
         "3": lambda n: n % 2 != 0 and n % 3 != 0}
check_std("logic-12b", {k for k, f in conds.items() if ns(N, f, B12b)[1]})

# ===================================================================== 13 / 13b
BC = [(b, c) for b in GRID[::2] for c in GRID[::2]] + [(F(1), F(1, 2)), (F(-5), F(0)), (F(5), F(2)), (F(0), F(1, 2))]
B13 = lambda bc: bc[0] ** 2 - 4 * bc[1] > 0
opts = [lambda bc: bc[0] ** 2 > bc[1], lambda bc: bc[0] > bc[1], lambda bc: bc[1] < 0,
        lambda bc: bc[0] ** 2 > 4 * bc[1], lambda bc: bc[1] < 1]
assert [ns(BC, o, B13) for o in opts] == [NEC_ONLY, NEITHER, SUF_ONLY, BOTH, NEITHER]
exactly([ns(BC, o, B13) == SUF_ONLY for o in opts], "logic-13")

X = sp.Symbol("x")
KS = [F(i, 4) for i in range(-24, 25)]


def n_distinct_real(expr):
    return len(set(sp.real_roots(sp.Poly(expr, X))))


three = {k: n_distinct_real(X ** 3 - 3 * X + sp.Rational(k.numerator, k.denominator)) == 3 for k in KS}
assert all(three[k] == (-2 < k < 2) for k in KS)
opts = [lambda k: k == 0, lambda k: 0 < k < 2, lambda k: -2 < k < 2, lambda k: abs(k) < 3, lambda k: k < 1]
assert [ns(KS, o, lambda k: three[k]) for o in opts] == [SUF_ONLY, SUF_ONLY, BOTH, NEC_ONLY, NEITHER]
exactly([ns(KS, o, lambda k: three[k]) == NEC_ONLY for o in opts], "logic-13b")

# ===================================================================== 14 / 14b
DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]
prime_total = lambda r: sp.isprime(r[0] + r[1])
conds = {"1": lambda r: r[0] % 2 == 1 or r[1] % 2 == 1, "2": lambda r: r[0] != r[1],
         "3": lambda r: (r[0] + r[1]) % 3 != 0}
check_std("logic-14", {k for k, f in conds.items() if ns(DICE, f, prime_total)[0]})

YEARS = range(1, 10001)
leap = lambda y: y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
assert leap(2000) and not leap(1900) and not leap(2200) and 2200 % 8 == 0
conds = {"1": lambda y: y % 8 == 0, "2": lambda y: y % 16 == 0, "3": lambda y: y % 4 == 0 and y % 100 != 0}
check_std("logic-14b", {k for k, f in conds.items() if ns(YEARS, f, leap)[1]})

# ===================================================================== 15 / 15b (chains)
prem = [lambda D, A, L, G: imp(D, A), lambda D, A, L, G: imp(L, A), lambda D, A, L, G: imp(A, G)]
c = {"1": lambda D, A, L, G: imp(not G, not D), "2": lambda D, A, L, G: imp(L, D), "3": lambda D, A, L, G: imp(L, G)}
check_std("logic-15", {k for k, f in c.items() if entails(prem, f, 4)})

prem = [lambda T, S, C, St: imp(T, S), lambda T, S, C, St: imp(S, C), lambda T, S, C, St: imp(St, C)]
c = {"1": lambda T, S, C, St: imp(not C, not T), "2": lambda T, S, C, St: imp(St, S),
     "3": lambda T, S, C, St: imp(C, S or St)}
check_std("logic-15b", {k for k, f in c.items() if entails(prem, f, 4)})

# ===================================================================== 16 / 16b (equivalences)
orig = lambda O, I, A: imp(O and I, A)
c = {"1": lambda O, I, A: imp(O, imp(I, A)), "2": lambda O, I, A: imp(not A, (not O) or (not I)),
     "3": lambda O, I, A: imp(O, A) and imp(I, A)}
check_std("logic-16", {k for k, f in c.items() if equiv(f, orig, 3)})

orig = lambda C, D, R: imp(C or D, R)
c = {"1": lambda C, D, R: imp(C, R) and imp(D, R), "2": lambda C, D, R: imp(not R, (not C) or (not D)),
     "3": lambda C, D, R: imp(C or D, R)}
check_std("logic-16b", {k for k, f in c.items() if equiv(f, orig, 3)})

# ===================================================================== 17 (left, violin, sing, piano)
W17 = [w for w in worlds(4)
       if all(not (L and V) for L, V, S, P in w) and any(V and S for L, V, S, P in w)
       and all(imp(S, L or P) for L, V, S, P in w)]
c = {"1": lambda w: any(P and V for L, V, S, P in w), "2": lambda w: any(S and not L for L, V, S, P in w),
     "3": lambda w: all(imp(L, not S) for L, V, S, P in w)}
check_std("logic-17", {k for k, f in c.items() if all(f(w) for w in W17)})

# ===================================================================== 17b (fiction, top shelf, paperback, old)
W17b = [w for w in worlds(4)
        if all(imp(Fi and T, P) for Fi, T, P, O in w) and any(T and not P for Fi, T, P, O in w)
        and all(imp(not Fi, not O) for Fi, T, P, O in w)]
c = {"1": lambda w: any(T and not Fi for Fi, T, P, O in w),
     "2": lambda w: any(T and not P and not O for Fi, T, P, O in w),
     "3": lambda w: all(imp(O, Fi) for Fi, T, P, O in w)}
check_std("logic-17b", {k for k, f in c.items() if all(f(w) for w in W17b)})

# ===================================================================== 18 (random finite models of "primes")
random.seed(1)
NS_, PS = range(1, 6), range(1, 13)
orig = lambda P: all(any(P[p] and n < p < 2 * n for p in PS) for n in NS_)
opts = [lambda P: any(all(imp(P[p], p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: any(all(imp(P[p], p <= n and p >= 2 * n) for p in PS) for n in NS_),
        lambda P: all(any(P[p] and (p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: all(all(imp(P[p], p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: any(any(P[p] and (p <= n or p >= 2 * n) for p in PS) for n in NS_)]
models = [{p: random.random() < 0.5 for p in PS} for _ in range(4000)]
models += [{p: sp.isprime(p) for p in PS}, {p: p in (3, 5, 7, 11) for p in PS}]
exactly([all(o(P) == (not orig(P)) for P in models) for o in opts], "logic-18")

# ===================================================================== 18b (students, heights, friendships)
models = []
for n in range(1, 4):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for hs in product(range(1, 4), repeat=n):
        for fb in product([False, True], repeat=len(pairs)):
            fr = {(i, j): False for i in range(n) for j in range(n)}
            for (i, j), v in zip(pairs, fb):
                fr[(i, j)] = fr[(j, i)] = v
            models.append((n, hs, fr))
orig = lambda m: all(any(m[2][(s, f)] and m[1][f] > m[1][s] for f in range(m[0])) for s in range(m[0]))
opts = [lambda m: not any(any(m[2][(s, f)] and m[1][f] > m[1][s] for f in range(m[0])) for s in range(m[0])),
        lambda m: any(any(m[2][(s, f)] and m[1][f] <= m[1][s] for f in range(m[0])) for s in range(m[0])),
        lambda m: any(all(imp(m[2][(s, f)], m[1][s] >= m[1][f]) for f in range(m[0])) for s in range(m[0])),
        lambda m: all(any(m[2][(s, f)] and m[1][f] <= m[1][s] for f in range(m[0])) for s in range(m[0])),
        lambda m: any(not any(m[2][(s, f)] for f in range(m[0])) for s in range(m[0]))]
exactly([all(o(m) == (not orig(m)) for m in models) for o in opts], "logic-18b")


# ===================================================================== 19 / 19b
def increasing(a):
    if a < 0:  # f(d) < f(-d) for small d > 0 with d^2 < -a
        d = F(1, 1000)
        while d * d >= -a:
            d /= 2
        return d ** 3 + a * d > (-d) ** 3 + a * (-d)
    xs = [F(i, 8) for i in range(-40, 41)]
    return all((x2 ** 3 + a * x2) > (x1 ** 3 + a * x1) for x1, x2 in zip(xs, xs[1:]))


AS = sorted(set(GRID) | {F(-1, 2), F(1, 100), F(-1, 100)})
inc = {a: increasing(a) for a in AS}
assert all(inc[a] == (a >= 0) for a in AS)
opts = [lambda a: a >= -1, lambda a: a <= 0, lambda a: a == 0, lambda a: a >= 0, lambda a: a > 0]
assert [ns(AS, o, lambda a: inc[a]) for o in opts] == [NEC_ONLY, NEITHER, SUF_ONLY, BOTH, SUF_ONLY]
exactly([ns(AS, o, lambda a: inc[a]) == NEC_ONLY for o in opts], "logic-19")

BS = [F(i, 4) for i in range(-28, 29)]
two_sp = {b: n_distinct_real(3 * X ** 2 + 2 * sp.Rational(b.numerator, b.denominator) * X + 3) == 2 for b in BS}
assert all(two_sp[b] == (abs(b) > 3) for b in BS)
opts = [lambda b: b > 3, lambda b: abs(b) > 3, lambda b: b * b > 4, lambda b: b > 4, lambda b: b < 4]
assert [ns(BS, o, lambda b: two_sp[b]) for o in opts] == [SUF_ONLY, BOTH, NEC_ONLY, SUF_ONLY, NEITHER]
exactly([ns(BS, o, lambda b: two_sp[b]) == NEC_ONLY for o in opts], "logic-19b")

# ===================================================================== 20: f(x) = x^2 + px + q >= 0 for all x >= 0
PQ = [(F(i, 4), F(j, 4)) for i in range(-24, 25) for j in range(-24, 25)]
XS = [F(i, 8) for i in range(0, 161)]


def S20(p, q):
    xs = XS + [max(F(0), -p / 2)]  # sample points plus the vertex (if to the right of 0)
    return min(x * x + p * x + q for x in xs) >= 0


def cond2(p, q):
    return q >= 0 and bool(sp.Rational(p.numerator, p.denominator) >= -2 * sp.sqrt(sp.Rational(q.numerator, q.denominator)))


S = {pq: S20(*pq) for pq in PQ}
conds = {"1": lambda pq: pq[0] >= 0 and pq[1] >= 0, "2": lambda pq: cond2(*pq), "3": lambda pq: pq[0] ** 2 <= 4 * pq[1]}
res = {k: ns(PQ, f, lambda pq: S[pq]) for k, f in conds.items()}
assert res == {"1": SUF_ONLY, "2": BOTH, "3": SUF_ONLY}, res
check_std("logic-20", {k for k, v in res.items() if v == BOTH})

# ===================================================================== 20b: two distinct positive roots
PQ2 = [(F(i, 2), F(j, 2)) for i in range(-16, 17) for j in range(-16, 17)]


def two_pos(p, q):
    r = sp.real_roots(sp.Poly(X ** 2 + sp.Rational(p.numerator, p.denominator) * X
                              + sp.Rational(q.numerator, q.denominator), X))
    r = set(r)
    return len(r) == 2 and all(v > 0 for v in r)


T20 = {pq: two_pos(*pq) for pq in PQ2}
conds = {"1": lambda pq: pq[0] ** 2 > 4 * pq[1] and pq[1] > 0,
         "2": lambda pq: pq[0] < 0 < pq[1] and pq[0] ** 2 > 4 * pq[1],
         "3": lambda pq: pq[0] < -3 and 0 < pq[1] < 2}
res = {k: ns(PQ2, f, lambda pq: T20[pq]) for k, f in conds.items()}
assert res == {"1": NEC_ONLY, "2": BOTH, "3": SUF_ONLY}, res
check_std("logic-20b", {k for k, v in res.items() if v[1]})

# ===================================================================== 21 / 21b (consistency of cases)
t1 = lambda H, R, Il, Ps: imp(Ps, H or R)
t2 = lambda H, R, Il, Ps: imp(R, imp(not Il, Ps))
t2_bic = lambda H, R, Il, Ps: imp(R, Ps == (not Il))  # robustness: two-way reading of "unless"
cases = {"1": (True, False, False, False), "2": (False, True, False, False), "3": (False, False, True, False)}
check_std("logic-21", {k for k, v in cases.items() if t1(*v) and t2(*v)})
assert {k for k, v in cases.items() if t1(*v) and t2_bic(*v)} == {"1", "3"}

r1 = lambda Nn, E, O, Nd: imp(Nd, Nn or E)
r2 = lambda Nn, E, O, Nd: imp(E, imp(not O, Nd))
r2_bic = lambda Nn, E, O, Nd: imp(E, Nd == (not O))
cases = {"1": (False, True, False, False), "2": (False, False, True, True), "3": (True, True, True, False)}
check_std("logic-21b", {k for k, v in cases.items() if r1(*v) and r2(*v)})
assert {k for k, v in cases.items() if r1(*v) and r2_bic(*v)} == {"3"}


# ===================================================================== 22 / 22b (integer witnesses)
def is_sq(m):
    return m >= 0 and isqrt(m) ** 2 == m


t = set()
if all(is_sq(a * a + 0) for a in range(-200, 201)): t.add("1")
# II fails at a = 1: 1 + b^2 = k^2 forces b = 0 (proof in solution); confirm over a large range
if any(is_sq(1 + b * b) for b in range(-100000, 100001) if b != 0): t.add("2")
if all(all((c - a) * (c - a) >= 0 for c in range(-60, 61)) for a in range(-60, 61)): t.add("3")
check_std("logic-22", t)
assert not any(is_sq(4 + b * b) for b in range(1, 100000))

t = set()
if all((n * n + n + 1) > 0 and is_sq(n + n * n + n + 1) for n in range(1, 5001)): t.add("1")
if all(not is_sq(n * n + 1) for n in range(1, 200001)): t.add("2")          # witness m = 1
# III: every m is defeated by n = (m+1)^2 - m > 0; if some m survived, III would be true
if not all((m + 1) ** 2 - m > 0 and is_sq((m + 1) ** 2) for m in range(1, 5001)): t.add("3")
check_std("logic-22b", t)

# ===================================================================== 23 (sequence property T)
EPS = [F(1, 1000), F(1, 2), F(1), F(3, 2), F(2), F(1000)]
NN = range(1, 41)
TAIL = 50
seqs = {"one_zero": lambda n: 1 if n % 2 else 0, "const1": lambda n: 1, "zero": lambda n: 0,
        "zero_then_one": lambda n: 0 if n % 3 else 1}


def tail(a, Nv):
    return [abs(a(n)) for n in range(Nv + 1, Nv + TAIL)]


T = lambda a: all(any(all(v < e for v in tail(a, Nv)) for Nv in NN) for e in EPS)
opts = [lambda a: any(all(all(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS),
        lambda a: any(any(all(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS),
        lambda a: any(all(any(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS),
        lambda a: any(all(any(v >= e for v in tail(a, Nv)) for e in EPS) for Nv in NN),
        lambda a: all(all(any(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS)]
Tv = {k: T(s) for k, s in seqs.items()}
assert Tv == {"one_zero": False, "const1": False, "zero": True, "zero_then_one": False}, Tv
exactly([all(o(s) == (not Tv[k]) for k, s in seqs.items()) for o in opts], "logic-23")
for _ in range(300):  # structural sanity on random periodic sequences
    per = [random.choice([0, 1, 2]) for _ in range(random.randint(1, 4))]
    a = lambda n, per=per: per[n % len(per)]
    assert opts[2](a) == (not T(a))

# ===================================================================== 23b (function property U), random finite models
# x ranges over 0..L-1, y over 0..L (so every x has some y > x), M over a finite set of levels.
L, LEVELS = 5, range(0, 4)
XR, YR = range(L), range(L + 1)
U = lambda f: all(any(all(f[y] > M for y in YR if y > x) for x in XR) for M in LEVELS)
opts = [lambda f: any(all(all(f[y] <= M for y in YR if y > x) for x in XR) for M in LEVELS),
        lambda f: any(all(any(f[y] <= M for y in YR if y > x) for x in XR) for M in LEVELS),
        lambda f: all(any(any(f[y] <= M for y in YR if y > x) for x in XR) for M in LEVELS),
        lambda f: any(any(any(f[y] <= M for y in YR if y > x) for x in XR) for M in LEVELS),
        lambda f: any(all(any(f[y] <= M for y in YR if y > x) for M in LEVELS) for x in XR)]
fmodels = [list(v) for v in product(range(0, 5), repeat=L + 1)]
exactly([all(o(f) == (not U(f)) for f in fmodels) for o in opts], "logic-23b")


# ===================================================================== 24 / 24b (self-reference)
def solve(stmts):
    out = []
    for tt in product([False, True], repeat=4):
        if list(tt) == stmts(tt):
            out.append(frozenset(i + 1 for i in range(4) if tt[i]))
    return out


sols = solve(lambda t: [4 - sum(t) == 1, (not t[0]) or (not t[3]), sum(t) <= 2, not t[2]])
assert sols == [frozenset({2, 3})]
opt_sets = [frozenset({1, 4}), frozenset({3}), frozenset({1, 2, 4}), frozenset({2, 3}), None]
exactly([(o is None and not sols) or (o is not None and sols == [o]) for o in opt_sets], "logic-24")

sols = solve(lambda t: [sum(t) >= 3, (not t[0]) or (not t[2]), not t[3], t[0] != t[1]])
assert sols == [frozenset({2, 4})]
opt_sets = [frozenset({3}), frozenset({2, 4}), frozenset({1, 2, 4}), frozenset({1, 3, 4}), None]
exactly([(o is None and not sols) or (o is not None and sols == [o]) for o in opt_sets], "logic-24b")

# ===================================================================== structural checks
orig_ids = [f"logic-{i:02d}" for i in range(1, 25)]
assert [q["id"] for q in QLIST] == [x for i in orig_ids for x in (i, i + "b")]
assert CHECKED == set(QS), sorted(set(QS) - CHECKED)
assert Counter(QS[i]["difficulty"] for i in orig_ids) == {2: 2, 3: 8, 4: 8, 5: 6}
BANNED = ["⇒", "⇔", "→", "∧", "∨", "¬", "∀", "∃", "\\Rightarrow", "\\Leftrightarrow", "\\iff", "\\implies",
          "\\land", "\\lor", "\\neg", "\\lnot", "\\forall", "\\exists", "\\to ", "truth table"]
for i in orig_ids:
    a, b = QS[i], QS[i + "b"]
    assert a["family"] == i and b["family"] == i
    assert a["difficulty"] == b["difficulty"], i
    assert a["answer"] != b["answer"], i
    assert a["stem"] != b["stem"], i
for q in QLIST:
    n = len(q["options"])
    assert n == 5 or q["options"] == III_OPTS, (q["id"], n)
    assert len(set(q["options"])) == n
    assert len(q["distractors"]) >= 3, q["id"]
    assert all(int(k) != q["answer"] and 0 <= int(k) < n for k in q["distractors"]), q["id"]
    for text in [q["stem"]] + q["options"]:
        assert not any(s in text for s in BANNED), (q["id"], text)
    assert q["topic"] == "logic" and q["paper"] == 2 and q["difficulty"] >= 2
pos = Counter(q["answer"] for q in QLIST)
assert max(pos.values()) / len(QLIST) <= 0.4, pos

print("answer positions:", dict(sorted(pos.items())))
print("ALL OK")
