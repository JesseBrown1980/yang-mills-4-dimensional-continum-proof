#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. (Z/3)x(Z/2), Q8, link reflection, the 512 point functions of the slice t=0, for the weights that decide the clause a_negative_c_2dim_fails_on_odd_L_at_T=2_here.
The kernel is read at class representatives from the plaquette words and compared with a walk over all V on a seeded sample of (b, a). Then a scan of pointwise non-negative w for G_EE < 0 at L = 1, 3, 5.
Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import FiniteGroup, q8_table
G = FiniteGroup("Q8")
CHI = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
ELEMENTS = range(8)
ONE = next(g for g in ELEMENTS if all(MUL[g][h] == h for h in ELEMENTS))
REP = [next(g for g in ELEMENTS if CLS[g] == k) for k in range(5)]
DIM = [1, 1, 1, 1, 2]


def word(*letters):
    h = ONE
    for x in letters:
        h = MUL[h][x]
    return h


def plane(w, lower, upper):
    # sum over V(0),V(1),V(2) of prod_x w(lower_x V(x+1) upper_x^-1 V(x)^-1)
    total = 0
    for v in itertools.product(ELEMENTS, repeat=3):
        term = 1
        for x in range(3):
            term *= w[CLS[word(lower[x], v[(x + 1) % 3], INV[upper[x]], INV[v[x]])]]
            if term == 0:
                break
        total += term
    return total


def holonomy_class(a):
    return CLS[word(a[0], a[1], a[2])]


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
        rk = m[k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(i, n):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = v
                m[j][i] = v
        prev = top
    return pos, neg, n


configs = list(itertools.product(ELEMENTS, repeat=3))
for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1), (1, -2, -2, -2, -1), (-8, -3, -3, -3, -1)):
    w = [sum(c[r] * CHI[r][k] for r in range(5)) for k in range(5)]
    rep = {}
    for x in range(5):
        for y in range(5):
            a, b = (REP[x], ONE, ONE), (REP[y], ONE, ONE)
            rep[(x, y)] = plane(w, a, b)
    state = 20261103
    checked, agree = 0, 0
    for _ in range(300):
        state = (state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        s = state >> 20
        b = tuple((s >> (3 * i)) & 7 for i in range(3))
        a = tuple((s >> (3 * i + 9)) & 7 for i in range(3))
        checked += 1
        agree += 1 if plane(w, a, b) == rep[(holonomy_class(a), holonomy_class(b))] else 0
    rows = [[rep[(holonomy_class(b), holonomy_class(a))] * rep[(holonomy_class(a), holonomy_class(b))] for a in configs] for b in configs]
    p, n, rank = bareiss_inertia(rows)
    print("RING3|lattice=(Z/3)x(Z/2)|group=Q8|c=%s|w=%s|family=all_512_point_functions_of_the_slice|pos=%d|neg=%d|rank=%d|kernel_sample=%d|agree=%d|json=0" % (",".join(map(str, c)), ",".join(map(str, w)), p, n, rank, checked, agree))

# The scan: w >= 0 pointwise with c_2dim < 0, L odd. G_EE = 2 t_E (t_0 + t_1 + t_2 + t_3), with t_a = c_a^L and t_E = (c_E/2)^L. c is measured in units of 1/8 so everything stays an integer: t_a*8^L, t_E*16^L.
tested, red, lowest_sum = 0, 0, None
for w in itertools.product(range(0, 7), repeat=5):
    size = [1, 1, 2, 2, 2]
    c8 = [sum(size[k] * w[k] * CHI[r][k] for k in range(5)) for r in range(5)]
    if c8[4] >= 0:
        continue
    for L in (1, 3, 5):
        tested += 1
        s = sum(c8[a] ** L for a in range(4))
        if s > 0:
            red += 1
        lowest_sum = s if lowest_sum is None or s < lowest_sum else lowest_sum
print("SCAN|w_in_0..6^5_with_c_2dim<0|L=1,3,5|cases=%d|G_EE_negative=%d|lowest_(t_0+t_1+t_2+t_3)_times_8^L=%d|json=0" % (tested, red, lowest_sum))
tested, psd_cases = 0, 0
for w in itertools.product(range(-6, 7), repeat=5):
    size = [1, 1, 2, 2, 2]
    c8 = [sum(size[k] * w[k] * CHI[r][k] for k in range(5)) for r in range(5)]
    if c8[4] >= 0 or c8[0] <= 0:
        continue
    tested += 1
    if sum(c8[a] ** 3 for a in range(4)) < 0:
        psd_cases += 1
print("SCAN_SIGNED|w_in_-6..6^5_with_c_0>0_and_c_2dim<0|L=3|cases=%d|G_EE_positive=%d|json=0" % (tested, psd_cases))
