#!/usr/bin/env python3
"""Literal Gram matrix of N_w(F1,F2) on the point functions of the open half under link reflection, from the definitions in sections 1 and 3 of the lemma:
U_p = U_mu(y) U_nu(y+mu) U_mu(y+nu)^-1 U_nu(y)^-1, (theta U)_i(x,t) = U_i(x,c-t), (theta V)(x,t) = V(x,c-t-1)^-1, c=-1.
Point functions with W_plus = 0 give zero rows, so only the support is kept. Every plaquette is read from its word. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *

def split(lat):
    m = lat.T // 2
    tm = lat.d - 1
    open_half, crossing = [], []
    for (x, mu) in lat.links:
        t = x[-1]
        if mu != tm:
            if t < m:
                open_half.append((x, mu))
        else:
            if t < m - 1:
                open_half.append((x, mu))
            elif t == m - 1 or t == lat.T - 1:
                crossing.append((x, mu))
    return open_half, crossing

def reflect_assign(lat, link, value, inv):
    """The link whose value is fixed by (theta U)(link) = value, and that value. c = -1."""
    x, mu = link
    tm = lat.d - 1
    t = x[-1]
    if mu != tm:
        return (x[:-1] + ((-1 - t) % lat.T,), mu), value
    return (x[:-1] + ((-1 - t - 1) % lat.T,), mu), inv[value]

def plaq_value(G, word, U):
    h = G.one
    for link, s in word:
        g = U[link]
        h = G.mul[h][g if s > 0 else G.inv[g]]
    return h

def open_support(G, w, lat):
    """All assignments of the open half with W_plus != 0, by a depth-first walk that prunes on each upper plaquette as soon as its four links are set."""
    open_half, crossing = split(lat)
    oset = set(open_half)
    upper = []
    for p in lat.plaqs:
        word = lat.word(p)
        if all(l in oset for l, s in word):
            upper.append((p, word))
    order = {l: i for i, l in enumerate(open_half)}
    at = [[] for _ in open_half]
    for p, word in upper:
        at[max(order[l] for l, s in word)].append(word)
    out = []
    U = {}
    def walk(i, W):
        if i == len(open_half):
            out.append((dict(U), W))
            return
        for g in range(G.n):
            U[open_half[i]] = g
            W2 = W
            for word in at[i]:
                W2 *= w[G.cls[plaq_value(G, word, U)]]
                if W2 == 0:
                    break
            if W2:
                walk(i + 1, W2)
        U.pop(open_half[i], None)
    walk(0, 1)
    return open_half, crossing, upper, out

def literal_gram(G, w, dims, limit=4000):
    lat = Lat(dims)
    open_half, crossing, upper, sup = open_support(G, w, lat)
    if len(sup) > limit:
        return None, len(sup)
    oset = set(open_half)
    cset = set(crossing)
    words = {p: lat.word(p) for p in lat.plaqs}
    # Which plaquettes hold a crossing link, and which lie wholly in the lower half.
    crossing_p = [words[p] for p in lat.plaqs if any(l in cset for l, s in words[p])]
    lower_p = [words[p] for p in lat.plaqs if not any(l in cset for l, s in words[p]) and not all(l in oset for l, s in words[p])]
    # Boundary links read by the crossing plaquettes, for a cache.
    keys = sorted({l for wd in crossing_p for l, s in wd if l not in cset})
    cache = {}
    rows = []
    n = len(sup)
    gram = [[0] * n for _ in range(n)]
    for ia, (a, wa) in enumerate(sup):
        lowerU = {}
        for link in open_half:
            l2, v2 = reflect_assign(lat, link, a[link], G.inv)
            lowerU[l2] = v2
        lowW = 1
        for wd in lower_p:
            lowW *= w[G.cls[plaq_value(G, wd, lowerU)]]
        for ib, (b, wb) in enumerate(sup):
            if lowW == 0:
                continue
            U = dict(b)
            U.update(lowerU)
            key = tuple(U[l] for l in keys)
            total = cache.get(key)
            if total is None:
                total = 0
                for vals in itertools.product(range(G.n), repeat=len(crossing)):
                    U2 = dict(U)
                    U2.update(zip(crossing, vals))
                    t = 1
                    for wd in crossing_p:
                        t *= w[G.cls[plaq_value(G, wd, U2)]]
                        if t == 0:
                            break
                    total += t
                cache[key] = total
            gram[ia][ib] = lowW * wb * total
    return gram, n

def coefficients_q8(w):
    # On +1,-1,i,j,k. Times 8.
    chi = [[1,1,1,1,1],[1,1,1,-1,-1],[1,1,-1,1,-1],[1,1,-1,-1,1],[2,-2,0,0,0]]
    size = [1,1,2,2,2]
    return [sum(size[k]*w[k]*chi[r][k] for k in range(5)) for r in range(5)]

def q8_group():
    # Order the classes +1,-1,i,j,k as in the lemma.
    G = Group(q8())
    return G

def run_q8(w, dims):
    G = q8_group()
    # G.cls numbers classes in first-seen order on the elements +1,-1,+i,-i,+j,-j,+k,-k, which is +1,-1,i,j,k.
    assert G.sizes == [1, 1, 2, 2, 2]
    gram, n = literal_gram(G, list(w), dims)
    if gram is None:
        return "LITERAL|group=Q8|dims=%s|w=%s|support=%d|too_large=1|json=0" % (dims, ",".join(map(str, w)), n)
    sym = all(gram[i][j] == gram[j][i] for i in range(n) for j in range(i))
    p, q, r = bareiss_inertia(gram) if sym else (-1, -1, -1)
    return "LITERAL|group=Q8|dims=%s|w=%s|c_times_8=%s|point_functions_with_W_plus_nonzero=%d|symmetric=%d|positive=%d|negative=%d|rank=%d|json=0" % ("x".join(map(str, dims)), ",".join(map(str, w)), ",".join(map(str, coefficients_q8(w))), n, 1 if sym else 0, p, q, r)

if __name__ == "__main__":
    # Controls against filed values on (Z/1)x(Z/4): c=8,3,3,3,1 is 25,0; c=8,3,3,3,-1 is 17,8; the grid's example w=-3,-3,0,1,3 is 8,4.
    for w in ((19, 15, 5, 5, 5), (15, 19, 5, 5, 5), (-3, -3, 0, 1, 3), (0, 1, 0, 0, 0), (1, 0, 0, 0, 0)):
        print(run_q8(w, (1, 4)), flush=True)
    # The candidate falsifier, k=2.
    for w in ((0, 1, 0, 0, 0), (0, 3, 0, 0, 0), (0, -1, 0, 0, 0)):
        print(run_q8(w, (1, 1, 4)), flush=True)
