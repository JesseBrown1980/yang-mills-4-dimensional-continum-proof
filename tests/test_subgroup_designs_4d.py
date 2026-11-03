#!/usr/bin/env python3
"""YM4-02b: finite subgroups of SU(2) average exactly as Haar through a fixed degree per link.

The average over a finite G in SU(2) equals the Haar integral for every polynomial of degree <= t on S^3, where t+1 is
the first n >= 1 at which G has an invariant on the spin-n/2 representation. Integrating links one at a time carries this
to any lattice observable of degree <= t in each link, on a lattice whose plaquettes hold four distinct links. This script builds
Q8, 2T, 2O and 2I, measures t, then uses Q8 and 2T as exact integrators on the 4D Wilson lattice, and compares the plaquette
series with the published table.

usage = test_subgroup_designs_4d.py [sabotage=NAME]
NAME is one of bad_group wrong_class wrong_table drop_direction drop_bent q8_everywhere, and each must exit 1.
Python standard library, integers only, json=0.
"""
import itertools
import math
import sys
from random import Random

SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage="):
        raise SystemExit("usage = test_subgroup_designs_4d.py [sabotage=NAME]")
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []


def check(name, ok):
    if not ok:
        FAILS.append(name)


# ---- Exact rationals as reduced integer pairs.
def red(n, d=1):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d) or 1
    return n // g, d // g


def padd(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def psub(a, b):
    return red(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def pmul(a, b):
    return red(a[0] * b[0], a[1] * b[1])


def text(a):
    return "%d" % a[0] if a[1] == 1 else "%d/%d" % a


# ---- 1. The four groups, built from doubled unit quaternions over Z, Z[sqrt 2] and Z[phi]. A coordinate (a, b) means a + b w with w^2 = p w + q.
def ring(p, q):
    def times(x, y):
        a, b = x
        c, d = y
        return a * c + b * d * q, a * d + b * c + b * d * p
    return times


Z, ROOT2, PHI = ring(0, 0), ring(0, 2), ring(1, 1)


def rplus(x, y):
    return x[0] + y[0], x[1] + y[1]


def rminus(x, y):
    return x[0] - y[0], x[1] - y[1]


def product(times, p, q):
    # (doubled p)(doubled q) = 4 p q, so the doubled product is half of it.
    a, b, c, d = p
    e, f, g, h = q
    r = (rminus(rminus(rminus(times(a, e), times(b, f)), times(c, g)), times(d, h)),
         rminus(rplus(rplus(times(a, f), times(b, e)), times(c, h)), times(d, g)),
         rplus(rplus(rminus(times(a, g), times(b, h)), times(c, e)), times(d, f)),
         rplus(rminus(rplus(times(a, h), times(b, g)), times(c, f)), times(d, e)))
    assert all(v[0] % 2 == 0 and v[1] % 2 == 0 for v in r)
    return tuple((v[0] // 2, v[1] // 2) for v in r)


def ints(*values):
    return tuple((v, 0) for v in values)


def even_permutations(values):
    for perm in itertools.permutations(range(4)):
        if sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j]) % 2 == 0:
            yield tuple(values[perm[i]] for i in range(4))


Q8_ELEMENTS = [ints(*(2 * s if i == j else 0 for i in range(4))) for j in range(4) for s in (1, -1)]
T2_ELEMENTS = Q8_ELEMENTS + [ints(*signs) for signs in itertools.product((1, -1), repeat=4)]
O2_ELEMENTS = list(T2_ELEMENTS)
for i, j in itertools.combinations(range(4), 2):
    for s, u in itertools.product((1, -1), repeat=2):
        element = [(0, 0)] * 4
        element[i], element[j] = (0, s), (0, u)
        O2_ELEMENTS.append(tuple(element))
I2_ELEMENTS = list(T2_ELEMENTS)
for values in even_permutations(((0, 1), (1, 0), (-1, 1), (0, 0))):
    places = [i for i in range(4) if values[i] != (0, 0)]
    for signs in itertools.product((1, -1), repeat=3):
        element = list(values)
        for i, s in zip(places, signs):
            element[i] = (s * values[i][0], s * values[i][1])
        I2_ELEMENTS.append(tuple(element))


def group_table(times, elements):
    index = {e: i for i, e in enumerate(elements)}
    assert len(index) == len(elements)
    mult = [[index[product(times, x, y)] for y in elements] for x in elements]
    inv = [index[(e[0], (-e[1][0], -e[1][1]), (-e[2][0], -e[2][1]), (-e[3][0], -e[3][1]))] for e in elements]
    trace = [e[0] for e in elements]
    one = index[ints(2, 0, 0, 0)]
    return mult, inv, trace, one


def group_is_valid(group):
    mult, inv, trace, one = group
    size = range(len(mult))
    return (all(mult[one][g] == g == mult[g][one] and mult[g][inv[g]] == one for g in size)
            and all(mult[mult[a][b]][c] == mult[a][mult[b][c]] for a in size for b in size for c in size))


def conjugacy_classes(group):
    mult, inv, trace, one = group
    seen, out = set(), []
    for g in range(len(mult)):
        if g not in seen:
            orbit = {mult[mult[h][g]][inv[h]] for h in range(len(mult))}
            seen |= orbit
            out.append((len(orbit), trace[g]))
    return out


RINGS = {"Q8": Z, "2T": Z, "2O": ROOT2, "2I": PHI}
ELEMENTS = {"Q8": Q8_ELEMENTS, "2T": T2_ELEMENTS, "2O": O2_ELEMENTS, "2I": I2_ELEMENTS}
GROUPS = {name: group_table(RINGS[name], ELEMENTS[name]) for name in ELEMENTS}
if SABOTAGE == "bad_group":
    row = GROUPS["Q8"][0][3]
    row[1], row[2] = row[2], row[1]
EXPECT_CLASS_SIZES = {"Q8": [1, 1, 2, 2, 2], "2T": [1, 1, 4, 4, 4, 4, 6], "2O": [1, 1, 6, 6, 6, 8, 8, 12], "2I": [1, 1, 12, 12, 12, 12, 20, 20, 30]}
# Elements counted by trace. These levels are what the character sums below use, derived from the groups just built.
LEVELS = {}
for name in ELEMENTS:
    times = RINGS[name]
    valid = group_is_valid(GROUPS[name]) and all(rplus(rplus(rplus(times(c0, c0), times(c1, c1)), times(c2, c2)), times(c3, c3)) == (4, 0) for c0, c1, c2, c3 in ELEMENTS[name])
    classes = conjugacy_classes(GROUPS[name])
    sizes = sorted(size for size, _ in classes)
    counts = {}
    for size, trace_value in classes:
        counts[trace_value] = counts.get(trace_value, 0) + size
    LEVELS[name] = (times, sorted(counts.items(), key=lambda kv: kv[0]))
    ok = valid and sizes == EXPECT_CLASS_SIZES[name]
    check("group table of " + name, ok)
    print("GROUP_TABLE|group=%s|order=%d|closed_associative_unit=%d|class_sizes=%s|ok=%d|json=0" % (name, len(ELEMENTS[name]), 1 if valid else 0, ",".join(map(str, sizes)), 1 if ok else 0))
if SABOTAGE == "wrong_class":
    trace_value, count = LEVELS["2I"][1][-1]
    LEVELS["2I"][1][-1] = (trace_value, count + 1)
CATALAN = [1, 1, 2, 5, 14, 42, 132]
EXPECT_T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}
EXPECT_MOMENT = {"Q8": (4, 4, 2), "2T": (6, 6, 5), "2O": (8, 15, 14), "2I": (12, 133, 132)}
INVARIANTS = {}


def class_average(name, value_of):
    """The exact average over the group of value_of(trace), an element of the ring, as an integer pair."""
    times, levels = LEVELS[name]
    order = sum(m for _, m in levels)
    total = (0, 0)
    for x, m in levels:
        v = value_of(x, times)
        total = (total[0] + m * v[0], total[1] + m * v[1])
    check("irrational part vanishes in " + name, total[1] == 0)
    return red(total[0], order)


def character(n):
    def value(x, times):
        prev, cur = (0, 0), (1, 0)
        for _ in range(n):
            nxt = times(x, cur)
            prev, cur = cur, (nxt[0] - prev[0], nxt[1] - prev[1])
        return cur
    return value


def trace_power(k):
    def value(x, times):
        cur = (1, 0)
        for _ in range(k):
            cur = times(cur, x)
        return cur
    return value


for name in ELEMENTS:
    invariants = []
    for n in range(0, 25):
        avg = class_average(name, character(n))
        check("invariant count is an integer in " + name, avg[1] == 1)
        invariants.append(avg[0])
    INVARIANTS[name] = invariants
    first = next(n for n in range(1, 25) if invariants[n])
    strength = first - 1
    degree, want, haar = EXPECT_MOMENT[name]
    have = class_average(name, trace_power(degree))
    below = all(class_average(name, trace_power(2 * k)) == (CATALAN[k], 1) for k in range(0, degree // 2))
    ok = strength == EXPECT_T[name] and have == (want, 1) and below and CATALAN[degree // 2] == haar
    check("design strength of " + name, ok)
    print("DESIGN|group=%s|first_invariant_degree=%d|strength=%d|E_trace_power_%d=%s|Haar_value=%d|lower_moments_equal_Haar=%d|ok=%d|json=0" % (name, first, strength, degree, text(have), haar, 1 if below else 0, 1 if ok else 0))


# ---- 2. The two groups with rational coordinates serve as integrators, their traces plain integers.
def integrator(name):
    mult, inv, trace, one = GROUPS[name]
    return mult, inv, [value[0] for value in trace], one


Q8 = integrator("Q8")
T2 = integrator("2T")


# ---- 3. The Wilson lattice. side=0 means unbounded Z^d.
class Lattice:
    def __init__(self, dim, side):
        self.dim, self.side = dim, side

    def shift(self, x, mu, step=1):
        y = list(x)
        y[mu] += step
        if self.side:
            y[mu] %= self.side
        return tuple(y)

    def plaquette(self, x, mu, nu):
        # U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1, the repository's convention.
        return [((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), -1), ((x, nu), -1)]


def expectation(lat, plaquettes, group):
    """E[product of a_p] over independent links with the group average on each, a_p = (1/2) Tr U_p, a spanning forest gauge-fixed. An integer pair."""
    mult, inv, trace, one = group
    size = len(mult)
    links = sorted({l for p in plaquettes for l, _ in p})
    parent = {}

    def find(v):
        parent.setdefault(v, v)
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    forest = set()
    for l in links:
        ru, rv = find(l[0]), find(lat.shift(l[0], l[1]))
        if ru != rv:
            parent[ru] = rv
            forest.add(l)
    free = []
    for p in plaquettes:
        for l, _ in p:
            if l not in forest and l not in free:
                free.append(l)
    position = {l: i for i, l in enumerate(free)}
    due = [[] for _ in range(len(free) + 1)]
    for p in plaquettes:
        word = [(position.get(l, -1), s) for l, s in p]
        due[max(i for i, _ in word) + 1].append(word)
    values = [one] * len(free)

    def walk(depth):
        term = 1
        for word in due[depth]:
            h = one
            for i, s in word:
                if i >= 0:
                    h = mult[h][values[i] if s > 0 else inv[values[i]]]
            term *= trace[h]
            if term == 0:
                return 0
        if depth == len(free):
            return term
        total = 0
        for g in range(size):
            values[depth] = g
            total += walk(depth + 1)
        return term * total
    return red(walk(0), 2 ** len(plaquettes) * size ** len(free))


# A plane with both sides of length 1 repeats each link inside the plaquette, U V U^-1 V^-1, so a_p has degree 2 in each link and agreement runs through floor(t/2).
# These rows also pin the inverse in the plaquette word, which every other row here is blind to, since SU(2) is pseudo-real.
SIDE = Lattice(2, 1)
word = SIDE.plaquette((0, 0), 0, 1)
values = (expectation(SIDE, [word], Q8), expectation(SIDE, [word, word], Q8), expectation(SIDE, [word, word], T2))
ok = values == ((1, 4), (1, 1), (1, 3))
check("side of length one", ok)
print("SIDE_ONE|d=2|degree_per_link=2|E_Q8_a=%s|E_Q8_a2=%s|E_2T_a2=%s|SU2_a2=1/3|ok=%d|json=0" % (text(values[0]), text(values[1]), text(values[2]), 1 if ok else 0))


# ---- 4. Moments of X = sum of a_p on (Z/2Z)^4, keeping every multiset with no singly covered link. A singly covered link integrates to zero.
Z2 = Lattice(4, 2)
SITES = list(itertools.product(range(2), repeat=4))
NAMES = [(x, mu, nu) for x in SITES for mu in range(4) for nu in range(mu + 1, 4)]
FACES = {k: Z2.plaquette(*k) for k in NAMES}
LINK_BIT = {}
for k in NAMES:
    for l, _ in FACES[k]:
        LINK_BIT.setdefault(l, 1 << len(LINK_BIT))
MASKS = [sum(LINK_BIT[l] for l, _ in FACES[k]) for k in NAMES]
check("sixty-four links and ninety-six plaquettes", len(LINK_BIT) == 64 and len(NAMES) == 96)
# The plaquette word is gauge-covariant: its trace survives a random gauge transformation, on 200 random fields with 2T.
rng = Random(27)
mult, inv, trace, one = T2
checks = 0
for _ in range(200):
    field = {l: rng.randrange(24) for l in LINK_BIT}
    gauge = {x: rng.randrange(24) for x in SITES}
    moved = {l: mult[mult[gauge[l[0]]][field[l]]][inv[gauge[Z2.shift(l[0], l[1])]]] for l in LINK_BIT}

    def loop_trace(values, word):
        h = one
        for l, s in word:
            h = mult[h][values[l] if s > 0 else inv[values[l]]]
        return trace[h]
    for k in NAMES:
        check("plaquette trace is gauge invariant", loop_trace(field, FACES[k]) == loop_trace(moved, FACES[k]))
        checks += 1
print("GAUGE_INVARIANCE|group=2T|fields=200|traces_checked=%d|json=0" % checks)
INDEX = {k: i for i, k in enumerate(NAMES)}
# Translations and axis permutations map the product measure to itself and a_p to a_p'. One expectation per orbit.
SYMMETRIES = []
for perm in itertools.permutations(range(4)):
    for tr in itertools.product(range(2), repeat=4):
        image = []
        for x, mu, nu in NAMES:
            y = [0] * 4
            for i in range(4):
                y[perm[i]] = (x[i] + tr[perm[i]]) % 2
            m, n = sorted((perm[mu], perm[nu]))
            image.append(INDEX[(tuple(y), m, n)])
        SYMMETRIES.append(image)


def multinomial(counts):
    total = math.factorial(sum(counts))
    for c in counts:
        total //= math.factorial(c)
    return total


def degree_per_link(combo):
    count = {}
    for i in combo:
        for l, _ in FACES[NAMES[i]]:
            count[l] = count.get(l, 0) + 1
    return max(count.values())


def moment(order, chooser):
    total, kept, kinds, memo = (0, 1), 0, {}, {}
    for combo in itertools.combinations_with_replacement(range(96), order):
        once, more = 0, 0
        for i in combo:
            more |= once & MASKS[i]
            once |= MASKS[i]
        if once & ~more:
            continue
        kept += 1
        counts = [combo.count(i) for i in sorted(set(combo))]
        canon = min(tuple(sorted(image[i] for i in combo)) for image in SYMMETRIES)
        if canon not in memo:
            memo[canon] = expectation(Z2, [FACES[NAMES[i]] for i in canon], chooser(canon))
        total = padd(total, pmul((multinomial(counts), 1), memo[canon]))
        key = "+".join(map(str, sorted(counts)))
        kinds[key] = kinds.get(key, 0) + 1
    return total, kept, kinds, len(memo)


def exact_group(combo):
    # Q8 is exact through degree 3 per link and 2T through degree 5.
    degree = degree_per_link(combo)
    assert degree <= 5
    return Q8 if degree <= 3 else T2


first_choice = (lambda combo: Q8) if SABOTAGE == "q8_everywhere" else exact_group
m2, kept2, _, classes2 = moment(2, first_choice)
m3, kept3, _, classes3 = moment(3, first_choice)
m4, kept4, kinds4, classes4 = moment(4, first_choice)
k4 = psub(m4, pmul((3, 1), pmul(m2, m2)))
ok = m2 == (24, 1) and m3 == (0, 1) and m4 == (6897, 4) and k4 == (-15, 4) and (kept2, kept3, kept4) == (96, 96, 4680) and kinds4 == {"1+1+1+1": 24, "2+2": 4560, "4": 96}
check("moments on Z2^4", ok)
print("Z2_4_MOMENTS|E_X2=%s|E_X3=%s|E_X4=%s|k4=%s|multisets_kept=%d,%d,%d|symmetry_classes=%d,%d,%d|kinds_at_order_4=%s|ok=%d|json=0" % (text(m2), text(m3), text(m4), text(k4), kept2, kept3, kept4, classes2, classes3, classes4, ";".join("%s=%d" % kv for kv in sorted(kinds4.items())), 1 if ok else 0))
forced, _, _, _ = moment(4, lambda combo: Q8)
rule = red(96 * INVARIANTS["Q8"][4], 2 ** 4)
ok = forced == (6945, 4) and psub(forced, (6897, 4)) == (12, 1) and rule == (12, 1)
check("Q8 forced past its strength", ok)
print("Q8_FORCED|E_X4=%s|difference_from_Haar=%s|rule_N_p_dim_inv_over_2^(t+1)=%s|ok=%d|json=0" % (text(forced), text(psub(forced, (6897, 4))), text(rule), 1 if ok else 0))
torus = [Z2.plaquette((a, b, 0, 0), 0, 1) for a in (0, 1) for b in (0, 1)]
values = [expectation(Z2, torus, g) for g in (Q8,)]
ok = values == [(1, 256)]
check("torus value", ok)
print("SURFACE_VALUE|surface=torus_side2|faces=4|chi=0|Q8=%s|expected=1/256|ok=%d|json=0" % (text(values[0]), 1 if ok else 0))


# ---- 5. Connected closed surfaces of distinct plaquettes on Z^d through 10 faces: every link covered an even number of times.
def surface_links(lat, face):
    return frozenset(l for l, _ in lat.plaquette(*face))


def faces_through(lat, link):
    y, m = link
    out = []
    for n in range(lat.dim):
        if n != m:
            a, b = sorted((m, n))
            out.append((y, a, b))
            out.append((lat.shift(y, n, -1), a, b))
    return out


def closed_surfaces(dim, limit):
    lat = Lattice(dim, 0)
    origin = (0,) * dim
    per_plane = {}
    for mu in range(dim):
        for nu in range(mu + 1, dim):
            found, visited = set(), set()

            def grow(faces, odd):
                if faces in visited:
                    return
                visited.add(faces)
                if not odd:
                    found.add(faces)
                    return
                if len(faces) + (len(odd) + 3) // 4 > limit:
                    return
                for q in faces_through(lat, min(odd)):
                    if q not in faces:
                        grow(faces | {q}, odd ^ surface_links(lat, q))
            start = (origin, mu, nu)
            grow(frozenset({start}), surface_links(lat, start))
            per_plane[(mu, nu)] = found
    return lat, per_plane


def euler(lat, faces):
    links = {l for f in faces for l in surface_links(lat, f)}
    sites = {x for l in links for x in (l[0], lat.shift(l[0], l[1]))}
    return len(sites) - len(links) + len(faces)


def tally(dim):
    lat, per_plane = closed_surfaces(dim, 10)
    counts, flat, bent, values = {}, 0, 0, {}
    for found in per_plane.values():
        for faces in found:
            size = len(faces)
            counts[size] = counts.get(size, 0) + 1
            spans = {d for f in faces for d in f[1:]}
            if size == 10:
                flat += 1 if len(spans) == 3 else 0
                bent += 1 if len(spans) == 4 else 0
            cover = {}
            for f in faces:
                for l in surface_links(lat, f):
                    cover[l] = cover.get(l, 0) + 1
            check("each link covered twice", set(cover.values()) == {2})
            kind = (size, len(spans), euler(lat, faces))
            if kind not in values:
                values[kind] = expectation(lat, [lat.plaquette(*f) for f in sorted(faces)], Q8)
    per_site = {}
    for size, total in counts.items():
        check("per-site count is an integer", total % size == 0)
        per_site[size] = total // size
    return per_site, flat // 10, bent // 10, values


EXPECT_SURFACES = {4: ({6: 4, 10: 36}, 12, 24), 3: ({6: 1, 10: 3}, 3, 0)}
TALLY = {}
VALUE_F = {}
for dim in (4, 3):
    used = 3 if (SABOTAGE == "drop_direction" and dim == 4) else dim
    per_site, flat, bent, values = tally(used)
    if SABOTAGE == "drop_bent" and dim == 4:
        per_site[10] -= 24
        bent -= 24
    TALLY[dim] = per_site
    want, want_flat, want_bent = EXPECT_SURFACES[dim]
    ok = per_site == want and flat == want_flat and bent == want_bent
    check("closed surfaces in d=%d" % dim, ok)
    print("SURFACES|d=%d|per_site_F6=%d|F7=%d|F8=%d|F9=%d|F10=%d|F10_flat=%d|F10_bent=%d|smaller_than_6=%d|ok=%d|json=0" % (dim, per_site.get(6, 0), per_site.get(7, 0), per_site.get(8, 0), per_site.get(9, 0), per_site.get(10, 0), flat, bent, sum(v for k, v in per_site.items() if k < 6), 1 if ok else 0))
    for (size, spans, chi), value in sorted(values.items()):
        rule = red(1, 2 ** size * 2 ** (size - chi))
        stored = VALUE_F.setdefault(size, value)
        ok = value == rule and chi == 2 and stored == value
        check("surface value", ok)
        print("SURFACE_VALUE|d=%d|faces=%d|directions=%d|chi=%d|Q8=%s|rule=%s|ok=%d|json=0" % (dim, size, spans, chi, text(value), text(rule), 1 if ok else 0))


# ---- 6. The plaquette series. With the character expansion of each face, a closed surface of F faces contributes value * (4u)^F to log Z,
# where u = z'/z from the single-plaquette z(b). Through b^10 in log Z only these surfaces enter: a j >= 1 face or two overlapping surfaces first appear at b^12.
ORDER = 13


def smul(a, b):
    out = [(0, 1)] * ORDER
    for i, x in enumerate(a):
        if x[0]:
            for j, y in enumerate(b):
                if y[0] and i + j < ORDER:
                    out[i + j] = padd(out[i + j], pmul(x, y))
    return out


def sderivative(a):
    return [pmul((i + 1, 1), a[i + 1]) for i in range(ORDER - 1)] + [(0, 1)]


def sdivide(a, b):
    assert b[0] == (1, 1)
    out = []
    for n in range(ORDER):
        acc = a[n]
        for j in range(n):
            acc = psub(acc, pmul(out[j], b[n - j]))
        out.append(acc)
    return out


def spower(a, n):
    out = [(1, 1)] + [(0, 1)] * (ORDER - 1)
    for _ in range(n):
        out = smul(out, a)
    return out


def single_plaquette(moment_of_even_power):
    # z(b) = sum over k of E[(Tr U)^(2k)] b^(2k) / (4^k (2k)!), through b^12, the last coefficient the moments reach.
    z = [(0, 1)] * ORDER
    for k in range(0, 7):
        z[2 * k] = pmul(moment_of_even_power(k), red(1, 4 ** k * math.factorial(2 * k)))
    return z


def su2_moment(k):
    return (CATALAN[k], 1)


Z_SU2 = single_plaquette(su2_moment)
U_SU2 = sdivide(sderivative(Z_SU2), Z_SU2)
DU_SU2 = sderivative(U_SU2)
planes = {4: 6, 3: 3}
SERIES = {}
for dim in (4, 3):
    series = list(U_SU2)
    parts = {}
    for size in (6, 10):
        coefficient = pmul((TALLY[dim].get(size, 0) * 4 ** size * size, planes[dim]), VALUE_F[size])
        term = smul(spower(U_SU2, size - 1), DU_SU2)
        term = [pmul(coefficient, t) for t in term]
        series = [padd(s, t) for s, t in zip(series, term)]
        parts[size] = term
    SERIES[dim] = (series, parts)
PUBLISHED = {1: (1, 4), 3: (-1, 96), 5: (7, 1536), 7: (-31, 23040), 9: (4451, 8847360)}
if SABOTAGE == "wrong_table":
    PUBLISHED[9] = (4452, 8847360)
series, parts = SERIES[4]
ok = all(series[n] == PUBLISHED[n] for n in PUBLISHED) and all(series[n] == (0, 1) for n in (0, 2, 4, 6, 8))
check("plaquette series against the published table", ok)
print("SERIES|d=4|b1=%s|b3=%s|b5=%s|b7=%s|b9=%s|published=arXiv_0807.0185_Table_1_opposite_sign_as_it_lists_1_minus_half_trace|ok=%d|json=0" % (text(series[1]), text(series[3]), text(series[5]), text(series[7]), text(series[9]), 1 if ok else 0))
split = (U_SU2[9], parts[6][9], parts[10][9])
ok = split == ((13, 4423680), (5, 18432), (15, 65536))
check("split of beta^9", ok)
print("SERIES_SPLIT|d=4|beta9_single_plaquette=%s|cube=%s|ten_face=%s|ok=%d|json=0" % (text(split[0]), text(split[1]), text(split[2]), 1 if ok else 0))
s3 = SERIES[3][0]
print("SERIES|d=3|b1=%s|b3=%s|b5=%s|b7=%s|b9=%s|role=the_same_rule_with_the_d3_surface_counts|json=0" % (text(s3[1]), text(s3[3]), text(s3[5]), text(s3[7]), text(s3[9])))
check("d=3 and d=4 first differ at beta^5", s3[1] == series[1] and s3[3] == series[3] and s3[5] != series[5])


# ---- 7. Where each group first leaves SU(2), in the single-plaquette series.
EXPECT_DIFFERENCE = {"Q8": (3, (1, 48)), "2T": (5, (1, 7680)), "2O": (7, (1, 1290240)), "2I": (11, (1, 163499212800))}
for name in ELEMENTS:
    z = single_plaquette(lambda k, name=name: class_average(name, trace_power(2 * k)))
    u = sdivide(sderivative(z), z)
    difference = [psub(x, y) for x, y in zip(u, U_SU2)]
    first = next((n for n in range(0, 12) if difference[n][0]), None)
    order, delta = EXPECT_DIFFERENCE[name]
    ok = first == order and difference[first] == delta
    check("first difference of " + name, ok)
    print("FIRST_DIFFERENCE|group=%s|order=%s|delta=%s|expected_order=%d|expected_delta=%s|ok=%d|json=0" % (name, first, text(difference[first]) if first is not None else "none", order, text(delta), 1 if ok else 0))

print("SCOPE|moments_on_Z2^4=1|series_on_Z^4_and_periodic_side_at_least_4_through_beta^9=1|remainder_bound_at_beta_above_0=OPEN|reflection_positivity=OPEN|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0")
print("SUBGROUP_DESIGNS_DONE|failed=%d|json=0" % len(FAILS))
for name in FAILS:
    print("FAILED|check=%s|json=0" % name.replace(" ", "_"))
sys.exit(1 if FAILS else 0)
