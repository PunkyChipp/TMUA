"""Verification for content/questions/seq.json (originals + twins). Run: python3 content/checks/seq_check.py"""
import json
import os
from collections import Counter
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QL = json.load(open(os.path.join(HERE, "..", "questions", "seq.json"), encoding="utf-8"))
QS = {q["id"]: q for q in QL}
x, d, a, r, n = sp.symbols("x d a r n")
done = set()


def key(qid, values, truth):
    """values: value of each option; exactly the keyed option must equal truth."""
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    hits = [i for i, v in enumerate(values) if sp.simplify(sp.nsimplify(v) - sp.nsimplify(truth)) == 0]
    assert hits == [q["answer"]], (qid, hits, q["answer"])
    assert len(set(map(str, values))) == len(values), (qid, "options not distinct")
    done.add(qid)


def key_pred(qid, preds, truth, grid):
    hits = [i for i, p in enumerate(preds) if all(p(v) == truth(v) for v in grid)]
    assert hits == [QS[qid]["answer"]], (qid, hits)
    done.add(qid)


def key_roman(qid, I, II, III):
    table = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4,
             (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}
    assert QS[qid]["answer"] == table[(int(I), int(II), int(III))], qid
    done.add(qid)


def coeff(expr, k):
    return sp.Poly(sp.expand(expr), x).coeff_monomial(x**k)


# seq-01: AP, u4 = 13, u9 = 28, S10
dd = F(28 - 13, 5); a1 = 13 - 3 * dd
key("seq-01", [145, 175, 190, 205, 350], sum(a1 + k * dd for k in range(10)))
assert 5 * (1 + 28) == 145 and 5 * (4 + 34) == 190 and 10 * F(13 + 28, 2) == 205

# seq-01b: rows 12, +3; total 810
m = 1
while sum(12 + 3 * k for k in range(m)) < 810:
    m += 1
assert sum(12 + 3 * k for k in range(m)) == 810
key("seq-01b", [12, 15, 20, 23, 27], m)
assert 15 * (12 + 3 * 14) == 810  # distractor: n * last row

# seq-02: 2, 7, 14, 23 quadratic
u2 = lambda k: k * k + 2 * k - 1
assert [u2(k) for k in range(1, 5)] == [2, 7, 14, 23]
first = next(k for k in range(1, 200) if u2(k) > 1000)
key("seq-02", [23, 30, 31, 32, 45], first)
assert next(k for k in range(1, 200) if 2 * k * k - k + 1 > 1000) == 23

# seq-02b: 3, 9, 17, 27, 39
u2b = lambda k: k * k + 3 * k - 1
assert [u2b(k) for k in range(1, 6)] == [3, 9, 17, 27, 39]
key("seq-02b", [31, 43, 44, 45, 63], sum(1 for k in range(1, 500) if u2b(k) < 2000))
assert sum(1 for k in range(1, 500) if 2 * k * k + 1 < 2000) == 31

# seq-03
key("seq-03", [7350, 14700, 15000, 15050, 22500], sum(k for k in range(1, 301) if k % 2 and k % 3))

# seq-03b
key("seq-03b", [2003, 2318, 2418, 2633, 4950], sum(k for k in range(1, 100) if k % 3 == 0 or k % 5 == 0))

# seq-04: (1+ax)^n with coefficients 12, 60
sols = [(nn, aa) for nn in range(1, 50) for aa in [F(12, nn)] if F(nn * (nn - 1), 2) * aa**2 == 60]
assert sols == [(6, 2)], sols
key("seq-04", [40, 80, 160, 240, 480], coeff((1 + 2 * x) ** 6, 3))

# seq-04b
k = sp.symbols("k")
ks = [s for s in sp.solve(sp.Eq(coeff((3 + k * x) ** 6, 2), coeff((3 + k * x) ** 6, 3)), k) if s != 0]
assert len(ks) == 1
key("seq-04b", [F(1, 4), F(3, 4), F(4, 3), F(9, 4), 4], ks[0])

# seq-05
e = sp.expand((x**2 - 2 / x) ** 6)
key("seq-05", [-240, -160, 15, 60, 240], sum(t for t in e.as_ordered_terms() if not t.has(x)))

# seq-05b
e = sp.expand((x - 3 / x) ** 8)
key("seq-05b", [-1512, -504, -168, 168, 1512], e.coeff(x, 2))

# seq-06: P_{n+1} = 0.8 P_n + 100, P_0 = 1000
P = [F(1000)]
for _ in range(15):
    P.append(F(4, 5) * P[-1] + 100)
q8 = F(4, 5)
forms = [lambda m: 1000 * q8**m + 100 * m, lambda m: 500 + 500 * q8 ** (m - 1), lambda m: 1000 * q8**m + 500,
         lambda m: 500 + 500 * q8**m, lambda m: 1000 * q8**m + 125 * (1 - q8**m)]
hits = [i for i, f in enumerate(forms) if all(f(m) == P[m] for m in range(16))]
assert hits == [QS["seq-06"]["answer"]], hits
done.add("seq-06")

# seq-06b: A_{n+1} = A_n/4 + 200, sup = 800/3, never attained
A = [F(200)]
for _ in range(60):
    A.append(A[-1] / 4 + 200)
L = F(800, 3)
assert all(v < L for v in A) and L - A[-1] < F(1, 10**30)
assert all(A[i] < A[i + 1] for i in range(60))
key("seq-06b", [F(200, 3), 250, F(800, 3), 400, 800], L)

# seq-07
s7 = [F(2)]
for _ in range(99):
    s7.append(1 / (1 - s7[-1]))
key("seq-07", [F(97, 2), F(99, 2), 50, F(103, 2), 53], sum(s7))

# seq-07b
s = [F(2)]
for _ in range(49):
    s.append((1 + s[-1]) / (1 - s[-1]))
key("seq-07b", [-6, -3, 1, 2, 6], sp.prod(s))


# seq-08 / 08b: compare truth sets with option predicates on a fine grid
def t8(v):
    rv = (2 * v - 1) / 3
    return abs(rv) < 1 and 1 / (1 - rv) > 2


grid = [F(kk, 97) for kk in range(-1000, 1000)]
key_pred("seq-08", [lambda v: v > F(5, 4), lambda v: F(5, 4) < v < 2, lambda v: -1 < v < 2,
                    lambda v: -1 < v < F(5, 4), lambda v: F(1, 2) < v < 2], t8, grid)


def t8b(v):
    rv = (v - 3) / 2
    return abs(rv) < 1 and 2 / (1 - rv) > 2


# check series really is 2 * r^n with r = (x-3)/2
xv = F(7, 2)
assert [2 * ((xv - 3) / 2) ** j for j in range(4)] == [2, xv - 3, (xv - 3) ** 2 / 2, (xv - 3) ** 3 / 4]
key_pred("seq-08b", [lambda v: v > 3, lambda v: 1 < v < 3, lambda v: 1 < v < 5, lambda v: 3 < v < 5,
                     lambda v: 3 < v < 7], t8b, grid)

# seq-09 / 09b
key("seq-09", [25, 30, 40, 45, 51], coeff((1 + x + x**2) ** 5, 4))
assert coeff((1 + x + x**2) ** 5, 5) == 51
key("seq-09b", [-24, -8, 8, 32, 56], coeff((1 + 2 * x - x**2) ** 4, 3))

# seq-10 / 10b
p10 = sp.Poly(sp.expand((2 - x) ** 7), x)
key("seq-10", [-2186, -1094, -1093, 1093, 1094], sum(p10.coeff_monomial(x**j) for j in (1, 3, 5, 7)))
p10b = sp.Poly(sp.expand((1 + x + x**2) ** 4), x)
key("seq-10b", [40, 41, 80, 81, 82], sum(p10b.coeff_monomial(x**j) for j in (0, 2, 4, 6, 8)))

# seq-11: brute force over rational a, d
sol11 = sp.solve([(a + d) ** 2 - a * (a + 3 * d), 10 * (2 * a + 19 * d) - 420], [a, d], dict=True)
sol11 = [s_ for s_ in sol11 if s_[d] != 0]
assert len(sol11) == 1
g1, g2 = sol11[0][a], sol11[0][a] + sol11[0][d]
rr = g2 / g1
assert sp.simplify(sol11[0][a] + 3 * sol11[0][d] - g1 * rr**2) == 0
key("seq-11", [62, 64, 126, 128, 254], sum(g1 * rr**j for j in range(6)))

# seq-11b
sol11b = sp.solve([(a + 2 * d) ** 2 - a * (a + 8 * d)], [a], dict=True)
ratios = []
for s_ in sol11b:
    aa = s_[a]
    if sp.simplify(aa) == 0:
        continue  # a = 0 gives GP starting with 0: not a geometric sequence
    rr = sp.simplify((aa + 2 * d) / aa)
    dval = sp.solve(sum(aa * rr**j for j in range(4)) - 160, d)
    ratios += [(aa.subs(d, dv), dv) for dv in dval if dv != 0]
assert len(ratios) == 1
a0, d0 = ratios[0]
key("seq-11b", [180, 220, 240, 440, 880], sum(a0 + j * d0 for j in range(10)))

# seq-12
A_, D_, R_ = sp.symbols("A D R", positive=True)
I = sp.simplify(2 ** (A_ + 2 * D_) / 2 ** (A_ + D_) - 2 ** (A_ + D_) / 2 ** A_) == 0
II = sp.simplify(sp.expand_log(sp.log(A_ * R_**2) - 2 * sp.log(A_ * R_) + sp.log(A_), force=True)) == 0
w = [1 + 2**j for j in range(3)]
III = F(w[1], w[0]) == F(w[2], w[1])
key_roman("seq-12", I, II, III)

# seq-12b
u = lambda m: a + (m - 1) * d
v = lambda m: sp.Symbol("b") + (m - 1) * sp.Symbol("e")
I = sp.simplify(u(2 * n + 2) - u(2 * n) - (u(2 * n + 4) - u(2 * n + 2))) == 0
II = [j * j for j in range(1, 4)]
II = (II[1] - II[0]) == (II[2] - II[1])
III = sp.expand((u(n + 1) + 2 * v(n + 1)) - (u(n) + 2 * v(n))).free_symbols.isdisjoint({n})
key_roman("seq-12b", I, II, III)


# seq-13
def geometric_k(kv):
    S = lambda m: 2 ** (m + 1) + kv
    terms = [S(1)] + [S(m) - S(m - 1) for m in range(2, 9)]
    if any(t == 0 for t in terms):
        return False
    return all(F(terms[i + 1], terms[i]) == F(terms[1], terms[0]) for i in range(len(terms) - 1))


assert [kv for kv in range(-20, 21) if geometric_k(kv)] == [-2]
assert [-4, -2, -1, 0][QS["seq-13"]["answer"]] == -2
done.add("seq-13")


# seq-13b
def arith_c(cv):
    S = lambda m: m * m + 4 * m + cv
    terms = [S(1)] + [S(m) - S(m - 1) for m in range(2, 10)]
    return len({terms[i + 1] - terms[i] for i in range(len(terms) - 1)}) == 1


assert [cv for cv in range(-20, 21) if arith_c(cv)] == [0]
assert [-5, -1, 0, 5][QS["seq-13b"]["answer"]] == 0
done.add("seq-13b")

# seq-14
sol = [s_ for s_ in sp.solve([a / (1 - r) - 3, a**2 / (1 - r**2) - 3], [a, r], dict=True) if abs(s_[r]) < 1]
assert len(sol) == 1
key("seq-14", [F(9, 4), 3, F(27, 8), F(27, 7), 9], sp.simplify(sol[0][a] ** 3 / (1 - sol[0][r] ** 3)))

# seq-14b
sol = [s_ for s_ in sp.solve([a / (1 - r) - 8, a * r / (1 - r**2) - F(8, 3)], [a, r], dict=True) if abs(s_[r]) < 1]
assert len(sol) == 1
key("seq-14b", [2, F(8, 3), 4, F(16, 3), 6], sol[0][a])

# seq-15
cnt = sum(1 for j in range(13) if (sp.binomial(12, j) * sp.sqrt(2) ** (12 - j) * sp.root(3, 3) ** j).is_rational)
key("seq-15", [2, 3, 4, 5, 7], cnt)

# seq-15b
xp = sp.symbols("xp", positive=True)
terms = sp.Add.make_args(sp.expand((xp + 2 / sp.sqrt(xp)) ** 10))
assert len(terms) == 11
cnt = sum(1 for t in terms if sp.Rational(t.as_coeff_exponent(xp)[1]).q == 1)
key("seq-15b", [4, 5, 6, 7, 11], cnt)

# seq-16 / 16b
key("seq-16", [5120, 14080, 25600, 28160, 56320], sum(j * j * sp.binomial(10, j) for j in range(11)))
key("seq-16b", [3072, 6144, 18432, 24576, 73728], sum(j * sp.binomial(6, j) * 3**j for j in range(7)))


# seq-17 / 17b: brute force
def ways(N):
    c = 0
    for start in range(1, N):
        tot, m = 0, start
        while tot < N:
            tot += m; m += 1
        if tot == N and m - start >= 2:
            c += 1
    return c


key("seq-17", [2, 3, 4, 7, 15], ways(1000))
key("seq-17b", [4, 5, 6, 15, 25], sum(1 for N in range(1, 51) if ways(N) == 0))


# seq-18
def run(f, k0, N=60):
    vv = [k0]
    for _ in range(N):
        vv.append(f(vv[-1]))
    return vv


f18 = lambda t: t * t - 2
I = all(t == 2 for t in run(f18, F(0), 10)[2:])
II = all(all(vv[i + 1] > vv[i] for i in range(6)) for vv in (run(f18, kv, 6) for kv in [-2.0001, -2.1, -2.5, -3, -10]))
k0 = (sp.sqrt(5) - 1) / 2
assert sp.simplify(f18(f18(k0)) - k0) == 0 and sp.simplify(f18(k0) - k0) != 0 and -2 < k0 < 2
III = False  # genuine 2-cycle inside (-2, 2): does not converge
key_roman("seq-18", I, II, III)

# seq-18b
f18b = lambda t: 2 * t - t * t
I = all(all(vv[i + 1] > vv[i] for i in range(10)) for vv in (run(f18b, F(kk, 10), 10) for kk in range(1, 20)))
vv = run(f18b, F(2), 10)
II = all(t == 0 for t in vv[1:])
III = all(all(vv[i + 1] < vv[i] for i in range(8)) for vv in (run(f18b, kv, 8) for kv in [F(201, 100), F(5, 2), F(3), F(7)]))
assert not I  # k = 3/2 gives u2 = 3/4
key_roman("seq-18b", I, II, III)

# ---------------- metadata ----------------
assert done == set(QS), sorted(set(QS) - done)
orig = [q for q in QL if not q["id"].endswith("b")]
assert sorted(q["id"] for q in orig) == [f"seq-{i:02d}" for i in range(1, 19)]
assert sorted(Counter(q["difficulty"] for q in orig).items()) == [(2, 2), (3, 6), (4, 7), (5, 3)]
for q in orig:
    t = QS[q["id"] + "b"]
    assert t["difficulty"] == q["difficulty"], q["id"]
    assert t["answer"] != q["answer"], q["id"]
    assert q["family"] == t["family"] == q["id"]
for q in QL:
    no = len(q["options"])
    assert no == 5 or q["options"][0] == "none of them", q["id"]
    assert len(set(q["options"])) == no and 0 <= q["answer"] < no
    assert q["difficulty"] >= 2
    assert len(q["distractors"]) >= 3 and all(int(kk) != q["answer"] for kk in q["distractors"]), q["id"]
print("ALL OK")
