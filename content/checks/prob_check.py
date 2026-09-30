"""Verification for content/questions/prob.json.

Every answer is brute-forced by enumerating the sample space (or all arrangements /
selections), and every distractor is checked to be wrong.
"""
import json
import os
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "prob.json"), encoding="utf-8"))}
assert len(QS) == 18 and all(f"prob-{i:02d}" in QS for i in range(1, 19))

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
    assert QS[qid]["answer"] == ROMAN_IDX[tuple(int(bool(t)) for t in truths)], f"{qid}: {truths}"
    print(qid, "ok")


def prob(space, event):
    space = list(space)
    return F(sum(1 for w in space if event(w)), len(space))


def frac_opts(qid):
    """Parse options of the form $\\frac{a}{b}$ into Fractions."""
    out = []
    for o in QS[qid]["options"]:
        a, b = o.replace("$\\frac{", "").rstrip("}$").split("}{")
        out.append(F(int(a), int(b)))
    return out


DICE2 = list(product(range(1, 7), repeat=2))

# 01
check_values("prob-01", frac_opts("prob-01"), prob(DICE2, lambda w: sum(w) == 8))

# 02
check_values("prob-02", frac_opts("prob-02"), prob(product("HT", repeat=3), lambda w: "H" in w))

# 03: label counters, ordered draws without replacement
bag = ["R"] * 5 + ["B"] * 3
draws = list(permutations(range(8), 2))
check_values("prob-03", frac_opts("prob-03"), prob(draws, lambda w: bag[w[0]] == bag[w[1]]))

# 04: LETTER arrangements, T's not adjacent
arr = set(permutations("LETTER"))
assert len(arr) == 180
good = [a for a in arr if "TT" not in "".join(a)]
check_values("prob-04", [60, 90, 120, 180, 240], len(good))

# 05: committees with at least one woman
people = ["M"] * 5 + ["W"] * 4
comms = list(combinations(range(9), 3))
check_values("prob-05", [30, 40, 74, 84, 112], sum(1 for c in comms if any(people[i] == "W" for i in c)))

# 06: expected gain
E = sum(F(1, 6) * (s if s % 2 == 0 else -3) for s in range(1, 7))
check_values("prob-06", [F(-3, 2), F(0), F(1, 2), F(3, 2), F(2)], E)

# 07: disease test via a population of 1000 (exact frequencies)
pop = [("D", "+")] * 9 + [("D", "-")] * 1 + [("N", "+")] * 99 + [("N", "-")] * 891
pos = [p for p in pop if p[1] == "+"]
check_values("prob-07", frac_opts("prob-07"), F(sum(1 for p in pos if p[0] == "D"), len(pos)))

# 08: first to roll a six; enumerate games by length exactly and solve exactly
p_exact = sp.Rational(1, 6) / (1 - sp.Rational(25, 36))
partial = sum(F(5, 6) ** (k - 1) * F(1, 6) for k in range(1, 400, 2))  # Ann wins on odd rolls
assert abs(float(partial) - float(p_exact)) < 1e-15
p_exact = F(int(sp.numer(p_exact)), int(sp.denom(p_exact)))
check_values("prob-08", frac_opts("prob-08"), p_exact)

# 09: PINs with exactly two distinct digits
check_values("prob-09", [270, 540, 630, 1260, 5040], sum(1 for p in product(range(10), repeat=4) if len(set(p)) == 2))

# 10: six rolls; the argument's value 1 is wrong, rolls independent, events overlap
rolls = list(product(range(1, 7), repeat=6))
p_any = prob(rolls, lambda w: 6 in w)
assert p_any == 1 - F(5, 6) ** 6 and p_any != 1
assert prob(rolls, lambda w: w[0] == 6 and w[1] == 6) == F(1, 36)  # overlap, and independence holds
assert prob(rolls, lambda w: w[0] == 6 and w[1] == 6) == prob(rolls, lambda w: w[0] == 6) * prob(rolls, lambda w: w[1] == 6)
assert F(1, 6) ** 6 != p_any
assert QS["prob-10"]["answer"] == 1
print("prob-10 ok")

# 11: 10 equally likely outcomes; A any 5-set, B any 4-set -> check I, II; III counterexample
U = range(10)
I_ok = II_ok = True
III_counter = False
for A in combinations(U, 5):
    A = set(A)
    for B in combinations(U, 4):
        B = set(B)
        pU = F(len(A | B), 10); pI = F(len(A & B), 10)
        I_ok &= pU >= F(1, 2)
        II_ok &= pI <= F(2, 5)
        if not (A & B) and pI != F(1, 2) * F(2, 5):
            III_counter = True
check_roman("prob-11", (I_ok, II_ok, not III_counter))

# 12: geometric probability on an exact midpoint grid (boundaries at multiples of 1/4)
N = 400
cnt = 0
for i in range(N):
    for j in range(N):
        x = F(2 * i + 1, 2 * N); y = F(2 * j + 1, 2 * N)
        if min(x, y, 1 - x, 1 - y) < F(1, 4):
            cnt += 1
check_values("prob-12", frac_opts("prob-12"), F(cnt, N * N))

# 13: 3 red 2 blue, conditional
bag = ["R"] * 3 + ["B"] * 2
pairs = list(combinations(range(5), 2))
cond = [p for p in pairs if any(bag[i] == "R" for i in p)]
check_values("prob-13", frac_opts("prob-13"), F(sum(1 for p in cond if all(bag[i] == "R" for i in p)), len(cond)))

# 14: no two consecutive from 1..10
check_values("prob-14", [48, 56, 64, 84, 120],
             sum(1 for c in combinations(range(1, 11), 3) if c[1] - c[0] > 1 and c[2] - c[1] > 1))

# 15: independence on two dice
A = lambda w: w[0] % 2 == 0
B = lambda w: sum(w) == 7
C = lambda w: sum(w) == 8
indep = lambda X, Y: prob(DICE2, lambda w: X(w) and Y(w)) == prob(DICE2, X) * prob(DICE2, Y)
check_roman("prob-15", (indep(A, B), indep(A, C), indep(B, C)))

# 16: n red, 3 blue, P(same) = 1/2
sols = []
for n in range(0, 300):
    balls = ["R"] * n + ["B"] * 3
    ps = list(combinations(range(len(balls)), 2))
    if F(sum(1 for p in ps if balls[p[0]] == balls[p[1]]), len(ps)) == F(1, 2):
        sols.append(n)
opt_sets = [frozenset(int(t) for t in o.strip("$\\{}").split(",")) for o in QS["prob-16"]["options"]]
check_values("prob-16", opt_sets, frozenset(sols))

# 17: three couples in a row
good = 0
tot = 0
for p in permutations(range(6)):  # person k's partner is k^1
    tot += 1
    if all(abs(p.index(k) - p.index(k ^ 1)) != 1 for k in (0, 2, 4)):
        good += 1
check_values("prob-17", frac_opts("prob-17"), F(good, tot))

# 18: hexagon triangles, exact coordinates
V = [(sp.cos(sp.pi * k / 3), sp.sin(sp.pi * k / 3)) for k in range(6)]
O = (0, 0)


def cross(o, a, b):
    return sp.nsimplify((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))


def d2(a, b):
    return sp.nsimplify((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


tris = list(combinations(range(6), 3))
inside_or_on = right = isos = 0
for t in tris:
    P, Q, R = (V[i] for i in t)
    s = [cross(P, Q, O), cross(Q, R, O), cross(R, P, O)]
    if all(x >= 0 for x in s) or all(x <= 0 for x in s):
        inside_or_on += 1
    sides = sorted([d2(P, Q), d2(Q, R), d2(R, P)], key=lambda z: float(z))
    if sp.simplify(sides[0] + sides[1] - sides[2]) == 0:
        right += 1
    if len({sp.nsimplify(x) for x in sides}) < 3:
        isos += 1
assert (inside_or_on, right, isos) == (14, 12, 8)
n = len(tris)
check_roman("prob-18", (F(inside_or_on, n) == F(1, 2), F(right, n) == F(3, 5), F(isos, n) == F(2, 5)))

assert Counter(q["difficulty"] for q in QS.values()) == Counter({1: 2, 2: 4, 3: 6, 4: 4, 5: 2})
print("ALL OK")
