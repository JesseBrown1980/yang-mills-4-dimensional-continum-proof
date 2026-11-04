#!/usr/bin/env python3
"""(Z/1)x(Z/4) with Q8 beyond the grid -3..3. Weights with a zero, c_0 > 0 (the sign is free since w and -w give one form), some c_rho c_0 < 0, up to permuting i,j,k. Early exit on the first negative pivot. Integers only, json=0. usage = q8_wide.py N"""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
G = Group(q8())
assert G.sizes == [1, 1, 2, 2, 2]
chi = [[1,1,1,1,1],[1,1,1,-1,-1],[1,1,-1,1,-1],[1,1,-1,-1,1],[2,-2,0,0,0]]
size = [1,1,2,2,2]
N = int(sys.argv[1])
M, I, CL, REP = G.mul, G.inv, G.cls, G.reps
# Pre-tabulate the class of x V y^-1 V^-1 as a count over V.
COUNT = [[[0]*5 for _ in range(5)] for _ in range(5)]
for x in range(5):
    for y in range(5):
        for v in range(8):
            COUNT[x][y][CL[M[M[M[REP[x]][v]][I[REP[y]]]][I[v]]]] += 1

def red_fast(rows):
    m = [list(r) for r in rows]
    n = len(m)
    prev = 1
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i]), None)
        if piv is None:
            if any(m[i][j] for i in range(k, n) for j in range(i + 1, n)):
                return True  # a zero diagonal with a nonzero off-diagonal is indefinite
            return False
        if m[piv][piv] * prev < 0:
            return True
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        for i in range(k + 1, n):
            mik = m[i][k]
            ri, rk = m[i], m[k]
            for j in range(i, n):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                ri[j] = v
                m[j][i] = v
        prev = top
    return False

total = psd = 0
ex = []
rng = range(-N, N + 1)
for a, b in itertools.product(rng, repeat=2):
    for c1 in rng:
        for c2 in rng:
            if c2 < c1:
                continue
            for c3 in rng:
                if c3 < c2:
                    continue
                w = (a, b, c1, c2, c3)
                if 0 not in w:
                    continue
                c8 = [sum(size[k] * w[k] * chi[r][k] for k in range(5)) for r in range(5)]
                if c8[0] <= 0 or min(c8) >= 0:
                    continue
                total += 1
                K = [[sum(COUNT[x][y][k] * w[k] for k in range(5)) for y in range(5)] for x in range(5)]
                S = [(x, y) for x in range(5) for y in range(5) if any(COUNT[x][y][k] and w[k] for k in range(5))]
                rows = [[K[p][p2] * K[q][q2] for (p2, q2) in S] for (p, q) in S]
                if not red_fast(rows):
                    psd += 1
                    if len(ex) < 12:
                        ex.append((w, c8, len(S)))
print("Q8_WIDE|lattice=(Z/1)x(Z/4)|value_range=-%d..%d|up_to_permuting_i,j,k|c_0>0|weights_with_a_zero_and_some_c_rho<0=%d|PSD=%d|json=0" % (N, N, total, psd))
for w, c8, s in ex:
    print("Q8_WIDE_EXAMPLE|w=%s|c_times_8=%s|dim_S=%d|json=0" % (",".join(map(str, w)), ",".join(map(str, c8)), s))
