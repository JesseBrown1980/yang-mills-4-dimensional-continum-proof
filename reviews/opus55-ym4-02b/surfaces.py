# Claim 4: closed mod-2 plaquette sets on Z^d by two algorithms that share no code with the script:
#  G: growth anchored at an origin face, branching on the LARGEST odd link (the script uses the smallest), and CONTINUING past a closed set, so sets holding a smaller closed set are reached.
#  C: boundaries of face-connected sets of 3-cubes (mod 2), by a different route altogether, plus pairs of cubes that touch without sharing a face.
# Integers only.
import itertools
import sys

sys.setrecursionlimit(10000)


def e(d, i, s=1):
    v = [0] * d
    v[i] = s
    return tuple(v)


def plus(x, y):
    return tuple(a + b for a, b in zip(x, y))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def face_links(d, f):
    x, mu, nu = f
    return (
        (x, mu),
        (plus(x, e(d, mu)), nu),
        (plus(x, e(d, nu)), mu),
        (x, nu),
    )


def faces_on(d, l):
    x, m = l
    out = []
    for n in range(d):
        if n == m:
            continue
        a, b = (m, n) if m < n else (n, m)
        out.append((x, a, b))
        out.append((minus(x, e(d, n)), a, b))
    return out


def grow_all(d, limit):
    """All link-connected closed sets of distinct faces holding a given origin face, for each plane: every such set is found exactly once per anchor plane."""
    results = {}
    origin = (0,) * d
    nodes = 0
    for mu, nu in itertools.combinations(range(d), 2):
        start = (origin, mu, nu)
        visited = set()
        found = set()
        stack = [(frozenset((start,)), frozenset(face_links(d, start)))]
        while stack:
            faces, odd = stack.pop()
            if faces in visited:
                continue
            visited.add(faces)
            nodes += 1
            size = len(faces)
            if not odd:
                found.add(faces)
                # continue past a closed set: any extension must add a further closed set, which has at least 4 faces (6 on Z^d, and we do not assume it).
                if size + 1 > limit:
                    continue
                cover = set()
                for f in faces:
                    cover.update(face_links(d, f))
                for l in cover:
                    for q in faces_on(d, l):
                        if q not in faces:
                            stack.append((faces | {q}, frozenset(face_links(d, q))))
                continue
            # lower bound: each new face covers at most four odd links
            if size + (len(odd) + 3) // 4 > limit:
                continue
            l = max(odd)
            for q in faces_on(d, l):
                if q not in faces:
                    stack.append((faces | {q}, odd ^ frozenset(face_links(d, q))))
        results[(mu, nu)] = found
    return results, nodes


def canon(faces):
    """Translation-canonical form."""
    d = len(next(iter(faces))[0])
    lo = [min(f[0][i] for f in faces) for i in range(d)]
    return tuple(sorted((tuple(f[0][i] - lo[i] for i in range(d)), f[1], f[2]) for f in faces))


def describe(d, faces):
    faces = list(faces)
    cover = {}
    for f in faces:
        for l in face_links(d, f):
            cover[l] = cover.get(l, 0) + 1
    links = set(cover)
    sites = set()
    for l in links:
        sites.add(l[0])
        sites.add(plus(l[0], e(d, l[1])))
    chi = len(sites) - len(links) + len(faces)
    spans = {dd for f in faces for dd in f[1:]}
    return {
        "F": len(faces),
        "chi": chi,
        "maxcover": max(cover.values()),
        "mincover": min(cover.values()),
        "spans": len(spans),
        "sites": len(sites),
        "links": len(links),
    }


def tally_growth(d, limit):
    res, nodes = grow_all(d, limit)
    counts = {}
    classes = {}
    for plane, found in res.items():
        for faces in found:
            F = len(faces)
            counts[F] = counts.get(F, 0) + 1
            classes.setdefault(canon(faces), None)
    per_site = {}
    for F, c in counts.items():
        assert c % F == 0, (F, c)
        per_site[F] = c // F
    # translation classes must equal per-site counts
    by_F = {}
    for k in classes:
        by_F[len(k)] = by_F.get(len(k), 0) + 1
    assert by_F == per_site, (by_F, per_site)
    return per_site, classes, nodes


# ---- Second algorithm: 3-chains.
def cube_faces(d, c):
    x, dirs = c  # dirs is a sorted triple
    out = []
    for third in dirs:
        a, b = [t for t in dirs if t != third]
        out.append((x, a, b))
        out.append((plus(x, e(d, third)), a, b))
    return frozenset(out)


def cubes_on_face(d, f):
    x, a, b = f
    out = []
    for c in range(d):
        if c in (a, b):
            continue
        dirs = tuple(sorted((a, b, c)))
        out.append((x, dirs))
        out.append((minus(x, e(d, c)), dirs))
    return out


def chain_boundaries(d, K, maxF):
    """Boundaries of face-connected sets of at most K cubes, up to translation, keeping weight <= maxF."""
    origin = (0,) * d
    seen = set()
    frontier = []
    for dirs in itertools.combinations(range(d), 3):
        c = (origin, dirs)
        frontier.append(frozenset((c,)))
    boundaries = {}
    animals = 0
    for k in range(1, K + 1):
        nxt = set()
        for A in frontier:
            lo = None
            b = frozenset()
            for c in A:
                b = b ^ cube_faces(d, c)
            animals += 1
            if b and len(b) <= maxF:
                boundaries.setdefault(canon(b), set()).add(k)
            if k == K:
                continue
            for c in A:
                for f in cube_faces(d, c):
                    for c2 in cubes_on_face(d, f):
                        if c2 not in A:
                            B = set(A)
                            B.add(c2)
                            # translation canonical animal
                            lo = [min(cc[0][i] for cc in B) for i in range(d)]
                            nxt.add(frozenset((tuple(cc[0][i] - lo[i] for i in range(d)), cc[1]) for cc in B))
        frontier = nxt
    return boundaries, animals


def touching_pairs(d):
    """Pairs of unit cubes with no shared face whose boundaries share at least one link (these are link-connected closed sets of 12 faces), and pairs sharing only a site."""
    origin = (0,) * d
    link_pairs, site_pairs = set(), set()
    allc = []
    for dirs in itertools.combinations(range(d), 3):
        allc.append((origin, dirs))
    rng = range(-1, 2)
    for c1 in allc:
        f1 = cube_faces(d, c1)
        l1 = {l for f in f1 for l in face_links(d, f)}
        s1 = {x for l in l1 for x in (l[0], plus(l[0], e(d, l[1])))}
        for off in itertools.product(rng, repeat=d):
            for dirs in itertools.combinations(range(d), 3):
                c2 = (off, dirs)
                if c2 == c1:
                    continue
                f2 = cube_faces(d, c2)
                if f1 & f2:
                    continue
                l2 = {l for f in f2 for l in face_links(d, f)}
                s2 = {x for l in l2 for x in (l[0], plus(l[0], e(d, l[1])))}
                if l1 & l2:
                    link_pairs.add(canon(f1 | f2))
                elif s1 & s2:
                    site_pairs.add(canon(f1 | f2))
    return link_pairs, site_pairs


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for d in (3, 4):
        per_site, classes, nodes = tally_growth(d, limit)
        print("GROWTH|d=%d|limit=%d|states_visited=%d|per_site=%s|json=0" % (d, limit, nodes, dict(sorted(per_site.items()))))
        table = {}
        for k in classes:
            info = describe(d, k)
            key = (info["F"], info["spans"], info["chi"], info["maxcover"], info["sites"], info["links"])
            table[key] = table.get(key, 0) + 1
        for key, c in sorted(table.items()):
            print("GROWTH_SHAPE|d=%d|F=%d|spans=%d|chi=%d|maxcover=%d|sites=%d|links=%d|per_site=%d|json=0" % ((d,) + key + (c,)))
        K = 6 if d == 3 else 5
        boundaries, animals = chain_boundaries(d, K, max(limit, 12))
        byF = {}
        for k, ks in boundaries.items():
            byF[len(k)] = byF.get(len(k), 0) + 1
        print("CHAINS|d=%d|K=%d|animals=%d|distinct_boundaries_per_site=%s|json=0" % (d, K, animals, dict(sorted(byF.items()))))
        lp, sp = touching_pairs(d)
        print("TOUCHING_PAIRS|d=%d|share_link_only_per_site=%d|share_site_only_per_site=%d|json=0" % (d, len(lp), len(sp)))
        # comparison at every F through the limit
        for F in sorted(set(per_site) | {len(k) for k in boundaries}):
            if F > limit:
                continue
            g = {k for k in classes if len(k) == F}
            c = {k for k in boundaries if len(k) == F}
            extra_pairs = {k for k in lp if len(k) == F}
            only_g = g - c - extra_pairs
            only_c = c - g
            print("COMPARE|d=%d|F=%d|growth=%d|chains=%d|link_pairs=%d|only_growth=%d|only_chains=%d|json=0" % (d, F, len(g), len(c), len(extra_pairs), len(only_g), len(only_c)))
            for k in list(only_g)[:3]:
                print("ONLY_GROWTH_EXAMPLE|%s" % (k,))
            for k in list(only_c)[:3]:
                print("ONLY_CHAINS_EXAMPLE|%s" % (k,))
    print("SURFACES_DONE|json=0")
