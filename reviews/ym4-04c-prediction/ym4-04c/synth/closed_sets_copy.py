"""Judge prototype for polymer-norm C01/C03: count Lemma-B-closed, off-link-connected
fine plaquette sets containing a seed off link, on fine (Z/L)^4 with b = 2 lines.
Integers only.  Usage: python3 closed_sets.py L nmax
"""
import sys
import time
from itertools import combinations

L = int(sys.argv[1])
NMAX = int(sys.argv[2])
D = 4


def site_id(x):
    i = 0
    for c in x:
        i = i * L + (c % L)
    return i


def link_id(x, mu):
    return site_id(x) * D + mu


def is_line(x, mu):
    return all(x[i] % 2 == 0 for i in range(D) if i != mu)


sites = []


def gen(prefix):
    if len(prefix) == D:
        sites.append(tuple(prefix))
        return
    for c in range(L):
        gen(prefix + [c])


gen([])

plaq_links = []
plaq_off = []
for x in sites:
    for mu, nu in combinations(range(D), 2):
        xm = list(x)
        xm[mu] += 1
        xn = list(x)
        xn[nu] += 1
        ls = [(x, mu), (tuple(xm), nu), (tuple(xn), mu), (x, nu)]
        ids = [link_id(y, m) for (y, m) in ls]
        offs = [link_id(y, m) for (y, m) in ls if not is_line(y, m)]
        plaq_links.append(ids)
        plaq_off.append(tuple(offs))

nlinks = len(sites) * D
link_plaqs = [[] for _ in range(nlinks)]
for p, offs in enumerate(plaq_off):
    for e in offs:
        link_plaqs[e].append(p)

# census
deg = []
for p, offs in enumerate(plaq_off):
    nb = set()
    for e in offs:
        for q in link_plaqs[e]:
            if q != p:
                nb.add(q)
    deg.append(len(nb))
print("plaquettes", len(plaq_off), "offcount hist", sorted(set(len(o) for o in plaq_off)),
      "deg max", max(deg), "deg min", min(deg))


def link_class(lid):
    s, mu = divmod(lid, D)
    x = sites[s]
    return sum(1 for i in range(D) if i != mu and x[i] % 2 == 1)


def count_closed(seed):
    """Closure-driven growth from the 6 plaquettes through seed; dedup by frozenset."""
    start = [frozenset([p]) for p in link_plaqs[seed]]
    seen = set(start)
    frontier = list(start)
    counts = {}
    states = 0
    while frontier:
        S = frontier.pop()
        states += 1
        mult = {}
        for p in S:
            for e in plaq_off[p]:
                mult[e] = mult.get(e, 0) + 1
        open_links = [e for e, m in mult.items() if m == 1]
        n = len(S)
        if not open_links:
            counts[n] = counts.get(n, 0) + 1
            if n < NMAX:
                cands = set()
                for e in mult:
                    for q in link_plaqs[e]:
                        if q not in S:
                            cands.add(q)
                for q in cands:
                    T = S | {q}
                    if T not in seen:
                        seen.add(T)
                        frontier.append(T)
            continue
        rem = NMAX - n
        if rem <= 0 or len(open_links) > 4 * rem:
            continue
        e0 = min(open_links)
        for q in link_plaqs[e0]:
            if q in S:
                continue
            T = S | {q}
            if T in seen:
                continue
            # prune: open links after adding q
            m2 = dict(mult)
            for e in plaq_off[q]:
                m2[e] = m2.get(e, 0) + 1
            op = sum(1 for v in m2.values() if v == 1)
            if op > 4 * (rem - 1):
                continue
            seen.add(T)
            frontier.append(T)
    return counts, states


reps = {}
for lid in range(nlinks):
    s, mu = divmod(lid, D)
    if is_line(sites[s], mu):
        continue
    c = link_class(lid)
    x = sites[s]
    if c not in reps:
        reps[c] = lid
    # prefer seeds near origin to avoid edge effects (torus anyway)
for c in sorted(reps):
    t0 = time.time()
    counts, states = count_closed(reps[c])
    print("class(odd transverse)=", c, "seed", reps[c], "counts", dict(sorted(counts.items())),
          "states", states, "time %.1fs" % (time.time() - t0))
    sys.stdout.flush()
