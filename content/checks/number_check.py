"""Verification for content/questions/number.json (originals number-NN and twins number-NNb).

Each check computes the answer independently (brute force / exact arithmetic where possible),
asserts that the keyed option equals it, and that no other option does.
Run: python3 content/checks/number_check.py
"""
import json
import math
import os
from collections import Counter
from fractions import Fraction as F
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "number.json"), encoding="utf-8"))}
ROMAN = ["none of them", "I only", "II only", "III only", "I and II only",
         "I and III only", "II and III only", "I, II and III"]
ROMAN_IDX = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4,
             (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}


def check_values(qid, values, correct, ascending=True):
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    hits = [i for i, v in enumerate(values) if v == correct]
    assert hits == [q["answer"]], f"{qid}: hits {hits}, key {q['answer']}, correct {correct}"
    if ascending:
        assert list(values) == sorted(values), f"{qid}: options not ascending"


def check_roman(qid, truths):
    q = QS[qid]
    assert q["options"] == ROMAN, qid
    assert q["answer"] == ROMAN_IDX[tuple(int(bool(t)) for t in truths)], f"{qid}: truths {truths}"


def opt_num(qid):
    """Parse simple numeric options like '$12$', '$\\frac{3}{22}$', '$\\frac16$', '$54\\,000$'."""
    import re
    out = []
    for o in QS[qid]["options"]:
        s = o.strip("$").replace("\\,", "")
        m = re.fullmatch(r"(-?)\\frac(?:\{(\d+)\}|(\d))(?:\{(\d+)\}|(\d+))", s)
        if m:
            v = F(int(m.group(2) or m.group(3)), int(m.group(4) or m.group(5)))
            out.append(-v if m.group(1) else v)
        else:
            out.append(F(s))
    return out


# number-01: 0.8^n < 1/3
n = 0
while F(4, 5) ** n >= F(1, 3):
    n += 1
check_values("number-01", opt_num("number-01"), n)
assert F(4, 5) ** 4 > F(1, 3) > F(4, 5) ** 5

# number-01b
n, c = 0, F(400)
while c <= 3000:
    c *= F(3, 2)
    n += 1
check_values("number-01b", opt_num("number-01b"), n)

# number-02: 0.1363636...
x = F(1, 10) + F(36, 990)
assert x == F(3, 22)
vals = [F(41, 330), F(5, 37), F(136, 999), F(3, 22), F(68, 495)]
assert opt_num("number-02") == vals
check_values("number-02", [float(v) for v in vals], float(x))
# decimal expansion check
digits = "".join(str((x * 10 ** k).__floor__() % 10) for k in range(1, 12))
assert digits == "13636363636"

# number-02b
v = F(18, 99) * (F(8, 10) + F(3, 90))
assert F(8, 10) + F(3, 90) == F(5, 6)
vals = [F(3, 20), F(5, 33), F(166, 1089), F(1, 6), F(83, 495)]
assert opt_num("number-02b") == vals
check_values("number-02b", [float(t) for t in vals], float(v))

# number-03: upper bound speed = 25.5 / (15.75 - 12.35)
v = F(255, 10) / (F(1575, 100) - F(1235, 100))
check_values("number-03", opt_num("number-03"), v)
assert opt_num("number-03") == [F(255, 10) / F(36, 10), F(25) / F(35, 10), F(255, 10) / F(35, 10), v, F(255, 10) / F(33, 10)]

# number-03b
v = 495 - 30 * F(25, 2)
check_values("number-03b", opt_num("number-03b"), v)

# number-04: 1.2^2 * 0.9^3
mult = F(12, 10) ** 2 * F(9, 10) ** 3
pct = float((mult - 1) * 100)
claims = [-13, 1, 5, 10, 30]   # option meanings (about)
close = [i for i, c in enumerate(claims) if abs(pct - c) < 0.6]
assert close == [QS["number-04"]["answer"]], (pct, close)
assert "5\\%" in QS["number-04"]["options"][2]

# number-04b
mult = F(15, 10) / F(125, 100) ** 2
assert mult == F(24, 25)
pct = (mult - 1) * 100
claims = [-4, 0, 4, 20, 134]
close = [i for i, c in enumerate(claims) if abs(float(pct) - c) < 0.5 and (c != 4 or pct > 0)]
assert close == [QS["number-04b"]["answer"]], close
assert "decrease of $4" in QS["number-04b"]["options"][0]


# number-05
def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))


comp = [i for i, n in enumerate((1, 10, 20, 30, 40)) if not is_prime(n * n + n + 41)]
assert comp == [QS["number-05"]["answer"]]
comp = [i for i, p in enumerate((2, 3, 5, 7, 11)) if not is_prime(2 * p + 1)]
assert comp == [QS["number-05b"]["answer"]] and all(is_prime(p) for p in (2, 3, 5, 7, 11))

# number-06: sqrt(4.9e7) / 2e-2
side = math.isqrt(49 * 10 ** 6)
assert side * side == 49 * 10 ** 6
v = F(side) / F(2, 100)
check_values("number-06", [F(35), F(140), F(110000), F(350000), F(1100000)], v)
assert QS["number-06"]["options"][3] == "$3.5\\times10^{5}$"

# number-06b: closest
exact = 0.00031 * 59800 / 0.0198
opts = [9, 90, 900, 9000, 90000]
assert opt_num("number-06b") == [F(t) for t in opts]
best = min(range(5), key=lambda i: abs(math.log(opts[i] / exact)))
assert best == QS["number-06b"]["answer"]
assert abs(exact - opts[best]) < abs(exact - opts[best + 1]) and abs(exact - opts[best]) < abs(exact - opts[best - 1])

# number-07
pairs = {(a, 360 * 6 // a) for a in range(6, 361, 6) if 360 * 6 % a == 0
         and math.gcd(a, 2160 // a) == 6 and a <= 2160 // a}
check_values("number-07", opt_num("number-07"), len(pairs))

# number-07b
cnt = sum(1 for m in range(1, 1000) if math.lcm(12, 18, m) == 180)
check_values("number-07b", opt_num("number-07b"), cnt)

# number-08
check_values("number-08", opt_num("number-08"), sum(1 for d in range(1, 721) if 720 % d == 0 and d % 6 == 0))
# number-08b
check_values("number-08b", opt_num("number-08b"), sum(1 for d in range(1, 1801) if 1800 % d == 0 and d % 2))

# number-09
sols = [(a, b) for a in range(1, 100) for b in range(1, 100) if F(1, a) + F(1, b) == F(1, 6)]
check_values("number-09", opt_num("number-09"), len(sols))
# number-09b
sols = [(a, b) for a in range(1, 200) for b in range(1, 200) if F(3, a) + F(4, b) == 1]
check_values("number-09b", opt_num("number-09b"), len(sols))

# number-10: litres per minute
rate_cm3_s = 50 * 180
check_values("number-10", opt_num("number-10"), F(rate_cm3_s * 60, 1000))

# number-10b
mass_kg = F(20 * 10 * 5 * 8, 1000)
area_m2 = F(10 * 5, 10 ** 4)
check_values("number-10b", opt_num("number-10b"), mass_kg * 10 / area_m2)

# number-11
rng = [n for n in range(-60, 61)]
t1 = all((n * n - n) % 2 == 0 for n in rng)
t2 = all((n ** 3 - n) % 6 == 0 for n in rng)
t3 = all((n ** 4 - n * n) % 24 == 0 for n in rng)
check_roman("number-11", (t1, t2, t3))
odd = [n for n in range(-61, 62) if n % 2]
check_roman("number-11b", (all((n * n - 1) % 8 == 0 for n in odd), all((n ** 4 - 1) % 32 == 0 for n in odd),
                           all((n * n + 3) % 4 == 0 for n in odd)))

# number-12
cnt = sum(1 for m in range(1000, 10000) if len(set(str(m))) == 4 and m % 2 == 0)
check_values("number-12", opt_num("number-12"), cnt)
# number-12b
cnt = sum(1 for m in range(100, 1000) if math.prod(int(d) for d in str(m)) == 24)
check_values("number-12b", opt_num("number-12b"), cnt)

# number-13: exact iteration
u, n = F(2000), 0
while u >= 1000:
    u = u * F(6, 5) - 500
    n += 1
check_values("number-13", opt_num("number-13"), n)
assert F(6, 5) ** 6 < 3 < F(6, 5) ** 7

# number-13b
b, n = F(8000), 0
while b > 0:
    b = b * F(5, 4)
    pay = min(b, F(2500))
    b -= pay
    n += 1
check_values("number-13b", opt_num("number-13b"), n)

# number-14
sols = [(a, b) for a in range(-100, 101) for b in range(-100, 101) if a * a - b * b == 60]
check_values("number-14", opt_num("number-14"), len(sols))
# number-14b
reps = {a * a - b * b for a in range(0, 60) for b in range(0, 60)}
check_values("number-14b", opt_num("number-14b"), sum(1 for m in range(1, 51) if m in reps))

# number-15: orderings
vals = {"2^{1/2}": 2 ** 0.5, "3^{1/3}": 3 ** (1 / 3), "5^{1/5}": 5 ** 0.2, "6^{1/6}": 6 ** (1 / 6)}
order = "$" + "<".join(sorted(vals, key=vals.get)) + "$"
assert [o for o in QS["number-15"]["options"]].index(order) == QS["number-15"]["answer"]
assert len(QS["number-15"]["options"]) == 5
vals = {"2^{48}": 2 ** 48, "3^{32}": 3 ** 32, "5^{20}": 5 ** 20, "7^{16}": 7 ** 16}
order = "$" + "<".join(sorted(vals, key=vals.get)) + "$"
assert QS["number-15b"]["options"].index(order) == QS["number-15b"]["answer"]

# number-16
rng = range(1, 5000)
s1 = all(n % 12 == 0 for n in rng if (n * n) % 24 == 0)
s2 = all(n % 12 == 0 for n in rng if n % 2 == 0 and n % 6 == 0)
s3 = all(n % 12 == 0 for n in rng if n ** 3 % 18 == 0)
check_roman("number-16", (s1, s2, s3))
s1 = all(n * n % 72 == 0 for n in rng if n % 12 == 0)
s2 = all(n * n % 72 == 0 for n in rng if n * n % 48 == 0)
s3 = all(n * n % 72 == 0 for n in rng if n ** 3 % 36 == 0)
check_roman("number-16b", (s1, s2, s3))


# number-17
def Z(m):
    z, p = 0, 5
    while p <= m:
        z += m // p
        p *= 5
    return z


attained = {Z(m) for m in range(1, 200)}
missing = [kk for kk in range(1, 31) if kk not in attained]
check_values("number-17", opt_num("number-17"), len(missing))
# number-17b
m = 1
while math.factorial(m) % 12 ** 10:
    m += 1
check_values("number-17b", opt_num("number-17b"), m)

# number-18
check_values("number-18", opt_num("number-18"), int("1" * 2026) % 7)
check_values("number-18b", opt_num("number-18b"), (2 ** 2026 + 3 ** 2026) % 7)

# ---------------------------------------------------------------- structure
ids = [f"number-{i:02d}" for i in range(1, 19)]
assert sorted(QS) == sorted(ids + [i + "b" for i in ids])
assert Counter(QS[i]["difficulty"] for i in ids) == Counter({2: 2, 3: 6, 4: 6, 5: 4})
for i in ids:
    a_, b_ = QS[i], QS[i + "b"]
    assert a_["family"] == b_["family"] == i
    assert a_["difficulty"] == b_["difficulty"], i
    assert a_["answer"] != b_["answer"], i
for q in QS.values():
    assert len(set(q["options"])) == len(q["options"])
    assert str(q["answer"]) not in q["distractors"]
    assert len(q["distractors"]) >= 3, q["id"]
    assert len(q["options"]) == 5 or q["options"] == ROMAN, q["id"]
    assert q["difficulty"] >= 2
print("ALL OK")
