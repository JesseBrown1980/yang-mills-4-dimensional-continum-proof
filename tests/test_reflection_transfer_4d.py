#!/usr/bin/env python3
"""YM4-02c: reflection positivity and the transfer operator of the finite 4D SU(2) Wilson lattice.

Exact checks against the rows of docs/PREDICTION-YM4-02c.hbp. The theorems of docs/LEMMA-0004-REFLECTION-TRANSFER.md hold
for a compact group with a real class weight with w(g^-1) = w(g), so Q8 and 2T with counting measure are instances of them in their own right.
Q8 stands in for Haar on SU(2) only where a row says so, within its exact degree of 3 per link.

usage = test_reflection_transfer_4d.py [sabotage=NAME]
NAME is one of SABOTAGE_NAMES below, and each must exit 1 on a named check.
Python standard library, integers only, json=0.
"""
import collections
import itertools
import math
import sys

SABOTAGE_NAMES = ("no_inverse_on_time_links", "wrong_plane", "wrong_multiplicity", "negative_weight_called_positive",
                  "signed_site_weight_called_positive", "bad_projector", "no_inverse_in_gram", "wrong_plane_in_gram",
                  "dropped_inverse_third_letter", "dropped_inverse_fourth_letter", "every_function_one_plane", "t4_half_weights_dropped")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_reflection_transfer_4d.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]
FAILS = []


def check(name, ok):
    if not ok:
        FAILS.append(name)
    return 1 if ok else 0


def power(base, exponent):
    """An integer power that refuses a negative exponent, since an int to a negative int is a float in Python."""
    if exponent < 0:
        raise ValueError("negative exponent")
    result = 1
    for _ in range(exponent):
        result *= base
    return result


# ---- Exact rationals as reduced integer pairs.
def red(n, d=1):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d)
    return n // g, d // g


def padd(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def psub(a, b):
    return red(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def pmul(a, b):
    return red(a[0] * b[0], a[1] * b[1])


def text(a):
    return "%d" % a[0] if a[1] == 1 else "%d/%d" % a


def scaled_floor(a, scale):
    return a[0] * scale // a[1]


def scaled_ceiling(a, scale):
    return -((-a[0] * scale) // a[1])


# ---- Exact PSD test. Fraction-free elimination with symmetric pivoting on an integer symmetric matrix.
def psd_exact(rows):
    """Returns (is_psd, rank, reason). After each pivot the trailing block is the Schur complement times the pivot, all exact integers, so its signs decide."""
    m = [list(r) for r in rows]
    n = len(m)
    if not all(m[i][j] == m[j][i] for i in range(n) for j in range(i)):
        return False, 0, "not_symmetric"
    prev = 1
    for k in range(n):
        if min(m[i][i] for i in range(k, n)) < 0:
            return False, k, "negative_pivot"
        pivot = next((i for i in range(k, n) if m[i][i] > 0), None)
        if pivot is None:
            if any(m[i][j] for i in range(k, n) for j in range(k, n)):
                return False, k, "zero_diagonal_with_nonzero_entry"
            return True, k, "none"
        m[k], m[pivot] = m[pivot], m[k]
        for row in m:
            row[k], row[pivot] = row[pivot], row[k]
        top = m[k][k]
        for i in range(k + 1, n):
            ri, rk, mik = m[i], m[k], m[i][k]
            for j in range(k + 1, n):
                value, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = value
        prev = top
    return True, n, "none"


def inertia_exact(rows):
    """Returns (positive, negative, rank) of an integer symmetric matrix, and rank -1 for an asymmetric one. Fraction-free elimination with diagonal pivots: each pivot is a leading principal minor of the permuted matrix, so a sign change between consecutive pivots marks one negative eigenvalue. When the diagonal of the trailing block is zero and an off-diagonal entry is not, adding one row and column to another is a unimodular congruence and makes a pivot."""
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


def determinant(rows):
    m = [list(r) for r in rows]
    n = len(m)
    prev, sign = 1, 1
    for k in range(n - 1):
        if m[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if m[i][k]), None)
            if swap is None:
                return 0
            m[k], m[swap] = m[swap], m[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                value, rest = divmod(m[i][j] * m[k][k] - m[i][k] * m[k][j], prev)
                assert rest == 0
                m[i][j] = value
        prev = m[k][k]
    return sign * m[n - 1][n - 1] if n else 1


def all_principal_minors_nonnegative(rows):
    n = len(rows)
    return all(determinant([[rows[i][j] for j in subset] for i in subset]) >= 0
               for size in range(1, n + 1) for subset in itertools.combinations(range(n), size))


def section_psd_controls():
    ok = (psd_exact([[1, 1], [1, 1]])[:2] == (True, 1) and psd_exact([[0, 1], [1, 0]])[0] is False
          and psd_exact([[1, 2], [2, 1]])[0] is False and psd_exact([[0, 0], [0, 3]])[:2] == (True, 1)
          and all_principal_minors_nonnegative([[1, 1], [1, 1]]) and not all_principal_minors_nonnegative([[1, 2], [2, 1]]))
    # Both matrices have a zero diagonal, so each enters the congruence branch of inertia_exact.
    pair, triangle = inertia_exact([[0, 1], [1, 0]]), inertia_exact([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    ok = ok and pair == (1, 1, 2) and triangle == (1, 2, 3)
    print("PSD_TEST_CONTROLS|rank_one=green|zero_diagonal_indefinite=red|negative_minor=red|inertia_of_[[0,1],[1,0]]=%d,%d|inertia_of_the_triangle=%d,%d|ok=%d|json=0" % (pair[0], pair[1], triangle[0], triangle[1], check("exact PSD test reads its controls", ok)))


# ---- Exact SU(2) elements as five ints (a, b, c, d, den), meaning (a, b, c, d) / den, reduced with den > 0.
def quat(a, b, c, d, den=1):
    g = math.gcd(math.gcd(math.gcd(math.gcd(a, b), c), d), den)
    return a // g, b // g, c // g, d // g, den // g


QONE = quat(1, 0, 0, 0)


def qmul(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return quat(a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n)


def qinv(p):
    return p[0], -p[1], -p[2], -p[3], p[4]


def qneg(p):
    return -p[0], -p[1], -p[2], -p[3], p[4]


def half_trace(p):
    return red(p[0], p[4])


QA, QB, QC = quat(3, 4, 0, 0, 5), quat(5, 0, 12, 0, 13), quat(8, 0, 0, 15, 17)
PALETTE = [QONE, QA, QB, QC, qinv(QA), qinv(QB), qinv(QC), qmul(QA, QB), qmul(QB, QC), qmul(QC, QA)]


class Stream:
    """A plain linear congruential stream, so that the configurations are the same on every Python."""

    def __init__(self, seed):
        self.state = seed

    def below(self, n):
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % 2 ** 64
        return (self.state >> 33) % n


# ---- The periodic lattice. The last direction is time. A link is (site, direction).
class Lattice:
    def __init__(self, *dims):
        self.dims = dims
        self.time = len(dims) - 1
        self.T = dims[-1]
        self.sites = list(itertools.product(*[range(n) for n in dims]))
        self.links = [(x, mu) for x in self.sites for mu in range(len(dims))]
        self.plaquettes = [(x, mu, nu) for x in self.sites for mu in range(len(dims)) for nu in range(mu + 1, len(dims))]

    def shift(self, x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % self.dims[mu]
        return tuple(y)

    def word(self, p):
        # U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1, the repository's convention.
        x, mu, nu = p
        third = 1 if SABOTAGE == "dropped_inverse_third_letter" else -1
        fourth = 1 if SABOTAGE == "dropped_inverse_fourth_letter" else -1
        return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), third), ((x, nu), fourth))


class Reflection:
    """t -> c - t. Site reflection has c = 0 and link reflection c = -1. (theta U)(link) = U(image) ^ sign."""

    def __init__(self, lat, kind):
        self.lat, self.kind = lat, kind
        self.c = 0 if kind == "site" else -1
        if SABOTAGE in ("wrong_plane", "wrong_plane_in_gram"):
            self.c = -1 - self.c

    def t(self, t):
        return (self.c - t) % self.lat.T

    def link(self, link):
        x, mu = link
        if mu != self.lat.time:
            return (x[:-1] + (self.t(x[-1]),), mu), 1
        # The edge from t to t+1 goes to the edge from c-t to c-t-1, the positive link at c-t-1 run backward.
        return (x[:-1] + (self.t(x[-1] + 1),), mu), (1 if SABOTAGE in ("no_inverse_on_time_links", "no_inverse_in_gram") else -1)

    def plaquette(self, p):
        x, mu, nu = p
        if nu != self.lat.time:
            return (x[:-1] + (self.t(x[-1]),), mu, nu)
        return (x[:-1] + (self.t(x[-1] + 1),), mu, nu)

    def word(self, word):
        out = []
        for l, s in word:
            image, sign = self.link(l)
            out.append((image, sign * s))
        return tuple(out)


def partition(lat, kind):
    """The declared split, (upper, shared, lower), written from the planes alone. Shared means fixed-slice for site reflection and crossing for link reflection."""
    m = lat.T // 2
    upper, shared, lower = [], [], []
    for p in lat.plaquettes:
        t, timelike = p[0][-1], p[2] == lat.time
        if kind == "site":
            side = (upper if t < m else lower) if timelike else (shared if t in (0, m) else (upper if t < m else lower))
        else:
            side = (shared if t in (m - 1, lat.T - 1) else (upper if t < m else lower)) if timelike else (upper if t < m else lower)
        side.append(p)
    return upper, shared, lower


def rotations(word):
    return [word[i:] + word[:i] for i in range(len(word))]


def inverse_word(word):
    return tuple((l, -s) for l, s in reversed(word))


def holonomy(word, field):
    out = QONE
    for l, s in word:
        out = qmul(out, field[l] if s > 0 else qinv(field[l]))
    return out


def reflected_field(lat, R, field):
    out = {}
    for l in lat.links:
        image, sign = R.link(l)
        out[l] = field[image] if sign > 0 else qinv(field[image])
    return out


def traces(lat, field):
    return {p: half_trace(holonomy(lat.word(p), field)) for p in lat.plaquettes}


def deficit(names, a):
    """The sum of (1 - a_p) over the named plaquettes, a reduced pair."""
    top, bottom = 0, 1
    for p in names:
        n, d = a[p]
        top, bottom = top * d + (d - n) * bottom, bottom * d
        g = math.gcd(top, bottom)
        top, bottom = top // g, bottom // g
    return top, bottom


def links_of(lat, names):
    return {l for p in names for l, _ in lat.word(p)}


def section_orientation(lat, L, T):
    """The plaquette words as oriented cycles, read against the path each traces and against the gauge action. The REFLECTION rows compare words up to rotation and inversion, so this row carries the orientation."""
    closed, forward, backward = 0, collections.Counter(), collections.Counter()
    for p in lat.plaquettes:
        x, mu, nu = p
        ends = []
        for (y, direction), s in lat.word(p):
            head = lat.shift(y, direction)
            ends.append((y, head) if s > 0 else (head, y))
            if s > 0:
                forward[((y, direction), mu, nu)] += 1
            else:
                backward[((y, direction), mu, nu)] += 1
        closed += 1 if ends[0][0] == x and all(ends[i][1] == ends[(i + 1) % 4][0] for i in range(4)) else 0
    once = set(forward) == set(backward) and all(v == 1 for v in forward.values()) and all(v == 1 for v in backward.values())
    conjugate, configurations = True, 2
    for seed in range(configurations):
        stream = Stream(424243 + 7919 * seed + 31 * L + T)
        field = {l: PALETTE[stream.below(len(PALETTE))] for l in lat.links}
        gauge = {x: PALETTE[stream.below(len(PALETTE))] for x in lat.sites}
        gauged = {(x, mu): qmul(qmul(gauge[x], field[(x, mu)]), qinv(gauge[lat.shift(x, mu)])) for (x, mu) in lat.links}
        for p in lat.plaquettes:
            word = lat.word(p)
            conjugate = conjugate and holonomy(word, gauged) == qmul(qmul(gauge[p[0]], holonomy(word, field)), qinv(gauge[p[0]]))
    ok = closed == len(lat.plaquettes) and once and conjugate
    print("PLAQUETTE_ORIENTATION|L=%d|T=%d|closed_paths=%d|of=%d|each_link_once_forward_and_once_backward_in_each_plane=%d|U_p(U^g)=g(y)U_p(U)g(y)^-1=%d|configurations=%d|ok=%d|json=0" % (
        L, T, closed, len(lat.plaquettes), 1 if once else 0, 1 if conjugate else 0, configurations, check("plaquette orientation on L=%d T=%d" % (L, T), ok)))


def section_geometry():
    """Part A, rows YM4_02C_GEOMETRY_RULE, YM4_02C_GEOMETRY and YM4_02C_ACTION_SPLIT."""
    expect = {(2, 2): (96, 48, 24), (2, 4): (192, 48, 72), (3, 4): (648, 162, 243)}
    for (L, T), (want_total, want_shared, want_half) in expect.items():
        lat = Lattice(L, L, L, T)
        m = T // 2
        for kind in ("link", "site"):
            R = Reflection(lat, kind)
            upper, shared, lower = partition(lat, kind)
            counts = len(lat.plaquettes) == want_total and len(shared) == want_shared and len(upper) == want_half and len(lower) == want_half
            rule = want_total == 6 * L ** 3 * T and want_shared == 6 * L ** 3 and want_half == 3 * L ** 3 * (T - 1)
            involution = True
            for l in lat.links:
                image, sign = R.link(l)
                back, sign2 = R.link(image)
                involution = involution and back == l and sign * sign2 == 1
            to_plaquettes = True
            for p in lat.plaquettes:
                target = lat.word(R.plaquette(p))
                image = R.word(lat.word(p))
                to_plaquettes = to_plaquettes and R.plaquette(R.plaquette(p)) == p and (image in rotations(target) or image in rotations(inverse_word(target)))
            sides = {R.plaquette(p) for p in upper} == set(lower) and all(R.plaquette(p) == p for p in shared)
            if kind == "site":
                # The two closed halves share exactly the spatial links of the fixed slices.
                closed_up = links_of(lat, upper + shared)
                closed_down = links_of(lat, lower + shared)
                fixed = {(x, mu) for (x, mu) in lat.links if mu != lat.time and x[-1] in (0, m)}
                support = closed_up & closed_down == fixed
            else:
                # The open halves share nothing, and each crossing plaquette holds two crossing links.
                crossing = {(x, mu) for (x, mu) in lat.links if mu == lat.time and x[-1] in (m - 1, T - 1)}
                support = (not links_of(lat, upper) & links_of(lat, lower) and not links_of(lat, upper) & crossing
                           and not links_of(lat, lower) & crossing and links_of(lat, shared) & crossing == crossing)
            agree, split, covariant = True, True, True
            configurations = 2
            for seed in range(configurations):
                stream = Stream(20261103 + 7919 * seed + 31 * L + T)
                field = {l: PALETTE[stream.below(len(PALETTE))] for l in lat.links}
                mirrored = reflected_field(lat, R, field)
                a = traces(lat, field)
                b = traces(lat, mirrored)
                agree = agree and all(b[R.plaquette(p)] == a[p] and b[p] == a[R.plaquette(p)] for p in lat.plaquettes)
                total = deficit(lat.plaquettes, a)
                if kind == "site":
                    half = pmul((1, 2), padd(deficit(shared, a), deficit(shared, b)))
                    split = split and total == padd(padd(deficit(upper, a), deficit(upper, b)), half)
                else:
                    split = split and total == padd(padd(deficit(upper, a), deficit(upper, b)), deficit(shared, a))
                gauge = {x: PALETTE[stream.below(len(PALETTE))] for x in lat.sites}
                gauged = {(x, mu): qmul(qmul(gauge[x], field[(x, mu)]), qinv(gauge[lat.shift(x, mu)])) for (x, mu) in lat.links}
                left = reflected_field(lat, R, gauged)
                gauge2 = {x: gauge[x[:-1] + (R.t(x[-1]),)] for x in lat.sites}
                right = {(x, mu): qmul(qmul(gauge2[x], mirrored[(x, mu)]), qinv(gauge2[lat.shift(x, mu)])) for (x, mu) in lat.links}
                covariant = covariant and left == right
            ok = counts and rule and involution and to_plaquettes and sides and support and agree and split and covariant
            print("REFLECTION|L=%d|T=%d|kind=%s|total=%d|%s=%d|each_half=%d|expected=%d,%d,%d|rule=%d|involution_on_links=%d|plaquettes_to_plaquettes=%d|mirror_halves=%d|support=%d|a_theta_p_of_theta_U=%d|action_split=%d|gauge_covariant=%d|configurations=%d|ok=%d|json=0" % (
                L, T, kind, len(lat.plaquettes), "crossing" if kind == "link" else "fixed", len(shared), len(upper), want_total, want_shared, want_half,
                1 if rule else 0, 1 if involution else 0, 1 if to_plaquettes else 0, 1 if sides else 0, 1 if support else 0, 1 if agree else 0, 1 if split else 0, 1 if covariant else 0, configurations,
                check("reflection %s on L=%d T=%d" % (kind, L, T), ok)))
        distinct = all(len({l for l, _ in lat.word(p)}) == 4 for p in lat.plaquettes)
        print("EXCLUSIVE_LINK|L=%d|T=%d|plaquettes_with_four_distinct_links=%d|so_E_a_p=0|ok=%d|json=0" % (L, T, sum(1 for p in lat.plaquettes if len({l for l, _ in lat.word(p)}) == 4), check("four distinct links", distinct)))
        section_orientation(lat, L, T)
        # The staggered flip U_mu(x) -> eta_mu(x) U_mu(x), eta_mu(x) = (-1)^(x_0+...+x_(mu-1)).
        stream = Stream(9973 + L + T)
        field = {l: PALETTE[stream.below(len(PALETTE))] for l in lat.links}
        flipped = {(x, mu): (qneg(field[(x, mu)]) if sum(x[:mu]) % 2 else field[(x, mu)]) for (x, mu) in lat.links}
        a, b = traces(lat, field), traces(lat, flipped)
        count = sum(1 for p in lat.plaquettes if b[p] == (-a[p][0], a[p][1]))
        commute = True
        for kind in ("link", "site"):
            R = Reflection(lat, kind)
            one = reflected_field(lat, R, flipped)
            two_base = reflected_field(lat, R, field)
            two = {(x, mu): (qneg(two_base[(x, mu)]) if sum(x[:mu]) % 2 else two_base[(x, mu)]) for (x, mu) in lat.links}
            commute = commute and one == two
        ok = (count == len(lat.plaquettes)) == (L % 2 == 0) and (commute or L % 2 == 1)
        print("STAGGERED_FLIP|L=%d|T=%d|plaquettes_flipped=%d|of=%d|commutes_with_both_reflections=%d|ok=%d|json=0" % (L, T, count, len(lat.plaquettes), 1 if commute else 0, check("staggered flip on L=%d" % L, ok)))


# ---- Part B. Characters of SU(2) as polynomials in the trace.
def multiplicity(n):
    return 1 if SABOTAGE == "wrong_multiplicity" else n + 1


def chi(n, tau):
    prev, cur = 0, 1
    for _ in range(n):
        prev, cur = cur, tau * cur - prev
    return cur


def s3_moment(p):
    """E[(Tr U)^p] under Haar on SU(2), from the S^3 measure: E[a^(2k)] = prod_(i<k) (2i+1)/(2i+4), with Tr U = 2a."""
    if p % 2:
        return 0, 1
    moment = (power(2, p), 1)
    for i in range(p // 2):
        moment = pmul(moment, red(2 * i + 1, 2 * i + 4))
    return moment


def chi_polynomial(n):
    """chi_n as integer coefficients of the powers of the trace."""
    prev, cur = [], [1]
    for _ in range(n):
        nxt = [0] + cur
        for j, v in enumerate(prev):
            nxt[j] -= v
        prev, cur = cur, nxt
    return cur


def l_coefficient(n, k):
    """The coefficient of beta^(2k+n) in l_n(beta), a positive rational."""
    return red(1, power(2, 2 * k + n) * math.factorial(k) * math.factorial(k + n + 1))


def bessel_coefficient(nu, k):
    """The coefficient of beta^k in I_nu(beta)."""
    if k < nu or (k - nu) % 2:
        return 0, 1
    return red(1, power(2, k) * math.factorial((k - nu) // 2) * math.factorial((k + nu) // 2))


def ballot(m, n):
    """E[(Tr U)^m chi_n] under Haar, an integer pair."""
    if m < n or (m - n) % 2:
        return 0, 1
    return red(multiplicity(n) * math.comb(m + 1, (m - n) // 2), m + 1)


def ring(p, q):
    def times(x, y):
        a, b = x
        c, d = y
        return a * c + b * d * q, a * d + b * c + b * d * p
    return times


# Each class is (number of elements, trace). An element (a, b) of a ring means a + b w with w^2 = p w + q.
Z_RING, ROOT2_RING, PHI_RING = ring(0, 0), ring(0, 2), ring(1, 1)
QUADRATURE = {
    "Q8": ("Z", Z_RING, [(1, (2, 0)), (1, (-2, 0)), (6, (0, 0))], 3),
    "2T": ("Z", Z_RING, [(1, (2, 0)), (1, (-2, 0)), (6, (0, 0)), (8, (1, 0)), (8, (-1, 0))], 5),
    "2O": ("Z[sqrt2]", ROOT2_RING, [(1, (2, 0)), (1, (-2, 0)), (18, (0, 0)), (8, (1, 0)), (8, (-1, 0)), (6, (0, 1)), (6, (0, -1))], 7),
    "2I": ("Z[phi]", PHI_RING, [(1, (2, 0)), (1, (-2, 0)), (30, (0, 0)), (20, (1, 0)), (20, (-1, 0)), (12, (0, 1)), (12, (1, -1)), (12, (-1, 1)), (12, (0, -1))], 11),
}


def quadrature_average(name, m, n):
    _, times, classes, _ = QUADRATURE[name]
    order = sum(c for c, _ in classes)
    total = (0, 0)
    for c, x in classes:
        power = (1, 0)
        for _ in range(m):
            power = times(power, x)
        prev, cur = (0, 0), (1, 0)
        for _ in range(n):
            nxt = times(x, cur)
            prev, cur = cur, (nxt[0] - prev[0], nxt[1] - prev[1])
        v = times(power, cur)
        total = (total[0] + c * v[0], total[1] + c * v[1])
    assert total[1] == 0
    return red(total[0], order)


def section_characters():
    """Part B, rows YM4_02C_CHARACTER and YM4_02C_BALLOT."""
    traces_used = (2, 1, 0, -1, -2)
    failures = 0
    for k in range(0, 21):
        for tau in traces_used:
            left = red(power(tau, k), power(2, k) * math.factorial(k))
            right = (0, 1)
            for n in range(k % 2, k + 1, 2):
                j = (k - n) // 2
                right = padd(right, pmul((multiplicity(n) * chi(n, tau), 1), l_coefficient(n, j)))
            failures += 0 if left == right else 1
    print("CHARACTER_SERIES|identity=exp(beta*cos_theta)=sum_n_(n+1)*l_n(beta)*chi_n|orders=0..20|traces=2,1,0,-1,-2|identities=%d|failures=%d|ok=%d|json=0" % (21 * len(traces_used), failures, check("character series through beta^20", failures == 0)))
    # The coefficient of beta^m in (n+1) l_n(beta) by a separate route: E[(tau/2)^m chi_n] / m!, with chi_n a polynomial in the trace and the moments from the S^3 measure.
    moments = [s3_moment(p) for p in range(0, 42)]
    positive, terms, odd_power, same = True, 0, True, True
    for n in range(0, 21):
        polynomial = chi_polynomial(n)
        for m in range(0, 21):
            value = (0, 1)
            for j, v in enumerate(polynomial):
                value = padd(value, pmul((v, 1), moments[m + j]))
            if m >= n and (m - n) % 2 == 0:
                terms += 1
                positive = positive and value[0] > 0
                same = same and pmul(value, red(1, power(2, m) * math.factorial(m))) == pmul((multiplicity(n), 1), l_coefficient(n, (m - n) // 2))
            else:
                odd_power = odd_power and value[0] == 0
    print("L_N_COEFFICIENTS|n=0..20|through_beta^20|terms=%d|route=E[tau^m*chi_n]/(2^m*m!)_from_the_S3_moments|equal_to_the_(n+1)*l_n_formula=%d|all_positive=%d|power_parity_equals_n_parity_so_odd_n_is_negative_at_beta<0=%d|ok=%d|json=0" % (terms, 1 if same else 0, 1 if positive else 0, 1 if odd_power else 0, check("l_n coefficients", same and positive and odd_power and terms == 121)))
    bessel_ok = True
    for n in range(0, 21):
        for k in range(0, 21):
            left = psub(bessel_coefficient(n, k), bessel_coefficient(n + 2, k))
            right = (0, 1)
            if k >= n and (k - n) % 2 == 0:
                right = pmul((multiplicity(n), 1), l_coefficient(n, (k - n) // 2))
            bessel_ok = bessel_ok and left == right
    print("BESSEL|identity=(n+1)*l_n=I_n-I_(n+2)|n=0..20|orders=0..20|ok=%d|json=0" % check("Bessel recurrence", bessel_ok))
    trace_one = True
    for k in range(0, 21):
        total = (0, 1)
        for n in range(k % 2, k + 1, 2):
            total = padd(total, pmul((multiplicity(n) * (n + 1), 1), l_coefficient(n, (k - n) // 2)))
        trace_one = trace_one and total == red(1, math.factorial(k))
    print("KERNEL_TRACE|identity=sum_n_(n+1)^2*l_n(beta)=exp(beta)|orders=0..20|so_trace_of_K_on_one_link=exp(-beta)*exp(beta)=1|ok=%d|json=0" % check("trace of the link kernel", trace_one))
    recursion = True
    for m in range(0, 41):
        for n in range(0, 42):
            right = padd(ballot(m, n - 1) if n else (0, 1), ballot(m, n + 1))
            recursion = recursion and ballot(m + 1, n) == right
    print("BALLOT_RECURSION|identity=tau*chi_n=chi_(n+1)+chi_(n-1)_gives_B(m+1,n)=B(m,n-1)+B(m,n+1)|m=0..40|ok=%d|json=0" % check("ballot recursion", recursion))
    # Haar on SU(2) directly. On S^3, E[a^(2k)] = prod_(i<k) (2i+1)/(2i+4), so E[(Tr U)^(2k)] = 4^k times that, the Catalan number.
    catalan = True
    for k in range(0, 25):
        moment = (power(4, k), 1)
        for i in range(k):
            moment = pmul(moment, red(2 * i + 1, 2 * i + 4))
        catalan = catalan and moment == (math.comb(2 * k, k) // (k + 1), 1)

    def haar_moment(p):
        return (math.comb(p, p // 2) // (p // 2 + 1), 1) if p % 2 == 0 else (0, 1)

    pairs, haar_ok = 0, True
    for m in range(0, 25):
        for n in range(0, 25 - m):
            prev, cur = [], [1]
            for _ in range(n):
                nxt = [0] + cur
                for j, v in enumerate(prev):
                    nxt[j] -= v
                prev, cur = cur, nxt
            total = (0, 1)
            for j, v in enumerate(cur):
                total = padd(total, pmul((v, 1), haar_moment(m + j)))
            haar_ok = haar_ok and total == ballot(m, n)
            pairs += 1
    print("HAAR_MOMENTS|E_trace^(2k)=Catalan_k_from_the_S3_measure=%d|k=0..24|E[(Tr_U)^m*chi_n]=ballot_for_m+n<=24|pairs=%d|ok=%d|json=0" % (1 if catalan else 0, pairs, check("Haar moments against the ballot formula", catalan and haar_ok)))
    for name in QUADRATURE:
        ring_name, _, classes, degree = QUADRATURE[name]
        pairs, ok = 0, True
        for m in range(0, degree + 1):
            for n in range(0, degree + 1 - m):
                ok = ok and quadrature_average(name, m, n) == ballot(m, n)
                pairs += 1
        past = quadrature_average(name, degree + 1, 0)
        haar = ballot(degree + 1, 0)
        print("QUADRATURE|group=%s|order=%d|ring=%s|exact_through_m+n=%d|pairs=%d|E_trace_power_%d=%s|Haar_value=%s|ok=%d|json=0" % (name, sum(c for c, _ in classes), ring_name, degree, pairs, degree + 1, text(past), text(haar), check("quadrature over " + name, ok and past != haar)))


def torus_su2_enclosure(side, time_extent):
    """Z = sum_n (exp(-beta) l_n(beta))^F on the 2D torus at beta = 1, enclosed by exact rationals."""
    faces = side * time_extent
    cut, terms = 12, 12
    low, high = (0, 1), (0, 1)
    for n in range(0, cut + 1):
        s = (0, 1)
        for k in range(0, terms):
            s = padd(s, l_coefficient(n, k))
        # Consecutive terms have ratio at most 1/8 at beta = 1, so the tail is at most twice the first omitted term.
        s_high = padd(s, pmul((2, 1), l_coefficient(n, terms)))
        low = padd(low, (power(s[0], faces), power(s[1], faces)))
        high = padd(high, (power(s_high[0], faces), power(s_high[1], faces)))
    # For n > cut, l_n(1) < 1 and l_n(1) <= 2 (1/2)^n / (n+1)!, whose sum over n > cut is at most 4 (1/2)^(cut+1) / (cut+2)!.
    high = padd(high, red(4, power(2, cut + 1) * math.factorial(cut + 2)))
    e_low, e_high = (0, 1), (0, 1)
    for k in range(0, 40):
        e_low = padd(e_low, red(power(-1, k), math.factorial(k)))
    e_high = padd(e_low, red(1, math.factorial(40)))
    # Partial sums of exp(-1) alternate. The sum through k = 39 lies below and the sum through k = 40 above.
    weight_low = (power(e_low[0], faces), power(e_low[1], faces))
    weight_high = (power(e_high[0], faces), power(e_high[1], faces))
    return faces, pmul(weight_low, low), pmul(weight_high, high), weight_high


def section_torus_su2():
    for side, extent in ((2, 2), (3, 2)):
        faces, z_low, z_high, jensen_high = torus_su2_enclosure(side, extent)
        scale = 10 ** 12
        ok = z_high[0] <= z_high[1] and z_low[0] > 0 and z_low[0] * jensen_high[1] >= jensen_high[0] * z_low[1]
        print("TORUS_SU2_ENCLOSURE|L=%d|T=%d|F=%d|beta=1|Z_times_10^12_low=%d|Z_times_10^12_high=%d|exp(-beta*F)_times_10^12_high=%d|bound_exp(-beta*F)<=Z<=1=%d|ok=%d|json=0" % (
            side, extent, faces, scaled_floor(z_low, scale), scaled_ceiling(z_high, scale), scaled_ceiling(jensen_high, scale), 1 if ok else 0, check("SU(2) torus enclosure", ok)))


def series_product(a, b, degree):
    out = [(0, 1)] * (degree + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= degree and x[0] and y[0]:
                out[i + j] = padd(out[i + j], pmul(x, y))
    return out


def gram_2d_series(degree):
    """The coefficients of (1/2) sum_n (l_n(beta) l_(n+1)(beta))^3 through beta^degree, multiplied out from the l_n series."""
    total = [(0, 1)] * (degree + 1)
    for n in range(0, degree + 1):
        one = [l_coefficient(n, (m - n) // 2) if m >= n and (m - n) % 2 == 0 else (0, 1) for m in range(degree + 1)]
        two = [l_coefficient(n + 1, (m - n - 1) // 2) if m >= n + 1 and (m - n - 1) % 2 == 0 else (0, 1) for m in range(degree + 1)]
        pair = series_product(one, two, degree)
        cube = series_product(series_product(pair, pair, degree), pair, degree)
        total = [padd(x, pmul((1, 2), y)) for x, y in zip(total, cube)]
    return total


def section_su2_red(cylinder):
    """The SU(2) Wilson weight on (Z/3)x(Z/2) with F = a_W: the numerator is (1/2) exp(-6 beta) sum_n (l_n(beta) l_(n+1)(beta))^3, and l_n(-beta) = (-1)^n l_n(beta)."""
    cut, terms = 12, 12
    low, high = [], []
    for n in range(0, cut + 2):
        s = (0, 1)
        for k in range(0, terms):
            s = padd(s, l_coefficient(n, k))
        low.append(s)
        high.append(padd(s, pmul((2, 1), l_coefficient(n, terms))))
    sum_low, sum_high = (0, 1), (0, 1)
    for n in range(0, cut + 1):
        a, b = pmul(low[n], low[n + 1]), pmul(high[n], high[n + 1])
        sum_low = padd(sum_low, (a[0] ** 3, a[1] ** 3))
        sum_high = padd(sum_high, (b[0] ** 3, b[1] ** 3))
    sum_high = padd(sum_high, red(4, power(2, cut + 1) * math.factorial(cut + 2)))
    half_low, half_high = pmul((1, 2), sum_low), pmul((1, 2), sum_high)
    # The same partial sums taken at beta = -1, term by term.
    at_minus = []
    for n in range(0, cut + 2):
        s = (0, 1)
        for k in range(0, terms):
            c = l_coefficient(n, k)
            s = padd(s, (power(-1, 2 * k + n) * c[0], c[1]))
        at_minus.append(s)
    flips = all(at_minus[n] == (power(-1, n) * low[n][0], low[n][1]) for n in range(0, cut + 2))
    cubes = []
    for n in range(0, cut + 1):
        a = pmul(at_minus[n], at_minus[n + 1])
        cubes.append((a[0] ** 3, a[1] ** 3))
    all_negative = all(c[0] < 0 for c in cubes)
    sum_minus = (0, 1)
    for c in cubes:
        sum_minus = padd(sum_minus, c)
    half_minus = pmul((1, 2), sum_minus)
    series = gram_2d_series(9)
    series_text = ",".join(text(v) for v in series)
    leading = series[3]
    doubled = pmul((2, 1), cylinder)
    second_seat_series = "0,0,0,1/128,0,5/1024,0,71/49152,0,133/491520"
    ok = all(v[0] == 0 for v in series[:3]) and leading == doubled and series_text == second_seat_series and sum_low[0] > 0 and flips and all_negative and half_minus == (-half_low[0], half_low[1])
    scale = 10 ** 12
    print("SU2_GRAM_2D|lattice=(Z/3)x(Z/2)|F=a_W|numerator_at_beta=+1_over_exp(-6)_times_10^12_low=%d|high=%d|numerator_at_beta=-1_over_exp(+6)_times_10^12_partial_sum=%d|l_n(-1)=(-1)^n*l_n(1)=%d|every_term_negative_at_beta=-1=%d|series_through_beta^9=%s|beta^3_coefficient=%s|twice_the_cylinder_value=%s|ok=%d|json=0" % (
        scaled_floor(half_low, scale), scaled_ceiling(half_high, scale), scaled_floor(half_minus, scale), 1 if flips else 0, 1 if all_negative else 0, series_text, text(leading), text(doubled), check("SU(2) 2D Gram entry", ok)))


# ---- Finite groups from doubled integer quaternions.
def doubled_product(p, q):
    a, b, c, d = p
    e, f, g, h = q
    r = (a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e)
    assert all(v % 2 == 0 for v in r)
    return tuple(v // 2 for v in r)


class Group:
    def __init__(self, elements):
        self.elements = elements
        self.order = len(elements)
        index = {e: i for i, e in enumerate(elements)}
        self.index = index
        self.mult = [[index[doubled_product(x, y)] for y in elements] for x in elements]
        self.inv = [index[(e[0], -e[1], -e[2], -e[3])] for e in elements]
        self.trace = [e[0] for e in elements]
        self.one = index[(2, 0, 0, 0)]
        self.cls = [-1] * self.order
        self.classes = []
        for g in range(self.order):
            if self.cls[g] < 0:
                members = sorted({self.mult[self.mult[h][g]][self.inv[h]] for h in range(self.order)})
                for m in members:
                    self.cls[m] = len(self.classes)
                self.classes.append(members)
        self.nclasses = len(self.classes)


Q8_ELEMENTS = [tuple(2 * s if i == j else 0 for i in range(4)) for j in range(4) for s in (1, -1)]
T2_ELEMENTS = Q8_ELEMENTS + list(itertools.product((1, -1), repeat=4))
Q8 = Group(Q8_ELEMENTS)
T2 = Group(T2_ELEMENTS)


def q8_characters():
    """Trivial, the three signs and the two-dimensional character, each a list over the conjugacy classes."""
    table = []
    for rho in range(5):
        row = []
        for members in Q8.classes:
            e = Q8.elements[members[0]]
            if rho == 0:
                row.append(1)
            elif rho == 4:
                row.append(e[0])
            else:
                row.append(1 if (e[0] != 0 or e[rho] != 0) else -1)
        table.append(row)
    return table


Q8_CHI = q8_characters()
Q8_DIM = [1, 1, 1, 1, 2]
E_INDEX = 4


def q8_weight(c):
    return [sum(c[rho] * Q8_CHI[rho][k] for rho in range(5)) for k in range(Q8.nclasses)]


def q8_orthonormal():
    return all(sum(len(Q8.classes[k]) * Q8_CHI[a][k] * Q8_CHI[b][k] for k in range(5)) == (8 if a == b else 0) for a in range(5) for b in range(5))


# Z[omega] with omega^2 = -1 - omega. An element is (a, b) = a + b omega.
EISENSTEIN = ring(-1, -1)


def econj(x):
    return x[0] - x[1], -x[1]


def t2_characters():
    """The seven irreducible characters of 2T from exact traces: 1, w, w^2, 3, 2, 2w, 2w^2, with lambda: 2T -> Z/3 trivial on Q8."""
    e = T2.index[(1, 1, 1, 1)]
    q8 = set(range(8))
    coset = [0] * 24
    e2 = T2.mult[e][e]
    for g in range(24):
        if g in q8:
            coset[g] = 0
        elif T2.mult[T2.inv[e]][g] in q8:
            coset[g] = 1
        else:
            assert T2.mult[T2.inv[e2]][g] in q8
            coset[g] = 2
    assert all(coset[T2.mult[a][b]] == (coset[a] + coset[b]) % 3 for a in range(24) for b in range(24))
    powers = [(1, 0), (0, 1), (-1, -1)]
    table = []
    for shape in ("1", "w", "w2", "3", "2", "2w", "2w2"):
        row = []
        for members in T2.classes:
            g = members[0]
            tau = T2.trace[g]
            lam = powers[coset[g]]
            lam2 = powers[(2 * coset[g]) % 3]
            row.append({"1": (1, 0), "w": lam, "w2": lam2, "3": (tau * tau - 1, 0), "2": (tau, 0),
                        "2w": (tau * lam[0], tau * lam[1]), "2w2": (tau * lam2[0], tau * lam2[1])}[shape])
        table.append(row)
    return table


T2_CHI = t2_characters()
T2_DIM = [1, 1, 1, 3, 2, 2, 2]


def t2_orthonormal():
    for a in range(7):
        for b in range(7):
            total = (0, 0)
            for k in range(T2.nclasses):
                v = EISENSTEIN(T2_CHI[a][k], econj(T2_CHI[b][k]))
                total = (total[0] + len(T2.classes[k]) * v[0], total[1] + len(T2.classes[k]) * v[1])
            if total != ((24, 0) if a == b else (0, 0)):
                return False
    return True


# ---- The one walker. Counts of tuples of conjugacy classes of the given words over all assignments of the free links.
def class_histogram(lat, group, words, fix_forest=True):
    """Each word is a tuple of (link, sign). With fix_forest a spanning forest of the used links is set to the identity, which needs gauge-invariant class data. Returns (histogram over tuples of classes, number of free links)."""
    links = sorted({l for w in words for l, _ in w})
    forest = set()
    if fix_forest:
        parent = {}

        def find(v):
            parent.setdefault(v, v)
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for l in links:
            a, b = find(l[0]), find(lat.shift(l[0], l[1]))
            if a != b:
                parent[a] = b
                forest.add(l)
    free = []
    for w in words:
        for l, _ in w:
            if l not in forest and l not in free:
                free.append(l)
    position = {l: i for i, l in enumerate(free)}
    size, mult, inv, cls, one, base = group.order, group.mult, group.inv, group.cls, group.one, group.nclasses
    values, inverses = [one] * len(free), [one] * len(free)
    compiled = [[(values if s > 0 else inverses, position[l]) for l, s in w if l in position] for w in words]
    n = len(free)
    due = [[] for _ in range(n)]
    order, key0 = [], 0
    for i, c in enumerate(compiled):
        if not c:
            order.append(i)
            key0 = key0 * base + cls[one]
    for depth in range(n):
        for i, c in enumerate(compiled):
            if c and max(p for _, p in c) == depth:
                order.append(i)
                due[depth].append(c)
    counts = collections.defaultdict(int)
    last = n - 1

    def walk(depth, key):
        here = due[depth]
        for g in range(size):
            values[depth] = g
            inverses[depth] = inv[g]
            k = key
            for word in here:
                h = one
                for array, slot in word:
                    h = mult[h][array[slot]]
                k = k * base + cls[h]
            if depth == last:
                counts[k] += 1
            else:
                walk(depth + 1, k)
    if n:
        walk(0, key0)
    else:
        counts[key0] += 1
    hist = {}
    for k, count in counts.items():
        digits = [0] * len(words)
        for i in reversed(order):
            digits[i] = k % base
            k //= base
        hist[tuple(digits)] = count
    return hist, n


def sum_over_weight(hist, weight, slots=None):
    """The exact sum of count * product of weight[class] over the given word slots, an integer."""
    total = 0
    for key, count in hist.items():
        term = count
        for i in (range(len(key)) if slots is None else slots):
            term *= weight[key[i]]
        total += term
    return total


def section_cylinder():
    """Part C, row YM4_02C_CYLINDER."""
    lat = Lattice(3, 3, 3, 4)
    R = Reflection(lat, "link")

    def line(t):
        return tuple((((k, 0, 0, t), 0), 1) for k in range(3))
    w_up = line(0)
    w_down = line(3)
    sides = [lat.word(((k, 0, 0, 3), 0, 3)) for k in range(3)]
    mirror_ok = R.word(w_up) == w_down
    words = [w_up, w_down] + sides
    used = sorted({l for w in words for l, _ in w})
    degree = collections.Counter(l for w in words for l, _ in w)
    sites = {x for l in used for x in (l[0], lat.shift(l[0], l[1]))}

    def value(group, chosen):
        hist, free = class_histogram(lat, group, chosen)
        trace = [group.trace[members[0]] for members in group.classes]
        return red(sum_over_weight(hist, trace), power(2, len(chosen)) * power(group.order, free)), free
    q8_value, free = value(Q8, words)
    t2_value, _ = value(T2, words)
    zero_two = value(Q8, [w_up, w_down])[0]
    zero_four = value(Q8, [w_up, w_down] + sides[:2])[0]
    w_links = {l for l, _ in w_up} | {l for l, _ in w_down}
    per_plaquette = {p: sum(1 for l, _ in lat.word(p) if l in w_links) for p in lat.plaquettes}
    most = max(per_plaquette.values())
    two = sorted(p for p, v in per_plaquette.items() if v == 2)
    only_sides = two == sorted(((k, 0, 0, 3), 0, 3) for k in range(3))
    ok = (q8_value == (1, 256) and t2_value == (1, 256) and mirror_ok and max(degree.values()) == 2 and zero_two == (0, 1) and zero_four == (0, 1)
          and most == 2 and only_sides and len(used) == 9 and len(sites) == 6)
    print("CYLINDER|lattice=(Z/3)^3x(Z/4)|links=%d|sites=%d|free=%d|max_degree_per_link=%d|mirror_of_W_is_W_at_t=-1=%d|Q8=%s|2T=%s|expected=1/256|without_the_sides=%s|with_two_sides=%s|max_W_links_per_plaquette=%d|plaquettes_with_two_W_links=%d|these_are_the_three_sides=%d|so_lower_orders_vanish_and_the_beta^3_coefficient=%s|ok=%d|json=0" % (
        len(used), len(sites), free, max(degree.values()), 1 if mirror_ok else 0, text(q8_value), text(t2_value), text(zero_two), text(zero_four), most, len(two), 1 if only_sides else 0, text(q8_value), check("cylinder", ok)))
    return q8_value


def section_torus(q8_32_hist):
    """Part D, row YM4_02C_TORUS_2D."""
    print("CHARACTER_TABLE|group=Q8|irreps=5|dims=1,1,1,1,2|orthonormal=%d|ok=%d|json=0" % (1 if q8_orthonormal() else 0, check("Q8 characters", q8_orthonormal())))
    ok = t2_orthonormal() and sum(d * d for d in T2_DIM) == 24 and T2.nclasses == 7
    print("CHARACTER_TABLE|group=2T|irreps=7|classes=%d|dims=1,1,1,3,2,2,2|from=exact_traces_and_the_map_2T_to_Z/3|ring=Z[omega]|orthonormal=%d|ok=%d|json=0" % (T2.nclasses, 1 if t2_orthonormal() else 0, check("2T characters", ok)))
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        weight = q8_weight(c)
        for side, extent in ((2, 2), (3, 2)):
            lat = Lattice(side, extent)
            words = [lat.word(p) for p in lat.plaquettes]
            if (side, extent) == (3, 2):
                hist, free = q8_32_hist, 7
                slots = list(range(2, 8))
            else:
                hist, free = class_histogram(lat, Q8, words)
                slots = None
            faces = side * extent
            direct = red(sum_over_weight(hist, weight, slots), power(8, free))
            rule = (0, 1)
            for rho in range(5):
                rule = padd(rule, red(power(c[rho], faces), power(Q8_DIM[rho], faces)))
            print("TORUS_2D|group=Q8|L=%d|T=%d|F=%d|c=%s|w_on_classes=%s|assignments=%d|Z_direct=%s|Z_rule=%s|ok=%d|json=0" % (
                side, extent, faces, ",".join(map(str, c)), ",".join(map(str, weight)), power(8, free), text(direct), text(rule), check("torus Q8 L=%d T=%d" % (side, extent), direct == rule)))
    # 2T with a complex weight: the integers differ between w and w^2, so w(g) has an imaginary part. Each link appears once forward and once backward.
    c = (7, 2, 1, 4, 3, 1, 2)
    weight = []
    for k in range(T2.nclasses):
        total = (0, 0)
        for rho in range(7):
            total = (total[0] + c[rho] * T2_CHI[rho][k][0], total[1] + c[rho] * T2_CHI[rho][k][1])
        weight.append(total)
    lat = Lattice(2, 2)
    words = [lat.word(p) for p in lat.plaquettes]
    hist, free = class_histogram(lat, T2, words)
    total = (0, 0)
    for key, count in hist.items():
        term = (count, 0)
        for k in key:
            term = EISENSTEIN(term, weight[k])
        total = (total[0] + term[0], total[1] + term[1])
    direct = red(total[0], power(24, free))
    rule = (0, 1)
    for rho in range(7):
        rule = padd(rule, red(c[rho] ** 4, T2_DIM[rho] ** 4))
    ok = total[1] == 0 and direct == rule
    print("TORUS_2D|group=2T|L=2|T=2|F=4|c_on_1,w,w2,3,2,2w,2w2=%s|weight_is_complex=%d|assignments=%d|imaginary_part=%d|Z_direct=%s|Z_rule=%s|ok=%d|json=0" % (
        ",".join(map(str, c)), 1 if any(v[1] for v in weight) else 0, power(24, free), total[1], text(direct), text(rule), check("torus 2T", ok)))


def gram_pass():
    """One pass over the 8^7 gauge-fixed assignments of (Z/3)x(Z/2), every weight afterwards from the histogram."""
    lat = Lattice(3, 2)

    def line(t):
        return tuple((((k, t), 0), 1) for k in range(3))
    words = [line(0), line(1)] + [lat.word(p) for p in lat.plaquettes]
    hist, free = class_histogram(lat, Q8, words)
    assert free == 7 and sum(hist.values()) == 8 ** 7
    return lat, hist


def gram_link_matrix(hist, weight):
    """Link reflection over the five characters of W, the holonomy of the t=0 slice. The mirror of W is the holonomy of the t=1 slice. Numerators over 8^7."""
    reduced = collections.defaultdict(int)
    for key, count in hist.items():
        term = count
        for k in key[2:]:
            term *= weight[k]
        reduced[(key[0], key[1])] += term
    return [[sum(v * Q8_CHI[a][w1] * Q8_CHI[b][w0] for (w0, w1), v in reduced.items()) for b in range(5)] for a in range(5)]


def site_family(w0, w1, pa, pb):
    e, s = Q8_CHI[E_INDEX], Q8_CHI[1]
    return (1, Q8_CHI[1][w0], Q8_CHI[2][w0], Q8_CHI[3][w0], e[w0], Q8_CHI[1][w1], Q8_CHI[2][w1], Q8_CHI[3][w1], e[w1], e[w0] * e[w1],
            e[pa], e[pa] * e[pb], e[w0] * e[pa], s[pa], e[pa] * s[w1])


def gram_site_matrix(lat, hist, weight):
    """Site reflection on (Z/3)x(Z/2). Both slices are fixed and the plaquettes at t=0 and t=1 are mirror images. Numerators over 8^7."""
    R = Reflection(lat, "site")
    slot = {p: i + 2 for i, p in enumerate(lat.plaquettes)}
    pa, pb = lat.plaquettes[0], lat.plaquettes[2]
    assert pa == ((0, 0), 0, 1) and pb == ((1, 0), 0, 1)
    ia, ib, ja, jb = slot[pa], slot[pb], slot[R.plaquette(pa)], slot[R.plaquette(pb)]
    reduced = collections.defaultdict(int)
    for key, count in hist.items():
        term = count
        for k in key[2:]:
            term *= weight[k]
        reduced[(site_family(key[0], key[1], key[ja], key[jb]), site_family(key[0], key[1], key[ia], key[ib]))] += term
    size = len(site_family(0, 0, 0, 0))
    matrix = [[0] * size for _ in range(size)]
    for (left, right), v in reduced.items():
        for a in range(size):
            if left[a]:
                row, x = matrix[a], v * left[a]
                for b in range(size):
                    row[b] += x * right[b]
    return matrix


def section_gram(lat, hist):
    """Part E, rows YM4_02C_GRAM_LINK, YM4_02C_GRAM_LINK_RED and YM4_02C_GRAM_SITE."""
    R_link, R_site = Reflection(lat, "link"), Reflection(lat, "site")

    def line(t):
        return tuple((((k, t), 0), 1) for k in range(3))
    mirror_ok = R_link.word(line(0)) == line(1) and R_site.word(line(0)) == line(0) and R_site.word(line(1)) == line(1)
    check("the mirror of W", mirror_ok)
    denominator = 8 ** 7
    declared = (8, 3, 3, 3, 1)
    if SABOTAGE == "negative_weight_called_positive":
        declared = (8, 3, 3, 3, -1)
    for c, want, want_psd, tag in ((declared, (593, 4), True, "GRAM_LINK"), ((8, 3, 3, 3, -1), (-593, 4), False, "GRAM_LINK_RED")):
        weight = q8_weight(c)
        matrix = gram_link_matrix(hist, weight)
        t = [red(c[rho] ** 3, Q8_DIM[rho] ** 3) for rho in range(5)]
        rule = pmul(pmul((2, 1), t[4]), padd(t[0], padd(t[1], padd(t[2], t[3]))))
        entry = red(matrix[E_INDEX][E_INDEX], denominator)
        psd, rank, reason = psd_exact(matrix)
        minors = all_principal_minors_nonnegative(matrix)
        ok = entry == want and rule == want and psd == want_psd and minors == want_psd and min(weight) > 0
        print("%s|lattice=(Z/3)x(Z/2)|group=Q8|c=%s|w_on_classes=%s|pointwise_positive=%d|assignments=%d|F=chi_2dim(W)|G_FF=%s|expected=%s|rule_2*t_2dim*(t_0+3*t_s)=%s|family=five_characters_of_W|PSD=%d|rank=%d|reason=%s|all_principal_minors_nonnegative=%d|Z=%s|ok=%d|json=0" % (
            tag, ",".join(map(str, c)), ",".join(map(str, weight)), 1 if min(weight) > 0 else 0, denominator, text(entry), text(want), text(rule), 1 if psd else 0, rank, reason, 1 if minors else 0, text(red(matrix[0][0], denominator)), check(tag, ok)))
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        weight = q8_weight(c)
        matrix = gram_site_matrix(lat, hist, weight)
        psd, rank, reason = psd_exact(matrix)
        print("GRAM_SITE|lattice=(Z/3)x(Z/2)|group=Q8|c=%s|family_size=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (",".join(map(str, c)), len(matrix), 1 if psd else 0, rank, reason, check("site Gram c=%s" % (c,), psd and rank == 15)))
    # This lattice has no plaquette inside a fixed slice, so the site theorem covers a weight of either sign.
    signed = [3, -2, 1, -1, 2]
    matrix = gram_site_matrix(lat, hist, signed)
    psd, rank, reason = psd_exact(matrix)
    in_fixed_slices = len(partition(lat, "site")[1])
    print("GRAM_SITE|lattice=(Z/3)x(Z/2)|group=Q8|weight_values_on_classes=3,-2,1,-1,2|plaquettes_in_the_fixed_slices=%d|family_size=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (in_fixed_slices, len(matrix), 1 if psd else 0, rank, reason, check("site Gram signed weight", psd and in_fixed_slices == 0 and rank == 15)))


def section_gram_t4():
    """Link reflection at T = 4, where the two planes act on different slices. Lattice (Z/1)x(Z/4), Q8."""
    lat = Lattice(1, 4)
    R = Reflection(lat, "link")
    loop = [(((0, t), 0), 1) for t in range(4)]
    plaq = [lat.word(((0, t), 0, 1)) for t in range(4)]
    words = [(letter,) for letter in loop] + plaq
    hist, free = class_histogram(lat, Q8, words)
    check("mirror of the slice links at T=4", R.link(((0, 0), 0))[0] == ((0, 3), 0) and R.link(((0, 1), 0))[0] == ((0, 2), 0) and R.plaquette(((0, 0), 0, 1)) == ((0, 2), 0, 1))
    e = Q8_CHI[E_INDEX]

    def family(a, b, p):
        return tuple(Q8_CHI[rho][a] for rho in range(5)) + (e[b], e[a] * e[b], e[p], e[p] * e[a])
    denominator = power(8, free)
    for c, want, want_psd in (((8, 3, 3, 3, 1), (2389, 8), True), ((8, 3, 3, 3, -1), (-2389, 8), False)):
        weight = q8_weight(c)
        reduced = collections.defaultdict(int)
        for key, count in hist.items():
            term = count
            for k in key[4:]:
                term *= weight[k]
            # Slots: U(0), U(1), U(2), U(3), then p(0), p(1), p(2), p(3). The mirror of (U(0), U(1), p(0)) is (U(3), U(2), p(2)).
            reduced[(family(key[3], key[2], key[6]), family(key[0], key[1], key[4]))] += term
        size = len(family(0, 0, 0))
        matrix = [[sum(v * left[a] * right[b] for (left, right), v in reduced.items()) for b in range(size)] for a in range(size)]
        entry = red(matrix[E_INDEX][E_INDEX], denominator)
        psd, rank, reason = psd_exact(matrix)
        print("GRAM_LINK_T4|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|assignments=%d|F=chi_2dim(U(0))|G_FF=%s|expected_t_E^3*(t_0+3*t_s)+t_E*(t_0^3+3*t_s^3)=%s|family_size=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), denominator, text(entry), text(want), size, 1 if psd else 0, rank, reason, check("link Gram at T=4 c=%s" % (c,), entry == want and psd == want_psd)))


def section_every_function():
    """Every function on the slice, including those that move under gauge transformations. At T = 2 the open half is the slice t=0, so its point functions span all F."""
    for side in (1, 2):
        lat = Lattice(side, 2)
        slice_configs = list(itertools.product(range(8), repeat=side))
        gauges = list(itertools.product(range(8), repeat=side))
        mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
        # Direct from the plaquette words. Plane t=1 to t=0 sums the links V(x,1), plane t=0 to t=1 the links V(x,0).
        counts = {}
        for b in slice_configs:
            for a in slice_configs:
                pair = {}
                for plane in (0, 1):
                    words = [lat.word(((x, plane), 0, 1)) for x in range(side)]
                    tally = collections.defaultdict(int)
                    for v in gauges:
                        value = {}
                        for x in range(side):
                            value[((x, 0), 0)] = a[x]
                            value[((x, 1), 0)] = b[x]
                            value[((x, plane), 1)] = v[x]
                        key = []
                        for word in words:
                            h = Q8.one
                            for l, s in word:
                                h = mult[h][value[l] if s > 0 else inv[value[l]]]
                            key.append(cls[h])
                        tally[tuple(key)] += 1
                    pair[plane] = tally
                counts[(b, a)] = pair
        for c, want_psd in (((8, 3, 3, 3, 1), True), ((8, 3, 3, 3, -1), side % 2 == 0)):
            weight = q8_weight(c)
            kernel = {}
            for (b, a), pair in counts.items():
                value = 1
                for plane in (0, 1):
                    subtotal = 0
                    for key, n in pair[plane].items():
                        term = n
                        for k in key:
                            term *= weight[k]
                        subtotal += term
                    value *= subtotal
                if SABOTAGE == "every_function_one_plane":
                    value = subtotal
                kernel[(b, a)] = value
            matrix = [[kernel[(b, a)] for a in slice_configs] for b in slice_configs]
            psd, rank, reason = psd_exact(matrix)
            blind = True
            for b in slice_configs:
                for a in slice_configs:
                    for g in gauges:
                        moved = tuple(mult[mult[g[x]][a[x]]][inv[g[(x + 1) % side]]] for x in range(side))
                        blind = blind and kernel[(b, moved)] == kernel[(b, a)]
            # The sum of all entries is 8^links Z, and the entry at (1, 1) is a square of one plane's sum, each from the rule alone.
            total = sum(kernel.values())
            rule = (0, 1)
            for rho in range(5):
                rule = padd(rule, red(power(c[rho], 2 * side), power(Q8_DIM[rho], 2 * side)))
            want_total = pmul((power(8, 4 * side), 1), rule)
            entry = kernel[((Q8.one,) * side, (Q8.one,) * side)]
            want_entry = (8 * weight[cls[Q8.one]]) ** 2 if side == 1 else (8 * sum(weight[cls[g]] ** 2 for g in range(8))) ** 2
            ok = psd == want_psd and blind and (not psd or rank == 5) and (total, 1) == want_total and entry == want_entry
            print("EVERY_FUNCTION|lattice=(Z/%d)x(Z/2)|group=Q8|c=%s|family=all_%d_point_functions_of_the_t=0_slice|PSD=%d|rank=%d|reason=%s|kernel_blind_to_gauge_moves_of_either_slice=%d|sum_of_all_entries=%d|expected_8^links*Z=%s|entry_at_(1,1)=%d|expected=%d|ok=%d|json=0" % (
                side, ",".join(map(str, c)), len(slice_configs), 1 if psd else 0, rank, reason, 1 if blind else 0, total, text(want_total), entry, want_entry, check("every function on L=%d c=%s" % (side, c), ok)))


def section_every_function_t4_and_site():
    """Exhaustive small cases at T = 4 and for site reflection, each entry from the plaquette words."""
    lat = Lattice(1, 4)
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    elements = range(8)

    def plaquette_class(t, lower, upper, v):
        value = {((0, t), 0): lower, ((0, (t + 1) % 4), 0): upper, ((0, t), 1): v}
        h = Q8.one
        for l, s in lat.word(((0, t), 0, 1)):
            h = mult[h][value[l] if s > 0 else inv[value[l]]]
        return cls[h]
    classes = {t: [[[plaquette_class(t, a, b, v) for v in elements] for b in elements] for a in elements] for t in range(4)}
    for c, want_psd in (((8, 3, 3, 3, 1), True), ((8, 3, 3, 3, -1), False)):
        weight = q8_weight(c)
        strip = {t: [[sum(weight[k] for k in classes[t][a][b]) for b in elements] for a in elements] for t in range(4)}
        pairs = list(itertools.product(elements, repeat=2))
        # F runs over the point functions of (U(0), U(1)). Its mirror depends on (U(3), U(2)). Every V(t) sums over its own plaquette.
        matrix = [[strip[0][a][b] * strip[1][b][b2] * strip[2][b2][a2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]
        if SABOTAGE == "t4_half_weights_dropped":
            matrix = [[strip[1][b][b2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]
        psd, rank, reason = psd_exact(matrix)
        total = sum(sum(row) for row in matrix)
        rule = (0, 1)
        for rho in range(5):
            rule = padd(rule, red(power(c[rho], 4), power(Q8_DIM[rho], 4)))
        want_total = pmul((8 ** 8, 1), rule)
        entry = matrix[0][0]
        want_entry = (8 * weight[cls[Q8.one]]) ** 4
        ok = psd == want_psd and (not want_psd or rank == 25) and pairs[0] == (Q8.one, Q8.one) and (total, 1) == want_total and entry == want_entry
        print("EVERY_FUNCTION_T4|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|family=all_64_point_functions_of_(U(0),U(1))|PSD=%d|rank=%d|reason=%s|sum_of_all_entries=%d|expected_8^links*Z=%s|entry_at_all_1=%d|expected=%d|ok=%d|json=0" % (
            ",".join(map(str, c)), 1 if psd else 0, rank, reason, total, text(want_total), entry, want_entry, check("every function at T=4 c=%s" % (c,), ok)))
    # Site reflection on (Z/1)x(Z/2): F on the closed half (U(0), U(1), V(0)), weight of either sign. The form splits into one block per fixed-slice value, each of rank one.
    lat2 = Lattice(1, 2)
    R = Reflection(lat2, "site")
    fixed_ok = R.link(((0, 0), 0)) == (((0, 0), 0), 1) and R.link(((0, 1), 0)) == (((0, 1), 0), 1) and R.link(((0, 0), 1)) == (((0, 1), 1), -1)

    def site_class(t, a, b, v):
        value = {((0, 0), 0): a, ((0, 1), 0): b, ((0, t), 1): v}
        h = Q8.one
        for l, s in lat2.word(((0, t), 0, 1)):
            h = mult[h][value[l] if s > 0 else inv[value[l]]]
        return cls[h]
    signed = [3, -2, 1, -1, 2]
    blocks, all_psd, top_rank = 0, True, 0
    for a in elements:
        for b in elements:
            # F(U) = delta(V(0) = v). Then F(theta U) = delta(V(1)^-1 = v2), so V(1) = v2^-1 in the lower plaquette.
            block = [[signed[site_class(1, a, b, inv[v2])] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]
            psd, rank, _ = psd_exact(block)
            all_psd = all_psd and psd
            top_rank = max(top_rank, rank)
            blocks += 1
    print("EVERY_FUNCTION_SITE|lattice=(Z/1)x(Z/2)|group=Q8|weight_values_on_classes=3,-2,1,-1,2|family=all_512_point_functions_of_(U(0),U(1),V(0))|blocks=%d|every_block_PSD=%d|largest_block_rank=%d|ok=%d|json=0" % (
        blocks, 1 if all_psd else 0, top_rank, check("every function for site reflection", fixed_ok and all_psd and top_rank == 1)))


def section_signed_site():
    """Part G, rows YM4_02C_SIGNED_SITE and YM4_02C_SIGNED_SITE_CONTROL, from every one of the 8^6 assignments."""
    lat = Lattice(1, 1, 2)
    R = Reflection(lat, "site")
    index = {l: i for i, l in enumerate(lat.links)}
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    n = len(lat.links)
    compiled = {p: tuple((index[l], s) for l, s in lat.word(p)) for p in lat.plaquettes}
    spatial = [((0, 0, t), 0, 1) for t in (0, 1)]
    timelike = [p for p in lat.plaquettes if p[2] == lat.time]
    check_fixed = all(R.plaquette(p) == p for p in spatial)
    theta = [(index[R.link(l)[0]], R.link(l)[1]) for l in lat.links]
    plus_class, minus_class = cls[Q8.index[(2, 0, 0, 0)]], cls[Q8.index[(-2, 0, 0, 0)]]
    i_element = Q8.index[(0, 2, 0, 0)]
    j_element = Q8.index[(0, 0, 2, 0)]
    e_chi = Q8_CHI[E_INDEX]
    u00, u10, u01, u11, v0 = (index[((0, 0, 0), 0)], index[((0, 0, 0), 1)], index[((0, 0, 1), 0)], index[((0, 0, 1), 1)], index[((0, 0, 0), 2)])

    def evaluate(word, config):
        h = Q8.one
        for i, s in word:
            h = mult[h][config[i] if s > 0 else inv[config[i]]]
        return h

    def family(config):
        s0 = cls[evaluate(compiled[spatial[0]], config)]
        s1 = cls[evaluate(compiled[spatial[1]], config)]
        side = cls[evaluate(compiled[((0, 0, 0), 0, 2)], config)]
        a = e_chi[cls[config[u00]]]
        return (1, 1 if s0 == minus_class else 0, 1 if s1 == minus_class else 0, 1 if (s0 == minus_class and s1 == plus_class) else 0,
                a, a * e_chi[cls[config[u01]]], 1 if config[u10] == i_element else 0,
                e_chi[cls[config[v0]]], 1 if config[v0] == j_element else 0, e_chi[side])
    fixed_size, closed_size = 7, 10
    table = {}
    hist = collections.defaultdict(int)
    only_signs = True
    for config in itertools.product(range(8), repeat=n):
        s0 = cls[evaluate(compiled[spatial[0]], config)]
        s1 = cls[evaluate(compiled[spatial[1]], config)]
        only_signs = only_signs and s0 in (plus_class, minus_class) and s1 in (plus_class, minus_class)
        sides = tuple(cls[evaluate(compiled[p], config)] for p in timelike)
        mirrored = tuple(config[i] if s > 0 else inv[config[i]] for i, s in theta)
        up_key = (config[u00], config[u10], config[u01], config[u11], config[v0])
        down_key = (mirrored[u00], mirrored[u10], mirrored[u01], mirrored[u11], mirrored[v0])
        if up_key not in table:
            table[up_key] = family(config)
        if down_key not in table:
            table[down_key] = family(mirrored)
        hist[(s0, s1, sides, table[down_key], table[up_key])] += 1

    def gram(fixed_weight, time_weight, size):
        matrix = [[0] * size for _ in range(size)]
        for (s0, s1, sides, left, right), count in hist.items():
            term = count * fixed_weight[s0] * fixed_weight[s1]
            for k in sides:
                term *= time_weight[k]
            for a in range(size):
                if left[a]:
                    row, x = matrix[a], term * left[a]
                    for b in range(size):
                        row[b] += x * right[b]
        return matrix
    denominator = power(8, n)
    time_flat = [1] * Q8.nclasses
    F_slot = 3

    def by_sign(plus, minus):
        table_weight = [0] * Q8.nclasses
        table_weight[plus_class], table_weight[minus_class] = plus, minus
        return table_weight
    signs_ok = check_fixed and only_signs
    check("fixed-slice plaquettes are commutators fixed by the reflection", signs_ok)
    commutators = collections.Counter(Q8.mult[Q8.mult[Q8.mult[a][b]][inv[a]]][inv[b]] for a in range(8) for b in range(8))
    plus_count, minus_count = commutators[Q8.index[(2, 0, 0, 0)]], commutators[Q8.index[(-2, 0, 0, 0)]]
    expected_a = red(plus_count - minus_count, 64)
    # Haar: integrating U gives (Tr V)^2 / 2 for Tr(U V U^-1 V^-1), so E[a_s] = E[(Tr V)^2] / 4.
    haar_a = pmul((1, 4), ballot(2, 0))
    print("COMMUTATOR|group=Q8|pairs=64|value_+1=%d|value_-1=%d|P(s=-1)=%s|expected=3/8|E_a_s=%s|Haar_E_a_s=%s|ok=%d|json=0" % (
        plus_count, minus_count, text(red(minus_count, 64)), text(expected_a), text(haar_a), check("commutator law", plus_count == 40 and minus_count == 24 and expected_a == haar_a)))
    matrix = gram(by_sign(1, -1), time_flat, fixed_size)
    numerator, z = red(matrix[F_slot][F_slot], denominator), red(matrix[0][0], denominator)
    psd, rank, reason = psd_exact(matrix)
    ok = numerator == (-15, 64) and z == (1, 16) and not psd
    print("SIGNED_SITE|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|assignments=%d|time_like_weight=1|fixed_slice_weight_plus1=1|fixed_slice_weight_minus1=-1|F=indicator_of_s0=-1_and_s1=+1|numerator=%s|expected=-15/64|Z=%s|expected_Z=1/16|Gram_PSD=%d|reason=%s|ok=%d|json=0" % (
        denominator, text(numerator), text(z), 1 if psd else 0, reason, check("signed site weight goes red", ok)))
    declared = by_sign(1, -1) if SABOTAGE == "signed_site_weight_called_positive" else by_sign(3, 1)
    matrix = gram(declared, time_flat, fixed_size)
    numerator, z = red(matrix[F_slot][F_slot], denominator), red(matrix[0][0], denominator)
    psd, rank, reason = psd_exact(matrix)
    ok = numerator == (45, 64) and z == (81, 16) and psd
    print("SIGNED_SITE_CONTROL|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|time_like_weight=1|fixed_slice_weight_plus1=%d|fixed_slice_weight_minus1=%d|numerator=%s|expected=45/64|Z=%s|expected_Z=81/16|family=functions_of_the_fixed_slice_links_size_%d|Gram_PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
        declared[plus_class], declared[minus_class], text(numerator), text(z), fixed_size, 1 if psd else 0, rank, reason, check("positive site weight control", ok)))
    # Theorem 2 with plaquette-dependent weights: a signed weight on the time-like plaquettes with a positive one on the fixed slices, and F on the closed half, moved by gauge transformations or not.
    matrix = gram(by_sign(3, 1), [3, -2, 1, -1, 2], closed_size)
    psd, rank, reason = psd_exact(matrix)
    print("SIGNED_OPEN_HALF|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|fixed_slice_weight=3,1|time_like_weight_values_on_classes=3,-2,1,-1,2|family=functions_on_the_closed_half_size_%d|Gram_PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
        closed_size, 1 if psd else 0, rank, reason, check("signed weight on the open half stays PSD", psd and rank == 9)))


def section_w_plus_control():
    """The clause of Theorem 2, at which W_plus(C, .) is not almost everywhere zero. On (Z/1)x(Z/1)x(Z/2) with Q8 the fixed slices carry the values 1, -1 on +1, -1, and two time-like weights run side by side: 1 everywhere, and 1 on +1, -1 with 0 elsewhere. f(C) < 0 on the same C for both. With the second weight W_plus vanishes at each of those C, and every Gram block stays PSD. Point functions of V(0) at each C, from the plaquette words, with the mirror from Reflection.link. N(delta_C) over 8^6."""
    lat = Lattice(1, 1, 2)
    R = Reflection(lat, "site")
    upper, shared, lower = partition(lat, "site")
    words_upper, words_shared, words_lower = [lat.word(p) for p in upper], [lat.word(p) for p in shared], [lat.word(p) for p in lower]
    time_zero = ((0, 0, 0), 2)
    time_one, sign = R.link(time_zero)
    mirror_ok = time_one == ((0, 0, 1), 2) and sign == -1
    if time_one != ((0, 0, 1), 2):
        print("W_PLUS_CONTROL|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|mirror_of_V(0)_lies_on_the_slice_t=1=0|ok=%d|json=0" % check("W_plus control mirror", False))
        return
    inv, cls = Q8.inv, Q8.cls
    plus_class, minus_class = cls[Q8.index[(2, 0, 0, 0)]], cls[Q8.index[(-2, 0, 0, 0)]]
    fixed_weight = [0] * Q8.nclasses
    fixed_weight[plus_class], fixed_weight[minus_class] = 1, -1
    support = [0] * Q8.nclasses
    support[plus_class], support[minus_class] = 1, 1
    elements = range(8)
    for time_weight, want in (([1] * Q8.nclasses, (1920, 1920, 0, 1920, -64)), (support, (1920, 0, 3840, 0, 0))):
        total, negative_f, negative_live, dead, negative_blocks, asymmetric, mirror_equal, lowest = 0, 0, 0, 0, 0, 0, 0, None
        for a0, b0, a1, b1 in itertools.product(elements, repeat=4):
            value = {((0, 0, 0), 0): a0, ((0, 0, 0), 1): b0, ((0, 0, 1), 0): a1, ((0, 0, 1), 1): b1}
            f = 1
            for word in words_shared:
                f *= fixed_weight[word_class(Q8, word, value)]
            ups, downs = [], []
            for v in elements:
                # F(U) reads V(0) = v, and F(theta U) reads V(1)^-1 = v, so V(1) = v^-1 in the lower plaquettes.
                value[time_zero] = v
                value[time_one] = inv[v] if sign < 0 else v
                up, down = 1, 1
                for word in words_upper:
                    up *= time_weight[word_class(Q8, word, value)]
                for word in words_lower:
                    down *= time_weight[word_class(Q8, word, value)]
                ups.append(up)
                downs.append(down)
            live = any(ups)
            total += 1
            mirror_equal += 1 if ups == downs else 0
            negative_f += 1 if f < 0 else 0
            negative_live += 1 if f < 0 and live else 0
            dead += 0 if live else 1
            positive, negative, rank = inertia_exact([[f * d * u for u in ups] for d in downs])
            asymmetric += 1 if rank < 0 else 0
            negative_blocks += 1 if negative else 0
            at_c = f * sum(ups) * sum(downs)
            lowest = at_c if lowest is None or at_c < lowest else lowest
        got = (negative_f, negative_live, dead, negative_blocks, lowest)
        label = ",".join(map(str, time_weight))
        print("W_PLUS_CONTROL|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|fixed_slice_weight_plus1=1|fixed_slice_weight_minus1=-1|time_like_weight_on_classes=%s|family=all_8_point_functions_of_V(0)_at_each_C|C=%d|mirror_equal_at_each_C=%d|C_with_f<0=%d|of_those_W_plus_not_identically_zero=%d|C_with_W_plus_identically_zero=%d|Gram_blocks_with_a_negative_eigenvalue=%d|blocks_not_symmetric=%d|lowest_N(delta_C)_over_8^6=%d|ok=%d|json=0" % (
            label, total, mirror_equal, negative_f, negative_live, dead, negative_blocks, asymmetric, lowest, check("W_plus control time-like weight %s" % label, mirror_ok and total == 4096 and mirror_equal == 4096 and asymmetric == 0 and got == want)))


# ---- Part F. The transfer operator on a spatial slice.
class Slice:
    def __init__(self, *dims):
        self.lat = Lattice(*dims)
        self.links = self.lat.links
        self.position = {x: i for i, x in enumerate(self.lat.sites)}
        self.index = {l: i for i, l in enumerate(self.links)}
        self.ends = [(self.position[l[0]], self.position[self.lat.shift(l[0], l[1])]) for l in self.links]
        self.faces = [tuple((self.index[l], s) for l, s in self.lat.word(p)) for p in self.lat.plaquettes]
        self.configs = list(itertools.product(range(Q8.order), repeat=len(self.links)))
        self.gauges = list(itertools.product(range(Q8.order), repeat=len(self.lat.sites)))

    def image(self, config, g, bad=False):
        mult, inv = Q8.mult, Q8.inv
        if bad:
            return tuple(mult[mult[g[s]][u]][g[r]] for u, (s, r) in zip(config, self.ends))
        return tuple(mult[mult[g[s]][u]][inv[g[r]]] for u, (s, r) in zip(config, self.ends))

    def face_classes(self, config):
        out = []
        for face in self.faces:
            h = Q8.one
            for i, s in face:
                h = Q8.mult[h][config[i] if s > 0 else Q8.inv[config[i]]]
            out.append(Q8.cls[h])
        return tuple(out)

    def orbits(self):
        seen, reps, members = set(), [], []
        for config in self.configs:
            if config not in seen:
                orbit = sorted({self.image(config, g) for g in self.gauges})
                seen.update(orbit)
                reps.append(config)
                members.append(orbit)
        return reps, members


def link_table(weight):
    return [[weight[Q8.cls[Q8.mult[a][Q8.inv[b]]]] for b in range(8)] for a in range(8)]


def transfer_matrix(S, weight, reps, members):
    """Returns A on the orbits and the integer table T[i][j] = sum over g of B(rep_i, rep_j^g)."""
    table = link_table(weight)
    n_gauge = len(S.gauges)
    a_values = []
    for rep in reps:
        value = 1
        for k in S.face_classes(rep):
            value *= weight[k]
        a_values.append(value)
    size = len(reps)
    links = range(len(S.links))
    out = [[0] * size for _ in range(size)]
    for i, rep in enumerate(reps):
        rows = [table[u] for u in rep]
        for j, orbit in enumerate(members):
            total = 0
            for other in orbit:
                term = 1
                for ell in links:
                    term *= rows[ell][other[ell]]
                total += term
            out[i][j] = total * n_gauge // len(orbit)
    return a_values, out


def section_transfer():
    """Part F, rows YM4_02C_TRANSFER and YM4_02C_TRANSFER_TEST."""
    # The link kernel on Q8, each eigenfunction exact.
    c = (8, 3, 3, 3, 1)
    weight = q8_weight(c)
    spectrum_ok = True
    for rho in range(4):
        for g in range(8):
            total = sum(weight[Q8.cls[Q8.mult[g][Q8.inv[h]]]] * Q8_CHI[rho][Q8.cls[h]] for h in range(8))
            spectrum_ok = spectrum_ok and total == 8 * c[rho] * Q8_CHI[rho][Q8.cls[g]]
    for coordinate in range(4):
        for g in range(8):
            total = sum(weight[Q8.cls[Q8.mult[g][Q8.inv[h]]]] * Q8.elements[h][coordinate] for h in range(8))
            spectrum_ok = spectrum_ok and 2 * total == 8 * c[E_INDEX] * Q8.elements[g][coordinate]
    eigen = [red(c[rho], Q8_DIM[rho]) for rho in range(5)]
    trace = sum(Q8_DIM[rho] * c[rho] for rho in range(5))
    print("LINK_SPECTRUM|group=Q8|c=8,3,3,3,1|eigenvalues=%s|multiplicities=%s|eigenfunctions=the_four_signs_and_the_four_quaternion_coordinates|trace=%d|w_at_1=%d|ok=%d|json=0" % (
        ",".join(text(e) for e in eigen), ",".join(str(d * d) for d in Q8_DIM), trace, weight[Q8.cls[Q8.one]], check("link kernel spectrum on Q8", spectrum_ok and weight[Q8.cls[Q8.one]] == trace)))
    bad = SABOTAGE == "bad_projector"
    S = Slice(2, 1)
    # The explicit trace of A B P: every spatial configuration and every gauge element, one histogram for every weight.
    hist = collections.defaultdict(int)
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    links = range(len(S.links))
    for config in S.configs:
        faces = S.face_classes(config)
        for g in S.gauges:
            moved = S.image(config, g, bad)
            hist[(faces, tuple(cls[mult[config[ell]][inv[moved[ell]]]] for ell in links))] += 1
    denominator = 8 ** (len(S.links) + len(S.lat.sites))
    lat3 = Lattice(2, 1, 1)
    words = [lat3.word(p) for p in lat3.plaquettes]
    direct_hist, free = class_histogram(lat3, Q8, words, fix_forest=False)
    forest_hist, forest_free = class_histogram(lat3, Q8, words)
    reps, members = S.orbits()
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        weight = q8_weight(c)
        total = 0
        for (faces, kernels), count in hist.items():
            term = count
            for k in faces:
                term *= weight[k]
            for k in kernels:
                term *= weight[k]
            total += term
        trace = red(total, denominator)
        direct = red(sum_over_weight(direct_hist, weight), power(8, free))
        forest = red(sum_over_weight(forest_hist, weight), power(8, forest_free))
        a_values, table = transfer_matrix(S, weight, reps, members)
        orbit_trace = red(sum(a_values[i] * table[i][i] * len(members[i]) for i in range(len(reps))), len(S.gauges) * len(S.configs))
        ok = trace == direct and direct == forest and orbit_trace == direct
        print("TRANSFER|spatial=(Z/2)x(Z/1)|N_t=1|group=Q8|c=%s|terms=%d|Tr_ABP=%s|Z_direct=%s|Z_direct_forest_fixed=%s|trace_over_the_%d_gauge_orbits=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), denominator, text(trace), text(direct), text(forest), len(reps), text(orbit_trace), check("Tr(A B P) against the lattice sum c=%s" % (c,), ok)))
    if bad:
        return
    # P is a projection and commutes with A and B.
    faces_ok, kernel_ok, idempotent = True, True, True
    for i, config in enumerate(S.configs[::97]):
        other = S.configs[(i * 131 + 17) % len(S.configs)]
        for g in S.gauges[::5]:
            faces_ok = faces_ok and S.face_classes(S.image(config, g)) == S.face_classes(config)
            one, two = S.image(config, g), S.image(other, g)
            kernel_ok = kernel_ok and all(cls[mult[one[e]][inv[two[e]]]] == cls[mult[config[e]][inv[other[e]]]] for e in links)
    start = S.configs[1234]
    once = collections.defaultdict(int)
    for g in S.gauges:
        once[S.image(start, g)] += 1
    twice = collections.defaultdict(int)
    for u, v in once.items():
        for g in S.gauges:
            twice[S.image(u, g)] += v
    idempotent = all(twice[u] == v * len(S.gauges) for u, v in once.items()) and set(twice) == set(once)
    print("PROJECTOR|spatial=(Z/2)x(Z/1)|gauge_elements=%d|orbits=%d|P^2=P=%d|A_invariant=%d|B_invariant_under_the_common_move=%d|ok=%d|json=0" % (
        len(S.gauges), len(reps), 1 if idempotent else 0, 1 if faces_ok else 0, 1 if kernel_ok else 0, check("projector", idempotent and faces_ok and kernel_ok and len(reps) == 176)))
    # N_t = 2. The direct sum on (Z/2)x(Z/1)x(Z/2) has 8^9 gauge-fixed leaves, minutes in pure Python, so the direct comparison runs on spatial (Z/1)x(Z/1), with 8^6 leaves.
    small = Slice(1, 1)
    small_reps, small_members = small.orbits()
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        weight = q8_weight(c)
        a_values, table = transfer_matrix(small, weight, small_reps, small_members)
        size = len(small_reps)
        symmetric = all(table[i][j] == table[j][i] for i in range(size) for j in range(size))
        scale = len(small.gauges) * len(small.configs)
        m = [[a_values[i] * table[i][j] * len(small_members[j]) for j in range(size)] for i in range(size)]
        trace1 = red(sum(m[i][i] for i in range(size)), scale)
        trace2 = red(sum(m[i][j] * m[j][i] for i in range(size) for j in range(size)), scale ** 2)
        for steps, trace in ((1, trace1), (2, trace2)):
            lat_small = Lattice(1, 1, steps)
            hist_small, free_small = class_histogram(lat_small, Q8, [lat_small.word(p) for p in lat_small.plaquettes], fix_forest=False)
            direct = red(sum_over_weight(hist_small, weight), power(8, free_small))
            print("TRANSFER|spatial=(Z/1)x(Z/1)|N_t=%d|group=Q8|c=%s|assignments=%d|Tr_T^N_t_P_over_the_%d_gauge_orbits=%s|Z_direct=%s|BP_symmetric=%d|ok=%d|json=0" % (
                steps, ",".join(map(str, c)), power(8, free_small), size, text(trace), text(direct), 1 if symmetric else 0, check("transfer on (Z/1)x(Z/1) N_t=%d c=%s" % (steps, c), trace == direct and symmetric)))
        form = [[len(small_members[i]) * table[i][j] * len(small_members[j]) for j in range(size)] for i in range(size)]
        psd, rank, reason = psd_exact(form)
        want = c[E_INDEX] > 0
        print("BP_FORM|spatial=(Z/1)x(Z/1)|group=Q8|c=%s|gauge_invariant_dimension=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (",".join(map(str, c)), size, 1 if psd else 0, rank, reason, check("BP on the gauge-invariant space c=%s" % (c,), psd == want and (rank == size or not want))))
    # The lattice (Z/2)x(Z/1)x(Z/1) sliced along two axes: spatial (Z/2)x(Z/1) with one step, spatial (Z/1)x(Z/1) with two.
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        weight = q8_weight(c)
        a_big, t_big = transfer_matrix(S, weight, reps, members)
        one_step = red(sum(a_big[i] * t_big[i][i] * len(members[i]) for i in range(len(reps))), len(S.gauges) * len(S.configs))
        a_small, t_small = transfer_matrix(small, weight, small_reps, small_members)
        scale_small = len(small.gauges) * len(small.configs)
        m_small = [[a_small[i] * t_small[i][j] * len(small_members[j]) for j in range(len(small_reps))] for i in range(len(small_reps))]
        two_steps = red(sum(m_small[i][j] * m_small[j][i] for i in range(len(small_reps)) for j in range(len(small_reps))), scale_small ** 2)
        print("TWO_SLICINGS|lattice=(Z/2)x(Z/1)x(Z/1)|group=Q8|c=%s|spatial_(Z/2)x(Z/1)_one_step=%s|spatial_(Z/1)x(Z/1)_two_steps=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), text(one_step), text(two_steps), check("two slicings c=%s" % (c,), one_step == two_steps)))
    # Spatial (Z/2)x(Z/1): the matrix on the 176 orbits, its square, the temporal-gauge trace and the Collatz-Wielandt bounds.
    c = (8, 3, 3, 3, 1)
    weight = q8_weight(c)
    a_values, table = transfer_matrix(S, weight, reps, members)
    size = len(reps)
    scale = len(S.gauges) * len(S.configs)
    m = [[a_values[i] * table[i][j] * len(members[j]) for j in range(size)] for i in range(size)]
    trace1 = red(sum(m[i][i] for i in range(size)), scale)
    trace2 = red(sum(m[i][j] * m[j][i] for i in range(size) for j in range(size)), scale ** 2)
    symmetric = all(table[i][j] == table[j][i] for i in range(size) for j in range(size))
    print("TRANSFER|spatial=(Z/2)x(Z/1)|N_t=2|group=Q8|c=8,3,3,3,1|Tr_T^N_t_P_over_the_176_gauge_orbits=%s|BP_symmetric=%d|Z_direct=NOT_MEASURED|reason=BUDGET_8^9_gauge_fixed_leaves_in_pure_Python|smaller_case=(Z/1)x(Z/1)x(Z/2)_above|ok=%d|json=0" % (
        text(trace2), 1 if symmetric else 0, check("BP symmetric on (Z/2)x(Z/1)", symmetric)))
    # The direct sum over 8^9 gauge-fixed leaves was run by the second seat, in Rust. This compares the orbit trace here with its value for both weights.
    direct_by_second_seat = (8835582291457, 16)
    a_minus, table_minus = transfer_matrix(S, q8_weight((8, 3, 3, 3, -1)), reps, members)
    m_minus = [[a_minus[i] * table_minus[i][j] * len(members[j]) for j in range(size)] for i in range(size)]
    trace_minus = red(sum(m_minus[i][j] * m_minus[j][i] for i in range(size) for j in range(size)), scale ** 2)
    for label, value in (("8,3,3,3,1", trace2), ("8,3,3,3,-1", trace_minus)):
        print("TRANSFER_DIRECT_SECOND_SEAT|spatial=(Z/2)x(Z/1)|N_t=2|group=Q8|c=%s|Tr_T^N_t_P_here=%s|direct_by_second_seat=%s|tag_of_that_sum=MEASURED_by_second_seat|leaves=134217728|equal=%d|ok=%d|json=0" % (
            label, text(value), text(direct_by_second_seat), 1 if value == direct_by_second_seat else 0, check("orbit trace against the second seat's direct sum c=%s" % label, value == direct_by_second_seat)))
    # Luescher's temporal gauge with cyclic time: every time link set to 1, no projector. His footnote 3 says it agrees with the ungauged sum only in the infinite volume limit.
    no_v_words = [tuple((l, s) for l, s in lat3.word(p) if l[1] != lat3.time) for p in lat3.plaquettes]
    fixed_hist, fixed_free = class_histogram(lat3, Q8, no_v_words, fix_forest=False)
    temporal = red(sum_over_weight(fixed_hist, weight), power(8, fixed_free))
    trace_ab = red(sum(a * len(orbit) * weight[Q8.cls[Q8.one]] ** len(S.links) for a, orbit in zip(a_values, members)), len(S.configs))
    z_value = trace1
    print("NO_PROJECTOR|spatial=(Z/2)x(Z/1)|N_t=1|group=Q8|c=8,3,3,3,1|Tr_AB=%s|direct_sum_with_every_time_link_1=%s|Z=Tr_ABP=%s|differ=%d|ok=%d|json=0" % (
        text(trace_ab), text(temporal), text(z_value), 1 if trace_ab != z_value else 0, check("temporal-gauge trace", trace_ab == temporal and trace_ab != z_value)))
    # Collatz-Wielandt on the positive matrix M = A B P, similar to T through A^(1/2). With f = 1 the ratio is A(U) c_0^N_links.
    first = [sum(row) for row in m]
    c0_power = c[0] ** len(S.links)
    explicit = all(first[i] == a_values[i] * c0_power * scale for i in range(size))
    low0, high0 = red(min(first), scale), red(max(first), scale)
    vector = [1] * size
    iterations = 24
    for _ in range(iterations):
        product = [sum(a * b for a, b in zip(row, vector)) for row in m]
        biggest = max(product)
        vector = [max(1, v * 2 ** 64 // biggest) for v in product]
    product = [sum(a * b for a, b in zip(row, vector)) for row in m]
    ratios = [red(x, y * scale) for x, y in zip(product, vector)]
    low, high = ratios[0], ratios[0]
    for r in ratios:
        if r[0] * low[1] < low[0] * r[1]:
            low = r
        if r[0] * high[1] > high[0] * r[1]:
            high = r
    positive = all(v > 0 for row in m for v in row)
    below_traces = low[0] * trace1[1] <= trace1[0] * low[1] and low[0] ** 2 * trace2[1] <= trace2[0] * low[1] ** 2
    ok = (explicit and positive and low[0] * high[1] <= high[0] * low[1] and low0[0] * low[1] <= low[0] * low0[1] and high[0] * high0[1] <= high0[0] * high[1] and below_traces)
    print("COLLATZ_WIELANDT|spatial=(Z/2)x(Z/1)|group=Q8|c=8,3,3,3,1|matrix_M=ABP_on_176_orbits_entries_positive=%d|f=1_gives_A(U)*c_0^4_exactly=%d|f=1_low=%s|f=1_high=%s|after_%d_power_steps_lambda_0_times_10^6_low=%d|high=%d|lambda_0^N_t<=Z_for_N_t=1,2=%d|lambda_1=OPEN|ok=%d|json=0" % (
        1 if positive else 0, 1 if explicit else 0, text(low0), text(high0), iterations, scaled_floor(low, 10 ** 6), scaled_ceiling(high, 10 ** 6), 1 if below_traces else 0, check("Collatz-Wielandt", ok)))


# ---- Second-round rows, from the second seat's findings on 1618199.
def side_one_strip(group, weight):
    """strip[a][b] = sum_v w(a v b^-1 v^-1), one plane of a lattice with spatial side 1."""
    mult, inv, cls = group.mult, group.inv, group.cls
    elements = range(group.order)
    return [[sum(weight[cls[mult[mult[mult[a][v]][inv[b]]][inv[v]]]] for v in elements) for b in elements] for a in elements]


def section_negative_coefficient(hist):
    """What a negative coefficient does depends on the lattice, on T and on the weight. At T = 2 the kernel is the pointwise square of BP, and the square can be PSD when BP is not. The third weight has c_2dim < 0 and takes both signs, and it is PSD at T = 2, so the red statement there asks for w >= 0, as in section_negative_coefficient_scan."""
    pairs = list(itertools.product(range(8), repeat=2))
    expect = (((8, -1, 3, 3, 2), True, (5, 0), (1130, 1), (435, 1), (263604, 1), (5, 0), (17, 8)),
              ((8, -1, 2, 2, 1), True, (4, 1), (527, 4), (-57343, 64), (16785473, 64), (4, 1), (17, 8)),
              ((1, -2, -2, -2, -1), False, (5, 0), (23, 4), (7169, 64), (12353, 64), (5, 0), (17, 8)))
    for c, want_positive, want_three, want_e, want_s, want_z, want_one, want_four in expect:
        weight = q8_weight(c)
        matrix = gram_link_matrix(hist, weight)
        three = inertia_exact(matrix)
        t = [red(power(c[rho], 3), power(Q8_DIM[rho], 3)) for rho in range(5)]
        rule_e = pmul(pmul((2, 1), t[4]), padd(t[0], padd(t[1], padd(t[2], t[3]))))
        rule_s = padd(padd(pmul((2, 1), pmul(t[0], t[1])), pmul((2, 1), pmul(t[2], t[3]))), pmul(t[4], t[4]))
        entry_e, entry_s, z = red(matrix[E_INDEX][E_INDEX], 8 ** 7), red(matrix[1][1], 8 ** 7), red(matrix[0][0], 8 ** 7)
        strip = side_one_strip(Q8, weight)
        one = inertia_exact([[strip[a][b] * strip[b][a] for a in range(8)] for b in range(8)])
        four = inertia_exact([[strip[a][b] * strip[b][b2] * strip[b2][a2] * strip[a2][a] for (a, b) in pairs] for (a2, b2) in pairs])
        ok = (three[:2] == want_three and entry_e == want_e == rule_e and entry_s == want_s == rule_s and z == want_z and one[:2] == want_one and four[:2] == want_four and (min(weight) > 0) == want_positive)
        print("NEGATIVE_COEFFICIENT|group=Q8|c=%s|w_on_classes=%s|pointwise_positive=%d|(Z/3)x(Z/2)_five_characters_positive=%d|negative=%d|G_EE=%s|rule_2*t_E*(t_0+t_1+t_2+t_3)=%s|G_s1s1=%s|rule_2*t_0*t_1+2*t_2*t_3+t_E^2=%s|Z=%s|(Z/1)x(Z/2)_all_8_positive=%d|negative=%d|(Z/1)x(Z/4)_all_64_positive=%d|negative=%d|ok=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, weight)), 1 if min(weight) > 0 else 0, three[0], three[1], text(entry_e), text(rule_e), text(entry_s), text(rule_s), text(z), one[0], one[1], four[0], four[1], check("negative coefficient c=%s" % (c,), ok)))


def section_negative_coefficient_scan():
    """The convolution line of Remark 6.2. With w2(x) the sum of w over the coset x of {+1, -1} in Q8, one has 8 c_a = sum_x w2(x) chi_a(x) for the four characters of the quotient, and Fourier inversion gives sum_a (8 c_a)^L = 4 (w2 * ... * w2)(1), with L factors. For w >= 0 with c_2dim < 0 the right side is at least 4 w2(1)^L > 0, so G_EE = 2 t_E (t_0 + t_1 + t_2 + t_3) is negative at every odd L."""
    coset = [next(i for i in range(4) if e[i]) for e in Q8.elements]
    quotient = [[0] * 4 for _ in range(4)]
    for g in range(8):
        for h in range(8):
            quotient[coset[g]][coset[h]] = coset[Q8.mult[g][h]]
    well_defined = all(quotient[coset[g]][coset[h]] == coset[Q8.mult[g][h]] for g in range(8) for h in range(8))
    sizes = [len(members) for members in Q8.classes]
    weights, cases, identity_failures, bound_failures, negative = 0, 0, 0, 0, 0
    for w in itertools.product(range(7), repeat=5):
        c8 = [sum(sizes[k] * w[k] * Q8_CHI[rho][k] for k in range(5)) for rho in range(5)]
        if c8[E_INDEX] >= 0:
            continue
        weights += 1
        w2 = [sum(w[Q8.cls[g]] for g in range(8) if coset[g] == x) for x in range(4)]
        convolution = w2
        for length in range(1, 6):
            if length > 1:
                step = [0] * 4
                for y in range(4):
                    for z in range(4):
                        step[quotient[y][z]] += convolution[y] * w2[z]
                convolution = step
            if length % 2:
                total = sum(power(c8[a], length) for a in range(4))
                entry = pmul(pmul((2, 1), red(power(c8[E_INDEX], length), power(16, length))), red(total, power(8, length)))
                cases += 1
                identity_failures += 0 if total == 4 * convolution[0] else 1
                bound_failures += 0 if convolution[0] >= power(w2[0], length) > 0 else 1
                negative += 1 if entry[0] < 0 else 0
    ok = well_defined and weights == 7203 and cases == 21609 and identity_failures == 0 and bound_failures == 0 and negative == cases
    print("NEGATIVE_COEFFICIENT_SCAN|group=Q8|weights=w_on_classes_in_0..6_with_c_2dim<0|weights_counted=%d|L=1,3,5|cases=%d|identity_sum_a_(8*c_a)^L=4*(w2^*L)(1)_failures=%d|(w2^*L)(1)>=w2(1)^L>0_failures=%d|G_EE_negative=%d|quotient_by_{+1,-1}_well_defined=%d|ok=%d|json=0" % (
        weights, cases, identity_failures, bound_failures, negative, 1 if well_defined else 0, check("negative coefficient scan", ok)))


def section_minus_w(hist):
    """Theorem 4 through -w at T = 2. N_p is even when T is even, so the product of -w over all plaquettes is the product of w, and c_rho c_0 >= 0 with c_0 < 0 gives a PSD form through the weight -w."""
    c, twin = (-8, -3, -3, -3, -1), (8, 3, 3, 3, 1)
    weight = q8_weight(c)
    plaquettes = len(Lattice(3, 2).plaquettes)
    matrix, matrix_twin = gram_link_matrix(hist, weight), gram_link_matrix(hist, q8_weight(twin))
    positive, negative, rank = inertia_exact(matrix)
    entry = red(matrix[E_INDEX][E_INDEX], 8 ** 7)
    ok = matrix == matrix_twin and (positive, negative) == (5, 0) and rank == 5 and entry == (593, 4) and plaquettes % 2 == 0
    print("MINUS_W|c=%s|w_on_classes=%s|twin_c=%s|lattice=(Z/3)x(Z/2)|N_p=%d|family=five_characters_of_W|Gram_equal_to_the_twin=%d|positive=%d|negative=%d|G_EE=%s|ok=%d|json=0" % (
        ",".join(map(str, c)), ",".join(map(str, weight)), ",".join(map(str, twin)), plaquettes, 1 if matrix == matrix_twin else 0, positive, negative, text(entry), check("the form of -w at T=2", ok)))


def section_t4_witness():
    """A witness at T = 4 for a nowhere-zero weight with c_rho c_0 < 0. F = chi_rho(U(0)) / w(p_0) lies on the open half, bounded since w is nowhere zero on a finite group, and the half weights cancel, so the numerator is the sum of chi_rho(U(3)) chi_rho(U(0)) w(p_1) w(p_3), with V(0) and V(2) free. The rule is (c_rho/d_rho)^L c_0^(2 N_links - L), and L = N_links = 1 here. The weight may take both signs, and c_0 need not be the order of the group."""
    for c, rho in (((8, -1, 3, 3, 2), 1), ((8, 3, 3, 3, -1), E_INDEX), ((1, -2, -2, -2, -1), 1), ((8, -3, 3, 3, 1), 1), ((-8, 3, -3, -3, -1), 1)):
        weight = q8_weight(c)
        strip = side_one_strip(Q8, weight)
        character = [Q8_CHI[rho][Q8.cls[g]] for g in range(8)]
        elements = range(8)
        top = sum(character[u3] * character[u0] * strip[u3][u0] for u0 in elements for u3 in elements)
        middle = sum(strip[u1][u2] for u1 in elements for u2 in elements)
        numerator = red(top * middle * 8 * 8, 8 ** 8)
        rule = pmul(red(c[rho], Q8_DIM[rho]), (c[0], 1))
        print("T4_RED_WITNESS|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|w_on_classes=%s|pointwise_positive=%d|F=chi_%s(U(0))/w(p_0)|numerator=%s|rule_(c_rho/d_rho)^L*c_0^(2*N_links-L)=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, weight)), 1 if min(weight) > 0 else 0, "2dim" if rho == E_INDEX else "s1", text(numerator), text(rule), check("witness at T=4 c=%s" % (c,), numerator == rule and numerator[0] < 0 and all(weight))))


def section_t4_open_half():
    """All 512 point functions of the open half (U(0), U(1), V(0)) on (Z/1)x(Z/4), each entry from the plaquette words. The mirror of (a, b, v) reads U(3) = a, U(2) = b, V(2) = v^-1."""
    lat = Lattice(1, 4)
    R = Reflection(lat, "link")
    mirror_ok = R.link(((0, 0), 0))[0] == ((0, 3), 0) and R.link(((0, 1), 0))[0] == ((0, 2), 0) and R.link(((0, 0), 1)) == (((0, 2), 1), -1)
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    elements = range(8)
    triples = list(itertools.product(elements, repeat=3))
    forms = {}
    for c, want in (((8, 3, 3, 3, 1), (25, 0)), ((8, 3, 3, 3, -1), (17, 8)), ((-8, -3, -3, -3, -1), (25, 0)), ((-8, -3, -3, -3, 1), (17, 8)), ((1, -2, -2, -2, -1), (17, 8))):
        weight = q8_weight(c)
        strip = side_one_strip(Q8, weight)

        def plaquette(lower, upper, v):
            return weight[cls[mult[mult[mult[lower][v]][inv[upper]]][inv[v]]]]
        matrix = [[plaquette(a, b, v) * strip[b][b2] * plaquette(b2, a2, inv[v2]) * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]
        forms[c] = matrix
        positive, negative, rank = inertia_exact(matrix)
        print("EVERY_FUNCTION_T4_OPEN_HALF|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|family=all_512_point_functions_of_(U(0),U(1),V(0))|positive=%d|negative=%d|rank=%d|ok=%d|json=0" % (
            ",".join(map(str, c)), positive, negative, rank, check("every function of the open half at T=4 c=%s" % (c,), mirror_ok and (positive, negative) == want and rank == 25)))
    # Theorem 4 through -w at T = 4. N_p is even when T is even, so the two weights give one form.
    c, twin = (-8, -3, -3, -3, -1), (8, 3, 3, 3, 1)
    equal = forms[c] == forms[twin]
    print("MINUS_W|c=%s|w_on_classes=%s|twin_c=%s|lattice=(Z/1)x(Z/4)|N_p=%d|family=all_512_point_functions_of_(U(0),U(1),V(0))|Gram_equal_to_the_twin=%d|ok=%d|json=0" % (
        ",".join(map(str, c)), ",".join(map(str, q8_weight(c))), ",".join(map(str, twin)), len(lat.plaquettes), 1 if equal else 0, check("the form of -w at T=4", equal and len(lat.plaquettes) % 2 == 0)))


def sign_is_character(group, weight):
    """Whether the sign of a nowhere-zero weight is plus or minus a homomorphism to {+1, -1}."""
    sign = [1 if weight[group.cls[g]] > 0 else -1 for g in range(group.order)]
    base = sign[group.one]
    return all(sign[group.mult[g][h]] * base == sign[g] * sign[h] for g in range(group.order) for h in range(group.order))


def word_class(group, word, value):
    h = group.one
    for l, s in word:
        h = group.mult[h][value[l] if s > 0 else group.inv[value[l]]]
    return group.cls[h]


def section_site_sharp():
    """Theorem 2's sharp form on (Z/2)x(Z/1)x(Z/2), Q8. N(delta_C) = A(C_0) A(C_1) T(C_0, C_1) T(C_1, C_0) depends only on the two gauge orbits, so the 8^8 values of C reduce to pairs of the 176 orbits. Numerators over 8^12."""
    S = Slice(2, 1)
    reps, members = S.orbits()
    size = len(reps)
    sizes = [len(orbit) for orbit in members]
    faces = [S.face_classes(config) for config in S.configs]
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    elements = range(8)
    # Lemma 3.1 on one time-like plaquette with its four links free: the upper word at (a, b, v0, v1) against the lower word at the mirror.
    mismatches = 0
    for a in elements:
        for b in elements:
            for v0 in elements:
                for v1 in elements:
                    if cls[mult[mult[mult[a][v1]][inv[b]]][inv[v0]]] != cls[mult[mult[mult[b][inv[v1]]][inv[a]]][v0]]:
                        mismatches += 1
    lat = Lattice(2, 1, 2)
    R = Reflection(lat, "site")
    upper, shared, lower = partition(lat, "site")
    time_links = [((0, 0, 0), 2), ((1, 0, 0), 2)]
    mirror_ok = R.link(time_links[0])[0] == ((0, 0, 1), 2) and R.link(time_links[1])[0] == ((1, 0, 1), 2)

    def block(weight, c0, c1):
        """The Gram block of the 64 point functions of (V(0,0,0), V(1,0,0)) at the fixed-slice links c0, c1, from the plaquette words, with the mirror from Reflection.link."""
        value = {}
        for i, ((x, y), mu) in enumerate(S.links):
            value[((x, y, 0), mu)] = c0[i]
            value[((x, y, 1), mu)] = c1[i]
        prefactor, fixed_values = 1, []
        for p in shared:
            fixed_values.append(weight[word_class(Q8, lat.word(p), value)])
            prefactor *= fixed_values[-1]
        ups, downs = [], []
        for v0, v1 in itertools.product(elements, repeat=2):
            for link, v in zip(time_links, (v0, v1)):
                value[link] = v
                image, sign = R.link(link)
                value[image] = inv[v] if sign < 0 else v
            up, down = 1, 1
            for p in upper:
                up *= weight[word_class(Q8, lat.word(p), value)]
            for p in lower:
                down *= weight[word_class(Q8, lat.word(p), value)]
            ups.append(up)
            downs.append(down)
        return prefactor, fixed_values, [[prefactor * d * u for u in ups] for d in downs]
    second_seat = {(3, 2, 1, -1, -2): (0, 20736, 53321326354432), (1, -1, 1, 1, 1): (1572864, -2304, 10989076480)}
    for w in ((3, 2, 1, -1, -2), (1, 1, 1, -1, -1), (3, 2, 1, -1, 2), (1, -1, 1, 1, 1)):
        weight = list(w)
        a_values, table = transfer_matrix(S, weight, reps, members)
        evaluations = sum(1 for f in faces for k in f if weight[k] < 0)
        negative_slices = sum(1 for f in faces if weight[f[0]] * weight[f[1]] < 0)
        positive_slices = sum(1 for f in faces if weight[f[0]] * weight[f[1]] > 0)
        prefactor_negative = 2 * negative_slices * positive_slices
        lowest, negative, z, weighed = None, 0, 0, 0
        for i in range(size):
            for j in range(size):
                value = a_values[i] * a_values[j] * table[i][j] * table[j][i]
                pair = sizes[i] * sizes[j]
                z += value * pair
                weighed += pair
                negative += pair if value < 0 else 0
                lowest = value if lowest is None or value < lowest else lowest
        every_block_psd = mismatches == 0 and prefactor_negative == 0
        ok = weighed == 8 ** 8 and mismatches == 0 and len(faces) == 4096 and (negative == 0) == every_block_psd
        if w in second_seat:
            ok = ok and (negative, lowest, z) == second_seat[w]
        print("SITE_SHARP|lattice=(Z/2)x(Z/1)x(Z/2)|group=Q8|w_on_classes=%s|sign_is_a_homomorphism=%d|slice_configurations=%d|fixed_plaquette_evaluations=%d|with_w<0=%d|slices_with_negative_product=%d|C_with_negative_prefactor=%d|plaquette_mirror_mismatches=%d|C_with_negative_N(delta_C)=%d|of=%d|lowest_N(delta_C)_over_8^12=%d|Z_over_8^12=%d|every_Gram_block_PSD_from_the_formula=%d|ok=%d|json=0" % (
            ",".join(map(str, w)), 1 if sign_is_character(Q8, weight) else 0, len(faces), 2 * len(faces), evaluations, negative_slices, prefactor_negative, mismatches, negative, weighed, lowest, z, 1 if every_block_psd else 0, check("sharp form of the site theorem w=%s" % (w,), ok)))
        # One Gram block from the words. A C whose slices hold a negative plaquette weight, with a negative prefactor when the weight has one.
        with_negative = [config for config, f in zip(S.configs, faces) if any(weight[k] < 0 for k in f)]
        c0 = next((config for config, f in zip(S.configs, faces) if weight[f[0]] * weight[f[1]] < 0), with_negative[0])
        c1 = next((config for config, f in zip(S.configs, faces) if weight[f[0]] * weight[f[1]] > 0), c0) if negative_slices else with_negative[-1]
        if not mirror_ok:
            print("SITE_SHARP_BLOCK|lattice=(Z/2)x(Z/1)x(Z/2)|group=Q8|w_on_classes=%s|mirror_of_the_time_links_at_t=1=0|ok=%d|json=0" % (",".join(map(str, w)), check("site block w=%s" % (w,), False)))
            continue
        prefactor, fixed_values, gram = block(weight, c0, c1)
        psd, rank, reason = psd_exact(gram)
        print("SITE_SHARP_BLOCK|lattice=(Z/2)x(Z/1)x(Z/2)|group=Q8|w_on_classes=%s|family=all_64_point_functions_of_(V(0,0,0),V(1,0,0))_at_one_C|w_on_its_fixed_plaquettes=%s|f(C)=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
            ",".join(map(str, w)), ",".join(map(str, fixed_values)), prefactor, 1 if psd else 0, rank, reason, check("site block w=%s" % (w,), psd == (prefactor > 0) and (rank == 1 or not psd) and min(fixed_values) < 0)))


def section_slice_pairs():
    """The two plaquettes of a slice of (Z/2)x(Z/1) with Q8, over all 4096 configurations: how often the second is the inverse of the first, how often they lie in one class up to the center, and how often the pair is +1, -1 in either order."""
    S = Slice(2, 1)
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    plus, minus = Q8.index[(2, 0, 0, 0)], Q8.index[(-2, 0, 0, 0)]
    inverse_pairs, same_class, sign_pairs = 0, 0, 0
    for config in S.configs:
        values = []
        for face in S.faces:
            h = Q8.one
            for i, s in face:
                h = mult[h][config[i] if s > 0 else inv[config[i]]]
            values.append(h)
        first, second = values
        inverse_pairs += 1 if second == inv[first] else 0
        same_class += 1 if cls[second] in (cls[first], cls[mult[minus][first]]) else 0
        sign_pairs += 1 if {first, second} == {plus, minus} else 0
    ok = (len(S.configs), inverse_pairs, same_class, sign_pairs) == (4096, 2176, 4096, 384)
    print("SLICE_PAIRS|slice=(Z/2)x(Z/1)|group=Q8|configurations=%d|second_plaquette_is_the_inverse_of_the_first=%d|same_class_up_to_the_center=%d|the_pair_+1,-1_in_either_order=%d|ok=%d|json=0" % (
        len(S.configs), inverse_pairs, same_class, sign_pairs, check("plaquette pairs of a slice", ok)))


def section_site_character():
    """A slice with every side 2. The plaquette classes are gauge invariant, so a spanning tree is set to 1 and 8^5 assignments remain."""
    lat = Lattice(2, 2)
    hist, free = class_histogram(lat, Q8, [lat.word(p) for p in lat.plaquettes])
    for w, want_character in (((3, 2, 1, -1, -2), True), ((1, 1, 1, -1, -1), True), ((-1, -1, -1, -1, -1), True), ((3, 2, 1, -1, 2), False), ((1, -1, 1, 1, 1), False)):
        weight = list(w)
        negative = 0
        for key, count in hist.items():
            term = 1
            for k in key:
                term *= weight[k]
            negative += count if term < 0 else 0
        character = sign_is_character(Q8, weight)
        ok = character == want_character and (negative == 0) == want_character and sum(hist.values()) == power(8, free)
        print("SITE_CHARACTER|slice=(Z/2)x(Z/2)|group=Q8|w_on_classes=%s|gauge_fixed_configurations=%d|sign_is_a_homomorphism=%d|negative_product=%d|ok=%d|json=0" % (
            ",".join(map(str, w)), power(8, free), 1 if character else 0, negative, check("site character w=%s" % (w,), ok)))


def section_single_w():
    """Theorem 2's controls with one class function on every plaquette, on (Z/1)^k x (Z/2). N(delta_C) over the pairs of gauge orbits."""
    cases = ((2, (1, 1), (((1, -1, 1, 1, 1), -64, (7, 64)), ((3, 1, 1, 1, 1), 64, (1179, 64)), ((3, 1, -2, 1, -1), 64, (2253, 64)), ((-1, -1, -1, -1, -1), 64, (1, 1)))),
             (3, (1, 1, 1), (((1, -1, 1, 1, 1), -64, (11, 128)), ((3, 1, 1, 1, 1), 64, (170535, 128)), ((3, 1, -2, 1, -1), 192, (423723, 128)), ((-1, -1, -1, -1, -1), 64, (1, 1)))))
    for k, dims, weights in cases:
        S = Slice(*dims)
        reps, members = S.orbits()
        size = len(reps)
        sizes = [len(orbit) for orbit in members]
        for w, want_lowest, want_z in weights:
            weight = list(w)
            a_values, table = transfer_matrix(S, weight, reps, members)
            lowest, total = None, 0
            for i in range(size):
                for j in range(size):
                    value = a_values[i] * a_values[j] * table[i][j] * table[j][i]
                    total += value * sizes[i] * sizes[j]
                    lowest = value if lowest is None or value < lowest else lowest
            z = red(total, power(8, 2 * k + 2))
            one_slice_negative = any(a < 0 for a in a_values)
            print("SINGLE_W_SITE|lattice=(Z/1)^%dx(Z/2)|group=Q8|w_on_classes=%s|lowest_N(delta_C)_over_8^%d=%d|Z=%s|product_over_one_slice_goes_negative=%d|ok=%d|json=0" % (
                k, ",".join(map(str, w)), 2 * k + 2, lowest, text(z), 1 if one_slice_negative else 0, check("single weight k=%d w=%s" % (k, w), lowest == want_lowest and z == want_z)))


def form_minimum(first, second):
    """The lowest value of x -> (second . x)(first . x) over x = alpha e_i + gamma e_j with alpha, gamma chosen to set the two factors against each other."""
    best = None
    for i in range(len(first)):
        for j in range(i):
            alpha, gamma = second[j] + first[j], -(second[i] + first[i])
            value = (alpha * second[i] + gamma * second[j]) * (alpha * first[i] + gamma * first[j])
            best = value if best is None or value < best else best
    return best


def section_gram_moved():
    """Site reflection on (Z/2)x(Z/2) with F moved by gauge transformations. Both slices are fixed and (A, B) holds their links, so F lives on the time links V(0,0), V(1,0), and the mirror comes from Reflection.link. The invalid reflection runs beside it as a red control, and the sabotages route it through Reflection.link. Numerators over 8^8."""
    lat = Lattice(2, 2)
    R = Reflection(lat, "site")
    fixed_ok = all(R.link(((x, t), 0)) == (((x, t), 0), 1) for x in range(2) for t in range(2))
    time_ok = all(R.link(((x, 0), 1))[0] == ((x, 1), 1) and R.link(((x, 1), 1))[0] == ((x, 0), 1) for x in range(2))
    word_ok = all(lat.word(((x, t), 0, 1)) == ((((x, t), 0), 1), (((x ^ 1, t), 1), 1), (((x, t ^ 1), 0), -1), (((x, t), 1), -1)) for x in range(2) for t in range(2))
    if not (fixed_ok and time_ok and word_ok):
        print("GRAM_SITE_MOVED|lattice=(Z/2)x(Z/2)|group=Q8|reflection_fixes_both_slices=%d|time_links_swap=%d|plaquette_words_as_written=%d|ok=%d|json=0" % (1 if fixed_ok else 0, 1 if time_ok else 0, 1 if word_ok else 0, check("gauge-moved site Gram", False)))
        return
    sign = R.link(((0, 0), 1))[1]
    c = (8, 3, 3, 3, 1)
    weight = q8_weight(c)
    mult, inv, cls = Q8.mult, Q8.inv, Q8.cls
    elements = range(8)
    table = [[[[weight[cls[mult[mult[mult[u][r]][inv[d]]][inv[l]]]] for l in elements] for d in elements] for r in elements] for u in elements]
    pairs = list(itertools.product(elements, repeat=2))
    position = {pair: k for k, pair in enumerate(pairs)}
    inverse_position = [position[(inv[v0], inv[v1])] for (v0, v1) in pairs]
    # Each element is a sign times a quaternion unit. F_(mu, nu)(v0, v1) is the coordinate mu of v0 times the coordinate nu of v1.
    coordinate = []
    for v in elements:
        e = Q8.elements[v]
        mu = next(i for i in range(4) if e[i])
        coordinate.append((mu, e[mu] // 2))

    def family_value(mu, nu, v0, v1):
        return coordinate[v0][1] * coordinate[v1][1] if coordinate[v0][0] == mu and coordinate[v1][0] == nu else 0
    i_element = Q8.index[(0, 2, 0, 0)]
    moved = all(any(family_value(mu, nu, mult[i_element][v0], v1) != family_value(mu, nu, v0, v1) for (v0, v1) in pairs) for mu in range(4) for nu in range(4))
    slots = [(1 + 4 * coordinate[v0][0] + coordinate[v1][0], coordinate[v0][1] * coordinate[v1][1]) for (v0, v1) in pairs]
    size, target = 17, 1 + 4 * 1 + 0
    matrix = [[0] * size for _ in range(size)]
    blocks, equal, lost, red_ff = 0, 0, 0, 0
    witness, witness_up, witness_bad = (0, 0, 2, 3), None, None
    for a0, a1, b0, b1 in itertools.product(elements, repeat=4):
        blocks += 1
        ta0, ta1, tb0, tb1 = table[a0], table[a1], table[b0], table[b1]
        up = [ta0[v1][b0][v0] * ta1[v0][b1][v1] for (v0, v1) in pairs]
        bad = [tb0[x1][a0][x0] * tb1[x0][a1][x1] for (x0, x1) in pairs]
        mirror = [bad[k] for k in inverse_position] if sign < 0 else bad
        equal += 1 if mirror == up else 0
        lost += 1 if bad != up else 0
        if (a0, a1, b0, b1) == witness:
            witness_up, witness_bad = up, bad
        g, h = [0] * size, [0] * size
        g[0], h[0] = sum(up), sum(mirror)
        bad_f = 0
        for k, (slot, s) in enumerate(slots):
            g[slot] += s * up[k]
            h[slot] += s * mirror[k]
            if slot == target:
                bad_f += s * bad[k]
        red_ff += bad_f * g[target]
        for a in range(size):
            x = h[a]
            if x:
                row = matrix[a]
                for b in range(size):
                    row[b] += x * g[b]
    rule = (0, 1)
    for rho in range(5):
        rule = padd(rule, red(power(c[rho], 4), power(Q8_DIM[rho], 4)))
    want_total = pmul((8 ** 8, 1), rule)
    total = matrix[0][0]
    print("GRAM_SITE_MOVED_BLOCKS|lattice=(Z/2)x(Z/2)|group=Q8|c=%s|family=all_64_point_functions_of_(V(0,0),V(1,0))_at_each_fixed_(A,B)|fixed_(A,B)=%d|mirror_equal_so_a_rank_one_square=%d|sum_of_all_entries=%d|expected_8^8*Z=%s|ok=%d|json=0" % (
        ",".join(map(str, c)), blocks, equal, total, text(want_total), check("gauge-moved site Gram blocks", blocks == 4096 and equal == blocks and (total, 1) == want_total)))
    entry = red(matrix[target][target], 8 ** 8)
    z = red(total, 8 ** 8)
    psd, rank, reason = psd_exact(matrix)
    symmetric = all(matrix[a][b] == matrix[b][a] for a in range(size) for b in range(a))
    print("GRAM_SITE_MOVED|lattice=(Z/2)x(Z/2)|group=Q8|c=%s|family=1_and_the_16_products_of_a_coordinate_of_V(0,0)_and_a_coordinate_of_V(1,0)|moved_by_gauge_transformations=%d|assignments=%d|F=e_1(V(0,0))*e_0(V(1,0))|G_FF=%s|expected=91/128|Z=%s|symmetric=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
        ",".join(map(str, c)), 1 if moved else 0, 8 ** 8, text(entry), text(z), 1 if symmetric else 0, 1 if psd else 0, rank, reason, check("gauge-moved site Gram", moved and entry == (91, 128) and psd and rank >= 1)))
    witness_value = form_minimum(witness_up, witness_bad)
    red_entry = red(red_ff, 8 ** 8)
    print("GRAM_SITE_MOVED_RED|lattice=(Z/2)x(Z/2)|group=Q8|c=%s|reflection=site_with_the_inverse_on_time_links_dropped|fixed_(A,B)_that_lose_symmetry=%d|expected_second_seat=3648|form_value_at_(A,B)=(0,0,2,3)=%d|expected_second_seat=-6351452416|G_FF=%s|expected=-91/128|ok=%d|json=0" % (
        ",".join(map(str, c)), lost, witness_value, text(red_entry), check("invalid reflection goes red", lost == 3648 and witness_value == -6351452416 and red_entry == (-91, 128))))


def section_two_t_controls():
    """Theorem 4 on a group with complex characters, and the control for w(g^-1) = w(g). Lattice (Z/1)x(Z/2), 2T."""
    mult, inv, cls = T2.mult, T2.inv, T2.cls
    elements = range(T2.order)
    inverse_class = [cls[inv[members[0]]] for members in T2.classes]
    asymmetric = [9, 7, 5, 8, 2, 3, 6]
    inverse_symmetric = all(asymmetric[k] == asymmetric[inverse_class[k]] for k in range(T2.nclasses))
    blocks, broken, worst = 0, 0, None
    for a in elements:
        for b in elements:
            # F is a point function of V(0) at fixed (a, b), and F(theta U) reads V(1)^-1.
            f = [asymmetric[cls[mult[mult[mult[a][v]][inv[b]]][inv[v]]]] for v in elements]
            h = [asymmetric[cls[mult[mult[mult[b][inv[v]]][inv[a]]][v]]] for v in elements]
            blocks += 1
            if f != h:
                broken += 1
                lowest = form_minimum(f, h)
                worst = lowest if worst is None or lowest < worst else worst
    print("W_INVERSE_CONTROL|lattice=(Z/1)x(Z/2)|group=2T|w_on_classes=%s|pointwise_positive=1|inverse_symmetric=%d|fixed_link_blocks=%d|blocks_not_symmetric=%d|lowest_form_value_on_two_coordinate_test_vectors=%d|ok=%d|json=0" % (
        ",".join(map(str, asymmetric)), 1 if inverse_symmetric else 0, blocks, broken, worst, check("w(g^-1) control on 2T", not inverse_symmetric and blocks == 576 and broken == 384 and worst == -144)))
    for c, want, want_weight in (((7, 2, 2, 4, 3, 1, 1), (7, 0), (33, 13, 7, 7, 7, 3, 3)), ((7, 2, 2, 4, -1, 1, 1), (6, 1), (25, 21, 7, 3, 3, 7, 7))):
        parts = [(sum(c[rho] * T2_CHI[rho][k][0] for rho in range(7)), sum(c[rho] * T2_CHI[rho][k][1] for rho in range(7))) for k in range(T2.nclasses)]
        weight = [p[0] for p in parts]
        real = all(p[1] == 0 for p in parts)
        strip = side_one_strip(T2, weight)
        matrix = [[strip[a][b] * strip[b][a] for a in elements] for b in elements]
        positive, negative, rank = inertia_exact(matrix)
        total = sum(sum(row) for row in matrix)
        rule = (0, 1)
        for rho in range(7):
            rule = padd(rule, red(c[rho] ** 2, T2_DIM[rho] ** 2))
        want_total = pmul((24 ** 4, 1), rule)
        ok = real and tuple(weight) == want_weight and (positive, negative) == want and (total, 1) == want_total
        print("LINK_2T|lattice=(Z/1)x(Z/2)|group=2T|c_on_1,w,w2,3,2,2w,2w2=%s|w_on_classes=%s|real=%d|family=all_24_point_functions_of_the_t=0_slice|positive=%d|negative=%d|rank=%d|sum_of_all_entries=%d|expected_24^4*Z=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, weight)), 1 if real else 0, positive, negative, rank, total, text(want_total), check("link reflection on 2T c=%s" % (c,), ok)))


def section_four_d():
    """Part H. (Z/1)^3 x (Z/2), a four-dimensional lattice: link reflection on every point function of the slice, reduced to the 176 gauge orbits, and the transfer trace. The numerator on the orbits i, j is o_i o_j A_i A_j T_ij T_ji over 8^8. It is congruent to T_ij T_ji through diag(o_i A_i), nonzero for w > 0, which keeps the integers small."""
    S = Slice(1, 1, 1)
    reps, members = S.orbits()
    size = len(reps)
    sizes = [len(orbit) for orbit in members]
    lat = Lattice(1, 1, 1, 2)
    hist, free = class_histogram(lat, Q8, [lat.word(p) for p in lat.plaquettes])
    e = Q8_CHI[E_INDEX]
    f = [e[Q8.cls[rep[0]]] for rep in reps]
    scale = len(S.gauges) * len(S.configs)
    expect = (((8, 3, 3, 3, 1), (176, 0), (5696786251574, 1), (366894732506723, 16), (559775981543075516869, 16)),
              ((8, 3, 3, 3, -1), (112, 64), (-1965328413750, 1), (257883799138323, 16), (333366012807212569335, 16)))
    for c, want, want_f, want_z, want_three in expect:
        weight = q8_weight(c)
        a_values, table = transfer_matrix(S, weight, reps, members)
        symmetric = all(table[i][j] == table[j][i] for i in range(size) for j in range(i))
        squares = [[table[i][j] * table[j][i] for j in range(size)] for i in range(size)]
        positive, negative, rank = inertia_exact(squares)
        left = [sizes[i] * a_values[i] for i in range(size)]
        z_form = red(sum(left[i] * left[j] * squares[i][j] for i in range(size) for j in range(size)), 8 ** 8)
        f_form = red(sum(left[i] * f[i] * left[j] * f[j] * squares[i][j] for i in range(size) for j in range(size)), 8 ** 8)
        direct = red(sum_over_weight(hist, weight), power(8, free))
        m = [[a_values[i] * table[i][j] * sizes[j] for j in range(size)] for i in range(size)]
        trace2 = red(sum(m[i][j] * m[j][i] for i in range(size) for j in range(size)), power(scale, 2))
        ok = (min(weight) > 0 and symmetric and (positive, negative) == want and rank == 176 and f_form == want_f and z_form == want_z and direct == want_z and trace2 == want_z)
        print("FOUR_D_LINK|lattice=(Z/1)^3x(Z/2)|group=Q8|c=%s|w_on_classes=%s|family=every_point_function_of_the_slice_reduced_to_%d_orbits|positive=%d|negative=%d|rank=%d|F=chi_2dim(U_1)|G_FF=%s|expected=%s|Z=%s|Tr_T^2_P=%s|Z_direct_forest_fixed=%s|assignments=%d|expected_Z=%s|BP_symmetric=%d|ok=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, weight)), size, positive, negative, rank, text(f_form), text(want_f), text(z_form), text(trace2), text(direct), power(8, free), text(want_z), 1 if symmetric else 0, check("four-dimensional link reflection c=%s" % (c,), ok)))
        columns = list(zip(*m))
        square = [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in m]
        trace3 = red(sum(square[i][j] * m[j][i] for i in range(size) for j in range(size)), power(scale, 3))
        print("FOUR_D_TRANSFER|spatial=(Z/1)^3|N_t=3|group=Q8|c=%s|Tr_T^N_t_P_here=%s|direct_by_second_seat=%s|tag_of_that_sum=MEASURED_by_second_seat|equal=%d|ok=%d|json=0" % (
            ",".join(map(str, c)), text(trace3), text(want_three), 1 if trace3 == want_three else 0, check("three steps against the second seat's direct sum c=%s" % (c,), trace3 == want_three)))


def main():
    if SABOTAGE in ("no_inverse_on_time_links", "wrong_plane", "dropped_inverse_third_letter", "dropped_inverse_fourth_letter"):
        section_geometry()
    elif SABOTAGE in ("no_inverse_in_gram", "wrong_plane_in_gram"):
        section_gram_moved()
    elif SABOTAGE == "every_function_one_plane":
        section_every_function()
    elif SABOTAGE == "t4_half_weights_dropped":
        section_every_function_t4_and_site()
    elif SABOTAGE == "wrong_multiplicity":
        section_characters()
    elif SABOTAGE == "negative_weight_called_positive":
        lat, hist = gram_pass()
        section_gram(lat, hist)
    elif SABOTAGE == "signed_site_weight_called_positive":
        section_signed_site()
    elif SABOTAGE == "bad_projector":
        section_transfer()
    else:
        section_psd_controls()
        section_geometry()
        section_characters()
        section_torus_su2()
        cylinder = section_cylinder()
        section_su2_red(cylinder)
        lat, hist = gram_pass()
        section_torus(hist)
        section_gram(lat, hist)
        section_negative_coefficient(hist)
        section_negative_coefficient_scan()
        section_minus_w(hist)
        section_gram_t4()
        section_every_function()
        section_every_function_t4_and_site()
        section_t4_witness()
        section_t4_open_half()
        section_signed_site()
        section_w_plus_control()
        section_site_sharp()
        section_slice_pairs()
        section_site_character()
        section_single_w()
        section_gram_moved()
        section_two_t_controls()
        section_transfer()
        section_four_d()
        print("SCOPE|each_statement_at_a_fixed_finite_lattice_and_fixed_beta=1|uniformity_in_volume_and_spacing=OPEN|lambda_1_and_a_quantitative_gap_for_SU2=OPEN|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0")
    print("REFLECTION_TRANSFER_DONE|failed=%d|json=0" % len(FAILS))
    for name in FAILS:
        print("FAILED|check=%s|json=0" % name.replace(" ", "_"))
    sys.exit(1 if FAILS else 0)


main()
