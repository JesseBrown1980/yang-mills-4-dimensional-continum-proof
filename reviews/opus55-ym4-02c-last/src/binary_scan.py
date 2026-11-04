#!/usr/bin/env python3
"""(Z/1)x(Z/4) with 2T, the binary tetrahedral subgroup of SU(2): weights with a zero, values in -4..4 on inverse-closed class orbits, c_0>0, some coefficient negative. Looks for a PSD case, since a falsifier inside SU(2)'s subgroups bears on the open item. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from k1scan import kmat
def quat_mul(a, b):
    return (a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3], a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2], a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1], a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0])
# Units of the Hurwitz order, coordinates doubled, so products divide by 2.
els = [(s*2,0,0,0) for s in (1,-1)] + [(0,s*2,0,0) for s in (1,-1)] + [(0,0,s*2,0) for s in (1,-1)] + [(0,0,0,s*2) for s in (1,-1)] + [(a,b,c,d) for a in (1,-1) for b in (1,-1) for c in (1,-1) for d in (1,-1)]
idx = {e: i for i, e in enumerate(els)}
mul = [[idx[tuple(x // 2 for x in quat_mul(a, b))] for b in els] for a in els]
G = Group(mul)
n = len(G.reps)
orbits, seen = [], set()
for k in range(n):
    if k not in seen:
        o = sorted({k, G.icls[k]})
        seen.update(o)
        orbits.append(o)
def red_fast(rows):
    m = [list(r) for r in rows]
    N = len(m)
    prev = 1
    for k in range(N):
        piv = next((i for i in range(k, N) if m[i][i]), None)
        if piv is None:
            return any(m[i][j] for i in range(k, N) for j in range(i + 1, N))
        if m[piv][piv] * prev < 0:
            return True
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        for i in range(k + 1, N):
            mik = m[i][k]
            ri, rk = m[i], m[k]
            for j in range(i, N):
                v = (ri[j] * top - mik * rk[j]) // prev
                ri[j] = v
                m[j][i] = v
        prev = top
    return False
# Tabulate class counts once.
COUNT = [[[0]*n for _ in range(n)] for _ in range(n)]
M, I, CL = G.mul, G.inv, G.cls
for x in range(n):
    for y in range(n):
        for v in range(G.n):
            COUNT[x][y][CL[M[M[M[G.reps[x]][v]][I[G.reps[y]]]][I[v]]]] += 1
total = psd = 0
ex = []
for vals in itertools.product(range(-4, 5), repeat=len(orbits)):
    if 0 not in vals or not any(vals):
        continue
    w = [0] * n
    for o, v in zip(orbits, vals):
        for k in o:
            w[k] = v
    c0 = sum(G.sizes[k] * w[k] for k in range(n))
    if c0 <= 0:
        continue
    K = [[sum(COUNT[x][y][k]*w[k] for k in range(n)) for y in range(n)] for x in range(n)]
    if not red_fast(K):
        continue   # K is positive semidefinite on classes, so no coefficient is negative
    total += 1
    S = [(x, y) for x in range(n) for y in range(n) if any(COUNT[x][y][k] and w[k] for k in range(n))]
    rows = [[K[a][a2]*K[b][b2] for (a2, b2) in S] for (a, b) in S]
    if not red_fast(rows):
        psd += 1
        if len(ex) < 8:
            ex.append((vals, c0, len(S)))
print("BINARY_SCAN|group=2T|order=%d|classes=%d|inverse_closed_orbits=%d|lattice=(Z/1)x(Z/4)|values=-4..4|c_0>0|with_a_zero_and_some_c_rho<0=%d|PSD=%d|json=0" % (G.n, n, len(orbits), total, psd), flush=True)
for e in ex:
    print("BINARY_SCAN_EXAMPLE|values_on_orbits=%s|c0_times_24=%d|dim_S=%d|json=0" % (",".join(map(str, e[0])), e[1], e[2]))
