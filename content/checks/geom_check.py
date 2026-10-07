"""Verification for content/questions/geom.json. Run: python3 content/checks/geom_check.py

Every original and twin: the keyed answer is recomputed independently (coordinates, sympy, brute
force) and every other option is shown to be wrong (exactly one option matches)."""
import itertools, json, math, os
from collections import Counter
import sympy as sp
from sympy import sqrt, pi, Rational as R, cbrt, Matrix as M

HERE = os.path.dirname(os.path.abspath(__file__))
QL = json.load(open(os.path.join(HERE, "..", "questions", "geom.json")))
Q = {q["id"]: q for q in QL}
done = set()
COMBO = ["none of them", "I only", "II only", "III only", "I and II only",
         "I and III only", "II and III only", "I, II and III"]


def key(qid, idx):
    q = Q[qid]
    assert q["answer"] == idx, (qid, q["answer"], idx)
    assert len(set(q["options"])) == len(q["options"]), qid
    done.add(qid)


def numeric(qid, opts, truth, ascending=True):
    assert len(opts) == len(Q[qid]["options"]), qid
    f = [float(v) for v in opts]
    if ascending:
        assert f == sorted(f) and len(set(f)) == len(f), (qid, f)
    hits = [i for i, v in enumerate(opts) if abs(float(v) - float(truth)) < 1e-9]
    assert len(hits) == 1, (qid, hits, float(truth))
    key(qid, hits[0])


def pick(qid, cands, truth):
    """Non-numeric options given as tuples of numbers; exactly one must equal truth."""
    assert len(cands) == len(Q[qid]["options"])
    hits = [i for i, c in enumerate(cands) if all(abs(float(a) - float(b)) < 1e-9 for a, b in zip(c, truth))]
    assert len(hits) == 1, (qid, hits)
    key(qid, hits[0])


def combo(qid, truths):
    assert Q[qid]["options"] == COMBO
    key(qid, COMBO.index({(0, 0, 0): "none of them", (1, 0, 0): "I only", (0, 1, 0): "II only", (0, 0, 1): "III only",
                          (1, 1, 0): "I and II only", (1, 0, 1): "I and III only", (0, 1, 1): "II and III only",
                          (1, 1, 1): "I, II and III"}[tuple(int(bool(t)) for t in truths)]))


def bearing_vec(deg, dist):
    t = math.radians(deg)
    return (dist * math.sin(t), dist * math.cos(t))      # (east, north)


def bearing_of(frm, to):
    return math.degrees(math.atan2(to[0] - frm[0], to[1] - frm[1])) % 360


def area2(p, q):  # area of triangle O p q
    return abs(p[0] * q[1] - p[1] * q[0]) / 2


# 01 bearings
P = (0.0, 0.0)
Qp = bearing_vec(60, 10)
Rp = (Qp[0] + bearing_vec(150, 10 * math.sqrt(3))[0], Qp[1] + bearing_vec(150, 10 * math.sqrt(3))[1])
numeric("geom-01", [120, 180, 240, 270, 300], round(bearing_of(Rp, P), 9))
# 01b: A origin, B (8,0); C on bearing 030 from A and 300 from B
u, v = bearing_vec(30, 1), bearing_vec(300, 1)
# A + s u = B + t v
s_, t_ = sp.symbols("s t")
sol = sp.solve([s_ * sp.sin(pi / 6) - (8 + t_ * sp.sin(5 * pi / 3)), s_ * sp.cos(pi / 6) - t_ * sp.cos(5 * pi / 3)], [s_, t_])
assert sol[s_] > 0 and sol[t_] > 0
numeric("geom-01b", [4, 4 * sqrt(2), 4 * sqrt(3), 8, 8 * sqrt(3)], sp.nsimplify(sol[t_]))

# 02: centre C with P' - C = k (P - C), area * k^2
k = R(-3, 2)
Pp, Pi_ = M([-3, 0]), M([7, 5])
C = (Pp - k * Pi_) / (1 - k)
assert Pp == C + k * (Pi_ - C)
pick("geom-02", [(2, R(5, 2), 18), (3, 3, 12), (3, 3, 18), (1, 2, 18), (3, 3, 27)], (C[0], C[1], 8 * k ** 2))
# 02b
T = [M([1, 0]), M([7, 0]), M([1, 9])]
Tp = [M([6, 5]), M([2, 5]), M([6, -1])]
kk = (Tp[1] - Tp[0])[0] / (T[1] - T[0])[0]
Cb = (Tp[0] - kk * T[0]) / (1 - kk)
assert all(Tp[i] == Cb + kk * (T[i] - Cb) for i in range(3))
pick("geom-02b", [(R(-3, 2), 4, 3), (R(-2, 3), 4, 3), (R(2, 3), 4, 3), (R(-2, 3), R(7, 2), R(5, 2)), (R(-2, 3), 3, 2)],
     (kk, Cb[0], Cb[1]))


# 03 / 03b: brute force over all stack heights consistent with plan and both elevations
def stacks(front, side):
    cols, rows = len(front), len(side)
    totals = []
    for hs in itertools.product(range(1, max(front) + 1), repeat=cols * rows):
        h = [[hs[r * cols + c] for c in range(cols)] for r in range(rows)]
        if all(max(h[r][c] for r in range(rows)) == front[c] for c in range(cols)) and \
           all(max(h[r]) == side[r] for r in range(rows)):
            totals.append(sum(hs))
    return min(totals), max(totals)


lo, hi = stacks([3, 2, 1], [3, 3, 1])
assert (lo, hi) == (14, 15)
numeric("geom-03", [9, 13, 14, 15, 18], lo)
assert "viewBox" in Q["geom-03"]["figure"]["svg"]
lo, hi = stacks([2, 3, 2], [3, 2])
assert (lo, hi) == (10, 13)
numeric("geom-03b", [6, 10, 12, 13, 14], hi)

# 04: unit circle, OAB = 25 deg, C on major arc
aob = math.radians(130)
A, B = (1.0, 0.0), (math.cos(aob), math.sin(aob))


def ang(p, vtx, q):
    a_ = (p[0] - vtx[0], p[1] - vtx[1]); b_ = (q[0] - vtx[0], q[1] - vtx[1])
    return math.degrees(math.acos((a_[0] * b_[0] + a_[1] * b_[1]) / (math.hypot(*a_) * math.hypot(*b_))))


assert abs(ang((0, 0), A, B) - 25) < 1e-9
vals = {round(ang(A, (math.cos(t), math.sin(t)), B), 9) for t in (3.0, 4.0, 5.5)}
assert len(vals) == 1
numeric("geom-04", [25, 50, 65, 115, 130], vals.pop())
# 04b: unit circle, A=(1,0), tangent at A is vertical; find B with tangent-chord angle 58 on the minor-arc side
th = math.radians(116)            # candidate: B at angle 116 deg; verify tangent-chord angle is 58
Bb = (math.cos(th), math.sin(th))
chord = (Bb[0] - 1, Bb[1])
tangent_up = (0, 1)               # direction of tangent towards the side where B lies (minor arc is above)
tc = math.degrees(math.acos((chord[0] * tangent_up[0] + chord[1] * tangent_up[1]) / math.hypot(*chord)))
assert abs(tc - 58) < 1e-9
numeric("geom-04b", [32, 58, 64, 116, 122], 116)

# 05: hemisphere r=3 + cone r=3 h=4, formulas as stated
l = sqrt(3 ** 2 + 4 ** 2)
numeric("geom-05", [30 * pi, 33 * pi, 42 * pi, 51 * pi, 60 * pi], pi * 3 * l + R(1, 2) * 4 * pi * 9)
h5 = sqrt(10 ** 2 - 6 ** 2)
n5 = (R(1, 3) * pi * 36 * h5) / (R(4, 3) * pi * 8)
assert n5 == int(n5)
numeric("geom-05b", [9, 11, 12, 27, 36], n5)


# 06 / 06b: congruence statements
def ssa_count(c, Adeg, a):   # angle A, adjacent side c=AB, opposite side a=BC
    Ar = math.radians(Adeg); sC = c * math.sin(Ar) / a
    if sC > 1 + 1e-12:
        return 0
    if abs(sC - 1) < 1e-12:
        return 1
    C1 = math.asin(sC)
    return sum(1 for Cc in {C1, math.pi - C1} if Ar + Cc < math.pi - 1e-9)


assert ssa_count(8, 30, 5) == 2           # I fails (SSA counterexample)
# II: AAS -> third angle known -> ASA (standard criterion). III: RHS -> third side fixed by Pythagoras -> SSS.
# With a right angle at A, SSA has a unique solution: the non-included-angle count is 1.
assert ssa_count(5, 90, 13) == 1
combo("geom-06", [ssa_count(8, 30, 5) == 1, True, True])
# 06b III: right triangles with equal hypotenuse and area: legs determined
a_, b_ = sp.symbols("a b", positive=True)
legs = sp.solve([a_ ** 2 + b_ ** 2 - 25, a_ * b_ - 12], [a_, b_], dict=True)
assert {frozenset((d[a_], d[b_])) for d in legs} == {frozenset((3, 4))}
# I: similar with equal area -> k^2 = 1 -> k = 1
kk_ = sp.symbols("kk", positive=True)
assert sp.solve(sp.Eq(kk_ ** 2, 1), kk_) == [1]
combo("geom-06b", [True, ssa_count(8, 30, 5) == 1, True])

# 07
av, bv = M([6, 2]), M([-2, 6])
Mv = av + R(3, 4) * (bv - av)
kq, tq = sp.symbols("kq tq")
s7 = sp.solve(list(kq * Mv - (bv + tq * av)), [kq, tq])
numeric("geom-07", [R(3, 4), 1, R(4, 3), 2, 4], s7[kq])
# 07b
s1, s2 = sp.symbols("s1 s2")
s7b = sp.solve(list(s1 * M([4, 3]) + s2 * M([-3, 4]) - M([0, 25])), [s1, s2])
assert s7b[s1] > 0 and s7b[s2] > 0
numeric("geom-07b", [5, 7, 10, 12, 14], s7b[s1] + s7b[s2] + M([0, 25]).norm() / 5)

# 08: O origin, P=(13,0); Q=(5,0); tangent at Q is x=5; meets PA where?
xA = R(25, 13); yA = sqrt(25 - xA ** 2)
assert sp.simplify(M([xA, yA]).dot(M([13 - xA, -yA]))) == 0        # OA perpendicular to AP
# line PA: P + t (A - P); x = 5
tt = (5 - 13) / (xA - 13)
yX = tt * yA
numeric("geom-08", [R(10, 3), R(60, 13), R(20, 3), 8, R(120, 13)], 2 * yX)
# 08b: numeric construction. Circle centre origin radius 1; pick A, B, C on circle so that TB:BC = 4:5
def make(theta_b, theta_c):
    Bq = (math.cos(theta_b), math.sin(theta_b)); Cq = (math.cos(theta_c), math.sin(theta_c))
    # tangent at A=(1,0) is x=1; line CB meets x=1 at T
    tpar = (1 - Cq[0]) / (Bq[0] - Cq[0])
    Tq = (1, Cq[1] + tpar * (Bq[1] - Cq[1]))
    return Bq, Cq, Tq


import random
random.seed(3)
ratios = set()
for _ in range(5):
    tc_ = random.uniform(2.0, 4.0)
    # solve for theta_b so that TB/BC = 4/5 (bisection), B between C and T
    f = lambda tb: (lambda Bq, Cq, Tq: math.dist(Tq, Bq) / math.dist(Bq, Cq) - 0.8)(*make(tb, tc_))
    lo_, hi_ = 0.05, tc_ - 0.05
    if f(lo_) * f(hi_) > 0:
        continue
    for _i in range(200):
        mid = (lo_ + hi_) / 2
        if f(lo_) * f(mid) <= 0:
            hi_ = mid
        else:
            lo_ = mid
    Bq, Cq, Tq = make(lo_, tc_)
    Aq = (1, 0)
    assert abs(math.dist(Tq, Aq) ** 2 - math.dist(Tq, Bq) * math.dist(Tq, Cq)) < 1e-6
    ratios.add(round(math.dist(Aq, Bq) / math.dist(Aq, Cq), 6))
assert len(ratios) >= 1 and all(abs(r_ - 2 / 3) < 1e-6 for r_ in ratios), ratios
numeric("geom-08b", [R(4, 9), R(1, 2), R(5, 9), R(2, 3), R(3, 2)], R(2, 3))

# 09
d9 = sp.symbols("d9", positive=True)
newd = sp.solve(sp.Eq((d9 / 6) ** 3, 2), d9)[0]
numeric("geom-09", [6 * cbrt(2), 6 * sqrt(2), 9, 6 * cbrt(4), 12], newd)
numeric("geom-09b", [6, 18, 54, 81, 162], 2 * sqrt(R(450, 50)) ** 3)

# 10: I regular 165; II equiangular convex with 100 deg; III convex with exactly four acute angles
I10 = 360 % (180 - 165) == 0
II10 = any(n * (180 - 100) == 360 for n in range(3, 100))
# III: four exterior angles each > 90 would exceed 360 -> search small integer exterior angles
# III: each acute interior angle has exterior angle > 90, and convex exterior angles sum to 360,
# so four acute angles need four numbers > 90 summing to less than 360: impossible (minimum sum > 360).
III10 = 4 * 90 < 360
combo("geom-10", [I10, II10, III10])
# 10b
I10b = sum([100, 110, 120, 130, 140, 150]) == (6 - 2) * 180
II10b = any(180 - 360 / n == 4 * (360 / n) for n in range(3, 100))
III10b = (5 - 2) * 180 - 2 * 90 == 3 * 120 and all(0 < e < 180 for e in (90, 90, 60, 60, 60)) and sum((90, 90, 60, 60, 60)) == 360
combo("geom-10b", [I10b, II10b, III10b])

# 11: octahedron with vertices (+-a,0,0),(0,+-a,0),(0,0,+-a), edge a*sqrt2 = 6
a11 = 6 / sqrt(2)
verts = [M(v) * a11 for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
assert sp.simplify((verts[0] - verts[2]).norm() - 6) == 0
V11 = 8 * abs(M.hstack(verts[0], verts[2], verts[4]).det()) / 6     # eight congruent corner tetrahedra
numeric("geom-11", [36 * sqrt(2), 72, 72 * sqrt(2), 72 * sqrt(3), 216 * sqrt(2)], sp.simplify(V11))
# 11b: cube [0,4]^3, apex above (2,2,4) with sloping edge 2 sqrt5
hh = sp.symbols("hh", positive=True)
h11 = sp.solve(sp.Eq(8 + hh ** 2, 20), hh)[0]
apex = M([2, 2, 4 + h11])
face = (M([4, 0, 4]) - apex).cross(M([0, 0, 4]) - apex).norm() / 2
numeric("geom-11b", [80 + 16 * sqrt(3), 112, 80 + 16 * sqrt(5), 128, 96 + 16 * sqrt(5)], 5 * 16 + 4 * sp.simplify(face))


# 12 / 12b: grid integration
def grid(inside, x0, x1, y0, y1, N=1500):
    c = 0
    for i in range(N):
        px = x0 + (x1 - x0) * (i + 0.5) / N
        for j in range(N):
            c += inside(px, y0 + (y1 - y0) * (j + 0.5) / N)
    return c * (x1 - x0) * (y1 - y0) / N ** 2


arch = grid(lambda p, q: q >= 0 and p * p + q * q <= 4 and (p - 2) ** 2 + q * q <= 4, 0, 2, 0, 2)
exact12 = 2 * (R(1, 2) * 4 * pi / 3) - sqrt(3)
assert abs(arch - float(exact12)) < 0.01
numeric("geom-12", [4 * pi / 3 - 2 * sqrt(3), 4 * pi / 3 + sqrt(3) - 4, 2 * pi / 3, 4 * pi / 3 - sqrt(3), 4 * pi / 3], exact12)
cs = [(1, 0), (1, 2), (0, 1), (2, 1)]
petal = grid(lambda p, q: sum((p - a) ** 2 + (q - b) ** 2 <= 1 for a, b in cs) >= 2, 0, 2, 0, 2)
assert abs(petal - float(2 * pi - 4)) < 0.01
numeric("geom-12b", [4 - pi, pi - 2, 2 * pi - 4, pi, 2 * pi - 2], 2 * pi - 4)
for qid in ("geom-12", "geom-12b"):
    svg = Q[qid]["figure"]["svg"]
    assert "viewBox" in svg and "currentColor" in svg

# 13: regular tetrahedron edge 2 from cube corners; inradius = distance from centroid to a face
s2 = sqrt(2)
Pt = [M(v) * s2 for v in [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]]
assert all(sp.simplify((Pt[i] - Pt[j]).norm() - 2) == 0 for i in range(4) for j in range(i))
G = (Pt[0] + Pt[1] + Pt[2] + Pt[3]) / 4
nrm = (Pt[2] - Pt[1]).cross(Pt[3] - Pt[1])
r13 = abs((G - Pt[1]).dot(nrm)) / nrm.norm()
numeric("geom-13", [sqrt(6) / 18, sqrt(6) / 6, 2 * sqrt(6) / 9, sqrt(6) / 3, sqrt(6) / 2], sp.simplify(r13))
# 13b: sphere centre (0,0,r) touches base z=0 and face through (3,-3,0),(3,3,0),(0,0,4)
rr = sp.symbols("rr", positive=True)
F1, F2, F3 = M([3, -3, 0]), M([3, 3, 0]), M([0, 0, 4])
n13 = (F2 - F1).cross(F3 - F1)
dist_face = sp.Abs((M([0, 0, rr]) - F1).dot(n13)) / n13.norm()
r13b = [s for s in sp.solve(sp.Eq(dist_face, rr), rr) if s < 4][0]
numeric("geom-13b", [R(1, 2), R(4, 3), R(3, 2), 2, R(12, 5)], r13b)


# 14 / 14b: intersection of lines in coordinates (a,b basis = standard basis; area ratios are affine invariants)
def meet(P1, D1, P2, D2):
    l1, l2 = sp.symbols("l1 l2")
    s = sp.solve(list(P1 + l1 * D1 - P2 - l2 * D2), [l1, l2])
    return P1 + s[l1] * D1


def poly_area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2


O, Av, Bv = M([0, 0]), M([1, 0]), M([0, 1])
Mm, Nn = Av / 2, Bv * R(2, 3)
X = meet(Av, Nn - Av, Bv, Mm - Bv)
frac14 = poly_area([O, Mm, X, Nn]) / poly_area([O, Av, Bv])
numeric("geom-14", [R(7, 30), R(1, 4), R(1, 3), R(5, 12), R(7, 12)], frac14)
# also check on a non-right triangle (affine invariance)
Av2, Bv2 = M([5, 1]), M([2, 4])
X2 = meet(Av2, Bv2 * R(2, 3) - Av2, Bv2, Av2 / 2 - Bv2)
assert poly_area([O, Av2 / 2, X2, Bv2 * R(2, 3)]) / poly_area([O, Av2, Bv2]) == frac14
a_v, c_v = M([4, 0]), M([1, 3])
Pm = a_v + c_v / 2
Rr = c_v / 3
S = meet(O, Pm, a_v, Rr - a_v)
frac14b = poly_area([O, S, Rr]) / abs(a_v[0] * c_v[1] - a_v[1] * c_v[0])
numeric("geom-14b", [R(1, 15), R(1, 12), R(1, 9), R(2, 15), R(4, 21)], frac14b)

# 15
tq_ = sp.symbols("tq_", positive=True)
t15 = sp.solve(sp.Eq(tq_ ** 2, R(1, 2)), tq_)[0]
numeric("geom-15", [sqrt(2) - 1, 1, sqrt(2), 2, sqrt(2) + 1], sp.simplify(t15 / (1 - t15)))
# 15b: AD = AB/sqrt3, AE = AB sqrt(2/3)
AD, AE = 1 / sqrt(3), sqrt(R(2, 3))
truth = (1, sp.simplify((AE - AD) / AD), sp.simplify((1 - AE) / AD))
assert sp.simplify(AD ** 2 - R(1, 3)) == 0 and sp.simplify(AE ** 2 - R(2, 3)) == 0
pick("geom-15b", [(1, 1, 1), (1, 2, 3), (1, sqrt(2) - 1, sqrt(3) - sqrt(2)), (1, sqrt(2), sqrt(3)), (1, 3, 5)], truth)

# 16: III counterexample kite; II rhombus cyclic -> square
tt16 = 1.0
Ak, Ck, Bk, Dk = (1, 0), (-1, 0), (math.cos(tt16), math.sin(tt16)), (math.cos(tt16), -math.sin(tt16))
assert abs(math.dist(Ak, Bk) - math.dist(Ak, Dk)) < 1e-12 and abs(math.dist(Ck, Bk) - math.dist(Ck, Dk)) < 1e-12
assert abs(math.dist(Ak, Bk) - math.dist(Ck, Bk)) > 0.1
# I: cyclic quad opposite angles: random check
random.seed(4)
for _ in range(20):
    ts = sorted(random.uniform(0, 2 * math.pi) for _ in range(4))
    pts = [(math.cos(t), math.sin(t)) for t in ts]
    assert abs(ang(pts[3], pts[0], pts[1]) + ang(pts[1], pts[2], pts[3]) - 180) < 1e-9
combo("geom-16", [True, True, False])
# 16b: II counterexample: B and D on the same side of a non-diameter chord AC
pts = {k_: (math.cos(t), math.sin(t)) for k_, t in {"A": 0.3, "C": 2.0, "B": 3.5, "D": 5.0}.items()}
assert abs(ang(pts["A"], pts["B"], pts["C"]) - ang(pts["A"], pts["D"], pts["C"])) < 1e-9
assert abs(math.dist(pts["A"], pts["C"]) - 2) > 0.1
# I: AC diameter -> both 90; III: equal inscribed angles at B -> equal chords (random check)
for _ in range(20):
    tb = random.uniform(0, 2 * math.pi); half = random.uniform(0.2, 1.4); td = tb + math.pi
    Bq = (math.cos(tb), math.sin(tb)); Dq = (math.cos(td), math.sin(td))
    # A and C symmetric about line BD -> angles ABD = CBD
    Aq = (math.cos(td + half), math.sin(td + half)); Cq = (math.cos(td - half), math.sin(td - half))
    assert abs(ang(Aq, Bq, Dq) - ang(Cq, Bq, Dq)) < 1e-9 and abs(math.dist(Aq, Dq) - math.dist(Cq, Dq)) < 1e-9
combo("geom-16b", [True, False, True])

# 17: hexagon x+y+z=3 in cube [0,2]^3
verts = [M(p) for p in itertools.permutations([0, 1, 2])]
cen = M([1, 1, 1]); nrm = M([1, 1, 1]) / sqrt(3)
e1 = (verts[0] - cen).normalized(); e2 = nrm.cross(e1)
verts.sort(key=lambda v_: math.atan2(float((v_ - cen).dot(e2)), float((v_ - cen).dot(e1))))
area17 = sum((verts[i] - cen).cross(verts[(i + 1) % 6] - cen).dot(nrm) / 2 for i in range(6))
numeric("geom-17", [2 * sqrt(3), 2 * sqrt(6), 3 * sqrt(3), 4 * sqrt(2), 6], sp.simplify(area17))
# 17b: plane x + y = 2z; intersection with all 12 edges of the cube
edges = []
for a0 in itertools.product([0, 2], repeat=3):
    for i in range(3):
        if a0[i] == 0:
            b0 = list(a0); b0[i] = 2
            edges.append((M(a0), M(b0)))
pts = set()
for p0, p1 in edges:
    lam = sp.symbols("lam")
    g = lambda v_: v_[0] + v_[1] - 2 * v_[2]
    if g(p0) == 0:
        pts.add(tuple(p0))
    if g(p1) == 0:
        pts.add(tuple(p1))
    if g(p0) * g(p1) < 0:
        l_ = sp.solve(g(p0 + lam * (p1 - p0)), lam)[0]
        pts.add(tuple(p0 + l_ * (p1 - p0)))
assert (2, 0, 1) in pts and (0, 0, 0) in pts and (2, 2, 2) in pts
pts = [M(p) for p in pts]
assert len(pts) == 4
cen = sum(pts, M([0, 0, 0])) / 4
nrm = M([1, 1, -2]) / sqrt(6)
e1 = (pts[0] - cen).normalized(); e2 = nrm.cross(e1)
pts.sort(key=lambda v_: math.atan2(float((v_ - cen).dot(e2)), float((v_ - cen).dot(e1))))
area17b = abs(sum((pts[i] - cen).cross(pts[(i + 1) % 4] - cen).dot(nrm) / 2 for i in range(4)))
numeric("geom-17b", [2 * sqrt(3), 2 * sqrt(6), 5, 3 * sqrt(3), 4 * sqrt(2)], sp.simplify(area17b))

# 18: cross-section apex (0,4), base (-3,0)-(3,0); right side 4x + 3y = 12
uu, rho = sp.symbols("uu rho", positive=True)
distline = lambda yc: (12 - 3 * yc) / 5
r1 = sp.solve(sp.Eq(distline(uu), uu), uu)[0]
sol18 = sp.solve([sp.Eq(distline(uu), rho), sp.Eq(uu - rho, 2 * r1)], [uu, rho], dict=True)[0]
numeric("geom-18", [R(1, 4), R(3, 8), R(1, 2), R(3, 4), R(15, 16)], sol18[rho])
# 18b: vertex at origin, axis = y-axis, side line at 30 deg to axis: x = y tan30. Centres (0, d) with dist to line = r
d1, d2, Rb = sp.symbols("d1 d2 Rb", positive=True)
dist_to_side = lambda d: d * sp.sin(pi / 6)
d1v = sp.solve(sp.Eq(dist_to_side(d1), 1), d1)[0]
sol18b = sp.solve([sp.Eq(dist_to_side(d2), Rb), sp.Eq(d2 - d1v, 1 + Rb)], [d2, Rb], dict=True)[0]
numeric("geom-18b", [1, 2, 3, 2 + sqrt(3), 7 + 4 * sqrt(3)], sol18b[Rb])

# ---------------------------------------------------------------- structure
ids = ["geom-%02d" % i for i in range(1, 19)]
assert sorted(Q) == sorted(ids + [i + "b" for i in ids])
assert done == set(Q), set(Q) - done
assert Counter(Q[i]["difficulty"] for i in ids) == {2: 2, 3: 6, 4: 6, 5: 4}
for i in ids:
    a0, b0 = Q[i], Q[i + "b"]
    assert a0["difficulty"] == b0["difficulty"] and a0["answer"] != b0["answer"], i
    assert a0["family"] == b0["family"] == i
for q in QL:
    n = len(q["options"])
    assert n == 5 or q["options"] == COMBO, q["id"]
    assert len(q["distractors"]) >= 3, q["id"]
    for k_ in q["distractors"]:
        assert int(k_) != q["answer"] and int(k_) < n, q["id"]
    if q["figure"]:
        assert "viewBox" in q["figure"]["svg"] and "currentColor" in q["figure"]["svg"]
# formulae for spheres, cones and pyramids must be stated in the stem when a volume/surface formula is needed
for qid in ("geom-05", "geom-05b", "geom-11", "geom-13", "geom-13b"):
    assert "[" in Q[qid]["stem"] and ("volume of" in Q[qid]["stem"] or "surface area" in Q[qid]["stem"]), qid
print("ALL OK")
