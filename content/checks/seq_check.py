"""Verification for content/questions/seq.json. Run: python3 content/checks/seq_check.py"""
import json
import os
from fractions import Fraction as F
from itertools import product

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "seq.json"), encoding="utf-8"))}
x, d, a, r = sp.symbols("x d a r")


def key(qid, values, truth):
    """values: numeric value of each option; truth: correct value. Exactly one option must match."""
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    hits = [i for i, v in enumerate(values) if sp.simplify(sp.nsimplify(v) - sp.nsimplify(truth)) == 0]
    assert hits == [q["answer"]], (qid, hits, q["answer"])
    assert len(set(map(str, values))) == len(values), (qid, "options not distinct")


def key_roman(qid, I, II, III):
    table = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4,
             (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}
    assert QS[qid]["answer"] == table[(int(I), int(II), int(III))], qid


# seq-01
dd = F(31 - 11, 5); a1 = 11 - 2 * dd
S10 = sum(a1 + k * dd for k in range(10))
key("seq-01", [190, 210, 230, 290, 420], S10)

# seq-02
t, s = F(12), F(0)
for _ in range(200):
    s += t; t *= F(-1, 2)
assert abs(s - 8) < F(1, 10**30)
key("seq-02", [4, 8, 12, 16, 24], 8)

# seq-03
key("seq-03", [570, 588, 590, 628, 630], sum(3 * k - 2 for k in range(1, 21)))

# seq-04
key("seq-04", [-560, -280, -35, 280, 560], sp.expand((2 - x) ** 7).coeff(x, 3))

# seq-05
e = sp.expand((x**2 - 2 / x) ** 6)
const = sum(t for t in e.as_ordered_terms() if not t.has(x))
key("seq-05", [-240, -160, 15, 60, 240], const)

# seq-06: all three must hold for every d
u = lambda n: 7 + (n - 5) * d
I = sp.simplify(u(1) + u(9) - 14) == 0
II = sp.simplify(sum(u(n) for n in range(1, 10)) - 63) == 0
III = sp.expand(49 - u(3) * u(7)) == 4 * d**2  # >= 0 always
key_roman("seq-06", I, II, III)

# seq-07
seq = [F(2)]
for _ in range(99):
    seq.append(1 / (1 - seq[-1]))
key("seq-07", [F(97, 2), F(99, 2), 50, F(103, 2), 53], sum(seq))

# seq-08: sample x values; compare truth set with each option predicate
def truth8(xv):
    rv = (2 * xv - 1) / 3
    return abs(rv) < 1 and 1 / (1 - rv) > 2
opts8 = [lambda v: v > F(5, 4), lambda v: F(5, 4) < v < 2, lambda v: -1 < v < 2,
         lambda v: -1 < v < F(5, 4), lambda v: 1 < v < 2]
grid = [F(k, 97) for k in range(-500, 500)]
match8 = [i for i, p in enumerate(opts8) if all(p(v) == truth8(v) for v in grid)]
assert match8 == [QS["seq-08"]["answer"]], match8

# seq-09
key("seq-09", [-9, -3, 3, 21, 45], sp.expand((1 + x) ** 6 * (1 - x) ** 4).coeff(x, 2))

# seq-10
p10 = sp.Poly(sp.expand((1 + 2 * x) ** 6), x)
key("seq-10", [32, 364, 365, 729, 730], sum(p10.coeff_monomial(x**k) for k in (0, 2, 4, 6)))

# seq-11
n = 1
while sum(50 - 3 * k for k in range(n)) >= 0:
    n += 1
key("seq-11", [17, 18, 34, 35, 36], n)

# seq-12
A, D, R = sp.symbols("A D R", positive=True)
I = sp.simplify(2 ** (A + 2 * D) / 2 ** (A + D) - 2 ** (A + D) / 2 ** A) == 0
II = sp.simplify(sp.expand_log(sp.log(A * R**2) - 2 * sp.log(A * R) + sp.log(A), force=True)) == 0
w = [1 + 2**k for k in range(3)]  # u_n = 1, v_n = 2^(n-1)
III = F(w[1], w[0]) == F(w[2], w[1])
key_roman("seq-12", I, II, III)

# seq-13: which k make the sequence geometric (check first 8 terms)
def geometric_k(kv):
    S = lambda m: 2 ** (m + 1) + kv
    terms = [S(1)] + [S(m) - S(m - 1) for m in range(2, 9)]
    if any(t == 0 for t in terms):
        return False
    return all(F(terms[i + 1], terms[i]) == F(terms[1], terms[0]) for i in range(len(terms) - 1))
good = [kv for kv in range(-20, 21) if geometric_k(kv)]
assert good == [-2]
ans13 = QS["seq-13"]["answer"]
assert [-4, -2, -1, 0, 2][ans13] == -2

# seq-14
sol = sp.solve([a / (1 - r) - 3, a**2 / (1 - r**2) - 3], [a, r], dict=True)
sol = [s_ for s_ in sol if abs(s_[r]) < 1]
assert len(sol) == 1
key("seq-14", [F(9, 4), 3, F(27, 8), F(27, 7), 9], sp.simplify(sol[0][a] ** 3 / (1 - sol[0][r] ** 3)))

# seq-15
count = sum(1 for k in range(13) if (sp.binomial(12, k) * sp.sqrt(2) ** (12 - k) * sp.root(3, 3) ** k).is_rational)
key("seq-15", [1, 2, 3, 4, 5, 7], count)

# seq-16
key("seq-16", [256, 512, 1024, 2048, 4096], sum(k * sp.binomial(8, k) for k in range(9)))

# seq-17: brute force
ways = 0
for start in range(1, 1000):
    tot, m = 0, start
    while tot < 1000:
        tot += m; m += 1
    if tot == 1000 and m - start >= 2:
        ways += 1
key("seq-17", [1, 2, 3, 4, 5, 6], ways)

# seq-18
def run(k, N=60):
    v = [k]
    for _ in range(N):
        v.append(v[-1] ** 2 - 2)
    return v
v = run(F(0), 10)
I = all(t == 2 for t in v[2:])
II = True
for kv in [-2.0001, -2.1, -2.5, -3, -5, -10]:
    vv = run(kv, 6)
    II &= all(vv[i + 1] > vv[i] for i in range(6))
k0 = (sp.sqrt(5) - 1) / 2
u2 = sp.simplify(k0**2 - 2); u3 = sp.simplify(u2**2 - 2)
assert sp.simplify(u3 - k0) == 0 and sp.simplify(u2 - k0) != 0 and -2 < k0 < 2
III = False  # counterexample above: genuine 2-cycle, does not converge
key_roman("seq-18", I, II, III)

# metadata checks
diffs = sorted(q["difficulty"] for q in QS.values())
assert diffs == [1] * 2 + [2] * 4 + [3] * 6 + [4] * 4 + [5] * 2, diffs
assert sorted(QS) == [f"seq-{i:02d}" for i in range(1, 19)]
for q in QS.values():
    assert 4 <= len(q["options"]) <= 8 and len(set(q["options"])) == len(q["options"])
    assert 0 <= q["answer"] < len(q["options"])
    assert len(q["distractors"]) >= 2 and all(int(k) != q["answer"] for k in q["distractors"])
print("ALL OK")
