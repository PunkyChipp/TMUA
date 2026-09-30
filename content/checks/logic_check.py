"""Verification for content/questions/logic.json.

Pure-logic questions are checked with a truth-table / finite-model engine;
mathematical claims are brute-forced over sensible domains (with explicit
witnesses / counterexamples for infinite domains).
For every single-answer question we compute the full set of options that
satisfy the criterion and assert it is exactly {keyed answer}, so every
distractor is also shown to be wrong.
"""
import json
import os
import random
from fractions import Fraction as F
from itertools import product, combinations
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "logic.json"), encoding="utf-8"))}

STD = {frozenset(): 0, frozenset("1"): 1, frozenset("2"): 2, frozenset("3"): 3,
       frozenset("12"): 4, frozenset("13"): 5, frozenset("23"): 6, frozenset("123"): 7}


def imp(a, b):
    return (not a) or b


def rows(n):
    return list(product([False, True], repeat=n))


def equiv(f, g, n):
    return all(bool(f(*r)) == bool(g(*r)) for r in rows(n))


def std(true_set):
    return STD[frozenset(true_set)]


def entails(premises, concl, n):
    return all(concl(*r) for r in rows(n) if all(p(*r) for p in premises))


def exactly(opts_ok, qid):
    good = [i for i, ok in enumerate(opts_ok) if ok]
    assert good == [QS[qid]["answer"]], (qid, good, QS[qid]["answer"])
    assert len(opts_ok) == len(QS[qid]["options"]), qid


def check_std(qid, true_set):
    assert QS[qid]["answer"] == std(true_set), (qid, true_set)


# grid of rationals for real-variable checks
GRID = sorted({F(i, 4) for i in range(-60, 61)} | {F(-2), F(2), F(-3), F(3)})

# ---- logic-01 contrapositive: equivalent to P->Q, and is the (not Q -> not P) form
orig = lambda P, Q: imp(P, Q)
opts = [lambda P, Q: imp(Q, P), lambda P, Q: imp(not P, not Q), lambda P, Q: imp(not Q, not P),
        lambda P, Q: P and not Q, lambda P, Q: imp(not P, Q)]
exactly([equiv(o, orig, 2) for o in opts], "logic-01")

# ---- logic-02 negation of "all cards red" over non-empty boxes (colours: R, B)
boxes = [b for k in range(1, 5) for b in product("RB", repeat=k)]
opts = [lambda b: all(c != "R" for c in b), lambda b: all(c != "R" for c in b),
        lambda b: any(c == "R" for c in b), lambda b: any(c != "R" for c in b),
        lambda b: sum(c != "R" for c in b) == 1]
exactly([all(o(b) == (not all(c == "R" for c in b)) for b in boxes) for o in opts], "logic-02")


# ---- necessary / sufficient helper: returns (necessary, sufficient) of cond A for B
def ns(dom, A, B):
    nec = all(A(x) for x in dom if B(x))
    suf = all(B(x) for x in dom if A(x))
    return nec, suf


NS_OPTS = [(True, False), (False, True), (True, True), (False, False)]

# ---- logic-03 x^2>4 relative to x>2
r = ns(GRID, lambda x: x * x > 4, lambda x: x > 2)
exactly([r == o for o in NS_OPTS], "logic-03")

# ---- logic-04 "P only if Q" == P->Q
orig = lambda P, Q: imp(P, Q)
opts = [lambda P, Q: imp(Q, P), lambda P, Q: imp(P, Q), lambda P, Q: imp(not P, not Q),
        lambda P, Q: P and Q, lambda P, Q: imp(not P, Q)]
exactly([equiv(o, orig, 2) for o in opts], "logic-04")

# ---- logic-05 counterexample: 5 | n^2+1 and last digit not in {2,3}
def is_cx(n):
    return (n * n + 1) % 5 == 0 and n % 10 not in (2, 3)
vals = [3, 5, 7, 12, 13]
ok = [is_cx(n) for n in vals] + [not any(is_cx(n) for n in range(1, 1000))]
exactly(ok, "logic-05")

# ---- logic-06 number of false rows of (P->Q)->R
cnt = sum(not imp(imp(P, Q), R) for P, Q, R in rows(3))
exactly([cnt == v for v in [1, 2, 3, 4, 5]], "logic-06")
assert sum(not imp(P, imp(Q, R)) for P, Q, R in rows(3)) == 1

# ---- logic-07 converse / inverse / contrapositive for 6|n -> 3|n
N = range(-600, 601)
t = set()
if all(imp(n % 3 == 0, n % 6 == 0) for n in N): t.add("1")
if all(imp(n % 6 != 0, n % 3 != 0) for n in N): t.add("2")
if all(imp(n % 3 != 0, n % 6 != 0) for n in N): t.add("3")
check_std("logic-07", t)

# ---- logic-08 "O unless F" == (not F -> O)
orig = lambda O, Fn: imp(not Fn, O)
opts = [lambda O, Fn: imp(Fn, not O), lambda O, Fn: imp(not Fn, not O), lambda O, Fn: imp(not O, Fn),
        lambda O, Fn: imp(O, not Fn), lambda O, Fn: Fn and not O]
exactly([equiv(o, orig, 2) for o in opts], "logic-08")

# ---- logic-09 nested quantifiers over reals (witness / counterexample functions)
t = set()
# I: witness y = x^2+1
if all((x * x + 1) > x * x for x in GRID): t.add("1")
# II: for every y, x = |y|+1 violates y > x^2 -> false; confirm the refuting x works on the grid
II_refuted = all(not (y > (abs(y) + 1) ** 2) for y in GRID)
if not II_refuted: t.add("2")
# III: witness x = 0
if all(y * y >= 0 for y in GRID): t.add("3")
check_std("logic-09", t)

# ---- logic-10 students / lectures: all worlds of <=3 students, 2 lectures
LECT = 2
student_types = [(passed, att) for passed in (False, True) for att in product([False, True], repeat=LECT)]
worlds = [w for k in range(0, 4) for w in product(student_types, repeat=k)]
prem = lambda w: all(imp(p, all(a)) for p, a in w)
opts = [lambda w: all(imp(all(a), p) for p, a in w),
        lambda w: all(imp(not all(a), not p) for p, a in w),
        lambda w: all(imp(not p, not all(a)) for p, a in w),
        lambda w: all(any(a) for p, a in w),
        lambda w: any(p for p, a in w)]
exactly([all(o(w) for w in worlds if prem(w)) for o in opts], "logic-10")

# ---- logic-11 negation of "at most one of a,b,c positive"
pats = rows(3)
orig = lambda s: sum(s) <= 1
opts = [lambda s: sum(s) == 0, lambda s: sum(s) >= 1, lambda s: sum(s) == 2,
        lambda s: sum(s) >= 2, lambda s: (3 - sum(s)) >= 2, lambda s: sum(s) == 3]
exactly([all(o(s) == (not orig(s)) for s in pats) for o in opts], "logic-11")

# ---- logic-12 necessary and sufficient for 12 | n
N = range(1, 20001)
B = lambda n: n % 12 == 0
conds = {"1": lambda n: n % 3 == 0 and n % 4 == 0,
         "2": lambda n: n % 2 == 0 and n % 6 == 0,
         "3": lambda n: (n * n) % 48 == 0}
check_std("logic-12", {k for k, c in conds.items() if ns(N, c, B) == (True, True)})

# ---- logic-13 c<0 vs two distinct real roots of x^2+bx+c
dom = [(b, c) for b in GRID[::2] for c in GRID[::2]]
r = ns(dom, lambda bc: bc[1] < 0, lambda bc: bc[0] ** 2 - 4 * bc[1] > 0)
exactly([r == o for o in NS_OPTS], "logic-13")

# ---- logic-14 if / only if / iff with x = -2
t = set()
if all(imp(x == -2, x * x == 4) for x in GRID): t.add("1")
if all(imp(x * x == 4, x == -2) for x in GRID): t.add("2")
if all((x ** 3 == -8) == (x == -2) for x in GRID): t.add("3")
check_std("logic-14", t)

# ---- logic-15 A->B, B->not C entail?
prem = [lambda A, B_, C: imp(A, B_), lambda A, B_, C: imp(B_, not C)]
cands = {"1": lambda A, B_, C: imp(A, not C), "2": lambda A, B_, C: imp(C, not A),
         "3": lambda A, B_, C: imp(not A, C)}
check_std("logic-15", {k for k, c in cands.items() if entails(prem, c, 3)})

# ---- logic-16 equivalents of (P and Q) -> R
orig = lambda P, Q, R: imp(P and Q, R)
cands = {"1": lambda P, Q, R: imp(P, imp(Q, R)),
         "2": lambda P, Q, R: imp(P, R) or imp(Q, R),
         "3": lambda P, Q, R: imp(P, R) and imp(Q, R)}
check_std("logic-16", {k for k, c in cands.items() if equiv(c, orig, 3)})

# ---- logic-17 syllogism: worlds = sets of member types (L, V, S)
types = rows(3)  # (left, violin, sing)
t_ok = {"1": True, "2": True, "3": True}
for mask in range(1, 1 << 8):
    w = [types[i] for i in range(8) if mask >> i & 1]
    if any(L and V for L, V, S in w):
        continue
    if not any(V and S for L, V, S in w):
        continue
    if not any(S and not L for L, V, S in w): t_ok["1"] = False
    if any(L and S for L, V, S in w): t_ok["2"] = False
    if not any(S and V for L, V, S in w): t_ok["3"] = False
check_std("logic-17", {k for k, v in t_ok.items() if v})

# ---- logic-18 negation of  forall n exists p [P(p) and n<p<2n]  -- random finite models
random.seed(1)
NS_, PS = range(1, 5), range(1, 11)
orig = lambda P: all(any(P[p] and n < p < 2 * n for p in PS) for n in NS_)
opts = [lambda P: any(all(imp(P[p], p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: any(all(imp(P[p], p <= n and p >= 2 * n) for p in PS) for n in NS_),
        lambda P: all(any(P[p] and (p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: all(all(imp(P[p], p <= n or p >= 2 * n) for p in PS) for n in NS_),
        lambda P: any(any(P[p] and (p <= n or p >= 2 * n) for p in PS) for n in NS_)]
models = [{p: random.random() < 0.4 for p in PS} for _ in range(3000)]
models.append({p: p in (2, 3, 5, 7) for p in PS})
exactly([all(o(P) == (not orig(P)) for P in models) for o in opts], "logic-18")


# ---- logic-19 f = x^3 + a x strictly increasing iff a >= 0
def increasing(a):
    xs = [F(i, 8) for i in range(-40, 41)]
    if a < 0:
        d = F(1, 1000)
        while d * d >= -a:
            d /= 2
        return d ** 3 + a * d > (-d) ** 3 + a * (-d)  # False: f(d) < f(-d)
    return all((x2 ** 3 + a * x2) > (x1 ** 3 + a * x1) for x1, x2 in zip(xs, xs[1:]))
AS = sorted(set(GRID) | {F(-1, 2), F(1, 100), F(-1, 100)})
inc = {a: increasing(a) for a in AS}
assert all(inc[a] == (a >= 0) for a in AS)
opts = [lambda a: a >= -1, lambda a: a <= 0, lambda a: a == 0, lambda a: a >= 0, lambda a: a > 0, lambda a: a > 1]
exactly([ns(AS, o, lambda a: inc[a]) == (True, False) for o in opts], "logic-19")


# ---- logic-20 complete set of a with  forall x (x>a -> x^2>4)
def stmt(a):
    xs = [a + F(k, 100) for k in range(1, 3000)]
    return all(x * x > 4 for x in xs)
AS = [F(i, 4) for i in range(-40, 41)]
truth = {a: stmt(a) for a in AS}
opts = [lambda a: a >= -2, lambda a: abs(a) >= 2, lambda a: a > 2, lambda a: a >= 2, lambda a: a >= 4]
exactly([all(o(a) == truth[a] for a in AS) for o in opts], "logic-20")

# ---- logic-21 teacher: not H -> (not R -> not P)
stmt21 = lambda H, R, P: imp(not H, imp(not R, not P))
cases = {"1": (True, False, True), "2": (False, False, True), "3": (False, False, False)}
check_std("logic-21", {k for k, v in cases.items() if stmt21(*v)})
# robustness: also under the biconditional reading of "unless"
bic = lambda H, R, P: imp(not H, (not P) == (not R))
assert {k for k, v in cases.items() if bic(*v)} == {"1", "3"}


# ---- logic-22 integer witnesses
def is_sq(m):
    return m >= 0 and isqrt(m) ** 2 == m
A = range(-200, 201)
t = set()
if all(is_sq(a * a + 0) for a in A): t.add("1")
# II: a=1 has no non-zero b (proof in solution; confirm on a big range)
if any(is_sq(1 + b * b) for b in range(-100000, 100001) if b != 0): t.add("2")
if all(all((c - a) * (c - a) >= 0 for c in range(-60, 61)) for a in range(-60, 61)): t.add("3")
check_std("logic-22", t)
assert not any(is_sq(4 + b * b) for b in range(1, 100000))  # a=2 also fails


# ---- logic-23 negation of property T, on explicit periodic 0/1 sequences.
# For such sequences every tail contains the same values, and quantifying over all
# eps > 0 reduces to the representative eps values below, so the finite check is faithful.
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
        lambda a: all(all(any(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS),
        lambda a: all(any(all(v >= e for v in tail(a, Nv)) for Nv in NN) for e in EPS)]
Tv = {k: T(s) for k, s in seqs.items()}
assert Tv == {"one_zero": False, "const1": False, "zero": True, "zero_then_one": False}, Tv
# C must agree with "not T" on every sequence; every other option must disagree on some sequence
res = [all(o(s) == (not Tv[k]) for k, s in seqs.items()) for o in opts]
exactly(res, "logic-23")


# also check C against not-T in random finite "eventually periodic" models (structural sanity)
def flip_check():
    for _ in range(300):
        per = [random.choice([0, 1, 2]) for _ in range(random.randint(1, 4))]
        a = lambda n, per=per: per[n % len(per)]
        assert opts[2](a) == (not T(a))
flip_check()

# ---- logic-24 self-referential statements
sols = []
for tt in product([False, True], repeat=4):
    s = sum(tt)
    v = [4 - s == 1, (not tt[0]) or (not tt[3]), s <= 2, not tt[2]]
    if list(tt) == v:
        sols.append(frozenset(i + 1 for i in range(4) if tt[i]))
assert len(sols) == 1
opt_sets = [frozenset(), frozenset({3}), frozenset({1, 4}), frozenset({2, 3}), frozenset({1, 2, 4})]
exactly([sols[0] == o for o in opt_sets] + [len(sols) == 0], "logic-24")

# ---- structural checks
ids = sorted(QS)
assert ids == [f"logic-{i:02d}" for i in range(1, 25)]
from collections import Counter
assert Counter(q["difficulty"] for q in QS.values()) == {1: 2, 2: 5, 3: 8, 4: 6, 5: 3}
for q in QS.values():
    assert 4 <= len(q["options"]) <= 8 and len(set(q["options"])) == len(q["options"]), q["id"]
    assert 0 <= q["answer"] < len(q["options"]), q["id"]
    assert len(q["distractors"]) >= 2 and all(int(k) != q["answer"] for k in q["distractors"]), q["id"]
    assert all(0 <= int(k) < len(q["options"]) for k in q["distractors"]), q["id"]

print("ALL OK")
