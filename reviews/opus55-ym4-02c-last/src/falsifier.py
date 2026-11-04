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

def run(name, G, w, dims, trials, seed):
    lat = Lat(dims)
    open_half, crossing = split(lat)
    sup = full_support(G, w, lat)
    rows = [(tuple(U[l] for l in open_half), theta_restrict(lat, U, open_half, G.inv), W) for U, W in sup]
    Z = sum(W for _, _, W in rows)
    rnd = random.Random(seed)
    # F is a table on the assignments of the open half that occur, seeded in -9..9. Dense random, then sparse random, then the characters where given.
    keys = sorted({a for a, _, _ in rows} | {b for _, b, _ in rows})
    negative, lowest = 0, None
    for trial in range(trials):
        if trial % 2:
            F = {k: rnd.randint(-9, 9) for k in keys}
        else:
            F = {k: 0 for k in keys}
            for k in rnd.sample(keys, min(4, len(keys))):
                F[k] = rnd.randint(-9, 9)
        N = sum(F[a] * F[b] * W for a, b, W in rows)
        negative += 1 if N < 0 else 0
        lowest = N if lowest is None or N < lowest else lowest
    print("FALSIFIER_DIRECT|group=%s|dims=%s|w=%s|links=%d|assignments_with_nonzero_weight=%d|Z_numerator=%d|open_half_points_seen=%d|seeded_F=%d|F_with_N<0=%d|lowest_N=%d|json=0" % (name, "x".join(map(str, dims)), ",".join(map(str, w)), len(lat.links), len(rows), Z, len(keys), trials, negative, lowest), flush=True)

Q = Group(q8())
assert Q.sizes == [1, 1, 2, 2, 2]
run("Q8", Q, [0, 1, 0, 0, 0], (1, 4), 400, 11)      # control, grid: 4 positive, 1 negative
run("Q8", Q, [0, 1, 0, 0, 0], (1, 1, 4), 400, 12)   # the falsifier
run("Q8", Q, [0, 1, 0, 0, 0], (1, 1, 6), 200, 13)   # every even T
Z6 = Group(cyclic(6))
run("Z6", Z6, [7, 4, 0, 0, 0, 4], (1, 4), 400, 14)
run("Z6", Z6, [3, 2, 0, 0, 0, 2], (1, 4), 400, 15)  # control: 15 positive, 3 negative
Z5 = Group(cyclic(5))
run("Z5", Z5, [-7, 0, 4, 4, 0], (1, 4), 400, 16)
