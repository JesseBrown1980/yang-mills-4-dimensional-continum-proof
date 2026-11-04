#!/usr/bin/env python3
"""A second reading of the falsifier, by a separate route: walk every full assignment of the lattice with a nonzero product of weights, and evaluate N_w(F) = sum conj(F(theta U)) F(U) prod_p w(U_p) directly, on many seeded integer F, with no Gram matrix and no use of the factorization. A seeded negative F is a witness of red. Integers only, json=0."""
import random, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
from literal import split, plaq_value

def full_support(G, w, lat):
    links = list(lat.links)
    # Order links so that plaquettes close early: by time, then the rest.
    links.sort(key=lambda l: (l[0][-1], l[1], l[0]))
    order = {l: i for i, l in enumerate(links)}
    at = [[] for _ in links]
    for p in lat.plaqs:
        word = lat.word(p)
        at[max(order[l] for l, s in word)].append(word)
    out = []
    U = {}
    def walk(i, W):
        if i == len(links):
            out.append((dict(U), W))
            return
        for g in range(G.n):
            U[links[i]] = g
            W2 = W
            for word in at[i]:
                W2 *= w[G.cls[plaq_value(G, word, U)]]
                if W2 == 0:
                    break
            if W2:
                walk(i + 1, W2)
        U.pop(links[i], None)
    walk(0, 1)
    return out

def theta_restrict(lat, U, open_half, inv):
    c = -1
    tm = lat.d - 1
    vals = []
    for (x, mu) in open_half:
        t = x[-1]
        if mu != tm:
            vals.append(U[(x[:-1] + ((c - t) % lat.T,), mu)])
        else:
            vals.append(inv[U[(x[:-1] + ((c - t - 1) % lat.T,), mu)]])
    return tuple(vals)

