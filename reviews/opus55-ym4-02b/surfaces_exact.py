# Third algorithm for closed mod-2 face sets: exact-once enumeration by "first option in S" branching with a forbidden set, no visited table, low memory.
# For a target closed set S holding the anchor: at an odd link, S must hold an option through it; branch on which option comes first in S and forbid the earlier ones.
# When the current set T is closed, record it; S may still be larger, in which case S\T holds a face touching T; branch the same way over all faces touching T.
# Integers only.
import itertools
import sys

sys.setrecursionlimit(100000)
D = int(sys.argv[1])
LIMIT = int(sys.argv[2])
ORIGIN = (0,) * D
_L = {}
_O = {}


def unit(i, s=1):
    v = [0] * D
    v[i] = s
    return tuple(v)


UNIT = [unit(i) for i in range(D)]
MINUS = [unit(i, -1) for i in range(D)]


def plus(x, y):
    return tuple(a + b for a, b in zip(x, y))


def links(f):
    r = _L.get(f)
    if r is None:
        x, mu, nu = f
        r = ((x, mu), (plus(x, UNIT[mu]), nu), (plus(x, UNIT[nu]), mu), (x, nu))
        _L[f] = r
    return r


def on_link(l):
    r = _O.get(l)
    if r is None:
        x, m = l
        out = []
        for n in range(D):
            if n != m:
                a, b = (m, n) if m < n else (n, m)
                out.append((x, a, b))
                out.append((plus(x, MINUS[n]), a, b))
        out.sort()
        r = tuple(out)
        _O[l] = r
    return r


FOUND = []
nodes = [0]


def rec(T, odd, forb):
    nodes[0] += 1
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
    # branch on the odd link with the fewest open options
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


def canon(faces):
    lo = [min(f[0][i] for f in faces) for i in range(D)]
    return tuple(sorted((tuple(f[0][i] - lo[i] for i in range(D)), f[1], f[2]) for f in faces))


counts = {}
classes = {}
for mu, nu in itertools.combinations(range(D), 2):
    start = (ORIGIN, mu, nu)
    FOUND.clear()
    rec({start}, set(links(start)), set())
    uniq = set(FOUND)
    assert len(uniq) == len(FOUND), ("duplicates", len(uniq), len(FOUND))
    for S in uniq:
        counts[len(S)] = counts.get(len(S), 0) + 1
        classes[canon(S)] = 1
per_site = {}
for F, c in counts.items():
    assert c % F == 0, (F, c)
    per_site[F] = c // F
byF = {}
for k in classes:
    byF[len(k)] = byF.get(len(k), 0) + 1
assert byF == per_site, (byF, per_site)
print("EXACT_ONCE|d=%d|limit=%d|nodes=%d|per_site=%s|json=0" % (D, LIMIT, nodes[0], dict(sorted(per_site.items()))))
with open("classes_d%d_F%d.txt" % (D, LIMIT), "w", encoding="utf8") as out:
    for k in sorted(classes, key=lambda z: (len(z), z)):
        out.write(repr(k) + "\n")
print("WROTE|classes_d%d_F%d.txt|n=%d|json=0" % (D, LIMIT, len(classes)))
