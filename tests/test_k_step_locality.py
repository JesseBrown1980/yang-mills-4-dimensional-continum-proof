#!/usr/bin/env python3
"""YM4-02e: the k-step bound, its limit constant, independent copies, and a bound from locality.

The controls named in docs/PREDICTION-YM4-02e.hbp, pushed before this file existed. The statements and their proofs are in
docs/NOTE-YM4-02e-KSTEP-AND-LOCALITY.md. The groups, the lattice and the pencil C - t D repeat those of
tests/test_quantitative_gap.py, whose file runs on import. C_k comes from exact integer matrix products, the largest four-point
ratio R_k from exact cross-multiplication, and eigenvalues from Sylvester's law. Symmetric blocks are a congruence, each symmetry
checked on the matrices before use, and a bracket found on a small block is certified on all of them.

usage = test_k_step_locality.py [sabotage=NAME]
NAME is one of SABOTAGE_NAMES below, and each must exit 1 on a named check. An unknown name exits 2.
Python standard library, integers only, json=0.
"""
import itertools
import math
import os
import sys
import time

START_NS = time.perf_counter_ns()
SABOTAGE_NAMES = ("A_inverted", "drop_spatial_weight", "dropped_fourth_inverse", "drop_orbit_measure", "no_kth_root", "small_epsilon", "bad_block_measure")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_k_step_locality.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []
HERE = os.path.dirname(os.path.abspath(__file__))
CONJECTURES = []


PRINTED = []


def say(text):
    PRINTED.append(text)
    print(text, flush=True)


def stamp(name):
    print("SECTION|%s|elapsed_seconds=%d" % (name, (time.perf_counter_ns() - START_NS) // 1000000000), file=sys.stderr, flush=True)


def check(name, ok):
    if not ok:
        FAILS.append(name)
        say("FAILED|check=%s|json=0" % name)


def read_rows(tag):
    rows = []
    with open(os.path.join(HERE, "..", "docs", "PREDICTION-YM4-02e.hbp"), encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("|")
            if parts[0] == tag:
                rows.append({p.split("=", 1)[0]: p.split("=", 1)[1] for p in parts[1:] if "=" in p})
    return rows


def ipow(base, exponent):
    assert exponent >= 0
    out = 1
    for _ in range(exponent):
        out *= base
    return out


def frac(n, d):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d)
    return n // g, d // g


def show(pair):
    return "%d/%d" % pair if pair[1] != 1 else "%d" % pair[0]


def read_frac(text):
    parts = text.split("/")
    return frac(int(parts[0]), int(parts[1]) if len(parts) > 1 else 1)


def times(a, b):
    return frac(a[0] * b[0], a[1] * b[1])


def fpow(a, k):
    return ipow(a[0], k), ipow(a[1], k)


def inertia(rows):
    """(positive, negative, rank) of an integer symmetric matrix, rank -1 if asymmetric. Fraction-free elimination."""
    m = [list(r) for r in rows]
    n = len(m)
    if not all(m[i][j] == m[j][i] for i in range(n) for j in range(i)):
        return 0, 0, -1
    prev, positive, negative = 1, 0, 0
    for k in range(n):
        pivot = next((i for i in range(k, n) if m[i][i]), None)
        if pivot is None:
            pair = next(((i, j) for i in range(k, n) for j in range(i + 1, n) if m[i][j]), None)
            if pair is None:
                return positive, negative, k
            i, j = pair
            for r in range(k, n):
                m[i][r] += m[j][r]
            for r in range(k, n):
                m[r][i] += m[r][j]
            pivot = i
        m[k], m[pivot] = m[pivot], m[k]
        for row in m:
            row[k], row[pivot] = row[pivot], row[k]
        top = m[k][k]
        if (top > 0) == (prev > 0):
            positive += 1
        else:
            negative += 1
        rk = m[k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(i, n):
                value, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = value
                m[j][i] = value
        prev = top
    return positive, negative, n


# ---- Groups, as tables. Element 0 is the identity.
class Group:
    def __init__(self, name, elements, product):
        self.name, self.elements = name, elements
        index = {x: i for i, x in enumerate(elements)}
        self.order = len(elements)
        self.mul = [[index[product(a, b)] for b in elements] for a in elements]
        self.inv = [row.index(0) for row in self.mul]
        assert all(self.mul[0][i] == i and self.mul[i][0] == i for i in range(self.order))
        self.abelian = all(self.mul[a][b] == self.mul[b][a] for a in range(self.order) for b in range(self.order))
        central = [z for z in range(1, self.order) if self.mul[z][z] == 0 and all(self.mul[z][x] == self.mul[x][z] for x in range(self.order))]
        self.central_involution = central[0] if len(central) == 1 else None


SIGNED = {(0, 0): (0, 1), (0, 1): (1, 1), (0, 2): (2, 1), (0, 3): (3, 1), (1, 0): (1, 1), (1, 1): (0, -1), (1, 2): (3, 1), (1, 3): (2, -1),
          (2, 0): (2, 1), (2, 1): (3, -1), (2, 2): (0, -1), (2, 3): (1, 1), (3, 0): (3, 1), (3, 1): (2, 1), (3, 2): (1, -1), (3, 3): (0, -1)}


def doubled_quaternion_product(a, b):
    out = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            k, sign = SIGNED[(i, j)]
            out[k] += sign * a[i] * b[j]
    assert all(x % 2 == 0 for x in out)
    return tuple(x // 2 for x in out)


def q8_elements():
    out = [(2, 0, 0, 0), (-2, 0, 0, 0)]
    for i in (1, 2, 3):
        for sign in (2, -2):
            e = [0, 0, 0, 0]
            e[i] = sign
            out.append(tuple(e))
    return out


def group_named(name):
    if name == "Z2":
        return Group("Z2", [0, 1], lambda a, b: (a + b) % 2)
    if name == "Z3":
        return Group("Z3", [0, 1, 2], lambda a, b: (a + b) % 3)
    if name == "S3":
        perms = [p for p in itertools.permutations(range(3))]
        perms.remove((0, 1, 2))
        perms.insert(0, (0, 1, 2))
        return Group("S3", perms, lambda a, b: tuple(a[b[i]] for i in range(3)))
    if name == "Q8":
        return Group("Q8", q8_elements(), doubled_quaternion_product)
    assert name == "2T"
    return Group("2T", q8_elements() + list(itertools.product((1, -1), repeat=4)), doubled_quaternion_product)


def weight_of(group, text):
    """Integer numerators over one common denominator, one per group element. r=p/s is the Wilson form on Q8 and 2T."""
    if text.startswith("q="):
        q = read_frac(text[2:])
        assert group.name == "Z2"
        return [q[1], q[0]], q[1]
    if text.startswith("r="):
        r = read_frac(text[2:])
        numerators = []
        for x in group.elements:
            exponent = 2 - x[0]
            numerators.append(ipow(r[0], exponent) * ipow(r[1], 4 - exponent))
        return numerators, ipow(r[1], 4)
    values = [read_frac(t) for t in text.split(",")]
    if group.name == "S3":
        kinds = [sum(1 for i in range(3) if p[i] != i) for p in group.elements]
        by_element = [values[{0: 0, 2: 1, 3: 2}[k]] for k in kinds]
    else:
        by_element = values
    common = 1
    for _, d in by_element:
        common = common * d // math.gcd(common, d)
    return [n * common // d for n, d in by_element], common


def tau_of(numerators, links):
    top, bottom = ipow(max(numerators), links), ipow(min(numerators), links)
    return frac(top - bottom, top + bottom)


# ---- The spatial lattice and the pencil.
class Lattice:
    def __init__(self, dims):
        self.dims = dims
        self.sites = list(itertools.product(*[range(d) for d in dims]))
        self.link_index = {}
        for s in self.sites:
            for mu in range(len(dims)):
                self.link_index[(s, mu)] = len(self.link_index)
        self.links = [None] * len(self.link_index)
        for key, i in self.link_index.items():
            self.links[i] = key
        self.plaquettes = []
        for s in self.sites:
            for mu, nu in itertools.combinations(range(len(dims)), 2):
                self.plaquettes.append((self.link_index[(s, mu)], self.link_index[(self.step(s, mu), nu)],
                                        self.link_index[(self.step(s, nu), mu)], self.link_index[(s, nu)]))

    def step(self, s, mu):
        moved = list(s)
        moved[mu] = (moved[mu] + 1) % self.dims[mu]
        return tuple(moved)

    def back(self, s, mu):
        moved = list(s)
        moved[mu] = (moved[mu] - 1) % self.dims[mu]
        return tuple(moved)

    def neighbours(self):
        """The largest, over links, of the sum over other links of the plaquettes shared with it."""
        best = 0
        for link in range(len(self.links)):
            best = max(best, sum(len(set(p)) - 1 for p in self.plaquettes if link in p))
        return best


class Pencil:
    """C - t D on gauge orbits, or on all configurations when full_space is set, scaled to integers."""

    def __init__(self, group, numerators, denominator, dims, full_space=False):
        self.group, self.numerators, self.denominator = group, numerators, denominator
        self.lattice = Lattice(dims)
        lat, g = self.lattice, group
        self.n_links, self.n_plaquettes = len(lat.links), len(lat.plaquettes)
        self.configs = list(itertools.product(range(g.order), repeat=self.n_links))
        self.weights = [ipow(g.order, i) for i in range(self.n_links)]
        self.code = {}
        for i, config in enumerate(self.configs):
            self.code[sum(c * w for c, w in zip(config, self.weights))] = i
        self.labels = self.orbit_labels(full_space)
        self.orbits = 1 + max(self.labels)
        self.members = [[] for _ in range(self.orbits)]
        for i, label in enumerate(self.labels):
            self.members[label].append(i)
        self.sizes = [len(m) for m in self.members]
        self.reps = [self.configs[m[0]] for m in self.members]
        self.spatial = [self.spatial_weight(x) for x in self.reps]
        self.build()

    def index_of(self, config):
        return self.code[sum(c * w for c, w in zip(config, self.weights))]

    def orbit_labels(self, full_space):
        lat, g = self.lattice, self.group
        labels = [-1] * len(self.configs)
        next_label = 0
        for start in range(len(self.configs)):
            if labels[start] >= 0:
                continue
            labels[start] = next_label
            stack = [start]
            while stack and not full_space:
                config = self.configs[stack.pop()]
                for site in lat.sites:
                    for h in range(1, g.order):
                        moved = list(config)
                        for mu in range(len(lat.dims)):
                            out = lat.link_index[(site, mu)]
                            moved[out] = g.mul[h][moved[out]]
                        for mu in range(len(lat.dims)):
                            back = lat.link_index[(lat.back(site, mu), mu)]
                            moved[back] = g.mul[moved[back]][g.inv[h]]
                        target = self.index_of(moved)
                        if labels[target] < 0:
                            labels[target] = next_label
                            stack.append(target)
            next_label += 1
        return labels

    def spatial_weight(self, config):
        if SABOTAGE == "drop_spatial_weight":
            return ipow(self.denominator, self.n_plaquettes)
        g = self.group
        common = 1
        for x in self.numerators:
            common = common * x // math.gcd(common, x)
        out = 1
        for a, b, c, d in self.lattice.plaquettes:
            last = config[d] if SABOTAGE == "dropped_fourth_inverse" else g.inv[config[d]]
            value = g.mul[g.mul[g.mul[config[a]][config[b]]][g.inv[config[c]]]][last]
            out *= common // self.numerators[value] if SABOTAGE == "A_inverted" else self.numerators[value]
        return out

    def build(self):
        g, n = self.group, self.orbits
        lcm_sizes = 1
        for s in self.sizes:
            lcm_sizes = lcm_sizes * s // math.gcd(lcm_sizes, s)
        table = [[self.numerators[g.mul[x][g.inv[y]]] for y in range(g.order)] for x in range(g.order)]
        self.scaled = [[0] * n for _ in range(n)]
        for i in range(n):
            x = self.reps[i]
            rows = [table[v] for v in x]
            for j in range(i, n):
                total = 0
                for index in self.members[j]:
                    y = self.configs[index]
                    product = 1
                    for row, v in zip(rows, y):
                        product *= row[v]
                    total += product
                value = total * (lcm_sizes // self.sizes[j])
                self.scaled[i][j] = value
                self.scaled[j][i] = value
        self.lcm_sizes = lcm_sizes
        lcm_spatial = 1
        for a in self.spatial:
            lcm_spatial = lcm_spatial * a // math.gcd(lcm_spatial, a)
        self.lcm_spatial = lcm_spatial
        scale = ipow(self.denominator, self.n_links + self.n_plaquettes) * ipow(g.order, self.n_links)
        self.diagonal = [(lcm_sizes // self.sizes[i]) * scale * (lcm_spatial // self.spatial[i]) for i in range(n)]

    def c_matrix(self):
        return [[self.lcm_spatial * x for x in row] for row in self.scaled]

    def top(self):
        return frac(ipow(max(self.numerators), self.n_links + self.n_plaquettes), ipow(self.denominator, self.n_links + self.n_plaquettes))


def lattice_perms(pencil):
    """Candidate symmetries of the orbits, as permutations: involutions, and shifts by one for the zero-momentum blocks."""
    lat, g = pencil.lattice, pencil.group
    involutions, cycles = [], []

    def perm_from(transform):
        out = []
        for x in pencil.reps:
            out.append(pencil.labels[pencil.index_of(transform(x))])
        return out

    def shift(mu, amount):
        def transform(x):
            moved = [0] * len(x)
            for link, (s, nu) in enumerate(lat.links):
                target = s
                for _ in range(amount):
                    target = lat.step(target, mu)
                moved[lat.link_index[(target, nu)]] = x[link]
            return moved
        return transform

    for mu, side in enumerate(lat.dims):
        if side > 1:
            cycles.append(perm_from(shift(mu, 1)))
        if side % 2 == 0:
            involutions.append(perm_from(shift(mu, side // 2)))
    z = g.central_involution
    if z is not None:
        for mu in range(len(lat.dims)):
            def twist(x, mu=mu):
                return [g.mul[z][v] if lat.links[i][1] == mu else v for i, v in enumerate(x)]
            involutions.append(perm_from(twist))
    if g.abelian and g.order > 2:
        involutions.append(perm_from(lambda x: [g.inv[v] for v in x]))
    return involutions, cycles


def commutes(perm, c, d):
    n = len(d)
    if sorted(perm) != list(range(n)) or any(d[perm[i]] != d[i] for i in range(n)):
        return False
    return all(c[perm[i]][perm[j]] == c[i][j] for i in range(n) for j in range(n))


def closure(perms, n):
    identity = tuple(range(n))
    seen = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for p in perms:
            moved = tuple(p[element[i]] for i in range(n))
            if moved not in seen:
                seen.add(moved)
                frontier.append(moved)
    return sorted(seen)


def block_vectors(n, involutions, cycle_elements):
    """Sparse integer vectors with disjoint supports inside a block, one block per character of the involutions."""
    g = len(involutions)
    masks = []
    for mask in range(ipow(2, g)):
        perm = list(range(n))
        for b in range(g):
            if (mask >> b) & 1:
                perm = [involutions[b][perm[i]] for i in range(n)]
        masks.append((mask, perm))
    blocks = {}
    seen = set()
    for i in range(n):
        for chi in range(ipow(2, g)):
            v = {}
            for mask, perm in masks:
                sign = -1 if bin(mask & chi).count("1") % 2 else 1
                j = perm[i]
                for element in cycle_elements:
                    k = element[j]
                    v[k] = v.get(k, 0) + sign
            v = {k: x for k, x in v.items() if x}
            if not v:
                continue
            common = 0
            for x in v.values():
                common = math.gcd(common, x)
            first = min(v)
            sign = -1 if v[first] < 0 else 1
            items = tuple(sorted((k, sign * x // common) for k, x in v.items()))
            key = (chi, items)
            if key not in seen:
                seen.add(key)
                blocks.setdefault(chi, []).append(dict(items))
    return blocks


def compress(block, c, d):
    size = len(block)
    cb = [[0] * size for _ in range(size)]
    db = [[0] * size for _ in range(size)]
    for a in range(size):
        va = block[a]
        for b in range(a, size):
            vb = block[b]
            total = 0
            for i, x in va.items():
                row = c[i]
                for j, y in vb.items():
                    total += x * y * row[j]
            cb[a][b] = total
            cb[b][a] = total
        db[a][a] = d[min(va)] if SABOTAGE == "bad_block_measure" else sum(x * x * d[i] for i, x in va.items())
    common = 0
    for row in cb:
        for x in row:
            common = math.gcd(common, x)
    for a in range(size):
        common = math.gcd(common, db[a][a])
    if common > 1:
        cb = [[x // common for x in row] for row in cb]
        db = [[x // common for x in row] for row in db]
    return cb, db


class BlockPencil:
    """Inertia of v C - u D by symmetric blocks. A congruence keeps the inertia, by Sylvester's law."""

    def __init__(self, c, d, involutions, cycles):
        n = len(d)
        kept = [p for p in involutions if commutes(p, c, d)]
        kept = [p for i, p in enumerate(kept) if p not in kept[:i] and p != list(range(n))]
        independent = []
        span = {tuple(range(n))}
        for p in kept:
            if tuple(p) in span:
                continue
            if any(any(p[q[i]] != q[p[i]] for i in range(n)) for q in independent):
                continue
            independent.append(p)
            span = span | {tuple(p[e[i]] for i in range(n)) for e in span}
        self.involutions = independent
        cyc = [p for p in cycles if commutes(p, c, d) and all(all(p[q[i]] == q[p[i]] for i in range(n)) for q in independent)]
        cyc_elements = closure(cyc, n) if cyc else [tuple(range(n))]
        full = block_vectors(n, independent, [tuple(range(n))])
        count = sum(len(b) for b in full.values())
        assert count == n, (count, n)
        self.full = [compress(b, c, d) for b in full.values()]
        small = block_vectors(n, independent, cyc_elements)
        self.small = [compress(b, c, d) for b in small.values()]
        self.block_size = max(len(b[0]) for b in self.full)

    def inertia_of(self, blocks, t):
        u, v = t
        positive, negative = 0, 0
        for cb, db in blocks:
            size = len(cb)
            rows = [[v * cb[i][j] - u * db[i][j] for j in range(size)] for i in range(size)]
            p, m, _ = inertia(rows)
            positive += p
            negative += m
        return positive, negative

    def above(self, t):
        return self.inertia_of(self.full, t)[0]

    def below(self, t):
        return self.inertia_of(self.full, t)[1]

    def above_small(self, t):
        return self.inertia_of(self.small, t)[0]


def power_of_two_above(pair):
    if pair[0] >= pair[1]:
        value = 1
        while value * pair[1] < pair[0]:
            value *= 2
        return value, 1
    value = 1
    while 2 * value * pair[0] <= pair[1]:
        value *= 2
    return 1, value


def bisect(count, k, lo, hi, bits, top):
    """Integers lo < hi with the k-th eigenvalue, counted from 0, in (lo, hi] on the grid top * i / 2^bits."""
    den = ipow(2, bits) * top[1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if count(frac(mid * top[0], den)) >= k + 1:
            lo = mid
        else:
            hi = mid
    return lo, hi


def top_two(bp, top, bits, upper=None):
    """Brackets of the top two eigenvalues, found on the small blocks and certified on all of them.

    The top one sits in the trivial block, by Perron. If another block holds a larger second eigenvalue, the search runs on all
    blocks, from what the small blocks gave up to the upper bound on the ratio when one is known."""
    top = power_of_two_above(top)
    den = ipow(2, bits) * top[1]

    def grid(i):
        return frac(i * top[0], den)

    # Eigenvalues found on a small block are true eigenvalues. So one count on all blocks at hi1 certifies the rest: if exactly one
    # eigenvalue lies above hi1, it is the small blocks' top, which is then lambda_0, and the second largest is in (lo1, hi1].
    lo0, hi0 = bisect(bp.above_small, 0, 0, ipow(2, bits), bits, top)
    lo1, hi1 = bisect(bp.above_small, 1, 0, hi0, bits, top)
    if bp.above(grid(hi1)) > 1:
        ceiling = hi0
        if upper is not None:
            bound = times(upper, grid(hi0))
            ceiling = min(hi0, -((-bound[0] * den) // (bound[1] * top[0])) + 1)
        lo1, hi1 = bisect(bp.above, 1, hi1, ceiling, bits, top)
        if bp.above(grid(hi1)) > 1:
            lo0, hi0 = bisect(bp.above, 0, 0, ipow(2, bits), bits, top)
            lo1, hi1 = bisect(bp.above, 1, 0, hi0, bits, top)
    negative_free = bp.below((-grid(hi1)[0], grid(hi1)[1])) == 0
    return grid(lo0), grid(hi0), grid(lo1), grid(hi1), negative_free


def ppm_floor(pair):
    return pair[0] * 1000000 // pair[1]


def ppm_ceil(pair):
    return -((-pair[0] * 1000000) // pair[1])


def ratio_bracket(lo0, hi0, lo1, hi1):
    return frac(lo1[0] * hi0[1], lo1[1] * hi0[0]), frac(hi1[0] * lo0[1], hi1[1] * lo0[0])


# ---- C_k and R_k.
def scale_down(m):
    common = 0
    for row in m:
        for x in row:
            common = math.gcd(common, x)
            if common == 1:
                return m
    return [[x // common for x in row] for row in m]


def product_through(a, d, b):
    n = len(d)
    out = [[0] * n for _ in range(n)]
    columns = [[b[l][j] for l in range(n)] for j in range(n)]
    for i in range(n):
        weighted = [a[i][l] * d[l] for l in range(n)]
        for j in range(i, n):
            total = sum(x * y for x, y in zip(weighted, columns[j]))
            out[i][j] = total
            out[j][i] = total
    return scale_down(out)


class KSteps:
    """C_k up to a constant, for k a power of 2, on orbits."""

    def __init__(self, pencil, no_a=False):
        self.d = []
        for i in range(pencil.orbits):
            a = 1 if no_a else pencil.spatial[i]
            self.d.append(a if SABOTAGE == "drop_orbit_measure" else a * pencil.sizes[i])
        common = 0
        for x in self.d:
            common = math.gcd(common, x)
        self.d = [x // common for x in self.d]
        self.matrix = {1: scale_down(pencil.scaled)}

    def at(self, k):
        if k not in self.matrix:
            half = self.at(k // 2)
            self.matrix[k] = product_through(half, self.d, half)
        return self.matrix[k]


def largest_ratio(rows, starts=None):
    """The largest four-point ratio of a positive matrix, as a reduced pair, over row pairs (i, i2), i in starts."""
    n = len(rows)
    best_top, best_bottom = 1, 1
    for i in (range(n) if starts is None else starts):
        first = rows[i]
        for i2 in range(n):
            if i2 == i:
                continue
            second = rows[i2]
            high_top, high_bottom = first[0], second[0]
            low_top, low_bottom = first[0], second[0]
            for a, b in zip(first, second):
                if a * high_bottom > high_top * b:
                    high_top, high_bottom = a, b
                elif a * low_bottom < low_top * b:
                    low_top, low_bottom = a, b
            top, bottom = high_top * low_bottom, high_bottom * low_top
            if top * best_bottom > best_top * bottom:
                best_top, best_bottom = top, bottom
    return frac(best_top, best_bottom)


def tau_at_least(r, y):
    """True when y <= tau for the given R, with y a pair below 1: R >= ((1 + y)/(1 - y))^2."""
    top, bottom = y[1] + y[0], y[1] - y[0]
    if bottom <= 0:
        return False
    return r[0] * bottom * bottom >= r[1] * top * top


def root_ppm(r, k):
    """floor and ceil of 10^6 tau^(1/k)."""
    million = ipow(1000000, k)
    lo, hi = 0, 1000000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if tau_at_least(r, (ipow(mid, k), million)):
            lo = mid
        else:
            hi = mid
    return lo, hi


SQRT_SCALE = ipow(10, 90)


def tau_bracket(r):
    """Rational lo <= tau <= hi from an integer square root, as pairs."""
    s = math.isqrt(r[0] * SQRT_SCALE * SQRT_SCALE // r[1])
    return frac(s - SQRT_SCALE, s + SQRT_SCALE), frac(s + 1 - SQRT_SCALE, s + 1 + SQRT_SCALE)


def c_milli(r, k, ratio_low, ratio_high):
    """floor and ceil of 1000 tau_k / theta^k."""
    tau_lo, tau_hi = tau_bracket(r)
    t_low, t_high = fpow(ratio_low, k), fpow(ratio_high, k)
    return tau_lo[0] * 1000 * t_high[1] // (tau_lo[1] * t_high[0]), -((-tau_hi[0] * 1000 * t_low[1]) // (tau_hi[1] * t_low[0]))


def read_sandwich(name, r, k, ratio_low):
    y = ratio_low if SABOTAGE == "no_kth_root" else fpow(ratio_low, k)
    ok = tau_at_least(r, y)
    check("sandwich_%s_k=%d" % (name, k), ok)
    return ok


def read_composition(name, results):
    good = True
    for k, r in results.items():
        if 2 * k in results:
            twice = results[2 * k]
            ok = 4 * r[0] * twice[0] * r[1] <= (r[0] + r[1]) * (r[0] + r[1]) * twice[1]
            check("composition_%s_k=%d" % (name, k), ok)
            good = good and ok
    return good


def dims_of(text):
    return tuple(int(d) for d in text.split(","))


def dims_name(text):
    return text.replace(",", "x")


def pencil_for(row, full_space=False):
    group = group_named(row["group"])
    numerators, denominator = weight_of(group, row["weight"])
    return Pencil(group, numerators, denominator, dims_of(row["dims"]), full_space), numerators


def blocks_of(pencil):
    involutions, cycles = lattice_perms(pencil)
    return BlockPencil(pencil.c_matrix(), pencil.diagonal, involutions, cycles)


def ratio_of(pencil, bits=40):
    """(ratio_low, ratio_high, negative_free) of the top two eigenvalues."""
    bp = blocks_of(pencil)
    lo0, hi0, lo1, hi1, free = top_two(bp, pencil.top(), bits)
    low, high = ratio_bracket(lo0, hi0, lo1, hi1)
    return low, high, free


# ---- Sections.
def r_row_matches(r, row, name):
    if "sqrt_R" in row:
        s = read_frac(row["sqrt_R"])
        ok = r[0] * s[1] * s[1] == r[1] * s[0] * s[0]
    else:
        ok = show(r) == row["R"]
    check(name, ok)
    if "tau" in row and "sqrt_R" in row:
        s = read_frac(row["sqrt_R"])
        check(name + "_tau", show(frac(s[0] - s[1], s[0] + s[1])) == row["tau"])
    return ok


def section_exact_rows(tag, label, store):
    groups = {}
    for row in read_rows(tag):
        groups.setdefault((row["group"], row["dims"], row["weight"]), []).append(row)
    for (group, dims, weight), rows in groups.items():
        pencil, _ = pencil_for(rows[0])
        steps = KSteps(pencil)
        low, high, free = ratio_of(pencil)
        results = {}
        for row in rows:
            k = int(row["k"])
            r = largest_ratio(steps.at(k))
            results[k] = r
            name = "%s_%s_dims_%s_k=%d" % (label, group, dims_name(dims), k)
            matched = r_row_matches(r, row, name)
            sandwich = read_sandwich("%s_dims_%s_%s" % (group, dims_name(dims), weight), r, k, low)
            root = root_ppm(r, k)
            constant = c_milli(r, k, low, high)
            say("YM4_02E_%s|group=%s|dims=%s|weight=%s|k=%d|links=%d|orbits=%d|R_digits=%d|root_ppm=%d..%d|ratio_ppm=%d..%d|C_milli=%d..%d|matched=%d|sandwich=%d|json=0" % (
                label.upper(), group, dims, weight, k, pencil.n_links, pencil.orbits, len(str(r[0])), root[0], root[1], ppm_floor(low), ppm_ceil(high), constant[0], constant[1], matched, sandwich))
        composition = read_composition("%s_dims_%s_%s" % (group, dims_name(dims), weight), results)
        check("no_negative_top_%s_dims_%s" % (group, dims_name(dims)), free)
        store[(group, dims, weight)] = (results, low, high, composition, pencil, steps)


def section_a_enters(store):
    section_exact_rows("YM4_02E_A_ENTERS", "a_enters", store)
    for row in read_rows("YM4_02E_THETA"):
        _, low, high, _, _, _ = store[(row["group"], row["dims"], row["weight"])]
        wanted = row["ratio_ppm"].split("..")
        ok = ppm_floor(low) == int(wanted[0]) and ppm_ceil(high) == int(wanted[1])
        check("theta_%s_dims_%s" % (row["group"], dims_name(row["dims"])), ok)
        say("YM4_02E_THETA|group=%s|dims=%s|ratio_ppm=%d..%d|as_predicted=%d|json=0" % (row["group"], row["dims"], ppm_floor(low), ppm_ceil(high), ok))
    for row in read_rows("YM4_02E_NO_A"):
        pencil, _ = pencil_for(row)
        k = int(row["k"])
        r = largest_ratio(KSteps(pencil, no_a=True).at(k))
        s = read_frac(row["sqrt_R"])
        ok = r[0] * s[1] * s[1] == r[1] * s[0] * s[0]
        check("no_a_%s_dims_%s_k=%d" % (row["group"], dims_name(row["dims"]), k), ok)
        say("YM4_02E_NO_A|group=%s|dims=%s|k=%d|sqrt_R=%s|as_predicted=%d|json=0" % (row["group"], row["dims"], k, row["sqrt_R"], ok))


def section_limit(store):
    for row in read_rows("YM4_02E_LIMIT"):
        key = (row["group"], row["dims"], row["weight"])
        results, low, high, _, _, _ = store[key]
        k = int(row["at_k"])
        constant = c_milli(results[k], k, low, high)
        target = read_frac(row["C"])
        allowed = int(row["within_percent"])
        lo_ok = constant[1] * 100 * target[1] >= target[0] * 1000 * (100 - allowed)
        hi_ok = constant[0] * 100 * target[1] <= target[0] * 1000 * (100 + allowed)
        check("limit_constant_%s_dims_%s" % (row["group"], dims_name(row["dims"])), lo_ok and hi_ok)
        say("YM4_02E_LIMIT|group=%s|dims=%s|weight=%s|at_k=%d|C_milli=%d..%d|predicted=%s|within=%d|json=0" % (row["group"], row["dims"], row["weight"], k, constant[0], constant[1], row["C"], lo_ok and hi_ok))


def section_seen():
    rows = read_rows("YM4_02E_SEEN")
    pencil, _ = pencil_for(rows[0])
    steps = KSteps(pencil)
    low, high, _ = ratio_of(pencil)
    results = {}
    for row in rows:
        k = int(row["k"])
        r = largest_ratio(steps.at(k))
        results[k] = r
        root = root_ppm(r, k)
        value = int(row["kth_root_ppm"])
        wanted = row["exact_ratio_ppm"].split("..")
        ok = root[0] - 1 <= value <= root[1] + 1 and ppm_floor(low) == int(wanted[0]) and ppm_ceil(high) == int(wanted[1])
        if "R" in row:
            ok = ok and show(r) == row["R"]
        check("seen_Z2_dims_2x2_k=%d" % k, ok)
        sandwich = read_sandwich("Z2_dims_2x2_q=1/2", r, k, low)
        say("YM4_02E_SEEN|group=Z2|dims=2,2|weight=q=1/2|k=%d|root_ppm=%d..%d|second_seat=%d|ratio_ppm=%d..%d|agrees=%d|sandwich=%d|json=0" % (k, root[0], root[1], value, ppm_floor(low), ppm_ceil(high), ok, sandwich))
    read_composition("Z2_dims_2x2_q=1/2", results)
    for row in read_rows("YM4_02E_SEEN_R"):
        pencil, _ = pencil_for(row)
        r = largest_ratio(KSteps(pencil).at(int(row["k"])))
        ok = show(r) == row["R"]
        check("seen_R_%s_dims_%s" % (row["group"], dims_name(row["dims"])), ok)
        say("YM4_02E_SEEN_R|group=%s|dims=%s|k=%s|R=%s|agrees=%d|json=0" % (row["group"], row["dims"], row["k"], show(r), ok))


def section_controls():
    for row in read_rows("YM4_02E_CONTROL_RATIO"):
        if SABOTAGE == "A_inverted" and row["dims"] != "2,1":
            continue
        if SABOTAGE == "dropped_fourth_inverse" and row["dims"] != "2,2":
            continue
        pencil, _ = pencil_for(row)
        low, high, free = ratio_of(pencil, bits=34)
        wanted = row["ratio_ppm"].split("..")
        ok = ppm_floor(low) >= int(wanted[0]) and ppm_ceil(high) <= int(wanted[1])
        check("control_ratio_%s_dims_%s" % (row["group"], dims_name(row["dims"])), ok)
        say("YM4_02E_CONTROL_RATIO|group=%s|dims=%s|weight=%s|orbits=%d|ratio_ppm=%d..%d|as_pinned=%d|no_negative_top=%d|json=0" % (row["group"], row["dims"], row["weight"], pencil.orbits, ppm_floor(low), ppm_ceil(high), ok, free))
    if SABOTAGE:
        return
    for row in read_rows("YM4_02E_CONTROL_NEGATIVE"):
        pencil, numerators = pencil_for(row)
        top, bottom = [read_frac(x) for x in row["eigenvalues"].split(",")]
        c, d = pencil.c_matrix(), pencil.diagonal

        def nullity(t):
            matrix = [[t[1] * c[i][j] - (t[0] * d[i] if i == j else 0) for j in range(2)] for i in range(2)]
            return 2 - inertia(matrix)[2]

        def signs(t):
            matrix = [[t[1] * c[i][j] - (t[0] * d[i] if i == j else 0) for j in range(2)] for i in range(2)]
            return inertia(matrix)[:2]

        ok = nullity(top) == 1 and nullity(bottom) == 1 and bottom[0] < 0
        check("negative_eigenvalue_exact", ok)
        tau = tau_of(numerators, 1)
        check("negative_equality", frac(-bottom[0] * top[1], bottom[1] * top[0]) == tau and show(tau) == row["tau"])
        # The certificate's negative side: nothing lies below -tau*lambda_0, and something lies just inside it.
        t = times(tau, top)
        fires = signs((-t[0], t[1]))[1] == 0 and signs(frac(-t[0] * 999, t[1] * 1000))[1] == 1
        check("negative_side_reads_it", fires)
        steps = KSteps(pencil)
        r1, r2 = largest_ratio(steps.at(1)), largest_ratio(steps.at(2))
        s1, s2 = read_frac(row["sqrt_R_at_k_1"]), read_frac(row["sqrt_R_at_k_2"])
        check("negative_k_rows", r1[0] * s1[1] * s1[1] == r1[1] * s1[0] * s1[0] and r2[0] * s2[1] * s2[1] == r2[1] * s2[0] * s2[0])
        say("YM4_02E_CONTROL_NEGATIVE|weight=%s|eigenvalues=%s|ratio=%s|tau=%s|negative_side_reads_it=%d|R_1=%s|R_2=%s|json=0" % (row["weight"], row["eigenvalues"], show(frac(-bottom[0] * top[1], bottom[1] * top[0])), show(tau), fires, show(r1), show(r2)))


def section_wilson():
    for row in read_rows("YM4_02E_WILSON"):
        pencil, numerators = pencil_for(row)
        steps = KSteps(pencil)
        low, high, free = ratio_of(pencil, bits=34)
        check("no_negative_top_%s_dims_%s" % (row["group"], dims_name(row["dims"])), free)
        results = {}
        for k in [int(x) for x in row["ks"].split(",")]:
            r = largest_ratio(steps.at(k))
            results[k] = r
            root = root_ppm(r, k)
            sandwich = read_sandwich("%s_dims_%s_%s" % (row["group"], dims_name(row["dims"]), row["weight"]), r, k, low)
            constant = c_milli(r, k, low, high)
            say("YM4_02E_WILSON|group=%s|dims=%s|weight=%s|links=%d|plaquettes=%d|orbits=%d|k=%d|root_ppm=%d..%d|ratio_ppm=%d..%d|tau_range_ppm=%d|C_milli=%d..%d|sandwich=%d|json=0" % (
                row["group"], row["dims"], row["weight"], pencil.n_links, pencil.n_plaquettes, pencil.orbits, k, root[0], root[1], ppm_floor(low), ppm_ceil(high), ppm_ceil(tau_of(numerators, pencil.n_links)), constant[0], constant[1], sandwich))
        read_composition("%s_dims_%s_%s" % (row["group"], dims_name(row["dims"]), row["weight"]), results)


# ---- Z2 by the Walsh transform, on a group index of bits.
def walsh(values):
    v = list(values)
    n = len(v)
    h = 1
    while h < n:
        for start in range(0, n, 2 * h):
            for i in range(start, start + h):
                a, b = v[i], v[i + h]
                v[i], v[i + h] = a + b, a - b
        h *= 2
    return v


class Z2Conv:
    """C_{k+1}(i, .) = (C_k(i, .) a) convolved with z, on the index group, with rows held for start indices alone."""

    def __init__(self, z, a, perms):
        self.z, self.a = z, a
        self.n = len(z)
        self.bits = self.n.bit_length() - 1
        self.spectrum = walsh(z)
        self.perms = [p for p in perms if self.commutes(p)]
        self.starts, self.lift = self.orbit_starts()

    def commutes(self, p):
        n = self.n
        if sorted(p) != list(range(n)) or any(self.a[p[i]] != self.a[i] for i in range(n)):
            return False
        return all(self.z[p[0] ^ p[i]] == self.z[i] for i in range(n))

    def orbit_starts(self):
        lift = [None] * self.n
        starts = []
        for i in range(self.n):
            if lift[i] is not None:
                continue
            starts.append(i)
            lift[i] = (i, list(range(self.n)))
            stack = [i]
            while stack:
                j = stack.pop()
                perm = lift[j][1]
                for p in self.perms:
                    target = p[j]
                    if lift[target] is None:
                        lift[target] = (i, [p[perm[x]] for x in range(self.n)])
                        stack.append(target)
        return starts, lift

    def rows_at(self, ks):
        """{k: full rows}, up to one constant for each k."""
        current = {i: [self.z[i ^ j] for j in range(self.n)] for i in self.starts}
        out = {}
        for k in range(1, max(ks) + 1):
            if k in ks:
                out[k] = self.unfold(current)
            if k < max(ks):
                common = 0
                for i, row in current.items():
                    moved = walsh([x * y for x, y in zip(row, self.a)])
                    moved = walsh([x * y for x, y in zip(moved, self.spectrum)])
                    moved = [x >> self.bits for x in moved]
                    current[i] = moved
                    for x in moved:
                        common = math.gcd(common, x)
                        if common == 1:
                            break
                if common > 1:
                    current = {i: [x // common for x in row] for i, row in current.items()}
        return out

    def unfold(self, current):
        rows = []
        for i in range(self.n):
            start, perm = self.lift[i]
            row = [0] * self.n
            base = current[start]
            for j in range(self.n):
                row[perm[j]] = base[j]
            rows.append(row)
        return rows

    def dense(self):
        """Integer C and D of the pencil, with eigenvalues those of a^(1/2) Z a^(1/2)."""
        common = 1
        for x in self.a:
            common = common * x // math.gcd(common, x)
        c = [[common * self.z[i ^ j] for j in range(self.n)] for i in range(self.n)]
        d = [common // x for x in self.a]
        top = (max(self.a) * sum(self.z), 1)
        return c, d, top


def ring(L, numerator, denominator):
    """T_v of Z2 on sides L x 1: the L self-loops, with A the product over x of w(v_x v_{x+1}). The holonomy is a separate factor."""
    n = ipow(2, L)
    w = [denominator, numerator]
    z = [1] * n
    a = [1] * n
    for i in range(n):
        for x in range(L):
            z[i] *= w[(i >> x) & 1]
            a[i] *= w[((i >> x) ^ (i >> ((x + 1) % L))) & 1]
    perms = [[n - 1 - i for i in range(n)]]
    if L > 1:
        turn = [((i << 1) & (n - 1)) | (i >> (L - 1)) for i in range(n)]
        perms.append(turn)
        if L % 2 == 0 and L > 2:
            half = list(range(n))
            for _ in range(L // 2):
                half = [turn[x] for x in half]
            perms.append(half)
    return Z2Conv(z, a, perms)


def ring_holonomy(L, numerator, denominator, k):
    """sqrt(R_W) of the holonomy factor at k, and its ratio rho_W = ((1 - q)/(1 + q))^L."""
    rho = fpow(frac(denominator - numerator, denominator + numerator), L)
    y = fpow(rho, k)
    return frac(y[1] + y[0], y[1] - y[0]), rho


def conv_ratio(conv, upper=None):
    c, d, top = conv.dense()
    inv = [p for p in conv.perms if all(p[p[i]] == i for i in range(conv.n))]
    cyc = [p for p in conv.perms if p not in inv]
    bp = BlockPencil(c, d, inv, cyc)
    lo0, hi0, lo1, hi1, free = top_two(bp, top, 46, upper)
    low, high = ratio_bracket(lo0, hi0, lo1, hi1)
    return low, high, free


def ring_results(L, numerator, denominator, ks):
    conv = ring(L, numerator, denominator)
    rows = conv.rows_at(ks)
    out = {}
    for k in ks:
        rv = largest_ratio(rows[k], conv.starts)
        sw, _ = ring_holonomy(L, numerator, denominator, k)
        out[k] = frac(rv[0] * sw[0] * sw[0], rv[1] * sw[1] * sw[1])
    largest = max(ks)
    low, high, free = conv_ratio(conv, (root_ppm(out[largest], largest)[1], 1000000))
    _, rho = ring_holonomy(L, numerator, denominator, 1)
    if low[0] * rho[1] < rho[0] * low[1]:
        low = rho
    if high[0] * rho[1] < rho[0] * high[1]:
        high = rho
    return out, low, high, free


class LadderZ2:
    """Z2 on any lattice, gauge fixed on a spanning tree, so that orbits are the bits of the other links."""

    def __init__(self, dims, numerator, denominator):
        self.lat = Lattice(dims)
        lat = self.lat
        site_id = {s: i for i, s in enumerate(lat.sites)}
        parent = list(range(len(lat.sites)))

        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x

        self.tree, self.free = [], []
        self.ends = []
        for link, (s, mu) in enumerate(lat.links):
            a, b = site_id[s], site_id[lat.step(s, mu)]
            self.ends.append((a, b))
            if root(a) != root(b):
                parent[root(a)] = root(b)
                self.tree.append(link)
            else:
                self.free.append(link)
        self.bits = len(self.free)
        self.n = ipow(2, self.bits)
        self.n_sites = len(lat.sites)
        self.bit_of = {link: b for b, link in enumerate(self.free)}
        w = [denominator, numerator]
        self.w = w
        self.adjacent = [[] for _ in range(self.n_sites)]
        for link in self.tree:
            a, b = self.ends[link]
            self.adjacent[a].append((b, link))
            self.adjacent[b].append((a, link))
        z = []
        for i in range(self.n):
            total = 0
            for g in range(ipow(2, self.n_sites - 1)):
                product = 1
                for link in range(len(lat.links)):
                    a, b = self.ends[link]
                    bit = self.value(i, link) ^ ((g >> a) & 1) ^ ((g >> b) & 1)
                    product *= w[bit]
                total += product
            z.append(total)
        a = []
        for i in range(self.n):
            product = 1
            for p in lat.plaquettes:
                bit = 0
                for link in p:
                    bit ^= self.value(i, link)
                product *= w[bit]
            a.append(product)
        self.conv = Z2Conv(z, a, self.perms())

    def value(self, i, link):
        b = self.bit_of.get(link)
        return 0 if b is None else (i >> b) & 1

    def index_of(self, config):
        """The orbit index of a configuration, by walking the tree from site 0."""
        potential = [None] * self.n_sites
        potential[0] = 0
        stack = [0]
        while stack:
            a = stack.pop()
            for b, link in self.adjacent[a]:
                if potential[b] is None:
                    potential[b] = potential[a] ^ config[link]
                    stack.append(b)
        out = 0
        for link in self.free:
            a, b = self.ends[link]
            out |= (config[link] ^ potential[a] ^ potential[b]) << self.bit_of[link]
        return out

    def perms(self):
        lat = self.lat
        out = []
        for mu, side in enumerate(lat.dims):
            if side > 1:
                perm = []
                for i in range(self.n):
                    moved = [0] * len(lat.links)
                    for link, (s, nu) in enumerate(lat.links):
                        moved[lat.link_index[(lat.step(s, mu), nu)]] = self.value(i, link)
                    perm.append(self.index_of(moved))
                out.append(perm)
                if side % 2 == 0 and side > 2:
                    half = list(range(self.n))
                    for _ in range(side // 2):
                        half = [perm[x] for x in half]
                    out.append(half)
            perm = []
            for i in range(self.n):
                moved = [self.value(i, link) ^ (1 if lat.links[link][1] == mu else 0) for link in range(len(lat.links))]
                perm.append(self.index_of(moved))
            out.append(perm)
        return out


def ladder_results(dims, numerator, denominator, ks):
    ladder = LadderZ2(dims, numerator, denominator)
    conv = ladder.conv
    rows = conv.rows_at(ks)
    out = {k: largest_ratio(rows[k], conv.starts) for k in ks}
    largest = max(ks)
    low, high, free = conv_ratio(conv, (root_ppm(out[largest], largest)[1], 1000000))
    return out, low, high, free


def section_engines():
    for text in read_rows("YM4_02E_ENGINE_AGREE")[0]["cases"].split(";"):
        group, dims, weight = text.split(":")
        row = {"group": group, "dims": dims, "weight": weight}
        pencil, _ = pencil_for(row)
        steps = KSteps(pencil)
        q = read_frac(weight[2:])
        dims_t = dims_of(dims)
        ks = (1, 2, 4)
        if dims_t[1] == 1:
            fast, fast_low, fast_high, _ = ring_results(dims_t[0], q[0], q[1], ks)
        else:
            fast, fast_low, fast_high, _ = ladder_results(dims_t, q[0], q[1], ks)
        low, high, _ = ratio_of(pencil)
        same = all(fast[k] == largest_ratio(steps.at(k)) for k in ks)
        same_ratio = ppm_floor(fast_low) == ppm_floor(low) and ppm_ceil(fast_high) == ppm_ceil(high)
        check("engines_agree_%s_dims_%s" % (group, dims_name(dims)), same and same_ratio)
        say("YM4_02E_ENGINE_AGREE|group=%s|dims=%s|weight=%s|same_R=%d|same_ratio=%d|json=0" % (group, dims, weight, same, same_ratio))


def section_scale():
    table = {}
    for row in read_rows("YM4_02E_SCALE"):
        q = read_frac(row["weight"][2:])
        ks = [int(x) for x in row["ks"].split(",")]
        for L in [int(x) for x in row["L"].split(",")]:
            dims = (L, 1) if row["family"] == "Lx1" else (L, 2)
            links = 2 * dims[0] * dims[1]
            results, low, high, free = ring_results(L, q[0], q[1], ks) if row["family"] == "Lx1" else ladder_results(dims, q[0], q[1], ks)
            check("no_negative_top_%s_L=%d_%s" % (row["family"], L, row["weight"]), free)
            name = "Z2_dims_%dx%d_%s" % (dims[0], dims[1], row["weight"])
            read_composition(name, results)
            tau = tau_of([q[1], q[0]], links)
            for k in ks:
                r = results[k]
                sandwich = read_sandwich(name, r, k, low)
                root = root_ppm(r, k)
                constant = c_milli(r, k, low, high)
                table[(row["family"], row["weight"], L, k)] = (r, root, constant, low, high)
                say("YM4_02E_SCALE|family=%s|weight=%s|L=%d|links=%d|k=%d|root_ppm=%d..%d|ratio_ppm=%d..%d|tau_range_ppm=%d|C_milli=%d..%d|sandwich=%d|json=0" % (
                    row["family"], row["weight"], L, links, k, root[0], root[1], ppm_floor(low), ppm_ceil(high), ppm_ceil(tau), constant[0], constant[1], sandwich))
    return table


def section_ring():
    table = {}
    for row in read_rows("YM4_02E_RING"):
        L = dims_of(row["dims"])[0]
        mu = int(row["mu"])
        q = read_frac(row["weight"][2:])
        ks = [L, 2 * L]
        results, low, high, free = ring_results(L, q[0], q[1], ks)
        check("no_negative_top_ring_mu=%d_L=%d" % (mu, L), free)
        read_composition("ring_mu=%d_L=%d" % (mu, L), results)
        for k in ks:
            r = results[k]
            sandwich = read_sandwich("ring_mu=%d_L=%d" % (mu, L), r, k, low)
            tau_lo, tau_hi = tau_bracket(r)
            constant = c_milli(r, k, low, high)
            table[(mu, L, k)] = (ppm_ceil(tau_hi), constant)
            say("YM4_02E_RING|mu=%d|L=%d|weight=%s|x_ppm=%s|ratio_ppm=%d..%d|k=%d|tau_ppm=%d..%d|theta_to_k_ppm=%d..%d|C_milli=%d..%d|sandwich=%d|json=0" % (
                mu, L, row["weight"], row["x_ppm"], ppm_floor(low), ppm_ceil(high), k, ppm_floor(tau_lo), ppm_ceil(tau_hi), ppm_floor(fpow(low, k)), ppm_ceil(fpow(high, k)), constant[0], constant[1], sandwich))
    return table


def epsilon_of(numerators):
    eps = frac(max(numerators) - min(numerators), max(numerators) + min(numerators))
    return (eps[0], eps[1] * 8) if SABOTAGE == "small_epsilon" else eps


def phi_at_most_one(x_ppm, eps, sigma):
    """eps (x + 1/x) + sigma <= 1 at x = x_ppm/10^6, in integers."""
    left = eps[0] * (x_ppm * x_ppm + 1000000 * 1000000) * sigma[1] + sigma[0] * x_ppm * 1000000 * eps[1]
    return left <= x_ppm * 1000000 * eps[1] * sigma[1]


def r_ppm_ceil(eps, sigma):
    lo, hi = 0, 1000000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if phi_at_most_one(mid, eps, sigma):
            hi = mid
        else:
            lo = mid
    return hi


def section_local():
    bounds = {}
    for row in read_rows("YM4_02E_LOCAL"):
        dims = dims_of(row["dims"])
        large_z2 = row["group"] == "Z2" and len(Lattice(dims).links) >= 10
        pencil, numerators = (None, weight_of(group_named("Z2"), row["weight"])[0]) if large_z2 else pencil_for(row)
        eps = epsilon_of(numerators)
        lattice = Lattice(dims) if large_z2 else pencil.lattice
        count = lattice.neighbours()
        sigma = times((count, 1), eps)
        name = "%s_dims_%s_%s" % (row["group"], dims_name(row["dims"]), row["weight"])
        check("local_neighbours_%s" % name, str(count) == row["neighbours"])
        r = r_ppm_ceil(eps, sigma)
        if not SABOTAGE:
            check("local_epsilon_%s" % name, show(eps) == row["epsilon"])
            check("local_r_%s" % name, str(r) == row["r_ppm_ceil"])
        if large_z2:
            q = read_frac(row["weight"][2:])
            conv = LadderZ2(dims, q[0], q[1]).conv
            low, high, free = conv_ratio(conv)
            n_links, orbits = len(lattice.links), conv.n
        else:
            low, high, free = ratio_of(pencil, bits=34)
            n_links, orbits = pencil.n_links, pencil.orbits
        ok = high[0] * 1000000 <= r * high[1] and free
        check("local_bound_%s" % name, ok)
        tau = tau_of(numerators, n_links)
        bounds[(row["group"], row["dims"], row["weight"])] = (r, eps, sigma)
        say("YM4_02E_LOCAL|group=%s|dims=%s|weight=%s|links=%d|orbits=%d|epsilon=%s|neighbours=%d|r_ppm=%d|ratio_ppm=%d..%d|tau_range_ppm=%d|within_r=%d|json=0" % (
            row["group"], row["dims"], row["weight"], n_links, orbits, show(eps), count, r, ppm_floor(low), ppm_ceil(high), ppm_ceil(tau), ok))
    if SABOTAGE:
        return bounds
    for text in read_rows("YM4_02E_LOCAL_FULL_SPACE")[0]["cases"].split(";"):
        group, dims, weight = text.split(":")
        row = {"group": group, "dims": dims, "weight": weight}
        pencil, numerators = pencil_for(row, full_space=True)
        r = bounds[(group, dims, weight)][0]
        low, high, free = ratio_of(pencil, bits=34)
        ok = high[0] * 1000000 <= r * high[1] and free
        check("local_full_space_%s_dims_%s" % (group, dims_name(dims)), ok)
        say("YM4_02E_LOCAL_FULL_SPACE|group=%s|dims=%s|weight=%s|dimension=%d|r_ppm=%d|ratio_ppm=%d..%d|within_r=%d|json=0" % (group, dims, weight, pencil.orbits, r, ppm_floor(low), ppm_ceil(high), ok))
    return bounds


def determinant(rows):
    """Fraction-free elimination."""
    m = [list(r) for r in rows]
    n = len(m)
    sign, prev = 1, 1
    for k in range(n):
        pivot = next((i for i in range(k, n) if m[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        rk, top = m[k], m[k][k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(k + 1, n):
                value, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = value
        prev = top
    return sign * m[n - 1][n - 1]


def section_charpoly():
    """det(C - i D) directly and through the blocks are polynomials of degree n in i. A constant ratio at n + 2 points makes them
    proportional, so the two solvers hold the same eigenvalues with the same multiplicities. The scope is these small matrices."""
    row = read_rows("YM4_02E_BLOCKS_CHARPOLY")[0]
    for text in row["cases"].split(";"):
        group, dims, weight = text.split(":")
        pencil, _ = pencil_for({"group": group, "dims": dims, "weight": weight})
        bp = blocks_of(pencil)
        c, d = pencil.c_matrix(), pencil.diagonal
        n = pencil.orbits
        same = True
        first = None
        for i in range(1, n + 3):
            direct = determinant([[c[a][b] - (i * d[a] if a == b else 0) for b in range(n)] for a in range(n)])
            through = 1
            for cb, db in bp.full:
                size = len(cb)
                through *= determinant([[cb[a][b] - i * db[a][b] for b in range(size)] for a in range(size)])
            if first is None:
                first = (direct, through)
                same = direct != 0 and through != 0
            elif direct * first[1] != first[0] * through:
                same = False
        check("blocks_charpoly_%s_dims_%s" % (group, dims_name(dims)), same)
        say("YM4_02E_BLOCKS_CHARPOLY|group=%s|dims=%s|weight=%s|orbits=%d|unequal_orbit_sizes=%d|blocks=%d|points=%d|same_polynomial=%d|scope=complete_characteristic_polynomial|json=0" % (
            group, dims, weight, n, len(set(pencil.sizes)) > 1, len(bp.full), n + 2, same))


def section_blocks():
    """The block solver against direct elimination, with unequal orbit sizes among the cases, and exact multiplicities through it."""
    row = read_rows("YM4_02E_BLOCKS_AGREE")[0]
    for text in row["cases"].split(";"):
        group, dims, weight = text.split(":")
        pencil, _ = pencil_for({"group": group, "dims": dims, "weight": weight})
        bp = blocks_of(pencil)
        c, d = pencil.c_matrix(), pencil.diagonal
        top = power_of_two_above(pencil.top())
        count = 12 if pencil.orbits <= 81 else 3
        thresholds = [(top[0], top[1] * ipow(2, j)) for j in range(1, count + 1)]
        thresholds += [(-top[0], top[1] * ipow(2, j)) for j in range(1, 3)]
        same = True
        n = pencil.orbits
        for t in thresholds:
            t = frac(t[0], t[1])
            direct = inertia([[t[1] * c[i][j] - (t[0] * d[i] if i == j else 0) for j in range(n)] for i in range(n)])
            same = same and direct[:2] == bp.inertia_of(bp.full, t)
        unequal = len(set(pencil.sizes)) > 1
        check("blocks_agree_%s_dims_%s" % (group, dims_name(dims)), same)
        say("YM4_02E_BLOCKS_AGREE|group=%s|dims=%s|weight=%s|orbits=%d|unequal_orbit_sizes=%d|blocks=%d|largest_block=%d|thresholds=%d|same_inertia=%d|scope=these_thresholds|json=0" % (group, dims, weight, n, unequal, len(bp.full), bp.block_size, len(thresholds), same))
    for text in row["conv_cases"].split(";"):
        kind, size, weight = text.split(":")
        q = read_frac(weight[2:])
        conv = ring(int(size), q[0], q[1]) if kind == "ring" else LadderZ2(dims_of(size), q[0], q[1]).conv
        c, d, top = conv.dense()
        inv = [p for p in conv.perms if all(p[p[i]] == i for i in range(conv.n))]
        cyc = [p for p in conv.perms if p not in inv]
        bp = BlockPencil(c, d, inv, cyc)
        top = power_of_two_above(top)
        same = True
        for j in range(1, 13):
            t = frac(top[0], top[1] * ipow(2, j))
            direct = inertia([[t[1] * c[i][k] - (t[0] * d[i] if i == k else 0) for k in range(conv.n)] for i in range(conv.n)])
            same = same and direct[:2] == bp.inertia_of(bp.full, t)
        check("blocks_agree_%s_%s" % (kind, size.replace(",", "x")), same)
        say("YM4_02E_BLOCKS_AGREE|engine=%s|size=%s|weight=%s|dimension=%d|blocks=%d|largest_block=%d|same_inertia=%d|scope=these_thresholds|json=0" % (kind, size, weight, conv.n, len(bp.full), bp.block_size, same))
    for spec in read_rows("YM4_02E_BLOCKS_SPECTRUM"):
        pencil, _ = pencil_for(spec)
        bp = blocks_of(pencil)
        total = 0
        exact = True
        for item in spec["eigenvalues"].split(","):
            value, _, repeats = item.partition("x")
            t = read_frac(value)
            repeats = int(repeats) if repeats else 1
            p, m = bp.inertia_of(bp.full, t)
            exact = exact and pencil.orbits - p - m == repeats
            total += repeats
        ok = exact and total == pencil.orbits
        check("blocks_multiplicities_%s_dims_%s" % (spec["group"], dims_name(spec["dims"])), ok)
        say("YM4_02E_BLOCKS_SPECTRUM|group=%s|dims=%s|weight=%s|orbits=%d|unequal_orbit_sizes=%d|eigenvalues=%s|exact=%d|json=0" % (spec["group"], spec["dims"], spec["weight"], pencil.orbits, len(set(pencil.sizes)) > 1, spec["eigenvalues"], ok))


def section_first_run():
    """Every row of the first run, stopped at 36 minutes, against this run. One row differs by the documented correction of its check."""
    path = os.path.join(HERE, "..", "reviews", "fable5-ym4-02e-first-run", "FIRST-RUN.hbp")
    with open(path, encoding="utf-8") as handle:
        rows = [line.rstrip("\n") for line in handle]
    printed = set(PRINTED)
    missing = []
    corrected = 0
    for line in rows:
        if line == "FAILED|check=control_ratio_Z3_dims_3x1|json=0":
            corrected += 1
            continue
        if "as_pinned=0" in line:
            corrected += 1
            line = line.replace("as_pinned=0", "as_pinned=1")
        if line not in printed:
            missing.append(line)
    for line in missing:
        say("YM4_02E_FIRST_RUN_DIFFERS|%s" % line)
    check("first_run_rows_reproduce", not missing)
    say("YM4_02E_FIRST_RUN|rows=%d|reproduced=%d|changed_by_the_documented_correction=%d|differ=%d|json=0" % (len(rows), len(rows) - corrected - len(missing), corrected, len(missing)))


def conjecture(name, met, detail):
    CONJECTURES.append((name, met))
    say("YM4_02E_CONJ_READ|name=%s|met=%d|%s|json=0" % (name, met, detail))


def read_conjectures(scale, rings):
    # C_8 grows linearly at fixed q.
    values = [scale[("Lx1", "q=4/5", L, 8)][2] for L in range(2, 7)]
    steps = [(values[i + 1][0] - values[i][1], values[i + 1][1] - values[i][0]) for i in range(len(values) - 1)]
    met = all(s[0] >= 550 and s[1] <= 950 for s in steps)
    conjecture("fixed_q_C_grows", met, "C_8_milli=%s|steps=%s" % (",".join("%d..%d" % v for v in values), ",".join("%d..%d" % s for s in steps)))
    # The k-th root rises with size at fixed q and k.
    bad = []
    for k in (1, 2, 4, 8):
        for L in range(2, 9):
            if scale[("Lx1", "q=1/2", L, k)][1][1] < scale[("Lx1", "q=1/2", L - 1, k)][1][0]:
                bad.append("%d:%d" % (k, L))
    conjecture("root_rises_with_size", not bad, "exceptions=%s" % (",".join(bad) if bad else "none"))
    # The ladder's ratio adds at fixed k.
    details = []
    met = True
    for k in (1, 2):
        r2, r3, r4 = [scale[("Lx2", "q=4/5", L, k)][0] for L in (2, 3, 4)]
        a = frac(r4[0] * r3[1], r4[1] * r3[0])
        b = frac(r3[0] * r2[1], r3[1] * r2[0])
        ratio = frac(a[0] * b[1], a[1] * b[0])
        met = met and 75 * ratio[1] <= 100 * ratio[0] <= 125 * ratio[1]
        details.append("k=%d:%d_permille" % (k, ratio[0] * 1000 // ratio[1]))
    conjecture("ladder_additive", met, ",".join(details))
    # The Ising ring, by its exact law.
    for name, weight, limit in (("ising_disordered", "q=1/2", (2, 3)), ("ising_high_t", "q=4/5", (5, 36))):
        lows = [scale[("Lx1", weight, L, 1)][3] for L in range(1, 7)]
        highs = [scale[("Lx1", weight, L, 1)][4] for L in range(1, 7)]
        rising = all(highs[i][0] * lows[i + 1][1] <= lows[i + 1][0] * highs[i][1] for i in range(5))
        below = all(h[0] * limit[1] <= limit[0] * h[1] for h in highs)
        conjecture(name, rising and below, "ratio_ppm=%s|limit=%s" % (",".join("%d" % ppm_ceil(h) for h in highs), show(limit)))
    lows = [scale[("Lx1", "q=1/5", L, 1)][3] for L in range(1, 7)]
    highs = [scale[("Lx1", "q=1/5", L, 1)][4] for L in range(1, 7)]
    rising = all(highs[i][0] * lows[i + 1][1] <= lows[i + 1][0] * highs[i][1] for i in range(5))
    conjecture("ising_ordered", rising and lows[5][0] * 10 > 9 * lows[5][1], "ratio_ppm=%s" % ",".join("%d" % ppm_ceil(h) for h in highs))
    # The ring at fixed mu.
    for mu in (1, 2):
        cs = [rings[(mu, L, 2 * L)][1] for L in range(2, 9)]
        in_range = all(c[0] >= 1000 and c[1] <= 1800 for c in cs)
        settled = all(abs(cs[i + 1][0] - cs[i][0]) <= 100 for i in range(3, 6))
        conjecture("ring_fixed_mu_C_bounded_mu=%d" % mu, in_range and settled, "C_milli=%s" % ",".join("%d..%d" % c for c in cs))
        taus = [rings[(mu, L, L)][0] for L in range(2, 9)]
        conjecture("ring_fixed_mu_tau_below_one_mu=%d" % mu, all(t <= 900000 for t in taus), "tau_ppm_at_k=L=%s" % ",".join("%d" % t for t in taus))


def section_limits():
    with open(os.path.abspath(__file__), encoding="utf-8") as handle:
        modules = sorted(line.split()[1] for line in handle if line.startswith("import "))
    elapsed = (time.perf_counter_ns() - START_NS) // 1000000000
    within = elapsed <= 1500
    check("runtime_within_1500_seconds", within)
    say("YM4_02E_LIMITS|runtime_within_1500_seconds=%d|modules=%s|json=0" % (within, ",".join(modules)))


def main():
    store = {}
    stamp("start")
    if SABOTAGE == "bad_block_measure":
        section_charpoly()
    if SABOTAGE in ("", "drop_orbit_measure"):
        section_exact_rows("YM4_02E_KSTEP", "kstep", store)
        stamp("kstep")
    if SABOTAGE in ("", "drop_spatial_weight", "no_kth_root"):
        section_a_enters(store)
        stamp("a_enters")
    if SABOTAGE in ("", "A_inverted", "dropped_fourth_inverse"):
        section_controls()
        stamp("controls")
    if SABOTAGE in ("", "small_epsilon"):
        section_local()
        stamp("local")
    if not SABOTAGE:
        section_exact_rows("YM4_02E_PRODUCT", "product", store)
        section_limit(store)
        section_seen()
        stamp("product_limit_seen")
        section_wilson()
        stamp("wilson")
        section_engines()
        stamp("engines")
        scale = section_scale()
        stamp("scale")
        rings = section_ring()
        stamp("ring")
        read_conjectures(scale, rings)
        section_blocks()
        section_charpoly()
        stamp("blocks")
        section_first_run()
        section_limits()
    say("YM4_02E_DONE|failed=%d|conjectures_read=%d|conjectures_met=%d|json=0" % (len(FAILS), len(CONJECTURES), sum(1 for _, m in CONJECTURES if m)))
    sys.exit(1 if FAILS else 0)


main()
