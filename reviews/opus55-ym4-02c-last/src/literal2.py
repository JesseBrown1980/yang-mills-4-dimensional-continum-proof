#!/usr/bin/env python3
"""Literal Gram for the falsifiers on other lattices and groups. Integers only, json=0."""
import sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from literal import literal_gram, run_q8

def run(name, G, w, dims, limit=4000):
    gram, n = literal_gram(G, list(w), dims, limit)
    if gram is None:
        print("LITERAL|group=%s|dims=%s|w=%s|support=%d|too_large=1|json=0" % (name, "x".join(map(str, dims)), ",".join(map(str, w)), n), flush=True)
        return
    sym = all(gram[i][j] == gram[j][i] for i in range(n) for j in range(i))
    p, q, r = bareiss_inertia(gram) if sym else (-1, -1, -1)
    print("LITERAL|group=%s|dims=%s|w=%s|point_functions_with_W_plus_nonzero=%d|symmetric=%d|positive=%d|negative=%d|rank=%d|json=0" % (name, "x".join(map(str, dims)), ",".join(map(str, w)), n, 1 if sym else 0, p, q, r), flush=True)

Z6 = Group(cyclic(6))
run("Z6", Z6, [7, 4, 0, 0, 0, 4], (1, 4))
run("Z6", Z6, [3, 2, 0, 0, 0, 2], (1, 4))
Z5 = Group(cyclic(5))
run("Z5", Z5, [-7, 0, 4, 4, 0], (1, 4))
print(run_q8((0, 1, 0, 0, 0), (1, 1, 6)), flush=True)
