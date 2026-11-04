#!/usr/bin/env python3
"""(Z/1)x(Z/4), small finite groups, weights with a zero, c_0 nonzero, some c_rho c_0 < 0 (sign read from the Gram of K on classes). Reports each group's first PSD case, and counts. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from k1scan import form, kmat

def inertia_K(K, sizes):
    # K on class functions: the operator is K(x,y) with measure size(y). Its eigen-signs are those of the symmetric matrix D^(1/2) K D^(1/2), whose inertia equals that of K as a quadratic form under diagonal congruence.
    return bareiss_inertia(K)

def run(name, G, rng, cap=None):
    # Weights: integer on each inverse-closed union of classes.
    n = len(G.reps)
    orbits = []
    seen = set()
    for k in range(n):
        if k not in seen:
            o = sorted({k, G.icls[k]})
            seen.update(o)
            orbits.append(o)
    total = psd = 0
    first = None
    examples = []
    for vals in itertools.product(rng, repeat=len(orbits)):
        if 0 not in vals or not any(vals):
            continue
        w = [0] * n
        for o, v in zip(orbits, vals):
            for k in o:
                w[k] = v
        c0 = sum(G.sizes[k] * w[k] for k in range(n))
        if c0 == 0:
            continue
        S, rows, K = form(G, w)
        pk, qk, rk = bareiss_inertia(K)
        # K's negative index, with c_0's sign. K carries the trivial eigenvector with eigenvalue proportional to c_0.
        opposite = (qk > 0) if c0 > 0 else (pk > 0)
        if not opposite:
            continue
        total += 1
        p, q, r = bareiss_inertia(rows)
        if q == 0:
            psd += 1
            if len(examples) < 4:
                examples.append((vals, c0, pk, qk, len(S), p, q, r))
    print("GROUP_SCAN|group=%s|order=%d|classes=%d|inverse_closed_orbits=%d|value_range=%d..%d|weights_with_a_zero_and_opposite_coefficient=%d|PSD=%d|json=0" % (name, G.n, n, len(orbits), rng[0], rng[-1], total, psd), flush=True)
    for e in examples:
        print("GROUP_SCAN_EXAMPLE|group=%s|values_on_orbits=%s|c0_times_order=%d|K_inertia=%d,%d|dim_S=%d|positive=%d|negative=%d|rank=%d|json=0" % (name, ",".join(map(str, e[0])), e[1], e[2], e[3], e[4], e[5], e[6], e[7]), flush=True)

S3 = perm_group([(1, 2, 0), (1, 0, 2)])
D4 = perm_group([(1, 2, 3, 0), (0, 3, 2, 1)])
Z22 = direct(cyclic(2), cyclic(2))
for name, mul, rng in (("Z2", cyclic(2), range(-9, 10)), ("Z3", cyclic(3), range(-9, 10)), ("Z4", cyclic(4), range(-9, 10)), ("Z2xZ2", Z22, range(-5, 6)), ("Z5", cyclic(5), range(-9, 10)), ("Z6", cyclic(6), range(-5, 6)), ("S3", S3, range(-7, 8)), ("D4", D4, range(-3, 4))):
    run(name, Group(mul), list(rng))
