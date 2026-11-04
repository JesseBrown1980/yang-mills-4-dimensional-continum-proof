# Does the hypothesis "four distinct links per plaquette" mark the exact edge, and does a side of length 1 always give floor(t/2)?
# Exact group sums on periodic lattices with mixed sides, in the ring of each group. Integers only, json=0.
import itertools
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/recheck-4d-20261103/ym4-02b/head/reviews/opus55-ym4-02b")
from grp import build, table  # noqa: E402


def red(n, d):
    g = math.gcd(n, d) or 1
    return n // g, d // g


def lattice(sides):
    dim = len(sides)
    sites = list(itertools.product(*[range(s) for s in sides]))

    def shift(x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % sides[mu]
        return tuple(y)
    faces = []
    for x in sites:
        for mu in range(dim):
            for nu in range(mu + 1, dim):
                faces.append(((x, mu), (shift(x, mu), nu), (shift(x, nu), mu), (x, nu)))
    return sites, shift, faces


def words(sides):
    sites, shift, faces = lattice(sides)
    links = sorted({l for f in faces for l in f})
    # spanning forest: only links in it are fixed to the unit, which leaves every plaquette trace distribution unchanged.
    parent = {x: x for x in sites}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    forest = set()
    for l in links:
        a, b = find(l[0]), find(shift(l[0], l[1]))
        if a != b:
            parent[a] = b
            forest.add(l)
    free = [l for l in links if l not in forest]
    position = {l: i for i, l in enumerate(free)}
    out = []
    for f in faces:
        out.append([(position.get(f[0], -1), 1), (position.get(f[1], -1), 1), (position.get(f[2], -1), -1), (position.get(f[3], -1), -1)])
    return free, out, faces


def histogram(sides, name):
    R, E = build(name)
    mult, inv, _ = table(R, E)
    trace = [e[0] for e in E]
    free, ws, faces = words(sides)
    n = len(E)
    hist = {}
    vals = [0] * len(free)
    onei = E.index(((2, 0), (0, 0), (0, 0), (0, 0)))
    for config in itertools.product(range(n), repeat=len(free)):
        total = (0, 0)
        for w in ws:
            h = onei
            for i, s in w:
                if i >= 0:
                    g = config[i]
                    h = mult[h][g if s > 0 else inv[g]]
            t = trace[h]
            total = (total[0] + t[0], total[1] + t[1])
        hist[total] = hist.get(total, 0) + 1
    return R, hist, n ** len(free), len(free), len(faces)


def moments(R, hist, configs, kmax):
    out = {}
    for k in range(0, kmax + 1):
        s = (0, 0)
        for x, c in hist.items():
            v = (1, 0)
            for _ in range(k):
                v = R(v, x)
            s = (s[0] + c * v[0], s[1] + c * v[1])
        assert s[1] == 0, (k, s)
        out[k] = red(s[0], configs * 2 ** k)
    return out


T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}
spec = []
for a in sys.argv[1:]:
    sides_text, kmax_text, groups_text = a.split(":")
    spec.append((tuple(int(v) for v in sides_text.split("x")), int(kmax_text), groups_text.split(",")))
for sides, kmax, groups in spec:
    res = {}
    for name in groups:
        R, hist, configs, nfree, np_ = histogram(sides, name)
        res[name] = moments(R, hist, configs, kmax)
        row = "|".join("E_X%d=%d/%d" % ((k,) + res[name][k]) for k in range(1, kmax + 1))
        print("MIXED|sides=%s|group=%s|free_links=%d|N_p=%d|%s|json=0" % ("x".join(map(str, sides)), name, nfree, np_, row))
        sys.stdout.flush()
    truth = groups[-1]
    for name in groups[:-1]:
        first = next((k for k in range(1, kmax + 1) if res[name][k] != res[truth][k]), None)
        print("MIXED_FIRST_DIFF|sides=%s|group=%s|t=%d|floor_t_over_2=%d|against=%s|agrees_through_k=%s|json=0" % ("x".join(map(str, sides)), name, T[name], T[name] // 2, truth, (first - 1) if first else ">=%d" % kmax))
print("MIXED_DONE|json=0")
