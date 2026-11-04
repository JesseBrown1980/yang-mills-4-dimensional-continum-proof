# Small reads: central counts on (Z/2)x(Z/2) by my own gauge fixing, and the x-end exclusive links that Remark 4.2 of the lemma names. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *
q8 = Q8_mat()
minus = next(i for i in range(8) if i and q8.tab[i][i] == 0)
lat = Lat(2, 2)
tr = set(lat.tree())
free = [i for i in range(len(lat.links)) if i not in tr]
cfg = [0] * 8
central = negative = 0
for vals in itertools.product(range(8), repeat=len(free)):
    for f, v in zip(free, vals):
        cfg[f] = v
    vs = [hol(q8, cfg, w) for w in lat.words]
    if all(v in (0, minus) for v in vs):
        central += 1
        negative += sum(1 for v in vs if v == minus) % 2
print("IND_ZERO_2x2|gauge_fixed=%d|central=%d|negative_S=%d|orbit=512|central_times_orbit=%d|negative_times_orbit=%d|json=0" % (8 ** 5, central, negative, central * 512, negative * 512))
# Remark 4.2 names U_nu(x) and U_nu(x-nu) as the exclusive links.
for dims in ((2, 2), (2, 3), (3, 3), (2, 2, 2), (2, 2, 3), (2, 3, 3), (2, 2, 2, 2)):
    lat = Lat(*dims)
    bad = 0
    for l, (x, mu) in enumerate(lat.links):
        staples = []
        for w in lat.words:
            if any(a == l for a, _ in w):
                staples.append([a for a, _ in w if a != l])
        for nu in range(lat.k):
            if nu == mu:
                continue
            for site in (x, lat.step(x, nu, -1)):
                e = lat.lid[(site, nu)]
                hits = sum(s.count(e) for s in staples)
                bad += 0 if hits == 1 else 1
    print("IND_REMARK_EXCLUSIVE|lattice=%s|failures=%d|json=0" % ("x".join(map(str, dims)), bad))
