#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. Theorem 4 with complex characters at T = 4, a case the rows leave at T = 2. (Z/1)x(Z/4), 2T, all 576 point functions of (U(0), U(1)). Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import FiniteGroup
T = FiniteGroup("2T")
n = T.n
mul, inv, cls = T.mul, T.inv, T.cls


def bareiss_inertia(rows):
    m = [list(r) for r in rows]
    size = len(m)
    prev, pos, neg = 1, 0, 0
    for k in range(size):
        piv = next((i for i in range(k, size) if m[i][i]), None)
        if piv is None:
            pair = next(((i, j) for i in range(k, size) for j in range(i + 1, size) if m[i][j]), None)
            if pair is None:
                return pos, neg, k
            i, j = pair
            for r in range(k, size):
                m[i][r] += m[j][r]
            for r in range(k, size):
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
        for i in range(k + 1, size):
            ri, mik = m[i], m[i][k]
            for j in range(i, size):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = v
                m[j][i] = v
        prev = top
    return pos, neg, size


for label, w in (("c=7,2,2,4,3,1,1", [33, 13, 7, 7, 7, 3, 3]), ("c=7,2,2,4,-1,1,1", [25, 21, 7, 3, 3, 7, 7])):
    strip = [[sum(w[cls[mul[mul[mul[a][v]][inv[b]]][inv[v]]]] for v in range(n)) for b in range(n)] for a in range(n)]
    pairs = list(itertools.product(range(n), repeat=2))
    rows = [[strip[a][b] * strip[b][b2] * strip[b2][a2] * strip[a2][a] for (a, b) in pairs] for (a2, b2) in pairs]
    p, q, r = bareiss_inertia(rows)
    print("LINK_2T_T4|lattice=(Z/1)x(Z/4)|group=2T|%s|w=%s|family=all_576_point_functions_of_(U(0),U(1))|pos=%d|neg=%d|rank=%d|json=0" % (label, ",".join(map(str, w)), p, q, r), flush=True)
