"""Verification for content/questions/geom.json. Run: python3 content/checks/geom_check.py"""
import json, math, os
from collections import Counter
import sympy as sp
from sympy import sqrt, pi, Rational as R, cbrt

HERE = os.path.dirname(os.path.abspath(__file__))
Q = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "geom.json")))}


def key(qid, idx):
    q = Q[qid]
    assert q["answer"] == idx, (qid, q["answer"], idx)
    assert len(set(q["options"])) == len(q["options"]), qid


def ascending(vals):
    f = [float(v) for v in vals]
    assert f == sorted(f) and len(set(f)) == len(f), f


def dist(p, q):
    return sp.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


# 01: interior angles of regular polygons
angles = [150, 155, 156, 160, 162, 165]
possible = [360 % (180 - a) == 0 for a in angles]
assert possible == [True, False, True, True, True, True]
key("geom-01", 1)

# 02
opts = [24, 36, 54, 81, 108]
k = sp.sqrt(R(9, 4))
assert 16 * k ** 3 == 54
key("geom-02", 2)

# 03: cube [0,2]^3, V = origin; centres of faces not containing V
centres = [(2, 1, 1), (1, 2, 1), (1, 1, 2)]
assert all(dist((0, 0, 0), c) == sqrt(6) for c in centres)
ascending([sqrt(5), sqrt(6), 2 * sqrt(2), 3, 2 * sqrt(3)])
key("geom-03", 1)

# 04: coordinates. Circle radius 1 centred at O; A, B placed so OAB = 25 deg; C on major arc
aob = math.radians(180 - 2 * 25)
A = (1.0, 0.0)
B = (math.cos(aob), math.sin(aob))
OA = (-A[0], -A[1]); AB = (B[0] - A[0], B[1] - A[1])
oab = math.degrees(math.acos((OA[0] * AB[0] + OA[1] * AB[1]) / (math.hypot(*OA) * math.hypot(*AB))))
assert abs(oab - 25) < 1e-9
for t in [3.0, 4.0, 5.5]:  # points on major arc (angles > 130 deg)
    C = (math.cos(t), math.sin(t))
    u = (A[0] - C[0], A[1] - C[1]); v = (B[0] - C[0], B[1] - C[1])
    acb = math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))
    assert abs(acb - 65) < 1e-9
key("geom-04", 2)

# 05
h = sp.sqrt(5 ** 2 - 3 ** 2)
Vc = R(1, 3) * pi * 9 * h
r = sp.symbols("r", positive=True)
rs = sp.solve(sp.Eq(R(4, 3) * pi * r ** 3, Vc), r)[0]
opts = [cbrt(3), cbrt(9), cbrt(R(45, 4)), cbrt(12), 3]
ascending(opts)
assert sp.simplify(rs - cbrt(9)) == 0
key("geom-05", 1)

# 06: I true, II false (square vs 60-120 rhombus have different angles), III true (angles 45,45,90)
assert {90} != {60, 120}
key("geom-06", 5)

# 07
A, B, C = sp.Matrix([0, 0]), sp.Matrix([3, 0]), sp.Matrix([1, 4])
D = A + R(2, 3) * (B - A)
E = A + R(1, 4) * (C - A)


def tri(P, Q_, S):
    return abs((Q_ - P)[0] * (S - P)[1] - (Q_ - P)[1] * (S - P)[0]) / 2


frac = 1 - tri(A, D, E) / tri(A, B, C)
opts = [R(2, 3), R(3, 4), R(7, 9), R(5, 6), R(11, 12)]
ascending(opts)
assert frac == R(5, 6)
key("geom-07", 3)

# 08: O origin, P (13,0), tangent points
xA = R(25, 13); yA = sp.sqrt(25 - xA ** 2)
assert sp.simplify(xA * 13 - 25) == 0 and yA == R(60, 13)   # OA.AP = 0 <=> x*13 = 25
assert sp.simplify((sp.Matrix([xA, yA])).dot(sp.Matrix([13 - xA, -yA]))) == 0
AB = 2 * yA
ascending([R(60, 13), R(120, 13), 10, 12, 24])
assert AB == R(120, 13)
key("geom-08", 1)

# 09
newd = 6 * cbrt(2)
assert sp.simplify((newd / 12) ** 3 / (R(6, 12)) ** 3 - 2) == 0
ascending([6 * cbrt(2), 6 * sqrt(2), 9, 6 * cbrt(4), 12])
key("geom-09", 0)

# 10
assert 360 % 15 == 0 and 360 % 35 != 0
rem = (7 - 2) * 180 - 6 * 130
assert 0 < rem < 180
key("geom-10", 5)

# 11: base corners (+-3, +-3, 0), apex (0,0,h) with edge 6
hh = sp.symbols("hh", positive=True)
hsol = sp.solve(sp.Eq(9 + 9 + hh ** 2, 36), hh)[0]
V = R(1, 3) * 36 * hsol
ascending([18 * sqrt(2), 36, 36 * sqrt(2), 36 * sqrt(3), 108 * sqrt(2)])
assert sp.simplify(V - 36 * sqrt(2)) == 0
key("geom-11", 2)

# 12: numeric integration over square [0,2]^2, discs radius 1 at side midpoints
cs = [(1, 0), (1, 2), (0, 1), (2, 1)]
N = 1200
petal = 0
covered = 0
for i in range(N):
    px = (i + 0.5) * 2 / N
    for j in range(N):
        py = (j + 0.5) * 2 / N
        n = sum(1 for cx, cy in cs if (px - cx) ** 2 + (py - cy) ** 2 <= 1)
        petal += n >= 2
        covered += n >= 1
cell = (2 / N) ** 2
assert abs(covered * cell - 4) < 1e-9                  # semicircles cover the square
assert abs(petal * cell - (2 * math.pi - 4)) < 0.01, petal * cell
ascending([4 - pi, pi - 2, 2 * pi - 4, pi, 2 * pi - 2])
key("geom-12", 2)

# 13: regular tetrahedron with edge 2 from alternate cube vertices (cube edge sqrt2)
s2 = sqrt(2)
P = [sp.Matrix(v) * s2 for v in [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]]
assert all(sp.simplify((P[i] - P[j]).norm() - 2) == 0 for i in range(4) for j in range(i))
Vt = abs(sp.Matrix.hstack(P[1] - P[0], P[2] - P[0], P[3] - P[0]).det()) / 6
ascending([s2 / 3, 2 * s2 / 3, 1, 4 * s2 / 3, 2 * s2])
assert sp.simplify(Vt - 2 * s2 / 3) == 0
key("geom-13", 1)

# 14: incentre formula (weighted by opposite sides), circumcentre = hypotenuse midpoint
Av, Bv, Cv = sp.Matrix([0, 0]), sp.Matrix([6, 0]), sp.Matrix([0, 8])
a, b, c = (Bv - Cv).norm(), (Av - Cv).norm(), (Av - Bv).norm()
I = (a * Av + b * Bv + c * Cv) / (a + b + c)
O = (Bv + Cv) / 2
assert list(I) == [2, 2] and list(O) == [3, 4]
assert all(sp.simplify((O - X).norm() - 5) == 0 for X in (Av, Bv, Cv))
ascending([1, 2, sqrt(5), 3, sqrt(13), 5])
assert (O - I).norm() == sqrt(5)
key("geom-14", 2)

# 15
t = sp.symbols("t", positive=True)  # t = AD/AB
tv = sp.solve(sp.Eq(t ** 2, R(1, 2)), t)[0]
ratio = sp.simplify(tv / (1 - tv))
ascending([sqrt(2) - 1, 1, sqrt(2), 2, sqrt(2) + 1, 3])
assert sp.simplify(ratio - (sqrt(2) + 1)) == 0
key("geom-15", 4)

# 16: III counterexample: kite A(1,0), C(-1,0), B(cos t, sin t), D(cos t, -sin t) on unit circle
tt = 1.0
Ak, Ck, Bk, Dk = (1, 0), (-1, 0), (math.cos(tt), math.sin(tt)), (math.cos(tt), -math.sin(tt))
dd = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
assert abs(dd(Ak, Bk) - dd(Ak, Dk)) < 1e-12 and abs(dd(Ck, Bk) - dd(Ck, Dk)) < 1e-12
assert abs(dd(Ak, Bk) - dd(Ck, Bk)) > 0.1        # not a rhombus, so not a square
# II: rhombus on circle -> opposite angles equal and supplementary -> 90
key("geom-16", 4)

# 17: section of cube [0,2]^3 by x+y+z=3
import itertools
verts = [sp.Matrix(p) for p in itertools.permutations([0, 1, 2])]
cen = sp.Matrix([1, 1, 1])
nrm = sp.Matrix([1, 1, 1]) / sqrt(3)
e1 = (verts[0] - cen).normalized()
e2 = nrm.cross(e1)
ang = lambda v: math.atan2(float((v - cen).dot(e2)), float((v - cen).dot(e1)))
verts.sort(key=ang)
area = 0
for i in range(6):
    area += (verts[i] - cen).cross(verts[(i + 1) % 6] - cen).dot(nrm) / 2
assert all(sum(v) == 3 for v in verts)
ascending([2 * sqrt(3), 2 * sqrt(6), 3 * sqrt(3), 4 * sqrt(2), 6])
assert sp.simplify(area - 3 * sqrt(3)) == 0, area
key("geom-17", 2)

# 18: cross-section: apex (0,4), base from (-3,0) to (3,0). Side line: 4x + 3y = 12 (right side).
u, rho = sp.symbols("u rho", positive=True)
distline = lambda yc: (12 - 3 * yc) / 5         # distance from (0,yc) to 4x+3y=12
r1 = sp.solve(sp.Eq(distline(u), u), u)[0]      # centre height = radius (touches base)
assert r1 == R(3, 2)
sol = sp.solve([sp.Eq(distline(u), rho), sp.Eq(u - rho, 2 * r1)], [u, rho], dict=True)[0]
ascending([R(1, 4), R(3, 8), R(1, 2), R(3, 4), R(15, 16)])
assert sol[rho] == R(3, 8)
key("geom-18", 1)

assert sorted(Q) == ["geom-%02d" % i for i in range(1, 19)]
assert Counter(q["difficulty"] for q in Q.values()) == {1: 2, 2: 4, 3: 6, 4: 4, 5: 2}
for q in Q.values():
    assert 4 <= len(q["options"]) <= 8
    for k_ in q["distractors"]:
        assert int(k_) != q["answer"] and int(k_) < len(q["options"]), q["id"]
    if q["figure"]:
        assert "viewBox" in q["figure"]["svg"] and "currentColor" in q["figure"]["svg"]
print("ALL OK")
