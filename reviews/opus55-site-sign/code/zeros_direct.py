# W_plus(C, .) read directly on odd-side and k = 2 lattices, for the one weight on every plaquette, by depth-first search over the time links at T = 2.
# Each count is exact over all 8^sites assignments of V. Positive controls: C1 a gauge move of C0 has solutions. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *

q8 = Q8_mat()
T, INV = q8.tab, q8.inv
MINUS = next(i for i in range(8) if i and T[i][i] == 0)
els = [x for x in range(8) if x not in (0, MINUS)]
I_ = els[0]
J_ = next(y for y in els if T[I_][y] != T[y][I_])


def central(g):
    return g == 0 or g == MINUS


def S_of(lat, cfg):
    s = 1
    for w in lat.words:
        h = hol(q8, cfg, w)
        if not central(h):
            return 0
        s *= 1 if h == 0 else -1
    return s


def count_V(lat, C0, C1, limit=None):
    """The number of V in Q8^sites with every time-like plaquette central."""
    sites = lat.sites
    pos = {x: i for i, x in enumerate(sites)}
    edges = [(pos[x], pos[lat.step(x, mu)], l) for l, (x, mu) in enumerate(lat.links)]
    by_last = [[] for _ in sites]
    for a, b, l in edges:
        by_last[max(a, b)].append((a, b, l))
    V = [0] * len(sites)
    total = [0]

    def rec(i):
        if i == len(sites):
            total[0] += 1
            return
        for v in range(8):
            if limit is not None and total[0] >= limit:
                return
            V[i] = v
            good = True
            for a, b, l in by_last[i]:
                h = T[T[T[C0[l]][V[b]]][INV[C1[l]]]][INV[V[a]]]
                if not central(h):
                    good = False
                    break
            if good:
                rec(i + 1)

    rec(0)
    return total[0]


def twist(lat):
    return [I_ if mu == 0 and x[0] == 0 else J_ if mu == 1 and x[1] == 0 else 0 for x, mu in lat.links]


for dims in ((3, 3, 3), (1, 1), (2, 1), (3, 1), (1, 1, 1), (1, 1, 3), (2, 2, 5)):
    lat = Lat(*dims)
    tw = twist(lat)
    triv = [0] * len(lat.links)
    s_tw, s_tr = S_of(lat, tw), S_of(lat, triv)
    n_diff = count_V(lat, tw, triv)
    n_same = count_V(lat, tw, tw, limit=1)
    print("IND_ZERO_DFS|lattice=%sxT2|S(twist)=%+d|S(trivial)=%+d|f(twist,trivial)=%+d|V_with_every_time_like_plaquette_central_at_(twist,trivial)=%d|at_least_this_many_at_(twist,twist)=%d|json=0" % ("x".join(map(str, dims)), s_tw, s_tr, s_tw * s_tr, n_diff, n_same))
    sys.stdout.flush()

# Random central slices with the two values of S, on the lattices where both occur.
for dims, seed in (((2, 2), 3), ((3, 3), 4), ((2, 2, 3), 5), ((2, 1), 6), ((3, 1), 7)):
    lat = Lat(*dims)
    rng = RNG(seed)
    bank = {1: [], -1: []}
    tries = 0
    pos = {x: i for i, x in enumerate(lat.sites)}
    while (len(bank[1]) < 12 or len(bank[-1]) < 12) and tries < 20000:
        tries += 1
        vals = [0, I_, J_, T[I_][J_]]
        pick = [vals[rng.below(4)] for _ in range(lat.k)]
        cfg = [pick[mu] if x[mu] == 0 else 0 for x, mu in lat.links]
        g = [rng.below(8) for _ in lat.sites]
        cfg = [T[T[g[pos[x]]][c]][INV[g[pos[lat.step(x, mu)]]]] for c, (x, mu) in zip(cfg, lat.links)]
        cfg = [T[MINUS][c] if rng.below(2) else c for c in cfg]
        s = S_of(lat, cfg)
        if s and len(bank[s]) < 12:
            bank[s].append(cfg)
    opposite_alive = same_alive = opposite_pairs = same_pairs = 0
    for a in bank[1]:
        for b in bank[-1]:
            opposite_pairs += 1
            opposite_alive += 1 if count_V(lat, a, b, limit=1) else 0
    for s in (1, -1):
        for a in bank[s]:
            for b in bank[s]:
                same_pairs += 1
                same_alive += 1 if count_V(lat, a, b, limit=1) else 0
    print("IND_ZERO_DFS_RANDOM|lattice=%sxT2|S+_slices=%d|S-_slices=%d|pairs_with_opposite_S=%d|of_those_with_W_plus_not_identically_0=%d|pairs_with_equal_S=%d|of_those_with_W_plus_not_identically_0=%d|json=0" % ("x".join(map(str, dims)), len(bank[1]), len(bank[-1]), opposite_pairs, opposite_alive, same_pairs, same_alive))
    sys.stdout.flush()
print("IND_ZERO_DFS_DONE|json=0")
