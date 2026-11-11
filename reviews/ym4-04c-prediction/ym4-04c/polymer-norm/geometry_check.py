#!/usr/bin/env python3
"""Scratch geometry facts for the b=2 line blocking on fine (Z/8)^4 (design lane, integers only)."""
import itertools
L = 8
d = 4
def add(x, mu, s=1):
    y = list(x); y[mu] = (y[mu] + s) % L; return tuple(y)
sites = list(itertools.product(range(L), repeat=d))
def is_line(x, mu):
    # fine link (x,mu) is a line link of coarse link iff all x_nu even for nu != mu
    return all(x[n] % 2 == 0 for n in range(d) if n != mu)
plaqs = []
for x in sites:
    for mu in range(d):
        for nu in range(mu + 1, d):
            links = [(x, mu), (add(x, mu), nu), (add(x, nu), mu), (x, nu)]
            plaqs.append(tuple(links))
link_to_p = {}
for i, p in enumerate(plaqs):
    for l in p:
        link_to_p.setdefault(l, []).append(i)
assert all(len(v) == 6 for v in link_to_p.values())
offdeg = []
noff = []
for i, p in enumerate(plaqs):
    nb = set()
    k = 0
    for l in p:
        if is_line(*l):
            continue
        k += 1
        for j in link_to_p[l]:
            if j != i:
                nb.add(j)
    offdeg.append(len(nb)); noff.append(k)
print("plaquettes", len(plaqs), "max_offlink_degree", max(offdeg), "min", min(offdeg), "off links per plaquette in", sorted(set(noff)))
# W(e0): off links of the 6 plaquettes through a line link
wsizes = set()
for l, ps in link_to_p.items():
    if not is_line(*l):
        continue
    W = set()
    for i in ps:
        for m in plaqs[i]:
            if not is_line(*m):
                W.add(m)
    wsizes.add(len(W))
print("|W(line link)| values", sorted(wsizes))
# fillings: number of coarse fillings containing an off link, by class
from collections import Counter
fill_count = Counter()
for x in sites:
    if any(c % 2 for c in x):
        continue
    for mu in range(d):
        for nu in range(mu + 1, d):
            # 4 fine plaquettes of the 2x2 block at x in plane mu,nu
            for s, t in itertools.product(range(2), repeat=2):
                y = add(add(x, mu, s), nu, t)
                p = ((y, mu), (add(y, mu), nu), (add(y, nu), mu), (y, nu))
                for l in p:
                    if not is_line(*l):
                        fill_count[l] += 1
offl = [l for l in link_to_p if not is_line(*l)]
print("off links", len(offl), "filling multiplicity histogram", Counter(fill_count[l] for l in offl))
