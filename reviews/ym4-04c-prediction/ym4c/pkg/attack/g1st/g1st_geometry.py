# Sanity read of the b=2 geometry facts G1 uses, on fine (Z/8)^4 with coarse (Z/4)^4. Integers only.
import itertools
M = 8; L = M // 2; D = 4
E = [tuple(1 if i == m else 0 for i in range(D)) for m in range(D)]
add = lambda x, y: tuple((a + b) % M for a, b in zip(x, y))
sub = lambda x, y: tuple((a - b) % M for a, b in zip(x, y))
sites = list(itertools.product(range(M), repeat=D))
def is_line(x, mu):  # every coordinate other than mu even
    return all(x[i] % 2 == 0 for i in range(D) if i != mu)
# coarse link of a line link: x = 2x' or 2x'+e_mu
def coarse_of(x, mu):
    base = x if x[mu] % 2 == 0 else sub(x, E[mu])
    return (tuple((c // 2) % L for c in base), mu), (0 if x[mu] % 2 == 0 else 1)
links = [(x, mu) for x in sites for mu in range(D)]
pos = {}
for (x, mu) in links:
    if is_line(x, mu):
        cl, p = coarse_of(x, mu)
        assert (cl, p) not in pos; pos[(cl, p)] = (x, mu)
ncoarse = L**D * D
assert len(pos) == 2 * ncoarse, len(pos)  # distinct coarse links have disjoint positions
# links at a site
def links_at(x):
    return [(x, mu) for mu in range(D)] + [(sub(x, E[mu]), mu) for mu in range(D)]
mid_ok = coarse_ok = 0
for x in sites:
    odd = [i for i in range(D) if x[i] % 2]
    at = links_at(x); nl = sum(is_line(*l) for l in at)
    if len(odd) == 1:
        assert nl == 2 and len(at) - nl == 6; mid_ok += 1
    if len(odd) == 0:
        assert nl == 8; coarse_ok += 1
assert mid_ok == ncoarse and coarse_ok == L**D  # one midpoint per coarse link; g~ well defined
# plaquettes: line-link count
hist = {}
for x in sites:
    for mu, nu in itertools.combinations(range(D), 2):
        pl = [(x, mu), (add(x, E[mu]), nu), (add(x, E[nu]), mu), (x, nu)]
        n = sum(is_line(*l) for l in pl); hist[n] = hist.get(n, 0) + 1
print("plaquettes by number of line links:", dict(sorted(hist.items())))
# coarse girth: no closed walk of 1..3 distinct links forms a cycle on (Z/L)^4
steps = [(m, s) for m in range(D) for s in (1, -1)]
def mv(x, m, s): return tuple((c + s * (i == m)) % L for i, c in enumerate(x))
short = 0
o = (0,) * D
for k in (1, 2, 3):
    for seq in itertools.product(steps, repeat=k):
        x = o; used = []
        for (m, s) in seq:
            y = mv(x, m, s); lk = (x, m) if s == 1 else (y, m); used.append(lk); x = y
        if x == o and len(set(used)) == k: short += 1
print("coarse cycles of length 1..3 through the origin:", short)
print("checks passed: positions disjoint (%d coarse links), midpoints 2 line + 6 off (%d), coarse sites 8 line links (%d)" % (ncoarse, mid_ok, coarse_ok))
