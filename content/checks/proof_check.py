"""Verification for content/questions/proof.json. Run: python3 content/checks/proof_check.py"""
import itertools
import json
import os
from fractions import Fraction as F

import sympy as sp
from sympy import isprime

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "proof.json")))}
ROMAN8 = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]


def key(qid, idx):
    q = QS[qid]
    assert q["answer"] == idx, (qid, q["answer"], idx)
    assert len(set(q["options"])) == len(q["options"]), qid
    assert 4 <= len(q["options"]) <= 8, qid


def roman(qid, truths):
    key(qid, ROMAN8.index({i + 1 for i, t in enumerate(truths) if t}))


# 01: counterexample to "p prime => p^2+2 not prime"
opts = [2, 3, 5, 7, 11]
ce = [p for p in opts if isprime(p) and isprime(p * p + 2)]
assert ce == [3]
assert [p for p in range(2, 2000) if isprime(p) and isprime(p * p + 2)] == [3]
key("proof-01", opts.index(3))

# 02: x^2 >= x
opts = [F(-2), F(0), F(1, 2), F(1), F(2)]
ce = [x for x in opts if not x * x >= x]
assert ce == [F(1, 2)]
key("proof-02", 2)

# 03: negation of P=>Q is P and not Q  (truth-table check)
for P, Qv in itertools.product([0, 1], repeat=2):
    impl = (not P) or Qv
    assert (not impl) == (P and not Qv)
    assert (((not P) or Qv)) == impl  # option E equivalent to the statement itself
key("proof-03", 2)

# 04: n^2+n+41
opts = [1, 10, 20, 39, 40]
ce = [n for n in opts if not isprime(n * n + n + 41)]
assert ce == [40] and 40 * 40 + 40 + 41 == 41 ** 2
key("proof-04", 4)

# 05
R = range(-200, 201)
I = all((n * n + n) % 2 == 0 for n in R)
II = all((n ** 3 - n) % 6 == 0 for n in R)
III = all((n ** 4 - n) % 4 == 0 for n in R)
assert sp.factor(sp.Symbol("n") ** 3 - sp.Symbol("n")) == sp.factor((sp.Symbol("n") - 1) * sp.Symbol("n") * (sp.Symbol("n") + 1))
roman("proof-05", [I, II, III])

# 06: odd squares = 1 mod 8; option C premise false (k can be even)
assert all(((2 * k + 1) ** 2) % 8 == 1 for k in range(-100, 100))
assert all((k * (k + 1)) % 2 == 0 for k in range(-100, 100))
assert 5 == 2 * 2 + 1  # n=5 gives k=2 even: option C's premise fails
assert 4 % 8 != 0 and 3 % 8 != 1  # A, E inferences false
key("proof-06", 1)

# 07: quantifiers
x, y = sp.symbols("x y", real=True)
# I: y = x^2+1 works for all x
assert sp.simplify((x ** 2 + 1) - x ** 2) == 1
# II false: for any y, x = sqrt(|y|)+1 gives x^2 > y
for yy in [F(-5), F(0), F(3), F(100), F(10 ** 6)]:
    xx = sp.sqrt(abs(yy)) + 1
    assert xx ** 2 > yy
# III: x = 0 gives 0*y = 0 = x for all y
assert sp.simplify(0 * y - 0) == 0
roman("proof-07", [True, False, True])

# 08
primes = list(sp.primerange(2, 100))
Iok, IIok, IIIok = True, True, True
for n in range(1, 12):
    ps = primes[:n]
    N = 1
    for p in ps:
        N *= p
    N += 1
    if not isprime(N):
        Iok = False
    if any(N % p == 0 for p in ps):
        IIok = False
    if max(sp.factorint(N)) <= ps[-1]:
        IIIok = False
assert 30031 == 59 * 509 and 2 * 3 * 5 * 7 * 11 * 13 + 1 == 30031
roman("proof-08", [Iok, IIok, IIIok])

# 09: converse counterexample
opts = [2, 3, 5, 7, 9, 11, 13]
ce = [n for n in opts if isprime(n) and not isprime(2 ** n - 1)]
assert ce == [11] and 2 ** 11 - 1 == 23 * 89
key("proof-09", opts.index(11))

# 10: counterexamples count
ce = [n for n in range(1, 21) if n % 2 == 1 and not isprime(n * n + 4)]
assert ce == [9, 11, 19]
opts = [0, 1, 2, 3, 4, 13]
key("proof-10", opts.index(len(ce)))

# 11: proof order via dependencies
deps = {"R": set(), "P": {"R"}, "T": {"P"}, "Q": {"T"}, "S": {"P", "Q"}}
valid = []
for q in QS["proof-11"]["options"]:
    order = [c.strip() for c in q.split(",")]
    seen, ok = set(), order[0] == "R"
    for s in order:
        ok = ok and deps[s] <= seen
        seen.add(s)
    ok = ok and order[-1] == "S"
    valid.append(ok)
assert valid.count(True) == 1
key("proof-11", valid.index(True))

# 12: a<b => 1/a > 1/b  counterexamples exactly a<0<b
vals = [F(k, 4) for k in range(-40, 41) if k != 0]
ces = [(a, b) for a in vals for b in vals if a < b and not (1 / a > 1 / b)]
assert ces and all(a < 0 < b for a, b in ces)
assert all((1 / a < 1 / b) for a in vals for b in vals if a < 0 < b)
key("proof-12", 2)

# 13: a^2+b^2 divisible by m => both divisible, m=3,5,7
def prop(m):
    return all((a % m == 0 and b % m == 0) for a in range(m) for b in range(m) if (a * a + b * b) % m == 0)
roman("proof-13", [prop(3), prop(5), prop(7)])

# 14: n^k - n divisible by k for all n (check all residues)
opts = [2, 3, 5, 7, 9, 13]
false_k = [k for k in opts if not all((pow(n, k, k) - n) % k == 0 for n in range(k))]
assert false_k == [9] and (2 ** 9 - 2) % 9 != 0
key("proof-14", opts.index(9))

# 15: B valid; C's square-root step invalid (sqrt(a^2+b^2) != a+b); sanity of claim
a, b = sp.symbols("a b", nonnegative=True)
assert sp.expand((sp.sqrt(a) - sp.sqrt(b)) ** 2 - (a + b - 2 * sp.sqrt(a * b))) == 0
assert sp.sqrt(3 ** 2 + 4 ** 2) != 3 + 4
key("proof-15", 1)

# 16: smallest N with N, N+1, N+2 representable as 3a+5b
rep = {3 * i + 5 * j for i in range(50) for j in range(50)}
N = next(n for n in range(0, 100) if n > 0 and {n, n + 1, n + 2} <= rep and all(m in rep for m in range(n, 100)))
assert N == 8
# confirm smaller candidates fail the "three consecutive base cases" test
assert all(not ({n, n + 1, n + 2} <= rep) for n in range(1, 8))
key("proof-16", [5, 6, 7, 8, 9, 15].index(8))

# 17: product of 1 mod 4 numbers is 1 mod 4; C and A false; D example
assert all(((4 * i + 1) * (4 * j + 1)) % 4 == 1 for i in range(30) for j in range(30))
assert (3 * 3) % 4 == 1 and not isprime(15)
assert 4 * 3 * 7 * 11 - 1 == 923 == 13 * 71
key("proof-17", 1)

# 18
X = sp.Symbol("X")
assert [r for r in sp.roots(X ** 3 + X + 1, filter="Q")] == []
Ivalid = all((p ** 3 + p * q * q + q ** 3) % 2 == 1 for p in range(2) for q in range(2) if not (p == 0 and q == 0))
p_, q_ = sp.symbols("p q")
assert sp.expand(p_ ** 3 + q_ ** 2 * (p_ + q_) - (p_ ** 3 + p_ * q_ ** 2 + q_ ** 3)) == 0
assert all(pp ** 3 + pp + 1 != 0 for pp in (1, -1))
# III's general claim is false: x^3-1 has one real root, rational
assert sp.real_roots(X ** 3 - 1) == [1]
IIIvalid = False
roman("proof-18", [Ivalid, True, IIIvalid])

from collections import Counter
assert Counter(q["difficulty"] for q in QS.values()) == Counter({1: 2, 2: 4, 3: 6, 4: 4, 5: 2})
assert sorted(QS) == [f"proof-{i:02d}" for i in range(1, 19)]
print("ALL OK")
