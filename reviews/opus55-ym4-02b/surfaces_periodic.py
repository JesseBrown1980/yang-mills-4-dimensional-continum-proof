# Scope check: on a periodic lattice of side L, which closed face sets of at most LIMIT faces exist? Exact-once branching as in surfaces_exact.py, coordinates mod L.
# Integers only.
import itertools
import sys

sys.setrecursionlimit(100000)
D = int(sys.argv[1])
SIDE = int(sys.argv[2])
LIMIT = int(sys.argv[3])
ORIGIN = (0,) * D
_L = {}
_O = {}


def plus(x, i, s=1):
    y = list(x)
    y[i] = (y[i] + s) % SIDE
    return tuple(y)


def links(f):
    r = _L.get(f)
    if r is None:
        x, mu, nu = f
        r = ((x, mu), (plus(x, mu), nu), (plus(x, nu), mu), (x, nu))
        assert len(set(r)) == 4
        _L[f] = r
    return r


def on_link(l):
    r = _O.get(l)
    if r is None:
        x, m = l
        out = set()
        for n in range(D):
            if n != m:
                a, b = (m, n) if m < n else (n, m)
                out.add((x, a, b))
                out.add((plus(x, n, -1), a, b))
        r = tuple(sorted(out))
        _O[l] = r
    return r


FOUND = []


def rec(T, odd, forb):
    size = len(T)
    if not odd:
        FOUND.append(frozenset(T))
        if size + 4 > LIMIT:
            return
        touch = set()
        for f in T:
            for l in links(f):
                for q in on_link(l):
                    if q not in T and q not in forb:
                        touch.add(q)
        added = []
        for q in sorted(touch):
            T.add(q)
            rec(T, set(links(q)), forb)
            T.discard(q)
            forb.add(q)
            added.append(q)
        for q in added:
            forb.discard(q)
        return
    if size + (len(odd) + 3) // 4 > LIMIT:
        return
    best, bestn = None, 99
    for l in odd:
        n = 0
        for q in on_link(l):
            if q not in T and q not in forb:
                n += 1
        if n < bestn:
            best, bestn = l, n
            if n <= 1:
                break
    if bestn == 0:
        return
    added = []
    for q in on_link(best):
        if q in T or q in forb:
            continue
        T.add(q)
        rec(T, odd.symmetric_difference(links(q)), forb)
        T.discard(q)
        forb.add(q)
        added.append(q)
    for q in added:
        forb.discard(q)


counts = {}
for mu, nu in itertools.combinations(range(D), 2):
    start = (ORIGIN, mu, nu)
    FOUND.clear()
    rec({start}, set(links(start)), set())
    uniq = set(FOUND)
    assert len(uniq) == len(FOUND)
    for S in uniq:
        counts[len(S)] = counts.get(len(S), 0) + 1
# sets holding the origin face, summed over planes, equal (faces per set) x (sets per site) when translations act freely; report the raw sums and F-divided rationals as pairs.
rows = []
for F in sorted(counts):
    rows.append("F%d:anchored=%d,per_site=%d/%d" % (F, counts[F], counts[F], F))
print("PERIODIC|d=%d|side=%d|limit=%d|%s|json=0" % (D, SIDE, LIMIT, "|".join(rows)))
