# Cube identity by free reduction, bipartite parity by F2 linear algebra, staple structure by direct listing. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import *


# ---- Part 1: the cube identity in the free group on the 12 edges.
# Vertices are bit triples, an edge is (v, axis) from v to v + axis.
def edge(v, axis):
    return (v, axis)


def flip(v, axis):
    w = list(v)
    w[axis] ^= 1
    return tuple(w)


def path_word(v, axes):
    """The word along a walk from v. Each step flips one axis: forward if the bit is 0, backward if 1."""
    word = []
    cur = v
    for a in axes:
        if cur[a] == 0:
            word.append((edge(cur, a), 1))
        else:
            word.append((edge(flip(cur, a), a), -1))
        cur = flip(cur, a)
    return word, cur


def reduce_free(word):
    out = []
    for letter in word:
        if out and out[-1][0] == letter[0] and out[-1][1] == -letter[1]:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word):
    return [(l, -e) for l, e in reversed(word)]


O = (0, 0, 0)
# Each face as a loop at its own corner, with a connector from O to that corner.
faces = {}
faces["z0"] = (((), (0, 1, 0, 1)))
faces["y0"] = (((), (0, 2, 0, 2)))
faces["x0"] = (((), (1, 2, 1, 2)))
faces["x1"] = (((0,), (1, 2, 1, 2)))
faces["y1"] = (((1,), (0, 2, 0, 2)))
faces["z1"] = (((2,), (0, 1, 0, 1)))


def lasso(name, inverted):
    conn, loop = faces[name]
    c, corner = path_word(O, conn)
    l, end = path_word(corner, loop)
    assert end == corner
    if inverted:
        l = inverse_word(l)
    return c + l + inverse_word(c)


names = sorted(faces)
found = []
for order in itertools.permutations(names):
    for bits in itertools.product((0, 1), repeat=5):
        # first letter fixed up to overall inversion
        signs = (0,) + bits
        word = []
        for n, b in zip(order, signs):
            word.extend(lasso(n, b))
        if not reduce_free(word):
            found.append((order, signs))
print("IND_CUBE_FREE|orderings_tested=%d|orderings_reducing_to_the_empty_word=%d|first=%s|json=0" % (720 * 32, len(found), (found[0][0], found[0][1]) if found else "none"))


# ---- Part 2: the F2 geometry of cubes and faces.
def cube_face_matrix(dims):
    lat = Lat(*dims)
    index = {p: i for i, p in enumerate(lat.plaq)}
    rows = []
    for x in lat.sites:
        r = 0
        for mu, nu, rho in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            r ^= 1 << index[(x, mu, nu)]
            r ^= 1 << index[(lat.step(x, rho), mu, nu)]
        rows.append(r)
    return lat, rows


def in_row_space(rows, v):
    basis = {}
    for r in rows:
        while r:
            b = r.bit_length() - 1
            if b in basis:
                r ^= basis[b]
            else:
                basis[b] = r
                break
    while v:
        b = v.bit_length() - 1
        if b in basis:
            v ^= basis[b]
        else:
            return False, len(basis)
    return True, len(basis)


for dims in ((2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3), (2, 2, 4), (2, 4, 4), (4, 4, 4), (1, 2, 2), (1, 1, 2), (1, 1, 1), (1, 2, 3), (1, 1, 3), (2, 2, 5)):
    lat, rows = cube_face_matrix(dims)
    F = len(lat.plaq)
    ones = (1 << F) - 1
    inside, rank = in_row_space(rows, ones)
    all_even = all(d % 2 == 0 for d in dims)
    # every Z/2 cycle (kernel of the cube matrix) has even weight exactly when the all-ones vector lies in the row space
    print("IND_CYCLE_PARITY|lattice=%s|faces=%d|cubes=%d|rank=%d|Z/2_cycles=2^%d|every_cycle_even=%d|every_side_even=%d|json=0" % ("x".join(map(str, dims)), F, len(rows), rank, F - rank, 1 if inside else 0, 1 if all_even else 0))


# ---- Part 3: staples. For each link of each lattice, list the staples and test the note's exclusive links and joint uniformity.
def staples(lat, l):
    """For link l, each plaquette holding it, walked so that it starts with l forward: returns (plaquette index, staple word)."""
    out = []
    for pi, w in enumerate(lat.words):
        positions = [i for i, (a, e) in enumerate(w) if a == l]
        for i in positions:
            e = w[i][1]
            cyc = list(w[i:]) + list(w[:i])
            if e < 0:
                cyc = inverse_word(list(w))
                j = [t for t, (a, _) in enumerate(cyc) if a == l and cyc[t][1] > 0][0]
                cyc = cyc[j:] + cyc[:j]
            out.append((pi, cyc[1:]))
    return out


def transverse_exclusive_ok(lat):
    """Reads the note's named links. Returns the counts over all links."""
    bad_named, bad_once = 0, 0
    for l, (x, mu) in enumerate(lat.links):
        sts = staples(lat, l)
        if len(sts) != 2 * (lat.k - 1):
            bad_once += 1
        if len({p for p, _ in sts}) != len(sts):
            bad_once += 1
        named = []
        for nu in range(lat.k):
            if nu == mu:
                continue
            ep = lat.lid[(lat.step(x, mu), nu)]
            em = lat.lid[(lat.step(lat.step(x, mu), nu, -1), nu)]
            named.append((nu, 1, ep))
            named.append((nu, -1, em))
        if len({e for _, _, e in named}) != len(named):
            bad_named += 1
            continue
        # each named link must sit in exactly one staple, once
        for _, _, e in named:
            hits = sum(sum(1 for a, _ in st if a == e) for _, st in sts)
            if hits != 1:
                bad_named += 1
    return bad_once, bad_named


for dims in ((2, 2), (2, 3), (3, 2), (3, 3), (2, 4), (2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3), (2, 2, 2, 2), (2, 1), (1, 2), (2, 1, 2), (3, 1)):
    lat = Lat(*dims)
    a, b = transverse_exclusive_ok(lat)
    print("IND_STAPLES|lattice=%s|links=%d|links_with_a_wrong_count_of_distinct_plaquettes=%d|named_link_failures=%d|json=0" % ("x".join(map(str, dims)), len(lat.links), a, b))


def staple_value(G, cfg, st):
    h = 0
    for l, e in st:
        v = cfg[l]
        h = G.tab[h][v if e > 0 else G.inv[v]]
    return h


def uniform_check(G, dims):
    """Exhaustive over the links the staples hold, for every link: is the tuple uniform on G^r?"""
    lat = Lat(*dims)
    worst = 0
    for l in range(len(lat.links)):
        sts = staples(lat, l)
        held = sorted({a for _, st in sts for a, _ in st})
        cfg = [0] * len(lat.links)
        counts = {}
        for vals in itertools.product(range(G.n), repeat=len(held)):
            for h, v in zip(held, vals):
                cfg[h] = v
            key = tuple(staple_value(G, cfg, st) for _, st in sts)
            counts[key] = counts.get(key, 0) + 1
        r = len(sts)
        expected_cells = G.n ** r
        expected_each = G.n ** len(held) // expected_cells
        ok = len(counts) == expected_cells and all(c == expected_each for c in counts.values())
        if not ok:
            worst += 1
    return worst, len(lat.links)


z3, s3, q8 = cyclic(3), S(3), Q8_mat()
for G, dims in ((s3, (2, 2)), (q8, (2, 2)), (z3, (2, 2)), (s3, (2, 3)), (z3, (2, 2, 2)), (z3, (2, 3)), (q8, (2, 3)), (s3, (2, 1)), (q8, (2, 1)), (q8, (3, 1))):
    bad, total = uniform_check(G, dims)
    print("IND_STAPLE_UNIFORM|group=%s|lattice=%s|links=%d|links_with_a_nonuniform_staple_tuple=%d|json=0" % (G.name, "x".join(map(str, dims)), total, bad))
    sys.stdout.flush()


# ---- Part 4: Steps 6, 7, 8 read on finite groups. kappa(h) |G| = sum_v s(v) s(v h). For every pattern: all |kappa| = 1 exactly when the pattern is on the rule, and kappa is then +- the hom.
def step678(G):
    good = 0
    agree = True
    for mask in range(1 << G.nmc):
        s = [1 - 2 * ((mask >> G.mc_of[i]) & 1) for i in range(G.n)]
        kappas = [sum(s[v] * s[G.tab[v][h]] for v in range(G.n)) for h in range(G.n)]
        all_unit = all(abs(k) == G.n for k in kappas)
        on_rule = mask in G.rule
        if all_unit != on_rule:
            agree = False
        if all_unit:
            good += 1
            # kappa/|G| is a homomorphism, and s = eps kappa
            kap = [k // G.n for k in kappas]
            hom = all(kap[G.tab[a][b]] == kap[a] * kap[b] for a in range(G.n) for b in range(G.n))
            eps = {s[i] * kap[i] for i in range(G.n)}
            if not hom or len(eps) != 1:
                agree = False
    return good, agree


for G in (cyclic(2), cyclic(3), cyclic(4), cyclic(6), s3, D(4), q8, D(5), A4(), Dic3(), F21(), S(4), SL23(), TwoO(), A5(), SL25()):
    good, agree = step678(G)
    print("IND_STEP678|group=%s|patterns=%d|patterns_with_all_abs_kappa_1=%d|rule=%d|agree_with_rule_and_s=eps_kappa=%d|json=0" % (G.name, 1 << G.nmc, good, len(G.rule), 1 if agree else 0))
    sys.stdout.flush()
print("IND_CUBE_DONE|json=0")
