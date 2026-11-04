#!/usr/bin/env python3
"""YM4-02c: which weights keep their sign on a fixed slice.

The controls named in docs/PREDICTION-YM4-02c-SITE-SIGN.hbp: rows 1 to 15 pushed at 820f727, rows 17 to 40 at 41f99a2 and row 41 at a56283b,
each before any of them ran. Row 16 is the missed row at 1078e6d. The statement and its proof are docs/NOTE-YM4-02c-SITE-SIGN.md. Q8, 2T, 2O and 2I
are multiplication tables built from exact doubled unit quaternions over the integers, Z[sqrt 2] and Z[phi]; S3, Z3, Z4 and Z5 are tables of permutations;
SU(2) and U(1) are read on exact rational points. Rows rebuilt from measured values are looked up in the prediction file, line by line.

usage = test_site_sign_4d.py [sabotage=NAME]
NAME is one of side_one_in_the_rule count_inverted_classes_apart drop_the_cycle time_like_weight_one, and each must exit 1 on a named check.
An unknown name exits 2. Python standard library, integers only, json=0.
A witness in a row lists, link by link in the lattice's link order, the index of the element in the group's element list.
"""
import collections
import itertools
import math
import os
import sys
import time
import tokenize

START_NS = time.perf_counter_ns()
SABOTAGE_NAMES = ("side_one_in_the_rule", "count_inverted_classes_apart", "drop_the_cycle", "time_like_weight_one")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_site_sign_4d.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []
COUNT = {"off_rule_constant": 0, "on_rule_both": 0, "central_odd": 0, "above_rule_with_the_link": 0, "alive_with_f_negative": 0, "odd_cube": 0}
HERE = os.path.dirname(os.path.abspath(__file__))


def read_rows(name):
    with open(os.path.join(HERE, os.pardir, "docs", name), encoding="utf-8") as handle:
        return [line.rstrip("\r\n") for line in handle]


PREDICTED = read_rows("PREDICTION-YM4-02c-SITE-SIGN.hbp")
EARLIER = read_rows("PREDICTION-YM4-02c.hbp")


def check(name, ok):
    if not ok:
        FAILS.append(name)
    return 1 if ok else 0


def flag(ok):
    return 1 if ok else 0


def in_row(rows, tag, field):
    """1 when a row with this tag holds this exact field between pipes."""
    return flag(any(line.startswith(tag + "|") and ("|" + field + "|") in line for line in rows))


# ---- Exact rings. Z[w] with w^2 = p w + q, an element (a, b) meaning a + b w.
class Ring:
    def __init__(self, name, p, q):
        self.name, self.p, self.q = name, p, q

    def product(self, x, y):
        a, b = x
        c, d = y
        bd = b * d
        return a * c + bd * self.q, a * d + b * c + bd * self.p


RING_Z, RING_ROOT2, RING_PHI = Ring("Z", 0, 0), Ring("Z[sqrt2]", 0, 2), Ring("Z[phi]", 1, 1)
ZERO, UNIT, TWO = (0, 0), (1, 0), (2, 0)


def negate(x):
    return -x[0], -x[1]


def signed(x, sign):
    return x if sign > 0 else negate(x)


# ---- Doubled unit quaternions, four ring elements with squares summing to 4.
# (a + b i + c j + d k)(e + f i + g j + h k), each component a list of (left slot, right slot, sign).
HAMILTON = (
    ((0, 0, 1), (1, 1, -1), (2, 2, -1), (3, 3, -1)),
    ((0, 1, 1), (1, 0, 1), (2, 3, 1), (3, 2, -1)),
    ((0, 2, 1), (1, 3, -1), (2, 0, 1), (3, 1, 1)),
    ((0, 3, 1), (1, 2, 1), (2, 1, -1), (3, 0, 1)),
)


def doubled_product(ring, x, y):
    """The doubled form of the product, which is the product of the doubled forms halved. None when a half leaves the ring."""
    out = []
    for terms in HAMILTON:
        first, second = 0, 0
        for i, j, sign in terms:
            a, b = ring.product(x[i], y[j])
            first += sign * a
            second += sign * b
        if first % 2 or second % 2:
            return None
        out.append((first // 2, second // 2))
    return tuple(out)


def conjugate(x):
    return x[0], negate(x[1]), negate(x[2]), negate(x[3])


def norm(ring, x):
    first, second = 0, 0
    for component in x:
        a, b = ring.product(component, component)
        first += a
        second += b
    return first, second


def q8_elements():
    """+1, -1, +i, -i, +j, -j, +k, -k in this order, so the classes come out as +1, -1, i, j, k."""
    return [tuple(value if slot == axis else ZERO for slot in range(4)) for axis in range(4) for value in (TWO, negate(TWO))]


def hurwitz_extra():
    return [tuple(signed(UNIT, s) for s in signs) for signs in itertools.product((1, -1), repeat=4)]


def octahedral_extra():
    root = (0, 1)
    out = []
    for first, second in itertools.combinations(range(4), 2):
        for s, t in itertools.product((1, -1), repeat=2):
            slots = [ZERO, ZERO, ZERO, ZERO]
            slots[first], slots[second] = signed(root, s), signed(root, t)
            out.append(tuple(slots))
    return out


def icosahedral_extra():
    """Even permutations of (0, +-1, +-1/phi, +-phi), with 1/phi = phi - 1."""
    base = (UNIT, (-1, 1), (0, 1))
    out = []
    for permutation in itertools.permutations(range(4)):
        inversions = sum(1 for i in range(4) for j in range(i + 1, 4) if permutation[i] > permutation[j])
        if inversions % 2 == 0:
            for signs in itertools.product((1, -1), repeat=3):
                values = (ZERO, signed(base[0], signs[0]), signed(base[1], signs[1]), signed(base[2], signs[2]))
                out.append(tuple(values[permutation[slot]] for slot in range(4)))
    return out


class Group:
    def __init__(self, name, ring, elements):
        self.name, self.ring, self.elements = name, ring, elements
        self.order = len(elements)
        self.index = {e: i for i, e in enumerate(elements)}
        self.distinct = len(self.index) == self.order
        self.norm_ok = all(norm(ring, e) == (4, 0) for e in elements)
        self.closure_misses = 0
        self.mult = []
        for x in elements:
            row = []
            for y in elements:
                k = self.index.get(doubled_product(ring, x, y), -1)
                self.closure_misses += 1 if k < 0 else 0
                row.append(k)
            self.mult.append(row)
        self.one = self.index[(TWO, ZERO, ZERO, ZERO)]
        self.minus = self.index[(negate(TWO), ZERO, ZERO, ZERO)]
        self.inv = [self.index.get(conjugate(e), -1) for e in elements]
        self.read_classes()

    def read_classes(self):
        self.classes, self.class_of = self.conjugacy_classes()
        self.merged, self.merged_of = self.merged_with_inverses()
        self.bit = [1 << c for c in self.merged_of]
        self.full = (1 << len(self.merged)) - 1
        self.homomorphisms = self.homomorphism_masks()
        # The rule. A sign pattern with S constant is plus or minus a homomorphism, and the two differ at the identity.
        self.rule = sorted(self.homomorphisms + [mask ^ self.full for mask in self.homomorphisms])

    def associative(self):
        m = self.mult
        for x in range(self.order):
            mx = m[x]
            for y in range(self.order):
                mxy, my = m[mx[y]], m[y]
                for z in range(self.order):
                    if mxy[z] != mx[my[z]]:
                        return False
        return True

    def inverses_ok(self):
        return all(self.inv[g] >= 0 and self.mult[g][self.inv[g]] == self.one and self.mult[self.inv[g]][g] == self.one for g in range(self.order))

    def conjugacy_classes(self):
        m, inv = self.mult, self.inv
        class_of = [-1] * self.order
        classes = []
        for g in range(self.order):
            if class_of[g] < 0:
                members = sorted({m[m[h][g]][inv[h]] for h in range(self.order)})
                for x in members:
                    class_of[x] = len(classes)
                classes.append(members)
        return classes, class_of

    def merged_with_inverses(self):
        merged, merged_of = [], [-1] * self.order
        for c, members in enumerate(self.classes):
            if merged_of[members[0]] < 0:
                together = list(members)
                partner = self.class_of[self.inv[members[0]]]
                if partner != c and SABOTAGE != "count_inverted_classes_apart":
                    together += self.classes[partner]
                for x in together:
                    merged_of[x] = len(merged)
                merged.append(sorted(together))
        return merged, merged_of

    def homomorphism_masks(self):
        """Every homomorphism to {+1, -1} takes one value per inversion-closed class, so reading each pattern against the table finds them all."""
        m = self.mult
        out = []
        for mask in range(1 << len(self.merged)):
            bits = [(mask >> c) & 1 for c in self.merged_of]
            if all(bits[m[x][y]] == bits[x] ^ bits[y] for x in range(self.order) for y in range(self.order)):
                out.append(mask)
        return out

    def index_of_commutators_and_squares(self):
        """The number of homomorphisms a second way: the order of G over the subgroup generated by commutators and squares."""
        m, inv = self.mult, self.inv
        generators = sorted({m[m[m[x][y]][inv[x]]][inv[y]] for x in range(self.order) for y in range(self.order)} | {m[x][x] for x in range(self.order)})
        reached, frontier = {self.one}, [self.one]
        while frontier:
            step = []
            for x in frontier:
                for g in generators:
                    y = m[x][g]
                    if y not in reached:
                        reached.add(y)
                        step.append(y)
            frontier = step
        return self.order // len(reached)

    def epsilon(self, mask):
        return -1 if (mask >> self.merged_of[self.one]) & 1 else 1


class PermutationGroup(Group):
    """A group of permutations, closed from its generators, with its classes and its rule read by the same methods from its own table."""

    def __init__(self, name, generators):
        self.name, self.ring = name, None
        identity = tuple(range(len(generators[0])))
        self.elements, frontier = [identity], [identity]
        seen = {identity}
        while frontier:
            step = []
            for x in frontier:
                for g in generators:
                    y = tuple(x[g[i]] for i in identity)
                    if y not in seen:
                        seen.add(y)
                        self.elements.append(y)
                        step.append(y)
            frontier = step
        self.order = len(self.elements)
        self.index = {e: i for i, e in enumerate(self.elements)}
        self.mult = [[self.index[tuple(x[y[i]] for i in identity)] for y in self.elements] for x in self.elements]
        self.one, self.minus = 0, -1
        self.inv = [row.index(0) for row in self.mult]
        self.read_classes()


BUILT = {}
PERMUTATIONS = {"S3": ((1, 2, 0), (1, 0, 2)), "Z3": ((1, 2, 0),), "Z4": ((1, 2, 3, 0),), "Z5": ((1, 2, 3, 4, 0),)}
ELEMENTS = {
    "Q8": (RING_Z, q8_elements),
    "2T": (RING_Z, lambda: q8_elements() + hurwitz_extra()),
    "2O": (RING_ROOT2, lambda: q8_elements() + hurwitz_extra() + octahedral_extra()),
    "2I": (RING_PHI, lambda: q8_elements() + hurwitz_extra() + icosahedral_extra()),
}
CLASS_SIZES = {"Q8": (1, 1, 2, 2, 2), "2T": (1, 1, 4, 4, 4, 4, 6), "2O": (1, 1, 6, 6, 6, 8, 8, 12), "2I": (1, 1, 12, 12, 12, 12, 20, 20, 30)}
GROUP_NAMES = ("Q8", "2T", "2O", "2I")


def group(name):
    if name not in BUILT:
        if name in PERMUTATIONS:
            BUILT[name] = PermutationGroup(name, PERMUTATIONS[name])
        else:
            ring, elements = ELEMENTS[name]
            BUILT[name] = Group(name, ring, elements())
    return BUILT[name]


def joined(values):
    return ",".join(str(v) for v in values)


def section_groups():
    for name in GROUP_NAMES:
        g = group(name)
        triples = g.order * g.order * g.order
        associative = g.associative()
        inverses = g.inverses_ok()
        sizes = sorted(len(c) for c in g.classes)
        row_ok = g.distinct and g.norm_ok and g.closure_misses == 0 and associative and inverses and tuple(sizes) == CLASS_SIZES[name]
        print("SITE_SIGN_GROUP|group=%s|ring=%s|order=%d|distinct=%d|doubled_norm_4=%d|products_outside_the_group=%d|associative_on_all_%d_triples=%d|inverses=%d|conjugacy_classes=%d|class_sizes=%s|expected_sizes=%s|ok=%d|json=0" % (
            name, g.ring.name, g.order, flag(g.distinct), flag(g.norm_ok), g.closure_misses, triples, flag(associative), flag(inverses), len(g.classes), joined(sizes), joined(CLASS_SIZES[name]), check("%s table" % name, row_ok)))
        classes = len(g.merged)
        patterns = 1 << classes
        closed = all(g.merged_of[g.inv[x]] == g.merged_of[x] for x in range(g.order))
        quotient = g.index_of_commutators_and_squares()
        row = "YM4_02C_SITE_SIGN_PATTERNS|group=%s|order=%d|inversion_closed_classes=%d|patterns=%d|homomorphisms_to_{+1,-1}=%d|constant_patterns=%d|json=0" % (name, g.order, classes, patterns, len(g.homomorphisms), len(g.rule))
        met = row in PREDICTED
        print("SITE_SIGN_PATTERNS|group=%s|order=%d|inversion_closed_classes=%d|each_closed_under_inverse=%d|merged_sizes=%s|patterns=%d|homomorphisms_to_{+1,-1}=%d|index_of_commutators_and_squares=%d|constant_patterns=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
            name, g.order, classes, flag(closed), joined(sorted(len(c) for c in g.merged)), patterns, len(g.homomorphisms), quotient, len(g.rule), flag(met),
            check("%s patterns row equals the prediction" % name, met and closed and quotient == len(g.homomorphisms))))
        if g.closure_misses:
            finish()


# ---- The periodic spatial lattice. A link is (site, direction), read from x to x + direction.
class Lattice:
    def __init__(self, *dims):
        self.dims = dims
        self.k = len(dims)
        self.sites = list(itertools.product(*[range(n) for n in dims]))
        self.position = {x: i for i, x in enumerate(self.sites)}
        self.links = [(x, mu) for x in self.sites for mu in range(self.k)]
        self.link_index = {l: i for i, l in enumerate(self.links)}
        self.plaquettes = [(x, mu, nu) for x in self.sites for mu in range(self.k) for nu in range(mu + 1, self.k)]
        # U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1, the repository's convention, as (a, b, c, d) with c and d inverted.
        self.faces = [(self.link_index[(x, mu)], self.link_index[(self.shift(x, mu), nu)], self.link_index[(self.shift(x, nu), mu)], self.link_index[(x, nu)]) for x, mu, nu in self.plaquettes]
        self.ends = [(self.position[x], self.position[self.shift(x, mu)]) for x, mu in self.links]
        self.name = lattice_name(dims)

    def shift(self, x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % self.dims[mu]
        return tuple(y)


def lattice_name(dims):
    if len(dims) >= 3 and len(set(dims)) == 1:
        return "(Z/%d)^%d" % (dims[0], len(dims))
    return "x".join("(Z/%d)" % d for d in dims)


def face_value(q, config, face):
    m, inv = q.mult, q.inv
    a, b, c, d = face
    return m[m[m[config[a]][config[b]]][inv[config[c]]]][inv[config[d]]]


def parity_of(q, lat, config):
    """Bit c holds the parity of the number of plaquettes in inversion-closed class c. S for a pattern is the sign of its overlap with this."""
    out = 0
    for face in lat.faces:
        out ^= q.bit[face_value(q, config, face)]
    return out


def sign_on(mask, parity):
    return -1 if (mask & parity).bit_count() & 1 else 1


def values_of_s(mask, parities):
    return {sign_on(mask, p) for p in parities}


def lattice_facts(lat):
    in_faces = [[] for _ in lat.links]
    for position, face in enumerate(lat.faces):
        for l in face:
            in_faces[l].append(position)
    four_distinct = all(len(set(face)) == 4 for face in lat.faces)
    once_each = all(len(set(v)) == len(v) for v in in_faces)
    right_count = all(len(v) == 2 * (lat.k - 1) for v in in_faces)
    even_use = all(len(v) % 2 == 0 for v in in_faces)
    # Step 4 of the proof: at each link, each staple holds a link found once in that staple and in no other staple of that link.
    exclusive = True
    for l, positions in enumerate(in_faces):
        staples = [[x for x in lat.faces[p] if x != l] for p in sorted(set(positions))]
        for i, staple in enumerate(staples):
            others = [x for j, other in enumerate(staples) if j != i for x in other]
            if not any(staple.count(x) == 1 and x not in others for x in staple):
                exclusive = False
    return four_distinct, once_each, right_count, even_use, exclusive


def section_lattices():
    """Sides at least 2 read all ones here. A side of 1 shows where the hypotheses of the note stop holding."""
    for dims, expected_full in (((2, 2), True), ((2, 3), True), ((2, 2, 2), True), ((3, 3), True), ((2, 2, 3), True), ((2, 1), False), ((1, 1), False), ((2, 1, 2), False)):
        lat = Lattice(*dims)
        four_distinct, once_each, right_count, even_use, exclusive = lattice_facts(lat)
        full = four_distinct and once_each and exclusive
        print("SITE_SIGN_LATTICE|lattice=%s|k=%d|sites=%d|links=%d|plaquettes=%d|each_plaquette_holds_four_distinct_links=%d|each_link_once_in_each_of_its_plaquettes=%d|each_link_used_2(k-1)_times=%d|each_link_used_an_even_number_of_times=%d|each_staple_holds_an_exclusive_link=%d|ok=%d|json=0" % (
            lat.name, lat.k, len(lat.sites), len(lat.links), len(lat.plaquettes), flag(four_distinct), flag(once_each), flag(right_count), flag(even_use), flag(exclusive),
            check("lattice facts on %s" % lat.name, full == expected_full and right_count and even_use)))


# ---- A plain linear congruential stream, so that the configurations are the same on every Python.
class Stream:
    def __init__(self, seed):
        self.state = seed

    def below(self, n):
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % 2 ** 64
        return (self.state >> 33) % n


def spanning_tree(lat):
    """One link for each site other than the origin, found outward from the origin."""
    seen = {lat.sites[0]}
    tree, frontier = [], [lat.sites[0]]
    while frontier:
        step = []
        for x in frontier:
            for mu in range(lat.k):
                y = lat.shift(x, mu)
                if y not in seen:
                    seen.add(y)
                    tree.append(lat.link_index[(x, mu)])
                    step.append(y)
        frontier = step
    return tree


def gauge_moved(q, lat, config, gauge):
    m, inv = q.mult, q.inv
    return [m[m[gauge[s]][u]][inv[gauge[r]]] for u, (s, r) in zip(config, lat.ends)]


def mask_of_weight(w):
    return sum(1 << c for c, value in enumerate(w) if value < 0)


FIVE_CASES = ((3, 2, 1, -1, -2), (1, 1, 1, -1, -1), (-1, -1, -1, -1, -1), (3, 2, 1, -1, 2), (1, -1, 1, 1, 1))


def section_exhaustive():
    """Q8 on (Z/2)x(Z/2) over 8^5 gauge-fixed configurations. S is unchanged by a gauge move since s is a class function, and with the origin
    held fixed each gauge orbit meets the set with the spanning tree at 1 exactly once, so this set sees every value of S on all 8^8 configurations."""
    q = group("Q8")
    lat = Lattice(*((2, 1) if SABOTAGE == "side_one_in_the_rule" else (2, 2)))
    tree = spanning_tree(lat)
    free = [i for i in range(len(lat.links)) if i not in tree]
    config = [q.one] * len(lat.links)
    parities = collections.Counter()
    negatives = [0] * len(FIVE_CASES)
    agree = True
    for values in itertools.product(range(q.order), repeat=len(free)):
        for slot, value in zip(free, values):
            config[slot] = value
        classes = [q.merged_of[face_value(q, config, face)] for face in lat.faces]
        parity = 0
        for c in classes:
            parity ^= 1 << c
        parities[parity] += 1
        for case, w in enumerate(FIVE_CASES):
            product = 1
            for c in classes:
                product *= w[c]
            if product < 0:
                negatives[case] += 1
            if (product < 0) != (sign_on(mask_of_weight(w), parity) < 0):
                agree = False
    read = sum(parities.values())
    patterns = 1 << len(q.merged)
    constant = [mask for mask in range(patterns) if len(values_of_s(mask, parities)) == 1]
    rule_met = constant == q.rule
    on_rule_values = sorted({sign_on(mask, parity) for mask in q.rule for parity in parities})
    fewest = read
    for mask in range(patterns):
        if mask not in q.rule:
            minus_count = sum(n for parity, n in parities.items() if sign_on(mask, parity) < 0)
            fewest = min(fewest, minus_count, read - minus_count)
    COUNT["off_rule_constant"] += sum(1 for mask in constant if mask not in q.rule)
    COUNT["on_rule_both"] += sum(1 for mask in q.rule if mask not in constant)
    print("SITE_SIGN_EXHAUSTIVE|group=Q8|lattice=%s|sites=%d|links=%d|tree_links=%d|free_links=%d|configurations_read=%d|expected=8^5=%d|plaquettes=%d|patterns=%d|constant_patterns=%d|equal_to_plus_or_minus_homomorphisms=%d|S_on_each_constant_pattern=%s|fewest_configurations_on_either_sign_off_the_rule=%d|ok=%d|json=0" % (
        lat.name, len(lat.sites), len(lat.links), len(tree), len(free), read, 8 ** 5, len(lat.plaquettes), patterns, len(constant), flag(rule_met),
        joined(on_rule_values), fewest, check("Q8 exhaustive keeps exactly the patterns of the rule", rule_met and len(constant) == 8)))
    check("Q8 exhaustive reads 8^5 configurations", read == 8 ** 5)
    fields = []
    for number, w in enumerate(FIVE_CASES):
        on_rule = mask_of_weight(w) in q.rule
        count_field = "0" if negatives[number] == 0 else "above_0"
        fields.append(("case_%d=w_%s:sign_is_a_homomorphism_%d:negative_product_%s" % (number + 1, joined(w), flag(on_rule), count_field), negatives[number]))
    earlier = all(in_row(EARLIER, "YM4_02C_SITE_CHARACTER", text) for text, _ in fields)
    print("SITE_SIGN_FIVE_CASES|group=Q8|lattice=%s|gauge_fixed_configurations=%d|%s|products_agree_with_S=%d|each_case_in_the_earlier_row=%d|ok=%d|json=0" % (
        lat.name, read, "|".join("%s:count_%d" % field for field in fields), flag(agree), flag(earlier), check("five Q8 cases", agree and earlier)))


# ---- A second route to the same counts. On a two-dimensional torus each link occurs once forward and once backward, so integrating out the links gives
# mean S = sum over irreducible rho of (c_rho / d_rho)^F, for s = sum c_rho chi_rho, at every side including a side of 1. Exact integers, with the
# characters of Q8 read from its table: the homomorphisms, and the doubled real part, which is the trace of the 2-dimensional representation.
def section_torus_route():
    q = group("Q8")
    sizes = [len(members) for members in q.merged]
    classes = range(len(q.merged))
    characters = [[1 - 2 * ((mask >> c) & 1) for c in classes] for mask in q.homomorphisms] + [[q.elements[members[0]][0][0] for members in q.merged]]
    degrees = [1] * len(q.homomorphisms) + [2]
    orthonormal = all(sum(sizes[c] * characters[a][c] * characters[b][c] for c in classes) == (q.order if a == b else 0) for a in range(len(degrees)) for b in range(len(degrees)))
    print("SITE_SIGN_TORUS_CHARACTERS|group=Q8|irreducible=%d|degrees=%s|orthonormal=%d|ok=%d|json=0" % (len(degrees), joined(degrees), flag(orthonormal), check("Q8 characters", orthonormal and len(degrees) == len(q.merged))))
    for dims, expected_constant in (((2, 2), 8), ((2, 1), 16), ((1, 1), 16)):
        lat = Lattice(*dims)
        total_faces = len(lat.faces)
        tree = spanning_tree(lat)
        free = [i for i in range(len(lat.links)) if i not in tree]
        config = [q.one] * len(lat.links)
        parities = collections.Counter()
        for values in itertools.product(range(q.order), repeat=len(free)):
            for slot, value in zip(free, values):
                config[slot] = value
            parities[parity_of(q, lat, config)] += 1
        read = sum(parities.values())
        matches, extreme = 0, 0
        for mask in range(1 << len(q.merged)):
            signs = [1 - 2 * ((mask >> c) & 1) for c in classes]
            # c_rho / d_rho = n_rho / (8 d_rho) = n_rho (2 // d_rho) / 16, and d_rho divides 2.
            scaled = [sum(sizes[c] * signs[c] * chi[c] for c in classes) * (2 // degree) for chi, degree in zip(characters, degrees)]
            top = sum(n ** total_faces for n in scaled)
            mean = sum(n * sign_on(mask, parity) for parity, n in parities.items())
            matches += 1 if top * read == mean * 16 ** total_faces else 0
            extreme += 1 if abs(mean) == read else 0
        print("SITE_SIGN_TORUS_ROUTE|group=Q8|lattice=%s|plaquettes=%d|gauge_fixed_configurations=%d|patterns_where_the_mean_of_S_equals_the_character_sum=%d_of_%d|patterns_with_mean_+1_or_-1=%d|ok=%d|json=0" % (
            lat.name, total_faces, read, matches, 1 << len(q.merged), extreme, check("torus route on %s" % lat.name, matches == 1 << len(q.merged) and extreme == expected_constant)))


# ---- Witnesses, for every other group and lattice.
WITNESS_DRAWS, WITNESS_BOUND = 4096, 1 << 20
WITNESS_LATTICES = ((2, 2), (2, 3), (2, 2, 2))
ADDED_LATTICE = (3, 3)


def exact_classes(q, lat, config):
    """The plaquette classes by exact ring arithmetic on the quaternions themselves, with the table left out."""
    e = q.elements
    out = []
    for a, b, c, d in lat.faces:
        x = doubled_product(q.ring, e[config[a]], e[config[b]])
        x = doubled_product(q.ring, x, conjugate(e[config[c]]))
        x = doubled_product(q.ring, x, conjugate(e[config[d]]))
        out.append(q.merged_of[q.index[x]])
    return out


def direct_s(mask, classes):
    value = 1
    for c in classes:
        if (mask >> c) & 1:
            value = -value
    return value


def predicted_constant(q, mask, plaquettes):
    return -1 if q.epsilon(mask) < 0 and plaquettes % 2 else 1


def read_witnesses(q, dims, seed, added):
    lat = Lattice(*dims)
    stream = Stream(seed)
    width, plaquettes = len(lat.links), len(lat.faces)
    classes = len(q.merged)
    target = classes - (len(q.rule).bit_length() - 1)
    expected = {mask: predicted_constant(q, mask, plaquettes) for mask in q.rule}
    seen, witnesses, reduced = set(), [], []
    base, draws, on_rule_constant = -1, 0, True
    while draws < WITNESS_DRAWS or (len(reduced) < target and draws < WITNESS_BOUND):
        draws += 1
        config = [stream.below(q.order) for _ in range(width)]
        parity = parity_of(q, lat, config)
        if parity in seen:
            continue
        seen.add(parity)
        if any(sign_on(mask, parity) != expected[mask] for mask in q.rule):
            on_rule_constant = False
        if base < 0:
            base = parity
            witnesses.append(config)
        else:
            difference = parity ^ base
            for lead, value in reduced:
                if (difference >> lead) & 1:
                    difference ^= value
            if difference:
                reduced.append((difference.bit_length() - 1, difference))
                witnesses.append(config)
    # The patterns are read on the witnesses alone, by exact ring arithmetic, one plaquette at a time.
    recheck = [exact_classes(q, lat, config) for config in witnesses]
    exact_ok, gauge_ok = True, True
    for config, face_classes in zip(witnesses, recheck):
        from_exact = 0
        for c in face_classes:
            from_exact ^= 1 << c
        exact_ok = exact_ok and from_exact == parity_of(q, lat, config)
        moved = gauge_moved(q, lat, config, [stream.below(q.order) for _ in lat.sites])
        gauge_ok = gauge_ok and [q.merged_of[face_value(q, moved, face)] for face in lat.faces] == face_classes
    both, off_rule, on_rule_ok = 0, 0, True
    constant = []
    for mask in range(1 << classes):
        values = {direct_s(mask, face_classes) for face_classes in recheck}
        if len(values) == 1:
            constant.append(mask)
        if mask in q.rule:
            on_rule_ok = on_rule_ok and values == {expected[mask]}
        else:
            off_rule += 1
            both += 1 if len(values) == 2 else 0
    on_rule_ok = on_rule_ok and on_rule_constant
    at_plus = sorted({direct_s(mask, face_classes) for mask in q.rule if q.epsilon(mask) > 0 for face_classes in recheck})
    at_minus = sorted({direct_s(mask, face_classes) for mask in q.rule if q.epsilon(mask) < 0 for face_classes in recheck})
    COUNT["off_rule_constant"] += off_rule - both
    COUNT["on_rule_both"] += 0 if on_rule_ok else 1
    ok = both == off_rule and on_rule_ok and exact_ok and gauge_ok and len(reduced) == target
    label = "%s on %s" % (q.name, lat.name)
    print("SITE_SIGN_WITNESS|group=%s|lattice=%s|added_beside_the_prediction=%d|plaquettes=%d|patterns=%d|on_the_rule=%d|off_the_rule=%d|draws=%d|distinct_parity_vectors=%d|affine_dimension=%d|classes_minus_log2_constant=%d|off_rule_showing_both_values_of_S=%d|on_rule_equal_to_the_predicted_constant_on_every_configuration_read=%d|S_read_at_epsilon_+1=%s|S_read_at_epsilon_-1=%s|witness_configurations=%d|exact_ring_recheck=%d|gauge_moved_witnesses_read_the_same_classes=%d|witnesses=%s|ok=%d|json=0" % (
        q.name, lat.name, flag(added), plaquettes, 1 << classes, len(q.rule), off_rule, draws, len(seen), len(reduced), target, both, flag(on_rule_ok), joined(at_plus), joined(at_minus), len(witnesses), flag(exact_ok), flag(gauge_ok),
        ";".join(".".join(str(v) for v in config) for config in witnesses), check("witnesses for %s" % label, ok)))
    return constant, draws


def section_witnesses():
    for name in GROUP_NAMES:
        q = group(name)
        for number, dims in enumerate(WITNESS_LATTICES):
            read_witnesses(q, dims, 1000 * (GROUP_NAMES.index(name) + 1) + number, False)
        # A fourth lattice, with an odd number of plaquettes, so that the constant for epsilon = -1 reads -1. The three named lattices all have an even number.
        read_witnesses(q, ADDED_LATTICE, 1000 * (GROUP_NAMES.index(name) + 1) + 9, True)


# ---- Side 1, where the hypotheses of the note stop holding.
def section_side_one():
    q = group("Q8")
    m, cls = q.mult, q.merged_of
    lat = Lattice(2, 1)
    first_face, second_face = lat.faces
    pairs = collections.Counter()
    inverse_pairs, up_to_centre, same_class, both_central, different_sign = 0, 0, 0, 0, 0
    for config in itertools.product(range(q.order), repeat=len(lat.links)):
        p0, p1 = face_value(q, config, first_face), face_value(q, config, second_face)
        c0, c1 = cls[p0], cls[p1]
        pairs[(c0, c1)] += 1
        inverse_pairs += 1 if p1 == q.inv[p0] else 0
        up_to_centre += 1 if c0 == c1 or cls[m[q.minus][p1]] == c0 else 0
        same_class += 1 if c0 == c1 else 0
        if c0 < 2 and c1 < 2:
            both_central += 1
            different_sign += 1 if c0 != c1 else 0
    read = sum(pairs.values())
    named = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (3, 3), (4, 4))
    class_pairs = joined(pairs[pair] for pair in named)
    other = read - sum(pairs[pair] for pair in named)
    field = in_row(PREDICTED, "YM4_02C_SITE_SIGN_ALREADY_SEEN", "class_pairs=%s" % class_pairs)
    print("SITE_SIGN_SIDE_ONE_PAIRS|lattice=%s|group=Q8|configurations=%d|class_pairs_on_+1,+1;+1,-1;-1,+1;-1,-1;i,i;j,j;k,k=%s|every_other_pair=%d|found_in_ALREADY_SEEN=%d|ok=%d|json=0" % (
        lat.name, read, class_pairs, other, field, check("class pairs on (Z/2)x(Z/1)", bool(field) and other == 0)))
    reproduced = (inverse_pairs, same_class, both_central, different_sign, up_to_centre) == (2176, 3712, 1024, 384, 4096)
    print("SITE_SIGN_SIDE_ONE_HOLONOMIES|lattice=%s|group=Q8|configurations=%d|second_is_the_inverse_of_the_first=%d|same_class=%d|same_class_up_to_the_centre=%d|both_central=%d|central_with_different_sign=%d|beside=reviews/fable5-q8-slice-count/RECEIPT.hbp|ok=%d|json=0" % (
        lat.name, read, inverse_pairs, same_class, up_to_centre, both_central, different_sign, check("holonomy counts on (Z/2)x(Z/1)", reproduced)))
    parities = collections.Counter()
    for (c0, c1), n in pairs.items():
        parities[(1 << c0) ^ (1 << c1)] += n
    constant = [mask for mask in range(1 << 5) if len(values_of_s(mask, parities)) == 1]
    rule_inside = all(mask in constant for mask in q.rule)
    weights = ((3, 2, 1, -1, -2), (1, 1, 1, -1, -1), (3, 2, 1, -1, 2), (1, -1, 1, 1, 1))
    expected_weights = ((0, 2048), (0, 2048), (0, 1024), (384, 512))
    read_weights = []
    for w in weights:
        negative = sum(n for (c0, c1), n in pairs.items() if w[c0] * w[c1] < 0)
        single = sum(n for (c0, c1), n in pairs.items() if w[c0] < 0)
        read_weights.append((negative, single))
    print("SITE_SIGN_SIDE_ONE_WEIGHTS|lattice=%s|group=Q8|%s|beside=reviews/fable5-q8-slice-count/RECEIPT.hbp|ok=%d|json=0" % (
        lat.name, "|".join("w_%s=negative_product_%d:negative_at_first_plaquette_%d" % (joined(w), read_weights[i][0], read_weights[i][1]) for i, w in enumerate(weights)),
        check("weights on (Z/2)x(Z/1)", tuple(read_weights) == expected_weights)))
    # The field second_seat_saw in ALREADY_SEEN names the fixed slice of the lattice with T = 2, and the row above reads that slice.
    saw = "second_seat_saw=w_%s_stays_positive_on_(Z/2)x(Z/1)x(Z/2)" % joined(weights[0])
    reference = "YM4_02C_SITE_SIGN_REFERENCE|beside=YM4_02C_SITE_SIGN_ALREADY_SEEN|field=second_seat_saw|object=the_fixed_slice_%s_of_the_lattice_(Z/2)x(Z/1)x(Z/2)_with_T=2|read_by=SITE_SIGN_SIDE_ONE_WEIGHTS:w_%s=negative_product_%d|the_row_named_SITE_SIGN_SECOND_SEAT_at_1078e6d_is_now=SITE_SIGN_SPATIAL_PRODUCT:all_12_plaquettes_of_a_spatial_(Z/2)x(Z/1)x(Z/2)|json=0" % (lat.name, joined(weights[0]), read_weights[0][0])
    print("SITE_SIGN_ALREADY_SEEN_READ|field=%s|field_found_in_ALREADY_SEEN=%d|slice=%s|negative_product=%d_of_%d|reference_row_found_in_the_prediction=%d|ok=%d|json=0" % (
        saw, in_row(PREDICTED, "YM4_02C_SITE_SIGN_ALREADY_SEEN", saw), lat.name, read_weights[0][0], read, flag(reference in PREDICTED), check("the reference beside ALREADY_SEEN", bool(in_row(PREDICTED, "YM4_02C_SITE_SIGN_ALREADY_SEEN", saw)) and reference in PREDICTED and read_weights[0][0] == 0)))
    off_rule_weight, negative_weight = (3, 2, 1, -1, 2), (1, -1, 1, 1, 1)
    off_rule_constant = mask_of_weight(off_rule_weight) in constant and mask_of_weight(off_rule_weight) not in q.rule
    corner = Lattice(1, 1)
    values = collections.Counter(cls[face_value(q, config, corner.faces[0])] for config in itertools.product(range(q.order), repeat=len(corner.links)))
    corner_read = sum(values.values())
    corner_constant = [mask for mask in range(1 << 5) if len(values_of_s(mask, {1 << c for c in values})) == 1]
    at_plus, at_minus = [], []
    for mask in range(1 << 5):
        if (mask & 1) != ((mask >> 1) & 1):
            count = sum(n for c, n in values.items() if (mask >> c) & 1)
            (at_minus if mask & 1 else at_plus).append(count)
    print("SITE_SIGN_SIDE_ONE_CORNER|lattice=%s|group=Q8|configurations=%d|commutator_+1=%d|commutator_-1=%d|constant_patterns=%d_of_%d|patterns_with_s(-1)=-s(1)=%d|negative_S_with_s(1)=+1=%s|negative_S_with_s(1)=-1=%s|value_opposite_s(1)=%d_of_%d|ok=%d|json=0" % (
        corner.name, corner_read, values[0], values[1], len(corner_constant), 1 << 5, len(at_plus) + len(at_minus), joined(sorted(set(at_plus))), joined(sorted(set(at_minus))), values[1], corner_read,
        check("commutators on (Z/1)x(Z/1)", values[0] == 40 and values[1] == 24 and at_plus == [24] * 8 and at_minus == [40] * 8)))
    row = "YM4_02C_SITE_SIGN_SIDE_ONE|lattice=%s|group=Q8|configurations=%d|constant_patterns=%d_of_%d|w_3,2,1,-1,2=constant_and_no_homomorphism|w_1,-1,1,1,1=negative_on_%d|lattice=%s|configurations=%d|constant_patterns=%d_of_%d|negative_for_s(-1)=-s(1)=%d_of_%d|json=0" % (
        lat.name, read, len(constant), 1 << 5, sum(n for (c0, c1), n in pairs.items() if negative_weight[c0] * negative_weight[c1] < 0), corner.name, corner_read, len(corner_constant), 1 << 5, at_plus[0], corner_read)
    found = row in PREDICTED
    literal = all(count == 24 for count in at_plus + at_minus)
    print("SITE_SIGN_SIDE_ONE|lattice=%s|constant_patterns=%d_of_%d|rule_patterns_inside=%d|w_3,2,1,-1,2=constant_%d|row_found_with_the_value_at_s(1)=+1=%d|value_met_on_all_16_patterns=%d|ok=%d|json=0" % (
        lat.name, len(constant), 1 << 5, flag(rule_inside), flag(off_rule_constant), flag(found), flag(literal),
        check("side one row", found and rule_inside and off_rule_constant and len(constant) == 16 and len(corner_constant) == 16)))
    if not literal:
        miss = "YM4_02C_SITE_SIGN_MISS|beside=YM4_02C_SITE_SIGN_SIDE_ONE|lattice=%s|said=negative_for_s(-1)=-s(1)=24_of_64|measured=%s_of_%d_on_the_%d_patterns_with_s(1)=+1:%s_of_%d_on_the_%d_patterns_with_s(1)=-1|what_holds_on_all_%d=the_value_opposite_s(1)_sits_on_%d_of_%d|found_by=this_run|tag=MEASURED|json=0" % (
            corner.name, joined(sorted(set(at_plus))), corner_read, len(at_plus), joined(sorted(set(at_minus))), corner_read, len(at_minus), len(at_plus) + len(at_minus), values[1], corner_read)
        print(miss)
        print("SITE_SIGN_MISS_BESIDE|line_16_of_the_prediction_is_the_row_above=%d|ok=%d|json=0" % (flag(PREDICTED[15] == miss), check("the missed row stands as line 16", PREDICTED[15] == miss)))


def section_spatial_product():
    """The product over all 12 plaquettes of a spatial (Z/2)x(Z/1)x(Z/2): the sign of this weight is a homomorphism, and each link is used an even number of times, so every such product is positive."""
    q = group("Q8")
    lat = Lattice(2, 1, 2)
    w = (3, 2, 1, -1, -2)
    mask = mask_of_weight(w)
    _, _, _, even_use, _ = lattice_facts(lat)
    stream = Stream(77)
    draws, negative = 1 << 14, 0
    for _ in range(draws):
        config = [stream.below(q.order) for _ in lat.links]
        product = 1
        for face in lat.faces:
            product *= w[q.merged_of[face_value(q, config, face)]]
        negative += 1 if product <= 0 else 0
    print("SITE_SIGN_SPATIAL_PRODUCT|lattice=%s|group=Q8|w=%s|sign_is_a_homomorphism=%d|each_link_used_an_even_number_of_times=%d|plaquettes=%d|fixed_seed_draws=%d|products_at_or_below_0=%d|on_every_configuration=positive_DERIVED_from_these_two_facts|ok=%d|json=0" % (
        lat.name, joined(w), flag(mask in q.homomorphisms), flag(even_use), len(lat.faces), draws, negative, check("product over all plaquettes stays positive", mask in q.homomorphisms and even_use and negative == 0)))


# ---- The side hypothesis. The proof uses every side at least 2, and the conclusion needs one link: l held once by a plaquette p, with a link e held once by p
# and by no other plaquette holding l. Then S = s(u y) A(u, rest) B(e, rest), with y Haar in e, A free of e and B free of u, and two values y, z give Step 5.
def the_argument_has_its_link(lat):
    holding = [[f for f, face in enumerate(lat.faces) if l in face] for l in range(len(lat.links))]
    for l, faces_of_l in enumerate(holding):
        for f in faces_of_l:
            face = lat.faces[f]
            if face.count(l) == 1:
                for e in face:
                    if e != l and face.count(e) == 1 and all(e not in lat.faces[other] for other in faces_of_l if other != f):
                        return True
    return False


def two_sides_or_a_long_one(dims):
    return sum(1 for side in dims if side >= 2) >= 2 or max(dims) >= 3


LINK_LATTICES = ((2, 2), (2, 3), (3, 1), (4, 1), (2, 1, 2), (3, 1, 1), (3, 1, 1, 1), (2, 1), (1, 1), (2, 1, 1), (1, 1, 1), (2, 1, 1, 1), (1, 1, 1, 1))
# A seed of 0 reads the pair exhaustively, and any other seed reads it by witnesses.
SIDE_COUNTS = (("Q8", (3, 1), 0), ("Q8", (2, 1, 2), 702), ("Q8", (2, 1, 1), 0), ("Q8", (1, 1, 1), 0), ("S3", (2, 1), 0), ("2I", (2, 1), 706))


def exhaustive_parities(q, lat):
    tree = spanning_tree(lat)
    free = [i for i in range(len(lat.links)) if i not in tree]
    config = [q.one] * len(lat.links)
    parities = collections.Counter()
    for values in itertools.product(range(q.order), repeat=len(free)):
        for slot, value in zip(free, values):
            config[slot] = value
        parities[parity_of(q, lat, config)] += 1
    return parities, free


def section_side_counts():
    agree, names = 0, []
    for dims in LINK_LATTICES:
        lat = Lattice(*dims)
        names.append(lat.name)
        agree += 1 if the_argument_has_its_link(lat) == two_sides_or_a_long_one(dims) else 0
    row = "YM4_02C_SITE_SIGN_SIDES_LINK|a_link_held_once_by_a_plaquette_with_another_link_held_once_and_in_no_other_plaquette_of_the_first=exists_exactly_at_two_sides_at_least_2_or_one_side_at_least_3|lattices=%s|agree=%d_of_%d|json=0" % (",".join(names), agree, len(names))
    print("SITE_SIGN_SIDES_LINK|lattices=%d|agree=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (len(names), agree, flag(row in PREDICTED), check("the argument's link exists exactly where it claims", row in PREDICTED)))
    for name, dims, seed in SIDE_COUNTS:
        q = group(name)
        lat = Lattice(*dims)
        patterns = 1 << len(q.merged)
        if seed == 0:
            parities, free = exhaustive_parities(q, lat)
            constant = [mask for mask in range(patterns) if len(values_of_s(mask, parities)) == 1]
            read_text = "exhaustive_over_%d^%d_gauge_fixed_configurations" % (q.order, len(free))
            configurations, read_ok = sum(parities.values()), sum(parities.values()) == q.order ** len(free)
        else:
            constant, configurations = read_witnesses(q, dims, seed, False)
            read_text, read_ok = "witnesses_rechecked_by_ring_arithmetic", True
        rule_inside = all(mask in constant for mask in q.rule)
        centre_pair = [mask for mask in range(patterns) if q.minus >= 0 and (mask >> q.merged_of[q.one]) & 1 == (mask >> q.merged_of[q.minus]) & 1]
        the_set = "the_rule" if constant == q.rule else "s(1)=s(-1)" if constant == centre_pair else "another_set"
        row = "YM4_02C_SITE_SIGN_SIDE_COUNT|group=%s|lattice=%s|read=%s|constant_patterns=%d_of_%d|the_constant_set=%s|json=0" % (name, lat.name, read_text, len(constant), patterns, the_set)
        found = row in PREDICTED
        link = the_argument_has_its_link(lat)
        COUNT["above_rule_with_the_link"] += sum(1 for mask in constant if mask not in q.rule) if link else 0
        print("SITE_SIGN_SIDE_COUNT|group=%s|lattice=%s|plaquettes=%d|read=%s|configurations_read=%d|patterns=%d|on_the_rule=%d|rule_inside=%d|constant_patterns=%d|the_constant_set=%s|the_argument_has_its_link=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
            name, lat.name, len(lat.faces), read_text, configurations, patterns, len(q.rule), flag(rule_inside), len(constant), the_set, flag(link), flag(found), check("side count for %s on %s" % (name, lat.name), found and rule_inside and read_ok)))


def section_u1():
    """U(1) at (Z/2)x(Z/1): the connected case. The two plaquettes are U_1(1) U_1(0)^-1 and its inverse, read on exact rational points of the circle and on three cyclic subgroups."""
    lat = Lattice(2, 1)
    first, second = lat.faces
    on_the_circle = all(a * a + b * b == den * den and c == 0 and d == 0 for a, b, c, d, den in CIRCLE)
    read, inverse, negative, s_plus = 0, 0, 0, 0
    for config in itertools.product(range(len(CIRCLE)), repeat=len(lat.links)):
        links = [CIRCLE[i] for i in config]
        p0, p1 = rational_word(links, first), rational_word(links, second)
        read += 1
        inverse += 1 if p1 == rational_inverse(p0) else 0
        negative += 1 if p0[0] < 0 else 0
        s_plus += 1 if p0[0] * p1[0] > 0 else 0
    parts = []
    for name in ("Z3", "Z4", "Z5"):
        q = group(name)
        parities, _ = exhaustive_parities(q, lat)
        patterns = 1 << len(q.merged)
        parts.append("%s:%d_of_%d:rule_%d" % (name, sum(1 for mask in range(patterns) if len(values_of_s(mask, parities)) == 1), patterns, len(q.rule)))
    row = "YM4_02C_SITE_SIGN_U1|group=U(1)|lattice=%s|the_second_plaquette_is_the_inverse_of_the_first|S=+1_for_every_sign_with_s(g^-1)=s(g)|exact_rational_points_of_the_circle=%d^%d_configurations|second_is_the_inverse=%d_of_%d|a_p_negative_at_the_first_plaquette=%s|S_for_a_p=+1_on_%d_of_%d|subgroups=%s|tag=the_connected_case_DERIVED|json=0" % (
        lat.name, len(CIRCLE), len(lat.links), inverse, read, "above_0" if negative else "0", s_plus, read, ",".join(parts))
    found = row in PREDICTED
    print("SITE_SIGN_U1|group=U(1)|lattice=%s|configurations=%d|on_the_circle=%d|second_is_the_inverse=%d|a_p_negative_at_the_first_plaquette=%d|S_for_a_p_+1=%d|subgroups=%s|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        lat.name, read, flag(on_the_circle), inverse, negative, s_plus, ",".join(parts), flag(found), check("U(1) at (Z/2)x(Z/1)", found and on_the_circle)))


BANDS = (((0, 1),), ((1, 2),), ((-1, 2),), ((3, 4),), ((-3, 4),), ((9, 10),), ((-9, 10),), ((-1, 2), (1, 2)), ((1, 4), (3, 4)), ((-3, 4), (-1, 4)), ((-9, 10), (9, 10)), ((-1, 2), (0, 1), (1, 2)), ((-3, 4), (-1, 2), (-1, 4), (1, 4), (1, 2), (3, 4)))
BAND_LATTICES = (((2, 1), 801), ((1, 1), 802), ((3, 1), 803), ((2, 1, 1), 804), ((1, 1, 1), 805), ((2, 1, 2), 806))


def band_sign(x, cuts):
    """+1 or -1 by the parity of the cuts below the real part of x, and 0 on a cut."""
    a, den = x[0], x[4]
    count = 0
    for top, bottom in cuts:
        left, right = a * bottom, top * den
        if left == right:
            return 0
        count += 1 if left > right else 0
    return -1 if count % 2 else 1


def section_su2_bands():
    names, reads, units_ok = [], [], True
    for dims, seed in BAND_LATTICES:
        lat = Lattice(*dims)
        stream = Stream(seed)
        both, most = 0, 0
        for cuts in BANDS:
            values, draws = set(), 0
            while len(values) < 2 and draws < 1 << 14:
                draws += 1
                links = [rational_unit(stream, 7, 1 + stream.below(7)) for _ in lat.links]
                units_ok = units_ok and all(is_rational_unit(x) for x in links)
                s = 1
                for face in lat.faces:
                    s *= band_sign(rational_word(links, face), cuts)
                    if s == 0:
                        break
                if s:
                    values.add(s)
            both += 1 if len(values) == 2 else 0
            most = max(most, draws)
        names.append(lat.name)
        reads.append((lat.name, both, most))
    every = all(both == len(BANDS) for _, both, _ in reads)
    row = "YM4_02C_SITE_SIGN_SU2_BANDS|group=SU(2)|exact_rational_unit_quaternions=%d|sign_of_the_real_part_on_bands=%d_patterns_with_a_p_among_them|lattices=%s|patterns_showing_both_values_of_S=%d_of_%d_on_each|json=0" % (flag(units_ok), len(BANDS), ",".join(names), len(BANDS) if every else 0, len(BANDS))
    found = row in PREDICTED
    print("SITE_SIGN_SU2_BANDS|%s|row_found_in_the_prediction=%d|ok=%d|json=0" % ("|".join("lattice=%s:patterns_showing_both_values_of_S=%d:most_draws=%d" % entry for entry in reads), flag(found), check("SU(2) bands on the side-1 lattices", found)))


# ---- Weights with zeros: w = 1, -1, 0, 0, 0 on the classes +1, -1, i, j, k of Q8.
# g != 0 exactly when every plaquette is central, and then g = S.
#
# The reduction read on (Z/2)^3. Write pi: Q8 -> V = Q8/{+1,-1}, which is (Z/2)^2. V is abelian and the kernel of pi is the centre, so every plaquette of U is
# central exactly when pi(U) is flat, that is when both Z/2 coordinates of pi(U) lie in the kernel of the coboundary from links to plaquettes. Each such U is
# one section of pi(U) times (-1)^b, for a unique b in Z/2 on the links, so the configurations with all plaquettes central are (flat fields) x (lift bits).
# -1 is central and each link occurs once in each of its plaquettes, so flipping b at a link multiplies exactly those plaquettes by -1. A link lies in 4 plaquettes,
# and in 0 or 2 faces of each cube. So the parity of the negative faces, in all and in each cube, is a function of the flat field alone. Reading one lift
# of every flat field reads those parities on every configuration with all plaquettes central. The controls: every lift of every field on (Z/2)x(Z/2) against
# the direct read of the gauge-fixed configurations there, and single flips against the table on a fixed-seed sample of fields on (Z/2)^3.
def f2_kernel(rows, width):
    pivots = []
    for row in rows:
        for pivot, value in pivots:
            if (row >> pivot) & 1:
                row ^= value
        if row:
            lead = row.bit_length() - 1
            pivots = [(p, v ^ row if (v >> lead) & 1 else v) for p, v in pivots]
            pivots.append((lead, row))
    taken = {p for p, _ in pivots}
    basis = []
    for column in range(width):
        if column not in taken:
            vector = 1 << column
            for pivot, value in pivots:
                if (value >> column) & 1:
                    vector |= 1 << pivot
            basis.append(vector)
    return basis


def flat_cochains(lat):
    rows = [sum(1 << l for l in face) for face in lat.faces]
    basis = f2_kernel(rows, len(lat.links))
    span = [0]
    for vector in basis:
        span += [value ^ vector for value in span]
    in_kernel = len(set(span)) == len(span) and all((row & value).bit_count() % 2 == 0 for row in rows for value in span)
    return len(basis), span, in_kernel


def q8_section(q):
    """section[u + 2 v + 4 b] for (u, v) in V, with i at (1, 0) and j at (0, 1), and b the lift bit. Returns it with the projection read back from the table."""
    i, j = q.elements.index(((0, 0), TWO, ZERO, ZERO)), q.elements.index(((0, 0), ZERO, TWO, ZERO))
    k = q.mult[i][j]
    section = [q.one, i, j, k]
    section += [q.mult[q.minus][x] for x in section]
    project = {x: slot % 4 for slot, x in enumerate(section)}
    ok = sorted(section) == list(range(8)) and all(project[q.mult[x][y]] == project[x] ^ project[y] for x in range(8) for y in range(8))
    central = [x for x in range(8) if all(q.mult[x][y] == q.mult[y][x] for y in range(8))]
    return section, ok and central == sorted((q.one, q.minus))


def cube_masks(lat):
    index = {p: f for f, p in enumerate(lat.plaquettes)}
    out = []
    for x in lat.sites:
        mask = 0
        for mu, nu, rho in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            # Counted mod 2, so that a side of 1 in the direction rho takes the two faces away together.
            mask ^= 1 << index[(x, mu, nu)]
            mask ^= 1 << index[(lat.shift(x, rho), mu, nu)]
        out.append(mask)
    return out


def dual_two_colouring(lat):
    """Colours the cubes, one per site, across shared faces. Returns the colours when two colours suffice, and None at an odd cycle."""
    colour = {lat.sites[0]: 0}
    frontier = [lat.sites[0]]
    while frontier:
        step = []
        for x in frontier:
            for rho in range(lat.k):
                y = lat.shift(x, rho)
                if y not in colour:
                    colour[y] = 1 - colour[x]
                    step.append(y)
                elif colour[y] == colour[x]:
                    return None
        frontier = step
    return colour


def section_zeros_control(q, section):
    """(Z/2)x(Z/2): every lift of every flat field, against the direct read of the gauge-fixed configurations."""
    lat = Lattice(2, 2)
    dimension, span, in_kernel = flat_cochains(lat)
    width = len(lat.links)
    faces = lat.faces
    fields, lifts_per_field, negative_field, read, one_value_per_field = 0, 1 << width, 0, 0, True
    distinct_counts, distinct_everywhere = set(), set()
    for u, v in itertools.product(span, repeat=2):
        fields += 1
        negative_here = 0
        on_this_field = set()
        for lift in range(lifts_per_field):
            config = [section[((u >> l) & 1) + 2 * ((v >> l) & 1) + 4 * ((lift >> l) & 1)] for l in range(width)]
            on_this_field.add(bytes(config))
            values = [face_value(q, config, face) for face in faces]
            read += 1
            if any(x != q.one and x != q.minus for x in values):
                one_value_per_field = False
            negative_here += sum(1 for x in values if x == q.minus) % 2
        if negative_here not in (0, lifts_per_field):
            one_value_per_field = False
        negative_field += 1 if negative_here else 0
        distinct_counts.add(len(on_this_field))
        distinct_everywhere |= on_this_field
    distinct_on_each = min(distinct_counts) if len(distinct_counts) == 1 else 0
    tree = spanning_tree(lat)
    free = [i for i in range(width) if i not in tree]
    config = [q.one] * width
    direct_central, direct_negative = 0, 0
    for values in itertools.product(range(q.order), repeat=len(free)):
        for slot, value in zip(free, values):
            config[slot] = value
        read_values = [face_value(q, config, face) for face in faces]
        if all(x == q.one or x == q.minus for x in read_values):
            direct_central += 1
            direct_negative += sum(1 for x in read_values if x == q.minus) % 2
    orbit = q.order ** len(lat.sites[1:])
    ok = in_kernel and one_value_per_field and dimension == len(lat.sites) - 1 + lat.k and read == direct_central * orbit and negative_field * lifts_per_field == direct_negative * orbit and negative_field > 0 and distinct_on_each == lifts_per_field and len(distinct_everywhere) == read
    print("SITE_SIGN_ZEROS_CONTROL|lattice=%s|group=Q8|flat_cochain_dimension=%d|flat_fields=%d|lifts_per_field=%d|distinct_configurations_on_each_field=%d|distinct_over_all_fields=%d|central_configurations_read_by_the_reduction=%d|gauge_fixed_central_read_directly=%d|times_gauge_orbit_%d=%d|negative_S_by_the_reduction=%d|negative_S_directly_times_orbit=%d|each_field_one_S_on_all_its_lifts=%d|ok=%d|json=0" % (
        lat.name, dimension, fields, lifts_per_field, distinct_on_each, len(distinct_everywhere), read, direct_central, orbit, direct_central * orbit, negative_field * lifts_per_field, direct_negative * orbit, flag(one_value_per_field), check("the reduction equals the direct read on (Z/2)x(Z/2)", ok)))
    return "control=%s:flat_fields=%d:lifts_per_field=%d:distinct_configurations_on_each_field=%d:distinct_over_all_fields=%d" % (lat.name, fields, lifts_per_field, distinct_on_each, len(distinct_everywhere))


def section_zeros_central(q, section):
    lat = Lattice(2, 2, 2)
    width, faces = len(lat.links), lat.faces
    dimension, span, in_kernel = flat_cochains(lat)
    cubes = cube_masks(lat)
    colour = dual_two_colouring(lat)
    bipartite = colour is not None
    even_cubes = [mask for x, mask in zip(lat.sites, cubes) if bipartite and colour[x] == 0]
    one_of_each = all(sum(1 for mask in cubes if (mask >> f) & 1) == 2 and sum(1 for mask in even_cubes if (mask >> f) & 1) == 1 for f in range(len(faces)))
    six_faces = all(mask.bit_count() == 6 for mask in cubes)
    link_faces = [sum(1 << f for f, face in enumerate(faces) if l in face) for l in range(width)]
    link_even_in_cubes = all((mask & faces_of_link).bit_count() % 2 == 0 for mask in cubes for faces_of_link in link_faces)
    odd_side = Lattice(2, 2, 3)
    odd_bipartite = dual_two_colouring(odd_side) is not None
    print("SITE_SIGN_ZEROS_DUAL|lattice=%s|cubes=%d|each_cube_six_faces=%d|each_face_in_one_even_and_one_odd_cube=%d|dual_lattice_two_colourable=%d|each_link_in_an_even_number_of_faces_of_each_cube=%d|each_link_in_4_faces=%d|lattice=%s|dual_lattice_two_colourable=%d|ok=%d|json=0" % (
        lat.name, len(cubes), flag(six_faces), flag(one_of_each), flag(bipartite), flag(link_even_in_cubes), flag(all(m.bit_count() == 4 for m in link_faces)), odd_side.name, flag(odd_bipartite),
        check("dual lattice", six_faces and one_of_each and bipartite and link_even_in_cubes and not odd_bipartite)))
    stream = Stream(4242)
    lifts = [[4 * stream.below(2) for _ in range(width)] for _ in range(4093)]
    u_bits = [[(u >> l) & 1 for l in range(width)] for u in span]
    v_bits = [[2 * bit for bit in row] for row in u_bits]
    m, inv, one, minus = q.mult, q.inv, q.one, q.minus
    read, noncentral, negative_s, odd_cubes = 0, 0, 0, 0
    negative_faces = collections.Counter()
    for u_row in u_bits:
        for v_row in v_bits:
            config = [section[a + b + c] for a, b, c in zip(u_row, v_row, lifts[read % 4093])]
            read += 1
            negative = 0
            for position, (a, b, c, d) in enumerate(faces):
                x = m[m[m[config[a]][config[b]]][inv[config[c]]]][inv[config[d]]]
                if x == minus:
                    negative |= 1 << position
                elif x != one:
                    noncentral += 1
            if SABOTAGE == "drop_the_cycle" and read == 1:
                # The face pattern this mode accepts: one negative face, so the two cubes holding it each read one.
                negative = 1
            negative_faces[negative.bit_count()] += 1
            negative_s += negative.bit_count() & 1
            for mask in cubes:
                odd_cubes += (negative & mask).bit_count() & 1
    # Single lift flips against the table, on a fixed-seed sample of fields.
    flips, flips_ok = 0, True
    sample = Stream(99)
    for _ in range(256):
        u_row, v_row = u_bits[sample.below(len(u_bits))], v_bits[sample.below(len(v_bits))]
        config = [section[a + b] for a, b in zip(u_row, v_row)]
        before = sum(1 << f for f, face in enumerate(faces) if face_value(q, config, face) == minus)
        for l in range(width):
            moved = list(config)
            moved[l] = m[minus][moved[l]]
            after = sum(1 << f for f, face in enumerate(faces) if face_value(q, moved, face) == minus)
            flips += 1
            flips_ok = flips_ok and after == before ^ link_faces[l]
    represented = read << width
    # A second route, using gauge invariance alone. With the spanning tree at 1, every lift of every flat field, in Gray code order, each flip read off the table on the plaquettes holding that link.
    tree_links = spanning_tree(lat)
    tree_mask = sum(1 << l for l in tree_links)
    free = [l for l in range(width) if not (tree_mask >> l) & 1]
    fixed_fields = [u for u in span if (u & tree_mask) == 0]
    faces_of_link = [[f for f, face in enumerate(faces) if l in face] for l in range(width)]
    gauge_read, gauge_off, gauge_negative, gauge_odd = 0, 0, 0, 0
    # The lifts of one field run over one coset of the image of the coboundary, whose rank is the links less the flat dimension.
    patterns_per_field, patterns_each_field_ok, every_pattern = 1 << (width - dimension), True, set()
    tree_at_one = True
    for u, v in itertools.product(fixed_fields, repeat=2):
        config = [section[((u >> l) & 1) + 2 * ((v >> l) & 1)] for l in range(width)]
        tree_at_one = tree_at_one and all(config[l] == one for l in tree_links)
        negative = sum(1 << f for f, face in enumerate(faces) if face_value(q, config, face) == minus)
        patterns = set()
        for step in range(1 << len(free)):
            if step:
                flip = free[(step & -step).bit_length() - 1]
                config[flip] = m[minus][config[flip]]
                for f in faces_of_link[flip]:
                    a, b, c, d = faces[f]
                    x = m[m[m[config[a]][config[b]]][inv[config[c]]]][inv[config[d]]]
                    if x == minus:
                        negative |= 1 << f
                    elif x == one:
                        negative &= ~(1 << f)
                    else:
                        gauge_off += 1
            gauge_read += 1
            gauge_negative += negative.bit_count() & 1
            patterns.add(negative)
            for mask in cubes:
                gauge_odd += (negative & mask).bit_count() & 1
        patterns_each_field_ok = patterns_each_field_ok and len(patterns) == patterns_per_field
        every_pattern |= patterns
    orbit = q.order ** len(lat.sites[1:])
    # Each face pattern read is even on every cube, so it is a Z/2 cycle on the dual lattice. The kernel of the cube matrix counts all of those cycles.
    cycles = 1 << len(f2_kernel(cubes, len(faces)))
    print("SITE_SIGN_ZEROS_GAUGE_FIXED|lattice=%s|group=Q8|flat_fields_with_the_tree_at_1=%d|every_tree_link_at_1_before_each_walk=%d|lift_bits_on_free_links=%d|configurations_read=%d|expected=2^23=%d|times_gauge_orbit_%d=%d|negative_face_patterns_on_each_field=%d|equal_on_every_field=%d|negative_face_patterns_over_all_fields=%d|Z/2_cycles_on_the_dual_lattice=%d|plaquettes_read_off_the_centre=%d|cubes_with_odd_negative_faces=%d|negative_S=%d|ok=%d|json=0" % (
        lat.name, len(fixed_fields) * len(fixed_fields), flag(tree_at_one), len(free), gauge_read, 2 ** 23, orbit, gauge_read * orbit, patterns_per_field, flag(patterns_each_field_ok), len(every_pattern), cycles, gauge_off, gauge_odd, gauge_negative,
        check("gauge-fixed central configurations on (Z/2)^3", tree_at_one and gauge_read == 2 ** 23 and gauge_read * orbit == 2 ** 44 and patterns_each_field_ok and len(every_pattern) == cycles and gauge_off == 0 and gauge_odd == 0 and gauge_negative == 0)))
    route_2 = "route_2=%s:flat_fields_with_the_tree_at_1=%d:every_tree_link_at_1_before_each_walk=%d" % (lat.name, len(fixed_fields) * len(fixed_fields), flag(tree_at_one))
    COUNT["central_odd"] += negative_s + gauge_negative
    row = "YM4_02C_SITE_SIGN_ZEROS|weight_on_classes_+1,-1,i,j,k=1,-1,0,0,0|group=Q8|lattice=%s|every_configuration_with_all_plaquettes_central|negative_S=%d|reason=a_Z/2_cycle_on_a_bipartite_dual_lattice|json=0" % (lat.name, negative_s)
    found = row in PREDICTED
    print("SITE_SIGN_ZEROS_CENTRAL|lattice=%s|group=Q8|flat_cochain_dimension=%d|expected=sites-1+k=%d|flat_fields_read=%d|lift_bits_per_field=%d|configurations_represented=%d|expected=2^44=%d|plaquettes_read_off_the_centre=%d|cubes_with_odd_negative_faces=%d|negative_S=%d|negative_face_counts_read=%s|single_lift_flips_equal_to_the_incidence=%d_of_%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        lat.name, dimension, len(lat.sites) - 1 + lat.k, read, width, represented, 2 ** 44, noncentral, odd_cubes, negative_s, ",".join("%d:%d" % (n, negative_faces[n]) for n in sorted(negative_faces)), flips if flips_ok else 0, flips, flag(found),
        check("configurations with all plaquettes central on (Z/2)^3 read S = +1", found and in_kernel and noncentral == 0 and flips_ok and represented == 2 ** 44)))
    check("every cube on (Z/2)^3 holds an even number of negative faces", odd_cubes == 0)
    return route_2


def section_zeros_twist(q):
    i, j = q.elements.index(((0, 0), TWO, ZERO, ZERO)), q.elements.index(((0, 0), ZERO, TWO, ZERO))
    weight = (1, -1, 0, 0, 0)
    read = []
    all_central, g_is_s = True, True
    for dims in ((2, 2, 2), (2, 2, 3), (2, 2)):
        lat = Lattice(*dims)
        config = [i if mu == 0 and x[0] == 0 else j if mu == 1 and x[1] == 0 else q.one for x, mu in lat.links]
        values = [face_value(q, config, face) for face in lat.faces]
        all_central = all_central and all(x == q.one or x == q.minus for x in values)
        product = 1
        for x in values:
            product *= weight[q.merged_of[x]]
        negatives = sum(1 for x in values if x == q.minus)
        g_is_s = g_is_s and product == (-1 if negatives % 2 else 1)
        read.append((lat.name, product, negatives))
    row = "YM4_02C_SITE_SIGN_ZEROS|weight_on_classes_+1,-1,i,j,k=1,-1,0,0,0|group=Q8|twist=a_is_i_on_1-links_at_x1_0_and_b_is_j_on_2-links_at_x2_0|%s|json=0" % "|".join("lattice=%s:S=%+d:negative_plaquettes=%d" % entry for entry in read)
    found = row in PREDICTED
    print("SITE_SIGN_ZEROS_TWIST|group=Q8|%s|all_central=%d|g_equals_S=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        "|".join("lattice=%s:S=%+d:negative_plaquettes=%d" % entry for entry in read), flag(all_central), flag(g_is_s), flag(found), check("twist on three lattices", found and all_central and g_is_s)))


def section_zeros():
    q = group("Q8")
    section, section_ok = q8_section(q)
    print("SITE_SIGN_ZEROS_SECTION|group=Q8|projection_to_(Z/2)^2_is_a_homomorphism_with_kernel_the_centre=%d|ok=%d|json=0" % (flag(section_ok), check("projection of Q8", section_ok)))
    control = section_zeros_control(q, section)
    route_2 = section_zeros_central(q, section)
    section_zeros_twist(q)
    row = "YM4_02C_SITE_SIGN_PINS|%s|%s|json=0" % (control, route_2)
    print("SITE_SIGN_PINS|%s|%s|row_found_in_the_prediction=%d|ok=%d|json=0" % (control, route_2, flag(row in PREDICTED), check("the pins on the control's lifts and the tree", row in PREDICTED)))


# ---- The same weight with the time direction read. T = 2 has fixed slices C0 and C1 and time links V, with A = V and W_plus the product over the time-like plaquettes of the
# one layer. Reading f(C) and W_plus(C, A) of Lemma 0004's Theorem 2 directly: at each C with f(C) < 0 the note says W_plus(C, .) is 0, because the cubes p x [t, t+1] carry S across the layer.
ZERO_WEIGHT = (1, -1, 0, 0, 0)


def zero_weight_slice(q, lat, config):
    product = 1
    for face in lat.faces:
        product *= ZERO_WEIGHT[q.merged_of[face_value(q, config, face)]]
    return product


def odd_cubes_in_layer(q, lat, lower, upper, time_links):
    """The number of spatial p with an odd number of faces at -1 on the cube p x [t, t+1], with lower and upper the slices and time_links the V of the layer."""
    m, inv, minus = q.mult, q.inv, q.minus
    time_like = [m[m[m[lower[l]][time_links[r]]][inv[upper[l]]]][inv[time_links[s]]] == minus for l, (s, r) in enumerate(lat.ends)]
    odd = 0
    for face in lat.faces:
        parity = (face_value(q, lower, face) == minus) ^ (face_value(q, upper, face) == minus)
        for l in face:
            parity ^= time_like[l]
        odd += 1 if parity else 0
    return odd


def central_time_links(q, lat, lower, upper, limit):
    """The number of V in G^sites with every time-like plaquette central, site by site, each link read once both its ends are set. A limit above 0 stops the count there."""
    m, inv, one, minus = q.mult, q.inv, q.one, q.minus
    by_last = [[] for _ in lat.sites]
    for l, (s, r) in enumerate(lat.ends):
        by_last[max(s, r)].append((s, r, l))
    v = [one] * len(lat.sites)

    def count_from(site):
        if site == len(lat.sites):
            return 1
        total = 0
        for value in range(q.order):
            v[site] = value
            good = True
            for s, r, l in by_last[site]:
                x = m[m[m[lower[l]][v[r]]][inv[upper[l]]]][inv[v[s]]]
                if x != one and x != minus:
                    good = False
                    break
            if good:
                total += count_from(site + 1)
                if limit and total >= limit:
                    return total
        return total

    return count_from(0)


def section_zeros_t():
    q = group("Q8")
    m, inv, one, minus = q.mult, q.inv, q.one, q.minus
    time_weight = (1, 1, 1, 1, 1) if SABOTAGE == "time_like_weight_one" else ZERO_WEIGHT
    # (Z/1)x(Z/1)xT2: every C and every A.
    lat = Lattice(1, 1)
    slices = list(itertools.product(range(q.order), repeat=len(lat.links)))
    g = {config: zero_weight_slice(q, lat, config) for config in slices}
    next_slices = {config: [] for config in slices}
    negative_f, negative_alive, alive, alive_f_plus, negative_n, cubes_read, cubes_odd = 0, 0, 0, 0, 0, 0, 0
    for c0 in slices:
        for c1 in slices:
            f = g[c0] * g[c1]
            total, here = 0, False
            for v in range(q.order):
                w_plus = 1
                for l in range(len(lat.links)):
                    w_plus *= time_weight[q.merged_of[m[m[m[c0[l]][v]][inv[c1[l]]]][inv[v]]]]
                total += w_plus
                if w_plus:
                    here = True
                    cubes_read += len(lat.faces)
                    cubes_odd += odd_cubes_in_layer(q, lat, c0, c1, [v])
            negative_f += 1 if f < 0 else 0
            negative_alive += 1 if f < 0 and here else 0
            alive += 1 if here else 0
            alive_f_plus += 1 if f > 0 and here else 0
            negative_n += 1 if f * total * total < 0 else 0
            if here:
                next_slices[c0].append(c1)
    read_c = len(slices) * len(slices)
    row = "YM4_02C_SITE_SIGN_ZEROS_T|weight_on_classes_+1,-1,i,j,k=1,-1,0,0,0_on_every_plaquette|group=Q8|lattice=%sxT2|C=%d|A_per_C=%d|f_negative=%d|of_those_with_W_plus_not_identically_0=%d|W_plus_not_identically_0=%d|f_on_those=%s|N(delta_C)_negative=%d|cubes_read=%d|cubes_with_odd_faces=%d|json=0" % (
        lat.name, read_c, q.order, negative_f, negative_alive, alive, "+1" if alive_f_plus == alive else "both", negative_n, cubes_read, cubes_odd)
    found = row in PREDICTED
    COUNT["alive_with_f_negative"] += negative_alive
    COUNT["odd_cube"] += cubes_odd
    print("SITE_SIGN_ZEROS_T|lattice=%sxT2|group=Q8|C=%d|f_negative=%d|of_those_with_W_plus_not_identically_0=%d|W_plus_not_identically_0=%d|f_+1_on_those=%d|N(delta_C)_negative=%d|cubes_read=%d|cubes_with_odd_faces=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        lat.name, read_c, negative_f, negative_alive, alive, alive_f_plus, negative_n, cubes_read, cubes_odd, flag(found), check("W_plus is 0 at each C with f negative on Q8 at T=2", found and negative_alive == 0)))
    if SABOTAGE:
        return
    # (Z/1)x(Z/1)xT4: the slice at t = 1 sits between the two layers.
    paths, opposite_1, opposite_2 = 0, 0, 0
    for c0 in slices:
        for c1 in next_slices[c0]:
            for c2 in next_slices[c1]:
                paths += 1
                opposite_1 += 1 if g[c1] != g[c0] else 0
                opposite_2 += 1 if g[c2] != g[c0] else 0
    nonzero = sum(1 for config in slices if g[config])
    row = "YM4_02C_SITE_SIGN_ZEROS_T|weight_on_classes_+1,-1,i,j,k=1,-1,0,0,0_on_every_plaquette|group=Q8|lattice=%sxT4|slices_with_g_nonzero=%d|paths_C0_C1_C2_with_every_time_like_plaquette_central=%d|g(C1)_opposite_g(C0)=%d|g(C2)_opposite_g(C0)=%d|json=0" % (lat.name, nonzero, paths, opposite_1, opposite_2)
    found = row in PREDICTED
    print("SITE_SIGN_ZEROS_T|lattice=%sxT4|group=Q8|slices_with_g_nonzero=%d|paths=%d|g(C1)_opposite_g(C0)=%d|g(C2)_opposite_g(C0)=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (lat.name, nonzero, paths, opposite_1, opposite_2, flag(found), check("S carried across two layers on Q8 at T=4", found)))
    # (Z/2)x(Z/2)x(Z/3)xT2: an odd side, where the twist has S = -1 and f takes negative values.
    lat = Lattice(2, 2, 3)
    i, j = q.elements.index(((0, 0), TWO, ZERO, ZERO)), q.elements.index(((0, 0), ZERO, TWO, ZERO))
    twist = [i if mu == 0 and x[0] == 0 else j if mu == 1 and x[1] == 0 else one for x, mu in lat.links]
    trivial = [one] * len(lat.links)
    s_twist, s_trivial = zero_weight_slice(q, lat, twist), zero_weight_slice(q, lat, trivial)
    at_opposite, at_same = central_time_links(q, lat, twist, trivial, 0), central_time_links(q, lat, twist, twist, 0)
    stream = Stream(909)
    quotient = (one, i, j, m[i][j])
    bank = {1: [], -1: []}
    draws = 0
    while (len(bank[1]) < 8 or len(bank[-1]) < 8) and draws < 1 << 12:
        draws += 1
        pick = [quotient[stream.below(4)] for _ in range(lat.k)]
        moved = gauge_moved(q, lat, [pick[mu] if x[mu] == 0 else one for x, mu in lat.links], [stream.below(q.order) for _ in lat.sites])
        config = [m[minus][u] if stream.below(2) else u for u in moved]
        value = zero_weight_slice(q, lat, config)
        if value and len(bank[value]) < 8:
            bank[value].append(config)
    opposite_pairs, opposite_alive, equal_pairs, equal_alive = 0, 0, 0, 0
    for a in bank[1]:
        for b in bank[-1]:
            opposite_pairs += 1
            opposite_alive += 1 if central_time_links(q, lat, a, b, 1) else 0
    for value in (1, -1):
        for a in bank[value]:
            for b in bank[value]:
                equal_pairs += 1
                equal_alive += 1 if central_time_links(q, lat, a, b, 1) else 0
    moved_read, moved_opposite, moved_off_centre, moved_cubes, moved_odd = 0, 0, 0, 0, 0
    for value in (1, -1):
        for lower in bank[value]:
            for _ in range(8):
                v = [stream.below(q.order) for _ in lat.sites]
                upper = [m[minus][x] if stream.below(2) else x for x in (m[m[inv[v[s]]][lower[l]]][v[r]] for l, (s, r) in enumerate(lat.ends))]
                moved_read += 1
                for l, (s, r) in enumerate(lat.ends):
                    x = m[m[m[lower[l]][v[r]]][inv[upper[l]]]][inv[v[s]]]
                    moved_off_centre += 1 if x != one and x != minus else 0
                moved_opposite += 1 if zero_weight_slice(q, lat, upper) != value else 0
                moved_cubes += len(lat.faces)
                moved_odd += odd_cubes_in_layer(q, lat, lower, upper, v)
    row = "YM4_02C_SITE_SIGN_ZEROS_T|weight_on_classes_+1,-1,i,j,k=1,-1,0,0,0_on_every_plaquette|group=Q8|lattice=%sxT2|S(twist)=%+d|S(trivial)=%+d|f(twist,trivial)=%+d|V_with_every_time_like_plaquette_central_at_(twist,trivial)=%d|at_(twist,twist)=%d|central_slices=%d_with_S=+1_and_%d_with_S=-1|opposite_S_pairs=%d|of_those_with_W_plus_not_identically_0=%d|equal_S_pairs=%d|of_those_with_W_plus_not_identically_0=%s|C1_moved_by_V_and_signs=%d|g(C1)_opposite_g(C0)=%d|cubes_read=%d|cubes_with_odd_faces=%d|json=0" % (
        lat.name, s_twist, s_trivial, s_twist * s_trivial, at_opposite, at_same, len(bank[1]), len(bank[-1]), opposite_pairs, opposite_alive, equal_pairs, "at_least_16" if equal_alive >= 16 else "below_16", moved_read, moved_opposite, moved_cubes, moved_odd)
    found = row in PREDICTED
    COUNT["alive_with_f_negative"] += opposite_alive
    COUNT["odd_cube"] += moved_odd
    print("SITE_SIGN_ZEROS_T|lattice=%sxT2|group=Q8|f(twist,trivial)=%+d|V_at_(twist,trivial)=%d|V_at_(twist,twist)=%d|expected_at_(twist,twist)=4*2^sites=%d|draws=%d|opposite_S_pairs=%d|alive=%d|equal_S_pairs=%d|alive=%d|C1_moved_by_V_and_signs=%d|time_like_read_off_the_centre=%d|g(C1)_opposite_g(C0)=%d|cubes_read=%d|cubes_with_odd_faces=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        lat.name, s_twist * s_trivial, at_opposite, at_same, 4 << len(lat.sites), draws, opposite_pairs, opposite_alive, equal_pairs, equal_alive, moved_read, moved_off_centre, moved_opposite, moved_cubes, moved_odd, flag(found), check("W_plus and the cubes on Q8 at (Z/2)x(Z/2)x(Z/3)xT2", found and moved_off_centre == 0 and at_same == 4 << len(lat.sites))))


# ---- SU(2) with the weight a_p, the real part of the plaquette. Exact rational unit quaternions as (a, b, c, d, den).
def reduced_quaternion(a, b, c, d, den):
    g = math.gcd(math.gcd(math.gcd(math.gcd(a, b), c), d), den)
    return a // g, b // g, c // g, d // g, den // g


def rational_product(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return reduced_quaternion(a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n)


def rational_inverse(p):
    return p[0], -p[1], -p[2], -p[3], p[4]


def rational_word(links, face):
    a, b, c, d = face
    return rational_product(rational_product(rational_product(links[a], links[b]), rational_inverse(links[c])), rational_inverse(links[d]))


def rational_unit(stream, bound, scale):
    """The point of the sphere at t / scale by stereographic projection, with t in [-bound, bound]^3: (scale^2 - |t|^2 + 2 scale t) / (scale^2 + |t|^2)."""
    t = [stream.below(2 * bound + 1) - bound for _ in range(3)]
    square, top = scale * scale, t[0] * t[0] + t[1] * t[1] + t[2] * t[2]
    return reduced_quaternion(square - top, 2 * scale * t[0], 2 * scale * t[1], 2 * scale * t[2], square + top)


def is_rational_unit(x):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + x[3] * x[3] == x[4] * x[4]


QUATERNION_ONE, QUATERNION_MINUS, QUATERNION_I, QUATERNION_J = (1, 0, 0, 0, 1), (-1, 0, 0, 0, 1), (0, 1, 0, 0, 1), (0, 0, 1, 0, 1)
CIRCLE = (QUATERNION_ONE, (3, 4, 0, 0, 5), (-3, 4, 0, 0, 5), (5, 12, 0, 0, 13), (8, -15, 0, 0, 17))
PALETTE =((1, 2, 2, 0, 3), (2, 1, 0, 2, 3), (2, 0, 1, -2, 3), (1, -2, 2, 0, 3), (2, 1, 2, 0, 3), (1, 1, 1, 1, 2), (1, -1, 1, -1, 2), (3, 4, 0, 0, 5), (0, 3, 0, 4, 5))


def real_parts(lat, config):
    out = []
    for a, b, c, d in lat.faces:
        x = rational_product(rational_product(PALETTE[config[a]], PALETTE[config[b]]), rational_inverse(PALETTE[config[c]]))
        x = rational_product(x, rational_inverse(PALETTE[config[d]]))
        out.append((x[0], x[4]))
    return out


def plain_real_parts(lat, config):
    """A second route, keeping the whole denominators and skipping every reduction."""
    out = []
    for a, b, c, d in lat.faces:
        total = (1, 0, 0, 0)
        den = 1
        for slot, inverted in ((a, False), (b, False), (c, True), (d, True)):
            e, f, g, h, n = PALETTE[config[slot]]
            if inverted:
                f, g, h = -f, -g, -h
            p, q, r, s = total
            total = (p * e - q * f - r * g - s * h, p * f + q * e + r * h - s * g, p * g - q * h + r * e + s * f, p * h + q * g - r * f + s * e)
            den *= n
        out.append((total[0], den))
    return out


def product_of_pairs(values):
    top, bottom = 1, 1
    for n, d in values:
        top, bottom = top * n, bottom * d
    g = math.gcd(top, bottom)
    return top // g, bottom // g


def section_su2():
    palette_ok = all(a * a + b * b + c * c + d * d == den * den for a, b, c, d, den in PALETTE)
    print("SITE_SIGN_SU2_PALETTE|palette=%s|each_of_norm_1=%d|ok=%d|json=0" % (";".join("%d,%d,%d,%d/%d" % p for p in PALETTE), flag(palette_ok), check("exact unit quaternions", palette_ok)))
    names = []
    for dims, seed in (((2, 2), 501), ((2, 2, 2), 502)):
        lat = Lattice(*dims)
        names.append(lat.name)
        stream = Stream(seed)
        found = {}
        draws, zeros = 0, 0
        while len(found) < 2 and draws < 1 << 16:
            draws += 1
            config = [stream.below(len(PALETTE)) for _ in lat.links]
            value = product_of_pairs(real_parts(lat, config))
            if value[0] == 0:
                zeros += 1
            else:
                found.setdefault(1 if value[0] > 0 else -1, (config, value))
        both = len(found) == 2
        parts = []
        routes_agree, signs_agree = True, True
        for sign in (1, -1):
            if sign in found:
                config, value = found[sign]
                plain = product_of_pairs(plain_real_parts(lat, config))
                routes_agree = routes_agree and plain == value
                negative_parts = sum(1 for n, d in real_parts(lat, config) if n < 0)
                signs_agree = signs_agree and (negative_parts % 2 == 1) == (sign < 0)
                parts.append("g_%+d=%d/%d:negative_a_p=%d:palette_indices=%s" % (sign, value[0], value[1], negative_parts, ".".join(str(v) for v in config)))
        print("SITE_SIGN_SU2|group=SU(2)|weight=a_p|lattice=%s|plaquettes=%d|draws=%d|draws_with_g_0=%d|%s|exact_second_route=%d|sign_of_g_is_S=%d|same_sign_on_a_neighbourhood_by_continuity=DERIVED|ok=%d|json=0" % (
            lat.name, len(lat.faces), draws, zeros, "|".join(parts), flag(routes_agree), flag(signs_agree), check("both signs of g on %s" % lat.name, both and routes_agree and signs_agree)))
    row = "YM4_02C_SITE_SIGN_SU2|group=SU(2)|weight=a_p|lattice=%s|exact_rational_quaternion_configurations_with_both_signs_of_g|lattice=%s|the_same|tag=an_instance_of_the_corollary|json=0" % (names[0], names[1])
    print("SITE_SIGN_SU2_ROW|row_found_in_the_prediction=%d|ok=%d|json=0" % (flag(row in PREDICTED), check("SU(2) row", row in PREDICTED)))


# ---- The weight with zeros on SU(2) itself: w = +1 within delta of 1, -1 within delta of -1, and 0 elsewhere, at delta = 8/25 < 1/3, on exact rational unit quaternions.
DELTA_TOP, DELTA_BOTTOM = 8, 25
TWIST_LATTICES = ((2, 2, 2), (2, 2, 3), (2, 2, 4), (2, 3, 3), (3, 3, 3), (2, 2, 5), (2, 2), (3, 3), (3, 2))
NEIGHBOURHOODS = (((2, 2, 2), 901), ((2, 2, 3), 902), ((2, 2, 4), 903), ((2, 2), 904), ((3, 3), 905))
NEIGHBOURHOOD_DRAWS = 32
PARITY_LATTICES = ((2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3), (2, 2, 4), (2, 4, 4), (4, 4, 4), (1, 2, 2), (1, 1, 2), (1, 1, 1), (1, 2, 3), (1, 1, 3), (2, 2, 5))
# A face is a loop at its own corner, with a connector from (0, 0, 0) to that corner. The word lists each face with 1 where it is inverted.
CUBE_FACES = {"x0": ((), (1, 2, 1, 2)), "x1": ((0,), (1, 2, 1, 2)), "y0": ((), (0, 2, 0, 2)), "y1": ((1,), (0, 2, 0, 2)), "z0": ((), (0, 1, 0, 1)), "z1": ((2,), (0, 1, 0, 1))}
CUBE_WORD = (("x0", 0), ("z1", 1), ("y0", 1), ("x1", 1), ("z0", 0), ("y1", 0))
CUBE_WORD_SWAPPED = (("z1", 1), ("x0", 0), ("y0", 1), ("x1", 1), ("z0", 0), ("y1", 0))


def support_sign(x):
    """+1 or -1 when the unit quaternion x is strictly within delta of that sign, and 0 otherwise. |x - sigma|^2 = 2 - 2 sigma a / den."""
    a, den = x[0], x[4]
    for sigma in (1, -1):
        if (2 * den - 2 * sigma * a) * DELTA_BOTTOM * DELTA_BOTTOM < DELTA_TOP * DELTA_TOP * den:
            return sigma
    return 0


def rational_twist(lat):
    return [QUATERNION_I if mu == 0 and x[0] == 0 else QUATERNION_J if mu == 1 and x[1] == 0 else QUATERNION_ONE for x, mu in lat.links]


def cube_walk(start, axes):
    """The letters of a walk from a corner of the cube. A letter is (corner, axis, +1 or -1), the edge from that corner along the axis, with the bit of the axis 0 at the corner."""
    letters, at = [], start
    for axis in axes:
        ahead = tuple(bit ^ 1 if slot == axis else bit for slot, bit in enumerate(at))
        letters.append((at, axis, 1) if at[axis] == 0 else (ahead, axis, -1))
        at = ahead
    return letters, at


def inverted_letters(letters):
    return [(corner, axis, -sign) for corner, axis, sign in reversed(letters)]


def cube_letters(word):
    out = []
    for name, inverted in word:
        connector, loop = CUBE_FACES[name]
        path, corner = cube_walk((0, 0, 0), connector)
        letters, _ = cube_walk(corner, loop)
        out += path + (inverted_letters(letters) if inverted else letters) + inverted_letters(path)
    return out


def freely_reduced(letters):
    out = []
    for corner, axis, sign in letters:
        if out and out[-1] == (corner, axis, -sign):
            out.pop()
        else:
            out.append((corner, axis, sign))
    return out


def read_letters(edges, letters):
    total = QUATERNION_ONE
    for corner, axis, sign in letters:
        total = rational_product(total, edges[(corner, axis)] if sign > 0 else rational_inverse(edges[(corner, axis)]))
    return total


def section_su2_zeros():
    entries, plane_ok, central_ok = [], True, True
    for dims in TWIST_LATTICES:
        lat = Lattice(*dims)
        links = rational_twist(lat)
        values = [rational_word(links, face) for face in lat.faces]
        negative = [f for f, x in enumerate(values) if x == QUATERNION_MINUS]
        central_ok = central_ok and all(x == QUATERNION_ONE or x == QUATERNION_MINUS for x in values)
        plane_ok = plane_ok and all(lat.plaquettes[f][1:] == (0, 1) for f in negative)
        entries.append("lattice=%s:S=%+d:negative_plaquettes=%d" % (lat.name, -1 if len(negative) % 2 else 1, len(negative)))
    row = "YM4_02C_SITE_SIGN_SU2_TWIST|group=SU(2)|read_on=real_quaternions|every_negative_plaquette_in_the_plane_12=%d|%s|json=0" % (flag(plane_ok), "|".join(entries))
    found = row in PREDICTED
    print("SITE_SIGN_SU2_TWIST|group=SU(2)|every_plaquette_exactly_+1_or_-1=%d|every_negative_plaquette_in_the_plane_12=%d|%s|row_found_in_the_prediction=%d|ok=%d|json=0" % (flag(central_ok), flag(plane_ok), "|".join(entries), flag(found), check("the twist on real quaternions", found and central_ok)))
    # Each link moved by a unit within 1/14 of 1, so each plaquette moves by at most 4/14 < 8/25 and keeps its sign.
    entries, moves_ok = [], True
    for dims, seed in NEIGHBOURHOODS:
        lat = Lattice(*dims)
        stream = Stream(seed)
        base = rational_twist(lat)
        cubes = cube_masks(lat) if lat.k == 3 else []
        in_support, even, s_values, counts = 0, 0, set(), set()
        for _ in range(NEIGHBOURHOOD_DRAWS):
            moves = [rational_unit(stream, 2, 100) for _ in base]
            moves_ok = moves_ok and all(is_rational_unit(x) and (2 * x[4] - 2 * x[0]) * 196 < x[4] for x in moves)
            links = [rational_product(u, move) for u, move in zip(base, moves)]
            signs = [support_sign(rational_word(links, face)) for face in lat.faces]
            if all(signs):
                in_support += 1
                negative = sum(1 << f for f, s in enumerate(signs) if s < 0)
                counts.add(negative.bit_count())
                s_values.add(-1 if negative.bit_count() % 2 else 1)
                even += 1 if all((negative & mask).bit_count() % 2 == 0 for mask in cubes) else 0
        entry = "lattice=%s:in_the_support=%d:S=%+d:negative_plaquettes=%d" % (lat.name, in_support, min(s_values) if len(s_values) == 1 else 0, min(counts) if len(counts) == 1 else 0)
        entries.append(entry + (":every_cube_even=%d" % even if lat.k == 3 else ""))
    row = "YM4_02C_SITE_SIGN_SU2_NEIGHBOURHOOD|group=SU(2)|delta=%d/%d|each_link_moved_by_a_rational_unit_within_1/14_of_1|so_each_plaquette_moves_by_at_most_4/14=below_8/25|draws=%d|%s|json=0" % (DELTA_TOP, DELTA_BOTTOM, NEIGHBOURHOOD_DRAWS, "|".join(entries))
    found = row in PREDICTED
    print("SITE_SIGN_SU2_NEIGHBOURHOOD|group=SU(2)|delta=%d/%d|each_move_within_1/14=%d|4/14_below_delta=%d|draws=%d|%s|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        DELTA_TOP, DELTA_BOTTOM, flag(moves_ok), flag(4 * DELTA_BOTTOM < DELTA_TOP * 14), NEIGHBOURHOOD_DRAWS, "|".join(entries), flag(found), check("a neighbourhood of the twist", found and moves_ok and 4 * DELTA_BOTTOM < DELTA_TOP * 14)))
    # The cube identity is a word in the free group on the 12 edges, so it holds under any identification of the edges, at sides of 1 and 2 as well.
    corners = list(itertools.product((0, 1), repeat=3))
    keys = [(corner, axis) for corner in corners for axis in range(3) if corner[axis] == 0]
    word, swapped = cube_letters(CUBE_WORD), cube_letters(CUBE_WORD_SWAPPED)
    reduces, swapped_reduces = not freely_reduced(word), not freely_reduced(swapped)
    stream = Stream(911)
    cubes_read, product_one, swapped_one = 0, 0, 0
    for _ in range(50):
        edges = {key: rational_unit(stream, 7, 1 + stream.below(7)) for key in keys}
        cubes_read += 1
        product_one += 1 if read_letters(edges, word) == QUATERNION_ONE else 0
        swapped_one += 1 if read_letters(edges, swapped) == QUATERNION_ONE else 0
    named = ",".join(name + ("^-1" if inverted else "") for name, inverted in CUBE_WORD)
    row = "YM4_02C_SITE_SIGN_SU2_CUBE|the_word=%s|reduces_to_the_empty_word_in_the_free_group_on_the_12_edges=%d|exact_rational_cubes=%d|ordered_product_equal_to_1=%d|json=0" % (named, flag(reduces), cubes_read, product_one)
    found = row in PREDICTED
    print("SITE_SIGN_SU2_CUBE|the_word=%s|edges=%d|letters=%d|reduces_to_the_empty_word=%d|exact_rational_cubes=%d|ordered_product_equal_to_1=%d|the_word_with_two_faces_swapped_reduces=%d|its_product_equal_to_1=%d|row_found_in_the_prediction=%d|ok=%d|json=0" % (
        named, len(keys), len(word), flag(reduces), cubes_read, product_one, flag(swapped_reduces), swapped_one, flag(found), check("the cube identity", found and len(keys) == 12 and not swapped_reduces and swapped_one == 0)))


def section_cycle_parity():
    """Every Z/2 cycle on the dual lattice has even length exactly when each vector of a basis of the kernel of the cube matrix has even weight."""
    names, entries, agree = [], [], 0
    for dims in PARITY_LATTICES:
        lat = Lattice(*dims)
        kernel = f2_kernel(cube_masks(lat), len(lat.faces))
        every_cycle_even = all(vector.bit_count() % 2 == 0 for vector in kernel)
        every_side_even = all(side % 2 == 0 for side in dims)
        agree += 1 if every_cycle_even == every_side_even else 0
        names.append(lat.name)
        entries.append("%s:cycles=2^%d:every_cycle_even=%d:every_side_even=%d" % (lat.name, len(kernel), flag(every_cycle_even), flag(every_side_even)))
    row = "YM4_02C_SITE_SIGN_CYCLE_PARITY|every_Z/2_cycle_on_the_dual_lattice_is_even_exactly_when_every_side_is_even|lattices=%s|agree=%d_of_%d|json=0" % (",".join(names), agree, len(names))
    found = row in PREDICTED
    print("SITE_SIGN_CYCLE_PARITY|%s|agree=%d_of_%d|row_found_in_the_prediction=%d|ok=%d|json=0" % ("|".join(entries), agree, len(names), flag(found), check("the parity of the cycles", found)))


def section_summary():
    named = ",".join(lattice_name(dims) for dims in WITNESS_LATTICES)
    method_rows = in_row(PREDICTED, "YM4_02C_SITE_SIGN_METHOD", "lattices=%s" % named) and in_row(PREDICTED, "YM4_02C_SITE_SIGN_METHOD", "exhaustive=Q8_on_(Z/2)x(Z/2)_over_8^5_gauge_fixed_configurations")
    rule_row = "YM4_02C_SITE_SIGN_RULE|a_sign_pattern_gives_one_value_per_inversion_closed_class|S_constant_iff_the_pattern_is_plus_or_minus_a_homomorphism_to_{+1,-1}|at_every_side_at_least_2_and_k_at_least_2|json=0"
    clean = COUNT["off_rule_constant"] == 0 and COUNT["on_rule_both"] == 0 and COUNT["central_odd"] == 0
    print("SITE_SIGN_RULE|group_and_lattice_pairs_by_witness=%d|added_beside_the_prediction=%d|pair_read_exhaustively=Q8_on_(Z/2)x(Z/2)|lattices=%s|method_row_found=%d|rule_row_found=%d|ok=%d|json=0" % (
        len(GROUP_NAMES) * len(WITNESS_LATTICES), len(GROUP_NAMES), named, flag(method_rows), flag(rule_row in PREDICTED), check("rule and method rows", bool(method_rows) and rule_row in PREDICTED and clean)))
    print("SITE_SIGN_FALSIFIERS|a_nonhomomorphism_pattern_with_S_constant_at_every_side_at_least_2=%d|a_homomorphism_pattern_with_both_values_of_S=%d|a_central_configuration_on_(Z/2)^3_with_odd_negative_faces=%d|a_false_step_in_the_proof=OPEN_independent_review|json=0" % (
        COUNT["off_rule_constant"], COUNT["on_rule_both"], COUNT["central_odd"]))
    print("SITE_SIGN_SCOPE|finite_groups_on_fixed_finite_lattices_read_exactly=1|SU(2)=exact_rational_witnesses_of_both_signs_of_g|the_theorem_for_every_compact_group=DERIVED_in_the_note_with_independent_review_OPEN|characterization_for_weights_with_zeros=OPEN|json=0")
    print("SITE_SIGN_FALSIFIERS_2|a_finite_group_with_constant_patterns_above_the_rule_on_a_lattice_with_two_sides_at_least_2_or_one_side_at_least_3=%d|a_C_with_f(C)<0_and_an_A_with_W_plus(C,A)_nonzero_for_the_weight_with_zeros=%d|a_cube_p_x_[t,t+1]_with_odd_faces=%d|json=0" % (
        COUNT["above_rule_with_the_link"], COUNT["alive_with_f_negative"], COUNT["odd_cube"]))
    check("the falsifiers of the second round read 0", COUNT["above_rule_with_the_link"] == 0 and COUNT["alive_with_f_negative"] == 0 and COUNT["odd_cube"] == 0)
    print("SITE_SIGN_SCOPE_2|the_conclusion_at_two_sides_at_least_2_or_one_side_at_least_3=DERIVED_in_the_note|SU(2)_at_k=2_on_the_lattices_left=DERIVED_by_the_second_seat|SU(2)_at_k_at_least_3_on_the_lattices_left=CONJECTURE|site_reflection_positivity_for_the_weight_with_zeros_at_every_lattice_with_T_even=DERIVED_in_the_note|json=0")


def imported_modules():
    """The top-level name of every import statement in this file, read from its tokens, so a string holding the word import stays out."""
    names = set()
    statement = []
    with open(os.path.abspath(__file__), encoding="utf-8") as handle:
        for token in tokenize.generate_tokens(handle.readline):
            if token.type == tokenize.NEWLINE or token.string == ";":
                if "import" in statement:
                    at = statement.index("import")
                    if "from" in statement[:at]:
                        names.add(statement[statement.index("from") + 1])
                    else:
                        wanted = True
                        for word in statement[at + 1:]:
                            if wanted:
                                names.add(word)
                            wanted = word == ","
                statement = []
            elif token.type in (tokenize.NAME, tokenize.OP):
                statement.append(token.string)
    return sorted(names)


def finish():
    elapsed_ns = time.perf_counter_ns() - START_NS
    within = elapsed_ns <= 600 * 10 ** 9
    modules = imported_modules()
    standard = all(name in sys.stdlib_module_names for name in modules)
    # Row 15 holds the limit and the standard-library field, and row 40, beside it, holds the modules.
    limit_read = in_row(PREDICTED, "YM4_02C_SITE_SIGN_LIMITS", "runtime_seconds_at_most=600") and in_row(PREDICTED, "YM4_02C_SITE_SIGN_LIMITS", "python_standard_library_only=1")
    modules_read = in_row(PREDICTED, "YM4_02C_SITE_SIGN_LIMITS_2", "modules=" + joined(modules))
    print("SITE_SIGN_LIMITS|runtime_within_600_seconds=%d|limit_and_standard_library_fields_found_in_row_15=%d|modules=%s|modules_found_in_row_40=%d|all_in_the_standard_library=%d|ok=%d|json=0" % (flag(within), limit_read, joined(modules), modules_read, flag(standard), check("runtime and modules", within and standard and bool(limit_read) and bool(modules_read))))
    print("SITE_SIGN_RUNTIME|milliseconds=%d|json=0" % (elapsed_ns // 10 ** 6), file=sys.stderr)
    print("SITE_SIGN_DONE|failed=%d|json=0" % len(FAILS))
    for name in FAILS:
        print("FAILED|check=%s|json=0" % name.replace(" ", "_"))
    sys.exit(1 if FAILS else 0)


def main():
    if SABOTAGE == "side_one_in_the_rule":
        section_exhaustive()
    elif SABOTAGE == "count_inverted_classes_apart":
        section_groups()
    elif SABOTAGE == "drop_the_cycle":
        section_zeros()
    elif SABOTAGE == "time_like_weight_one":
        section_zeros_t()
    else:
        print("SITE_SIGN_TAGS|each_row_below=MEASURED_by_this_script|a_field_reading_DERIVED_or_OPEN_carries_that_tag_in_place|json=0")
        section_groups()
        section_lattices()
        section_exhaustive()
        section_torus_route()
        section_witnesses()
        section_side_one()
        section_spatial_product()
        section_side_counts()
        section_u1()
        section_su2_bands()
        section_zeros()
        section_zeros_t()
        section_su2()
        section_su2_zeros()
        section_cycle_parity()
        section_summary()
    finish()


main()
