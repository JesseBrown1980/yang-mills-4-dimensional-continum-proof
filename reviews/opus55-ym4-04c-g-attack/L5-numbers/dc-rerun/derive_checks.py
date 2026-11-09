#!/usr/bin/env python3
"""
YM4-04C, the freeze commit: small exact checks of facts the rows of docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp
rest on (note section 14). Integers only, with rationals as reduced integer numerator/denominator pairs, the standard library
only, json=0. No float enters: the file holds no float literal, no true-division operator and no negative power, and it checks
that of its own source before it runs.

A. Fuss-Catalan. F_20(n) = C(20n, n)/(19n + 1) = C(20n, n - 1)/n as exact integers; the frozen values F_20(4..12) and
   6F_20(1..5); F_20(2) = 20 against F_19(2) = 19; the product formula of Lemma 3.11, strict increase and the bound below
   mu = 20^20/19^19 for n <= 59; mu in [53.00068, 53.00069]; F_20(n+2)/F_20(n); the C03 counting-gap arithmetic.
B. The W07 aligned tile. The 12 links of a fine 2x2 tile as exact rational unit quaternions, its 4 plaquettes and its
   boundary holonomy, the ratio (1 - a(V'))/(1 - a(U_p)), and the identity 16 - 40e + 32e^2 - 8e^3 = 8(1 - e)^2 (2 - e).
C. The alias rationals at b = 2 and b = 4. The coarse Gaussian propagator of the line map for a transverse polarization,
   C'(p) = b^(2-d) sum over aliases with n_mu = 0, evaluated as an exact rational function of sigma = sin^2(q/2): the W01
   profile and corners, the W03 profile and corners, d = 2, and the slopes A_1, A_2 (d = 4) and A(2,3), A(4,3) both from
   their lattice-sum definition and as the exact limit of (1/r - 1)/phat^2 at sigma -> 0.
D. The b = 8 slopes. A(8,4) = A_3 and A(8,3) in Q(sqrt2), where the sqrt2 parts cancel; the W03 increments; A_k/2^k.
E. W05. The transverse corner in the covariant gauges xi = 1/2, 1, 3 and the three longitudinal ratios (xi/4)/C'_nunu(xi).
F. C10b's moment identity at one rational coarse configuration: E_pi[(chi_b + chi_t)^(2m)] = Cat_m (2 + chi_1/2(V))^m for
   m <= 6 and the odd moments 0, by exact monomial integration over the unit 3-sphere (Haar measure on SU(2)).
G. Small constants: Machin's identity and pi > 333/106 > 80000/25467, so 8/(3 pi) < 848/999 < 8489/10000 (Lemmas 3.2, 4.22);
   1/(8 N_p) on 8^4, 12^4, 16^4 (C17).

Run as python3 -I -B derive_checks.py. Its output is DERIVE-CHECKS.hbp beside it, byte for byte.
"""
import io
import itertools
import sys
import tokenize
from math import comb, factorial, gcd

CHECKS = [0]
FAILED = [0]
ROWS = []


def say(text):
    ROWS.append(text)
    sys.stdout.write(text + "\n")


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILED[0] += 1
        say("FAILED|check=" + name + "|" + detail + "|json=0")
    return ok


# ---- exact rationals as reduced (numerator, denominator) integer pairs with denominator > 0

def fr(n, d=1):
    """the reduced pair n/d, with the sign on the numerator; equal rationals give equal pairs."""
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    return (n // g, d // g)


def qadd(a, b):
    return fr(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qsub(a, b):
    return fr(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def qneg(a):
    return (-a[0], a[1])


def qmul(a, b):
    return fr(a[0] * b[0], a[1] * b[1])


def qdiv(a, b):
    """a / b as a reduced pair, by the cross products, without the true-division operator."""
    assert b[0] != 0
    return fr(a[0] * b[1], a[1] * b[0])


def ipow(base, k):
    """base^k for an integer k >= 0 by repeated multiplication; a negative exponent is refused."""
    assert k >= 0
    r = 1
    for _ in range(k):
        r *= base
    return r


def qpow(a, k):
    return fr(ipow(a[0], k), ipow(a[1], k))


def qsum(xs):
    s = fr(0)
    for x in xs:
        s = qadd(s, x)
    return s


def qprod(xs):
    p = fr(1)
    for x in xs:
        p = qmul(p, x)
    return p


def qlt(a, b):
    return a[0] * b[1] < b[0] * a[1]


def qle(a, b):
    return a[0] * b[1] <= b[0] * a[1]


def qs(x):
    return str(x[0]) if x[1] == 1 else str(x[0]) + "/" + str(x[1])


def dec(x, places):
    """the decimal string of floor(x * 10^places) / 10^places, for display, by integer arithmetic."""
    sign = "-" if x[0] < 0 else ""
    n = (abs(x[0]) * ipow(10, places)) // x[1]
    s = str(n).rjust(places + 1, "0")
    return sign + s[:-places] + "." + s[-places:]


def inside(x, lo, hi):
    return qle(lo, x) and qle(x, hi)


# ---- the no-float self-check of this source

def self_check():
    src = open(__file__, encoding="utf-8").read()
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    bad_num = [t.string for t in toks if t.type == tokenize.NUMBER
               and any(c in t.string.lower() for c in ".ej") and not t.string.lower().startswith("0x")]
    bad_div = [t.start[0] for t in toks if t.type == tokenize.OP and t.string in ("/", "/=")]
    bad_pow = [toks[i].start[0] for i in range(len(toks) - 1)
               if toks[i].type == tokenize.OP and toks[i].string == "**" and toks[i + 1].string == "-"]
    bad_name = [t.string for t in toks if t.type == tokenize.NAME and t.string in ("float", "sqrt", "exp", "log", "pi", "sin", "cos")]
    ok = not (bad_num or bad_div or bad_pow or bad_name)
    check("no_float_source", ok, "numbers=%s;div_lines=%s;neg_pow_lines=%s;names=%s" % (bad_num, bad_div, bad_pow, bad_name))
    say("YM4_04C_DC_NO_FLOAT|float_literals=%d|true_division_ops=%d|negative_powers=%d|float_names=%d|tag=MEASURED|json=0" % (
        len(bad_num), len(bad_div), len(bad_pow), len(bad_name)))


# ---- A. Fuss-Catalan

def F(n, D=20):
    c = comb(D * n, n)
    q, r = divmod(c, (D - 1) * n + 1)
    assert r == 0
    if n >= 1:
        q2, r2 = divmod(comb(D * n, n - 1), n)
        assert r2 == 0 and q2 == q
    return q


def part_a():
    frozen = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150, 117544525178080,
              5406686759963586, 251754316822792420]
    vals = [F(n) for n in range(4, 13)]
    check("F20_4_12", vals == frozen)
    six = [6 * F(n) for n in range(1, 6)]
    check("6F20_1_5", six == [6, 120, 3540, 123240, 4705470])
    check("F20_2_vs_F19_2", F(2) == 20 and F(2, 19) == 19)
    mu = fr(20 ** 20, 19 ** 19)
    mu_ok = 5300068 * 19 ** 19 <= 100000 * 20 ** 20 <= 5300069 * 19 ** 19
    check("mu_bracket", mu_ok)
    ok, prev = True, None
    for n in range(0, 60):
        r = fr(F(n + 1), F(n))
        prod = fr(20)
        for j in range(1, 20):
            prod = qmul(prod, fr(20 * n + j, 19 * n + j + 1))
        ok = ok and r == prod and qlt(r, mu) and (prev is None or qlt(prev, r))
        prev = r
    check("ratio_product_increasing_below_mu_n0_59", ok)
    r108, r1210 = fr(F(10), F(8)), fr(F(12), F(10))
    check("F10_over_F8", inside(r108, fr(201684, 100), fr(201685, 100)))
    check("F12_over_F10", inside(r1210, fr(214177, 100), fr(214178, 100)))
    first = min(n for n in range(1, 40) if qlt(fr(2000), fr(F(n + 2), F(n))))
    check("F_n2_over_F_n_above_2000_from_8", first == 8)
    gaps = [fr(6 * F(8), 32), fr(6 * F(10), 304), fr(6 * F(12), 2326)]
    check("counting_gaps", inside(gaps[0], fr(109 * 10 ** 8), fr(110 * 10 ** 8)) and inside(gaps[1], fr(231 * 10 ** 10), fr(233 * 10 ** 10))
          and inside(gaps[2], fr(649 * 10 ** 12), fr(650 * 10 ** 12)))
    g1, g2 = fr(304, 32), fr(2326, 304)
    check("growth_ratios", g1 == fr(19, 2) and g2 == fr(1163, 152) and inside(g2, fr(765, 100), fr(766, 100)))
    check("growth_square_roots", inside(g1, qpow(fr(308, 100), 2), qpow(fr(309, 100), 2)) and inside(g2, qpow(fr(276, 100), 2), qpow(fr(277, 100), 2)))
    say("YM4_04C_DC_FUSS_CATALAN|F_20(4..12)=%s|6F_20(1..5)=%s|F_20(2)=20|F_19(2)=19|mu_in_[53.00068,53.00069]=%d|"
        "ratio=20*prod_j(20n+j)/(19n+j+1),increasing,below_mu_n=0..59|F(10)/F(8)=%s|F(12)/F(10)=%s|F(n+2)/F(n)>2000_from_n=%d|tag=MEASURED|json=0" % (
            ",".join(str(v) for v in vals), ",".join(str(v) for v in six), int(mu_ok), dec(r108, 4), dec(r1210, 4), first))
    say("YM4_04C_DC_COUNTING_GAP|6F(8)/N(8)=%s|6F(10)/N(10)=%s|6F(12)/N(12)=%s|N(10)/N(8)=%s|N(12)/N(10)=%s|"
        "sqrt_brackets=[3.08,3.09],[2.76,2.77]|counts=C03,CONJECTURE|tag=MEASURED_arithmetic_of_a_CONJECTURE|json=0" % (
            qs(gaps[0]), qs(gaps[1]), qs(gaps[2]), qs(g1), qs(g2)))


# ---- quaternions (w, x, y, z) with rational-pair entries

def qdot(signs, xs, ys):
    return qsum(qmul(fr(s), qmul(x, y)) for s, x, y in zip(signs, xs, ys))


def hmul(a, b):
    b0, b1, b2, b3 = b
    return (qdot((1, -1, -1, -1), a, (b0, b1, b2, b3)),
            qdot((1, 1, 1, -1), a, (b1, b0, b3, b2)),
            qdot((1, -1, 1, 1), a, (b2, b3, b0, b1)),
            qdot((1, 1, -1, 1), a, (b3, b2, b1, b0)))


def hconj(a):
    return (a[0], qneg(a[1]), qneg(a[2]), qneg(a[3]))


def hnorm2(a):
    return qsum(qmul(x, x) for x in a)


ONE = (fr(1), fr(0), fr(0), fr(0))


def hpow(a, k):
    r = ONE
    for _ in range(k):
        r = hmul(r, a)
    return r


# ---- B. the W07 aligned tile

def part_b():
    stated = {fr(63, 65): fr(4064256, 274625), fr(255, 257): fr(266342400, 16974593), fr(1023, 1025): fr(17146331136, 1076890625)}
    sines = {fr(63, 65): fr(16, 65), fr(255, 257): fr(32, 257), fr(1023, 1025): fr(64, 1025)}
    poly = [16, -40, 32, -8]
    a1 = [1, -2, 1]                    # (1 - e)^2
    a2 = [2, -1]                       # (2 - e)
    prod = [0] * 4
    for i, x in enumerate(a1):
        for j, y in enumerate(a2):
            prod[i + j] += 8 * x * y
    check("aligned_tile_polynomial_identity", prod == poly)
    out = []
    for c, ratio in stated.items():
        s = sines[c]
        g = (c, fr(0), fr(0), s)
        check("unit_" + qs(c), hnorm2(g) == fr(1))
        # links of the tile [0,2]^2 in the plane (1,2): U_1 = 1, U_2(x) = g^{x_1}
        U1 = {(x1, x2): ONE for x1 in range(2) for x2 in range(3)}
        U2 = {(x1, x2): hpow(g, x1) for x1 in range(3) for x2 in range(2)}
        check("twelve_links_" + qs(c), len(U1) + len(U2) == 12)
        eps_all = []
        for x1 in range(2):
            for x2 in range(2):
                h = hmul(hmul(U1[(x1, x2)], U2[(x1 + 1, x2)]), hmul(hconj(U1[(x1, x2 + 1)]), hconj(U2[(x1, x2)])))
                eps_all.append(qsub(fr(1), h[0]))
        eps = qsub(fr(1), c)
        check("plaquettes_" + qs(c), all(e == eps for e in eps_all))
        V = ONE
        path = [U1[(0, 0)], U1[(1, 0)], U2[(2, 0)], U2[(2, 1)], hconj(U1[(1, 2)]), hconj(U1[(0, 2)]), hconj(U2[(0, 1)]), hconj(U2[(0, 0)])]
        for u in path:
            V = hmul(V, u)
        r = qdiv(qsub(fr(1), V[0]), eps)
        pv = qsum(qmul(fr(poly[k]), qpow(eps, k)) for k in range(4))
        ok = (r == ratio and r == pv and r == qprod([fr(8), qpow(qsub(fr(1), eps), 2), qsub(fr(2), eps)]) and qlt(r, fr(16))
              and qle(qsub(fr(1), V[0]), qmul(fr(4), qsum(eps_all))))
        check("aligned_ratio_" + qs(c), ok)
        out.append("cos=%s:ratio=%s" % (qs(c), qs(r)))
    say("YM4_04C_DC_ALIGNED_TILE|%s|each_equal_to_16-40e+32e^2-8e^3=8(1-e)^2(2-e)_at_e=1-cos|each_below_16|"
        "1-a(V')<=4sum(1-a(U_p))|tag=MEASURED|json=0" % ";".join(out))


# ---- polynomials in sigma (coefficient lists of rational pairs, lowest degree first) and rational functions

def padd(p, q):
    n = max(len(p), len(q))
    return [qadd(p[i] if i < len(p) else fr(0), q[i] if i < len(q) else fr(0)) for i in range(n)]


def pmul(p, q):
    r = [fr(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] = qadd(r[i + j], qmul(x, y))
    return r


def pscale(c, p):
    return [qmul(c, x) for x in p]


def peval(p, s):
    return qsum(qmul(c, qpow(s, k)) for k, c in enumerate(p))


def radd(a, b):
    return (padd(pmul(a[0], b[1]), pmul(b[0], a[1])), pmul(a[1], b[1]))


def valuation(p):
    for k, c in enumerate(p):
        if c[0] != 0:
            return k, c
    return None, fr(0)


# 4 sin^2(pi n/b) for n in Z_b, b = 2, 4: rational
SIN2 = {2: [fr(0), fr(4)], 4: [fr(0), fr(2), fr(4), fr(2)]}


def pairsum(b, X):
    """sum over n_nu in Z_b of 1/(4 sin^2((q + 2 pi n_nu)/(2b)) + X), as a rational function of sigma = sin^2(q/2).
    b = 2: (4 + 2X)/(4 sigma + 4X + X^2). b = 4: (4 + 2X)(2Y - 4)/(Y^2 - 4Y + 4 sigma), Y = (2 + X)^2."""
    four_plus_2x = qadd(fr(4), qmul(fr(2), X))
    if b == 2:
        return ([four_plus_2x], [qadd(qmul(fr(4), X), qmul(X, X)), fr(4)])
    Y = qpow(qadd(fr(2), X), 2)
    return ([qmul(four_plus_2x, qsub(qmul(fr(2), Y), fr(4)))], [qsub(qmul(Y, Y), qmul(fr(4), Y)), fr(4)])


def Cprime(b, d):
    """C'(sigma) = b^(2-d) sum over the d - 2 directions other than mu and nu (each n_lambda in Z_b) of pairsum."""
    total = ([fr(0)], [fr(1)])
    for ns in itertools.product(range(b), repeat=d - 2):
        X = qsum(SIN2[b][n] for n in ns)
        total = radd(total, pairsum(b, X))
    num = pscale(qdiv(qpow(fr(b), 2), qpow(fr(b), d)), total[0])
    return (num, total[1])


def r_at(b, d, sigma):
    num, den = Cprime(b, d)
    C = qdiv(peval(num, sigma), peval(den, sigma))
    return qdiv(qdiv(fr(1), qmul(fr(4), sigma)), C)


def slope_limit(b, d):
    """lim_{sigma->0} (4 sigma b^(d-4) C'(sigma) - 1)/(4 sigma): the normalized slope A of the alias formula."""
    num, den = Cprime(b, d)
    norm = qdiv(qpow(fr(b), d), qpow(fr(b), 4))
    Fn = padd(pscale(qmul(fr(4), norm), [fr(0)] + num), pscale(fr(-1), den))   # (4 sigma norm num - den), over den
    Fd = pscale(fr(4), [fr(0)] + den)                                            # times 1/(4 sigma)
    vn, cn = valuation(Fn)
    vd, cd = valuation(Fd)
    v0n, c0n = valuation(padd(pscale(qmul(fr(4), norm), [fr(0)] + num), [fr(0)]))
    v0d, c0d = valuation(den)
    marginal = (v0n == v0d and c0n == c0d)                                       # 4 sigma norm C' -> 1
    if vn is None:                                                               # 4 sigma norm C' = 1 identically (d = 2)
        return fr(0), marginal
    if vn > vd:
        return fr(0), marginal
    assert vn == vd
    return qdiv(cn, cd), marginal


def A_def(b, d):
    """b^-2 sum_{n in Z_b^(d-1), n != 0} 1/khat^2(2 pi n/b) - (1 - b^-2)/12, for b = 2, 4 (rational)."""
    s = fr(0)
    for n in itertools.product(range(b), repeat=d - 1):
        if any(n):
            s = qadd(s, qdiv(fr(1), qsum(SIN2[b][m] for m in n)))
    return qsub(qdiv(s, fr(b * b)), qdiv(qsub(fr(1), qdiv(fr(1), fr(b * b))), fr(12)))


def part_c():
    ts = [fr(1, 16), fr(1, 8), fr(1, 4), fr(1, 2), fr(1)]
    sig = [qdiv(qmul(t, t), qadd(fr(1), qmul(t, t))) for t in ts] + [fr(1)]   # q = pi: sigma = 1
    w01 = [fr(12689633, 12736932), fr(813281, 825252), fr(56033, 59172), fr(4961, 5892), fr(833, 1212), fr(15, 28)]
    prof = [r_at(2, 4, s) for s in sig]
    check("W01_profile_b2", prof == w01)
    check("W01_profile_decreasing", all(qlt(prof[i + 1], prof[i]) for i in range(5)))
    r2c = r_at(4, 4, fr(1))
    check("W01_corner_r2", r2c == fr(25823, 98640))
    A1, m1 = slope_limit(2, 4)
    A2, m2 = slope_limit(4, 4)
    check("W01_A1", A1 == fr(23, 96) and A_def(2, 4) == fr(23, 96) and m1)
    check("W01_A2", A2 == fr(1367, 1920) and A_def(4, 4) == fr(1367, 1920) and m2)
    two_r1, four_r2 = qmul(fr(2), prof[5]), qmul(fr(4), r2c)
    check("W01_2k_rk", two_r1 == fr(15, 14) and four_r2 == fr(25823, 24660) and qlt(four_r2, two_r1))
    w03 = [fr(2057, 4120), fr(521, 1048), fr(137, 280), fr(41, 88), fr(17, 40), fr(3, 8)]
    prof3 = [r_at(2, 3, s) for s in sig]
    check("W03_profile_b2_d3", prof3 == w03)
    c3_2, c3_4 = qmul(fr(2), r_at(2, 3, fr(1))), qmul(fr(4), r_at(4, 3, fr(1)))
    check("W03_corners", c3_2 == fr(3, 4) and c3_4 == fr(119, 208))
    A23, m23 = slope_limit(2, 3)
    A43, m43 = slope_limit(4, 3)
    check("W03_A_b2_b4", A23 == fr(3, 32) and A_def(2, 3) == fr(3, 32) and A43 == fr(73, 384) and A_def(4, 3) == fr(73, 384) and m23 and m43)
    d2 = []
    for b in (2, 4):
        for s in (fr(1, 2), fr(3, 4), fr(1)):                                 # q = pi/2, 2pi/3, pi
            d2.append(r_at(b, 2, s) == fr(1, b * b))
        Ad, md = slope_limit(b, 2)
        d2.append(Ad == fr(0) and md)
    check("W03_d2_exact_closure", all(d2))
    say("YM4_04C_DC_ALIAS_B2_B4|W01_r_1(t_W=1/16,1/8,1/4,1/2,1;q=pi)=%s|r_2(pi)=%s|A_1=%s|A_2=%s|2r_1(pi)=%s|4r_2(pi)=%s|"
        "r->1_as_q->0=%d|slopes_by_definition_and_by_the_alias_limit_agree=1|tag=MEASURED|json=0" % (
            ",".join(qs(x) for x in prof), qs(r2c), qs(A1), qs(A2), qs(two_r1), qs(four_r2), int(m1 and m2)))
    say("YM4_04C_DC_ALIAS_D3_D2|W03_r_1_d=3=%s|b*r(pi)_b=2,4=%s,%s|A(2,3)=%s|A(4,3)=%s|d=2:r=1/b^2_at_q=pi/2,2pi/3,pi_and_A=0_at_b=2,4=%d|tag=MEASURED|json=0" % (
        ",".join(qs(x) for x in prof3), qs(c3_2), qs(c3_4), qs(A23), qs(A43), int(all(d2))))


# ---- D. b = 8 in Q(sqrt2): pairs (p, q) of rational pairs meaning p + q sqrt2

def s2add(a, b):
    return (qadd(a[0], b[0]), qadd(a[1], b[1]))


def s2mul(a, b):
    return (qadd(qmul(a[0], b[0]), qmul(fr(2), qmul(a[1], b[1]))), qadd(qmul(a[0], b[1]), qmul(a[1], b[0])))


def s2inv(a):
    n = qsub(qmul(a[0], a[0]), qmul(fr(2), qmul(a[1], a[1])))
    assert n[0] != 0
    return (qdiv(a[0], n), qdiv(qneg(a[1]), n))


def s2sign(a):
    p, q = a                                                                   # each pair has the sign of its numerator
    if q[0] == 0:
        return (p[0] > 0) - (p[0] < 0)
    if p[0] == 0:
        return (q[0] > 0) - (q[0] < 0)
    if p[0] > 0 and q[0] > 0:
        return 1
    if p[0] < 0 and q[0] < 0:
        return -1
    if p[0] > 0:
        return 1 if qlt(qmul(fr(2), qmul(q, q)), qmul(p, p)) else -1
    return 1 if qlt(qmul(p, p), qmul(fr(2), qmul(q, q))) else -1


def A8(d):
    c = [(fr(1), fr(0)), (fr(0), fr(1, 2)), (fr(0), fr(0)), (fr(0), fr(-1, 2)), (fr(-1), fr(0)), (fr(0), fr(-1, 2)), (fr(0), fr(0)), (fr(0), fr(1, 2))]
    tab = [(qsub(fr(2), qmul(fr(2), x[0])), qmul(fr(-2), x[1])) for x in c]  # 4 sin^2(pi m/8) = 2 - 2 cos(pi m/4)
    tot = (fr(0), fr(0))
    for n in itertools.product(range(8), repeat=d - 1):
        if any(n):
            den = (fr(0), fr(0))
            for m in n:
                den = s2add(den, tab[m])
            tot = s2add(tot, s2inv(den))
    return (qsub(qdiv(tot[0], fr(64)), qdiv(qsub(fr(1), fr(1, 64)), fr(12))), qdiv(tot[1], fr(64)))


def part_d():
    a84, a83 = A8(4), A8(3)
    check("A3_rational", a84[1] == fr(0) and a84[0] == fr(113360987, 66106880))
    check("A83_rational", a83[1] == fr(0) and a83[0] == fr(54335, 182784))
    check("A3_bracket", inside(a84[0], fr(17148137531, 10 ** 10), fr(17148137532, 10 ** 10)))
    check("A83_bracket", inside(a83[0], fr(2972634366, 10 ** 10), fr(2972634367, 10 ** 10)))
    inc1, inc2 = qsub(fr(73, 384), fr(3, 32)), qsub(a83[0], fr(73, 384))
    check("W03_increments", inc1 == fr(37, 384) and inc2 == fr(6529, 60928) and inside(inc2, fr(1071592, 10 ** 7), fr(1071593, 10 ** 7))
          and inside(inc1, fr(9, 100), fr(12, 100)) and inside(inc2, fr(9, 100), fr(12, 100)))
    check("W03_old_bracket_excludes", not inside(inc2, fr(10716, 10 ** 5), fr(10717, 10 ** 5)))
    q1, q2, q3 = fr(23, 192), fr(1367, 7680), qdiv(a84[0], fr(8))
    check("A_k_over_2k_increasing_below_G3", qlt(q1, q2) and qlt(q2, q3) and qlt(q3, fr(2527310, 10 ** 7)) and q3 == fr(113360987, 528855040))
    check("Q_sqrt2_sign_test", s2sign((fr(3), fr(-2))) == 1 and s2sign((fr(-3), fr(2))) == -1 and s2sign((fr(1), fr(-1))) == -1)
    say("YM4_04C_DC_B8|A_3=A(8,4)=%s|A(8,3)=%s|sqrt2_parts=0,0|increments_d=3=%s,%s|A_k/2^k=%s,%s,%s|A_3/8<0.2527310=1|tag=MEASURED|json=0" % (
        qs(a84[0]), qs(a83[0]), qs(inc1), qs(inc2), qs(q1), qs(q2), qs(q3)))


# ---- E. W05: covariant gauges at b = 2, d = 4, q = pi

def part_e():
    out_t, out_l = [], []
    for xi in (fr(1, 2), fr(1), fr(3)):
        # transverse mu: weight 4cos^2(k_mu/2) = 4 if n_mu = 0, 0 if n_mu = 1; khat_mu = 0 on the surviving aliases
        Ct = fr(0)
        Cl = fr(0)
        for n in itertools.product(range(2), repeat=4):                      # (n_nu, n_mu, n_l1, n_l2)
            khn2 = fr(2)                                                        # 4 sin^2(pi/4 + pi n_nu/2) = 2
            others = [SIN2[2][m] for m in n[1:]]
            kh2 = qadd(khn2, qsum(others))
            khmu2 = others[0]
            wmu = fr(4) if n[1] == 0 else fr(0)
            Gmumu = qdiv(qsub(fr(1), qmul(qsub(fr(1), xi), qdiv(khmu2, kh2))), kh2)
            Ct = qadd(Ct, qmul(wmu, Gmumu))
            Gnunu = qdiv(qsub(fr(1), qmul(qsub(fr(1), xi), qdiv(khn2, kh2))), kh2)
            Cl = qadd(Cl, qmul(fr(2), Gnunu))                                   # 4 cos^2(pi/4 + pi n_nu/2) = 2
        Ct, Cl = qdiv(Ct, fr(16)), qdiv(Cl, fr(16))
        out_t.append(qdiv(fr(1, 4), Ct))
        out_l.append(qdiv(qdiv(xi, fr(4)), Cl))
    check("W05_transverse", all(x == fr(15, 28) for x in out_t))
    check("W05_longitudinal", out_l == [fr(3675, 7372), fr(35, 48), fr(11025, 10456)] and len(set(out_l)) == 3)
    say("YM4_04C_DC_W05|transverse_corner_xi=1/2,1,3=%s|longitudinal_(xi/4)/C'_nunu_xi=1/2,1,3=%s|pairwise_unequal=1|tag=MEASURED|json=0" % (
        ",".join(qs(x) for x in out_t), ",".join(qs(x) for x in out_l)))


# ---- F. the Catalan moment identity at one rational coarse configuration

def dfact(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def sphere_moment(e):
    """E[prod pi_i^e_i] for pi uniform on the unit 3-sphere: 0 unless every e_i is even;
    otherwise prod (e_i - 1)!! / (2^K (K + 1)!), K = sum e_i / 2 (REPORTED: the moments of the uniform measure on S^3)."""
    if any(x % 2 for x in e):
        return fr(0)
    Kk = sum(e) // 2                                                            # exact: every e_i is even here
    return fr(eval_prod([dfact(x - 1) for x in e]), ipow(2, Kk) * factorial(Kk + 1))


def eval_prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def part_f():
    # cross-check of the sphere moments against Lemma 3.2 item 2: E[a^(2m)] = 4^-m (2m)!/(m!(m+1)!)
    ok = all(sphere_moment((2 * m, 0, 0, 0)) == fr(factorial(2 * m), ipow(4, m) * factorial(m) * factorial(m + 1)) for m in range(7))
    check("sphere_moments_vs_Lemma_3_2", ok)
    A = (fr(1, 5), fr(2, 5), fr(2, 5), fr(4, 5))
    Bq = (fr(2, 3), fr(1, 3), fr(0), fr(2, 3))
    check("unit_A_B", hnorm2(A) == fr(1) and hnorm2(Bq) == fr(1))
    chi = qmul(fr(2), hmul(A, Bq)[0])                                         # chi_1/2(V) = tr(AB) = 2 Re(AB)
    basis = [ONE, (fr(0), fr(1), fr(0), fr(0)), (fr(0), fr(0), fr(1), fr(0)), (fr(0), fr(0), fr(0), fr(1))]
    # L(pi) = tr(A pi) + tr(pi^-1 B) = 2 Re(A pi) + 2 Re(conj(pi) B), linear in the coordinates of pi
    w = [qadd(qmul(fr(2), hmul(A, e)[0]), qmul(fr(2), hmul(hconj(e), Bq)[0])) for e in basis]
    check("norm_identity", qsum(qmul(x, x) for x in w) == qmul(fr(4), qadd(fr(2), chi)))
    moments = []
    for M in range(0, 13):
        tot = fr(0)
        for e in itertools.product(range(M + 1), repeat=4):
            if sum(e) != M:
                continue
            coef = factorial(M) // (factorial(e[0]) * factorial(e[1]) * factorial(e[2]) * factorial(e[3]))   # exact: a multinomial
            tot = qadd(tot, qprod([fr(coef), qpow(w[0], e[0]), qpow(w[1], e[1]), qpow(w[2], e[2]), qpow(w[3], e[3]), sphere_moment(e)]))
        moments.append(tot)
    cat = [qmul(fr(catalan(m)), qpow(qadd(fr(2), chi), m)) for m in range(7)]
    ok_even = all(moments[2 * m] == cat[m] for m in range(7))
    ok_odd = all(moments[2 * m + 1] == fr(0) for m in range(6))
    check("catalan_moment_identity", ok_even and ok_odd)
    # the C10c leading-order input is not read here: no SU(2) integral of X = chi(A pi) chi(pi^-1 B) is computed before the freeze
    say("YM4_04C_DC_CATALAN_MOMENTS|A=(1,2,2,4)/5|B=(2,1,0,2)/3|chi_1/2(V)=tr(AB)=%s|E_pi[(chi_b+chi_t)^(2m)]_m=0..6=%s|"
        "Cat_m(2+chi)^m=%s|odd_moments_m<=11=0|route=exact_monomial_integration_on_S^3|tag=MEASURED|json=0" % (
            qs(chi), ",".join(qs(moments[2 * m]) for m in range(7)), ",".join(qs(cat[m]) for m in range(7))))


# ---- G. small constants

def part_g():
    z = (5, 1)
    p = (1, 0)
    for _ in range(4):
        p = (p[0] * z[0] - p[1] * z[1], p[0] * z[1] + p[1] * z[0])
    p = (p[0] * 239 + p[1] * 1, p[1] * 239 - p[0] * 1)                 # times (239 - i)
    check("machin", p == (114244, 114244))
    at5 = qsub(qadd(qsub(fr(1, 5), fr(1, 375)), fr(1, 15625)), fr(1, 546875))
    pi_lo = qsub(qmul(fr(16), at5), qmul(fr(4), fr(1, 239)))
    check("pi_lower", pi_lo == fr(1231847548, 392109375) and qlt(fr(333, 106), pi_lo) and qlt(fr(80000, 25467), fr(333, 106)))
    e_up = qdiv(fr(8), qmul(fr(3), fr(333, 106)))
    check("e_chi_upper", e_up == fr(848, 999) and qlt(e_up, fr(8489, 10000)))
    np = [(Nn, 6 * Nn ** 4, 8 * 6 * Nn ** 4) for Nn in (8, 12, 16)]
    check("one_over_8Np", [x[2] for x in np] == [196608, 995328, 3145728])
    check("global_route_at_1_100", 8 * 12 < 100 < 8 * 13)
    say("YM4_04C_DC_CONSTANTS|(5+i)^4(239-i)=114244(1+i)|pi>=%s>333/106>80000/25467|8/(3pi)<848/999<8489/10000|"
        "1/(8N_p)=1/196608(8^4),1/995328(12^4),1/3145728(16^4)|8N_p>100_iff_N_p>=13|tag=MEASURED|json=0" % qs(pi_lo))


def main():
    say("YM4_04C_CHECKS_START|file=reviews/ym4-04c-prediction/derive_checks.py|rows=docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp|"
        "integers_and_fractions_only=1|json=0")
    self_check()
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    part_f()
    part_g()
    say("YM4_04C_CHECKS_END|checks=%d|failed=%d|tag=MEASURED|json=0" % (CHECKS[0], FAILED[0]))
    return 0 if FAILED[0] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
