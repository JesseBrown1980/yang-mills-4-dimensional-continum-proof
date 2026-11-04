#!/usr/bin/env python3
"""Link reflection on (Z/L)x(Z/1)x(Z/T), T>=4, Q8, by gauge orbits of a slice. H(O0,O1) is free on the pairs that W_plus reaches, and the form is K tensor K on those pairs, with K the crossing kernel between orbits. Checked against the literal Gram on L=1. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
Q = Group(q8())
assert Q.sizes == [1, 1, 2, 2, 2]
M, I, CL = Q.mul, Q.inv, Q.cls
chi = [[1,1,1,1,1],[1,1,1,-1,-1],[1,1,-1,1,-1],[1,1,-1,-1,1],[2,-2,0,0,0]]
size = [1,1,2,2,2]

def c8(w):
    return [sum(size[k] * w[k] * chi[r][k] for k in range(5)) for r in range(5)]

class Slice:
    """Links: a[x] in direction 1 and b[x] in direction 2, x in Z/L, direction 2 of side 1. A configuration is (a_0..a_{L-1}, b_0..b_{L-1})."""
    def __init__(self, L):
        self.L = L
    def plaquette_classes(self, cfg):
        L = self.L
        a, b = cfg[:L], cfg[L:]
        out = []
        for x in range(L):
            y = (x + 1) % L
            # U_1(x) U_2(x+1) U_1(x+2hat)^-1 U_2(x)^-1, and the shift in direction 2 is trivial.
            h = M[M[M[a[x]][b[y]]][I[a[x]]]][I[b[x]]]
            out.append(CL[h])
        return tuple(out)
    def gauge(self, cfg, g):
        L = self.L
        a, b = cfg[:L], cfg[L:]
        na = tuple(M[M[g[x]][a[x]]][I[g[(x + 1) % L]]] for x in range(L))
        nb = tuple(M[M[g[x]][b[x]]][I[g[x]]] for x in range(L))
        return na + nb
    def time_classes(self, cfg, cfg2, v):
        """Classes of the time-like plaquettes between two slices, with time links v[x]: U_i(x,t) V(x+i,t) U_i(x,t+1)^-1 V(x,t)^-1."""
        L = self.L
        a, b = cfg[:L], cfg[L:]
        a2, b2 = cfg2[:L], cfg2[L:]
        out = []
        for x in range(L):
            y = (x + 1) % L
            out.append(CL[M[M[M[a[x]][v[y]]][I[a2[x]]]][I[v[x]]]])
            out.append(CL[M[M[M[b[x]][v[x]]][I[b2[x]]]][I[v[x]]]])
        return out

def orbits(S, allowed):
    """Gauge orbits among configurations whose slice plaquettes lie in the allowed classes. Returns reps with their class list."""
    L = S.L
    seen = {}
    reps = []
    gauges = list(itertools.product(range(8), repeat=L))
    # Walk with pruning on plaquettes is unnecessary at L<=3 with 2L links, at most 8^6.
    for cfg in itertools.product(range(8), repeat=2 * L):
        pc = S.plaquette_classes(cfg)
        if not all(c in allowed for c in pc):
            continue
        if cfg in seen:
            continue
        k = len(reps)
        reps.append(cfg)
        for g in gauges:
            seen[S.gauge(cfg, g)] = k
    return reps

def kernel(S, reps, w):
    gauges = list(itertools.product(range(8), repeat=S.L))
    n = len(reps)
    K = [[0] * n for _ in range(n)]
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total, r = 0, False
            for v in gauges:
                t = 1
                for c in S.time_classes(reps[i], reps[j], v):
                    t *= w[c]
                    if t == 0:
                        break
                if t:
                    r = True
                    total += t
            K[i][j], reach[i][j] = total, r
    return K, reach

def form(S, w):
    allowed = {k for k in range(5) if w[k]}
    reps = orbits(S, allowed)
    K, reach = kernel(S, reps, w)
    n = len(reps)
    pairs = [(i, j) for i in range(n) for j in range(n) if reach[i][j]]
    rows = [[K[a][a2] * K[b][b2] for (a2, b2) in pairs] for (a, b) in pairs]
    return len(reps), pairs, rows, K

if __name__ == "__main__":
    for L, w in ((1, (0, 1, 0, 0, 0)), (3, (0, 1, 0, 0, 0)), (2, (0, 1, 0, 0, 0))):
        S = Slice(L)
        nreps, pairs, rows, K = form(S, list(w))
        pk, qk, rk = bareiss_inertia(K)
        p, q, r = bareiss_inertia(rows)
        print("K2_ORBITS|lattice=(Z/%d)x(Z/1)x(Z/T),T>=4|group=Q8|w=%s|c_times_8=%s|slice_orbits=%d|K_on_those_positive=%d|K_negative=%d|pairs_reached=%d|positive=%d|negative=%d|rank=%d|json=0" % (L, ",".join(map(str, w)), ",".join(map(str, c8(w))), nreps, pk, qk, len(pairs), p, q, r), flush=True)
