#!/usr/bin/env python3
"""YM4-03: one-scale blocking, the exact pushforward, and what it induces.

The controls named in docs/PREDICTION-YM4-03.hbp, pushed at 7e6b111 before this file existed. The statements and their proofs are in
docs/NOTE-YM4-03-ONE-SCALE-BLOCKING.md. A law that holds or fails is a check, and a failed check exits 1. A value the prediction wrote by
hand is read as MET or MISS beside it, and a miss stays on record with no effect on the exit.

usage = test_one_scale_blocking.py [sabotage=NAME]
NAME is one of SABOTAGE_NAMES below, and each must exit 1 on a named check. An unknown name exits 2.
Python standard library, integers only, json=0.
"""
import itertools
import math
import os
import sys
import time

START_NS = time.perf_counter_ns()
SABOTAGE_NAMES = ("reversed_order", "shifted_endpoint", "dropped_inverse", "theta_no_inverse", "wrong_convolution_power", "wrong_first_coefficient", "extra_plaquette_factor", "wrong_block_shell", "twist_every_link", "flux_wrong_sign", "overlap_skips_next", "visibility_ignores_omega_error")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_one_scale_blocking.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []
MISSES = []
CHECKS = [0]


def say(text):
    print(text, flush=True)


def stamp(name):
    print("SECTION|%s|elapsed_seconds=%d" % (name, (time.perf_counter_ns() - START_NS) // 1000000000), file=sys.stderr, flush=True)


def check(name, ok):
    CHECKS[0] += 1
    if not ok:
        FAILS.append(name)
        say("FAILED|check=%s|json=0" % name)


def read_row(name, ok, read, predicted):
    say("YM4_03_READ|row=%s|result=%s|read=%s|predicted=%s|json=0" % (name, "MET" if ok else "MISS", read, predicted))
    if not ok:
        MISSES.append(name)


def ipow(base, exponent):
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


def fadd(a, b):
    return frac(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def fmul(a, b):
    return frac(a[0] * b[0], a[1] * b[1])


def fsub(a, b):
    return frac(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def show(pair):
    return "%d/%d" % pair if pair[1] != 1 else "%d" % pair[0]


class Stream:
    """A fixed linear congruential stream, so every run reads the same integers."""

    def __init__(self, seed):
        self.state = seed

    def next(self, bound):
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.state >> 33) % bound


# ---- SU(2) on the first route: rational unit quaternions (w, x, y, z, den).


def quat_norm(q):
    w, x, y, z, d = q
    g = math.gcd(math.gcd(math.gcd(math.gcd(w, x), y), z), d)
    if g > 1:
        w, x, y, z, d = w // g, x // g, y // g, z // g, d // g
    if d < 0:
        w, x, y, z, d = -w, -x, -y, -z, -d
    return w, x, y, z, d


def qmul(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return quat_norm((a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n))


def qinv(p):
    return p[0], -p[1], -p[2], -p[3], p[4]


Q_ONE = (1, 0, 0, 0, 1)


def is_unit(q):
    return q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3] == q[4] * q[4]


def qsquare_unit(a, b, c, d):
    """(a + bi + cj + dk)^2 / |.|^2, a rational unit quaternion."""
    p = (a, b, c, d, 1)
    s = qmul(p, p)
    return quat_norm((s[0], s[1], s[2], s[3], s[4] * (a * a + b * b + c * c + d * d)))


def half_trace(q):
    return frac(q[0], q[4])


def quaternion_pool(seed, size):
    stream = Stream(seed)
    pool = []
    while len(pool) < size:
        a, b, c, d = (stream.next(7) - 3 for _ in range(4))
        if a or b or c or d:
            q = qsquare_unit(a, b, c, d)
            assert is_unit(q)
            pool.append(q)
    return pool


# ---- SU(2) on the second route: 2 x 2 matrices of Gaussian rationals, (a,b,c,d,e,f,g,h,den) for [[a+ib, c+id],[e+if, g+ih]]/den.


def mat_from_quat(q):
    w, x, y, z, d = q
    return w, x, y, z, -y, z, w, -x, d


def mat_mul(p, q):
    a, b, c, d, e, f, g, h, m = p
    i, j, k, l, s, t, u, v, n = q
    out = (a * i - b * j + c * s - d * t, a * j + b * i + c * t + d * s, a * k - b * l + c * u - d * v, a * l + b * k + c * v + d * u,
           e * i - f * j + g * s - h * t, e * j + f * i + g * t + h * s, e * k - f * l + g * u - h * v, e * l + f * k + g * v + h * u, m * n)
    r = out[8]
    for value in out[:8]:
        r = math.gcd(r, value)
    return tuple(value // r for value in out) if r > 1 else out


def mat_inv(p):
    """The conjugate transpose, for a unitary matrix."""
    a, b, c, d, e, f, g, h, m = p
    return a, -b, e, -f, c, -d, g, -h, m


def mat_reduce(p):
    r = p[8]
    for value in p[:8]:
        r = math.gcd(r, value)
    return tuple(value // r for value in p)


MAT_ONE = (1, 0, 0, 0, 0, 0, 1, 0, 1)

# ---- The lattice.


def add(x, mu, sides, step=1):
    y = list(x)
    y[mu] = (y[mu] + step) % sides[mu]
    return tuple(y)


def sites_of(sides):
    return list(itertools.product(*(range(s) for s in sides)))


def fine_links_of_coarse(x_c, mu, b):
    """The fine links of the coarse link (x_c, mu), with the block factor per direction."""
    start = tuple(c * bi for c, bi in zip(x_c, b))
    out = []
    y = start
    for _ in range(b[mu]):
        out.append((y, mu))
        y = tuple((yi + (1 if i == mu else 0)) for i, yi in enumerate(y))
    return out


def wrap(link, sides):
    y, mu = link
    return tuple(c % s for c, s in zip(y, sides)), mu


def block_map(U, x_c, mu, b, sides, mul, one):
    order = fine_links_of_coarse(x_c, mu, b)
    if SABOTAGE == "reversed_order":
        order = order[::-1]
    out = one
    for link in order:
        out = mul(out, U[wrap(link, sides)])
    return out


def section_covariance():
    stamp("covariance")
    total = 0
    for name, b, sides, coarse in (("b=2", (2, 2, 2, 2), (4, 4, 4, 4), (2, 2, 2, 2)), ("b=3", (3, 3, 3, 3), (6, 6, 6, 6), (2, 2, 2, 2))):
        pool = quaternion_pool(20261105 + b[0], 48)
        stream = Stream(90210 + b[0])
        sites = sites_of(sides)
        U = {(x, mu): pool[stream.next(48)] for x in sites for mu in range(4)}
        g = {x: pool[stream.next(48)] for x in sites}
        gauged = {}
        for (x, mu), value in U.items():
            gauged[(x, mu)] = qmul(qmul(g[x], value), qinv(g[add(x, mu, sides)]))
        wrong_end = wrong_inv = 0
        rows = 0
        ok = True
        for x_c in sites_of(coarse):
            for mu in range(4):
                left = block_map(gauged, x_c, mu, b, sides, qmul, Q_ONE)
                start = tuple(c * bi for c, bi in zip(x_c, b))
                end = add(start, mu, sides, b[mu])
                inner = block_map(U, x_c, mu, b, sides, qmul, Q_ONE)
                formula = g[start]
                right_end = g[end]
                shifted = g[add(start, mu, sides, b[mu] - 1)]
                if SABOTAGE == "shifted_endpoint":
                    right_end = shifted
                inverse = qinv(right_end)
                if SABOTAGE == "dropped_inverse":
                    inverse = right_end
                right = qmul(qmul(formula, inner), inverse)
                ok = ok and left == right
                rows += 1
                if qmul(qmul(formula, inner), qinv(shifted)) != left:
                    wrong_end += 1
                if qmul(qmul(formula, inner), g[end]) != left:
                    wrong_inv += 1
        check("covariance_%s" % name, ok)
        check("broken_endpoint_differs_%s" % name, wrong_end > 0)
        check("broken_inverse_differs_%s" % name, wrong_inv > 0)
        # The reversed product is read by itself, whatever the sabotage.
        reversed_differs = 0
        for x_c in sites_of(coarse):
            for mu in range(4):
                order = fine_links_of_coarse(x_c, mu, b)
                product = Q_ONE
                for link in order[::-1]:
                    product = qmul(product, gauged[wrap(link, sides)])
                start = tuple(c * bi for c, bi in zip(x_c, b))
                if product != qmul(qmul(g[start], block_map(U, x_c, mu, b, sides, qmul, Q_ONE)), qinv(g[add(start, mu, sides, b[mu])])):
                    reversed_differs += 1
        check("broken_order_differs_%s" % name, reversed_differs > 0)
        say("YM4_03_COVARIANCE|%s|fine=%s|coarse_links=%d|broken_endpoint_rows=%d|broken_inverse_rows=%d|broken_order_rows=%d|json=0" % (name, "x".join(map(str, sides)), rows, wrong_end, wrong_inv, reversed_differs))
        total += rows
    return total


def holonomy_steps(U, start, steps, sides, mul, inv, one, unit):
    """The ordered product along steps (mu, sign), each moving `unit` fine links in direction mu."""
    x = start
    out = one
    for mu, sign in steps:
        for _ in range(unit[mu]):
            if sign > 0:
                out = mul(out, U[(x, mu)])
                x = add(x, mu, sides)
            else:
                x = add(x, mu, sides, -1)
                out = mul(out, inv(U[(x, mu)]))
    return out, x


def section_loops():
    stamp("closed_loops")
    for name, bi, sides in (("b=2", 2, (4, 4, 4, 4)), ("b=3", 3, (6, 6, 6, 6))):
        b = (bi,) * 4
        coarse = (2, 2, 2, 2)
        pool = quaternion_pool(777 + bi, 48)
        stream = Stream(4242 + bi)
        sites = sites_of(sides)
        U = {(x, mu): pool[stream.next(48)] for x in sites for mu in range(4)}
        M = {key: mat_from_quat(value) for key, value in U.items()}
        V = {(x, mu): block_map(U, x, mu, b, sides, qmul, Q_ONE) for x in sites_of(coarse) for mu in range(4)}
        families = {}
        families["plaquette"] = [((m, 1), (n, 1), (m, -1), (n, -1)) for m in range(4) for n in range(m + 1, 4)]
        families["rectangle_1x2"] = [((m, 1), (n, 1), (n, 1), (m, -1), (n, -1), (n, -1)) for m in range(4) for n in range(4) if m != n]
        families["hexagon"] = [((m, 1), (n, 1), (r, 1), (m, -1), (n, -1), (r, -1)) for m, n, r in itertools.permutations(range(4), 3)]
        families["winding"] = [((m, 1), (m, 1)) for m in range(4)]
        noncommuting = 0
        for family, words in families.items():
            good = routes = rows = 0
            for x_c in sites_of(coarse):
                start = tuple(c * bi for c in x_c)
                for word in words:
                    coarse_hol = Q_ONE
                    y = x_c
                    for mu, sign in word:
                        if sign > 0:
                            coarse_hol = qmul(coarse_hol, V[(y, mu)])
                            y = add(y, mu, coarse)
                        else:
                            y = add(y, mu, coarse, -1)
                            coarse_hol = qmul(coarse_hol, qinv(V[(y, mu)]))
                    assert y == x_c
                    fine_hol, end = holonomy_steps(U, start, word, sides, qmul, qinv, Q_ONE, b)
                    assert end == start
                    fine_mat, _ = holonomy_steps(M, start, word, sides, mat_mul, mat_inv, MAT_ONE, b)
                    rows += 1
                    good += coarse_hol == fine_hol
                    routes += mat_reduce(mat_from_quat(fine_hol)) == mat_reduce(fine_mat)
                    noncommuting += qmul(coarse_hol, V[(x_c, word[0][0])]) != qmul(V[(x_c, word[0][0])], coarse_hol)
            check("closed_loops_%s_%s" % (name, family), good == rows)
            check("two_routes_%s_%s" % (name, family), routes == rows)
            say("YM4_03_LOOPS|%s|family=%s|rows=%d|equal=%d|routes_equal=%d|json=0" % (name, family, rows, good, routes))
        check("closed_loops_%s_noncommuting" % name, noncommuting > 0)


def section_reflection():
    stamp("reflection_map")
    for bi, side in ((2, 4), (3, 6)):
        b = (bi,) * 4
        sides = (side,) * 4
        coarse = (2, 2, 2, 2)
        pool = quaternion_pool(1313 + bi, 48)
        stream = Stream(5151 + bi)
        sites = sites_of(sides)
        U = {(x, mu): pool[stream.next(48)] for x in sites for mu in range(4)}
        for c_coarse in (0, -1):
            c = bi * c_coarse
            reflected = {}
            for (x, mu) in U:
                t = x[3]
                if mu < 3:
                    reflected[(x, mu)] = U[((x[0], x[1], x[2], (c - t) % side), mu)]
                else:
                    value = U[((x[0], x[1], x[2], (c - t - 1) % side), 3)]
                    reflected[(x, mu)] = value if SABOTAGE == "theta_no_inverse" else qinv(value)
            V = {(x, mu): block_map(U, x, mu, b, sides, qmul, Q_ONE) for x in sites_of(coarse) for mu in range(4)}
            good = rows = broken = 0
            for x_c in sites_of(coarse):
                for mu in range(4):
                    left = block_map(reflected, x_c, mu, b, sides, qmul, Q_ONE)
                    t = x_c[3]
                    if mu < 3:
                        right = V[((x_c[0], x_c[1], x_c[2], (c_coarse - t) % 2), mu)]
                    else:
                        right = qinv(V[((x_c[0], x_c[1], x_c[2], (c_coarse - t - 1) % 2), 3)])
                        if left != V[((x_c[0], x_c[1], x_c[2], (c_coarse - t - 1) % 2), 3)]:
                            broken += 1
                    rows += 1
                    good += left == right
            check("reflection_map_b=%d_c=%d" % (bi, c_coarse), good == rows)
            check("reflection_broken_differs_b=%d_c=%d" % (bi, c_coarse), broken > 0)
            say("YM4_03_REFLECTION|b=%d|c_coarse=%d|rows=%d|equal=%d|broken_rows=%d|json=0" % (bi, c_coarse, rows, good, broken))


# ---- Finite groups.


class Group:
    def __init__(self, name, table):
        self.name = name
        self.n = len(table)
        self.table = table
        self.identity = next(i for i in range(self.n) if all(table[i][j] == j for j in range(self.n)))
        self.inverse = [next(j for j in range(self.n) if table[i][j] == self.identity) for i in range(self.n)]
        seen = {}
        classes = []
        for g in range(self.n):
            if g in seen:
                continue
            members = {table[table[h][g]][self.inverse[h]] for h in range(self.n)}
            for m in members:
                seen[m] = len(classes)
            classes.append(sorted(members))
        self.classes = classes
        self.class_of = seen

    def mul(self, a, b):
        return self.table[a][b]


def group_from(name, elements, product):
    index = {e: i for i, e in enumerate(elements)}
    return Group(name, [[index[product(a, b)] for b in elements] for a in elements])


def doubled_hurwitz(a, b):
    """The product of quaternions held at twice their value."""
    p, q, r, s = a
    t, u, v, w = b
    out = (p * t - q * u - r * v - s * w, p * u + q * t + r * w - s * v, p * v - q * w + r * t + s * u, p * w + q * v - r * u + s * t)
    return tuple(c // 2 for c in out)


def make_groups():
    groups = {}
    groups["Z2"] = Group("Z2", [[(a + b) % 2 for b in range(2)] for a in range(2)])
    groups["Z3"] = Group("Z3", [[(a + b) % 3 for b in range(3)] for a in range(3)])
    perms = list(itertools.permutations(range(3)))
    groups["S3"] = group_from("S3", perms, lambda a, b: tuple(a[b[i]] for i in range(3)))
    q8 = [(2, 0, 0, 0), (-2, 0, 0, 0), (0, 2, 0, 0), (0, -2, 0, 0), (0, 0, 2, 0), (0, 0, -2, 0), (0, 0, 0, 2), (0, 0, 0, -2)]
    groups["Q8"] = group_from("Q8", q8, doubled_hurwitz)
    t2 = q8 + [tuple(s) for s in itertools.product((1, -1), repeat=4)]
    groups["2T"] = group_from("2T", t2, doubled_hurwitz)
    return groups, q8, t2


GROUPS, Q8_ELEMENTS, T2_ELEMENTS = make_groups()


def weight_three_plus(group_name):
    """w = 3 + chi, with chi the fundamental or sum of faithful characters, on each element: positive, and of positive character coefficients."""
    g = GROUPS[group_name]
    if group_name == "Z2":
        return [4 if i == g.identity else 2 for i in range(2)]
    if group_name == "Z3":
        return [5 if i == g.identity else 2 for i in range(3)]
    if group_name == "S3":
        perms = list(itertools.permutations(range(3)))
        out = []
        for p in perms:
            fixed = sum(1 for i in range(3) if p[i] == i)
            out.append(3 + fixed - 1)
        return out
    if group_name == "Q8":
        return [3 + e[0] for e in Q8_ELEMENTS]
    if group_name == "2T":
        return [3 + e[0] for e in T2_ELEMENTS]
    raise ValueError(group_name)


def section_haar():
    stamp("haar_pushforward")
    for name in ("Z2", "Z3", "S3", "Q8", "2T"):
        g = GROUPS[name]
        for b in (2, 3):
            counts = [0] * g.n
            for word in itertools.product(range(g.n), repeat=b):
                value = g.identity
                for u in word:
                    value = g.table[value][u]
                counts[value] += 1
            check("haar_pushforward_%s_b=%d" % (name, b), all(c == ipow(g.n, b - 1) for c in counts))
        say("YM4_03_HAAR|group=%s|order=%d|every_V_has_preimages=%d_at_b=2_and_%d_at_b=3|json=0" % (name, g.n, g.n, g.n * g.n))


class FiniteLattice:
    """Fine lattice with block factors per direction. Links are indexed, and plaquettes are words of (link, sign)."""

    def __init__(self, sides, b):
        self.sides = sides
        self.b = b
        self.d = len(sides)
        self.coarse = tuple(s // bi for s, bi in zip(sides, b))
        self.sites = sites_of(sides)
        self.links = {}
        for x in self.sites:
            for mu in range(self.d):
                self.links[(x, mu)] = len(self.links)
        self.plaquettes = []
        self.plaquette_keys = []
        for x in self.sites:
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    word = ((self.links[(x, mu)], 1), (self.links[(add(x, mu, sides), nu)], 1), (self.links[(add(x, nu, sides), mu)], -1), (self.links[(x, nu)], -1))
                    self.plaquettes.append(word)
                    self.plaquette_keys.append((x, mu, nu))
        self.coarse_links = []
        self.line_of = {}
        for x_c in sites_of(self.coarse):
            for mu in range(self.d):
                fine = [self.links[wrap(link, sides)] for link in fine_links_of_coarse(x_c, mu, b)]
                index = len(self.coarse_links)
                self.coarse_links.append(((x_c, mu), fine))
                for position, link in enumerate(fine):
                    self.line_of[link] = (index, position)
        self.coarse_index = {key: i for i, (key, _) in enumerate(self.coarse_links)}
        self.coarse_plaquettes = []
        for x_c in sites_of(self.coarse):
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    self.coarse_plaquettes.append(((self.coarse_index[(x_c, mu)], 1), (self.coarse_index[(add(x_c, mu, self.coarse), nu)], 1), (self.coarse_index[(add(x_c, nu, self.coarse), mu)], -1), (self.coarse_index[(x_c, nu)], -1)))

    def word_value(self, word, values, g):
        out = g.identity
        for link, sign in word:
            u = values[link]
            out = g.table[out][u if sign > 0 else g.inverse[u]]
        return out


def eliminate(n, factors, keep=()):
    """Exact sum over all variables not in keep of the product of factors. A factor is (vars, dict assignment -> integer)."""
    factors = list(factors)
    keep = set(keep)
    variables = set()
    for vs, _ in factors:
        variables.update(vs)
    variables -= keep
    while variables:
        best = None
        for v in variables:
            union = set()
            for vs, _ in factors:
                if v in vs:
                    union.update(vs)
            size = len(union)
            if best is None or size < best[0]:
                best = (size, v, union)
        _, v, union = best
        chosen = [f for f in factors if v in f[0]]
        rest = [f for f in factors if v not in f[0]]
        others = sorted(union - {v})
        table = {}
        positions = [[(others.index(u) if u != v else -1) for u in vs] for vs, _ in chosen]
        for assignment in itertools.product(range(n), repeat=len(others)):
            total = 0
            for value in range(n):
                product = 1
                for (vs, data), pos in zip(chosen, positions):
                    key = tuple(value if p < 0 else assignment[p] for p in pos)
                    entry = data.get(key, 0)
                    if not entry:
                        product = 0
                        break
                    product *= entry
                total += product
            if total:
                table[assignment] = total
        factors = rest + [(tuple(others), table)]
        variables.discard(v)
    out = 1
    for vs, data in factors:
        if not vs:
            out *= data.get((), 0)
    return out, factors


def raw_density(lat, g, weight, V, extra=False, exclude_constraint=False):
    """Sum over fine configurations with B U = V of prod_p w(U_p), by elimination with the lines' constraints as factors."""
    n = g.n
    factors = []
    plaquettes = list(lat.plaquettes)
    if extra:
        plaquettes.append(plaquettes[0])
    for word in plaquettes:
        vs = sorted({link for link, _ in word})
        data = {}
        for assignment in itertools.product(range(n), repeat=len(vs)):
            local = dict(zip(vs, assignment))
            data[assignment] = weight[lat.word_value(word, local, g)]
        factors.append((tuple(vs), data))
    for index, (key, fine) in enumerate(lat.coarse_links):
        data = {}
        vs = tuple(fine)
        for assignment in itertools.product(range(n), repeat=len(fine)):
            value = g.identity
            for u in assignment:
                value = g.table[value][u]
            if value == V[index]:
                data[assignment] = 1
        factors.append((vs, data))
    total, _ = eliminate(n, factors)
    return total


def brute_density(lat, g, weight, extra=False):
    """Every fine configuration, once: raw[V], the sum over B U = V of prod_p w, on small lattices."""
    n = g.n
    links = len(lat.links)
    raw = {}
    total = 0
    words = lat.plaquettes + ([lat.plaquettes[0]] if extra else [])
    for values in itertools.product(range(n), repeat=links):
        product = 1
        for word in words:
            product *= weight[lat.word_value(word, values, g)]
        V = []
        for _, fine in lat.coarse_links:
            value = g.identity
            for link in fine:
                value = g.table[value][values[link]]
            V.append(value)
        V = tuple(V)
        raw[V] = raw.get(V, 0) + product
        total += product
    return raw, total


def raw_fixed(lat, g, weight, V, extra=False):
    """raw_density by the gauge at the sites off the coarse lattice: each line carries V on its last link, and each further site fixes one off link.
    Every fixed link is worth a factor n, so raw = n^fixed * the sum over the rest. Read against raw_density on the small lattices."""
    n = g.n
    index_to_key = {v: k for k, v in lat.links.items()}
    values = {}
    anchored = {tuple(c * bi for c, bi in zip(x_c, lat.b)) for x_c in sites_of(lat.coarse)}
    fixed_count = 0
    for index, (_, fine) in enumerate(lat.coarse_links):
        for k, link in enumerate(fine):
            values[link] = V[index] if k == len(fine) - 1 else g.identity
            x, mu = index_to_key[link]
            for site in (x, add(x, mu, lat.sides)):
                anchored.add(site)
        fixed_count += len(fine) - 1
    # A self-loop off the lines stays free; the rest grows a forest out of the anchored sites.
    off = [link for link in index_to_key if link not in values]
    fixed = set()
    changed = True
    while changed:
        changed = False
        for link in off:
            if link in fixed:
                continue
            x, mu = index_to_key[link]
            y = add(x, mu, lat.sides)
            if (x in anchored) != (y in anchored):
                fixed.add(link)
                anchored.add(y if x in anchored else x)
                values[link] = g.identity
                fixed_count += 1
                changed = True
    factors = []
    constant = 1
    plaquettes = list(lat.plaquettes)
    if extra:
        plaquettes.append(plaquettes[0])
    for word in plaquettes:
        vs = sorted({link for link, _ in word if link not in values})
        if not vs:
            constant *= weight[lat.word_value(word, values, g)]
            continue
        data = {}
        for assignment in itertools.product(range(n), repeat=len(vs)):
            local = dict(values)
            local.update(zip(vs, assignment))
            data[assignment] = weight[lat.word_value(word, local, g)]
        factors.append((tuple(vs), data))
    total, _ = eliminate(n, factors)
    free = {v for vs, _ in factors for v in vs}
    untouched = len(off) - len(fixed) - len(free)
    return constant * total * ipow(n, fixed_count + untouched)


def convolution_power(g, weight, m):
    """W_m with w^(m) = W_m / n^(m-1), as integers on the elements."""
    out = list(weight)
    for _ in range(m - 1):
        next_out = [0] * g.n
        for x in range(g.n):
            for y in range(g.n):
                next_out[x] += out[g.table[x][g.inverse[y]]] * weight[y]
        out = next_out
    return out


def coarse_product(lat, g, power, V):
    product = 1
    for word in lat.coarse_plaquettes:
        product *= power[lat.word_value(word, V, g)]
    return product


def section_pushforward():
    stamp("integral_identity")
    # Two routes on small lattices: every fine configuration against elimination, with the integral identity and the normalization.
    for name, sides, b in (("Z3", (2, 2), (2, 2)), ("S3", (2, 2), (2, 2))):
        g = GROUPS[name]
        w = weight_three_plus(name)
        lat = FiniteLattice(sides, b)
        raw, total = brute_density(lat, g, w)
        coarse_count = len(lat.coarse_links)
        equal = rows = 0
        eliminated = {}
        for V in itertools.product(range(g.n), repeat=coarse_count):
            if rows >= 40 and name == "S3":
                break
            rows += 1
            eliminated[V] = raw_density(lat, g, w, V, extra=(SABOTAGE == "extra_plaquette_factor"))
            equal += eliminated[V] == raw.get(V, 0)
        check("normalization_%s" % name, sum(eliminated.values()) == total)
        check("brute_equals_elimination_%s" % name, equal == rows)
        check("gauge_fixed_equals_brute_%s" % name, all(raw_fixed(lat, g, w, V) == value for V, value in itertools.islice(raw.items(), 0, 40)))
        # F: a noncommuting coarse Wilson loop, and a function that is gauge-variant.
        left_loop = 0
        right_loop = 0
        for V, value in eliminated.items():
            loop = lat.word_value(lat.coarse_plaquettes[0], V, g)
            f_value = w[loop]
            left_loop += f_value * value
            f_variant = 1 + V[0]
            right_loop += f_variant * value
        direct_loop = direct_variant = 0
        for values in itertools.product(range(g.n), repeat=len(lat.links)):
            product = 1
            for word in lat.plaquettes:
                product *= w[lat.word_value(word, values, g)]
            V = []
            for _, fine in lat.coarse_links:
                value = g.identity
                for link in fine:
                    value = g.table[value][values[link]]
                V.append(value)
            V = tuple(V)
            direct_loop += w[lat.word_value(lat.coarse_plaquettes[0], V, g)] * product
            direct_variant += (1 + V[0]) * product
        check("integral_identity_loop_%s" % name, left_loop == direct_loop)
        check("integral_identity_variant_%s" % name, right_loop == direct_variant)
        # The coarse loop against the fine b x b rectangle, by its own word.
        rectangle_equal = True
        for values in itertools.islice(itertools.product(range(g.n), repeat=len(lat.links)), 0, 400):
            V = []
            for _, fine in lat.coarse_links:
                value = g.identity
                for link in fine:
                    value = g.table[value][values[link]]
                V.append(value)
            rectangle = g.identity
            x = (0, 0)
            for mu, sign, count in ((0, 1, 2), (1, 1, 2), (0, -1, 2), (1, -1, 2)):
                for _ in range(count):
                    if sign > 0:
                        rectangle = g.table[rectangle][values[lat.links[(x, mu)]]]
                        x = add(x, mu, sides)
                    else:
                        x = add(x, mu, sides, -1)
                        rectangle = g.table[rectangle][g.inverse[values[lat.links[(x, mu)]]]]
            rectangle_equal = rectangle_equal and rectangle == lat.word_value(lat.coarse_plaquettes[0], V, g)
        check("coarse_loop_is_fine_rectangle_%s" % name, rectangle_equal)
        # Gauge invariance of rho, every coarse g on the one coarse site, on all V.
        invariant = True
        for V, value in raw.items():
            for h in range(g.n):
                moved = tuple(g.table[g.table[h][v]][g.inverse[h]] for v in V)
                invariant = invariant and raw.get(moved, 0) == value
        check("rho_gauge_invariant_%s" % name, invariant)
        say("YM4_03_PUSHFORWARD|group=%s|fine=%s|sum_over_fine_configurations=%d|V_read_by_elimination=%d|equal=%d|json=0" % (name, "x".join(map(str, sides)), total, rows, equal))
    # Two coarse sites: gauge invariance with independent g at each.
    g = GROUPS["Z3"]
    w = weight_three_plus("Z3")
    lat = FiniteLattice((4, 2), (2, 2))
    stream = Stream(31)
    invariant = True
    for _ in range(6):
        V = [stream.next(3) for _ in lat.coarse_links]
        base = raw_density(lat, g, w, V)
        for h0 in range(3):
            for h1 in range(3):
                gauge = {(0, 0): h0, (1, 0): h1}
                moved = []
                for ((x_c, mu), _), value in zip(lat.coarse_links, V):
                    moved.append(g.table[g.table[gauge[x_c]][value]][g.inverse[gauge[add(x_c, mu, lat.coarse)]]])
                invariant = invariant and raw_density(lat, g, w, moved) == base
    check("rho_gauge_invariant_two_sites_Z3", invariant)
    stream = Stream(32)
    check("gauge_fixed_equals_elimination_Z3_4x2", all(raw_fixed(lat, g, w, V) == raw_density(lat, g, w, V) for V in ([stream.next(3) for _ in lat.coarse_links] for _ in range(5))))
    g = GROUPS["Q8"]
    w = weight_three_plus("Q8")
    lat = FiniteLattice((2, 2), (2, 2))
    stream = Stream(33)
    check("gauge_fixed_equals_elimination_Q8_2x2", all(raw_fixed(lat, g, w, V) == raw_density(lat, g, w, V) for V in ([stream.next(8) for _ in lat.coarse_links] for _ in range(3))))
    say("YM4_03_PUSHFORWARD_TWO_SITES|group=Z3|fine=4x2|configurations=6|gauge_images=9_each|invariant=%d|json=0" % invariant)


def real_characters(name):
    g = GROUPS[name]
    if name == "S3":
        perms = list(itertools.permutations(range(3)))
        chars = {}
        chars["trivial"] = (1, [1] * 6)
        sign = []
        two = []
        for p in perms:
            fixed = sum(1 for i in range(3) if p[i] == i)
            sign.append(1 if fixed != 1 else -1)
            two.append(fixed - 1)
        chars["sign"] = (1, sign)
        chars["two"] = (2, two)
        return chars
    if name == "Q8":
        chars = {"trivial": (1, [1] * 8), "fund": (2, [e[0] for e in Q8_ELEMENTS])}
        for axis, label in ((1, "i"), (2, "j"), (3, "k")):
            values = []
            for e in Q8_ELEMENTS:
                values.append(1 if e[0] != 0 or e[axis] != 0 else -1)
            chars[label] = (1, values)
        return chars
    raise ValueError(name)


def section_two_dimensions():
    stamp("two_dimensions")
    cases = [("Z3", (2, 2), (2, 2), 81), ("S3", (2, 2), (2, 2), 60), ("Q8", (2, 2), (2, 2), 40), ("2T", (2, 2), (2, 2), 12), ("Z3", (3, 3), (3, 3), 81), ("S3", (3, 3), (3, 3), 8), ("Z3", (4, 2), (2, 2), 40), ("S3", (4, 2), (2, 2), 6), ("Z3", (4, 4), (2, 2), 12), ("S3", (4, 4), (2, 2), 6)]
    for name, sides, b, limit in cases:
        g = GROUPS[name]
        w = weight_three_plus(name)
        lat = FiniteLattice(sides, b)
        m = b[0] * b[1]
        power_used = m + 1 if SABOTAGE == "wrong_convolution_power" else m
        power = convolution_power(g, w, power_used)
        coarse_links = len(lat.coarse_links)
        stream = Stream(600 + g.n + b[0])
        rows = good = 0
        scale_left = ipow(g.n, (m - 1) * len(lat.coarse_plaquettes))
        scale_right = ipow(g.n, len(lat.links) - coarse_links)
        if SABOTAGE == "wrong_convolution_power":
            scale_left = ipow(g.n, (power_used - 1) * len(lat.coarse_plaquettes))
        for _ in range(limit):
            V = [stream.next(g.n) for _ in range(coarse_links)]
            raw = raw_fixed(lat, g, w, V)
            rows += 1
            good += raw * scale_left == coarse_product(lat, g, power, V) * scale_right
        check("two_dimensions_closes_%s_b=%d_%s" % (name, b[0], "x".join(map(str, sides))), good == rows)
        say("YM4_03_TWO_DIMENSIONS|group=%s|fine=%s|b=%d|V_read=%d|equal_to_the_closed_form=%d|json=0" % (name, "x".join(map(str, sides)), b[0], rows, good))
    # The flow on characters.
    for name in ("S3", "Q8"):
        g = GROUPS[name]
        w = weight_three_plus(name)
        chars = real_characters(name)
        for label, (dimension, values) in chars.items():
            base = frac(sum(w[i] * values[g.inverse[i]] for i in range(g.n)), g.n * dimension)
            good = True
            for m in (2, 4, 9):
                power = convolution_power(g, w, m)
                got = frac(sum(power[i] * values[g.inverse[i]] for i in range(g.n)), ipow(g.n, m - 1) * g.n * dimension)
                good = good and got == frac(ipow(base[0], m), ipow(base[1], m))
            check("character_flow_%s_%s" % (name, label), good)
            say("YM4_03_CHARACTER_FLOW|group=%s|character=%s|dimension=%d|c=%s|c_at_m=2,4,9_equals_c^m=%d|json=0" % (name, label, dimension, show(base), good))
    # No term beyond the plaquette in d = 2: the four-point ratio on links in no common coarse plaquette.
    g = GROUPS["Z3"]
    w = weight_three_plus("Z3")
    lat = FiniteLattice((4, 4), (2, 2))
    a = lat.coarse_index[((0, 0), 0)]
    c = lat.coarse_index[((1, 0), 0)]
    in_common = any({a, c} <= {link for link, _ in word} for word in lat.coarse_plaquettes)
    check("two_dimensions_pair_shares_no_plaquette", not in_common)
    stream = Stream(777)
    equal = rows = 0
    for _ in range(3):
        V = [stream.next(3) for _ in lat.coarse_links]
        Va = list(V)
        Vb = list(V)
        Vab = list(V)
        Va[a] = (V[a] + 1) % 3
        Vb[c] = (V[c] + 1) % 3
        Vab[a] = Va[a]
        Vab[c] = Vb[c]
        rows += 1
        equal += raw_fixed(lat, g, w, V) * raw_fixed(lat, g, w, Vab) == raw_fixed(lat, g, w, Va) * raw_fixed(lat, g, w, Vb)
    check("two_dimensions_no_far_term_Z3", equal == rows)
    say("YM4_03_NO_FAR_TERM|d=2|group=Z3|fine=4x4|configurations=%d|four_point_ratio_exactly_1=%d|json=0" % (rows, equal))


def section_three_dimensions():
    stamp("three_dimensions")
    g = GROUPS["Q8"]
    w = weight_three_plus("Q8")
    lat = FiniteLattice((2, 2, 1), (2, 2, 1))
    one = Q8_ELEMENTS.index((2, 0, 0, 0))
    i = Q8_ELEMENTS.index((0, 2, 0, 0))
    j = Q8_ELEMENTS.index((0, 0, 2, 0))
    coarse_index = {lat.coarse_links[k][0][1]: k for k in range(3)}
    values = {}
    for label, triple in (("1,1,1", (one, one, one)), ("i,1,1", (i, one, one)), ("1,i,1", (one, i, one)), ("1,1,i", (one, one, i)), ("i,j,1", (i, j, one)), ("i,1,j", (i, one, j))):
        V = [0, 0, 0]
        for mu in range(3):
            V[coarse_index[mu]] = triple[mu]
        values[label] = raw_fixed(lat, g, w, V)
    total_links = len(lat.links)
    same_commutators = values["1,1,1"] != values["i,1,1"] or values["1,1,1"] != values["1,1,i"]
    read_row("three_dimensions_leaves_wilson_form", same_commutators, "rho(i,1,1)/rho(1,1,1)=%s;rho(1,1,i)/rho(1,1,1)=%s" % (show(frac(values["i,1,1"], values["1,1,1"])), show(frac(values["1,1,i"], values["1,1,1"]))), "not_1")
    say("YM4_03_THREE_DIMENSIONS|group=Q8|fine=2x2x1|fine_links=%d|%s|json=0" % (total_links, "|".join("raw(%s)=%d" % (k, v) for k, v in values.items())))
    # The same reading in d = 2 is exact: rho depends on the commutator alone.
    lat2 = FiniteLattice((2, 2), (2, 2))
    power = convolution_power(g, w, 4)
    check("d2_comparison_commutator_only", raw_fixed(lat2, g, w, [i, one]) == raw_fixed(lat2, g, w, [one, one]) and coarse_product(lat2, g, power, [i, one]) == coarse_product(lat2, g, power, [one, one]))
    # Z2 on two coarse sites: a pair in no common coarse plaquette.
    g2 = GROUPS["Z2"]
    w2 = [3, 1]
    lat3 = FiniteLattice((4, 2, 2), (2, 2, 2))
    a = lat3.coarse_index[((0, 0, 0), 1)]
    c = lat3.coarse_index[((1, 0, 0), 2)]
    common = any({a, c} <= {link for link, _ in word} for word in lat3.coarse_plaquettes)
    check("z2_small_pair_shares_no_plaquette", not common)
    V = [0] * len(lat3.coarse_links)
    Va = list(V)
    Va[a] = 1
    Vb = list(V)
    Vb[c] = 1
    Vab = list(Va)
    Vab[c] = 1
    base, ra, rb, rab = (raw_fixed(lat3, g2, w2, x) for x in (V, Va, Vb, Vab))
    ratio = frac(base * rab, ra * rb)
    read_row("z2_exact_small", ratio != (1, 1), show(ratio), "not_1_at_u=1/2")


# ---- First dependence on V, for SU(2), with 2T within its design degree.

T2_QUATS = [quat_norm((e[0], e[1], e[2], e[3], 2)) for e in T2_ELEMENTS]


def term_for_component(lat, multiset, line_values, points=None):
    """E[prod a_p^m] over the off links the set touches, by 2T within its degree, with the lines carrying V at a chosen position.
    Gauge at the sites of the set with no coarse site or line fixes one link per spanning step, so the sum stays small."""
    used = {}
    for p, multiplicity in multiset:
        for link, _ in lat.plaquettes[p]:
            used[link] = used.get(link, 0) + multiplicity
    free = sorted(link for link in used if link not in line_values)
    for link in free:
        assert used[link] <= 5, "beyond the design degree"
    # A free link appearing once integrates the character to zero by the same parity the enumeration used; here all appear at least twice.
    link_sites = {}
    index_to_key = {v: k for k, v in lat.links.items()}
    for link in free:
        x, mu = index_to_key[link]
        link_sites[link] = (x, add(x, mu, lat.sides))
    # Sites fixed by the lines or the coarse lattice stay anchored.
    anchored = set()
    for link in used:
        if link in line_values:
            x, mu = index_to_key[link]
            anchored.add(x)
            anchored.add(add(x, mu, lat.sides))
    for x in lat.sites:
        if all(c % bi == 0 for c, bi in zip(x, lat.b)):
            anchored.add(x)
    fixed = set()
    changed = True
    while changed:
        changed = False
        for link in free:
            if link in fixed:
                continue
            a, b = link_sites[link]
            if a == b:
                continue
            if (a in anchored) != (b in anchored):
                other = b if a in anchored else a
                if not (all(c % bi == 0 for c, bi in zip(other, lat.b))):
                    fixed.add(link)
                    anchored.add(other)
                    changed = True
    # Sites off the anchored set, with no path to it, can still each fix one link.
    while True:
        roots = [link for link in free if link not in fixed and link_sites[link][0] != link_sites[link][1] and link_sites[link][0] not in anchored and link_sites[link][1] not in anchored]
        if not roots:
            break
        a, b = link_sites[roots[0]]
        anchored.add(a)
        changed = True
        while changed:
            changed = False
            for link in free:
                if link in fixed:
                    continue
                c, d = link_sites[link]
                if c == d:
                    continue
                if (c in anchored) != (d in anchored):
                    fixed.add(link)
                    anchored.add(d if c in anchored else c)
                    changed = True
    variables = [link for link in free if link not in fixed]
    values = dict(line_values)
    for link in fixed:
        values[link] = Q_ONE
    total = (0, 1)
    count = 0
    for assignment in itertools.product(points or T2_QUATS, repeat=len(variables)):
        for link, q in zip(variables, assignment):
            values[link] = q
        product = (1, 1)
        for p, multiplicity in multiset:
            out = Q_ONE
            for link, sign in lat.plaquettes[p]:
                out = qmul(out, values[link] if sign > 0 else qinv(values[link]))
            trace = half_trace(out)
            for _ in range(multiplicity):
                product = fmul(product, trace)
        total = fadd(total, product)
        count += 1
    return frac(total[0], total[1] * count)


SINGLE_POWER = {}


def single_power(m):
    """E[a^m] with a = half the trace of one Haar element, by 2T within its degree."""
    if m not in SINGLE_POWER:
        total = (0, 1)
        for q in T2_QUATS:
            trace = half_trace(q)
            value = (1, 1)
            for _ in range(m):
                value = fmul(value, trace)
            total = fadd(total, value)
        SINGLE_POWER[m] = frac(total[0], total[1] * len(T2_QUATS))
    return SINGLE_POWER[m]


def term_for_multiset(lat, multiset, line_values, memo):
    """The term splits over the sets of plaquettes joined by off links. A plaquette alone with an off link is E[a^m], whatever the rest of its word."""
    parent = {p: p for p, _ in multiset}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    owner = {}
    for p, _ in multiset:
        for link, _ in lat.plaquettes[p]:
            if link in line_values:
                continue
            if link in owner:
                parent[find(p)] = find(owner[link])
            else:
                owner[link] = p
    groups = {}
    for p, m in multiset:
        groups.setdefault(find(p), []).append((p, m))
    out = (1, 1)
    for group in groups.values():
        key = tuple(sorted(group))
        if key not in memo:
            if len(group) == 1 and any(link not in line_values for link, _ in lat.plaquettes[group[0][0]]):
                words = lat.plaquettes[group[0][0]]
                free_links = [link for link, _ in words if link not in line_values]
                if len(set(free_links)) == len(free_links):
                    memo[key] = single_power(group[0][1])
                else:
                    memo[key] = term_for_component(lat, key, line_values)
            else:
                memo[key] = term_for_component(lat, key, line_values)
        out = fmul(out, memo[key])
        if out[0] == 0:
            return (0, 1)
    return out


def surviving_multisets(lat, size, touching):
    """Multisets of `size` plaquettes where each off link appears an even number of times and each line's links share one parity, with at least one plaquette in `touching`."""
    masks = []
    line_groups = {}
    for link, (index, _) in lat.line_of.items():
        line_groups.setdefault(index, []).append(link)
    for word in lat.plaquettes:
        mask = 0
        for link, _ in word:
            mask ^= 1 << link
        masks.append(mask)
    allowed_groups = [sum(1 << link for link in links) for links in line_groups.values()]
    off_mask = 0
    for link in range(len(lat.links)):
        if link not in lat.line_of:
            off_mask |= 1 << link

    def admissible(mask):
        if mask & off_mask:
            return False
        for group in allowed_groups:
            part = mask & group
            if part and part != group:
                return False
        return True

    n = len(masks)
    out = []
    if size == 1:
        for p in range(n):
            if admissible(masks[p]) and p in touching:
                out.append(((p, 1),))
        return out
    if size == 2:
        for p in range(n):
            for q in range(p, n):
                if admissible(masks[p] ^ masks[q]) and (p in touching or q in touching):
                    out.append(((p, 2),) if p == q else ((p, 1), (q, 1)))
        return out
    pairs = {}
    for p in range(n):
        for q in range(p, n):
            pairs.setdefault(masks[p] ^ masks[q], []).append((p, q))
    # Each admissible total is a sum over the coarse-line groups, so it is enough to walk one plaquette from touching and close it.
    found = set()
    allowed_totals = [0]
    for group in allowed_groups:
        allowed_totals = allowed_totals + [t ^ group for t in allowed_totals]
    if size == 3:
        for p in touching:
            for total in allowed_totals:
                for q, r in pairs.get(masks[p] ^ total, ()):
                    found.add(tuple(sorted((p, q, r))))
    else:
        for p in touching:
            for q in range(n):
                for total in allowed_totals:
                    for r, s in pairs.get(masks[p] ^ masks[q] ^ total, ()):
                        found.add(tuple(sorted((p, q, r, s))))
    for items in sorted(found):
        counted = {}
        for p in items:
            counted[p] = counted.get(p, 0) + 1
        out.append(tuple(sorted(counted.items())))
    return out


def multinomial_inverse(multiset):
    d = 1
    for _, m in multiset:
        for i in range(2, m + 1):
            d *= i
    return 1, d


def rational_unit_direction(a, b, c, den):
    """A pure unit quaternion from a rational point on the sphere: (a,b,c)/den with a^2+b^2+c^2 = den^2."""
    assert a * a + b * b + c * c == den * den
    return quat_norm((0, a, b, c, den))


def coarse_chi(lat, V_quats):
    out = (0, 1)
    for word in lat.coarse_plaquettes:
        product = Q_ONE
        for index, sign in word:
            product = qmul(product, V_quats[index] if sign > 0 else qinv(V_quats[index]))
        out = fadd(out, fmul((2, 1), half_trace(product)))
    return out


def lines_with_V(lat, V_quats, position):
    values = {}
    for index, (_, fine) in enumerate(lat.coarse_links):
        at = position % len(fine)
        for k, link in enumerate(fine):
            values[link] = V_quats[index] if k == at else Q_ONE
    return values


def flat_filling_coefficient(bi):
    """E_V of the flat b x b filling over chi(V_p') on (Z/b)^3, at noncommuting V. Each free link of the filling has degree exactly 2, and on homogeneous polynomials of degree 2 the four points 1, i, j, k average as Haar does, so they carry the average."""
    lat = FiniteLattice((bi, bi, bi), (bi, bi, bi))
    v_x, v_y = (3, 4, 0, 0, 5), (5, 0, 12, 0, 13)
    multiset = tuple(sorted((lat.plaquette_keys.index(((s, r, 0), 0, 1)), 1) for s in range(bi) for r in range(bi)))
    term = term_for_component(lat, multiset, lines_with_V(lat, [v_x, v_y, Q_ONE], 0), [(1, 0, 0, 0, 1), (0, 1, 0, 0, 1), (0, 0, 1, 0, 1), (0, 0, 0, 1, 1)])
    chi = fmul((2, 1), half_trace(qmul(qmul(qmul(v_x, v_y), qinv(v_x)), qinv(v_y))))
    return frac(term[0] * chi[1], term[1] * chi[0])


def section_first_dependence():
    stamp("first_dependence")
    coefficient = (1, 64) if SABOTAGE == "wrong_first_coefficient" else (1, 128)
    read_b2, read_b3 = flat_filling_coefficient(2), flat_filling_coefficient(3)
    read_row("leading_coefficient_b=2", (1, 128) == read_b2, show(read_b2), "1/128")
    read_row("leading_coefficient_b=3", (1, 131072) == read_b3, show(read_b3), "1/131072")
    pool = [q for q in quaternion_pool(2026, 40) if (q[1], q[2], q[3]) != (0, 0, 0)][:12]
    for sides in ((2, 2, 2, 2), (4, 2, 2, 2)):
        lat = FiniteLattice(sides, (2, 2, 2, 2))
        count = len(lat.coarse_links)
        V_a = [pool[k % 12] for k in range(count)]
        V_b = [pool[(k * 5 + 3) % 12] for k in range(count)]
        V_one = [Q_ONE] * count
        for position in (0, 1):
            carrying = {link for index, (_, fine) in enumerate(lat.coarse_links) for k, link in enumerate(fine) if k == position % len(fine)}
            touching = {p for p, word in enumerate(lat.plaquettes) if any(link in carrying for link, _ in word)}
            sums = {}
            memo_count = {}
            lists = {}
            for size in (1, 2, 3, 4):
                lists[size] = surviving_multisets(lat, size, touching)
                memo_count[size] = len(lists[size])
            for label, V in (("one", V_one), ("a", V_a), ("b", V_b)):
                values = lines_with_V(lat, V, position)
                by_size = {}
                memo = {}
                for size in (1, 2, 3, 4):
                    total = (0, 1)
                    for multiset in lists[size]:
                        term = term_for_multiset(lat, multiset, values, memo)
                        total = fadd(total, fmul(multinomial_inverse(multiset), term))
                    by_size[size] = total
                sums[label] = by_size
            independent = all(sums["a"][s] == sums["one"][s] == sums["b"][s] for s in (1, 2, 3))
            check("first_dependence_below_b^2_%s_position=%d" % ("x".join(map(str, sides)), position), independent)
            law_ab = fmul(coefficient, fsub(coarse_chi(lat, V_a), coarse_chi(lat, V_b)))
            law_a1 = fmul(coefficient, fsub(coarse_chi(lat, V_a), coarse_chi(lat, V_one)))
            read_ab = fsub(sums["a"][4], sums["b"][4])
            read_a1 = fsub(sums["a"][4], sums["one"][4])
            check("first_dependence_(%s)_position=%d" % (",".join(map(str, sides)), position), law_ab == read_ab and law_a1 == read_a1)
            say("YM4_03_FIRST_DEPENDENCE|fine=%s|coarse_links=%d|V_at_position=%d|survivors_size_1,2,3,4=%s|V_independent_below_order_4=%d|E[X^4]/4!_difference=%s|law=%s|json=0" % ("x".join(map(str, sides)), count, position, ",".join(str(memo_count[s]) for s in (1, 2, 3, 4)), independent, show(read_a1), show(law_a1)))


def section_core_count():
    """The count in Theorem 9, read by search: the fewest plaquettes with every free link of degree other than 1, covering one coarse line."""
    stamp("first_dependence_count")
    for d, side_list, bi in ((2, ((2, 2), (4, 4)), 2), (3, ((2, 2, 2), (4, 4, 4), (8, 8, 8)), 2), (4, ((2, 2, 2, 2), (4, 4, 4, 4)), 2), (2, ((3, 3), (6, 6)), 3), (3, ((3, 3, 3), (6, 6, 6)), 3), (4, ((6, 6, 6, 6),), 3)):
        for sides in side_list:
            found = None
            limit = bi * bi
            for budget in range(1, limit + 1):
                if search_cover(sides, d, bi, budget):
                    found = budget
                    break
            check("core_count_d=%d_b=%d_%s" % (d, bi, "x".join(map(str, sides))), found == limit)
            say("YM4_03_CORE_COUNT|d=%d|b=%d|fine=%s|fewest_plaquettes_covering_a_line=%s|law=%d|json=0" % (d, bi, "x".join(map(str, sides)), found, limit))


def plaquette_links(x, mu, nu, sides):
    return ((x, mu), (add(x, mu, sides), nu), (add(x, nu, sides), mu), (x, nu))


def plaquettes_at(link, sides, d):
    x, mu = link
    out = []
    for nu in range(d):
        if nu == mu:
            continue
        lo, hi = (mu, nu) if mu < nu else (nu, mu)
        out.append((x, lo, hi))
        y = add(x, nu, sides, -1)
        out.append((y, lo, hi))
    return out


def search_cover(sides, d, b, budget):
    origin = (0,) * d
    on_line = set()
    for mu in range(d):
        for x in sites_of(tuple(side // b for side in sides)):
            start = tuple(c * b for c in x)
            y = start
            for _ in range(b):
                on_line.add((y, mu))
                y = add(y, mu, sides)
    target = []
    y = origin
    for _ in range(b):
        target.append((y, 0))
        y = add(y, 0, sides)

    def degree_map(chosen):
        degree = {}
        for key in chosen:
            for link in set(plaquette_links(key[0], key[1], key[2], sides)):
                degree[link] = degree.get(link, 0) + 1
        return degree

    seen = set()

    def walk(chosen):
        key = frozenset(chosen)
        if key in seen:
            return False
        seen.add(key)
        degree = degree_map(chosen)
        missing = [link for link in target if degree.get(link, 0) == 0]
        pending = sorted(link for link, count in degree.items() if count == 1 and link not in on_line)
        if not missing and not pending:
            return True
        if len(chosen) >= budget:
            return False
        if len(chosen) + (len(pending) + 3) // 4 + len(missing) > budget and not pending:
            return False
        work = pending[0] if pending else missing[0]
        for option in plaquettes_at(work, sides, d):
            if option not in chosen:
                if walk(chosen | {option}):
                    return True
        return False

    return walk(frozenset())


def section_certified():
    stamp("certified_truncation")
    # beta = 10^-12, N_p = 96, b = 2: 2 (beta N_p)^5 exp(beta N_p)/5!, with exp(x) <= 1 + 2x for 0 <= x <= 1.
    beta = (1, ipow(10, 12))
    x = fmul(beta, (96, 1))
    bound = fmul(fmul((2, 120), (ipow(x[0], 5), ipow(x[1], 5))), fadd((1, 1), fmul((2, 1), x)))
    below = bound[0] * ipow(10, 52) < 2 * bound[1]
    read_row("certified_bound_below_2e-52", below, "%d_e-54" % (bound[0] * ipow(10, 54) // bound[1]), "below_2e-52")
    leading = fmul((ipow(beta[0], 4), ipow(beta[1], 4)), (1, 128))
    lat = FiniteLattice((2, 2, 2, 2), (2, 2, 2, 2))
    check("certified_block_plaquettes", len(lat.plaquettes) == 96 and len(lat.coarse_plaquettes) == 6)
    # The best rational configuration read: four directions near the tetrahedron, pure unit quaternions, against V = 1.
    directions = [(1, 2, 2, 3), (-2, -1, 2, 3), (2, -2, 1, 3), (-1, 2, -2, 3)]
    best = None
    pool = []
    for a, b, c, den in ((1, 2, 2, 3), (2, 1, 2, 3), (2, 2, 1, 3), (1, 4, 8, 9), (4, 1, 8, 9), (8, 4, 1, 9), (4, 8, 1, 9), (8, 1, 4, 9), (1, 8, 4, 9), (3, 4, 12, 13), (12, 3, 4, 13), (4, 12, 3, 13), (2, 3, 6, 7), (3, 6, 2, 7), (6, 2, 3, 7), (6, 3, 2, 7), (2, 6, 3, 7), (3, 2, 6, 7)):
        for sa, sb, sc in itertools.product((1, -1), repeat=3):
            pool.append(rational_unit_direction(sa * a, sb * b, sc * c, den))
    # The frame bound fixes the limit, 64/3; search near it greedily over the rational directions, one direction at a time.
    current = [rational_unit_direction(*directions[k]) for k in range(4)]
    identity_chi = coarse_chi(lat, [Q_ONE] * 4)

    def value_of(config):
        return fsub(identity_chi, coarse_chi(lat, config))

    best = value_of(current)
    improved = True
    while improved:
        improved = False
        for k in range(4):
            for q in pool:
                trial = list(current)
                trial[k] = q
                got = value_of(trial)
                if got[0] * best[1] > best[0] * got[1]:
                    best = got
                    current = trial
                    improved = True
    limit = (64, 3)
    check("certified_range_below_frame_limit", best[0] * limit[1] <= limit[0] * best[1])
    range_read = fmul(leading, best)
    range_limit = fmul(leading, limit)
    ok_row = range_read[0] * ipow(10, 49) >= 18 * range_read[1] // 10
    read_row("certified_range_at_least_1.8e-49", ok_row, "%d_e-52_at_rational_V_with_limit_%d_e-52" % (range_read[0] * ipow(10, 52) // range_read[1], range_limit[0] * ipow(10, 52) // range_limit[1]), "at_least_1.8e-49")
    check("certified_resolves_the_leading_term", bound[0] * range_read[1] < range_read[0] * bound[1])
    say("YM4_03_CERTIFIED_4D|block=(Z/2)^4_to_(Z/1)^4|beta=10^-12|N_p=96|bound_e-54=%d|leading_coefficient_e-54=%d|range_at_rational_V_e-54=%d|range_limit=(beta^4/128)(64/3)_e-54=%d|json=0" % (bound[0] * ipow(10, 54) // bound[1], leading[0] * ipow(10, 54) // leading[1], range_read[0] * ipow(10, 54) // range_read[1], range_limit[0] * ipow(10, 54) // range_limit[1]))


# ---- Transfer operators on small spatial lattices, on gauge orbits.


class Transfer:
    def __init__(self, name, sides, weight):
        self.g = GROUPS[name]
        self.name = name
        self.sides = sides
        self.d = len(sides)
        g = self.g
        n = g.n
        self.sites = sites_of(sides)
        self.links = {}
        for x in self.sites:
            for mu in range(self.d):
                self.links[(x, mu)] = len(self.links)
        count = len(self.links)
        self.count = count
        self.words = []
        for x in self.sites:
            for mu in range(self.d):
                for nu in range(mu + 1, self.d):
                    self.words.append(((self.links[(x, mu)], 1), (self.links[(add(x, mu, sides), nu)], 1), (self.links[(add(x, nu, sides), mu)], -1), (self.links[(x, nu)], -1)))
        configs = list(itertools.product(range(n), repeat=count))
        self.configs = configs
        index = {c: i for i, c in enumerate(configs)}
        self.index = index
        parent = list(range(len(configs)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        site_generators = [(x, h) for x in self.sites for h in range(n)]
        endpoints = [(x, mu, add(x, mu, sides)) for (x, mu) in self.links]
        link_list = list(self.links.items())
        for c_index, c in enumerate(configs):
            for x, h in site_generators:
                moved = list(c)
                for ((y, mu), link) in link_list:
                    z = add(y, mu, sides)
                    value = moved[link]
                    if y == x:
                        value = g.table[h][value]
                    if z == x:
                        value = g.table[value][g.inverse[h]]
                    moved[link] = value
                other = index[tuple(moved)]
                a, b = find(c_index), find(other)
                if a != b:
                    parent[a] = b
        orbits = {}
        for i in range(len(configs)):
            orbits.setdefault(find(i), []).append(i)
        self.orbits = list(orbits.values())
        self.orbit_of = {}
        for k, members in enumerate(self.orbits):
            for i in members:
                self.orbit_of[i] = k
        self.m = len(self.orbits)
        self.sizes = [len(o) for o in self.orbits]
        self.reps = [configs[o[0]] for o in self.orbits]
        ww = [[weight[g.table[a][g.inverse[b]]] for b in range(n)] for a in range(n)]
        self.kernel = []
        for rep in self.reps:
            row = [0] * self.m
            for i, c in enumerate(configs):
                product = 1
                for u, v in zip(rep, c):
                    product *= ww[u][v]
                row[self.orbit_of[i]] += product
            self.kernel.append(row)
        self.diag = []
        for rep in self.reps:
            product = 1
            for word in self.words:
                out = g.identity
                for link, sign in word:
                    u = rep[link]
                    out = g.table[out][u if sign > 0 else g.inverse[u]]
                product *= weight[out]
            self.diag.append(product)

    def apply_s(self, vector):
        """S = B A, on orbit functions, with the scale n^count held out of B."""
        weighted = [d * v for d, v in zip(self.diag, vector)]
        return [sum(r * w for r, w in zip(row, weighted)) for row in self.kernel]


def rational_basis_add(basis, pivots, vector):
    """Row reduce with integers. Returns True if the vector raised the rank."""
    v = list(vector)
    for row, pivot in zip(basis, pivots):
        if v[pivot]:
            a, b = row[pivot], v[pivot]
            g = math.gcd(a, b)
            mult_v, mult_r = a // g, b // g
            v = [mult_v * x - mult_r * y for x, y in zip(v, row)]
    pivot = next((i for i, x in enumerate(v) if x), None)
    if pivot is None:
        return False
    g = 0
    for x in v:
        g = math.gcd(g, x)
    if g > 1:
        v = [x // g for x in v]
    basis.append(v)
    pivots.append(pivot)
    return True


def inertia_positive(rows):
    """The number of positive eigenvalues of an integer symmetric matrix, by fraction-free elimination with symmetric pivoting of 2 x 2 blocks by sum."""
    m = [list(r) for r in rows]
    n = len(m)
    prev, positive = 1, 0
    negative = 0
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
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            for r in range(n):
                m[r][k], m[r][pivot] = m[r][pivot], m[r][k]
        p = m[k][k]
        if (p > 0) == (prev > 0):
            positive += 1
        else:
            negative += 1
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (p * m[i][j] - m[i][k] * m[k][j]) // prev
        prev = p
    return positive, negative, n


def section_coarse_space():
    stamp("coarse_space")
    # Spatial lattices small enough for exact work, and the coarse functions on them.
    for name, sides, b_space, b_time in (("Z2", (2, 2), (2, 2), 2), ("Z2", (2, 1), (2, 1), 2), ("S3", (2, 1), (2, 1), 2), ("Q8", (2, 1), (2, 1), 2), ("Z3", (2, 1), (2, 1), 3)):
        w = weight_three_plus(name)
        if name == "Z2":
            w = [3, 1]
        model = Transfer(name, sides, w)
        g = model.g
        # The transfer model against the lattice's own plaquette words, and its time kernel's symmetry in the orbit measure.
        word_lattice = FiniteLattice(sides, b_space)
        same_plaquettes = True
        for rep, value in zip(model.reps, model.diag):
            product = 1
            for word in word_lattice.plaquettes:
                product *= w[word_lattice.word_value(word, rep, g)]
            same_plaquettes = same_plaquettes and product == value
        check("transfer_plaquettes_match_lattice_%s_%s" % (name, "x".join(map(str, sides))), same_plaquettes)
        check("transfer_kernel_symmetric_%s_%s" % (name, "x".join(map(str, sides))), all(model.sizes[a] * model.kernel[a][c] == model.sizes[c] * model.kernel[c][a] for a in range(model.m) for c in range(a)))
        coarse_sides = tuple(s // bi for s, bi in zip(sides, b_space))
        coarse_keys = []
        for x_c in sites_of(coarse_sides):
            for mu in range(len(sides)):
                fine = [model.links[wrap(link, sides)] for link in fine_links_of_coarse(x_c, mu, b_space)]
                coarse_keys.append(fine)
        # The coarse value of each orbit under coarse gauge: orbits of the coarse function are read on all members.
        coarse_value_of_config = []
        for c in model.configs:
            values = []
            for fine in coarse_keys:
                value = g.identity
                for link in fine:
                    value = g.table[value][c[link]]
                values.append(value)
            coarse_value_of_config.append(tuple(values))
        # A gauge-invariant coarse function: the partition of orbits by coarse classes, built from the coarse values on orbit members.
        signature = []
        for members in model.orbits:
            signature.append(frozenset(coarse_value_of_config[i] for i in members))
        labels = {}
        for k, s in enumerate(signature):
            labels.setdefault(s, []).append(k)
        indicators = [[1 if k in set(members) else 0 for k in range(model.m)] for members in labels.values()]
        # The smallest subspace holding 1 and closed under S^b and the coarse multiplications.
        basis, pivots = [], []
        work = [[1] * model.m]
        kept = []
        while work:
            vector = work.pop()
            if rational_basis_add(basis, pivots, vector):
                kept.append(vector)
                moved = vector
                for _ in range(b_time):
                    moved = model.apply_s(moved)
                g0 = 0
                for x in moved:
                    g0 = math.gcd(g0, x)
                if g0 > 1:
                    moved = [x // g0 for x in moved]
                work.append(moved)
                for indicator in indicators:
                    product = [a * c for a, c in zip(indicator, vector)]
                    if any(product):
                        work.append(product)
        rank = len(kept)
        # Closure, read again from the kept basis.
        closed = True
        probe_basis, probe_pivots = [list(r) for r in basis], list(pivots)
        for vector in kept:
            moved = vector
            for _ in range(b_time):
                moved = model.apply_s(moved)
            if rational_basis_add(probe_basis, probe_pivots, moved):
                closed = False
        check("coarse_space_invariant_%s_%s" % (name, "x".join(map(str, sides))), closed)
        # The pencil K - t G on W and on the whole orbit space. <A^{1/2}u, T^k A^{1/2}v> = u^t Delta A (B A)^k v, with B's scale n^count per step.
        n = g.n
        scale = ipow(n, model.count)
        delta_a = [s * d for s, d in zip(model.sizes, model.diag)]

        def pencil(vectors, steps):
            images = []
            for v in vectors:
                moved = v
                for _ in range(steps):
                    moved = model.apply_s(moved)
                images.append(moved)
            size = len(vectors)
            big_g = [[sum(da * a * c for da, a, c in zip(delta_a, vectors[i], vectors[j])) for j in range(size)] for i in range(size)]
            big_k = [[sum(da * a * c for da, a, c in zip(delta_a, vectors[i], images[j])) for j in range(size)] for i in range(size)]
            return big_g, big_k

        unit_vectors = [[1 if i == k else 0 for i in range(model.m)] for k in range(model.m)]
        small_enough = model.m <= 60
        part_g, part_k = pencil(kept, b_time)
        whole_g, whole_k = pencil(unit_vectors, b_time) if small_enough else (None, None)

        def above(big_g, big_k, t_n, t_d):
            size = len(big_g)
            rows = [[t_d * big_k[i][j] - t_n * big_g[i][j] for j in range(size)] for i in range(size)]
            return inertia_positive(rows)[0]

        # The top eigenvalue by Collatz-Wielandt: for a positive vector v, the smallest and largest of (S^b v)_i / v_i bracket it, and the vector lies in W.
        vector = [1] * model.m
        for _ in range(24):
            moved = vector
            for _ in range(b_time):
                moved = model.apply_s(moved)
            g0 = 0
            for x in moved:
                g0 = math.gcd(g0, x)
            vector = [x // g0 for x in moved]
            top_bits = max(x.bit_length() for x in vector)
            if top_bits > 2048:
                vector = [(x >> (top_bits - 2048)) + 1 for x in vector]
        moved = vector
        for _ in range(b_time):
            moved = model.apply_s(moved)
        ratios = [frac(a, c) for a, c in zip(moved, vector)]
        lo_n, lo_d = min(ratios, key=lambda r: (r[0] << 2400) // r[1])
        hi_n, hi_d = max(ratios, key=lambda r: (r[0] << 2400) // r[1])
        # In units where T^b has the scale of the pencil, the bracket divides by scale^b; the thresholds are lo and hi just outside it.
        # Rounded outward at 64 bits of the bracket's own size, so the pencil's entries stay small.
        shift = max(0, lo_n.bit_length() - lo_d.bit_length() - 64)
        low = (lo_n * 999999 // (lo_d * 1000000)) >> shift
        high = ((hi_n * 1000001 // (hi_d * 1000000)) >> shift) + 1
        lo_n, lo_d, hi_n, hi_d = low << shift, 1, high << shift, 1
        if small_enough:
            top_equal = above(part_g, part_k, lo_n, lo_d) >= 1 and above(part_g, part_k, hi_n, hi_d) == 0 and above(whole_g, whole_k, lo_n, lo_d) >= 1 and above(whole_g, whole_k, hi_n, hi_d) == 0
        else:
            # The whole space's top lies in the bracket by Collatz-Wielandt on the positive matrix S^b, and the pencil on W reads W's top in the same bracket.
            top_equal = above(part_g, part_k, lo_n, lo_d) >= 1 and above(part_g, part_k, hi_n, hi_d) == 0
        check("coarse_space_top_equal_%s_%s" % (name, "x".join(map(str, sides))), top_equal)
        # The next value: at thresholds running down from the top, W never holds more eigenvalues above t than the whole space.
        counts_ok = True
        visible = []
        for k in (1, 3):
            if not small_enough:
                break
            t_n, t_d = lo_n * ipow(3, k), lo_d * ipow(4, k)
            a_part, a_whole = above(part_g, part_k, t_n, t_d), above(whole_g, whole_k, t_n, t_d)
            counts_ok = counts_ok and a_part <= a_whole
            visible.append("%d/%d" % (a_part, a_whole))
        check("coarse_space_counts_%s_%s" % (name, "x".join(map(str, sides))), counts_ok)
        second_part = second_whole = "not_read"
        if small_enough and rank >= 2:
            def second_value(big_g, big_k):
                low, high = 0, lo_n
                for _ in range(48):
                    middle = (low + high) // 2
                    if above(big_g, big_k, middle, 1) >= 2:
                        low = middle
                    else:
                        high = middle
                return low

            value_part = second_value(part_g, part_k)
            value_whole = second_value(whole_g, whole_k)
            # The note's table reads the second value on W equal to the whole space's: within the bisection's step, on each case read.
            check("coarse_space_second_value_%s_%s" % (name, "x".join(map(str, sides))), abs(value_part - value_whole) <= (lo_n >> 46))
            second_part = "%d" % (value_part * 1000000 // lo_n)
            second_whole = "%d" % (value_whole * 1000000 // lo_n)
        say("YM4_03_COARSE_SPACE|group=%s|spatial=%s|b_space=%s|b_time=%d|orbits=%d|coarse_functions=%d|dim_W=%d|closed=%d|top_equal=%d|above_t_W/whole_at_(3/4)^k=%s|second_over_top_ppm_on_W=%s|second_over_top_ppm_on_the_whole=%s|json=0" % (name, "x".join(map(str, sides)), "x".join(map(str, b_space)), b_time, model.m, len(indicators), rank, closed, top_equal, ",".join(visible), second_part, second_whole))
        # Reflection positivity of coarse slice observables through a link plane: Tr(M_i T^(2b+1) M_j T^(2b+1)) has no negative eigenvalue when T is positive. At an even power the Gram is positive for every symmetric T.
        if name in ("Z3", "S3", "Q8") and model.m <= 200:
            two = 2 * b_time + 1
            images = []
            for indicator in indicators:
                moved = indicator
                for _ in range(two):
                    moved = model.apply_s(moved)
                images.append(moved)
            full_two = []
            for k in range(model.m):
                moved = unit_vectors[k]
                for _ in range(two):
                    moved = model.apply_s(moved)
                full_two.append(moved)
            size = len(indicators)
            gram = [[0] * size for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    total = 0
                    # Tr(M_i S^(2b) M_j S^(2b)) over the orbit basis.
                    for a in range(model.m):
                        if not indicators[i][a]:
                            continue
                        for c in range(model.m):
                            if indicators[j][c]:
                                total += full_two[c][a] * full_two[a][c]
                    gram[i][j] = total
            symmetric = all(gram[i][j] == gram[j][i] for i in range(size) for j in range(i))
            pos, neg, rank_g = inertia_positive(gram)
            check("coarse_gram_positive_%s" % name, symmetric and neg == 0)
            say("YM4_03_COARSE_GRAM|group=%s|spatial=%s|observables=%d|positive=%d|negative=%d|rank=%d|json=0" % (name, "x".join(map(str, sides)), size, pos, neg, rank_g))


def section_circle():
    stamp("circle_spectrum")
    for name in ("Z2", "Z3", "S3", "Q8", "2T"):
        g = GROUPS[name]
        n = g.n
        w = weight_three_plus(name)
        for b, coarse_len in ((2, 1), (3, 1), (2, 2)):
            fine_len = b * coarse_len
            if ipow(n, fine_len) > 15000:
                continue
            power = convolution_power(g, w, b * b)
            classes = g.classes

            def holonomy(config):
                value = g.identity
                for u in config:
                    value = g.table[value][u]
                return value

            def matrix(length, weight):
                configs = list(itertools.product(range(n), repeat=length))
                size = len(classes)
                table = [[0] * size for _ in range(size)]
                ww = [[weight[g.table[a][g.inverse[y]]] for y in range(n)] for a in range(n)]
                for k, members in enumerate(classes):
                    rep = (members[0],) + (g.identity,) * (length - 1)
                    for c in configs:
                        product = 1
                        for u, v in zip(rep, c):
                            product *= ww[u][v]
                        table[k][g.class_of[holonomy(c)]] += product
                return table

            fine = matrix(fine_len, w)
            coarse = matrix(coarse_len, power)
            # T^b on class functions against T_c, with scales: fine n^(fine_len) per step, coarse n^coarse_len and power's n^(b^2-1) per link.
            size = len(classes)
            product = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
            for _ in range(b):
                product = [[sum(product[i][k] * fine[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
            scale_fine = ipow(n, fine_len * b)
            scale_coarse = ipow(n, coarse_len) * ipow(n, (b * b - 1) * coarse_len)
            equal = all(product[i][j] * scale_coarse == coarse[i][j] * scale_fine for i in range(size) for j in range(size))
            check("circle_spectrum_%s_b=%d_L'=%d" % (name, b, coarse_len), equal)
            say("YM4_03_CIRCLE|group=%s|b=%d|coarse_length=%d|classes=%d|T^b_equals_coarse_T_as_matrices=%d|json=0" % (name, b, coarse_len, size, equal))


# ---- SU(2) in two dimensions: integer brackets on the modified Bessel functions.

BITS = 640


def bessel_bracket(n, beta):
    """(lo, hi) of I_n(beta) at scale 2^BITS, beta a positive integer. Positive series, floored and raised."""
    numerator = ipow(beta, n) << BITS
    denominator = ipow(2, n)
    for k in range(2, n + 1):
        denominator *= k
    lo_term = numerator // denominator
    hi_term = lo_term + 1
    lo, hi = 0, 0
    k = 0
    square = beta * beta
    while True:
        lo += lo_term
        hi += hi_term
        d = 4 * (k + 1) * (n + k + 1)
        lo_term = (lo_term * square) // d
        hi_term = (hi_term * square) // d + 1
        k += 1
        if d >= 2 * square and hi_term < (1 << 8):
            # The rest is below a geometric series of ratio 1/2 from here.
            hi += 2 * hi_term
            break
    return lo, hi


def scaled_ratio_bracket(lo_a, hi_a, lo_b, hi_b):
    return (lo_a << BITS) // hi_b, ((hi_a << BITS) // lo_b) + 1


def power_bracket(lo, hi, m):
    out_lo, out_hi = 1 << BITS, 1 << BITS
    base_lo, base_hi = lo, hi
    e = m
    while e:
        if e & 1:
            out_lo = (out_lo * base_lo) >> BITS
            out_hi = ((out_hi * base_hi) >> BITS) + 1
        base_lo = (base_lo * base_lo) >> BITS
        base_hi = ((base_hi * base_hi) >> BITS) + 1
        e >>= 1
    return out_lo, out_hi


def ceiling_sqrt(x):
    r = math.isqrt(x)
    return r if r * r == x else r + 1


def section_su2_two_dimensions():
    stamp("su2_two_dimensions")
    top = 16
    for beta in (1, 4, 16, 64, 256, 1024, 4096):
        b = ceiling_sqrt(4 * beta)
        m = b * b
        brackets = {n: bessel_bracket(n, beta) for n in range(1, top + 2)}
        t = {}
        for n in range(1, top + 2):
            t[n] = scaled_ratio_bracket(brackets[n][0], brackets[n][1], brackets[1][0], brackets[1][1])
        delta_lo, delta_hi = 0, 0
        for n in range(2, top + 1):
            lo, hi = power_bracket(t[n][0], t[n][1], m)
            delta_lo += n * n * lo
            delta_hi += n * n * hi
        # The rest: t_n <= t_N q^(n-N) with q = t_(N+1)/t_N, since I_(n+1)/I_n falls with n; (N+k)^2 <= (N+1)^2 k^2 and Sum k^2 r^k <= 12 r for r <= 1/2.
        q_hi = ((t[top + 1][1] << BITS) // t[top][0]) + 1
        r_hi = power_bracket(q_hi, q_hi, m)[1]
        last_hi = power_bracket(t[top][0], t[top][1], m)[1]
        check("su2_tail_ratio_small_beta=%d" % beta, 2 * r_hi <= (1 << BITS))
        delta_hi += ((top + 1) * (top + 1) * 12 * ((last_hi * r_hi) >> BITS)) + 1
        check("su2_two_dimensions_uniform_delta_beta=%d" % beta, 8 * delta_hi < (1 << BITS))
        t2_lo, t2_hi = power_bracket(t[2][0], t[2][1], m)
        # t <= 4 - sqrt 15 exactly when (4 - t)^2 >= 15, for t < 4.
        four = 4 << BITS
        check("su2_two_dimensions_uniform_t2_beta=%d" % beta, (four - t2_hi) * (four - t2_hi) >= 15 << (2 * BITS))
        # Amos on the grid: q^2 beta + 2 nu q <= beta.
        amos = True
        for nu in range(1, 9):
            q = ((brackets[nu + 1][1] << BITS) // brackets[nu][0]) + 1
            amos = amos and (((q * q) >> BITS) * beta + 2 * nu * q) <= beta << BITS
        check("amos_on_the_grid_beta=%d" % beta, amos)
        # Physical length b a g = 2 b / sqrt(beta), in millionths, floored.
        length = (2 * b * 1000000 * 1000000) // math.isqrt(beta * 1000000 * 1000000)
        say("YM4_03_SU2_D2|beta=%d|b=%d|delta_ppm_lo=%d|delta_ppm_hi=%d|t2^(b^2)_ppm_lo=%d|t2^(b^2)_ppm_hi=%d|b_a_g_ppm=%d|bound_m_over_g_ppm=%d|json=0" % (beta, b, delta_lo * 1000000 >> BITS, (delta_hi * 1000000 >> BITS) + 1, t2_lo * 1000000 >> BITS, (t2_hi * 1000000 >> BITS) + 1, length, (2063437 * 1000000) // length))
        if beta == 1:
            read_row("su2_delta_at_beta=1_near_0.0133", 13000 <= delta_lo * 1000000 >> BITS and (delta_hi * 1000000 >> BITS) <= 13700, "%d_ppm" % (delta_hi * 1000000 >> BITS), "near_13300_ppm")
        if beta == 4096:
            read_row("su2_delta_as_beta_grows_near_0.0099", 9000 <= delta_lo * 1000000 >> BITS and (delta_hi * 1000000 >> BITS) <= 10800, "%d_ppm" % (delta_hi * 1000000 >> BITS), "near_9900_ppm")
    # The exact gap on the shortest circle against the bound: log(1/t2^L)/... reads at L = b.
    # log(1/(4 - sqrt 15)) = log(4 + sqrt 15), read between 2.063437 and 2.063438 by the exponential's bracket.
    four_plus_root = (4 << BITS) + math.isqrt(15 << (2 * BITS))
    constant_ok = exp_bracket(2063437, 1000000)[1] <= four_plus_root and four_plus_root + 1 <= exp_bracket(2063438, 1000000)[0]
    read_row("su2_m_over_g_bound", constant_ok, "2063437/4_ppm_of_g=515859", "0.516")
    # The exact m/g at l = 4/g is -beta log t_2. At the last beta of the grid, read between 149/100 and 151/100.
    t2_power = power_bracket(t[2][0], t[2][1], beta)
    exact_ok = exp_bracket(-151, 100)[1] <= t2_power[0] and t2_power[1] <= exp_bracket(-149, 100)[0]
    read_row("su2_exact_m_over_g_at_l=4/g", exact_ok, "3*4/8=3/2", "1.5")
    # The truncation and the expansion itself: at m = 1 the series against e^(beta cos theta)/((2/beta) I_1), at rational cos theta.
    for beta in (1, 4):
        i1 = bessel_bracket(1, beta)
        cosines = [(0, 1), (3, 5), (-4, 5), (1, 1), (-1, 1)]
        ok = True
        for cn, cd in cosines:
            # e^(beta c) by its series, in integers, bracketed; c may be negative, so split even and odd parts by sign.
            lo_exp, hi_exp = exp_bracket(beta * cn, cd)
            direct_lo = (lo_exp * beta << BITS) // (2 * i1[1])
            direct_hi = ((hi_exp * beta << BITS) // (2 * i1[0])) + 1
            series_lo, series_hi = 0, 0
            for n in range(1, 40):
                t_lo, t_hi = scaled_ratio_bracket(*bessel_bracket(n, beta), i1[0], i1[1])
                chi_n, chi_d = chebyshev_u(n - 1, cn, cd)
                if chi_n >= 0:
                    series_lo += n * t_lo * chi_n // chi_d
                    series_hi += n * t_hi * chi_n // chi_d + 1
                else:
                    series_lo += n * t_hi * chi_n // chi_d
                    series_hi += n * t_lo * chi_n // chi_d + 1
            tail = (1 << (BITS - 60))
            ok = ok and series_lo <= direct_hi + tail and direct_lo <= series_hi + tail
        check("su2_character_expansion_beta=%d" % beta, ok)
        # Sum n^2 t_n^2 c_1^2 = integral of w^2: Sum n^2 (2/beta)^2 I_n(beta)^2 = (1/beta) I_1(2 beta).
        lo_sum, hi_sum = 0, 0
        for n in range(1, 60):
            a = bessel_bracket(n, beta)
            lo_sum += n * n * ((a[0] * a[0]) >> BITS)
            hi_sum += n * n * (((a[1] * a[1]) >> BITS) + 1)
        i_double = bessel_bracket(1, 2 * beta)
        # 4/beta^2 Sum = (1/beta) I_1(2 beta), so 4 Sum = beta I_1(2 beta). The sum stops at n = 59, and its tail at beta <= 4 is below 2^-300 of the unit.
        tail_room = 1 << (BITS - 300)
        check("su2_convolution_sum_rule_beta=%d" % beta, 4 * lo_sum <= beta * i_double[1] + (1 << 40) and beta * i_double[0] <= 4 * hi_sum + tail_room)
        for m, top_n in ((4, 3), (16, 3)):
            tail_lo = 0
            for n in range(top_n + 1, top + 1):
                t_lo, t_hi = scaled_ratio_bracket(*bessel_bracket(n, beta), i1[0], i1[1])
                tail_lo += n * n * power_bracket(t_lo, t_hi, m)[1]
            say("YM4_03_SU2_TRUNCATION|beta=%d|m=%d|cut_at_n=%d|sup_norm_error_e-12_at_most=%d|json=0" % (beta, m, top_n, (tail_lo * 1000000000000 >> BITS) + 1))
            # The omitted terms at rational angles stay inside the bound, at each angle read.
            inside = True
            for cn, cd in ((1, 1), (-1, 1), (0, 1), (3, 5), (-4, 5)):
                omitted = 0
                for n in range(top_n + 1, top + 1):
                    t_lo, t_hi = scaled_ratio_bracket(*bessel_bracket(n, beta), i1[0], i1[1])
                    chi_n, chi_d = chebyshev_u(n - 1, cn, cd)
                    omitted += n * power_bracket(t_lo, t_hi, m)[1] * abs(chi_n) // chi_d
                inside = inside and omitted <= tail_lo + 1
            check("su2_character_truncation_beta=%d_m=%d" % (beta, m), inside)
            if beta == 1 and m == 4:
                # GPT-6's tile in PR 28: W = Sum (n+1) (f_n/f_0)^4 chi_n, cut at its n <= 2, with error at most 25/671741424 on beta <= 1.
                read_row("pr28_tile_bound_stands_above_this_read_at_beta=1", tail_lo * 671741424 <= 25 << BITS, "%d_e-12" % ((tail_lo * 1000000000000 >> BITS) + 1), "at_most_25/671741424")


def exp_bracket(numerator, denominator):
    """(lo, hi) of exp(numerator/denominator) at scale 2^BITS, by the series, exact to rounding."""
    negative = numerator < 0
    a = abs(numerator)
    lo = hi = 1 << BITS
    term_lo = term_hi = 1 << BITS
    k = 1
    while True:
        term_lo = (term_lo * a) // (denominator * k)
        term_hi = ((term_hi * a) // (denominator * k)) + 1
        lo += term_lo
        hi += term_hi
        k += 1
        if k > 4 * a // denominator + 8 and term_hi < 16:
            hi += 2 * term_hi
            break
    if not negative:
        return lo, hi
    one = 1 << (2 * BITS)
    return one // hi, one // lo + 1


def chebyshev_u(k, cn, cd):
    """U_k(c) with c = cn/cd, as (numerator, denominator): chi_(k+1) at the angle with cos theta = c."""
    u0 = (1, 1)
    if k == 0:
        return u0
    u1 = frac(2 * cn, cd)
    for _ in range(k - 1):
        two_c = frac(2 * cn, cd)
        u0, u1 = u1, fsub(fmul(two_c, u1), u0)
    return u1


# ---- Z2 surfaces with a prescribed boundary, by enumeration on a large lattice.


def z2_boundary(plaquettes_set, sides):
    odd = set()
    for key in plaquettes_set:
        for link in plaquette_links(key[0], key[1], key[2], sides):
            odd ^= {link}
    return odd


def coarse_filling(start, mu, nu, sides, b):
    out = set()
    for s in range(b):
        for r in range(b):
            x = list(start)
            x[mu] = (x[mu] + s) % sides[mu]
            x[nu] = (x[nu] + r) % sides[nu]
            lo, hi = (mu, nu) if mu < nu else (nu, mu)
            out.add((tuple(x), lo, hi))
    return out


def count_surfaces(target, sides, d, budget):
    """Every plaquette set of size at most budget with boundary exactly target, each connected component touching target; the number per size."""
    counts = {}
    seen = set()

    def walk(chosen, odd):
        key = frozenset(chosen)
        if key in seen:
            return
        seen.add(key)
        if not odd:
            counts[len(chosen)] = counts.get(len(chosen), 0) + 1
            return
        remaining = budget - len(chosen)
        if remaining <= 0 or len(odd) > 4 * remaining:
            return
        work = min(odd)
        for option in plaquettes_at(work, sides, d):
            if option in chosen:
                continue
            links = plaquette_links(option[0], option[1], option[2], sides)
            moved = set(odd)
            for link in links:
                moved ^= {link}
            walk(chosen | {option}, moved)

    walk(frozenset(), set(target))
    return counts


def section_z2_surfaces():
    stamp("z2_surfaces")
    b = 2
    for d in (3, 4):
        sides = (8,) * d
        origin = (0,) * d
        P = coarse_filling(origin, 0, 1, sides, b)
        Q = coarse_filling(origin, 0, 2, sides, b)
        dP, dQ = z2_boundary(P, sides), z2_boundary(Q, sides)
        target = dP ^ dQ
        counts = count_surfaces(target, sides, d, 10)
        single = count_surfaces(dP, sides, d, 8)
        coefficient_8 = counts.get(8, 0)
        coefficient_10 = counts.get(10, 0)
        below = sum(v for k, v in counts.items() if k < 8)
        check("z2_perpendicular_leading_d=%d" % d, coefficient_8 == 1 and below == 0 and single.get(4, 0) == 1)
        read_row("z2_nonlocal_perpendicular_d=%d" % d, coefficient_10 == 2, "%d_at_u^10" % coefficient_10, "2_at_u^10")
        check("z2_perpendicular_three_at_u^10_d=%d" % d, coefficient_10 == 3)
        say("YM4_03_Z2_PERPENDICULAR|d=%d|fine=8^%d|surfaces_by_size=%s|single_filling_by_size=%s|json=0" % (d, d, ",".join("%d:%d" % (k, counts[k]) for k in sorted(counts)), ",".join("%d:%d" % (k, single[k]) for k in sorted(single))))
    d = 3
    sides = (12, 12, 12)
    origin = (0, 0, 0)
    P = coarse_filling(origin, 0, 1, sides, b)
    Q = coarse_filling((0, 0, 2), 0, 1, sides, b)
    dP, dQ = z2_boundary(P, sides), z2_boundary(Q, sides)
    counts = count_surfaces(dP ^ dQ, sides, d, 12)
    single = count_surfaces(dP, sides, d, 8)
    a4, a8 = single.get(4, 0), single.get(8, 0)
    # log coefficient of W_P W_Q through u^12: A(PQ) - A(P) A(Q), with both normalized by the vacuum sum, which starts at u^6 and enters only from u^14 here.
    term_8 = counts.get(8, 0) - a4 * a4
    term_12 = counts.get(12, 0) - 2 * a4 * a8
    term_10 = counts.get(10, 0)
    read_row("z2_nonlocal_parallel", term_8 == 0 and term_10 == 0 and term_12 == 0, "u^8:%d,u^10:%d,u^12:%d" % (term_8, term_10, term_12), "0,0,0")
    check("z2_parallel_vanishes_through_u^12", term_8 == 0 and term_10 == 0 and term_12 == 0)
    say("YM4_03_Z2_PARALLEL|d=3|fine=12^3|surfaces_by_size=%s|single_filling_by_size=%s|json=0" % (",".join("%d:%d" % (k, counts[k]) for k in sorted(counts)), ",".join("%d:%d" % (k, single[k]) for k in sorted(single))))


# ---- Electric flux: the center twist, its sectors, and what coarse observables reach in them.

CENTER = {"Z2": 1, "Q8": 1}


def fundamental_character(name):
    if name == "Z2":
        return [1, -1]
    if name == "Q8":
        return [e[0] for e in Q8_ELEMENTS]
    raise ValueError(name)


def twist_perm(model, mu, s):
    """The action of Z_mu on orbits: z times U_mu on the plane x_mu = s. The check that an orbit goes to one orbit is in the caller."""
    g = model.g
    z = CENTER[model.name]
    links = [link for (x, nu), link in model.links.items() if nu == mu and (x[mu] == s or SABOTAGE == "twist_every_link")]
    perm = []
    single = True
    for members in model.orbits:
        images = set()
        for i in members:
            moved = list(model.configs[i])
            for link in links:
                moved[link] = g.table[z][moved[link]]
            images.add(model.orbit_of[model.index[tuple(moved)]])
        single = single and len(images) == 1
        perm.append(min(images))
    return perm, single


def holonomy_function(model, coarse_b, path, character):
    """character(holonomy of the fine path), as a value per orbit, and whether it is constant on each orbit. path is a list of (mu, sign, count) steps from the origin."""
    g = model.g
    sides = model.sides
    values = []
    invariant = True
    for members in model.orbits:
        seen = set()
        for i in members:
            c = model.configs[i]
            x = (0,) * model.d
            out = g.identity
            for mu, sign, count in path:
                for _ in range(count):
                    if sign > 0:
                        out = g.table[out][c[model.links[(x, mu)]]]
                        x = add(x, mu, sides)
                    else:
                        x = add(x, mu, sides, -1)
                        out = g.table[out][g.inverse[c[model.links[(x, mu)]]]]
            seen.add(character[out])
        invariant = invariant and len(seen) == 1
        values.append(min(seen))
    return values, invariant


def weighted(model, a, c):
    return sum(s * d * x * y for s, d, x, y in zip(model.sizes, model.diag, a, c))


def reduced(vector):
    g0 = 0
    for x in vector:
        g0 = math.gcd(g0, x)
    return [x // g0 for x in vector] if g0 > 1 else list(vector)


def pencil_on(model, basis):
    images = [model.apply_s(v) for v in basis]
    size = len(basis)
    big_g = [[weighted(model, basis[i], basis[j]) for j in range(size)] for i in range(size)]
    big_k = [[weighted(model, basis[i], images[j]) for j in range(size)] for i in range(size)]
    return big_g, big_k


def count_above(pencil, value, shift):
    """How many eigenvalues of the pencil lie above value / 2^shift."""
    big_g, big_k = pencil
    size = len(big_g)
    rows = [[(big_k[i][j] << shift) - value * big_g[i][j] for j in range(size)] for i in range(size)]
    return inertia_positive(rows)[0]


def level_bracket(pencil, top, wanted, shift):
    """(low, high) at scale 2^shift, with at least `wanted` eigenvalues above low and fewer above high, one unit apart."""
    low, high = 0, top
    if count_above(pencil, low, shift) < wanted:
        return 0, 0
    while high - low > 1:
        middle = (low + high) // 2
        if count_above(pencil, middle, shift) >= wanted:
            low = middle
        else:
            high = middle
    return low, high


def certify_overlap(model, w, top_low, top_high, next_high, shift, label, leak=None, quiet=False):
    """The share of w in the eigenspace of the top value, between a certified low and high, from <w, T^(2n) w>, with the other eigenvalues in [0, next_high], all three at scale 2^shift.
    In e = 0 a value above the target sits there too, the ground. leak = (num, den, ground_high): the ground's weight in w is at most num/den of |w|^2, and its value at most
    ground_high/2^shift, so <w, T^(2n) w> <= (num/den) |w|^2 ground_high^(2n) + share |w|^2 top_high^(2n) + |w|^2 next_high^(2n), and each n takes that first term off the low end."""
    norm = weighted(model, w, w)
    lows, highs = [], []
    moved = list(w)
    done = 0
    for n in (2, 4, 8, 16, 32, 64):
        while done < n:
            moved = model.apply_s(moved)
            done += 1
        a = weighted(model, moved, moved) << (2 * n * shift)
        skip = SABOTAGE == "overlap_skips_next"
        rest = 0 if skip else ipow(next_high, 2 * n)
        numerator = a - rest * norm
        denominator = (ipow(top_high, 2 * n) - rest) * norm
        if leak is None:
            lows.append((numerator * 1000000000) // denominator)
        else:
            num, den, ground_high = leak
            lows.append(((numerator * den - num * norm * ipow(ground_high, 2 * n)) * 1000000000) // (denominator * den))
        highs.append((a * 1000000000) // (ipow(top_low, 2 * n) * norm) + 1)
    low, high = max(lows), min(highs)
    if not quiet:
        check("overlap_bracket_%s" % label, low <= high)
        check("overlap_bracket_narrow_%s" % label, high - low <= 2000)
    return low, high


def exact_vector_visible(share_low, w_sq, error_num, error_den):
    """The computed vector's part in the level, at least (share_low/10^9) |w|^2 as a square, exceeds error_num/error_den, the most the rational Omega's error can put there,
    so the same construction on the exact Omega has a nonzero part in that level."""
    if SABOTAGE == "visibility_ignores_omega_error":
        error_num = 0
    return share_low > 0 and share_low * w_sq * error_den > 1000000000 * error_num


def section_flux():
    stamp("electric_flux")
    averages = []
    for n in range(1, 7):
        total = (0, 1)
        for q in T2_QUATS:
            cos_theta = half_trace(q)
            total = fadd(total, chebyshev_u(n, cos_theta[0], cos_theta[1]))
        averages.append(total)
    check("t2_is_a_design_of_degree_5", all(a[0] == 0 for a in averages[:5]) and averages[5] == (24, 1))
    say("YM4_03_T2_DESIGN|sum_of_chi_n/2_over_the_24_elements,n=1..6=%s|json=0" % ",".join(show(a) for a in averages))
    # The design as Lemma 9a uses it, on the 24 points themselves: each monomial in the four coordinates averages to its moment on S^3, through degree 5, and degree 6 has one apart from it.
    apart = []
    for degree in range(1, 7):
        count = 0
        for powers in itertools.product(range(degree + 1), repeat=4):
            if sum(powers) != degree:
                continue
            total = (0, 1)
            for q in T2_QUATS:
                total = fadd(total, (ipow(q[0], powers[0]) * ipow(q[1], powers[1]) * ipow(q[2], powers[2]) * ipow(q[3], powers[3]), ipow(q[4], degree)))
            top, bottom = 1, 1
            if any(p % 2 for p in powers):
                top = 0
            else:
                for p in powers:
                    for k in range(1, p, 2):
                        top *= k
                for j in range(degree // 2):
                    bottom *= 4 + 2 * j
            count += frac(total[0], total[1] * 24) != frac(top, bottom)
        apart.append(count)
    check("t2_moments_on_s3_through_degree_5", apart[:5] == [0, 0, 0, 0, 0] and apart[5] > 0)
    say("YM4_03_T2_MOMENTS|monomials_apart_from_S3,degree=1..6=%s|json=0" % ",".join(map(str, apart)))
    # Winding parity on the four-dimensional lattice, on exact quaternions, at every plane.
    for bi, side in ((2, 4), (3, 6)):
        pool = quaternion_pool(4040 + bi, 48)
        stream = Stream(5050 + bi)
        sides = (side,) * 4
        sites = sites_of(sides)
        U = {(x, mu): pool[stream.next(48)] for x in sites for mu in range(4)}
        minus = (-1, 0, 0, 0, 1)
        b = (bi,) * 4
        good = rows = 0
        for s in range(side):
            twisted = dict(U)
            for (x, mu), value in U.items():
                if mu == 0 and (x[0] == s or SABOTAGE == "twist_every_link"):
                    twisted[(x, mu)] = qmul(minus, value)
            for start_c in sites_of((2, 2, 2, 2)):
                start = tuple(c * bi for c in start_c)
                # Once around in direction 0, twice around, and a contractible coarse loop.
                once, _ = holonomy_steps(U, start, ((0, 1), (0, 1)), sides, qmul, qinv, Q_ONE, b)
                once_t, _ = holonomy_steps(twisted, start, ((0, 1), (0, 1)), sides, qmul, qinv, Q_ONE, b)
                twice_t, _ = holonomy_steps(twisted, start, ((0, 1), (0, 1), (0, 1), (0, 1)), sides, qmul, qinv, Q_ONE, b)
                twice, _ = holonomy_steps(U, start, ((0, 1), (0, 1), (0, 1), (0, 1)), sides, qmul, qinv, Q_ONE, b)
                loop = ((0, 1), (1, 1), (0, -1), (1, -1))
                closed, _ = holonomy_steps(U, start, loop, sides, qmul, qinv, Q_ONE, b)
                closed_t, _ = holonomy_steps(twisted, start, loop, sides, qmul, qinv, Q_ONE, b)
                rows += 1
                good += once_t == qmul(minus, once) and once_t != once and twice_t == twice and half_trace(closed_t) == half_trace(closed)
        check("winding_parity_b=%d" % bi, good == rows)
        say("YM4_03_WINDING_PARITY|b=%d|fine=%d^4|planes=%d|rows=%d|as_the_law_says=%d|json=0" % (bi, side, side, rows, good))
    if SABOTAGE == "twist_every_link":
        return
    # The sectors on small spatial lattices.
    for name, sides, b_space in (("Z2", (2, 1), (2, 1)), ("Z2", (2, 2), (2, 2)), ("Z2", (3, 1), (3, 1)), ("Z2", (3, 2), (3, 2)), ("Q8", (2, 1), (2, 1))):
        tag = "%s_%s" % (name, "x".join(map(str, sides)))
        w = [3, 1] if name == "Z2" else weight_three_plus(name)
        model = Transfer(name, sides, w)
        d = len(sides)
        perms = []
        commute = True
        planes_equal = True
        single_orbit = True
        for mu in range(d):
            perm, single = twist_perm(model, mu, 0)
            single_orbit = single_orbit and single
            for s in range(1, sides[mu]):
                other, single_s = twist_perm(model, mu, s)
                single_orbit = single_orbit and single_s
                planes_equal = planes_equal and other == perm
            perms.append(perm)
            commute = commute and all(model.diag[perm[a]] == model.diag[a] and model.sizes[perm[a]] == model.sizes[a] for a in range(model.m))
            commute = commute and all(model.kernel[perm[a]][perm[c]] == model.kernel[a][c] for a in range(model.m) for c in range(model.m))
        check("flux_commutation_%s" % tag, commute and single_orbit)
        check("flux_planes_equal_%s" % tag, planes_equal)
        # The rational Perron vector, with the bits held down the same way at every coordinate, so its symmetry stays exact.
        u = [1] * model.m
        for _ in range(240):
            u = reduced(model.apply_s(u))
            top_bits = max(x.bit_length() for x in u)
            if top_bits > 3072:
                u = [(x >> (top_bits - 3072)) + 1 for x in u]
        check("flux_perron_vector_even_%s" % tag, all(u[perm[a]] == u[a] for perm in perms for a in range(model.m)))
        moved = model.apply_s(u)
        ratio_high = max(((m_ << 64) // x) + 1 for m_, x in zip(moved, u))
        ratio_low = min((m_ << 64) // x for m_, x in zip(moved, u))
        lam_low, lam_high = ratio_low >> 64, (ratio_high >> 64) + 1
        # Sectors.
        sector_rows = []
        whole_top = lam_high
        results = {}
        for e in itertools.product((1, -1), repeat=d):
            basis, pivots, kept = [], [], []
            for k in range(model.m):
                vector = [0] * model.m
                terms = [(k, 1)]
                for mu in range(d):
                    sign = e[mu]
                    if SABOTAGE == "flux_wrong_sign" and mu == 0:
                        sign = -sign
                    next_terms = {}
                    for a, coefficient in terms:
                        next_terms[a] = next_terms.get(a, 0) + coefficient
                        image = perms[mu][a]
                        next_terms[image] = next_terms.get(image, 0) + sign * coefficient
                    terms = list(next_terms.items())
                for a, coefficient in terms:
                    vector[a] += coefficient
                if any(vector) and rational_basis_add(basis, pivots, vector):
                    kept.append(reduced(vector))
            results[e] = dict(dimension=len(kept), basis=kept)
        total_dimension = sum(r["dimension"] for r in results.values())
        check("flux_sectors_span_%s" % tag, total_dimension == model.m)
        check("flux_every_sector_nonempty_%s" % tag, all(r["dimension"] > 0 for r in results.values()))
        shift = max(0, (32 if model.m > 60 else 44) - whole_top.bit_length())
        whole_top = whole_top << shift
        zero = (1,) * d
        for e, record in results.items():
            if record["dimension"] == 0:
                record["levels"] = None
                continue
            pencil = pencil_on(model, record["basis"])
            record["pencil"] = pencil
            levels = []
            if e == zero:
                needed = 3
            else:
                needed = 2
            wanted = 1
            while len(levels) < needed and wanted <= record["dimension"]:
                low, high = level_bracket(pencil, whole_top, wanted, shift)
                multiplicity = count_above(pencil, low, shift)
                levels.append((low, high, multiplicity))
                wanted = multiplicity + 1
            record["levels"] = levels
            check("flux_spectrum_at_least_minus_the_step_%s_%s" % (tag, e), count_above(pencil, -1, shift) == record["dimension"])
        ground = results[zero]["levels"][0]
        check("flux_ground_in_e=0_%s" % tag, ground[2] == 1 and all(results[e]["levels"] is None or e == zero or results[e]["levels"][0][1] <= ground[0] for e in results))
        check("flux_ground_is_perron_%s" % tag, ground[0] <= lam_high << shift and lam_low << shift <= ground[1])
        # The named coarse functions.
        coarse = tuple(s // bi for s, bi in zip(sides, b_space))
        character = fundamental_character(name)
        windings = {}
        for mu in range(d):
            windings[mu] = holonomy_function(model, b_space, [(mu, 1, sides[mu])], character)
            check("flux_winding_function_invariant_%s_%d" % (tag, mu), windings[mu][1])
        # Epsilon, the rational Perron vector's error: its residual over the gap, as squares.
        rho_n = weighted(model, u, moved)
        rho_d = weighted(model, u, u)
        residual = [rho_d * m_ - rho_n * x for m_, x in zip(moved, u)]
        residual_sq = weighted(model, residual, residual)
        gap = (rho_n << shift) // rho_d - results[zero]["levels"][1][1] if len(results[zero]["levels"]) > 1 else (rho_n << shift) // rho_d
        check("flux_gap_positive_%s" % tag, gap > 0)
        # delta^2 <= residual^2/gap^2. In e = 0 the certificate multiplies what is left of Omega by (ground/first)^128, so that product has to stay below 2^-60.
        first_low = results[zero]["levels"][1][0] if len(results[zero]["levels"]) > 1 else 1
        epsilon_ok = (residual_sq * ipow(ground[1], 128)) << (60 + 2 * shift) <= (gap * gap) * rho_d * rho_d * rho_d * ipow(max(first_low, 1), 128)
        check("flux_rational_omega_close_%s" % tag, epsilon_ok)
        # sin^2(u, Omega) <= |S u - rho u|^2/(gap^2 |u|^2), with the residual at rho_d times that and gap at 2^shift: sin2_num/sin2_den. u lies in e = 0 (flux_perron_vector_even),
        # so only e = 0's values enter, and they sit at or under the first excited level's high end. A vector orthogonal to u holds at most sin^2 of its |w|^2 along Omega.
        sin2_num, sin2_den = residual_sq << (2 * shift), gap * gap * rho_d * rho_d * rho_d
        norm_u = weighted(model, u, u)
        delta_rows = []
        for e, record in results.items():
            if record["levels"] is None:
                continue
            path = []
            for mu in range(d):
                if e[mu] < 0:
                    path.append((mu, 1, sides[mu]))
            if path:
                f_values, invariant = holonomy_function(model, b_space, path, character)
                check("flux_function_invariant_%s_%s" % (tag, e), invariant)
                charged = all(f_values[perms[mu][a]] == (e[mu] * f_values[a]) for mu in range(d) for a in range(model.m))
                check("winding_parity_on_orbits_%s_%s" % (tag, e), charged)
                access = any(f_values)
                check("coarse_sector_access_%s_%s" % (tag, e), access)
                # P_e(F) nonzero, read through the sector's own basis: F lies in the sector.
                in_sector = rank_keeps(record["basis"], f_values)
                check("coarse_function_in_sector_%s_%s" % (tag, e), in_sector)
                vector = [f * x for f, x in zip(f_values, u)]
                top_low, top_high, mult = record["levels"][0]
                next_high = record["levels"][1][1] if len(record["levels"]) > 1 else 0
                low, high = certify_overlap(model, vector, top_low, top_high, next_high, shift, "%s_%s" % (tag, e))
                if tag == "Z2_2x1" and e == (1, -1):
                    # By hand, with no power of T: in the chain basis S on e = 0 is [[1280, 1024], [256, 320]], S on this sector is 128 [[5, 4], [4, 5]], the inner product is [[5, 4], [4, 5]], and r = (sqrt(481) - 15)/32 is the ratio in Omega. The share 9 (1 + r)^2 / (2 (5 + 5 r^2 + 8 r)) increases with r.
                    root = math.isqrt(481 << 200)
                    closed = []
                    for s_ in (root, root + 1):
                        r_n, r_d = s_ - (15 << 100), 32 << 100
                        closed.append((9 * (r_d + r_n) * (r_d + r_n) * 1000000000) // (2 * (5 * r_d * r_d + 5 * r_n * r_n + 8 * r_n * r_d)))
                    check("overlap_closed_form_%s_%s" % (tag, e), low <= closed[0] and closed[1] + 1 <= high)
                # F u = |u| (cos F Omega + sin F xi): the part in the level of F Omega is nonzero when that of F u exceeds |u| sin max|f|.
                f_max = max(abs(f) for f in f_values)
                visible = exact_vector_visible(low, weighted(model, vector, vector), norm_u * sin2_num * f_max * f_max, sin2_den)
                read_row("lowest_state_visible_%s_e=%s" % (tag, ",".join(map(str, e))), visible, "share_e-9_in_[%d,%d]_of_multiplicity_%d" % (low, high, mult), "positive")
                delta_rows.append((e, top_high, mult, low, high, "winding"))
            else:
                # e = 0: a contractible or even coarse function, with Omega taken out; failing that, two insertions.
                candidates = []
                if d >= 2:
                    mu, nu = 0, 1
                    candidates.append(("commutator", [(mu, 1, sides[mu]), (nu, 1, sides[nu]), (mu, -1, sides[mu]), (nu, -1, sides[nu])]))
                top_low, top_high, mult = record["levels"][1] if len(record["levels"]) > 1 else (0, 0, 0)
                mult -= record["levels"][0][2]
                next_high = record["levels"][2][1] if len(record["levels"]) > 2 else 0
                found = None
                leak = (sin2_num, sin2_den, ground[1])

                def certified_beyond_the_error(vector, op_sq_num, op_sq_den, quiet=True, label_c=""):
                    """w = |u|^2 v - <u, v> u with v = O u. With u = |u| (cos Omega + sin xi), the part in the level of O Omega is nonzero when |P w| > |u|^2 sin (|v| + |u| |O|),
                    and (x + y)^2 <= 2 x^2 + 2 y^2 gives the square read here, with |O|^2 at most op_sq_num/op_sq_den."""
                    along = weighted(model, u, vector)
                    full = [norm_u * v - along * x for v, x in zip(vector, u)]
                    full_sq = weighted(model, full, full)
                    if full_sq == 0:
                        return None
                    centered = reduced(full)
                    low, high = certify_overlap(model, centered, top_low, top_high, next_high, shift, label_c, leak=leak, quiet=quiet)
                    v_sq = weighted(model, vector, vector)
                    error_num = 2 * norm_u * norm_u * sin2_num * (v_sq * op_sq_den + norm_u * op_sq_num)
                    error_den = sin2_den * op_sq_den
                    return (low, high, centered) if exact_vector_visible(low, full_sq, error_num, error_den) else None

                for label, path_c in candidates:
                    f_values, invariant = holonomy_function(model, b_space, path_c, character)
                    check("flux_even_function_invariant_%s_%s" % (tag, label), invariant)
                    vector = [f * x for f, x in zip(f_values, u)]
                    f_max = max(abs(f) for f in f_values)
                    reached = certified_beyond_the_error(vector, f_max * f_max, 1)
                    if reached is not None:
                        found = (label, reached[2])
                        break
                read_row("first_excited_visible_single_insertion_%s" % tag, found is not None, found[0] if found else "only_constants_among_even_single_insertions", "a_contractible_or_even_coarse_F")
                if found is None:
                    # F T^b F Omega in e = 0, with the first winding function whose centered vector stands above u's own error: its size squared against 2^100 sin^2 theta, with sin^2 theta <= residual^2/gap^2.
                    # With a transverse side of 1 the winding in the other direction has F S F = 2^(-L_0) S on e = 0, exactly, so its vector is a multiple of Omega and centering returns u's own residual, and the row takes the next direction.
                    if sides[1] == 1:
                        f_values = windings[0][0]
                        scaled = all((f * x) << sides[0] == y for v in record["basis"] for f, x, y in zip(f_values, model.apply_s([f * c for f, c in zip(f_values, v)]), model.apply_s(v)))
                        check("flux_winding_0_scales_S_on_e=0_%s" % tag, scaled)
                    rejected = []
                    for mu in range(d):
                        f_values = windings[mu][0]
                        vector = [f * x for f, x in zip(f_values, u)]
                        for _ in range(b_space[0]):
                            vector = model.apply_s(vector)
                        vector = [f * x for f, x in zip(f_values, vector)]
                        # |F T^b F| <= max|f|^2 ground^b.
                        f_max = max(abs(f) for f in f_values)
                        reached = certified_beyond_the_error(vector, ipow(f_max, 4) * ipow(ground[1], 2 * b_space[0]), 1 << (2 * b_space[0] * shift))
                        if reached is not None:
                            found = ("winding_%d_T^b_winding_%d" % (mu, mu), reached[2])
                            break
                        rejected.append(mu)
                    check("flux_two_insertions_above_the_residual_%s" % tag, found is not None)
                    if sides[1] == 1:
                        # Negative control: the winding in direction 0 gives F T^b F Omega = 2^(-b L_0) T^b Omega, a multiple of Omega, so its part in the first excited level is exactly 0, and the certificate reads it not certified.
                        check("flux_exact_zero_overlap_not_certified_%s" % tag, 0 in rejected)
                    if found is None:
                        continue
                low, high = certify_overlap(model, found[1], top_low, top_high, next_high, shift, "%s_e=0" % tag, leak=leak)
                read_row("first_excited_visible_%s" % tag, low > 0, "%s_share_e-9_in_[%d,%d]_of_multiplicity_%d" % (found[0], low, high, mult), "positive")
                delta_rows.append((e, top_high, mult, low, high, found[0]))
        # Delta_full, read off the rows as the larger of the two ratios to the ground value.
        ground_low = ground[0]
        flux_top = max((row[1] for row in delta_rows if row[0] != zero), default=0)
        zero_top = max((row[1] for row in delta_rows if row[0] == zero), default=0)
        # Delta_full = min(Delta_0, Delta_flux) rests on the sectors being orthogonal and S keeping each: every cross entry of G and K vanishes, and with the span the sectors' spectra are the whole spectrum.
        cross = True
        bases = [r["basis"] for r in results.values()]
        images = [[model.apply_s(v) for v in basis] for basis in bases]
        for i in range(len(bases)):
            for j in range(i):
                for left in bases[i]:
                    for right, right_image in zip(bases[j], images[j]):
                        cross = cross and weighted(model, left, right) == 0 and weighted(model, left, right_image) == 0
        say("YM4_03_FLUX|%s|orbits=%d|sector_dimensions=%s|top_e=0_over_ground_ppm=%d|top_flux_over_ground_ppm=%d|lowest_of_the_two_gaps=%s|json=0" % (tag, model.m, ",".join("%s:%d" % ("".join("+" if x > 0 else "-" for x in e), r["dimension"]) for e, r in results.items()), zero_top * 1000000 // ground_low, flux_top * 1000000 // ground_low, "flux" if flux_top >= zero_top else "e=0"))
        check("flux_full_gap_is_the_min_%s" % tag, cross and total_dimension == model.m)
        # The same read on the whole orbit space, at most 128 orbits: above the second value sits the ground alone, and at the low end of the highest level below the ground, the ground and that level.
        if model.m <= 128:
            whole = pencil_on(model, [[1 if i == k else 0 for i in range(model.m)] for k in range(model.m)])
            full_low = max(r["levels"][1 if e == zero else 0][0] for e, r in results.items() if r["levels"] is not None)
            check("flux_second_value_on_the_whole_%s" % tag, count_above(whole, max(flux_top, zero_top), shift) == 1 and count_above(whole, full_low, shift) >= 2)


def rank_keeps(basis, vector):
    """True when vector lies in the span of basis, exactly."""
    rows, pivots = [], []
    for row in basis:
        rational_basis_add(rows, pivots, row)
    return not rational_basis_add(rows, pivots, vector)


def section_walls():
    stamp("walls")
    for name, sides, b, trials in (("Z2", (2, 2, 2), (2, 2, 2), 6), ("Z2", (4, 2, 2), (2, 2, 2), 4), ("S3", (2, 2), (2, 2), 6), ("S3", (4, 2), (2, 2), 4), ("Z2", (2, 4, 2), (2, 2, 2), 4), ("Z2", (2, 2, 4), (2, 2, 2), 4)):
        g = GROUPS[name]
        w = [3, 1] if name == "Z2" else weight_three_plus(name)
        lat = FiniteLattice(sides, b)
        index_to_key = {v: k for k, v in lat.links.items()}
        wall_links = set()
        for link, (x, mu) in index_to_key.items():
            y = add(x, mu, sides)
            for nu in range(lat.d):
                # A link lies in a wall when a coordinate transverse to it sits on a multiple of the block.
                if SABOTAGE == "wrong_block_shell" and nu == 0:
                    continue
                if nu != mu and x[nu] % b[nu] == 0 and y[nu] % b[nu] == 0:
                    wall_links.add(link)
        blocks = {}
        for x in lat.sites:
            blocks.setdefault(tuple(c // bi for c, bi in zip(x, b)), []).append(x)
        stream = Stream(7000 + g.n)
        good = rows = 0
        for _ in range(trials):
            walls = {link: stream.next(g.n) for link in wall_links}
            words = lat.plaquettes
            # The whole sum over interior links, by elimination.
            factors = []
            constant = 1
            for word in words:
                vs = sorted({link for link, _ in word if link not in walls})
                if not vs:
                    constant *= w[lat.word_value(word, walls, g)]
                    continue
                data = {}
                for assignment in itertools.product(range(g.n), repeat=len(vs)):
                    local = dict(walls)
                    local.update(zip(vs, assignment))
                    data[assignment] = w[lat.word_value(word, local, g)]
                factors.append((tuple(vs), data))
            whole, _ = eliminate(g.n, factors)
            # Each connected group of interior links by itself: the product over those groups.
            parent = {}

            def find(a):
                while parent[a] != a:
                    parent[a] = parent[parent[a]]
                    a = parent[a]
                return a

            for vs, _ in factors:
                for v in vs:
                    parent.setdefault(v, v)
                for v in vs[1:]:
                    parent[find(v)] = find(vs[0])
            groups = {}
            for factor in factors:
                groups.setdefault(find(factor[0][0]), []).append(factor)
            separate = 1
            for factor_group in groups.values():
                value, _ = eliminate(g.n, factor_group)
                separate *= value
            rows += 1
            # Blocks in the block structure: no interior group crosses a wall.
            crossing = 0
            for group_factors in groups.values():
                cells = set()
                for vs, _ in group_factors:
                    for v in vs:
                        x, mu = index_to_key[v]
                        cells.add(tuple(c // bi for c, bi in zip(x, b)))
                if len(cells) > 1:
                    crossing += 1
            good += whole == separate and crossing == 0
        check("walls_%s_%s" % (name, "x".join(map(str, sides))), good == rows)
        say("YM4_03_WALLS|group=%s|fine=%s|wall_links=%d|interior_links=%d|blocks=%d|configurations=%d|product_over_blocks=%d|json=0" % (name, "x".join(map(str, sides)), len(wall_links), len(lat.links) - len(wall_links), len(blocks), rows, good))


def main():
    say("YM4_03_START|prediction=docs/PREDICTION-YM4-03.hbp|integers_only=1|json=0")
    links = section_covariance()
    say("YM4_03_COVARIANCE_TOTAL|coarse_links=%d|json=0" % links)
    section_loops()
    section_reflection()
    section_haar()
    section_pushforward()
    section_two_dimensions()
    section_three_dimensions()
    section_core_count()
    section_first_dependence()
    section_certified()
    section_coarse_space()
    section_circle()
    section_su2_two_dimensions()
    section_z2_surfaces()
    section_walls()
    section_flux()
    stamp("done")
    say("YM4_03_DONE|checks=%d|failed=%d|prediction_misses=%d|misses=%s|json=0" % (CHECKS[0], len(FAILS), len(MISSES), ",".join(MISSES) if MISSES else "none"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
