#!/usr/bin/env python3
"""
L4-sec4-part2 lane checks (note section 4.9 to the end of section 4, plus checks T1, T2, T3_stepk, T4).
Integer-only outward enclosures (ival.py). Every printed row is a re-derivation on this seat, not a copy of a frozen value.
Run: python3 -I -B l4p2_checks.py  (from this directory; ival.py is imported from the script's own directory).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ival import (ONE, P, rat, pt, add, sub, neg, mul, imul, div, powi, hull, imax, le, lt, iexp, iln1p,
                  iroot6, dec, ds, self_check, exp_point, fdiv, cdiv)

ROWS = []
NCHK = [0]
NFAIL = [0]


def say(s):
    ROWS.append(s)
    sys.stdout.write(s + "\n")
    sys.stdout.flush()


def check(name, ok, detail=""):
    NCHK[0] += 1
    if not ok:
        NFAIL[0] += 1
        say("FAILED|check=" + name + "|" + detail + "|json=0")
    return ok


KAPPA = rat(1, 4)
QUARTER = ONE >> 2
EM1 = iexp(rat(-1))          # e^{-1}


def inside(a, lo, hi):
    """certified lo <= a <= hi for an interval a and exact rationals lo=(n,d), hi=(n,d)."""
    L = rat(*lo)
    H = rat(*hi)
    return a[0] >= L[1] and a[1] <= H[0]


# ---------------------------------------------------------------- step-k quantities

def dprime(d):
    return mul(d, iexp(d))


def lam(d):
    dp = dprime(d)
    return add(dp, iln1p(dp))


def g_hi(lmb_hi, f):
    # upper enclosure of e^{-(1/4 - lambda) f} - e^{-f/4}
    a = iexp(imul(sub(rat(1, 4), pt(lmb_hi)), -f))[1]
    b = iexp(rat(-f, 4))[0]
    return a - b


def g_lo(lmb_lo, f):
    a = iexp(imul(sub(rat(1, 4), pt(lmb_lo)), -f))[0]
    b = iexp(rat(-f, 4))[1]
    return a - b


def sup_g(lmb):
    """certified enclosure of sup_{f>=4} g(f) for lambda in lmb with lmb_hi < 1/4, with the tail cut of the note:
    stop at the first f with e^{-(1/4-lambda^+) f} <= best upper value so far."""
    assert lmb[1] < QUARTER
    best_hi, best_lo, arg = None, None, None
    f = 4
    while True:
        tail = iexp(imul(sub(rat(1, 4), pt(lmb[1])), -f))[1]
        if best_hi is not None and tail <= best_hi:
            return (best_lo, best_hi), arg, f
        gh, gl = g_hi(lmb[1], f), g_lo(lmb[0], f)
        if best_hi is None or gh > best_hi:
            best_hi = gh
        if best_lo is None or gl > best_lo:
            best_lo = gl
            arg = f
        f += 1
        if f > 100000:
            raise RuntimeError("scan did not stop")


def cfin(d, lmb=None):
    """enclosure of c_fin(delta) for delta in the interval d; also each entry."""
    if lmb is None:
        lmb = lam(d)
    e2 = iexp(add(add(d, lmb), rat(-5, 4)))
    sg, arg, fstop = sup_g(lmb)
    e3 = mul(iexp(add(d, rat(-1, 8))), sg)
    c = imax(imax(EM1, e2), e3)
    return c, EM1, e2, e3, arg, fstop


def cfin_fallback(d):
    """route A's c* with roots m >= 1: c_fin with lambda replaced by 2 delta' (the fallback of the rows)."""
    lmb = imul(dprime(d), 2)
    return cfin(d, lmb)


# ---------------------------------------------------------------- G0 quantities (for the edges)

def comb(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def F20(n):
    c = comb(20 * n, n)
    q, r = divmod(c, 19 * n + 1)
    assert r == 0
    return q


MU = rat(20 ** 20, 19 ** 19)


def c0(tn, td):
    """enclosure of c_0(t) = sum_m (t/2)^{2m}/(m!(m+1)!) for t = tn/td >= 0, partial sums plus a tail bound."""
    # term_m = tn^{2m} / (4^m td^{2m} m! (m+1)!)
    lo, hi = 0, 0
    m = 0
    num, den = 1, 1   # exact term as num/den
    while True:
        tlo, thi = fdiv(num * ONE, den), cdiv(num * ONE, den)
        lo += tlo
        hi += thi
        # ratio of the next term: (t/2)^2 / ((m+1)(m+2))
        rn, rd = tn * tn, 4 * td * td * (m + 1) * (m + 2)
        if thi <= 1 and 2 * rn <= rd:
            # tail <= term_m * (r + r^2 + ...) <= term_m when r <= 1/2
            return (lo, hi + thi + 1)
        num, den = num * rn, den * rd
        m += 1
        if m > 5000:
            raise RuntimeError("c0")


def eps6(bn, bd):
    """enclosure of eps_6(beta), eps_6^6 = sum_k C(6,k)(-1)^{6-k} c_0(k beta)/c_0(beta)^k (note Lemma 3.2 item 4)."""
    cb = c0(bn, bd)
    tot = (0, 0)
    for k in range(0, 7):
        ck = c0(k * bn, bd) if k > 0 else (ONE, ONE)
        term = div(ck, powi(cb, k))
        term = imul(term, comb(6, k) * (1 if (6 - k) % 2 == 0 else -1))
        tot = add(tot, term)
    assert tot[0] >= 0, "eps6^6 lower end negative: precision"
    return iroot6(tot), tot


def head(kind):
    if kind == "crude":
        return [6 * F20(n) for n in range(4, 11)]
    if kind == "c03":
        return [1, 0, 12, 0, 32, 32, 304]
    if kind == "headfree":
        return [0] * 7
    raise ValueError(kind)


def coeffs(kind):
    """coefficients c_n for n = 0..48 of the polynomial part of S."""
    c = [0] * 49
    h = head(kind)
    for i, n in enumerate(range(4, 11)):
        c[n] = h[i]
    for n in range(11, 49):
        c[n] = 6 * F20(n)
    return c


TAIL49 = 6 * F20(49)


def S_hi(kind, x):
    """upper enclosure of S at x in the interval x (x >= 0), or None when the pole test mu^+ x^+ < 1 fails."""
    mx = mul(MU, (x[1], x[1]))[1]
    if mx >= ONE:
        return None
    c = coeffs(kind)
    xs = (x[1], x[1])
    s = (0, 0)
    pw = (ONE, ONE)
    for n in range(0, 49):
        if c[n]:
            s = add(s, imul(pw, c[n]))
        pw = mul(pw, xs)
    # pw = x^49 now
    den = (ONE - mx, ONE - mx)
    s = add(s, div(imul(pw, TAIL49), den))
    return s[1]


def S_lo(kind, x):
    """lower enclosure of S at the lower end of x (exact mu, rounded down), assuming mu x < 1 there."""
    mxl = mul(MU, (x[0], x[0]))
    if mxl[1] >= ONE:
        return None
    c = coeffs(kind)
    xs = (x[0], x[0])
    s = (0, 0)
    pw = (ONE, ONE)
    for n in range(0, 49):
        if c[n]:
            s = add(s, imul(pw, c[n]))
        pw = mul(pw, xs)
    den = (ONE - mxl[0], ONE - mxl[0])   # an upper bound of 1 - mu x
    s = add(s, div(imul(pw, TAIL49), den))
    return s[0]


def Sp_hi(kind, x):
    """upper enclosure of S'(x) at x^+ (None if the pole test fails)."""
    mx = mul(MU, (x[1], x[1]))[1]
    if mx >= ONE:
        return None
    c = coeffs(kind)
    xs = (x[1], x[1])
    s = (0, 0)
    pw = (ONE, ONE)   # x^{n-1}
    for n in range(1, 49):
        if c[n]:
            s = add(s, imul(pw, c[n] * n))
        pw = mul(pw, xs)
    # pw = x^48
    den = (ONE - mx, ONE - mx)
    t1 = div(imul(pw, 49 * TAIL49), den)
    x49 = mul(pw, xs)
    t2 = div(mul(imul(x49, TAIL49), MU), mul(den, den))
    s = add(add(s, t1), t2)
    return s[1]


def xof(eps, alpha):
    """enclosure of x = eps * e^{2 alpha + 1/4} for an exact rational alpha=(n,d)."""
    a = rat(*alpha)
    e = iexp(add(imul(a, 2), rat(1, 4)))
    return mul(eps, e)


def met_read(kind, eps, alpha):
    """MET: mu^+ x^+ < 1 and S^+(x^+) <= alpha."""
    x = xof(eps, alpha)
    s = S_hi(kind, x)
    if s is None:
        return False, "pole"
    return s <= rat(*alpha)[0], s


def notmet_read(kind, eps, alpha):
    """NOT_MET at alpha: g^-(alpha) > 0 and g'^+(alpha) < 0 (so the least root exceeds alpha, by convexity)."""
    x = xof(eps, alpha)
    sl = S_lo(kind, x)
    sp = Sp_hi(kind, x)
    if sl is None or sp is None:
        return False, "pole"
    a = rat(*alpha)
    gminus = sl - a[1]
    gpplus = cdiv(2 * x[1] * sp, ONE) + 2 - ONE
    return (gminus > 0 and gpplus < 0), (gminus, gpplus)


def least_root(kind, eps, lo_n=0, hi_n=None, den=10 ** 13):
    """bracket the least root alpha_- of S(eps e^{2 alpha + 1/4}) = alpha on the grid alpha = n/den:
    returns (a_lo, a_hi) with NOT_MET certified at a_lo and MET certified at a_hi."""
    if hi_n is None:
        hi_n = None
        for j in range(1, 251):
            okj, _ = met_read(kind, eps, (j, 2000))
            if okj:
                hi_n = j * (den // 2000)
                break
        if hi_n is None:
            return None
    ok, _ = met_read(kind, eps, (hi_n, den))
    if not ok:
        return None
    lo = lo_n
    hi = hi_n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        okm, _ = met_read(kind, eps, (mid, den))
        if okm:
            hi = mid
            continue
        okn, _ = notmet_read(kind, eps, (mid, den))
        if okn:
            lo = mid
            continue
        return ("undecided", lo, hi, mid)
    okl, _ = notmet_read(kind, eps, (lo, den))
    okh, _ = met_read(kind, eps, (hi, den))
    if not (okl and okh):
        return ("unverified_ends", lo, hi, int(okl), int(okh))
    return (lo, hi, den)


def run():
    nb = self_check(os.path.abspath(__file__)) + self_check(os.path.join(HERE, "ival.py"))
    say("L4P2_NO_FLOAT|float_literals=%d|true_division_ops=%d|negative_powers=%d|float_names=%d|P_bits=%d|tag=MEASURED|json=0" % (
        nb[0] + nb[4], nb[1] + nb[5], nb[2] + nb[6], nb[3] + nb[7], P))
    check("no_float", sum(nb) == 0)

    say("L4P2_E|e^-1=%s|tag=MEASURED|json=0" % ds(EM1, 13))

    # ---- delta_crit and the fallback edge
    dlo, dhi = rat(114846768, 10 ** 9), rat(114846769, 10 ** 9)
    l1 = lam(dlo)
    l2 = lam(dhi)
    ok_crit = l1[1] <= QUARTER and l2[0] > QUARTER
    check("delta_crit_bracket", ok_crit)
    say("L4P2_DELTA_CRIT|lambda(0.114846768)=%s|lambda(0.114846769)=%s|bracket_[0.114846768,0.114846769]=%d|tag=MEASURED|json=0" % (
        ds(l1, 13), ds(l2, 13), int(ok_crit)))
    # refine delta_crit to 10^-18 for the c_fin(delta_crit^-) read
    lo, hi = 114846768 * 10 ** 9, 114846769 * 10 ** 9
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lm = lam(rat(mid, 10 ** 18))
        if lm[1] <= QUARTER:
            lo = mid
        elif lm[0] > QUARTER:
            hi = mid
        else:
            break
    say("L4P2_DELTA_CRIT_FINE|delta_crit_in_[%d,%d]e-18|tag=MEASURED|json=0" % (lo, hi))
    # fallback 2 delta' <= 1/4
    f1 = imul(dprime(rat(111780108, 10 ** 9)), 2)
    f2 = imul(dprime(rat(111780109, 10 ** 9)), 2)
    ok_fb = f1[1] <= QUARTER and f2[0] > QUARTER
    check("fallback_bracket", ok_fb)
    say("L4P2_FALLBACK_EDGE|2delta'(0.111780108)=%s|2delta'(0.111780109)=%s|bracket=%d|tag=MEASURED|json=0" % (ds(f1, 12), ds(f2, 12), int(ok_fb)))
    # frozen C_k edge 2 delta' <= 1/8
    z1 = imul(dprime(rat(58923670, 10 ** 9)), 2)
    z2 = imul(dprime(rat(58923671, 10 ** 9)), 2)
    ok_fr = z1[1] <= (ONE >> 3) and z2[0] > (ONE >> 3)
    check("frozen_Ck_edge", ok_fr)
    say("L4P2_FROZEN_CK_EDGE|0.058923670/0.058923671=%d|tag=MEASURED|json=0" % int(ok_fr))
    # lambda(kappa/2) > kappa (Lemma 4.17)
    lk = lam(rat(1, 8))
    check("lambda_kappa_half", lk[0] > QUARTER)
    say("L4P2_L417|lambda(1/8)=%s>1/4=%d|e^{1/8}<8/7=%d|tag=MEASURED|json=0" % (
        ds(lk, 10), int(lk[0] > QUARTER), int(iexp(rat(1, 8))[1] < rat(8, 7)[0])))

    # ---- c_fin flat range and the C13 reads
    for (n, d, expect_flat) in [(78733761, 10 ** 9, True), (78733762, 10 ** 9, False)]:
        dd = rat(n, d)
        c, e1, e2, e3, arg, fstop = cfin(dd)
        flat = e2[1] <= EM1[0] and e3[1] <= EM1[0]
        above = e3[0] > EM1[1]
        if expect_flat:
            check("cfin_flat_%d" % n, flat)
        else:
            check("cfin_above_%d" % n, above and arg == 7)
        say("L4P2_CFIN_EDGE|delta=%d/%d|entry2=%s|entry3=%s|argmax_f=%d|scan_stop_f=%d|cfin=e^-1:%d|cfin>e^-1:%d|tag=MEASURED|json=0" % (
            n, d, ds(e2, 10), ds(e3, 10), arg, fstop, int(flat), int(above)))
    for (n, d, lo_s, hi_s, fexp) in [(1, 10, (611173, 10 ** 6), (611174, 10 ** 6), 9),
                                     (11, 100, (811310, 10 ** 6), (811311, 10 ** 6), 13),
                                     (114846768, 10 ** 9, (989898, 10 ** 6), (989899, 10 ** 6), None)]:
        dd = rat(n, d)
        c, e1, e2, e3, arg, fstop = cfin(dd)
        okv = inside(c, lo_s, hi_s) and (fexp is None or arg == fexp)
        check("cfin_%d_%d" % (n, d), okv)
        say("L4P2_CFIN|delta=%d/%d|cfin=%s|argmax_f=%d|scan_stop_f=%d|in_frozen_bracket=%d|tag=MEASURED|json=0" % (
            n, d, ds(c, 10), arg, fstop, int(okv)))
    for (n, d) in [(49, 1000), (1, 20)]:
        c, e1, e2, e3, arg, fstop = cfin(rat(n, d))
        flat = e2[1] <= EM1[0] and e3[1] <= EM1[0]
        check("cfin_flat_%d_%d" % (n, d), flat)
        say("L4P2_CFIN|delta=%d/%d|cfin=e^-1:%d|tag=MEASURED|json=0" % (n, d, int(flat)))
    # assembly note after Lemma 4.17
    m1 = iexp(rat(114846769 * 8 - 10 ** 9, 8 * 10 ** 9))
    m2 = iexp(rat(1148467681 * 8 - 10 ** 10, 8 * 10 ** 10))
    l3 = lam(rat(1148467681, 10 ** 10))
    say("L4P2_L417_NOTE|e^{0.114846769-1/8}=%s|le_0.989898139=%d|le_0.98989814=%d|lambda(0.1148467681)>1/4=%d|e^{0.1148467681-1/8}=%s|le_0.989898139=%d|tag=MEASURED|json=0" % (
        ds(m1, 12), int(m1[1] <= rat(989898139, 10 ** 9)[0]), int(m1[1] <= rat(98989814, 10 ** 8)[0]),
        int(l3[0] > QUARTER), ds(m2, 12), int(m2[1] <= rat(989898139, 10 ** 9)[0])))
    check("L417_note_middle_false", m1[0] > rat(989898139, 10 ** 9)[1])
    check("L417_note_end_true", l3[0] > QUARTER and m2[1] <= rat(989898139, 10 ** 9)[0])
    # c_fin at the true delta_crit^- from the fine bracket, and at the end of the whole domain (lambda -> kappa)
    c, e1, e2, e3, arg, fstop = cfin(rat(lo, 10 ** 18))
    say("L4P2_CFIN_FINE|delta=%de-18|cfin=%s|argmax_f=%d|tag=MEASURED|json=0" % (lo, ds(c, 10), arg))

    # ---- fallback factor e^{-1} range (route A c* with m >= 1, 2 delta' <= kappa)
    for (n, d, expect_flat) in [(77320139, 10 ** 9, True), (77320140, 10 ** 9, False)]:
        c, e1, e2, e3, arg, fstop = cfin_fallback(rat(n, d))
        flat = e2[1] <= EM1[0] and e3[1] <= EM1[0]
        above = e3[0] > EM1[1] or e2[0] > EM1[1]
        check("fb_flat_%d" % n, flat if expect_flat else above)
        say("L4P2_FALLBACK_FLAT|delta=%d/%d|cfin_fb=e^-1:%d|above:%d|tag=MEASURED|json=0" % (n, d, int(flat), int(above)))

    # ---- Lemma 4.16: closed form against a brute-force sup over 1<=f<=60, 1<=m<=40 (computational evidence only)
    for (n, d) in [(1, 100), (3, 100), (5, 100), (7, 100), (8, 100), (11, 100)]:
        dd = rat(n, d)
        lmb = lam(dd)
        best = None
        barg = None
        for m in range(1, 41):
            for f in range(1, 61):
                if f + m < 4:
                    continue
                # q(f,m) = e^{-kappa f - kappa m/2} [ e^{-kappa (m mod 2)/2} 1[m>=8] + e^{lambda f} - 1 ], upper end
                pre = iexp(rat(-(2 * f + m), 8))
                br = sub(iexp(imul(lmb, f)), (ONE, ONE))
                if m >= 8:
                    br = add(br, iexp(rat(-(m % 2), 8)))
                q = mul(pre, br)
                if best is None or q[0] > best[0]:
                    best = q
                    barg = (f, m)
        e2 = iexp(sub(lmb, rat(5, 4)))
        sg, arg, fstop = sup_g(lmb)
        e3 = mul(iexp(rat(-1, 8)), sg)
        closed = imax(e2, e3)
        agree = best[0] <= closed[1] and closed[0] <= best[1] + (closed[1] - closed[0]) + 4
        check("Q_closed_%d_%d" % (n, d), agree)
        say("L4P2_Q_BRUTE|delta=%d/%d|brute_sup=%s|at_(f,m)=(%d,%d)|closed=%s|agree=%d|tag=MEASURED_evidence_only|json=0" % (
            n, d, ds(best, 10), barg[0], barg[1], ds(closed, 10), int(agree)))

    # ---- Lemma 4.22 constants: Machin, pi bounds, 16/(3 pi) e^{-1}
    re, im = 1, 0
    for _ in range(4):
        re, im = re * 5 - im * 1, re * 1 + im * 5
    re, im = re * 239 + im * 1, -re * 1 + im * 239
    machin = (re == 114244 and im == 114244)
    check("machin", machin)
    # pi >= 16*(1/5 - 1/375 + 1/15625 - 1/546875) - 4/239 as an exact rational: numerators over the lcm
    den = 5 * 375 * 15625 * 546875 * 239
    num = 16 * (den // 5 - den // 375 + den // 15625 - den // 546875) - 4 * (den // 239)
    pin, pid = 1231847548, 392109375
    pi_ok = num * pid >= pin * den
    check("pi_machin_lower", pi_ok)
    check("pi_gt_333_106", pin * 106 > 333 * pid)
    check("333_106_gt_80000_25467", 333 * 25467 > 80000 * 106)
    # (16/(3 pi)) e^{-1} upper bounds under the three pi bounds
    b_mach = mul(rat(16 * pid, 3 * pin), EM1)
    b_333 = mul(rat(16 * 106, 3 * 333), EM1)
    b_8489 = mul(rat(2 * 8489, 10000), EM1)
    say("L4P2_L422|machin_identity=%d|pi>=%d/%d:%d|bound_machin=%s|bound_333/106=%s|bound_8489=%s|tag=MEASURED|json=0" % (
        int(machin), pin, pid, int(pi_ok), ds(b_mach, 8), ds(b_333, 8), ds(b_8489, 8)))
    check("L422_machin_le_0.6245318", b_mach[1] <= rat(6245318, 10 ** 7)[0])
    check("L422_machin_lt_0.62454", b_mach[1] < rat(62454, 10 ** 5)[0])
    check("L422_333_above_0.62454", b_333[0] > rat(62454, 10 ** 5)[1] and b_333[1] < rat(6245481, 10 ** 7)[0])
    check("L422_8489_lt_0.62459", b_8489[1] < rat(62459, 10 ** 5)[0] and b_8489[0] > rat(62454, 10 ** 5)[1])
    cap = mul(rat(62454, 10 ** 5), rat(114846769, 10 ** 9))
    check("beta_cap_0.07173", cap[1] < rat(7173, 10 ** 5)[0])
    say("L4P2_BETA_CAP|0.62454*delta_crit^+=%s<0.07173=%d|tag=MEASURED|json=0" % (ds(cap, 9), int(cap[1] < rat(7173, 10 ** 5)[0])))

    # ---- C10c Taylor tail: |e^{1/4}-1| and -ln(1-(e^{1/4}-1)) < 1/2, i.e. 2 - e^{1/4} > e^{-1/2}
    e14 = iexp(rat(1, 4))
    em12 = iexp(rat(-1, 2))
    cauchy = (2 * ONE - e14[1]) > em12[1]
    check("C10c_cauchy_half", cauchy)
    say("L4P2_C10C_TAIL|e^{1/4}-1=%s|2-e^{1/4}>e^{-1/2}:%d|so_abs(f)<1/2_on_abs(s)<=1/16|tag=MEASURED|json=0" % (
        ds(sub(e14, (ONE, ONE)), 8), int(cauchy)))

    # ---- G0 edges (T1, T4): eps_6 sanity against C02, then the admissibility reads
    for (bn, bd, lo_s, hi_s) in [(1, 100, (6538419, 10 ** 9), (6538420, 10 ** 9)),
                                 (1, 64, (10216544, 10 ** 9), (10216545, 10 ** 9)),
                                 (1, 40, (16347585, 10 ** 9), (16347586, 10 ** 9))]:
        e6, e6p = eps6(bn, bd)
        okv = inside(e6, lo_s, hi_s)
        check("eps6_%d_%d" % (bn, bd), okv)
        say("L4P2_EPS6|beta=%d/%d|eps6=%s|C02_bracket=%d|tag=MEASURED|json=0" % (bn, bd, ds(e6, 13), int(okv)))

    a_minus = (114846768, 6 * 10 ** 9)
    a_plus = (114846769, 6 * 10 ** 9)
    fb_minus = (111780108, 6 * 10 ** 9)
    fb_plus = (111780109, 6 * 10 ** 9)
    edges = [("c03", 2074, 2075, a_minus, a_plus, "C14_final"),
             ("headfree", 2074, 2075, a_minus, a_plus, "C14_headfree"),
             ("crude", 1767, 1768, a_minus, a_plus, "C13_crude_final"),
             ("crude", 1761, 1762, fb_minus, fb_plus, "C13_crude_fallback"),
             ("c03", 2074, 2075, fb_minus, fb_plus, "C14_fallback")]
    for (kind, bm, bn_, am, ap, name) in edges:
        em, _ = eps6(bm, 10 ** 5)
        en, _ = eps6(bn_, 10 ** 5)
        okm, sm = met_read(kind, em, am)
        okn, gn = notmet_read(kind, en, ap)
        xm = xof(em, am)
        pole_m = mul(MU, (xm[1], xm[1]))[1]
        check("edge_" + name, okm and okn)
        say("L4P2_EDGE|%s|head=%s|MET_at_0.%05d=%d|mu^+x^+(MET)=%s|NOT_MET_at_0.%05d=%d|tag=MEASURED|json=0" % (
            name, kind, bm, int(okm), dec(pole_m, 6, up=True), bn_, int(okn)))

    # delta_1 brackets (6 * least-root bracket)
    for (kind, bn, bd, lo_s, hi_s, name) in [("c03", 2074, 10 ** 5, (1088558, 10 ** 7), (1088559, 10 ** 7), "C14_0.02074"),
                                             ("c03", 2075, 10 ** 5, (1158911, 10 ** 7), (1158912, 10 ** 7), "C14_0.02075"),
                                             ("headfree", 2074, 10 ** 5, (1088527, 10 ** 7), (1088528, 10 ** 7), "HF_0.02074"),
                                             ("headfree", 2075, 10 ** 5, (1158861, 10 ** 7), (1158862, 10 ** 7), "HF_0.02075"),
                                             ("crude", 1767, 10 ** 5, (1145675, 10 ** 7), (1145676, 10 ** 7), "C13_0.01767"),
                                             ("crude", 1768, 10 ** 5, (1150830, 10 ** 7), (1150831, 10 ** 7), "C13_0.01768"),
                                             ("crude", 1, 100, (55222, 10 ** 7), (55223, 10 ** 7), "C07_0.01")]:
        e6, _ = eps6(bn, bd)
        r = least_root(kind, e6)
        if r is None or isinstance(r[0], str):
            check("delta1_" + name, False, str(r))
            continue
        alo, ahi, den = r
        d1 = (rat(6 * alo, den)[0], rat(6 * ahi, den)[1])
        okv = inside(d1, lo_s, hi_s)
        check("delta1_" + name, okv)
        say("L4P2_DELTA1|%s|head=%s|beta=%d/%d|delta_1_in_[%s,%s]|frozen_bracket_[%d/%d,%d/%d]=%d|tag=MEASURED|json=0" % (
            name, kind, bn, bd, dec(d1[0], 10), dec(d1[1], 10, up=True), lo_s[0], lo_s[1], hi_s[0], hi_s[1], int(okv)))
        if name == "C07_0.01":
            # C16: the engine reads delta_1^+ = 6 alpha^+ with alpha^+ on dyadics of denominator 2^48
            e6c = e6
            D48 = 1 << 48
            hi48 = cdiv(ahi * D48, den)
            lo48 = fdiv(alo * D48, den)
            # find the least dyadic MET point
            while hi48 - lo48 > 1:
                mid = (lo48 + hi48) // 2
                okm, _ = met_read("crude", e6c, (mid, D48))
                if okm:
                    hi48 = mid
                else:
                    okn, _ = notmet_read("crude", e6c, (mid, D48))
                    if okn:
                        lo48 = mid
                    else:
                        break
            okh48, _ = met_read("crude", e6c, (hi48, D48))
            check("C16_alpha48_met", okh48)
            d1p = rat(6 * hi48, D48)
            e19 = iexp(rat(-19))
            d20 = mul(e19, d1p)
            osc = mul(mul(rat(512), EM1), d20)
            check("C16_delta20_le_3.093991e-11", d20[1] <= rat(3093991, 10 ** 17)[0])
            ok20 = d20[1] <= rat(30940, 10 ** 15)[0]
            okosc = osc[1] <= rat(5828, 10 ** 12)[0]
            bad = mul(e19, rat(55223, 10 ** 7))
            check("C16_delta20", ok20)
            check("C16_osc", okosc)
            say("L4P2_C16|alpha^+=%d/2^48|delta_1^+=%s|delta_20<=e^-19*delta_1^+=%s|le_3.0940e-11=%d|osc<=(512/e)delta_20=%s|le_5.828e-9=%d|e^-19*0.0055223=%s|tag=MEASURED|json=0" % (
                hi48, dec(d1p[1], 12, up=True), dec(d20[1], 17, up=True), int(ok20), dec(osc[1], 14, up=True), int(okosc),
                dec(bad[0], 17)))
            d2 = mul(EM1, d1p)
            ssum = div(d1p, sub((ONE, ONE), EM1))
            say("L4P2_C07_CHAIN|delta_2<=%s|le_2.0316e-3=%d|sum<=%s|le_8.737e-3=%d|tag=MEASURED|json=0" % (
                dec(d2[1], 9, up=True), int(d2[1] <= rat(20316, 10 ** 7)[0]), dec(ssum[1], 8, up=True),
                int(ssum[1] <= rat(8737, 10 ** 6)[0])))

    say("L4P2_END|checks=%d|failed=%d|tag=MEASURED|json=0" % (NCHK[0], NFAIL[0]))


if __name__ == "__main__":
    run()
