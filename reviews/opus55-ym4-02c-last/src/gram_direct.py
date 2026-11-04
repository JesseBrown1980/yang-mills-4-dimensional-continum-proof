#!/usr/bin/env python3
"""The Gram matrix read off the full walk: each assignment U with a nonzero product of weights adds that product to the entry (theta U restricted to the open half, U restricted to the open half). No crossing kernel, no cache, no factorization. Integers only, json=0."""
import sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from literal import split
from falsifier_lib import full_support, theta_restrict

def run(name, G, w, dims):
    lat = Lat(dims)
    open_half, crossing = split(lat)
    sup = full_support(G, w, lat)
    entries = {}
    keys = set()
    for U, W in sup:
        b = tuple(U[l] for l in open_half)
        a = theta_restrict(lat, U, open_half, G.inv)
        keys.add(a); keys.add(b)
        entries[(a, b)] = entries.get((a, b), 0) + W
    keys = sorted(keys)
    idx = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    m = [[0] * n for _ in range(n)]
    for (a, b), v in entries.items():
        m[idx[a]][idx[b]] = v
    sym = all(m[i][j] == m[j][i] for i in range(n) for j in range(i))
    p, q, r = bareiss_inertia(m)
    print("GRAM_DIRECT|group=%s|dims=%s|w=%s|assignments_with_nonzero_weight=%d|open_half_points=%d|symmetric=%d|positive=%d|negative=%d|rank=%d|json=0" % (name, "x".join(map(str, dims)), ",".join(map(str, w)), len(sup), n, 1 if sym else 0, p, q, r), flush=True)

Q = Group(q8())
run("Q8", Q, [0, 1, 0, 0, 0], (1, 4))
run("Q8", Q, [0, 1, 0, 0, 0], (1, 1, 4))
run("Q8", Q, [0, -1, 0, 0, 0], (1, 1, 4))
run("Q8", Q, [0, 1, 0, 0, 0], (1, 1, 6))
Z6 = Group(cyclic(6))
run("Z6", Z6, [7, 4, 0, 0, 0, 4], (1, 4))
run("Z6", Z6, [3, 2, 0, 0, 0, 2], (1, 4))
Z5 = Group(cyclic(5))
run("Z5", Z5, [-7, 0, 4, 4, 0], (1, 4))
