#!/usr/bin/env python3
"""YM4-02c: reflection positivity and the transfer operator of the finite 4D SU(2) Wilson lattice.

Exact checks against the rows of docs/PREDICTION-YM4-02c.hbp. The theorems of docs/LEMMA-0004-REFLECTION-TRANSFER.md hold
for a compact group with a real class weight, so Q8 and 2T with counting measure are instances of them in their own right.
Q8 stands in for Haar on SU(2) only where a row says so, within its exact degree of 3 per link.

usage = test_reflection_transfer_4d.py [sabotage=NAME]
NAME is one of no_inverse_on_time_links wrong_plane wrong_multiplicity negative_weight_called_positive
signed_site_weight_called_positive bad_projector, and each must exit 1 on a named check.
Python standard library, integers only, json=0.
"""
import collections
import itertools
import math
import sys

SABOTAGE_NAMES = ("no_inverse_on_time_links", "wrong_plane", "wrong_multiplicity", "negative_weight_called_positive",
                  "signed_site_weight_called_positive", "bad_projector")
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
    assert all(m[i][j] == m[j][i] for i in range(n) for j in range(i))
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
    print("PSD_TEST_CONTROLS|rank_one=green|zero_diagonal_indefinite=red|negative_minor=red|ok=%d|json=0" % check("exact PSD test reads its controls", ok))


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
        return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), -1), ((x, nu), -1))


class Reflection:
    """t -> c - t. Site reflection has c = 0 and link reflection c = -1. (theta U)(link) = U(image) ^ sign."""

    def __init__(self, lat, kind):
        self.lat, self.kind = lat, kind
        self.c = 0 if kind == "site" else -1
        if SABOTAGE == "wrong_plane":
            self.c = -1 - self.c

    def t(self, t):
        return (self.c - t) % self.lat.T

    def link(self, link):
        x, mu = link
        if mu != self.lat.time:
            return (x[:-1] + (self.t(x[-1]),), mu), 1
        # The edge from t to t+1 goes to the edge from c-t to c-t-1, the positive link at c-t-1 run backward.
        return (x[:-1] + (self.t(x[-1] + 1),), mu), (1 if SABOTAGE == "no_inverse_on_time_links" else -1)

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


def l_coefficient(n, k):
    """The coefficient of beta^(2k+n) in l_n(beta), a positive rational."""
    return red(1, 2 ** (2 * k + n) * math.factorial(k) * math.factorial(k + n + 1))


def bessel_coefficient(nu, k):
    """The coefficient of beta^k in I_nu(beta)."""
    if k < nu or (k - nu) % 2:
        return 0, 1
    return red(1, 2 ** k * math.factorial((k - nu) // 2) * math.factorial((k + nu) // 2))


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
            left = red(tau ** k, 2 ** k * math.factorial(k))
            right = (0, 1)
            for n in range(k % 2, k + 1, 2):
                j = (k - n) // 2
                right = padd(right, pmul((multiplicity(n) * chi(n, tau), 1), l_coefficient(n, j)))
            failures += 0 if left == right else 1
    print("CHARACTER_SERIES|identity=exp(beta*cos_theta)=sum_n_(n+1)*l_n(beta)*chi_n|orders=0..20|traces=2,1,0,-1,-2|identities=%d|failures=%d|ok=%d|json=0" % (21 * len(traces_used), failures, check("character series through beta^20", failures == 0)))
    positive, terms, odd_power = True, 0, True
    for n in range(0, 21):
        for k in range(0, 11):
            if 2 * k + n <= 20:
                c = l_coefficient(n, k)
                positive = positive and c[0] > 0
                odd_power = odd_power and ((2 * k + n) % 2 == n % 2)
                terms += 1
    print("L_N_COEFFICIENTS|n=0..20|through_beta^20|terms=%d|all_positive=%d|power_parity_equals_n_parity_so_odd_n_is_negative_at_beta<0=%d|ok=%d|json=0" % (terms, 1 if positive else 0, 1 if odd_power else 0, check("l_n coefficients", positive and odd_power)))
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
        moment = (4 ** k, 1)
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
        low = padd(low, (s[0] ** faces, s[1] ** faces))
        high = padd(high, (s_high[0] ** faces, s_high[1] ** faces))
    # For n > cut, l_n(1) < 1 and l_n(1) <= 2 (1/2)^n / (n+1)!, whose sum over n > cut is at most 4 (1/2)^(cut+1) / (cut+2)!.
    high = padd(high, red(4, 2 ** (cut + 1) * math.factorial(cut + 2)))
    e_low, e_high = (0, 1), (0, 1)
    for k in range(0, 40):
        e_low = padd(e_low, red((-1) ** k, math.factorial(k)))
    e_high = padd(e_low, red(1, math.factorial(40)))
    # Partial sums of exp(-1) alternate. The sum through k = 39 lies below and the sum through k = 40 above.
    weight_low = (e_low[0] ** faces, e_low[1] ** faces)
    weight_high = (e_high[0] ** faces, e_high[1] ** faces)
    return faces, pmul(weight_low, low), pmul(weight_high, high), weight_high


def section_torus_su2():
    for side, extent in ((2, 2), (3, 2)):
        faces, z_low, z_high, jensen_high = torus_su2_enclosure(side, extent)
        scale = 10 ** 12
        ok = z_high[0] <= z_high[1] and z_low[0] > 0 and z_low[0] * jensen_high[1] >= jensen_high[0] * z_low[1]
        print("TORUS_SU2_ENCLOSURE|L=%d|T=%d|F=%d|beta=1|Z_times_10^12_low=%d|Z_times_10^12_high=%d|exp(-beta*F)_times_10^12_high=%d|bound_exp(-beta*F)<=Z<=1=%d|ok=%d|json=0" % (
            side, extent, faces, scaled_floor(z_low, scale), scaled_ceiling(z_high, scale), scaled_ceiling(jensen_high, scale), 1 if ok else 0, check("SU(2) torus enclosure", ok)))


def section_su2_red():
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
    sum_high = padd(sum_high, red(4, 2 ** (cut + 1) * math.factorial(cut + 2)))
    half_low, half_high = pmul((1, 2), sum_low), pmul((1, 2), sum_high)
    # The same partial sums taken at beta = -1, term by term.
    at_minus = []
    for n in range(0, cut + 2):
        s = (0, 1)
        for k in range(0, terms):
            c = l_coefficient(n, k)
            s = padd(s, ((-1) ** (2 * k + n) * c[0], c[1]))
        at_minus.append(s)
    flips = all(at_minus[n] == ((-1) ** n * low[n][0], low[n][1]) for n in range(0, cut + 2))
    cubes = []
    for n in range(0, cut + 1):
        a = pmul(at_minus[n], at_minus[n + 1])
        cubes.append((a[0] ** 3, a[1] ** 3))
    all_negative = all(c[0] < 0 for c in cubes)
    sum_minus = (0, 1)
    for c in cubes:
        sum_minus = padd(sum_minus, c)
    half_minus = pmul((1, 2), sum_minus)
    leading = pmul((1, 2), red(1, 4 ** 3))
    doubled = pmul((2, 1), (1, 256))
    ok = leading == (1, 128) and leading == doubled and sum_low[0] > 0 and flips and all_negative and half_minus == (-half_low[0], half_low[1])
    scale = 10 ** 12
    print("SU2_GRAM_2D|lattice=(Z/3)x(Z/2)|F=a_W|numerator_at_beta=+1_over_exp(-6)_times_10^12_low=%d|high=%d|numerator_at_beta=-1_over_exp(+6)_times_10^12_partial_sum=%d|l_n(-1)=(-1)^n*l_n(1)=%d|every_term_negative_at_beta=-1=%d|beta^3_coefficient=%s|twice_the_cylinder_value=%s|ok=%d|json=0" % (
        scaled_floor(half_low, scale), scaled_ceiling(half_high, scale), scaled_floor(half_minus, scale), 1 if flips else 0, 1 if all_negative else 0, text(leading), text(doubled), check("SU(2) 2D Gram entry", ok)))


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
        return red(sum_over_weight(hist, trace), 2 ** len(chosen) * group.order ** free), free
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
            direct = red(sum_over_weight(hist, weight, slots), 8 ** free)
            rule = (0, 1)
            for rho in range(5):
                rule = padd(rule, red(c[rho] ** faces, Q8_DIM[rho] ** faces))
            print("TORUS_2D|group=Q8|L=%d|T=%d|F=%d|c=%s|w_on_classes=%s|assignments=%d|Z_direct=%s|Z_rule=%s|ok=%d|json=0" % (
                side, extent, faces, ",".join(map(str, c)), ",".join(map(str, weight)), 8 ** free, text(direct), text(rule), check("torus Q8 L=%d T=%d" % (side, extent), direct == rule)))
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
    direct = red(total[0], 24 ** free)
    rule = (0, 1)
    for rho in range(7):
        rule = padd(rule, red(c[rho] ** 4, T2_DIM[rho] ** 4))
    ok = total[1] == 0 and direct == rule
    print("TORUS_2D|group=2T|L=2|T=2|F=4|c_on_1,w,w2,3,2,2w,2w2=%s|weight_is_complex=%d|assignments=%d|imaginary_part=%d|Z_direct=%s|Z_rule=%s|ok=%d|json=0" % (
        ",".join(map(str, c)), 1 if any(v[1] for v in weight) else 0, 24 ** free, total[1], text(direct), text(rule), check("torus 2T", ok)))


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
        print("GRAM_SITE|lattice=(Z/3)x(Z/2)|group=Q8|c=%s|family_size=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (",".join(map(str, c)), len(matrix), 1 if psd else 0, rank, reason, check("site Gram c=%s" % (c,), psd)))
    # This lattice has no plaquette inside a fixed slice, so the site theorem covers a weight of either sign.
    signed = [3, -2, 1, -1, 2]
    matrix = gram_site_matrix(lat, hist, signed)
    psd, rank, reason = psd_exact(matrix)
    in_fixed_slices = len(partition(lat, "site")[1])
    print("GRAM_SITE|lattice=(Z/3)x(Z/2)|group=Q8|weight_values_on_classes=3,-2,1,-1,2|plaquettes_in_the_fixed_slices=%d|family_size=%d|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (in_fixed_slices, len(matrix), 1 if psd else 0, rank, reason, check("site Gram signed weight", psd and in_fixed_slices == 0)))


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
    denominator = 8 ** free
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
                kernel[(b, a)] = value
            matrix = [[kernel[(b, a)] for a in slice_configs] for b in slice_configs]
            psd, rank, reason = psd_exact(matrix)
            blind = True
            for b in slice_configs:
                for a in slice_configs:
                    for g in gauges:
                        moved = tuple(mult[mult[g[x]][a[x]]][inv[g[(x + 1) % side]]] for x in range(side))
                        blind = blind and kernel[(b, moved)] == kernel[(b, a)]
            ok = psd == want_psd and blind and (not psd or rank == 5)
            print("EVERY_FUNCTION|lattice=(Z/%d)x(Z/2)|group=Q8|c=%s|family=all_%d_point_functions_of_the_t=0_slice|PSD=%d|rank=%d|reason=%s|kernel_blind_to_gauge_moves_of_either_slice=%d|ok=%d|json=0" % (
                side, ",".join(map(str, c)), len(slice_configs), 1 if psd else 0, rank, reason, 1 if blind else 0, check("every function on L=%d c=%s" % (side, c), ok)))


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
        psd, rank, reason = psd_exact(matrix)
        ok = psd == want_psd and (not want_psd or rank == 25)
        print("EVERY_FUNCTION_T4|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|family=all_64_point_functions_of_(U(0),U(1))|PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
            ",".join(map(str, c)), 1 if psd else 0, rank, reason, check("every function at T=4 c=%s" % (c,), ok)))
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
    denominator = 8 ** n
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
    # The theorem in full: a signed weight on the open half with a positive one on the fixed slices, and F on the closed half, moved by gauge transformations or not.
    matrix = gram(by_sign(3, 1), [3, -2, 1, -1, 2], closed_size)
    psd, rank, reason = psd_exact(matrix)
    print("SIGNED_OPEN_HALF|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|fixed_slice_weight=3,1|time_like_weight_values_on_classes=3,-2,1,-1,2|family=functions_on_the_closed_half_size_%d|Gram_PSD=%d|rank=%d|reason=%s|ok=%d|json=0" % (
        closed_size, 1 if psd else 0, rank, reason, check("signed weight on the open half stays PSD", psd)))


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
        direct = red(sum_over_weight(direct_hist, weight), 8 ** free)
        forest = red(sum_over_weight(forest_hist, weight), 8 ** forest_free)
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
            direct = red(sum_over_weight(hist_small, weight), 8 ** free_small)
            print("TRANSFER|spatial=(Z/1)x(Z/1)|N_t=%d|group=Q8|c=%s|assignments=%d|Tr_T^N_t_P_over_the_%d_gauge_orbits=%s|Z_direct=%s|BP_symmetric=%d|ok=%d|json=0" % (
                steps, ",".join(map(str, c)), 8 ** free_small, size, text(trace), text(direct), 1 if symmetric else 0, check("transfer on (Z/1)x(Z/1) N_t=%d c=%s" % (steps, c), trace == direct and symmetric)))
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
    # Luescher's temporal gauge with cyclic time: every time link set to 1, no projector. His footnote 3 says it agrees with the ungauged sum only in the infinite volume limit.
    no_v_words = [tuple((l, s) for l, s in lat3.word(p) if l[1] != lat3.time) for p in lat3.plaquettes]
    fixed_hist, fixed_free = class_histogram(lat3, Q8, no_v_words, fix_forest=False)
    temporal = red(sum_over_weight(fixed_hist, weight), 8 ** fixed_free)
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


def main():
    if SABOTAGE in ("no_inverse_on_time_links", "wrong_plane"):
        section_geometry()
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
        section_su2_red()
        section_cylinder()
        lat, hist = gram_pass()
        section_torus(hist)
        section_gram(lat, hist)
        section_gram_t4()
        section_every_function()
        section_every_function_t4_and_site()
        section_signed_site()
        section_transfer()
        print("SCOPE|each_statement_at_a_fixed_finite_lattice_and_fixed_beta=1|uniformity_in_volume_and_spacing=OPEN|lambda_1_and_a_quantitative_gap_for_SU2=OPEN|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0")
    print("REFLECTION_TRANSFER_DONE|failed=%d|json=0" % len(FAILS))
    for name in FAILS:
        print("FAILED|check=%s|json=0" % name.replace(" ", "_"))
    sys.exit(1 if FAILS else 0)


main()
