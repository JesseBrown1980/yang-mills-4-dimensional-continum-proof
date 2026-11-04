#!/usr/bin/env python3
"""YM4-02b, the periodic 1 x L lattice in two dimensions, with L >= 2.

There a plaquette is P_x = A_x V_x A_{x+1}^-1 V_x^-1, which holds V_x twice. Even so, a finite G of strength t agrees with Haar on
every monomial of the a(P_x) = (1/2) Tr P_x of total degree at most t, and the Haar value has the closed form

    E[prod_x a(P_x)^m_x] = 2^-k sum_n prod_x B(m_x, n) / (n+1)^L,    k = sum_x m_x,

with B(m, n) the multiplicity of spin n/2 in (spin 1/2)^m. This script compares that form with exact group sums on Q8, 2T, 2O and
2I, and with L = 1, where each plaquette holds both its links twice and agreement stops at floor(t/2).

usage = test_one_by_l_2d.py [sabotage=NAME]
NAME is one of wrong_multiplicity no_inverse_on_the_plaquette no_inverse_on_the_far_link one_side_of_two_read_as_one a_subset_for_a_group,
and each must exit 1. Dropping either inverse moves one row only: every class of Q8, 2O, 2I and SU(2) is closed under inversion, so the
law of these words cannot see it, and through degree t 2T agrees with SU(2). Only 2T past its strength can, on 1 x 2 at k = 6.
Python standard library, integers only, json=0.
"""
import itertools
import math
import sys

SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage="):
        raise SystemExit("usage = test_one_by_l_2d.py [sabotage=NAME]")
    SABOTAGE = argument.split("=", 1)[1]
if SABOTAGE not in ("", "wrong_multiplicity", "no_inverse_on_the_plaquette", "no_inverse_on_the_far_link", "one_side_of_two_read_as_one", "a_subset_for_a_group"):
    print("usage = test_one_by_l_2d.py [sabotage=NAME]")
    raise SystemExit(2)
FAILS = []


def check(name, ok):
    if not ok:
        FAILS.append(name)
        print("FAILED|check=%s|json=0" % name)


# ---- Exact rationals as reduced integer pairs.
def red(n, d=1):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d) or 1
    return n // g, d // g


def padd(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def text(a):
    return "%d" % a[0] if a[1] == 1 else "%d/%d" % a


# ---- The closed form.
def multiplicity(m, n):
    # B(m, n), the multiplicity of spin n/2 in (spin 1/2)^m: walks of m steps +-1 on the non-negative integers from 0 to n.
    if n > m or (m - n) % 2:
        return 0
    value = (n + 1) * math.comb(m + 1, (m - n) // 2)
    assert value % (m + 1) == 0
    if SABOTAGE == "wrong_multiplicity" and n == m and m >= 1:
        return 2
    return value // (m + 1)


def walk_count(m, n):
    # The same multiplicity by the recursion, for the check below.
    row = [1]
    for _ in range(m):
        new = [0] * (len(row) + 1)
        for j, v in enumerate(row):
            new[j + 1] += v
            if j:
                new[j - 1] += v
        row = new
    return row[n] if n < len(row) else 0


def haar_monomial(powers):
    L = len(powers)
    k = sum(powers)
    total = (0, 1)
    for n in range(min(powers) + 1):
        top = 1
        for m in powers:
            top *= multiplicity(m, n)
        total = padd(total, red(top, int_power(n + 1, L)))
    return red(total[0], total[1] * int_power(2, k))


def int_power(base, exponent):
    assert exponent >= 0
    out = 1
    for _ in range(exponent):
        out *= base
    return out


def compositions(k, parts):
    if parts == 1:
        yield (k,)
        return
    for first in range(k + 1):
        for rest in compositions(k - first, parts - 1):
            yield (first,) + rest


def multinomial(k, powers):
    out = math.factorial(k)
    for m in powers:
        out //= math.factorial(m)
    return out


def haar_x_power(k, L):
    total = (0, 1)
    for powers in compositions(k, L):
        value = haar_monomial(powers)
        total = padd(total, red(multinomial(k, powers) * value[0], value[1]))
    return total


# ---- The four groups, as doubled unit quaternions over Z, Z[sqrt 2] and Z[phi]. A coordinate (a, b) means a + b w with w^2 = p w + q.
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


class Group:
    def __init__(self, name, times, elements, strength):
        self.name, self.times, self.strength = name, times, strength
        index = {e: i for i, e in enumerate(elements)}
        assert len(index) == len(elements)
        self.size = len(elements)
        self.mult = [[index[product(times, x, y)] for y in elements] for x in elements]
        self.inv = [index[(e[0], (-e[1][0], -e[1][1]), (-e[2][0], -e[2][1]), (-e[3][0], -e[3][1]))] for e in elements]
        self.one = index[ints(2, 0, 0, 0)]
        # Half the trace of g is half its doubled real coordinate, and the doubled real coordinate is a ring element.
        self.values = sorted({e[0] for e in elements})
        where = {v: i for i, v in enumerate(self.values)}
        self.trace_id = [where[e[0]] for e in elements]


def valid(group):
    size = range(group.size)
    m, inv, one = group.mult, group.inv, group.one
    return (all(m[one][g] == g == m[g][one] and m[g][inv[g]] == one for g in size)
            and all(m[m[a][b]][c] == m[a][m[b][c]] for a in size for b in size for c in size))


def ring_power(times, x, n):
    out = (1, 0)
    for _ in range(n):
        out = times(out, x)
    return out


def group_monomial(group, histogram, total, powers):
    # E[prod a^m] from the histogram of trace values; a = (doubled real coordinate) / 2. Returns (a, b, d) for (a + b w) / d.
    rational, surd = 0, 0
    for key, count in histogram.items():
        term = (1, 0)
        for value_id, m in zip(key, powers):
            term = group.times(term, ring_power(group.times, group.values[value_id], m))
        rational += count * term[0]
        surd += count * term[1]
    return rational, surd, total * int_power(2, sum(powers))


def histogram_1xl(group, L):
    # Gauge fixed: V_0 .. V_{L-2} = 1, which leaves A_0 .. A_{L-1} and V_{L-1}, and a(P_x) depends on gauge-invariant data only.
    m, inv, tid = group.mult, group.inv, group.trace_id
    elements = range(group.size)
    hist = {}
    total = 0
    if SABOTAGE == "a_subset_for_a_group":
        elements = range(group.size - 1)
    for links in itertools.product(elements, repeat=L):
        ids = [tid[m[links[x]][inv[links[x + 1]]]] for x in range(L - 1)]
        first, last = links[0] if SABOTAGE == "no_inverse_on_the_far_link" else inv[links[0]], links[L - 1]
        for v in elements:
            if SABOTAGE == "no_inverse_on_the_plaquette":
                closing = m[m[m[last][v]][first]][v]
            else:
                closing = m[m[m[last][v]][first]][inv[v]]
            key = tuple(ids) + (tid[closing],)
            hist[key] = hist.get(key, 0) + 1
            total += 1
    return hist, total


def full_histogram_1xl(group, L):
    # No gauge fixing, to confirm the reduction on small cases.
    m, inv, tid = group.mult, group.inv, group.trace_id
    hist = {}
    total = 0
    for links in itertools.product(range(group.size), repeat=2 * L):
        A, V = links[:L], links[L:]
        key = []
        for x in range(L):
            y = (x + 1) % L
            key.append(tid[m[m[m[A[x]][V[x]]][inv[A[y]]]][inv[V[x]]]])
        key = tuple(key)
        hist[key] = hist.get(key, 0) + 1
        total += 1
    return hist, total


def histogram_1x1(group):
    m, inv, tid = group.mult, group.inv, group.trace_id
    hist = {}
    total = 0
    for a in range(group.size):
        for b in range(group.size):
            key = (tid[m[m[m[a][b]][inv[a]]][inv[b]]],)
            hist[key] = hist.get(key, 0) + 1
            total += 1
    return hist, total


def equal_to_haar(moment, haar):
    rational, surd, denominator = moment
    return surd == 0 and rational * haar[1] == haar[0] * denominator


def read(moment):
    rational, surd, denominator = moment
    if surd == 0:
        return text(red(rational, denominator))
    return "(%d+%dw)/%d" % (rational, surd, denominator)


def x_power_moment(group, histogram, total, k, L):
    rational, surd = 0, 0
    for powers in compositions(k, L):
        r, s, _ = group_monomial(group, histogram, total, powers)
        c = multinomial(k, powers)
        rational += c * r
        surd += c * s
    return rational, surd, total * int_power(2, k)


GROUPS = {
    "Q8": Group("Q8", Z, Q8_ELEMENTS, 3),
    "2T": Group("2T", Z, T2_ELEMENTS, 5),
    "2O": Group("2O", ROOT2, O2_ELEMENTS, 7),
    "2I": Group("2I", PHI, I2_ELEMENTS, 11),
}
for name, group in GROUPS.items():
    ok = valid(group) and group.size == {"Q8": 8, "2T": 24, "2O": 48, "2I": 120}[name]
    check("group_table_of_%s" % name, ok)

# The closed form's multiplicities, against the recursion.
pairs = [(m, n) for m in range(0, 25) for n in range(0, m + 1)]
bad = sum(1 for m, n in pairs if multiplicity(m, n) != walk_count(m, n))
check("multiplicity_against_the_walk_count", bad == 0)
print("ONE_BY_L_MULTIPLICITY|pairs=%d|differ=%d|json=0" % (len(pairs), bad))

# Values the closed form must give, read by hand in the lemma.
known = ((2, 2, (5, 8)), (3, 3, (3, 32)), (4, 3, (3, 2)), (5, 3, (15, 32)), (4, 2, (11, 12)), (6, 2, (465, 256)), (8, 2, (1351, 320)))
for k, L, value in known:
    check("closed_form_X^%d_on_1x%d" % (k, L), haar_x_power(k, L) == value)
print("ONE_BY_L_CLOSED_FORM|%s|json=0" % "|".join("E[X^%d]_1x%d=%s" % (k, L, text(haar_x_power(k, L))) for k, L, _ in known))
one_a = haar_monomial((1,))
one_a2 = haar_monomial((2,))
check("closed_form_on_1x1", one_a == (1, 4) and one_a2 == (1, 3))
print("ONE_BY_ONE_SU2|E_a=%s|E_a2=%s|json=0" % (text(one_a), text(one_a2)))

# The gauge-fixed reduction against the full sum, on the cases small enough to read in full.
for name, L in (("Q8", 2), ("Q8", 3)):
    group = GROUPS[name]
    fixed, fixed_total = histogram_1xl(group, L)
    full, full_total = full_histogram_1xl(group, L)
    same = all(fixed.get(k, 0) * full_total == full.get(k, 0) * fixed_total for k in set(fixed) | set(full))
    check("gauge_fixed_reduction_%s_1x%d" % (name, L), same)
    print("ONE_BY_L_REDUCTION|group=%s|L=%d|fixed=%d|full=%d|same=%d|json=0" % (name, L, fixed_total, full_total, 1 if same else 0))

# The theorem's rows: every monomial through degree t, and the first k at which X^k differs.
# The second seat's filed values past each group's strength pin the plaquette word, including its inverses.
FILED = {("Q8", 2): "5/2", ("2T", 2): "25/12", ("2O", 2): "2245/512"}
CASES = (("Q8", 2), ("Q8", 3), ("Q8", 4), ("Q8", 5), ("2T", 2), ("2T", 3), ("2T", 4), ("2O", 2), ("2O", 3), ("2I", 2))
if SABOTAGE == "one_side_of_two_read_as_one":
    CASES = (("Q8", 1),)
for name, L in CASES:
    group = GROUPS[name]
    t = group.strength
    hist, total = histogram_1xl(group, L) if L >= 2 or SABOTAGE != "one_side_of_two_read_as_one" else histogram_1x1(group)
    monomials = wrong = 0
    for k in range(1, t + 1):
        for powers in compositions(k, L):
            monomials += 1
            if not equal_to_haar(group_monomial(group, hist, total, powers), haar_monomial(powers)):
                wrong += 1
    check("every_monomial_through_t_%s_1x%d" % (name, L), wrong == 0)
    moment = x_power_moment(group, hist, total, t + 1, L)
    haar = haar_x_power(t + 1, L)
    differs = not equal_to_haar(moment, haar)
    check("X^(t+1)_differs_%s_1x%d" % (name, L), differs)
    if (name, L) in FILED:
        check("filed_value_%s_1x%d" % (name, L), read(moment) == FILED[(name, L)])
    print("ONE_BY_L|group=%s|L=%d|t=%d|assignments=%d|monomials_through_t=%d|wrong=%d|k=%d|E_G=%s|E_Haar=%s|differs=%d|json=0" % (name, L, t, total, monomials, wrong, t + 1, read(moment), text(haar), 1 if differs else 0))

# L = 1: both links twice in the plaquette, and agreement stops at floor(t/2).
for name, group in GROUPS.items():
    t = group.strength
    hist, total = histogram_1x1(group)
    through = 0
    for k in range(1, t + 2):
        if equal_to_haar(group_monomial(group, hist, total, (k,)), haar_monomial((k,))):
            through = k
        else:
            break
    check("side_one_stops_at_floor(t/2)_%s" % name, through == t // 2)
    moment = group_monomial(group, hist, total, (through + 1,))
    print("ONE_BY_ONE|group=%s|t=%d|assignments=%d|agrees_through=%d|k=%d|E_G=%s|E_Haar=%s|json=0" % (name, t, total, through, through + 1, read(moment), text(haar_monomial((through + 1,)))))

print("SCOPE|periodic_1xL_in_two_dimensions=1|higher_dimensions_with_one_side_of_1=OPEN|uniform_bridge_at_large_beta=OPEN|json=0")
print("ONE_BY_L_DONE|failed=%d|json=0" % len(FAILS))
raise SystemExit(1 if FAILS else 0)
