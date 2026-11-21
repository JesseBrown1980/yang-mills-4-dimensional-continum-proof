# YM4-04C final-constants recompute, S lane. Scratch arithmetic, not an engine and not evidence.
# Edited from repair/G0-repair-checks.py (eps_6, the closed form S, the readout) and
# repair/G1-repair-checks.py (exp, ln(1+x), lambda, c_fin, the slice and per-root bounds).
# Final constants: delta_1 = 6 alpha e^{-4(theta-kappa)} and T = (8489/10000) 6 alpha e^{-8 theta} (note section 3);
# C_k MET iff lambda(delta) = delta' + ln(1+delta') <= kappa, factor c_fin(delta) (note section 4).
# Integers and Fractions only. Every enclosure is outward: up() and down() round to B significant bits.
# Floats appear only inside fmt(), for display. Run: python3 -I final_s_lane.py [section ...]
import sys
from fractions import Fraction as Q
from math import comb

B = 256
K = Q(1, 4)                      # kappa
FAC = 6                          # the proved prefactor of delta_1 and T
E_CHI_UP = Q(8489, 10000)        # upper bound on E|chi_1/2| = 8/(3 pi)


def up(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (abs(n).bit_length() - d.bit_length()))
    return Q(-((-n << s) // d), 1 << s)


def down(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (abs(n).bit_length() - d.bit_length()))
    return Q((n << s) // d, 1 << s)


def fmt(x, k=12):
    return format(x.numerator / x.denominator, '.%dg' % k)


_EXP = {}


def ex(y, M=50):
    """[lo, hi] with lo <= e^y <= hi for rational y: Taylor sum, geometric remainder, halving."""
    y = Q(y)
    if y in _EXP:
        return _EXP[y]
    if y < 0:
        lo, hi = ex(-y, M)
        r = (down(1 / hi), up(1 / lo))
    elif y > Q(1, 4):
        lo, hi = ex(y / 2, M)
        r = (down(lo * lo), up(hi * hi))
    else:
        s, t = Q(0), Q(1)
        for m in range(M + 1):
            s += t
            t = t * y / (m + 1)
        r = (down(s), up(s + t / (1 - y / (M + 2))))
    _EXP[y] = r
    return r


EM1 = ex(-1)


def ln1p(x, N=60):
    """[lo, hi] for ln(1+x), 0 < x < 1: two consecutive alternating partial sums."""
    x = Q(x)
    s, t, sums = Q(0), Q(1), []
    for j in range(1, N + 2):
        t = t * x
        s += (t if j % 2 else -t) / j
        sums.append(s)
    a_, b_ = sums[-2], sums[-1]
    return down(min(a_, b_)), up(max(a_, b_))


def dprime(d):
    lo, hi = ex(d)
    return down(d * lo), up(d * hi)


def lam(d):
    p_lo, p_hi = dprime(d)
    return down(p_lo + ln1p(p_lo)[0]), up(p_hi + ln1p(p_hi)[1])


def g_sup(rate_lo, rate_hi, kap, fmin=4):
    """sup over integers f >= fmin of e^{-r f} - e^{-kap f}, r in [rate_lo, rate_hi]; certified tail cut."""
    best_hi, arg, f, vals_lo = Q(0), None, fmin, {}
    while True:
        if ex(-rate_lo * f)[1] <= best_hi:
            break
        ghi = up(ex(-rate_lo * f)[1] - ex(-kap * f)[0])
        glo = down(ex(-rate_hi * f)[0] - ex(-kap * f)[1])
        vals_lo[f] = glo
        if ghi > best_hi:
            best_hi, arg = ghi, f
        f += 1
    return max(vals_lo.values()), best_hi, arg


def cfin(dlo, dhi=None):
    """[lo, hi] for c_fin over [dlo, dhi] (nondecreasing in delta, Lemma 4.19); needs lambda^+ < kappa."""
    if dhi is None:
        dhi = dlo
    l_lo, l_hi = lam(dlo)[0], lam(dhi)[1]
    assert l_hi < K
    e2 = (ex(dlo + l_lo - 5 * K)[0], ex(dhi + l_hi - 5 * K)[1])
    glo, ghi, arg = g_sup(K - l_hi, K - l_lo, K)
    e3 = (down(ex(dlo - K / 2)[0] * glo), up(ex(dhi - K / 2)[1] * ghi))
    return (max(EM1[0], e2[0], e3[0]), max(EM1[1], e2[1], e3[1]),
            {'off_hi': max(e2[1], e3[1]), 'off_lo': max(e2[0], e3[0]), 'argf': arg})


def c1_fallback(dlo, dhi=None):
    """the fallback factor under 2 delta' <= kappa (G1 section 4.14): lambda replaced by 2 delta'."""
    if dhi is None:
        dhi = dlo
    p_lo, p_hi = dprime(dlo)[0], dprime(dhi)[1]
    assert 2 * p_hi < K
    e2 = (ex(dlo + 2 * p_lo - 5 * K)[0], ex(dhi + 2 * p_hi - 5 * K)[1])
    glo, ghi, arg = g_sup(K - 2 * p_hi, K - 2 * p_lo, K)
    e3 = (down(ex(dlo - K / 2)[0] * glo), up(ex(dhi - K / 2)[1] * ghi))
    return max(EM1[0], e2[0], e3[0]), max(EM1[1], e2[1], e3[1]), {'off_hi': max(e2[1], e3[1])}


# ---------------- G0 inputs: eps_6, the closed form S, the alpha-root ----------------
F = lambda n: comb(20 * n, n) // (19 * n + 1)
MU = Q(20 ** 20, 19 ** 19)
HEADS = {
    'crude': {n: 6 * F(n) for n in range(4, 11)},
    'C03': dict(zip(range(4, 11), [1, 0, 12, 0, 32, 32, 304])),
    'headfree': {n: 0 for n in range(4, 11)},
}
COEF = {h: [0] * 4 + [(HEADS[h][n] if n <= 10 else 6 * F(n)) for n in range(4, 49)] for h in HEADS}
F49 = 6 * F(49)


def S_and_dS(x, h):
    """S(x) and S'(x) exactly at rational x; None if mu x >= 1 (Lemma 3.30: the pole test comes first)."""
    if MU * x >= 1:
        return None
    c = COEF[h]
    s, ds, p = Q(0), Q(0), x ** 3
    for n in range(4, 49):
        ds += n * c[n] * p
        p *= x
        s += c[n] * p
    den = 1 - MU * x
    s += F49 * p * x / den
    ds += F49 * (49 * p / den + MU * p * x / den ** 2)
    return s, ds


def c0e(x, M=40):
    q = (x / 2) ** 2
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    return s, s + t / (1 - q / ((M + 2) * (M + 3)))


def iroot(n, k):
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            break
        x = y
    while x ** k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


_EPS = {}


def eps6(beta, bits=200):
    if beta in _EPS:
        return _EPS[beta]
    c1l, c1h = c0e(beta)
    lo = hi = Q(0)
    for k in range(7):
        ckl, ckh = c0e(k * beta)
        rl, rh = ckl / c1h ** k, ckh / c1l ** k
        sg = (-1) ** (6 - k) * comb(6, k)
        if sg > 0:
            lo, hi = lo + sg * rl, hi + sg * rh
        else:
            lo, hi = lo + sg * rh, hi + sg * rl
    lo, hi = down(lo), up(hi)
    assert 0 < lo <= hi
    n_lo = (lo.numerator << (6 * bits)) // lo.denominator
    n_hi = -((-hi.numerator << (6 * bits)) // hi.denominator)
    zl, zh = iroot(n_lo, 6), iroot(n_hi, 6)
    if zh ** 6 < n_hi:
        zh += 1
    r = (Q(zl, 1 << bits), Q(zh, 1 << bits))
    _EPS[beta] = r
    return r


def alpha_root(beta, h, theta=K, iters=200):
    """[a_lo, a_up] around the least root alpha_- of g(alpha) = S(eps e^{2 alpha + theta}) - alpha.
    a_lo: Newton from alpha = 0 with g^- and |g'|^+, which stays below alpha_- (g convex, Lemma 3.31).
    a_up: certified by S^+(x^+(a_up)) <= a_up. Returns None when the iterate meets the pole or passes 1/4
    (no certificate at this theta) and ok=False when the upper read fails."""
    el, eh = eps6(beta)
    a = Q(0)
    for _ in range(iters):
        xl = down(el * ex(2 * a + theta)[0])
        r = S_and_dS(xl, h)
        if r is None:
            return None
        g_lo = r[0] - a
        if g_lo <= 0:
            break
        slope = 1 - 2 * xl * r[1]          # |g'|^+ at the lower x; g' = 2 x S'(x) - 1
        if slope <= 0:
            return None                    # g stops decreasing before a root: no certificate
        a_new = down(a + g_lo / slope)
        if a_new > Q(1, 4):
            return None
        if a_new - a <= a * Q(1, 10 ** 40):
            a = a_new
            break
        a = a_new
    a_up = up(a * (1 + Q(1, 10 ** 30)) + Q(1, 10 ** 60))
    r = S_and_dS(up(eh * ex(2 * a_up + theta)[1]), h)
    ok = r is not None and up(r[0]) <= a_up
    return a, a_up, ok


def read_admissible(beta, h, thr_met, thr_not, factor=FAC):
    """MET: S^+(x^+(alpha_c)) <= alpha_c at alpha_c = thr_met/factor, so delta_1 = factor alpha_- <= thr_met.
    NOT_MET: at alpha_c = thr_not/factor, g^-(alpha_c) > 0 and g'^+(alpha_c) < 0, so by convexity every
    alpha <= alpha_c has g > 0, alpha_- > alpha_c and delta_1 > thr_not (or C_0 is not MET at all).
    A pole at x^-(alpha_c) proves nothing here and is reported as UNDECIDED."""
    el, eh = eps6(beta)
    am = thr_met / factor
    r = S_and_dS(up(eh * ex(2 * am + K)[1]), h)
    met = r is not None and up(r[0]) <= am
    an = thr_not / factor
    xl, xh = down(el * ex(2 * an + K)[0]), up(eh * ex(2 * an + K)[1])
    rl, rh = S_and_dS(xl, h), S_and_dS(xh, h)
    if rl is None or rh is None:
        notmet = 'UNDECIDED_pole'
    else:
        notmet = (rl[0] - an > 0) and (2 * xh * rh[1] - 1 < 0)
    return met, notmet


out = []


def P(*a):
    line = ' '.join(str(t) for t in a)
    out.append(line)
    print(line, flush=True)


def dfmt(lo, hi, k=10):
    return '[%s, %s]' % (fmt(lo, k), fmt(hi, k))


def P10(b):
    return b ** 4 / 128 - b ** 6 / 768 + b ** 8 / 1536 - Q(467, 2211840) * b ** 10


SECTIONS = sys.argv[1:] or ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# ---------------- A. the final C_k domain, delta_crit, and c_fin ----------------
def edge_grid(test, lo, hi, scale=10 ** 9):
    lo, hi = int(lo * scale), int(hi * scale)
    assert test(Q(lo, scale)) and not test(Q(hi, scale))
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if test(Q(mid, scale)):
            lo = mid
        else:
            hi = mid
    return Q(lo, scale), Q(hi, scale)


DC_LO, DC_HI = edge_grid(lambda d: lam(d)[1] <= K, Q(11, 100), Q(12, 100))
DKP_LO, DKP_HI = edge_grid(lambda d: 2 * dprime(d)[1] <= K, Q(10, 100), Q(12, 100))
if 'A' in SECTIONS:
    P('A e^{-1} in', dfmt(EM1[0], EM1[1], 13))
    P('A delta_crit: lambda <= 1/4 certified at', fmt(DC_LO), '; lambda > 1/4 certified at', fmt(DC_HI), ':', lam(DC_HI)[0] > K)
    P('A at delta_crit^-: c_fin in', dfmt(*cfin(DC_LO)[:2]), '; analytic bound e^{d-1/8} <=', fmt(ex(DC_HI - K / 2)[1], 10))
    P('A fallback domain 2delta\' <= 1/4: certified at', fmt(DKP_LO), '; > 1/4 at', fmt(DKP_HI), ':', 2 * dprime(DKP_HI)[0] > K)
    flo, fhi = edge_grid(lambda d: cfin(d)[2]['off_hi'] <= EM1[0], Q(7, 100), Q(8, 100))
    P('A c_fin = e^{-1} through', fmt(flo), '(object channel upper', fmt(cfin(flo)[2]['off_hi'], 10), '); at', fmt(fhi),
      'object channel lower', fmt(cfin(fhi)[2]['off_lo'], 10), '> e^{-1} upper:', cfin(fhi)[2]['off_lo'] > EM1[1])
    glo_, ghi_ = edge_grid(lambda d: c1_fallback(d)[2]['off_hi'] <= EM1[0], Q(7, 100), Q(8, 100))
    P('A fallback factor = e^{-1} through', fmt(glo_), '; leaves it by', fmt(ghi_))
    for d in [Q(49, 1000), Q(1, 20), Q(8, 100), Q(1, 10), Q(11, 100), Q(114, 1000)]:
        lo_, hi_, inf_ = cfin(d)
        P('A c_fin(%s) in %s, argmax f = %s, lambda in %s' % (fmt(d, 6), dfmt(lo_, hi_), inf_['argf'], dfmt(*lam(d))))

# ---------------- B. the rows at beta_0 = 1/100, 1/64, 1/50 ----------------
ROOT = {}


def row_chain(label, beta, h):
    r = alpha_root(beta, h)
    assert r is not None and r[2], (label, r)
    a_lo, a_up, _ = r
    ROOT[(beta, h)] = (a_lo, a_up)
    d_lo, d_hi = FAC * a_lo, FAC * a_up
    p_lo, p_hi = dprime(d_lo)[0], dprime(d_hi)[1]
    l_lo, l_hi = lam(d_lo)[0], lam(d_hi)[1]
    c_lo, c_hi, inf_ = cfin(d_lo, d_hi)
    d2 = up(c_hi * d_hi)
    sm = up(d_hi / (1 - c_hi))
    P('B %s: delta_1 = 6alpha_- in %s; 12alpha_- in %s; 2delta\' in %s; lambda in %s; c_fin in %s%s; delta_2 <= %s; sum_k delta_k <= %s' % (
        label, dfmt(d_lo, d_hi), dfmt(2 * d_lo, 2 * d_hi), dfmt(2 * p_lo, 2 * p_hi), dfmt(l_lo, l_hi), dfmt(c_lo, c_hi),
        ' = e^{-1}' if inf_['off_hi'] <= EM1[0] else ' (argmax f=%s)' % inf_['argf'], fmt(d2, 10), fmt(sm, 10)))
    return d_lo, d_hi, c_hi


if 'B' in SECTIONS:
    for beta in [Q(1, 100), Q(1, 64), Q(1, 50)]:
        e = eps6(beta)
        P('B eps_6(%s) in %s' % (beta, dfmt(e[0], e[1], 13)))
    c07 = row_chain('C07 crude 1/100', Q(1, 100), 'crude')
    c08 = row_chain('C08 C03 1/100', Q(1, 100), 'C03')
    c08h = row_chain('C08 head-free 1/100', Q(1, 100), 'headfree')
    c11 = row_chain('C11 crude 1/64', Q(1, 64), 'crude')
    c14 = row_chain('C14 C03 1/64', Q(1, 64), 'C03')
    c12h = row_chain('C12 head-free 1/50', Q(1, 50), 'headfree')
    c12 = row_chain('C12 C03 1/50', Q(1, 50), 'C03')
    r = alpha_root(Q(1, 50), 'crude')
    P('B C12 crude 1/50: Newton from 0 finds no root (pole or g\' >= 0):', r is None)
    # C08: the coarse Wilson term's norm 12 e c_1/2 with c_1/2 from the MEASURED P_10, and the crude/refined ratio
    elo, ehi = ex(1)
    w_lo, w_hi = 12 * elo * P10(Q(1, 100)), 12 * ehi * P10(Q(1, 100))
    P('B C08: 12e P_10(1/100) in %s; delta_1(C03)/(12e P_10) in %s; crude/C03 delta_1 ratio in %s' % (
        dfmt(w_lo, w_hi, 8), dfmt(c08[0] / w_hi, c08[1] / w_lo, 9), dfmt(c07[0] / c08[1], c07[1] / c08[0], 9)))
    # C16: delta_20 <= c_fin(delta_1)^19 delta_1 and osc <= (512/e) delta_20 on the coarse 4^4 torus (Lemma 4.21)
    d20 = up(c07[2] ** 19 * c07[1])
    osc = up(512 * EM1[1] * d20)
    P('B C16: delta_20 <= c_fin^19 delta_1^+ <=', fmt(d20, 10), '; osc_V log rho_20 <= (512/e) delta_20 <=', fmt(osc, 10))

# ---------------- C. C09: T/P_10 over the theta grid, and the readout_grid_128 fault ----------------
def T_bracket(beta, i):
    th = K + Q(i, 64)
    r = alpha_root(beta, 'C03', theta=th)
    if r is None or not r[2]:
        return None
    a_lo, a_up, _ = r
    e8 = ex(-8 * th)
    return down(E_CHI_UP * FAC * a_lo * e8[0]), up(E_CHI_UP * FAC * a_up * e8[1])


if 'C' in SECTIONS:
    for beta, i_exp in [(Q(1, 4000), 194), (Q(1, 2000), 150), (Q(1, 1000), 105), (Q(1, 700), 83), (Q(1, 600), 73), (Q(1, 100), 0)]:
        vals = {}
        for i in range(0, 321):
            t = T_bracket(beta, i)
            if t is not None:
                vals[i] = t
        istar = min(vals, key=lambda i: vals[i][1])
        unique = all(vals[istar][1] < vals[i][0] for i in vals if i != istar)
        p = P10(beta)
        lo, hi = vals[istar][0] / p, vals[istar][1] / p
        P('C C09 beta=%s: certified theta indices %d..%d (%d values); argmin i=%d (expected %d), strict: %s; T/P_10 in %s' % (
            beta, min(vals), max(vals), len(vals), istar, i_exp, unique, dfmt(lo, hi, 8)))
        if beta in (Q(1, 4000), Q(1, 2000), Q(1, 1000)):
            lead = beta ** 8 / 2048
            P('C   low power: T/(beta^8/2048) >= %s; P_10 - 2t_2^4 = (beta^8/2048)(1 - eta), eta in [0, 4e-7] (v2-checks/c09_readout_tail.out)' % (
                fmt(vals[istar][0] / lead, 6)))
        if beta == Q(1, 4000):
            cut = {i: v for i, v in vals.items() if i <= 128}
            ic = min(cut, key=lambda i: cut[i][1])
            P('C readout_grid_128 at 1/4000: argmin over i <= 128 is i=%d; T/P_10 in %s' % (ic, dfmt(cut[ic][0] / p, cut[ic][1] / p, 8)))

# ---------------- D. the self-map edges on the 1e-5 grid ----------------
def edge_pair(label, h, i, thr_met, thr_not):
    b0, b1 = Q(i, 10 ** 5), Q(i + 1, 10 ** 5)
    m0, n0 = read_admissible(b0, h, thr_met, thr_not)
    m1, n1 = read_admissible(b1, h, thr_met, thr_not)
    r0, r1 = alpha_root(b0, h), alpha_root(b1, h)
    s0 = dfmt(FAC * r0[0], FAC * r0[1], 9) + (' (certified)' if r0 and r0[2] else ' (upper not certified)') if r0 else 'no root'
    s1 = dfmt(FAC * r1[0], FAC * r1[1], 9) + (' (certified)' if r1 and r1[2] else ' (upper not certified)') if r1 else 'no root'
    P('D %s, %s: MET at %s certified %s (delta_1 in %s); NOT_MET at %s certified %s (delta_1 in %s)' % (
        label, h, fmt(b0, 6), m0, s0, fmt(b1, 6), n1, s1))
    return m0 is True and n1 is True


if 'D' in SECTIONS:
    for h, i in [('crude', 1767), ('C03', 2074), ('headfree', 2074)]:
        edge_pair('final lambda <= 1/4, factor 6', h, i, DC_LO, DC_HI)
    for h, i in [('crude', 1761), ('C03', 2074), ('headfree', 2074)]:
        edge_pair('fallback 2delta\' <= 1/4, factor 6', h, i, DKP_LO, DKP_HI)
    T49 = Q(49, 1000)
    edge_pair('surrogate delta_1 <= 49/1000, factor 6', 'crude', 1552, T49, T49)

# ---------------- E. C10b and C10c against c_fin, the slice bound and the per-root bound ----------------
def c0(x, M=30):
    q = (x / 2) ** 2
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    return s, s + t / (1 - q / ((M + 2) * (M + 3)))


if 'E' in SECTIONS:
    for s in [Q(1, 2000), Q(1, 4096)]:
        e6 = ex(6 * K)
        din = (down(12 * s * e6[0]), up(12 * s * e6[1]))
        c0lo, c0hi = c0(4 * s)
        lg = (c0lo - 1 - (c0lo - 1) ** 2 / 2, c0hi - 1)      # ln(1+y) in [y - y^2/2, y]
        e4 = ex(4 * K)
        dout = (down(3 * e4[0] * lg[0]), up(3 * e4[1] * lg[1]))
        c_lo, c_hi, inf_ = cfin(din[0], din[1])
        assert inf_['off_hi'] <= EM1[0]
        l_lo, l_hi = lam(din[0])[0], lam(din[1])[1]
        r_lo, r_hi = down(dout[0] / (EM1[1] * din[1])), up(dout[1] / (EM1[0] * din[0]))
        pr_lo = down(ex(din[0] - 4 * K)[0] * (ex(2 * l_lo)[0] - 1))   # e^{delta} q(2,4) = e^{delta-4k}(e^{2 lambda}-1)
        pr_hi = up(ex(din[1] - 4 * K)[1] * (ex(2 * l_hi)[1] - 1))
        pb = (Q(400, 10 ** 9), Q(401, 10 ** 9))
        P('E C10b s=%s: delta_in in %s; lambda in %s; c_fin = e^{-1}; natural delta_out = slice bound in %s; delta_out/delta_in in %s' % (
            s, dfmt(din[0], din[1], 9), dfmt(l_lo, l_hi), dfmt(dout[0], dout[1], 9), dfmt(dout[0] / din[1], dout[1] / din[0], 7)))
        P('E   delta_out/(c_fin delta_in) in %s; slack in %s; per-root factor in %s; per-root bound / natural delta_out in %s' % (
            dfmt(r_lo, r_hi, 7), dfmt(1 / r_hi, 1 / r_lo, 8), dfmt(pr_lo, pr_hi, 8),
            dfmt(down(pr_lo * din[0] / dout[1]), up(pr_hi * din[1] / dout[0]), 8)))
        if s == Q(1, 2000):
            P('E   projection bound [4.00e-7, 4.01e-7] / (c_fin delta_in) in %s' % dfmt(pb[0] / (EM1[1] * din[1]), pb[1] / (EM1[0] * din[0]), 6))
    for s in [Q(1, 8192), Q(1, 65536)]:
        e10 = ex(10 * K)
        din = (down(24 * s * e10[0]), up(24 * s * e10[1]))
        e4 = ex(4 * K)
        dout = (down(6 * e4[0] * (s - 4 * s * s)), up(6 * e4[1] * (s + 4 * s * s)))
        c_lo, c_hi, inf_ = cfin(din[0], din[1])
        assert inf_['off_hi'] <= EM1[0]
        l_lo, l_hi = lam(din[0])[0], lam(din[1])[1]
        r_lo, r_hi = down(dout[0] / (EM1[1] * din[1])), up(dout[1] / (EM1[0] * din[0]))
        pr_lo = ex(din[0] - 6 * K + 2 * l_lo)[0]      # e^{delta} q(2,8) = e^{delta-6k+2 lambda}
        pr_hi = ex(din[1] - 6 * K + 2 * l_hi)[1]
        # the frozen every-decomposition (projection) bound 6 e^{4k} |c_P| / E|chi|, c_P in [s/2 - 4s^2 E|chi|, s/2 + 4s^2 E|chi|]
        echi = (Q(8488263, 10 ** 7), Q(8488264, 10 ** 7))
        proj = (down(6 * e4[0] * (s / 2 - 4 * s * s * echi[1]) / echi[1]), up(6 * e4[1] * (s / 2 + 4 * s * s * echi[1]) / echi[0]))
        P('E C10c s=%s: delta_in in %s; lambda in %s; 2delta\' in %s; c_fin = e^{-1}; natural delta_out = slice bound in %s; delta_out/delta_in in %s' % (
            s, dfmt(din[0], din[1], 9), dfmt(l_lo, l_hi), dfmt(2 * dprime(din[0])[0], 2 * dprime(din[1])[1]),
            dfmt(dout[0], dout[1], 9), dfmt(dout[0] / din[1], dout[1] / din[0], 7)))
        P('E   delta_out/(c_fin delta_in) in %s; slack in %s; per-root factor in %s; per-root bound / natural delta_out in %s' % (
            dfmt(r_lo, r_hi, 7), dfmt(1 / r_hi, 1 / r_lo, 8), dfmt(pr_lo, pr_hi, 8),
            dfmt(down(pr_lo * din[0] / dout[1]), up(pr_hi * din[1] / dout[0]), 8)))
        P('E   projection bound / delta_in in %s; projection bound / (c_fin delta_in) in %s' % (
            dfmt(proj[0] / din[1], proj[1] / din[0], 7), dfmt(proj[0] / (EM1[1] * din[1]), proj[1] / (EM1[0] * din[0]), 7)))
    e32 = ex(Q(-3, 2))
    P('E e^{-3/2}/4 in', dfmt(e32[0] / 4, e32[1] / 4, 10))

# ---------------- F. the C_0 reads that do not involve the prefactor: wall quantity at the guard points ----------------
if 'F' in SECTIONS:
    for beta in [Q(1, 40), Q(2248, 10 ** 5)]:
        el, eh = eps6(beta)
        w = MU * el * ex(K)[0]
        P('F guard beta=%s: mu e^{1/4} eps_6^- >= %s (>= 1: %s)' % (fmt(beta, 6), fmt(w, 8), w >= 1))

# ---------------- G. orderings and the regime ----------------
if 'G' in SECTIONS:
    P('G ordering beta_ind^crude < beta_crude: 0.01767 < 0.01904:', Q(1767, 10 ** 5) < Q(1904, 10 ** 5))
    P('G ordering beta_ind < beta_stop < beta_wall: 0.02074 < 0.02075 < 0.02247:', Q(2074, 10 ** 5) < Q(2075, 10 ** 5) < Q(2247, 10 ** 5))
    db = (Q(2575118, 10 ** 7), Q(2575119, 10 ** 7))
    P('G beta_wall upper / Delta_beta lower = %s < 9/100: %s' % (fmt(Q(2248, 10 ** 5) / db[0], 6), Q(2248, 10 ** 5) / db[0] < Q(9, 100)))
    P('G |beta_m| <= (16/(3 pi)) e^{-1} delta_m < 0.62454 delta_m; at delta_crit^+:', fmt(Q(62454, 10 ** 5) * DC_HI, 8))

# ---------------- H. self-check: the source holds no float literal ----------------
if 'H' in SECTIONS:
    import io
    import tokenize
    src = open(__file__).read()
    bad = [t.string for t in tokenize.generate_tokens(io.StringIO(src).readline)
           if t.type == tokenize.NUMBER and any(ch in t.string.lower() for ch in '.ej') and not t.string.lower().startswith('0x')]
    P('H float literals in this file:', len(bad))

name = __file__.replace('.py', '.out') if len(sys.argv) == 1 else __file__.replace('.py', '-' + ''.join(SECTIONS) + '.out')
with open(name, 'w') as f:
    f.write('\n'.join(out) + '\n')
