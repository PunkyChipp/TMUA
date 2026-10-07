"""Verification for content/questions/prob.json (probability & statistics, originals + twins).

Every key is recomputed by brute force (enumerating sample spaces, arrangements, data
sets) or exact arithmetic, every option is checked to be distinct from the correct value,
and family / twin rules are checked (same difficulty, different answer letter).
"""
import json
import os
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QL = json.load(open(os.path.join(HERE, "..", "questions", "prob.json"), encoding="utf-8"))
QS = {q["id"]: q for q in QL}
IDS = [f"prob-{i:02d}" for i in range(1, 19)]
assert len(QS) == 36 and all(i in QS and i + "b" in QS for i in IDS)

ROMAN_IDX = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3,
             (1, 1, 0): 4, (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}


def check_values(qid, values, correct):
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    assert len(set(values)) == len(values), f"{qid}: duplicate option values"
    assert values[q["answer"]] == correct, f"{qid}: key value {values[q['answer']]} != {correct}"
    assert sum(v == correct for v in values) == 1, qid
    print(qid, "ok")


def check_roman(qid, truths):
    assert len(QS[qid]["options"]) == 8, qid
    assert QS[qid]["answer"] == ROMAN_IDX[tuple(int(bool(t)) for t in truths)], f"{qid}: {truths}"
    print(qid, "ok")


def prob(space, event):
    space = list(space)
    return F(sum(1 for w in space if event(w)), len(space))


def opt_vals(qid):
    """Parse options like $\\frac{a}{b}$, $n$, $n$ g, $n\\%$ into Fractions."""
    out = []
    for o in QS[qid]["options"]:
        s = o.replace("\\%", "").replace(" g", "").strip("$")
        if s.startswith("\\frac{"):
            a, b = s[len("\\frac{"):].rstrip("}").split("}{")
            out.append(F(int(a), int(b)))
        else:
            out.append(F(s))
    return out


def set_opts(qid):
    out = []
    for o in QS[qid]["options"]:
        if o.startswith("$\\{"):
            out.append(frozenset(int(t) for t in o.strip("$").strip("\\{}").split(",")))
        else:
            assert "no possible" in o
            out.append(frozenset())
    return out


def mean(xs):
    return F(sum(xs), len(xs))


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return F(xs[n // 2]) if n % 2 else F(xs[n // 2 - 1] + xs[n // 2], 2)


def unique_mode(xs):
    c = Counter(xs)
    m = max(c.values())
    ms = [k for k in c if c[k] == m]
    return ms[0] if len(ms) == 1 and m > 1 else None


def interp(bounds, cf, pos):
    """Value at cumulative position pos by linear interpolation; bounds[0] has cf 0."""
    for i in range(1, len(bounds)):
        if cf[i - 1] <= pos <= cf[i] and cf[i] > cf[i - 1]:
            return bounds[i - 1] + F(pos - cf[i - 1], cf[i] - cf[i - 1]) * (bounds[i] - bounds[i - 1])
    raise ValueError


def cf_at(bounds, cf, x):
    for i in range(1, len(bounds)):
        if bounds[i - 1] <= x <= bounds[i]:
            return cf[i - 1] + F(x - bounds[i - 1], bounds[i] - bounds[i - 1]) * (cf[i] - cf[i - 1])
    raise ValueError


DICE2 = list(product(range(1, 7), repeat=2))

# ---------------- 01: squad ages (brute: any ages consistent give the same mean)
rest8 = 250 - 30 - 34
new3 = 11 * 24 - rest8
check_values("prob-01", opt_vals("prob-01"), F(new3, 3))
# 01b
tenth = 10 * 65 - 8 * 62 - 70
check_values("prob-01b", opt_vals("prob-01b"), F(tenth))

# ---------------- 02: y = a x + b with a, b > 0; brute over a sample data set
a, b = sp.symbols("a b", positive=True)
sol = sp.solve([sp.Eq(8 * a, 20), sp.Eq(12 * a + b, 34)], [a, b], dict=True)
assert len(sol) == 1 and sol[0][b] > 0
A_, B_ = sol[0][a], sol[0][b]
data = [8, 10, 11, 12, 13, 14, 16]  # mean 12, range 8, contains 10
assert mean(data) == 12 and max(data) - min(data) == 8
new = [A_ * x + B_ for x in data]
assert sum(new) / len(new) == 34 and max(new) - min(new) == 20
check_values("prob-02", opt_vals("prob-02"), F(int(A_ * 10 + B_)))
# 02b: an 11-value data set with Q1 (3rd) 11, median 15, Q3 (9th) 18
d = sorted([5, 9, 11, 12, 14, 15, 16, 17, 18, 20, 25])
assert d[2] == 11 and d[5] == 15 and d[8] == 18
nd = sorted(60 - 2 * x for x in d)
check_values("prob-02b", opt_vals("prob-02b"), F(nd[8]))

# ---------------- 03: ordered draws without replacement
bag = ["R"] * 5 + ["B"] * 3
p = prob(permutations(range(8), 2), lambda w: bag[w[0]] == bag[w[1]])
check_values("prob-03", opt_vals("prob-03"), 224 * p)
socks = ["K"] * 4 + ["G"] * 6
p = prob(permutations(range(10), 2), lambda w: socks[w[0]] != socks[w[1]])
check_values("prob-03b", opt_vals("prob-03b"), 75 * p)

# ---------------- 04
arr = set(permutations("LETTER"))
check_values("prob-04", opt_vals("prob-04"), F(sum(1 for a_ in arr if "TT" not in "".join(a_))))
arr = set(permutations("PEPPER"))
assert len(arr) == 60
check_values("prob-04b", opt_vals("prob-04b"), F(sum(1 for a_ in arr if "PP" not in "".join(a_))))

# ---------------- 05: histogram, area = frequency
classes = [(0, 10), (10, 15), (15, 20), (20, 30), (30, 50)]
heights = [F(3, 2), 6, 8, 3, 1]
scale = F(24, 5 * 6)
freqs = [scale * (hi - lo) * h for (lo, hi), h in zip(classes, heights)]
assert all(f.denominator == 1 for f in freqs)
over25 = sum(f * F(max(0, hi - max(lo, 25)), hi - lo) for (lo, hi), f in zip(classes, freqs))
check_values("prob-05", opt_vals("prob-05"), over25)
# 05b
classes = [(100, 120), (120, 130), (130, 140), (140, 160), (160, 200)]
k = sp.symbols("k")
fds = [F(3, 2), 4, k, 3, F(1, 2)]
ksol = sp.solve(sum((hi - lo) * fd for (lo, hi), fd in zip(classes, fds)) - 200, k)
assert ksol == [5]
fds[2] = 5
freqs = [(hi - lo) * fd for (lo, hi), fd in zip(classes, fds)]
bounds = [100] + [hi for _, hi in classes]
cf = [0]
for f in freqs:
    cf.append(cf[-1] + f)
check_values("prob-05b", opt_vals("prob-05b"), interp(bounds, cf, 100))

# ---------------- 06: cumulative frequency
bounds = [15, 20, 25, 30, 35, 40]
cfA = [0, 8, 20, 60, 72, 80]
cfB = [0, 20, 30, 50, 70, 80]
qa = [interp(bounds, cfA, p_) for p_ in (20, 40, 60)]
qb = [interp(bounds, cfB, p_) for p_ in (20, 40, 60)]
assert qa == [25, F(55, 2), 30] and qb == [20, F(55, 2), F(65, 2)]
I = qa[1] == qb[1]
II = (qb[2] - qb[0]) > 2 * (qa[2] - qa[0])
# III: "fastest in B" is not forced: both groups have someone in (15, 20]; a data set with
# A's fastest = 15.5 and B's fastest = 19 matches the table.
III = not (cfA[1] > 0)  # valid only if A had nobody in the first class
check_roman("prob-06", (I, II, III))
# 06b
bh = [0, 10, 20, 30, 40, 50]
cfP = [0, 5, 15, 30, 70, 100]
cfQ = [0, 10, 30, 60, 85, 100]
uqQ = interp(bh, cfQ, 75)
assert uqQ == 36
check_values("prob-06b", opt_vals("prob-06b"), 100 - cf_at(bh, cfP, uqQ))

# ---------------- 07: expected-frequency populations
pop = [("D", "+")] * 9 + [("D", "-")] * 1 + [("N", "+")] * 99 + [("N", "-")] * 891
pos = [x for x in pop if x[1] == "+"]
check_values("prob-07", opt_vals("prob-07"), F(sum(1 for x in pos if x[0] == "D"), len(pos)))
bolts = [("P", 1)] * 30 + [("P", 0)] * 570 + [("Q", 1)] * 40 + [("Q", 0)] * 360
fl = [x for x in bolts if x[1]]
check_values("prob-07b", opt_vals("prob-07b"), F(sum(1 for x in fl if x[0] == "Q"), len(fl)))


# ---------------- 08: turn-taking, exact by restart equation and by series
def first_wins(ps, who):
    miss = 1
    for q_ in ps:
        miss *= 1 - q_
    before = 1
    for q_ in ps[:who]:
        before *= 1 - q_
    return before * ps[who] / (1 - miss)


pA = first_wins([F(1, 6), F(1, 3)], 0)
series = sum(float((F(5, 6) * F(2, 3)) ** r * F(1, 6)) for r in range(300))
assert abs(series - float(pA)) < 1e-12
check_values("prob-08", opt_vals("prob-08"), pA)
pZ = first_wins([F(1, 6)] * 3, 2)
assert sum(first_wins([F(1, 6)] * 3, i) for i in range(3)) == 1
check_values("prob-08b", opt_vals("prob-08b"), pZ)

# ---------------- 09
check_values("prob-09", opt_vals("prob-09"), F(sum(1 for p_ in product(range(10), repeat=4) if len(set(p_)) == 2)))
check_values("prob-09b", opt_vals("prob-09b"), F(sum(1 for p_ in product("RGB", repeat=5) if len(set(p_)) == 3)))

# ---------------- 10 / 10b: correlation (reasoning; modelled facts)
# 10: I causal claim -> invalid; II x=25 outside [2,15] and predicts 115 > 100 -> invalid; III valid
assert not (2 <= 25 <= 15) and 3 * 25 + 40 > 100
check_roman("prob-10", (False, False, True))
# 10b: I association -> valid; II causal -> invalid; III 'could be' confounder -> valid
check_roman("prob-10b", (True, False, True))

# ---------------- 11: 10 equally likely outcomes; A any 5-set, B any 4-set
U = range(10)
I_ok = II_ok = True
III_counter = False
for A in combinations(U, 5):
    A = set(A)
    for B in combinations(U, 4):
        B = set(B)
        I_ok &= F(len(A | B), 10) >= F(1, 2)
        II_ok &= F(len(A & B), 10) <= F(2, 5)
        if not (A & B) and F(0) != F(1, 2) * F(2, 5):
            III_counter = True
check_roman("prob-11", (I_ok, II_ok, not III_counter))
# 11b: overlap x feasible range
feas = [x for x in range(0, 31) if min(18 - x, 15 - x, x, 30 - (33 - x)) >= 0]
assert feas == list(range(3, 16))
I = all(x == 3 for x in feas)
II = all(x == 9 for x in feas if F(x, 30) == F(18, 30) * F(15, 30)) and any(F(x, 30) == F(18, 30) * F(15, 30) for x in feas)
III = all(x - 3 <= 12 for x in feas)
check_roman("prob-11b", (I, II, III))

# ---------------- 12 / 12b: brute force over all lists
L7 = [L for L in combinations_with_replacement(range(1, 60), 7)
      if sum(L) == 70 and L[3] == 9 and unique_mode(L) == 12]
check_values("prob-12", opt_vals("prob-12"), F(max(L[-1] - L[0] for L in L7)))
L6 = [L for L in combinations_with_replacement(range(1, 45), 6)
      if sum(L) == 54 and median(L) == 8 and unique_mode(L) == 5]
check_values("prob-12b", opt_vals("prob-12b"), F(min(L[-1] - L[0] for L in L6)))
# distractor witnesses quoted in solutions
assert unique_mode((5, 5, 7, 9, 13, 15)) == 5 and sum((5, 5, 7, 9, 13, 15)) == 54
assert unique_mode((5, 5, 5, 11, 11, 17)) == 5 and sum((5, 5, 5, 11, 11, 17)) == 54

# ---------------- 13
bag = ["R"] * 3 + ["B"] * 2
pairs = list(combinations(range(5), 2))
cond = [p_ for p_ in pairs if any(bag[i] == "R" for i in p_)]
check_values("prob-13", opt_vals("prob-13"), F(sum(1 for p_ in cond if all(bag[i] == "R" for i in p_)), len(cond)))
cond = [w for w in DICE2 if 6 in w]
check_values("prob-13b", opt_vals("prob-13b"), F(sum(1 for w in cond if sum(w) >= 10), len(cond)))

# ---------------- 14: combining groups
I = F(20 * 60 + 30 * 70, 50) == 66
II = F(30 * 70 - 65, 29) > 70 and F(20 * 60 + 65, 21) > 60  # depends only on the totals
Bex = [72] * 16 + [68] * 12 + [66] * 2
assert len(Bex) == 30 and mean(Bex) == 70 and median(Bex) == 72 and max(Bex) <= 72
Aex = [50] * 9 + [58] * 2 + [70] * 8 + [74]  # a valid class A, for completeness
assert len(Aex) == 20 and mean(Aex) == 60 and median(Aex) == 58
III = False  # counterexample Bex
check_roman("prob-14", (I, II, III))
# 14b
I = F(10 * 30 + 15 * 20, 25) == 25
Pex = [27] * 4 + [32] * 6
assert mean(Pex) == 30 and median(Pex) == 32 and max(Pex) <= 32
II = False
# III: brute-check on many Q sets: mean rises, median unchanged
import random
random.seed(1)
III = True
cnt = 0
while cnt < 2000:
    lo = [random.randint(0, 18) for _ in range(7)]
    hi = [random.randint(18, 40) for _ in range(6)]
    last = 300 - sum(lo) - 18 - sum(hi)
    if last < max(hi):
        continue
    Qd = sorted(lo + [18] + hi + [last])
    assert sum(Qd) == 300 and Qd[7] == 18
    cnt += 1
    Q2 = Qd[:-1] + [Qd[-1] + 10]
    III &= mean(Q2) > mean(Qd) and median(Q2) == median(Qd)
check_roman("prob-14b", (I, II, III))


# ---------------- 15
def indep(space, X, Y):
    return prob(space, lambda w: X(w) and Y(w)) == prob(space, X) * prob(space, Y)


A = lambda w: w[0] % 2 == 0
B = lambda w: sum(w) == 7
C = lambda w: sum(w) == 8
check_roman("prob-15", (indep(DICE2, A, B), indep(DICE2, A, C), indep(DICE2, B, C)))
cards = range(1, 13)
A = lambda n: n % 2 == 0
B = lambda n: n % 3 == 0
C = lambda n: n <= 8
check_roman("prob-15b", (indep(cards, A, B), indep(cards, A, C), indep(cards, B, C)))


# ---------------- 16
def solve_n(k, target, same):
    out = []
    for n in range(0, 300):
        balls = ["X"] * n + ["Y"] * k
        ps = list(combinations(range(len(balls)), 2))
        if len(ps) == 0:
            continue
        hit = sum(1 for p_ in ps if (balls[p_[0]] == balls[p_[1]]) == same)
        if F(hit, len(ps)) == target:
            out.append(n)
    return frozenset(out)


check_values("prob-16", set_opts("prob-16"), solve_n(3, F(1, 2), True))
assert all(n >= 1 for n in solve_n(4, F(8, 15), False))
check_values("prob-16b", set_opts("prob-16b"), solve_n(4, F(8, 15), False))

# ---------------- 17
good = tot = 0
for p_ in permutations(range(6)):
    tot += 1
    if all(abs(p_.index(k_) - p_.index(k_ ^ 1)) != 1 for k_ in (0, 2, 4)):
        good += 1
check_values("prob-17", opt_vals("prob-17"), F(good, tot))
der = sum(1 for p_ in permutations(range(5)) if all(p_[i] != i for i in range(5)))
check_values("prob-17b", opt_vals("prob-17b"), F(der, 120))

# ---------------- 18: hexagon
V = [(sp.cos(sp.pi * k_ / 3), sp.sin(sp.pi * k_ / 3)) for k_ in range(6)]
O = (0, 0)


def cross(o, a_, b_):
    return sp.nsimplify((a_[0] - o[0]) * (b_[1] - o[1]) - (a_[1] - o[1]) * (b_[0] - o[0]))


def d2(a_, b_):
    return sp.nsimplify(sum((x - y) ** 2 for x, y in zip(a_, b_)))


tris = list(combinations(range(6), 3))
inside_or_on = right = isos = 0
for t in tris:
    P, Qp, R = (V[i] for i in t)
    s = [cross(P, Qp, O), cross(Qp, R, O), cross(R, P, O)]
    if all(x >= 0 for x in s) or all(x <= 0 for x in s):
        inside_or_on += 1
    sides = sorted([d2(P, Qp), d2(Qp, R), d2(R, P)], key=float)
    if sp.simplify(sides[0] + sides[1] - sides[2]) == 0:
        right += 1
    if len(set(sides)) < 3:
        isos += 1
n = len(tris)
check_roman("prob-18", (F(inside_or_on, n) == F(1, 2), F(right, n) == F(3, 5), F(isos, n) == F(2, 5)))
# 18b: cube
cube = list(product((0, 1), repeat=3))
eq = rt = iso = 0
tris = list(combinations(cube, 3))
for t in tris:
    s = sorted(sum((x - y) ** 2 for x, y in zip(t[i], t[j])) for i, j in ((0, 1), (1, 2), (0, 2)))
    eq += s[0] == s[2]
    rt += s[0] + s[1] == s[2]
    iso += len(set(s)) < 3
n = len(tris)
assert (n, eq, rt, iso) == (56, 8, 48, 32)
check_roman("prob-18b", (F(eq, n) == F(1, 7), F(rt, n) == F(6, 7), F(iso, n) == F(3, 7)))

# ---------------- structure: families, difficulty spread, twins
originals = [QS[i] for i in IDS]
assert Counter(q["difficulty"] for q in originals) == Counter({2: 2, 3: 6, 4: 6, 5: 4})
for i in IDS:
    x, y = QS[i], QS[i + "b"]
    assert x["family"] == i and y["family"] == i, i
    assert x["difficulty"] == y["difficulty"], i
    assert x["answer"] != y["answer"], f"{i}: twin has same answer letter"
    assert x["stem"] != y["stem"]
for q in QL:
    assert 1 < q["difficulty"] <= 5
    assert len(q["options"]) == 5 or len(q["options"]) == 8, q["id"]
    wrong = [k_ for k_ in q["distractors"] if int(k_) != q["answer"]]
    assert len(wrong) >= 3, q["id"]
print("ALL OK")
