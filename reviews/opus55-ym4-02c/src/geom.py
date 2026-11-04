#!/usr/bin/env python3
"""Second seat: the reflection derived from the universal cover, with no use of the rule c-t-1, the plaquette map or the declared partition of the builder.
Lattice (Z/L_1)x...x(Z/L_k)x(Z/T). A site of the cover is a tuple in Z^d. A directed edge of the cover is carried to the edge between the image sites.
Standard library, integers only, json=0."""
import itertools
import random
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import rat, radd, rmul


def reduce_site(a, dims):
    return tuple(v % n for v, n in zip(a, dims))


def edge_label(a, b, dims):
    """Edge of the cover from a to b, adjacent. Returns (link, sign) where link = (reduced base, direction)."""
    diff = [q - p for p, q in zip(a, b)]
    assert sorted(abs(v) for v in diff)[-1] == 1 and sum(abs(v) for v in diff) == 1
    mu = next(i for i, v in enumerate(diff) if v)
    if diff[mu] == 1:
        return (reduce_site(a, dims), mu), 1
    return (reduce_site(b, dims), mu), -1


def theta_cover(a, c):
    return a[:-1] + (c - a[-1],)


def path_of_plaquette(x, mu, nu):
    """Corners in the cover, in the repository's order: x, x+mu, x+mu+nu, x+nu."""
    e = lambda i: tuple(1 if j == i else 0 for j in range(len(x)))
    add = lambda p, q: tuple(u + v for u, v in zip(p, q))
    return [x, add(x, e(mu)), add(add(x, e(mu)), e(nu)), add(x, e(nu))]


def word(path, dims):
    return tuple(edge_label(path[i], path[(i + 1) % 4], dims) for i in range(4))


def rot(w):
    return [w[i:] + w[:i] for i in range(4)]


def rev(w):
    return tuple((l, -s) for l, s in reversed(w))


def qm(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return (a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n)


def qi(p):
    return (p[0], -p[1], -p[2], -p[3], p[4])


UNITS = [(1, 0, 0, 0, 1), (1, 2, 2, 4, 5), (1, 2, 4, 2, 5), (2, 4, 1, 2, 5), (1, 1, 1, 1, 2), (1, -1, 1, -1, 2), (1, 2, 2, 0, 3), (2, -1, 0, 2, 3), (2, 3, 6, 0, 7), (6, 2, 0, -3, 7), (9, 2, 6, 6, 13), (5, 12, 0, 0, 13)]


def half_trace(w, field):
    h = (1, 0, 0, 0, 1)
    for l, s in w:
        h = qm(h, field[l] if s > 0 else qi(field[l]))
    return rat(h[0], h[4])


def run(dims, kind, seed):
    T = dims[-1]
    m = T // 2
    c = 0 if kind == "site" else -1
    d = len(dims)
    sites = list(itertools.product(*[range(n) for n in dims]))
    links = [(s, mu) for s in sites for mu in range(d)]
    plaq = [(s, mu, nu) for s in sites for mu in range(d) for nu in range(mu + 1, d)]
    words = {p: word(path_of_plaquette(*p), dims) for p in plaq}
    lookup = {}
    for p, w in words.items():
        for r in rot(w):
            lookup.setdefault(r, []).append((p, 1))
        for r in rot(rev(w)):
            lookup.setdefault(r, []).append((p, -1))
    # The image of each plaquette from the cover alone.
    image = {}
    same = bad = 0
    for p in plaq:
        path = [theta_cover(a, c) for a in path_of_plaquette(*p)]
        w = word(path, dims)
        hits = lookup.get(w, [])
        if not hits:
            bad += 1
            continue
        # Degenerate side-1 plaquettes may match both orientations. Keep the set.
        image[p] = hits
    assert bad == 0
    # Regions from the cover. A plaquette's corners have t in [t0, t0+1] for time-like and t0 for spatial, with t0 in [0, T).
    def region(p):
        s, mu, nu = p
        t0 = s[-1]
        timelike = nu == d - 1
        if kind == "link":
            if timelike:
                if t0 == m - 1 or t0 == T - 1:
                    return "shared"
                return "upper" if t0 + 1 <= m - 1 else "lower"
            return "upper" if t0 <= m - 1 else "lower"
        if timelike:
            return "upper" if t0 + 1 <= m else "lower"
        if t0 in (0, m):
            return "shared"
        return "upper" if t0 < m else "lower"
    regions = {p: region(p) for p in plaq}
    counts = {r: sum(1 for p in plaq if regions[p] == r) for r in ("upper", "shared", "lower")}
    mirror_ok = True
    shared_self = True
    shared_reversed = 0
    for p in plaq:
        targets = [q for q, _ in image[p]]
        if regions[p] == "shared":
            shared_self = shared_self and p in targets
            if any(q == p and o == -1 for q, o in image[p]):
                shared_reversed += 1
        elif regions[p] == "upper":
            mirror_ok = mirror_ok and all(regions[q] == "lower" for q in targets)
        else:
            mirror_ok = mirror_ok and all(regions[q] == "upper" for q in targets)
    # The reflected field from the cover: (theta U)(e) = U(theta e).
    rng = random.Random(seed + sum(dims) * 101)
    field = {l: UNITS[rng.randrange(len(UNITS))] for l in links}
    reflected = {}
    for (s, mu) in links:
        a = s
        b = tuple(v + (1 if i == mu else 0) for i, v in enumerate(s))
        (lab, sg) = edge_label(theta_cover(a, c), theta_cover(b, c), dims)
        reflected[(s, mu)] = field[lab] if sg > 0 else qi(field[lab])
    # a_p(theta U) = a_(theta p)(U), using the image from the geometry.
    identity = True
    for p in plaq:
        v = half_trace(words[p], reflected)
        identity = identity and all(half_trace(words[q], field) == v for q, _ in image[p])
    # Action split, with half weights on fixed plaquettes for site reflection.
    def deficit(names, f):
        tot = (0, 1)
        for p in names:
            tr = half_trace(words[p], f)
            tot = radd(tot, rat(tr[1] - tr[0], tr[1]))
        return tot
    up = [p for p in plaq if regions[p] == "upper"]
    sh = [p for p in plaq if regions[p] == "shared"]
    total = deficit(plaq, field)
    if kind == "site":
        split = radd(radd(deficit(up, field), deficit(up, reflected)), rmul((1, 2), radd(deficit(sh, field), deficit(sh, reflected))))
    else:
        split = radd(radd(deficit(up, field), deficit(up, reflected)), deficit(sh, field))
    # Links of the halves.
    lk = lambda names: {l for p in names for l, _ in words[p]}
    lo = [p for p in plaq if regions[p] == "lower"]
    if kind == "site":
        fixed_links = {(s, mu) for (s, mu) in links if mu != d - 1 and s[-1] in (0, m)}
        support = lk(up + sh) & lk(lo + sh) == fixed_links
    else:
        crossing_links = {(s, mu) for (s, mu) in links if mu == d - 1 and s[-1] in (m - 1, T - 1)}
        support = not (lk(up) & lk(lo)) and not (lk(up) & crossing_links) and not (lk(lo) & crossing_links)
    exclusive = 0
    commutators = 0
    for p, w in words.items():
        tally = {}
        for l, _ in w:
            tally[l] = tally.get(l, 0) + 1
        if any(v == 1 for v in tally.values()):
            exclusive += 1
        else:
            commutators += 1
    return (len(plaq), counts, mirror_ok, shared_self, shared_reversed, identity, total == split, support, exclusive, commutators)


def main():
    cases = [(2, 2, 2, 2), (2, 2, 2, 4), (3, 3, 3, 4), (1, 1, 1, 2), (1, 1, 1, 4), (3, 3, 3, 2), (2, 2, 2, 6), (1, 2, 3, 4), (3, 2, 1, 2), (3, 2), (1, 2), (1, 4), (1, 1, 2), (2, 1, 2), (1, 1, 1, 6), (4, 4, 4, 2)]
    for dims in cases:
        for kind in ("link", "site"):
            for seed in (11, 23, 57):
                total, counts, mirror, shared_self, rev_count, identity, split, support, exclusive, comm = run(dims, kind, seed)
                if seed != 11 and identity and split:
                    continue
                k = len(dims) - 1
                prod = 1
                for n in dims[:-1]:
                    prod *= n
                rule_total = (k * (k + 1) // 2) * prod * dims[-1]
                rule_shared = (2 * k * prod) if kind == "link" else (2 * (k * (k - 1) // 2) * prod)
                print("GEOM|dims=%s|kind=%s|total=%d|shared=%d|upper=%d|lower=%d|rule_total=%d|rule_shared=%d|mirror=%d|shared_fixed=%d|shared_reversed=%d|a_identity=%d|split=%d|support=%d|plaquettes_with_exclusive_link=%d|commutators=%d|json=0" % (
                    "x".join(map(str, dims)), kind, total, counts["shared"], counts["upper"], counts["lower"], rule_total, rule_shared, mirror, shared_self, rev_count, identity, split, support, exclusive, comm), flush=True)


main()
