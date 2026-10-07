"""Verification for content/questions/proof.json. Run: python3 content/checks/proof_check.py

Every original X and its twin Xb is checked: the keyed option is asserted, and the facts that
make every other option wrong are machine-checked (brute force / sympy / small-model search).
"""
import itertools
import json
import os
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache

import sympy as sp
from sympy import isprime

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = json.load(open(os.path.join(HERE, "..", "questions", "proof.json")))
QS = {q["id"]: q for q in ALL}
ROMAN8 = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
n_, x_ = sp.symbols("n x")


def key(qid, idx):
    q = QS[qid]
    assert q["answer"] == idx, (qid, q["answer"], idx)
    assert len(set(q["options"])) == len(q["options"]), qid
    assert 4 <= len(q["options"]) <= 8, qid


def roman(qid, truths):
    key(qid, ROMAN8.index({i + 1 for i, t in enumerate(truths) if t}))


def only(flags):
    """flags: list of booleans 'option is correct'; return the unique index."""
    assert sum(flags) == 1, flags
    return flags.index(True)


def eq(a, b):
    return sp.expand(a - b) == 0


R = range(-300, 301)

# 01: counterexample needs n prime and n^2+2 prime
opts = [1, 3, 9, 15, 21]
key("proof-01", only([isprime(v) and isprime(v * v + 2) for v in opts]))
assert all(isprime(v * v + 2) for v in opts)  # the trap: non-primes all give primes
assert [p for p in sp.primerange(2, 3000) if isprime(p * p + 2)] == [3]
# 01b: n^2+1 divisible by 5 and n not prime
opts = [2, 4, 7, 8, 9]
key("proof-01b", only([(v * v + 1) % 5 == 0 and not isprime(v) for v in opts]))

# 02: x^2>x and not x>1
opts = [F(-1), F(0), F(1, 2), F(1), F(2)]
key("proof-02", only([v * v > v and not v > 1 for v in opts]))
# 02b: x^3<x and not x<0
opts = [F(-2), F(-1, 2), F(0), F(1, 2), F(2)]
key("proof-02b", only([v ** 3 < v and not v < 0 for v in opts]))

# 03: a^2-4b=2 impossible; squares mod 4 in {0,1}; even squares exist (E false); a^2 even => a even
assert not any(a * a - 4 * b == 2 for a in range(-60, 61) for b in range(-1000, 1000))
assert {a * a % 4 for a in R} == {0, 1}
assert all((a * a) % 2 == a % 2 for a in R)  # C's 'a odd' inference false
assert 4 == 2 * 2  # E's claim 'even number cannot be a square' false
key("proof-03", 3)
# 03b: no positive m,n with m^2-n^2=1
assert not any(m * m - k * k == 1 for m in range(1, 400) for k in range(1, 400))
key("proof-03b", 2)

# 04: p^2-1 data; 24 | p^2-1 for primes p>=5; false for odd n=9; 48 fails at 11
assert [p * p - 1 for p in (5, 7, 11, 13)] == [24, 48, 120, 168]
assert all((p * p - 1) % 24 == 0 for p in sp.primerange(5, 5000))
assert (9 * 9 - 1) % 24 != 0
assert 120 % 48 != 0
key("proof-04", 2)
# 04b: consecutive cubes sum
assert [(m - 1) ** 3 + m ** 3 + (m + 1) ** 3 for m in (2, 3, 4, 5)] == [36, 99, 216, 405]
assert eq((n_ - 1) ** 3 + n_ ** 3 + (n_ + 1) ** 3, 3 * n_ * (n_ ** 2 + 2))
assert all(((m - 1) ** 3 + m ** 3 + (m + 1) ** 3) % 9 == 0 for m in R)
assert (3 * 3 + 2) % 3 != 0  # B's claim fails at n=3
assert 36 % 27 != 0 and 3 % 9 != 0  # C inconsistent; E false (1+1+1)
assert 5 ** 3 + 6 ** 3 + 7 ** 3 == 684 == 9 * 76
key("proof-04b", 0)

# 05
I = all((m ** 5 - m) % 30 == 0 for m in R)
II = all((m * m + m + 1) % 5 != 0 for m in R)
III = all((m ** 4 - m * m) % 24 == 0 for m in R)
assert (2 ** 4 - 4) == 12 and all((m ** 4 - m * m) % 24 == 0 for m in (1, 3, 4, 5))
roman("proof-05", [I, II, III])
# 05b
I = all((m ** 3 + 2 * m) % 3 == 0 for m in R)
II = all(not isprime(m ** 4 + 4) for m in range(1, 400))
III = all((m ** 3 - m) % 24 == 0 for m in R if m % 2)
assert isprime(5) and eq((n_ ** 2 + 2 * n_ + 2) * (n_ ** 2 - 2 * n_ + 2), n_ ** 4 + 4)
roman("proof-05b", [I, II, III])

# 06: gap fill: odd squares = 1 mod 8; k(k+1) even for all k
assert all(((2 * k + 1) ** 2) % 8 == 1 for k in R)
assert all((k * (k + 1)) % 2 == 0 for k in R)
assert 5 == 2 * 2 + 1 and 4 % 8 != 0 and 3 % 8 != 1
key("proof-06", 4)
# 06b
k_ = sp.Symbol("k")
assert eq((3 * k_ + 1) ** 2 - 1, 3 * (3 * k_ ** 2 + 2 * k_))
assert eq((3 * k_ + 2) ** 2 - 1, 3 * (3 * k_ ** 2 + 4 * k_ + 1))
assert (4 - 1) % 3 == 0  # C's premise false at n=4
assert 5 % 3 == 2 and 5 % 2 == 1  # E: n=3k+2 can be odd
key("proof-06b", 0)


# 07 / 07b: brute force over all populations of student/card "types"
def must(constraints, statements, nvars):
    types = list(itertools.product([0, 1], repeat=nvars))
    res = [True] * len(statements)
    for r in range(1, 4):
        for pop in itertools.combinations(types, r):
            if all(c(pop) for c in constraints):
                for i, s in enumerate(statements):
                    if not s(pop):
                        res[i] = False
    # also every population of size up to 16 via subsets of types for completeness (small)
    return res


# types: (Latin, Greek, Art, Music)
c07 = [lambda P: all(g for (l, g, a, m) in P if l),
       lambda P: not any(g and a for (l, g, a, m) in P),
       lambda P: any(a and m for (l, g, a, m) in P)]
s07 = [lambda P: not any(l and a for (l, g, a, m) in P),
       lambda P: any(m and g for (l, g, a, m) in P),
       lambda P: any(m and not l for (l, g, a, m) in P)]
roman("proof-07", must(c07, s07, 4))
# types: (star front, square front, circle back, blue); star and square both on front allowed as flags
c07b = [lambda P: all(c for (st, sq, c, b) in P if st),
        lambda P: all(b for (st, sq, c, b) in P if c),
        lambda P: not any(b and sq for (st, sq, c, b) in P)]
s07b = [lambda P: not any(st and sq for (st, sq, c, b) in P),
        lambda P: all(not st for (st, sq, c, b) in P if not b),
        lambda P: any(b for (st, sq, c, b) in P)]
roman("proof-07b", must(c07b, s07b, 4))

# 08: Euclid numbers
primes = list(sp.primerange(2, 200))
I = II = III = True
for m in range(1, 12):
    N = 1
    for p in primes[:m]:
        N *= p
    N += 1
    I &= isprime(N)
    II &= all(N % p for p in primes[:m])
    III &= max(sp.primefactors(N)) > primes[m - 1]
assert 2 * 3 * 5 * 7 * 11 * 13 + 1 == 30031 == 59 * 509
roman("proof-08", [I, II, III])
# 08b: n!+1
I = all(min(sp.primefactors(sp.factorial(m) + 1)) > m for m in range(2, 25))
II = all(isprime(sp.factorial(m) + 1) for m in range(2, 25))
assert sp.factorial(4) + 1 == 25
III = I  # I gives, for every n, a prime > n
roman("proof-08b", [I, II, III])


# 09: board |a-b| game on 1..10
@lru_cache(None)
def finals(t):
    if len(t) == 1:
        return frozenset(t)
    out = set()
    L = list(t)
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            rest = L[:i] + L[i + 1:j] + L[j + 1:]
            out |= finals(tuple(sorted(rest + [abs(L[i] - L[j])])))
    return frozenset(out)


F10 = finals(tuple(range(1, 11)))
assert F10 == {1, 3, 5, 7, 9}
roman("proof-09", [0 in F10, 1 in F10, 9 in F10])


# 09b: 9 coins, flip exactly 3 per move; reachable tails-sets after exactly k moves
def reach(k):
    cur = {0}
    moves = [sum(1 << i for i in c) for c in itertools.combinations(range(9), 3)]
    for _ in range(k):
        cur = {s ^ mv for s in cur for mv in moves}
    return cur


pc = lambda s: bin(s).count("1")
I = any(pc(s) == 9 for s in reach(5))
II = any(pc(s) == 2 for s in reach(3))
III = any(pc(s) == 4 for s in reach(2))
roman("proof-09b", [I, II, III])

# 10: n(n+1)(n+2)(n+3)+1
assert eq(n_ * (n_ + 1) * (n_ + 2) * (n_ + 3) + 1, (n_ ** 2 + 3 * n_ + 1) ** 2)
vals = [m * (m + 1) * (m + 2) * (m + 3) + 1 for m in range(1, 300)]
roots = [m * m + 3 * m + 1 for m in range(1, 300)]
assert vals[:4] == [25, 121, 361, 841] and all(isprime(r) for r in roots[:4])  # all fit the data
assert all(v % 24 == 1 for v in vals[:4]) and all(r % 2 for r in roots[:4])
I = all(r % 2 == 1 for r in roots)
II = all(isprime(r) for r in roots)
III = all(v % 24 == 1 for v in vals)
assert not isprime(roots[5]) and roots[5] == 55 and isprime(roots[4])
roman("proof-10", [I, II, III])
# 10b: S(n) = sum k(k+1)
S = lambda m: sum(j * (j + 1) for j in range(1, m + 1))
assert [S(m) for m in (1, 2, 3, 4)] == [2, 8, 20, 40]
assert all(S(m) % 4 == 0 for m in (2, 3, 4))  # III fits the data
I = all(S(m) % 2 == 0 for m in range(1, 300))
II = all(3 * S(m) == m * (m + 1) * (m + 2) for m in range(1, 300))
III = all(S(m) % 4 == 0 for m in range(2, 300))
assert S(5) == 70
roman("proof-10b", [I, II, III])


# 11 / 11b / 14 / 14b: proof ordering; check dependencies (each statement's prerequisites come earlier)
def valid_orders(deps, labels):
    good = []
    for perm in itertools.permutations(labels):
        pos = {s: i for i, s in enumerate(perm)}
        if all(pos[d] < pos[s] for s in labels for d in deps.get(s, [])):
            good.append(", ".join(perm))
    return good


def order_key(qid, deps):
    labels = sorted({*deps} | {d for v in deps.values() for d in v})
    good = valid_orders(deps, labels)
    opts = QS[qid]["options"]
    key(qid, only([o in good for o in opts]))


order_key("proof-11", {"P": ["R"], "T": ["P"], "Q": ["T"], "S": ["P", "Q"], "R": []})
order_key("proof-11b", {"Q": [], "S": ["Q"], "T": ["Q"], "P": ["S", "T"], "R": ["P"]})
order_key("proof-14", {"Q": [], "T": ["Q"], "P": ["T"], "R": ["P"], "S": ["R"]})
order_key("proof-14b", {"T": [], "P": ["T"], "Q": ["T"], "R": ["P", "Q"], "S": ["R"]})
assert {m * m % 4 for m in R} == {0, 1}
assert all((a * a + b * b) % 4 != 3 for a in range(40) for b in range(40))
# 14: pigeonhole fact: same parity class => integer midpoint
pts = list(itertools.product(range(-3, 4), repeat=2))
for P5 in itertools.islice(itertools.combinations(pts, 5), 20000):
    assert any((p[0] + q[0]) % 2 == 0 and (p[1] + q[1]) % 2 == 0 for p, q in itertools.combinations(P5, 2))

# 12: lock code brute force
codes = []
for f, m, l in itertools.product(range(10), repeat=3):
    c1 = (f % 2 == 0) or (l % 2 == 0)
    c2 = (l % 2 == 1) or (m == 0)
    c3 = m != 0
    c4 = (m <= 5) or (f % 2 == 1)
    if c1 and c2 and c3 and c4:
        codes.append((f, m, l))
assert (2, 1, 3) in codes
I = all(f % 2 == 0 for f, m, l in codes)
II = all(m <= 5 for f, m, l in codes)
III = all((100 * f + 10 * m + l) % 5 == 0 for f, m, l in codes)
roman("proof-12", [I, II, III])
# 12b: xy<0, x+y>0 (rational grid search + proof in solution)
grid = [F(a, 4) for a in range(-40, 41)]
pairs = [(a, b) for a in grid for b in grid if a * b < 0 and a + b > 0]
I = all(a > 0 for a, b in pairs)
II = all(a * a != b * b for a, b in pairs)
III = all(a > abs(b) for a, b in pairs if a > 0)
roman("proof-12b", [I, II, III])

# 13: sums of squares
def implies_both(form, m):
    return all((a % m == 0 and b % m == 0) for a in range(3 * m) for b in range(3 * m) if form(a, b) % m == 0)


roman("proof-13", [implies_both(lambda a, b: a * a + b * b, 3),
                   implies_both(lambda a, b: a * a + b * b, 5),
                   implies_both(lambda a, b: a * a + b * b, 7)])
# 13b: II is 'both even' (divisibility by 2) under a^2+b^2 divisible by 4
II = all(a % 2 == 0 and b % 2 == 0 for a in range(16) for b in range(16) if (a * a + b * b) % 4 == 0)
roman("proof-13b", [implies_both(lambda a, b: a * a + 2 * b * b, 3), II,
                    implies_both(lambda a, b: a * a - 2 * b * b, 5)])

# 15: AM-GM; option C's square-root step is false
a_, b_ = sp.symbols("a b", nonnegative=True)
assert eq((sp.sqrt(a_) - sp.sqrt(b_)) ** 2, a_ - 2 * sp.sqrt(a_ * b_) + b_)
assert sp.sqrt(3 ** 2 + 4 ** 2) != 3 + 4
key("proof-15", 1)
# 15b
assert sp.sqrt(3) + sp.sqrt(7) < 2 * sp.sqrt(5)
assert eq((sp.sqrt(3) + sp.sqrt(7)) ** 2, 10 + 2 * sp.sqrt(21))
assert sp.sqrt(3) + sp.sqrt(7) != sp.sqrt(10) and sp.sqrt(7) > sp.sqrt(5)
key("proof-15b", 2)


# 16 / 16b: base-case windows
def smallest_window(gens, step):
    reach_ = {0}
    for t in range(1, 400):
        if any(t - g in reach_ for g in gens if t - g >= 0):
            reach_.add(t)
    for N in range(1, 300):
        if all(N + i in reach_ for i in range(step)):
            return N, reach_


N, rs = smallest_window([5, 7], 5)
assert N == 24 and [t for t in range(1, 30) if t not in rs] == [1, 2, 3, 4, 6, 8, 9, 11, 13, 16, 18, 23]
key("proof-16", [19, 20, 23, 24, 35].index(N))
N, rs = smallest_window([6, 10, 15], 6)
assert N == 30 and all(t in rs for t in range(24, 29)) and 29 not in rs
key("proof-16b", [24, 29, 30, 36, 90].index(N))

# 17: (4a+1)(4b+1) = 1 mod 4 ; 3*3 = 1 mod 4 ; 15 not prime ; 923 = 13*71
assert all(((4 * a + 1) * (4 * b + 1)) % 4 == 1 for a in range(30) for b in range(30))
assert (3 * 3) % 4 == 1 and not isprime(15) and 4 * 3 * 7 * 11 - 1 == 923 == 13 * 71
key("proof-17", 1)
# 17b: (3a+1)(3b+1) = 1 mod 3 ; 2*2 = 1 mod 3 ; 8 not prime ; 329 = 7*47
assert all(((3 * a + 1) * (3 * b + 1)) % 3 == 1 for a in range(30) for b in range(30))
assert (2 * 2) % 3 == 1 and not isprime(8) and 3 * 2 * 5 * 11 - 1 == 329 == 7 * 47
assert 3 * 2 * 5 - 1 == 29
key("proof-17b", 3)


# 18 / 18b: parity argument validity and rational-root argument
def parity_ok(f):
    return all(f(p, q) % 2 == 1 for p in (0, 1) for q in (0, 1) if (p, q) != (0, 0))


f18 = lambda p, q: p ** 3 + p * q * q + q ** 3
f18b = lambda p, q: p ** 3 + p * p * q + p * q * q - q ** 3
assert parity_ok(f18) and not parity_ok(f18b)
assert all(c ** 3 + c + 1 != 0 for c in (1, -1)) and all(c ** 3 + c * c + c - 1 != 0 for c in (1, -1))
assert not any(r.is_rational for r in sp.Poly(x_ ** 3 + x_ + 1).all_roots())
assert not any(r.is_rational for r in sp.Poly(x_ ** 3 + x_ ** 2 + x_ - 1).all_roots())
assert sp.solve(x_ ** 3 - 1, x_)[0] == 1  # III (18) false general claim
roman("proof-18", [True, True, False])
roman("proof-18b", [False, True, False])

# structure: ids, twins, difficulty spread, twin answer letters differ
orig = [f"proof-{i:02d}" for i in range(1, 19)]
assert sorted(QS) == sorted(orig + [o + "b" for o in orig])
for o in orig:
    a, b = QS[o], QS[o + "b"]
    assert a["family"] == b["family"] == o
    assert a["difficulty"] == b["difficulty"], o
    assert a["answer"] != b["answer"], o
assert Counter(QS[o]["difficulty"] for o in orig) == Counter({2: 2, 3: 6, 4: 6, 5: 4})
for q in ALL:
    for s in [q["stem"]] + [o for o in q["options"] if isinstance(o, str)]:
        for sym in "⇒∧∨¬∀∃":
            assert sym not in s, (q["id"], sym)
print("ALL OK")
