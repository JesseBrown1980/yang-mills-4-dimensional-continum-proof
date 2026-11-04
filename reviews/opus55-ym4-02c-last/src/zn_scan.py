#!/usr/bin/env python3
"""Z/n, n even, w(0)=a, w(+-1)=b, 0 elsewhere. Exact inertia of K tensor K on S at (Z/1)x(Z/4). The character (-1)^x has coefficient (a-2b)/n and c_0=(a+2b)/n. Integers only."""
import sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from k1scan import *
for n in (6, 8, 10, 12, 14, 16):
    G = Group(cyclic(n))
    for a, b in ((3, 2), (7, 4), (13, 7), (15, 8), (19, 10), (9, 5), (11, 6), (39, 20), (79, 40), (159, 80)):
        w = [0] * n
        w[0] = a; w[1] = b; w[n - 1] = b
        S, rows, K = form(G, w)
        p, q, r = bareiss_inertia(rows)
        print("ZN|n=%d|a=%d|b=%d|c0_times_n=%d|c_alt_times_n=%d|dim_S=%d|positive=%d|negative=%d|rank=%d|json=0" % (n, a, b, a + 2 * b, a - 2 * b, len(S), p, q, r), flush=True)
