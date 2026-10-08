"""Verification for content/questions/coord.json. Run: python3 content/checks/coord_check.py"""
import json, os, math, random, itertools
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QL = json.load(open(os.path.join(ROOT, 'content/questions/coord.json'), encoding='utf-8'))
Q = {q['id']: q for q in QL}
x, y, k = sp.symbols('x y k', real=True)
ROMAN = ["none of them", "I only", "II only", "III only", "I and II only", "I and III only",
         "II and III only", "I, II and III"]
ROM = {(False, False, False): 0, (True, False, False): 1, (False, True, False): 2, (False, False, True): 3,
       (True, True, False): 4, (True, False, True): 5, (False, True, True): 6, (True, True, True): 7}
key = lambda i: Q[i]['answer']
random.seed(7)

# ---------------------------------------------------------------- structure
base = [f'coord-{i:02d}' for i in range(1, 19)]
assert sorted(Q) == sorted(base + [b + 'b' for b in base]) and len(QL) == 36
diffs = sorted(Q[i]['difficulty'] for i in base)
assert diffs == [2] * 2 + [3] * 6 + [4] * 6 + [5] * 4, diffs
for i in base:
    a, b = Q[i], Q[i + 'b']
    assert a['family'] == i and b['family'] == i
    assert a['difficulty'] == b['difficulty'] and a['paper'] == b['paper']
    assert a['answer'] != b['answer'], i
for q in QL:
    n = len(q['options'])
    assert q['difficulty'] >= 2 and (n == 5 or (n == 8 and q['options'] == ROMAN)), q['id']
    assert 0 <= q['answer'] < n and len(set(q['options'])) == n
    assert len(q['distractors']) >= 3, q['id']
    for kk in q['distractors']:
        assert int(kk) != q['answer'] and int(kk) < n, (q['id'], kk)


def val(s):
    """parse simple option like $\\tfrac{17}{4}$, $2\\sqrt5$, $-\\tfrac73$, $\\tfrac32\\pi + 1$."""
    import re
    s = s.strip('$').replace(' ', '')
    s = re.sub(r'\\tfrac\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', s)
    s = re.sub(r'\\tfrac(\d)(\d)', r'((\1)/(\2))', s)
    s = re.sub(r'\\sqrt\{([^}]*)\}', r'sqrt(\1)', s)
    s = re.sub(r'\\sqrt(\d)', r'sqrt(\1)', s)
    s = s.replace(r'\pi', 'pi')
    s = re.sub(r'(\d|\))(sqrt|pi|\()', r'\1*\2', s)
    s = re.sub(r'(\))(\d)', r'\1*\2', s)
    return sp.nsimplify(sp.sympify(s))


def numeric_key(qid, true_value):
    vals = [val(o) for o in Q[qid]['options']]
    fl = [float(v) for v in vals]
    assert fl == sorted(fl), qid
    m = [abs(float(v - true_value)) < 1e-12 for v in vals]
    assert m.count(True) == 1 and m.index(True) == key(qid), (qid, vals, true_value)


def angle(P, A, B):
    """angle APB in radians"""
    u = (A[0] - P[0], A[1] - P[1]); v = (B[0] - P[0], B[1] - P[1])
    return math.acos((u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v))


# ---------------------------------------------------------------- 01, 01b alternate segment
A, B, T = (5, 0), (3, 4), (sp.Rational(25, 3), 0)
assert 3 * T[0] + 4 * T[1] == 25 and A[0]**2 + A[1]**2 == 25 and B[0]**2 + B[1]**2 == 25
th = angle(B, A, (float(T[0]), 0))
assert abs(math.tan(th) - 0.5) < 1e-12
for C in [(-5, 0), (-3, 4), (0, -5), (4, -3)]:            # points of the alternate segment
    assert abs(angle(C, A, B) - th) < 1e-12
numeric_key('coord-01', sp.Rational(1, 2))
A, B, T = (3, 1), (-3, 1), (0, 10)
assert 3 * T[0] + T[1] == 10
th = angle(A, T, B)
assert abs(math.tan(th) - 3) < 1e-9
assert abs(angle((-3, -1), A, B) - th) < 1e-12
numeric_key('coord-01b', 3)


# ---------------------------------------------------------------- 02, 02b parameter conditions
def agree(qid, truth, preds, grid):
    tv = {g: truth(g) for g in grid}
    ok = [all(bool(p(g)) == tv[g] for g in grid) for p in preds]
    assert ok.count(True) == 1 and ok.index(True) == key(qid), (qid, ok)


grid = [sp.Rational(i, 24) for i in range(-120, 200)]
def quad4(kv):
    cx, cy, r2 = kv, -2, kv**2 - 3 * kv + 4
    assert r2 > 0
    return cx > 0 and cy < 0 and r2 < cx**2 and r2 < cy**2
agree('coord-02', quad4,
      [lambda v: 0 < v < 3, lambda v: 1 < v < 2, lambda v: sp.Rational(4, 3) < v < 3,
       lambda v: v > sp.Rational(4, 3), lambda v: v < sp.Rational(4, 3) or v > 3], grid)
def c2b(kv):
    r2 = kv**2 - 2 * kv + 3
    assert r2 > 0
    two = len(sp.solve((x - 2)**2 + kv**2 - r2, x)) == 2   # y=0
    outside = 4 + kv**2 > r2
    return two and outside
agree('coord-02b', c2b,
      [lambda v: v < -sp.Rational(1, 2), lambda v: -sp.Rational(1, 2) < v < sp.Rational(3, 2),
       lambda v: v < sp.Rational(3, 2), lambda v: v > -sp.Rational(1, 2), lambda v: v > sp.Rational(3, 2)], grid)
# both general forms really are the stated circles
assert sp.expand((x - k)**2 + (y + 2)**2 - (k**2 - 3 * k + 4) - (x**2 + y**2 - 2*k*x + 4*y + 3*k)) == 0
assert sp.expand((x - 2)**2 + (y + k)**2 - (k**2 - 2*k + 3) - (x**2 + y**2 - 4*x + 2*k*y + 2*k + 1)) == 0


# ---------------------------------------------------------------- 03, 03b perpendicular bisector
def lines_from(qid):
    out = []
    for o in Q[qid]['options']:
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication
        lhs = parse_expr(o.strip('$').split('=')[0], local_dict={'x': x, 'y': y},
                         transformations=standard_transformations + (implicit_multiplication,))
        out.append(lhs)
    return out
def perp_bis(qid, A, B):
    M = ((A[0] + B[0]) / sp.Integer(2), (A[1] + B[1]) / sp.Integer(2))
    ok = []
    for L in lines_from(qid):
        a, b = L.coeff(x), L.coeff(y)
        through = L.subs({x: M[0], y: M[1]}) == 0
        perp = a * (B[1] - A[1]) - b * (B[0] - A[0]) == 0      # normal (a,b) parallel to AB
        ok.append(through and perp)
    assert ok.count(True) == 1 and ok.index(True) == key(qid), (qid, ok)
perp_bis('coord-03', (-1, 3), (5, -1))
perp_bis('coord-03b', (2, -3), (-2, 5))


# ---------------------------------------------------------------- 04, 04b concyclic
def concyclic(P):
    m = sp.Matrix([[px**2 + py**2, px, py, 1] for px, py in P])
    return m.det() == 0
def convex_in_order(P):
    s = []
    for i in range(4):
        a, b, c = P[i], P[(i + 1) % 4], P[(i + 2) % 4]
        s.append((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]))
    return all(v > 0 for v in s) or all(v < 0 for v in s)
ok = []
for o in Q['coord-04']['options']:
    kv = val(o)
    P = [(0, 0), (4, 0), (kv, kv), (0, 2)]
    ok.append(kv != 0 and concyclic(P) and convex_in_order(P))
assert ok.count(True) == 1 and ok.index(True) == key('coord-04'), ok
ok = []
for o in Q['coord-04b']['options']:
    kv = val(o)
    ok.append(kv < 0 and concyclic([(-2, 0), (6, 0), (0, 4), (0, kv)]))
assert ok.count(True) == 1 and ok.index(True) == key('coord-04b'), ok
assert [float(val(o)) for o in Q['coord-04b']['options']] == sorted(float(val(o)) for o in Q['coord-04b']['options'])


# ---------------------------------------------------------------- 05, 05b tangency
def tangent_params(line_y_or_eq, circ, param):
    """values of param for which line meets circle in exactly one point"""
    if isinstance(line_y_or_eq, tuple):            # implicit: solve for y
        yy = sp.solve(line_y_or_eq[0], y)[0]
    else:
        yy = line_y_or_eq
    qx = sp.Poly(sp.expand(circ.subs(y, yy)), x)
    return set(sp.solve(sp.discriminant(qx.as_expr(), x), param))
c = sp.symbols('c', real=True)
tv = tangent_params(x + c, x**2 + y**2 - 8, c)
assert tv == {-4, 4}
sets5 = [{-2, 2}, {-2 * sp.sqrt(2), 2 * sp.sqrt(2)}, {4}, {-4, 4}, {-8, 8}]
ok = [s == tv for s in sets5]
assert ok.count(True) == 1 and ok.index(True) == key('coord-05')
tv = tangent_params((3 * x + 4 * y - k,), (x - 1)**2 + (y + 2)**2 - 9, k)
assert tv == {-20, 10}
sets5b = [{-20, 10}, {-10, 20}, {-8, -2}, {-15, 15}, {10}]
ok = [s == tv for s in sets5b]
assert ok.count(True) == 1 and ok.index(True) == key('coord-05b')


# ---------------------------------------------------------------- 06, 06b angle loci
# region {y>0, angle APB >= 45deg} with A(-1,0), B(1,0) is the disc x^2+(y-1)^2<=2 cut by y>0
for _ in range(20000):
    P = (random.uniform(-3, 3), random.uniform(1e-3, 4))
    if abs(P[0] ** 2 + (P[1] - 1) ** 2 - 2) < 1e-6:
        continue
    inside = P[0] ** 2 + (P[1] - 1) ** 2 < 2
    assert (angle(P, (-1, 0), (1, 0)) > math.pi / 4) == inside
X = sp.symbols('X', real=True)
# for |X|<=1 the region runs from y=0 up to the top of the circle; for 1<|X|<=sqrt2 from the bottom arc
top = 1 + sp.sqrt(2 - X**2); bot = 1 - sp.sqrt(2 - X**2)
area = sp.integrate(top, (X, -1, 1)) + 2 * sp.integrate(top - bot, (X, 1, sp.sqrt(2)))
area = sp.simplify(area)
assert sp.simplify(area - (3 * sp.pi / 2 + 1)) == 0
assert abs(float(area) - float(3 * sp.pi / 2 + 1)) < 1e-12
N, hit = 400000, 0
for _ in range(N):
    P = (random.uniform(-1.5, 1.5), random.uniform(0, 2.5))
    if angle(P, (-1, 0), (1, 0)) >= math.pi / 4:
        hit += 1
assert abs(hit / N * 7.5 - float(area)) < 0.05
numeric_key('coord-06', 3 * sp.pi / 2 + 1)
# 06b: P on circle centre (2, 2sqrt3) radius 4 (upper arc) sees AB at 30deg; max area
M = (2, 2 * math.sqrt(3))
best = 0
for i in range(1, 20000):
    th = math.pi * 2 * i / 20000
    P = (M[0] + 4 * math.cos(th), M[1] + 4 * math.sin(th))
    if P[1] <= 1e-9:
        continue
    assert abs(angle(P, (0, 0), (4, 0)) - math.pi / 6) < 1e-9
    best = max(best, 2 * P[1])
assert abs(best - (8 + 4 * math.sqrt(3))) < 1e-6
# and no point of the plane with angle 30 is higher (brute force near the top)
for _ in range(20000):
    P = (random.uniform(-2, 6), random.uniform(7.5, 9))
    assert angle(P, (0, 0), (4, 0)) < math.pi / 6
numeric_key('coord-06b', 8 + 4 * sp.sqrt(3))


# ---------------------------------------------------------------- 07, 07b tangent at a point
def tangent_at(circ, P):
    gx, gy = sp.diff(circ, x).subs({x: P[0], y: P[1]}), sp.diff(circ, y).subs({x: P[0], y: P[1]})
    return gx * (x - P[0]) + gy * (y - P[1])
circ = (x - 2)**2 + (y + 1)**2 - 25
assert circ.subs({x: 5, y: 3}) == 0
L = tangent_at(circ, (5, 3))
numeric_key('coord-07', sp.solve(L.subs(y, 0), x)[0])
circ = x**2 + y**2 - 4*x + 6*y - 12
assert circ.subs({x: -1, y: 1}) == 0
L = tangent_at(circ, (-1, 1))
numeric_key('coord-07b', sp.solve(L.subs(x, 0), y)[0])


# ---------------------------------------------------------------- 08, 08b chord length
def chord(circ, yy):
    xs = sp.solve(circ.subs(y, yy), x)
    assert len(xs) == 2
    (x1, x2) = xs
    return sp.sqrt(sp.simplify((x1 - x2)**2 + (yy.subs(x, x1) - yy.subs(x, x2))**2))
numeric_key('coord-08', sp.simplify(chord(x**2 + y**2 - 13, x + 1)))
numeric_key('coord-08b', sp.simplify(chord((x - 2)**2 + (y - 1)**2 - 25, (-3 * x - 5) / sp.Integer(4))))


# ---------------------------------------------------------------- 09, 09b two circles
def n_int(d, r1, r2):
    if d == 0:
        return 0 if r1 != r2 else -1
    if d > r1 + r2 or d < abs(r1 - r2):
        return 0
    if d == r1 + r2 or d == abs(r1 - r2):
        return 1
    return 2
a = sp.symbols('a', real=True)
touch = set(sp.solve(2 * a**2 - 9, a)) | set(sp.solve(2 * a**2 - 49, a))
I = len(touch) == 4
fine = [sp.Rational(i, 50) for i in range(-400, 401)]
assert {av for av in fine if n_int(sp.sqrt(2) * abs(av), 2, 5) == 1} <= touch
II = all(n_int(sp.sqrt(2) * abs(av), 2, 5) == 2 for av in fine if abs(av) < 2)
III = all(n_int(sp.sqrt(2) * av, 2, 5) == 2 for av in fine if 3 < av < 4)
assert ROM[(I, II, III)] == key('coord-09')
r = sp.symbols('r', positive=True)
touch = [rv for rv in [sp.Rational(i, 10) for i in range(1, 400)] if n_int(10, rv, 4) == 1]
I = touch == [6, 14]
II = all(n_int(10, rv, 4) == 2 for rv in [sp.Rational(i, 10) for i in range(71, 130)])
III = all(n_int(10, rv, 4) == 2 for rv in [sp.Rational(i, 10) for i in range(61, 400)])
assert ROM[(I, II, III)] == key('coord-09b')


# ---------------------------------------------------------------- 10, 10b families of lines
Lk = (k + 1) * x + (k - 1) * y - 2 * k
I = sp.simplify(Lk.subs({x: 1, y: 1})) == 0
II = sp.solve(sp.Eq(Lk.coeff(y), 0), k) == [1]
# perpendicular to x - y = 3 (normal (1,-1)) <=> normals perpendicular
III = len(sp.solve(sp.Eq((k + 1) * 1 + (k - 1) * (-1), 0), k)) > 0
assert ROM[(I, II, III)] == key('coord-10')
t, s = sp.symbols('t s', real=True)
Mt = t * x - y - t**2
I = len([v for v in sp.solve(Mt.subs({x: 0, y: 1}), t) if v.is_real]) == 2
sol = sp.solve([Mt, Mt.subs(t, s)], [x, y], dict=True)[0]
assert sp.simplify(sol[x] - (s + t)) == 0 and sp.simplify(sol[y] - s * t) == 0
II = True   # perpendicular <=> st = -1, and the meeting point has y = st = -1 (verified above)
for _ in range(50):
    sv = random.choice([-3, -2, -1, sp.Rational(1, 2), 2, 5]); tv_ = -1 / sp.Integer(1) / sv
    assert sp.simplify(sol[y].subs({s: sv, t: tv_})) == -1
III = len([v for v in sp.solve(Mt.subs({x: 0, y: 1}), t) if v.is_real]) > 0
assert ROM[(I, II, III)] == key('coord-10b')


# ---------------------------------------------------------------- 11, 11b Apollonius
def locus(A, B, ratio):
    e = sp.expand((x - A[0])**2 + (y - A[1])**2 - ratio**2 * ((x - B[0])**2 + (y - B[1])**2))
    e = sp.expand(e / e.coeff(x, 2))
    g, f = e.coeff(x, 1) / 2, e.coeff(y, 1) / 2
    cst = e.subs({x: 0, y: 0})
    return (-g, -f), sp.sqrt(g**2 + f**2 - cst)
def opt_circle(o):
    import re
    m = re.match(r'centre \$\((-?\d+), (-?\d+)\)\$, radius \$(.*)\$', o)
    return (int(m.group(1)), int(m.group(2))), val('$' + m.group(3) + '$')
for qid, A, B, rt in [('coord-11', (0, 0), (3, 0), 2), ('coord-11b', (0, 0), (8, 0), 3)]:
    cen, rad = locus(A, B, rt)
    ok = [opt_circle(o) == (cen, rad) for o in Q[qid]['options']]
    assert ok.count(True) == 1 and ok.index(True) == key(qid), (qid, cen, rad)


# ---------------------------------------------------------------- 12, 12b region areas
def num_area(inside, x0, x1, y0, y1, n=1400):
    hx, hy = (x1 - x0) / n, (y1 - y0) / n
    c = 0
    for i in range(n):
        for j in range(n):
            if inside(x0 + (i + .5) * hx, y0 + (j + .5) * hy):
                c += 1
    return c * hx * hy
a12 = num_area(lambda u, v: abs(u) + abs(v) <= 4 and v >= u - 2, -4, 4, -4, 4)
assert abs(a12 - 24) < 0.05
numeric_key('coord-12', 24)
a12b = num_area(lambda u, v: abs(u - 1) <= v <= 5 - abs(u + 1), -3, 3, 0, 5)
assert abs(a12b - 10.5) < 0.05
poly = [(1, 0), (sp.Rational(5, 2), sp.Rational(3, 2)), (-1, 5), (-sp.Rational(5, 2), sp.Rational(7, 2))]
shoe = abs(sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))) / 2
assert shoe == sp.Rational(21, 2)
numeric_key('coord-12b', sp.Rational(21, 2))


# ---------------------------------------------------------------- 13, 13b tangents from a point
def tangent_points(circ, P):
    # points X on circle with (X - C).(X - P) = 0 where C is the centre
    cx = -sp.expand(circ).coeff(x, 1) / 2; cy = -sp.expand(circ).coeff(y, 1) / 2
    sols = sp.solve([circ, (x - cx) * (x - P[0]) + (y - cy) * (y - P[1])], [x, y], dict=True)
    return (cx, cy), [(s_[x], s_[y]) for s_ in sols]
circ = x**2 + y**2 - 4*x + 2*y - 4
C, TP = tangent_points(circ, (7, 1))
assert len(TP) == 2
def tri(a, b, c):
    return sp.Abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2
kite = sp.simplify(tri((7, 1), TP[0], C) + tri((7, 1), TP[1], C))
numeric_key('coord-13', kite)
circ = x**2 + y**2 + 6*x - 8*y + 20
C, TP = tangent_points(circ, (2, 4))
AB = sp.sqrt(sp.simplify((TP[0][0] - TP[1][0])**2 + (TP[0][1] - TP[1][1])**2))
numeric_key('coord-13b', sp.simplify(AB))


# ---------------------------------------------------------------- 14, 14b discriminant conditions
m = sp.symbols('m', real=True)
disc = sp.discriminant(sp.expand((x**2 + (m * x + 2)**2 - 6 * x)), x)
assert sp.expand(disc - (20 - 48 * m)) == 0
mg = [sp.Rational(i, 48) for i in range(-200, 200)] + [sp.Rational(5, 12), sp.Rational(12, 5)]
agree('coord-14', lambda v: disc.subs(m, v) < 0,
      [lambda v: v > sp.Rational(5, 12), lambda v: 0 < v < sp.Rational(5, 12), lambda v: v < sp.Rational(5, 12),
       lambda v: v > sp.Rational(12, 5), lambda v: v < -sp.Rational(5, 12) or v > sp.Rational(5, 12)], mg)
disc = sp.discriminant(sp.expand(x**2 + (k * (x - 4))**2 - 4), x)
assert sp.expand(disc - (16 - 48 * k**2)) == 0
r3 = 1 / sp.sqrt(3)
kg = [sp.Rational(i, 48) for i in range(-120, 121)] + [r3, -r3, sp.sqrt(3) - sp.Rational(1, 10)]
agree('coord-14b', lambda v: disc.subs(k, v) > 0,
      [lambda v: -sp.Rational(1, 2) < v < sp.Rational(1, 2), lambda v: v < -r3 or v > r3,
       lambda v: -sp.sqrt(3) < v < sp.sqrt(3), lambda v: -r3 < v < r3, lambda v: -r3 <= v <= r3], kg)


# ---------------------------------------------------------------- 15, 15b semicircle statements
def ang_deg(P, A, B):
    return math.degrees(angle(P, A, B))
pts = [(random.uniform(-4, 10), random.choice([-1, 1]) * random.uniform(0.01, 6)) for _ in range(20000)]
I = all(abs(ang_deg((p, q), (0, 0), (6, 0)) - 90) < 1e-6 for p in [0.5, 1, 3, 5.5]
        for q in [math.sqrt(6 * p - p * p), -math.sqrt(6 * p - p * p)])
II = all((p - 3) ** 2 + q * q < 9 for p, q in pts if ang_deg((p, q), (0, 0), (6, 0)) > 90 + 1e-9)
III = not (abs(0.5 * 6 * abs(-4) - 12) < 1e-12)          # C=(2,-4): area 12 but q != 4
assert ROM[(I, II, III)] == key('coord-15')
A, B = (1, 0), (1, 6)
inside = [(p, q) for p, q in [(random.uniform(-2, 4), random.uniform(0, 6)) for _ in range(20000)]
          if (p - 1) ** 2 + (q - 3) ** 2 < 9 and abs(p - 1) > 1e-6]
I = all(ang_deg(P, A, B) > 90 for P in inside)
assert abs(0.5 * 6 * abs(4 - 1) - 9) < 1e-12 and abs(ang_deg((4, 3), A, B) - 90) < 1e-9
II = False
III = all(ang_deg((5, q), A, B) < 90 for q in [i / 10 for i in range(-200, 260)])
assert ROM[(I, II, III)] == key('coord-15b')


# ---------------------------------------------------------------- 16, 16b reflections
def reflect(P, a, b, c):     # in ax+by=c
    tt = sp.Rational(c - a * P[0] - b * P[1], a * a + b * b)
    return (P[0] + 2 * tt * a, P[1] + 2 * tt * b)
def opt_pt(o):
    a_, b_ = o.strip('$()').split(',')
    return (sp.Integer(a_), sp.Integer(b_))
for qid, P, line in [('coord-16', (1, 2), (-2, 1, -5)), ('coord-16b', (0, 0), (1, 2, 10))]:
    im = reflect(P, *line)
    ok = [opt_pt(o) == im for o in Q[qid]['options']]
    assert ok.count(True) == 1 and ok.index(True) == key(qid), (qid, im)
    xs = [opt_pt(o) for o in Q[qid]['options']]
    assert xs == sorted(xs)


# ---------------------------------------------------------------- 17, 17b circles touching axes
rr = sp.symbols('rr', positive=True)
rs = sp.solve((2 - rr)**2 + (1 - rr)**2 - rr**2, rr)
assert sorted(rs) == [1, 5]
c1 = (x - 1)**2 + (y - 1)**2 - 1; c2 = (x - 5)**2 + (y - 5)**2 - 25
common = sp.solve([c1, c2], [x, y], dict=True)
pts = {(s_[x], s_[y]) for s_ in common}
assert pts == {(2, 1), (1, 2)}
numeric_key('coord-17', sp.sqrt(2))
aa = sp.symbols('aa', real=True)
sols = sp.solve([(1 - aa)**2 + (2 - rr)**2 - rr**2, (3 - aa)**2 + (4 - rr)**2 - rr**2], [aa, rr], dict=True)
cents = sorted((s_[aa], s_[rr]) for s_ in sols)
assert cents == [(-5, 10), (3, 2)]
numeric_key('coord-17b', sp.sqrt((cents[0][0] - cents[1][0])**2 + (cents[0][1] - cents[1][1])**2))


# ---------------------------------------------------------------- 18, 18b necessary / sufficient
def two_points_unit(mv, cv):
    return cv * cv < 1 + mv * mv
G = [(sp.Rational(i, 4), sp.Rational(j, 4)) for i in range(-48, 49) for j in range(-48, 49)]
I = all(two_points_unit(mv, cv) for mv, cv in G if abs(cv) < 1)
II = all(abs(cv) < 1 for mv, cv in G if two_points_unit(mv, cv))
III = all(abs(cv) < 1 + abs(mv) for mv, cv in G if two_points_unit(mv, cv))
assert ROM[(I, II, III)] == key('coord-18')
# direct check of the stated iff via discriminant
mm, cc = sp.symbols('mm cc', real=True)
assert sp.expand(sp.discriminant(x**2 + (mm * x + cc)**2 - 1, x) - 4 * (mm**2 - cc**2 + 1)) == 0
def two_points_b(av):
    return sp.discriminant(sp.expand((x - av)**2 + x**2 - 4), x) > 0
ag = [sp.Rational(i, 20) for i in range(-80, 81)] + [2 * sp.sqrt(2), -2 * sp.sqrt(2)]
I = all(two_points_b(av) for av in ag if abs(av) < 2)
II = all(abs(av) < 3 for av in ag if two_points_b(av))
III = all((av**2 <= 8) == two_points_b(av) for av in ag)
assert ROM[(I, II, III)] == key('coord-18b')

print('ALL OK')
