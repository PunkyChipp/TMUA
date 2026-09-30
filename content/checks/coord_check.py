"""Verification for content/questions/coord.json. Run: python3 content/checks/coord_check.py"""
import json, os, random
import sympy as sp
from sympy import Rational as R, sqrt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {q['id']: q for q in json.load(open(os.path.join(ROOT, 'content/questions/coord.json'), encoding='utf-8'))}
x, y, m, c, t = sp.symbols('x y m c t', real=True)

assert len(Q) == 18 and sorted(Q) == [f'coord-{i:02d}' for i in range(1, 19)]
assert sorted(q['difficulty'] for q in Q.values()) == [1]*2 + [2]*4 + [3]*6 + [4]*4 + [5]*2
for q in Q.values():
    assert 4 <= len(q['options']) <= 8 and 0 <= q['answer'] < len(q['options'])
    assert len(set(q['options'])) == len(q['options']), q['id']
    assert len(q['distractors']) >= 2
    for key in q['distractors']:
        assert int(key) != q['answer'] and int(key) < len(q['options']), (q['id'], key)

ROM = {(False, False, False): 0, (True, False, False): 1, (False, True, False): 2, (False, False, True): 3,
       (True, True, False): 4, (True, False, True): 5, (False, True, True): 6, (True, True, True): 7}

def pick(qid, values, target):
    """values: numeric value for each option in order; exactly one equals target and it is the key."""
    q = Q[qid]
    assert len(values) == len(q['options']), qid
    hits = [i for i, v in enumerate(values) if sp.simplify(sp.sympify(v) - target) == 0]
    assert hits == [q['answer']], (qid, hits)
    # numeric options should be ascending
    nums = [float(sp.sympify(v)) for v in values]
    assert nums == sorted(nums), qid

def pick_obj(qid, values, target):
    q = Q[qid]
    assert len(values) == len(q['options']), qid
    hits = [i for i, v in enumerate(values) if v == target]
    assert hits == [q['answer']], (qid, hits)

# 01
line = sp.Line(sp.Point(1, 2), sp.Point(4, 11))
cval = sp.solve(line.equation(x, y).subs(x, 0), y)[0]
pick('coord-01', [-3, -1, R(1, 3), 3, 5], cval)

# 02
circ = x**2 + y**2 - 6*x + 4*y - 12
centre = (3, -2)
assert sp.expand((x - 3)**2 + (y + 2)**2 - 25 - circ) == 0
pick_obj('coord-02', [((3, -2), 5), ((3, -2), 1), ((-3, 2), 5), ((3, -2), sqrt(12)), ((3, -2), 25)], (centre, 5))

# 03 perpendicular bisector
A, B = sp.Point(-1, 3), sp.Point(5, -1)
pb = sp.Segment(A, B).perpendicular_bisector()
opts = [3*x - 2*y - 4, 2*x - 3*y - 1, 3*x + 2*y - 8, 2*x + 3*y - 7, 3*x - 2*y - 5]
def same_line(e1, e2):
    a1, b1, c1 = [sp.Poly(e1, x, y).coeff_monomial(mm) for mm in (x, y, 1)]
    a2, b2, c2 = [sp.Poly(e2, x, y).coeff_monomial(mm) for mm in (x, y, 1)]
    return sp.Matrix([[a1, b1, c1], [a2, b2, c2]]).rank() == 1
hits = [i for i, e in enumerate(opts) if same_line(e, pb.equation(x, y))]
assert hits == [Q['coord-03']['answer']]

# 04 triangle area
area = abs(sp.Triangle(sp.Point(1, 2), sp.Point(5, 3), sp.Point(2, 7)).area)
pick('coord-04', [R(17, 2), 9, R(19, 2), 10, 19], area)

# 05 tangency
disc = sp.discriminant(sp.expand(x**2 + (x + c)**2 - 8), x)
sols = set(sp.solve(disc, c))
assert sols == {4, -4}
opt_sets = [{2, -2}, {2*sqrt(2), -2*sqrt(2)}, {4}, {4, -4}, {8, -8}]
assert [s == sols for s in opt_sets].index(True) == Q['coord-05']['answer'] and sum(s == sols for s in opt_sets) == 1

# 06
P = sp.solve([2*x + 3*y - 7, 4*x - y - 7], [x, y])
d6 = sp.Point(P[x], P[y]).distance(sp.Point(5, 5))
pick('coord-06', [3, 4, 5, 6, 7], d6)

# 07 tangent x-intercept
C7 = sp.Circle(sp.Point(2, -1), 5)
assert sp.Point(5, 3) in C7
tan = C7.tangent_lines(sp.Point(5, 3))[0]
a7 = sp.solve(tan.equation(x, y).subs(y, 0), x)[0]
pick('coord-07', [1, R(11, 4), R(27, 4), R(29, 4), 9], a7)

# 08 chord
pts = sp.Circle(sp.Point(0, 0), sqrt(13)).intersection(sp.Line(sp.Point(0, 1), sp.Point(1, 2)))
L8 = pts[0].distance(pts[1])
pick('coord-08', [5*sqrt(2)/2, 5, 5*sqrt(2), 2*sqrt(13), 10], L8)

# 09 circles
def n_int(a):
    return len(sp.Circle(sp.Point(0, 0), 2).intersection(sp.Circle(sp.Point(a, 4), 3)))
for a in [R(n, 4) for n in range(-11, 12)]:  # -2.75..2.75
    assert n_int(a) == 2
assert n_int(3) == 1 and n_int(-3) == 1
touch = [a for a in [R(n, 4) for n in range(-80, 81)] if n_int(a) == 1]
assert sorted(touch) == [-3, 3]
# III: inside needs d < 1; d = sqrt(a^2+16) >= 4 always
a_ = sp.Symbol('a', real=True)
assert sp.solveset(a_**2 + 16 < 1, a_, sp.S.Reals) == sp.S.EmptySet
assert ROM[(True, True, False)] == Q['coord-09']['answer']

# 10 family kx + y = 2k + 3
k = sp.Symbol('k', real=True)
L = k*x + y - 2*k - 3
assert sp.simplify(L.subs({x: 2, y: 3})) == 0
I10 = True
II10 = False  # coefficient of y is 1 for all k: never vertical
assert sp.Poly(L, x, y).coeff_monomial(y) == 1
grad = -sp.Poly(L, x, y).coeff_monomial(x) / sp.Poly(L, x, y).coeff_monomial(y)
III10 = len(sp.solve(sp.Eq(grad * 1, -1), k)) > 0  # perpendicular to gradient 1
assert ROM[(I10, II10, III10)] == Q['coord-10']['answer']

# 11 locus PA = 2PB
loc = sp.expand(x**2 + y**2 - 4*((x - 3)**2 + y**2))
assert sp.expand(-loc / 3 - ((x - 4)**2 + y**2 - 4)) == 0
pick_obj('coord-11', [((-1, 0), 2), ((4, 0), 2), ((2, 0), 2), ((4, 0), 2*sqrt(7)), ((4, 0), 4)], ((4, 0), 2))

# 12 region area: exact polygon + brute-force grid count
poly = sp.Polygon((3, 1), (0, 4), (-4, 0), (-1, -3))
assert abs(poly.area) == 24
N = 400
cnt = 0
for i in range(-N, N):
    for j in range(-N, N):
        px, py = (i + 0.5) * 4 / N, (j + 0.5) * 4 / N
        if abs(px) + abs(py) <= 4 and py >= px - 2:
            cnt += 1
approx = cnt * (4 / N)**2
assert abs(approx - 24) < 0.1, approx
pick('coord-12', [16, 20, 24, 28, 48], 24)

# 13 kite area
C13 = sp.Point(2, -1)
assert sp.expand((x - 2)**2 + (y + 1)**2 - 9 - (x**2 + y**2 - 4*x + 2*y - 4)) == 0
circ13 = sp.Circle(C13, 3)
tl = circ13.tangent_lines(sp.Point(7, 1))
T = [circ13.intersection(l)[0] for l in tl]
kite = sp.Polygon(sp.Point(7, 1), T[0], C13, T[1])
pick('coord-13', [3*sqrt(5), 2*sqrt(29), 6*sqrt(5), 3*sqrt(29), 12*sqrt(5)], sp.nsimplify(sp.simplify(abs(kite.area))))

# 14 no intersection
d14 = sp.expand(sp.discriminant(sp.expand(x**2 + (m*x + 2)**2 - 6*x), x))
assert d14 == 20 - 48*m
region = sp.solveset(d14 < 0, m, sp.S.Reals)
assert region == sp.Interval.open(R(5, 12), sp.oo)
cands = [sp.Interval.open(R(5, 12), sp.oo), sp.Interval.open(0, R(5, 12)), sp.Interval.open(-sp.oo, R(5, 12)),
         sp.Interval.open(R(12, 5), sp.oo), sp.Union(sp.Interval.open(-sp.oo, -R(5, 12)), sp.Interval.open(R(5, 12), sp.oo))]
assert [cc == region for cc in cands].index(True) == Q['coord-14']['answer'] and sum(cc == region for cc in cands) == 1

# 15
random.seed(0)
I15 = II15 = True
for _ in range(3000):
    p_, q_ = R(random.randint(-100, 700), 100), R(random.randint(-400, 400), 100)
    if q_ == 0:
        continue
    dot = (-p_) * (6 - p_) + q_**2
    if p_**2 + q_**2 == 6*p_ and dot != 0:
        I15 = False
    if dot < 0 and not ((p_ - 3)**2 + q_**2 < 9):
        II15 = False
# explicit on-circle points for I
for th in [R(1, 3), R(1, 2), 2]:
    pp = (3 + 3*(1 - th**2)/(1 + th**2), 3*2*th/(1 + th**2))
    assert pp[0]**2 + pp[1]**2 == 6*pp[0] and (-pp[0])*(6 - pp[0]) + pp[1]**2 == 0
III15 = False  # q = -4 gives area 12
assert abs(sp.Triangle(sp.Point(0, 0), sp.Point(6, 0), sp.Point(1, -4)).area) == 12
assert ROM[(I15, II15, III15)] == Q['coord-15']['answer']

# 16 reflection
img = sp.Point(1, 2).reflect(sp.Line(sp.Point(0, -5), sp.Point(1, -3)))
pick_obj('coord-16', [(-3, 4), (3, 1), (4, -1), (5, 0), (9, -2)], (img.x, img.y))

# 17 circles touching both axes through (2,1)
r = sp.Symbol('r', positive=True)
rs = sp.solve((2 - r)**2 + (1 - r)**2 - r**2, r)
assert sorted(rs) == [1, 5]
c1, c2 = sp.Circle(sp.Point(1, 1), 1), sp.Circle(sp.Point(5, 5), 5)
ip = c1.intersection(c2)
assert set((p_.x, p_.y) for p_ in ip) == {(2, 1), (1, 2)}
# other quadrants: a circle touching both axes through (2,1) must be in the first quadrant
pick('coord-17', [1, sqrt(2), 2, 2*sqrt(2), 4*sqrt(2)], ip[0].distance(ip[1]))

# 18 necessary / sufficient
meets = lambda mm, cc: cc**2 < 1 + mm**2
vals = [R(n, 10) for n in range(-40, 41)]
I18 = all(meets(mm, cc) for mm in vals for cc in vals if abs(cc) < 1)
II18 = all(abs(cc) < 1 for mm in vals for cc in vals if meets(mm, cc))
III18 = all(abs(cc) < 1 + abs(mm) for mm in vals for cc in vals if meets(mm, cc))
assert (I18, II18, III18) == (True, False, True)
# confirm the stated 'iff' via discriminant
d18 = sp.discriminant(sp.expand(x**2 + (m*x + c)**2 - 1), x)
assert sp.expand(d18 - 4*(1 + m**2 - c**2)) == 0
assert not meets(1, R(19, 10)) and abs(R(19, 10)) < 2
assert ROM[(I18, II18, III18)] == Q['coord-18']['answer']

print('ALL OK')
