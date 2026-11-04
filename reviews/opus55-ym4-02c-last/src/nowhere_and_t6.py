#!/usr/bin/env python3
"""Two reads. (1) The exact statement of Remark 6.2 on other finite groups at (Z/1)x(Z/4): nowhere-zero w, c_0 nonzero, PSD exactly when no coefficient has sign opposite to c_0. (2) The Z/6 falsifier at T=6, for scope. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from k1scan import form

S3 = perm_group([(1, 2, 0), (1, 0, 2)])
D4 = perm_group([(1, 2, 3, 0), (0, 3, 2, 1)])
A4 = perm_group([(1, 2, 0, 3), (1, 0, 3, 2)])
for name, mul in (("Z3", cyclic(3)), ("Z4", cyclic(4)), ("Z5", cyclic(5)), ("Z6", cyclic(6)), ("S3", S3), ("D4", D4), ("A4", A4)):
    G = Group(mul)
    n = len(G.reps)
    orbits, seen = [], set()
    for k in range(n):
        if k not in seen:
            o = sorted({k, G.icls[k]})
            seen.update(o)
            orbits.append(o)
    agree = disagree = 0
    for vals in itertools.product([v for v in range(-3, 4) if v], repeat=len(orbits)):
        w = [0] * n
        for o, v in zip(orbits, vals):
            for k in o:
                w[k] = v
        c0 = sum(G.sizes[k] * w[k] for k in range(n))
        if c0 == 0:
            continue
        S, rows, K = form(G, w)
        pk, qk, rk = bareiss_inertia(K)
        opposite = qk > 0 if c0 > 0 else pk > 0
        p, q, r = bareiss_inertia(rows)
        if (q == 0) == (not opposite):
            agree += 1
        else:
            disagree += 1
    print("NOWHERE_ZERO|group=%s|lattice=(Z/1)x(Z/4)|values_on_inverse_closed_orbits=-3..3_nonzero|c_0_nonzero|PSD_iff_no_opposite_coefficient_agree=%d|disagree=%d|json=0" % (name, agree, disagree), flush=True)

# (2) T=6 on (Z/1)x(Z/6), Z/6: H(x0,x2) free on pairs joined through some x1. K tensor K on those.
G = Group(cyclic(6))
w = [7, 4, 0, 0, 0, 4]
D = {g for g in range(6) if w[g]}
S2 = [(x, y) for x in range(6) for y in range(6) if any(((x - z) % 6 in D) and ((z - y) % 6 in D) for z in range(6))]
K = [[w[(x - y) % 6] for y in range(6)] for x in range(6)]
rows = [[K[a][a2] * K[b][b2] for (a2, b2) in S2] for (a, b) in S2]
print("Z6_T6|w=7,4,0,0,0,4|pairs=%d|inertia=%d,%d,%d|json=0" % ((len(S2),) + bareiss_inertia(rows)))
