# E_G[X^k] on small periodic lattices by plaquette multisets: exact group sums against the group-free polynomial integration (haarpoly.py).
# Tests the new proposition (N_p dim(V^G)/2^(t+1)) and the side-1 sentence on lattices the receipts do not hold. Integers only, json=0.
import itertools
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/recheck-4d-20261103/ym4-02b/head/reviews/opus55-ym4-02b")
from grp import build, table  # noqa: E402
import haarpoly  # noqa: E402

sys.setrecursionlimit(10000)


def red(n, d):
    g = math.gcd(n, d) or 1
    if d < 0:
        n, d = -n, -d
    return n // g, d // g


def padd(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def pmul(a, b):
    return red(a[0] * b[0], a[1] * b[1])


class Lat:
    def __init__(self, sides):
        self.sides = sides
        self.dim = len(sides)
        self.sites = list(itertools.product(*[range(s) for s in sides]))
        self.faces = []
        for x in self.sites:
            for mu in range(self.dim):
                for nu in range(mu + 1, self.dim):
                    self.faces.append(((x, mu), (self.shift(x, mu), nu), (self.shift(x, nu), mu), (x, nu)))

    def shift(self, x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % self.sides[mu]
        return tuple(y)


GROUPS = {}


def group(name):
    if name not in GROUPS:
        R, E = build(name)
        mult, inv, _ = table(R, E)
        trace = [e[0] for e in E]
        assert all(t[1] == 0 for t in trace) or name in ("2O", "2I")
        one = E.index(((2, 0), (0, 0), (0, 0), (0, 0)))
        GROUPS[name] = (mult, inv, [t[0] for t in trace], one)
    return GROUPS[name]


def group_expect(lat, plist, name):
    mult, inv, trace, one = group(name)
    links = sorted({l for f in plist for l in f})
    parent = {}

    def find(v):
        parent.setdefault(v, v)
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    forest = set()
    for l in links:
        a, b = find(l[0]), find(lat.shift(l[0], l[1]))
        if a != b:
            parent[a] = b
            forest.add(l)
    free = [l for l in links if l not in forest]
    position = {l: i for i, l in enumerate(free)}
    due = [[] for _ in range(len(free) + 1)]
    for f in plist:
        word = [(position.get(f[0], -1), 1), (position.get(f[1], -1), 1), (position.get(f[2], -1), -1), (position.get(f[3], -1), -1)]
        due[max(i for i, _ in word) + 1].append(word)
    vals = [one] * len(free)
    size = len(mult)

    def walk(depth):
        term = 1
        for word in due[depth]:
            h = one
            for i, s in word:
                if i >= 0:
                    h = mult[h][vals[i] if s > 0 else inv[vals[i]]]
            term *= trace[h]
            if term == 0:
                return 0
        if depth == len(free):
            return term
        total = 0
        for g in range(size):
            vals[depth] = g
            total += walk(depth + 1)
        return term * total
    return red(walk(0), 2 ** len(plist) * size ** len(free))


def haar_expect(plist):
    words = [[(f[0], 1), (f[1], 1), (f[2], -1), (f[3], -1)] for f in plist]
    ids = {}
    out = []
    for w in words:
        out.append([(ids.setdefault(l, len(ids)), s) for l, s in w])
    return haarpoly.expect_words(out)


def canonical(plist):
    ids = {}
    key = []
    for f in plist:
        key.append(tuple(ids.setdefault(l, len(ids)) for l in f))
    return tuple(key)


def moment(lat, k, names):
    np_ = len(lat.faces)
    totals = {n: (0, 1) for n in names}
    memo = {}
    kept = 0
    for combo in itertools.combinations_with_replacement(range(np_), k):
        deg = {}
        for i in combo:
            for l in lat.faces[i]:
                deg[l] = deg.get(l, 0) + 1
        if any(v % 2 for v in deg.values()):
            continue
        kept += 1
        counts = [combo.count(i) for i in sorted(set(combo))]
        mult = math.factorial(k)
        for c in counts:
            mult //= math.factorial(c)
        plist = [lat.faces[i] for i in combo]
        key = canonical(plist)
        if key not in memo:
            memo[key] = {n: (haar_expect(plist) if n == "Haar" else group_expect(lat, plist, n)) for n in names}
        for n in names:
            totals[n] = padd(totals[n], pmul((mult, 1), memo[key][n]))
    return totals, kept, len(memo), np_


for arg in sys.argv[1:]:
    sides_text, kmax_text, names_text = arg.split(":")
    sides = tuple(int(v) for v in sides_text.split("x"))
    names = names_text.split(",")
    lat = Lat(sides)
    for k in range(1, int(kmax_text) + 1):
        totals, kept, classes, np_ = moment(lat, k, names)
        row = "|".join("%s=%d/%d" % ((n,) + totals[n]) for n in names)
        print("MOMENT|sides=%s|N_p=%d|k=%d|kept=%d|patterns=%d|%s|json=0" % (sides_text, np_, k, kept, classes, row))
        sys.stdout.flush()
print("MULTISET_DONE|json=0")
