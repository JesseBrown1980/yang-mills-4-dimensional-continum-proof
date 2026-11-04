#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. The second seat's CONJECTURE, odd L at T>=4: is a negative coefficient red for every weight? (Z/1)x(Z/4), Q8.
The form on the open half is D (S tensor S) D, so its inertia is that of S tensor S on the pairs of classes that the plaquette weight reaches.
Standard library, integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import FiniteGroup, q8_table, rat, rtext
G = FiniteGroup("Q8")
CHI = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
DIM = [1, 1, 1, 1, 2]
SIZE = [1, 1, 2, 2, 2]
REP = [next(g for g in range(8) if CLS[g] == k) for k in range(5)]
LOW, HIGH = int(sys.argv[1]), int(sys.argv[2])

def bareiss_inertia(rows):
    m = [list(r) for r in rows]
    n = len(m)
    prev, pos, neg = 1, 0, 0
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i]), None)
        if piv is None:
            pair = next(((i, j) for i in range(k, n) for j in range(i + 1, n) if m[i][j]), None)
            if pair is None:
                return pos, neg, k
            i, j = pair
            for r in range(k, n):
                m[i][r] += m[j][r]
            for r in range(k, n):
                m[r][i] += m[r][j]
            piv = i
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        if (top > 0) == (prev > 0):
            pos += 1
        else:
            neg += 1
        for i in range(k + 1, n):
            mik = m[i][k]
            ri, rk = m[i], m[k]
            for j in range(i, n):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = v
                m[j][i] = v
        prev = top
    return pos, neg, n

def plaquette(w, a, b, v):
    return w[CLS[MUL[MUL[MUL[a][v]][INV[b]]][INV[v]]]]

def form_rows(w):
    st = {}
    for x in range(5):
        for y in range(5):
            st[(x, y)] = sum(plaquette(w, REP[x], REP[y], v) for v in range(8))
    supp = [(x, y) for x in range(5) for y in range(5) if any(plaquette(w, REP[x], REP[y], v) for v in range(8))]
    # h(x, y) is free on supp. Scale: each class pair carries one coordinate; S is the class-level strip.
    return supp, [[st[(x2, x)] * st[(y2, y)] for (x, y) in supp] for (x2, y2) in supp]

def coefficients_times_8(w):
    return [sum(SIZE[k] * w[k] * CHI[r][k] for k in range(5)) for r in range(5)]

def literal_512(w):
    n = 8
    strip = [[sum(plaquette(w, a, b, v) for v in range(n)) for b in range(n)] for a in range(n)]
    tr = list(itertools.product(range(n), repeat=3))
    return [[plaquette(w, a, b, v) * strip[b][b2] * plaquette(w, b2, a2, INV[v2]) * strip[a2][a] for (a, b, v) in tr] for (a2, b2, v2) in tr]

cats = {}
examples = {}
total = 0
for w in itertools.product(range(LOW, HIGH + 1), repeat=5):
    if not any(w):
        continue
    total += 1
    c8 = coefficients_times_8(w)
    supp, rows = form_rows(w)
    pos, neg, rank = bareiss_inertia(rows)
    nowhere_zero = all(w)
    has_negative = any(x < 0 for x in c8)
    if c8[0] > 0:
        s0 = "c0_pos"
    elif c8[0] < 0:
        s0 = "c0_neg"
    else:
        s0 = "c0_zero"
    opposite = any(x * c8[0] < 0 for x in c8[1:])
    key = (s0, "nowhere_zero" if nowhere_zero else "has_a_zero", "opposite_sign_coefficient" if opposite else "no_opposite_coefficient", "PSD" if neg == 0 else "RED")
    cats[key] = cats.get(key, 0) + 1
    examples.setdefault(key, (w, c8, pos, neg, len(supp)))
print("GRID|lattice=(Z/1)x(Z/4)|group=Q8|w_range=%d..%d|weights=%d|json=0" % (LOW, HIGH, total))
for key in sorted(cats):
    w, c8, pos, neg, supp = examples[key]
    print("GRID_CAT|%s|count=%d|example_w=%s|c_times_8=%s|pos=%d|neg=%d|class_pairs_in_support=%d|json=0" % ("|".join(key), cats[key], ",".join(map(str, w)), ",".join(map(str, c8)), pos, neg, supp))
