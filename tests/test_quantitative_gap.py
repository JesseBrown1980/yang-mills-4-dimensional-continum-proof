#!/usr/bin/env python3
"""YM4-02d: an explicit gap at each fixed lattice.

The controls named in docs/PREDICTION-YM4-02d.hbp, pushed before this file existed. The statement and its proof are
docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md. On a finite group with a rational weight, the transfer operator on gauge orbits
is a rational pencil C - t D, with C the gauge-averaged B and D = diag(1 / (A_i mu_i)). By Sylvester's law, the number
of eigenvalues above t is the positive inertia of the pencil at t, so eigenvalues are read exactly, by fraction-free
elimination, with no eigenvalue solver. Q8 and 2T come from doubled integer quaternions.

usage = test_quantitative_gap.py [sabotage=NAME]
NAME is one of SABOTAGE_NAMES below, and each must exit 1 on a named check. An unknown name exits 2.
Python standard library, integers only, json=0.
"""
import itertools
import math
import os
import sys
import time

START_NS = time.perf_counter_ns()
SABOTAGE_NAMES = ("drop_gauge_average", "drop_orbit_measure", "half_the_exponent", "drop_spatial_weight")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_quantitative_gap.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def check(name, ok):
    if not ok:
        FAILS.append(name)
        print("FAILED|check=%s|json=0" % name)


def read_rows(tag):
    rows = []
    with open(os.path.join(HERE, "..", "docs", "PREDICTION-YM4-02d.hbp"), encoding="utf-8") as handle:
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


# Hamilton's table: (left basis, right basis) gives (result basis, sign), with 0 for 1 and 1, 2, 3 for i, j, k.
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
            exponent = 2 - x[0]  # 2 - tr(g), and the doubled real part is tr(g)
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


def hypotheses(group, numerators):
    """Which hypothesis of the proposition fails, or none."""
    if min(numerators) < 0:
        return "negative_weight"
    if min(numerators) == 0:
        return "zero_weight"
    if any(numerators[i] != numerators[group.inv[i]] for i in range(group.order)):
        return "asymmetric_weight"
    for g in range(group.order):
        for x in range(group.order):
            if numerators[group.mul[group.mul[x][g]][group.inv[x]]] != numerators[g]:
                return "not_a_class_function"
    return "none"


def tau_of(numerators, links):
    big, small = max(numerators), min(numerators)
    top, bottom = ipow(big, links), ipow(small, links)
    if SABOTAGE == "half_the_exponent":
        return half_exponent_tau(big, small, links)
    return frac(top - bottom, top + bottom)


def half_exponent_tau(big, small, links):
    root_big, root_small = math.isqrt(ipow(big, links)), math.isqrt(ipow(small, links))
    return frac(root_big - root_small, root_big + root_small)


# ---- The spatial lattice and the pencil.
class Lattice:
    def __init__(self, dims):
        self.dims = dims
        self.sites = list(itertools.product(*[range(d) for d in dims]))
        self.site_index = {s: i for i, s in enumerate(self.sites)}
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


class Pencil:
    """C - t D on gauge orbits, or on all configurations when full_space is set, scaled to integers."""

    def __init__(self, group, numerators, denominator, dims, full_space=False):
        self.group, self.numerators, self.denominator = group, numerators, denominator
        self.lattice = Lattice(dims)
        lat, g = self.lattice, group
        self.n_links, self.n_plaquettes = len(lat.links), len(lat.plaquettes)
        self.configs = list(itertools.product(range(g.order), repeat=self.n_links))
        self.labels = self.orbit_labels(full_space)
        self.orbits = 1 + max(self.labels)
        self.members = [[] for _ in range(self.orbits)]
        for i, label in enumerate(self.labels):
            self.members[label].append(i)
        self.sizes = [len(m) for m in self.members]
        self.reps = [self.configs[m[0]] for m in self.members]
        self.spatial = [self.spatial_weight(x) for x in self.reps]
        self.build()

    def orbit_labels(self, full_space):
        lat, g = self.lattice, self.group
        size = g.order
        weights = [ipow(size, i) for i in range(self.n_links)]
        code = {}
        for i, config in enumerate(self.configs):
            code[sum(c * w for c, w in zip(config, weights))] = i
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
                    for h in range(1, size):
                        moved = list(config)
                        for mu in range(len(lat.dims)):
                            out = lat.link_index[(site, mu)]
                            moved[out] = g.mul[h][moved[out]]
                        for mu in range(len(lat.dims)):
                            back = lat.link_index[(self.back_of(site, mu), mu)]
                            moved[back] = g.mul[moved[back]][g.inv[h]]
                        target = code[sum(c * w for c, w in zip(moved, weights))]
                        if labels[target] < 0:
                            labels[target] = next_label
                            stack.append(target)
            next_label += 1
        return labels

    def back_of(self, s, mu):
        moved = list(s)
        moved[mu] = (moved[mu] - 1) % self.lattice.dims[mu]
        return tuple(moved)

    def spatial_weight(self, config):
        if SABOTAGE == "drop_spatial_weight":
            return ipow(self.denominator, self.n_plaquettes)
        g = self.group
        out = 1
        for a, b, c, d in self.lattice.plaquettes:
            value = g.mul[g.mul[g.mul[config[a]][config[b]]][g.inv[config[c]]]][g.inv[config[d]]]
            out *= self.numerators[value]
        return out

    def build(self):
        g, n = self.group, self.orbits
        lcm_sizes = 1
        for s in self.sizes:
            lcm_sizes = lcm_sizes * s // math.gcd(lcm_sizes, s)
        self.scaled = [[0] * n for _ in range(n)]
        self.entry_bounds_hold = True
        low, high = ipow(min(self.numerators), self.n_links), ipow(max(self.numerators), self.n_links)
        for i, x in enumerate(self.reps):
            for j in range(n):
                members = self.members[j] if SABOTAGE != "drop_gauge_average" else [self.members[j][0]] * self.sizes[j]
                total = 0
                for index in members:
                    y = self.configs[index]
                    product = 1
                    for link in range(self.n_links):
                        product *= self.numerators[g.mul[x[link]][g.inv[y[link]]]]
                    total += product
                self.scaled[i][j] = total * (lcm_sizes // self.sizes[j])
                if not low * self.sizes[j] <= total <= high * self.sizes[j]:
                    self.entry_bounds_hold = False
        self.lcm_sizes = lcm_sizes
        lcm_spatial = 1
        for a in self.spatial:
            lcm_spatial = lcm_spatial * a // math.gcd(lcm_spatial, a)
        self.lcm_spatial = lcm_spatial
        total_configs = ipow(g.order, self.n_links)
        scale = ipow(self.denominator, self.n_links + self.n_plaquettes) * total_configs
        self.diagonal = []
        for i in range(n):
            measure = lcm_sizes // self.sizes[i] if SABOTAGE != "drop_orbit_measure" else lcm_sizes
            self.diagonal.append(measure * scale * (lcm_spatial // self.spatial[i]))

    def at(self, t):
        """The integer matrix of C - t D times a positive constant. t is an integer pair."""
        u, v = t
        n = self.orbits
        rows = [[v * self.lcm_spatial * self.scaled[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            rows[i][i] -= u * self.diagonal[i]
        return rows

    def above(self, t):
        return inertia(self.at(t))[0]

    def below(self, t):
        return inertia(self.at(t))[1]

    def nullity(self, t):
        rank = inertia(self.at(t))[2]
        return self.orbits - rank if rank >= 0 else -1


def bracket(pencil, k, bits, top=(1, 1)):
    """Dyadic lo < the k-th eigenvalue <= hi, counting from 0, at absolute width top / 2^bits."""
    lo, hi = 0, ipow(2, bits)
    den = ipow(2, bits) * top[1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if pencil.above(frac(mid * top[0], den)) >= k + 1:
            lo = mid
        else:
            hi = mid
    return frac(lo * top[0], den), frac(hi * top[0], den)


def times(a, b):
    return frac(a[0] * b[0], a[1] * b[1])


def ppm_floor(pair):
    return pair[0] * 1000000 // pair[1]


def ppm_ceil(pair):
    return -((-pair[0] * 1000000) // pair[1])


def eigenvalue_list(text):
    out = []
    for item in text.split(","):
        value, _, count = item.partition("x")
        out.append((read_frac(value), int(count) if count else 1))
    return out


# ---- Sections.
def section_exact():
    for row in read_rows("YM4_02D_EXACT"):
        group = group_named(row["group"])
        dims = tuple(int(d) for d in row["dims"].split(","))
        numerators, denominator = weight_of(group, row["weight"])
        name = "%s_dims_%s" % (row["group"], row["dims"].replace(",", "x"))
        check("hypotheses_hold_%s" % name, hypotheses(group, numerators) == "none")
        pencil = Pencil(group, numerators, denominator, dims)
        check("orbits_%s" % name, str(pencil.orbits) == row["orbits"])
        spectrum = eigenvalue_list(row["eigenvalues"])
        complete = sum(c for _, c in spectrum) == pencil.orbits
        exact = all(pencil.nullity(t) == c for t, c in spectrum)
        check("exact_spectrum_%s" % name, complete and exact)
        top, second = spectrum[0][0], spectrum[1][0]
        check("top_two_%s" % name, pencil.above(top) == 0 and pencil.above(second) == 1)
        ratio = frac(second[0] * top[1], second[1] * top[0])
        tau = tau_of(numerators, pencil.n_links)
        check("ratio_row_%s" % name, show(ratio) == row["ratio"])
        check("tau_row_%s" % name, show(tau) == row["tau"])
        check("bound_%s" % name, ratio[0] * tau[1] <= tau[0] * ratio[1])
        equal = ratio == tau
        check("equality_row_%s" % name, str(int(equal)) == row["equality"])
        print("YM4_02D_EXACT|group=%s|dims=%s|weight=%s|links=%d|orbits=%d|eigenvalues=%s|ratio=%s|tau=%s|equality=%d|json=0" % (
            row["group"], row["dims"], row["weight"], pencil.n_links, pencil.orbits, row["eigenvalues"], show(ratio), show(tau), equal))
        cross_ratio(pencil, numerators, name)


def cross_ratio(pencil, numerators, name):
    """Every four-point ratio with A equals the one without A, and the largest is at most (M/m)^(2N)."""
    if pencil.orbits > 32:
        return
    s, a = pencil.scaled, pencil.spatial
    n = pencil.orbits
    best = (0, 1)
    same = True
    big = ipow(max(numerators), 2 * pencil.n_links)
    small = ipow(min(numerators), 2 * pencil.n_links)
    for i, j in itertools.product(range(n), repeat=2):
        for k, l in itertools.product(range(n), repeat=2):
            top, bottom = s[i][k] * s[j][l], s[i][l] * s[j][k]
            if top * best[1] > best[0] * bottom:
                best = (top, bottom)
            with_a_top = a[i] * s[i][k] * a[k] * a[j] * s[j][l] * a[l]
            with_a_bottom = a[i] * s[i][l] * a[l] * a[j] * s[j][k] * a[k]
            if with_a_top * bottom != top * with_a_bottom:
                same = False
    best = frac(best[0], best[1])
    check("cross_ratio_A_cancels_%s" % name, same)
    check("entries_in_range_%s" % name, pencil.entry_bounds_hold)
    check("cross_ratio_at_most_R_%s" % name, best[0] * small <= big * best[1])
    print("YM4_02D_CROSS_RATIO|case=%s|largest=%s|R=%s|A_cancels=%d|entries_in_range=%d|json=0" % (
        name, show(best), show(frac(big, small)), same, pencil.entry_bounds_hold))
    if name == "Z2_dims_1":
        check("cross_ratio_Z2_dims_1_reads_16", show(best) == "16")


def certificate(pencil, lo, tau):
    """lambda_0 > lo, at most one eigenvalue above tau*lo, and none below -tau*lo, so every other |mu| <= tau*lambda_0."""
    t = times(tau, lo)
    return pencil.above(lo) >= 1 and pencil.above(t) <= 1 and pencil.below((-t[0], t[1])) == 0


def section_plaquettes():
    kept = {}
    for row in read_rows("YM4_02D_PLAQUETTES"):
        if SABOTAGE and int(row["orbits"]) > 81:
            continue
        group = group_named(row["group"])
        dims = tuple(int(d) for d in row["dims"].split(","))
        numerators, denominator = weight_of(group, row["weight"])
        name = "%s_dims_%s_%s" % (row["group"], row["dims"].replace(",", "x"), row["weight"])
        check("hypotheses_hold_%s" % name, hypotheses(group, numerators) == "none")
        pencil = Pencil(group, numerators, denominator, dims)
        check("links_%s" % name, str(pencil.n_links) == row["links"])
        check("plaquettes_%s" % name, str(pencil.n_plaquettes) == row["plaquettes"])
        check("orbits_%s" % name, str(pencil.orbits) == row["orbits"])
        tau = tau_of(numerators, pencil.n_links)
        check("tau_row_%s" % name, show(tau) == row["tau"])
        check("symmetric_%s" % name, inertia(pencil.at((0, 1)))[2] >= 0)
        check("entries_in_range_%s" % name, pencil.entry_bounds_hold)
        top = frac(max(numerators), denominator)
        scale = (ipow(top[0], pencil.n_links + pencil.n_plaquettes), ipow(top[1], pencil.n_links + pencil.n_plaquettes))
        bits = 36 if pencil.orbits <= 32 else 26 if pencil.orbits <= 81 else 11
        lo0, hi0 = bracket(pencil, 0, bits, scale)
        check("certificate_%s" % name, certificate(pencil, lo0, tau))
        ratio_low, ratio_high = "-", "-"
        if pencil.orbits <= 81:
            lo1, hi1 = bracket(pencil, 1, bits, scale)
            low_pair = frac(lo1[0] * hi0[1], lo1[1] * hi0[0])
            high_pair = frac(hi1[0] * lo0[1], hi1[1] * lo0[0])
            ratio_low, ratio_high = ppm_floor(low_pair), ppm_ceil(high_pair)
            check("ratio_below_tau_%s" % name, high_pair[0] * tau[1] <= tau[0] * high_pair[1])
            if "holds_the_GPT6_ratio_in_its_bracket" in row:
                value = int(row["holds_the_GPT6_ratio_in_its_bracket"])
                check("GPT6_value_in_bracket_%s" % row["weight"], ratio_low <= value + 1 and value - 1 <= ratio_high)
            if "exact_ratio" in row:
                exact = read_frac(row["exact_ratio"])
                check("exact_ratio_%s" % name, low_pair[0] * exact[1] <= exact[0] * low_pair[1] and exact[0] * high_pair[1] <= high_pair[0] * exact[1])
        print("YM4_02D_PLAQUETTES|group=%s|dims=%s|weight=%s|links=%d|plaquettes=%d|orbits=%d|tau=%s|lambda_0_lo=%s|ratio_ppm_low=%s|ratio_ppm_high=%s|json=0" % (
            row["group"], row["dims"], row["weight"], pencil.n_links, pencil.n_plaquettes, pencil.orbits, show(tau), show(lo0), ratio_low, ratio_high))
        cross_ratio(pencil, numerators, name)
        kept[(row["group"], row["dims"])] = (lo0, hi0)
    return kept


FULL_SPACE = (("Z2", (2, 1, 1), "q=1/2"), ("Z3", (2, 1), "1,1/2,1/2"), ("Q8", (1, 1), "r=1/2"))


def section_full_space(kept):
    for name, dims, weight in FULL_SPACE:
        group = group_named(name)
        numerators, denominator = weight_of(group, weight)
        pencil = Pencil(group, numerators, denominator, dims, full_space=True)
        label = "%s_dims_%s" % (name, "x".join(str(d) for d in dims))
        lo0, hi0 = kept[(name, ",".join(str(d) for d in dims))]
        tau = tau_of(numerators, pencil.n_links)
        same_top = pencil.above(lo0) >= 1 and pencil.above(hi0) == 0
        check("full_space_top_is_the_orbit_top_%s" % label, same_top)
        check("full_space_certificate_%s" % label, certificate(pencil, lo0, tau))
        print("YM4_02D_FULL_SPACE|case=%s|dimension=%d|top_in_the_orbit_bracket=%d|certificate=%d|json=0" % (
            label, pencil.orbits, same_top, certificate(pencil, lo0, tau)))


def section_broken():
    rows = {r["name"]: r for r in read_rows("YM4_02D_BROKEN_KERNEL")}
    z3 = group_named("Z3")
    for name in ("negative_weight", "zero_weight"):
        row = rows[name]
        numerators, denominator = weight_of(z3, row["weight"])
        refused = hypotheses(z3, numerators) == name
        check("refused_%s" % name, refused)
        pencil = Pencil(z3, numerators, denominator, (1,))
        spectrum = eigenvalue_list(row["exact_eigenvalues"])
        exact = sum(c for _, c in spectrum) == pencil.orbits and all(pencil.nullity(t) == c for t, c in spectrum)
        check("exact_spectrum_%s" % name, exact)
        if name == "negative_weight":
            magnitudes = [abs(x) for x in numerators]
            tau = tau_of(magnitudes, 1)
            check("tau_from_the_range_of_w_reads_1/3", show(tau) == "1/3")
            top = spectrum[0][0]
            violated = pencil.above(times(tau, top)) == 2
            check("the_bound_is_false_on_%s" % name, violated)
        print("YM4_02D_BROKEN_KERNEL|name=%s|refused=%d|exact_spectrum=%d|json=0" % (name, refused, exact))
    row = rows["asymmetric_weight"]
    numerators, denominator = weight_of(z3, row["weight"])
    refused = hypotheses(z3, numerators) == "asymmetric_weight"
    pencil = Pencil(z3, numerators, denominator, (1,))
    asymmetric = inertia(pencil.at((0, 1)))[2] == -1
    check("refused_asymmetric_weight", refused and asymmetric)
    print("YM4_02D_BROKEN_KERNEL|name=asymmetric_weight|refused=%d|inertia_reports_asymmetric=%d|json=0" % (refused, asymmetric))
    row = rows["half_the_exponent"]
    z2 = group_named("Z2")
    numerators, denominator = weight_of(z2, row["weight"])
    smaller = half_exponent_tau(max(numerators), min(numerators), 1)
    exact = read_frac(row["exact_ratio"])
    check("half_exponent_value", show(smaller) == row["tau_with_half_the_exponent"])
    check("the_smaller_constant_is_false", exact[0] * smaller[1] > smaller[0] * exact[1])
    print("YM4_02D_BROKEN_KERNEL|name=half_the_exponent|tau=%s|exact_ratio=%s|false_here=%d|json=0" % (show(smaller), show(exact), exact[0] * smaller[1] > smaller[0] * exact[1]))


def section_limits():
    modules = sorted(m for m in ("itertools", "math", "os", "sys", "time") if m in sys.modules)
    elapsed = (time.perf_counter_ns() - START_NS) // 1000000000
    within = elapsed <= 600
    check("runtime_within_600_seconds", within)
    print("YM4_02D_LIMITS|runtime_within_600_seconds=%d|modules=%s|json=0" % (within, ",".join(modules)))


def main():
    section_exact()
    kept = section_plaquettes()
    section_full_space(kept)
    section_broken()
    section_limits()
    print("YM4_02D_DONE|failed=%d|json=0" % len(FAILS))
    sys.exit(1 if FAILS else 0)


main()
