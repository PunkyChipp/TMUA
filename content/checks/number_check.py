"""Verification for content/questions/number.json.

Each check computes the answer independently (brute force where possible), asserts that
the keyed option matches, and asserts that every other option is wrong.
"""
import json
import os
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm

from sympy import isprime

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "number.json"), encoding="utf-8"))}
assert len(QS) == 18 and all(f"number-{i:02d}" in QS for i in range(1, 19))

ROMAN_IDX = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3,
             (1, 1, 0): 4, (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}


def check_values(qid, values, correct):
    """values[i] is the mathematical value of option i."""
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    assert len(set(values)) == len(values), f"{qid}: duplicate option values"
    assert values[q["answer"]] == correct, f"{qid}: key {q['answer']} value {values[q['answer']]} != {correct}"
    assert sum(v == correct for v in values) == 1, qid
    assert len(set(q["options"])) == len(q["options"]), qid
    print(qid, "ok")


def check_roman(qid, truths):
    q = QS[qid]
    assert q["answer"] == ROMAN_IDX[tuple(int(bool(t)) for t in truths)], f"{qid}: truths {truths}"
    print(qid, "ok")


# 01: +25% then -20%
check_values("number-01", [F(-5), F(-4), F(0), F(4), F(5)], (F(125, 100) * F(80, 100) - 1) * 100)

# 02: last digit of 7^2026
check_values("number-02", [1, 3, 7, 9], pow(7, 2026, 10))

# 03: removed number (brute-ish: totals)
check_values("number-03", [1, 11, 12, 13, 21], 10 * 12 - 9 * 11)

# 04: reverse percentage; search over pence
orig = [p for p in range(1, 100000) if p * 85 == 6800 * 100]  # price in pence, 0.85p = 6800
assert orig == [8000]
check_values("number-04", [F(5780, 100), F(7820, 100), F(80), F(85)], F(orig[0], 100))

# 05: counterexample to n^2+n+41 prime
vals = [n * n + n + 41 for n in (1, 10, 20, 30, 40)]
comp = [not isprime(v) for v in vals]
assert comp == [False, False, False, False, True]
assert QS["number-05"]["answer"] == 4
print("number-05 ok")

# 06: I mean increases (proof + random test), II median, III range counterexamples
import random
from statistics import median
random.seed(1)
for _ in range(20000):
    L = [random.randint(-20, 20) for _ in range(random.randint(2, 6))]
    mu = F(sum(L), len(L))
    x = mu + F(random.randint(1, 40), random.randint(1, 5))
    L2 = L + [x]
    assert F(sum(L2)) / len(L2) > mu
L = [1, 5, 5, 5]; x = 6
assert x > F(sum(L), 4) and median(L + [x]) == median(L)
L = [1, 2, 9]; x = 5
assert x > F(sum(L), 3) and max(L + [x]) - min(L + [x]) == max(L) - min(L)
check_roman("number-06", (True, False, False))

# 07: HCF 6, LCM 360 unordered pairs (brute force)
pairs = [(a, b) for a in range(1, 361) for b in range(a, 361) if gcd(a, b) == 6 and lcm(a, b) == 360]
assert sorted(pairs) == sorted([(6, 360), (24, 90), (18, 120), (30, 72)])
check_values("number-07", [3, 4, 6, 8, 12], len(pairs))

# 08: divisors of 720 that are multiples of 6
check_values("number-08", [8, 12, 16, 20, 24, 30], sum(1 for d in range(1, 721) if 720 % d == 0 and d % 6 == 0))
assert sum(1 for d in range(1, 721) if 720 % d == 0) == 30
assert sum(1 for d in range(1, 721) if 720 % d == 0 and d % 2 == 0) == 24

# 09: 1/x + 1/y = 1/6 ordered positive pairs (x,y <= 42 since x-6 divides 36)
sols = [(x, y) for x in range(1, 500) for y in range(1, 500) if F(1, x) + F(1, y) == F(1, 6)]
assert all(x <= 42 and y <= 42 for x, y in sols)
check_values("number-09", [4, 5, 8, 9, 10, 18], len(sols))

# 10: divisible by 3 or 5 but not 15
c = sum(1 for n in range(1, 1001) if (n % 3 == 0 or n % 5 == 0) and n % 15 != 0)
check_values("number-10", [335, 401, 467, 533], c)

# 11
t1 = all((n * n - n) % 2 == 0 for n in range(1, 5000))
t2 = all((n ** 3 - n) % 6 == 0 for n in range(1, 5000))
t3 = all((n ** 4 - n ** 2) % 24 == 0 for n in range(1, 5000))
assert (n := 2) and (n ** 4 - n ** 2) % 24 != 0
check_roman("number-11", (t1, t2, t3))

# 12: five distinct positive integers, mean 10, median 8, max largest
best = max(max(s) for s in combinations(range(1, 51), 5) if sum(s) == 50 and sorted(s)[2] == 8)
check_values("number-12", [26, 29, 30, 31, 32], best)

# 13: last digit of sum k^k
check_values("number-13", [1, 3, 5, 7, 9], sum(k ** k for k in range(1, 11)) % 10)

# 14: integer solutions of x^2 - y^2 = 60 (|x|,|y| <= 31 since (|x|-|y|)(|x|+|y|)=60)
sols = [(x, y) for x in range(-100, 101) for y in range(-100, 101) if x * x - y * y == 60]
check_values("number-14", [2, 4, 6, 8, 12, 16], len(sols))

# 15: ordering
import math
nums = {"2": 2 ** 0.5, "3": 3 ** (1 / 3), "5": 5 ** 0.2, "6": 6 ** (1 / 6)}
order = "".join(sorted(nums, key=nums.get))
# exact integer confirmation of every pairwise comparison
assert 2 ** 3 < 3 ** 2 and 5 ** 2 < 2 ** 5 and 6 ** 5 < 5 ** 6
opt_orders = []
for o in QS["number-15"]["options"]:
    bases = [tok.split("^")[0].strip("$ ") for tok in o.split("<")]
    opt_orders.append("".join(bases))
check_values("number-15", opt_orders, order)

# 16: sufficiency for 12 | n
R = range(-3000, 3001)
s1 = all(n % 12 == 0 for n in R if (n * n) % 24 == 0)
s2 = all(n % 12 == 0 for n in R if n % 2 == 0 and n % 6 == 0)
s3 = all(n % 12 == 0 for n in R if (n ** 3) % 18 == 0)
check_roman("number-16", (s1, s2, s3))

# 17: values k in 1..30 not achieved as trailing zeros of n!
def tz(m):
    s = str(m)
    return len(s) - len(s.rstrip("0"))
fact = 1
achieved = set()
for n in range(1, 200):
    fact *= n
    achieved.add(tz(fact))
missing = [k for k in range(1, 31) if k not in achieved]
assert missing == [5, 11, 17, 23, 29, 30]
check_values("number-17", [1, 4, 5, 6, 7], len(missing))

# 18: repunit of 2026 ones mod 7
check_values("number-18", [0, 1, 2, 3, 4, 5, 6], int("1" * 2026) % 7)

# difficulty spread
from collections import Counter
assert Counter(q["difficulty"] for q in QS.values()) == Counter({1: 2, 2: 4, 3: 6, 4: 4, 5: 2})
print("ALL OK")
