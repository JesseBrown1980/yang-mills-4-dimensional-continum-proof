#!/usr/bin/env python3
# L3-sec4-part1: integer interval reads of the G1 quantities that Theorem G1's
# statement, Corollary G1-frozen and check G1b point at, kappa = 1/4:
#   lambda(delta) = delta' + ln(1+delta'), delta' = delta e^delta
#   c_fin(delta)  = max{ e^{-4k}, e^{delta+lambda-5k}, e^{delta-k/2} sup_{f>=4} g(f) },
#   g(f) = e^{-(k-lambda) f} - e^{-k f}
#   c_frz(delta)  = e^delta [ e^{-4k} + sup_{n>=4} ( e^{-(k/2-2delta')n} - e^{-kn/2} ) ]
# Every number is an integer scaled by 2^P with directed (outward) rounding.
# No float, no fractions module, no decimal.  Reads at finitely many points are
# computational evidence, not proof.
P = 256
ONE = 1 << P

def cdiv(a, b): return -((-a) // b)

def exp_pos(X, up):
    # e^{X/2^P} for 0 <= X <= 2*ONE; floor terms for the lower bound, ceil + tail for upper
    # floored terms are lower bounds of the true terms (monotone recursion), so s is a
    # lower bound; the per-term floor error stays <= 3 ulps for X <= 2*ONE, and the tail
    # after the first zero term is < 8 ulps, so s + 4n + 16 is an upper bound.
    assert 0 <= X <= 2 * ONE
    s = 0; t = ONE; k = 0
    while True:
        s += t
        k += 1
        t = (t * X) // (ONE * k)
        if t == 0: break
        if k > 4000: raise SystemExit("exp did not converge")
    return s + 4 * k + 16 if up else s

def exp_big(X, up):
    # e^{X/2^P} for X >= 0 of any size: halve r times into [0, ONE], then square r times,
    # rounding each square outward in the requested direction
    r = 0
    while (X >> r) > ONE: r += 1
    Y = (X >> r) if not up else cdiv(X, 1 << r)
    v = exp_pos(Y, up)
    for _ in range(r):
        v = cdiv(v * v, ONE) if up else (v * v) // ONE
    return v

def exp_iv(lo, hi):
    # e^x on the interval [lo, hi] (scaled ints, any sign): outward
    def e_lo(x):
        if x >= 0: return exp_big(x, False)
        return (ONE * ONE) // exp_big(-x, True)
    def e_hi(x):
        if x >= 0: return exp_big(x, True)
        return cdiv(ONE * ONE, exp_big(-x, False))
    return e_lo(lo), e_hi(hi)

def ln1p_pt(X, up):
    # ln(1 + X/2^P), 0 <= X <= ONE/2: alternating series, partial sums bracket the value;
    # each term floored (error < 1 ulp per term), slack added outward
    s = 0; k = 1; pw = X; n = 0
    while True:
        term = pw // k
        if term == 0: break
        s += term if k % 2 == 1 else -term
        n += 1
        k += 1
        pw = (pw * X) // ONE
    return s + (2 * n + 4) if up else s - (2 * n + 4)

def mul_pos(a, b, up): return cdiv(a * b, ONE) if up else (a * b) // ONE

def dec(num, den):  # exact rational -> outward interval
    return (num * ONE) // den, cdiv(num * ONE, den)

KAP = dec(1, 4)

def lam_iv(d):
    elo, ehi = exp_iv(d[0], d[1])
    dp = (mul_pos(d[0], elo, False), mul_pos(d[1], ehi, True))
    return dp, (dp[0] + ln1p_pt(dp[0], False), dp[1] + ln1p_pt(dp[1], True))

def neg_exp(ylo, yhi):  # e^{-y} for y in [ylo, yhi]
    return exp_iv(-yhi, -ylo)

def g_iv(lam, f):
    k = KAP[0]  # 1/4 is exact in binary: KAP[0] == KAP[1]
    a = neg_exp((k - lam[1]) * f, (k - lam[0]) * f)
    b = neg_exp(k * f, k * f)
    return a[0] - b[1], a[1] - b[0]

def third_entry(d, lam, F=400):
    # e^{d - k/2} * sup_{f >= 4} g(f): max over 4..F, plus the tail bound g(f) <= e^{-(k-lam)F}
    best_lo = None; best_hi = 0; arg = None
    for f in range(4, F + 1):
        lo, hi = g_iv(lam, f)
        if best_lo is None or lo > best_lo: best_lo, arg = lo, f
        best_hi = max(best_hi, hi)
    tail = neg_exp((KAP[0] - lam[1]) * F, (KAP[0] - lam[0]) * F)[1]
    assert tail < best_lo, "tail cut not certified"
    pre = exp_iv(d[0] - KAP[0] // 2, d[1] - KAP[0] // 2)
    return mul_pos(pre[0], best_lo, False), mul_pos(pre[1], best_hi, True), arg

def show(x, digits=10):
    lo, hi = x
    a = (lo * 10 ** digits) // ONE; b = cdiv(hi * 10 ** digits, ONE)
    return "[%d.%0*d,%d.%0*d]" % (a // 10 ** digits, digits, a % 10 ** digits, b // 10 ** digits, digits, b % 10 ** digits)

def main():
    rows = []
    em1 = exp_iv(-ONE, -ONE)
    # delta_crit bracket: lambda(0.114846768) < 1/4 < lambda(0.114846769)
    for num in (114846768, 114846769, 1148467681):
        den = 10 ** 9 if num < 10 ** 9 else 10 ** 10
        d = dec(num, den); dp, lam = lam_iv(d)
        side = "below" if lam[1] < KAP[0] else ("above" if lam[0] > KAP[0] else "UNDECIDED")
        rows.append("L3_DELTA_CRIT|delta=%d/%d|lambda=%s|vs_1/4=%s" % (num, den, show(lam, 12), side))
    # Lemma 4.17's lambda(k/2) > k at k = 1/4
    dp, lam = lam_iv(dec(1, 8))
    rows.append("L3_LAMBDA_HALF_KAPPA|lambda(1/8)=%s|gt_1/4=%d" % (show(lam), int(lam[0] > KAP[0])))
    # flat-range end: c_fin = e^{-1} at 0.078733761, not at 0.078733762
    for num in (78733761, 78733762):
        d = dec(num, 10 ** 9); dp, lam = lam_iv(d)
        lo, hi, arg = third_entry(d, lam)
        second = exp_iv(d[0] + lam[0] - 5 * KAP[0], d[1] + lam[1] - 5 * KAP[1])
        rel = "le_e^-1" if hi <= em1[0] else ("gt_e^-1" if lo > em1[1] else "UNDECIDED")
        rows.append("L3_FLAT_END|delta=%d/10^9|lambda=%s|third_entry=%s|argmax_f=%d|second_entry=%s|e^-1=%s|third_vs_e^-1=%s"
                    % (num, show(lam), show((lo, hi)), arg, show(second), show(em1), rel))
    # c_fin(delta_crit^-) read: third entry at 0.114846768 against [0.989898,0.989899]
    d = dec(114846768, 10 ** 9); dp, lam = lam_iv(d)
    lo, hi, arg = third_entry(d, lam, F=4000)
    rows.append("L3_CFIN_NEAR_CRIT|delta=0.114846768|third_entry=%s|argmax_f=%d|in_[0.989898,0.989899]=%d"
                % (show((lo, hi)), arg, int(lo >= dec(989898, 10 ** 6)[1] and hi <= dec(989899, 10 ** 6)[0])))
    # Corollary G1-frozen: c_fin <= c_frz on 2 delta' <= k/2, at sample points (evidence only;
    # the note-level proof is entrywise, see the filing)
    for num in (1, 5, 10, 30, 50, 58):
        d = dec(num, 1000); dp, lam = lam_iv(d)
        if not (2 * dp[1] <= KAP[0] // 2):
            rows.append("L3_FROZEN_CMP|delta=%d/1000|outside_frozen_domain=1" % num); continue
        lo3, hi3, arg = third_entry(d, lam)
        e4 = exp_iv(-ONE, -ONE)
        sec = exp_iv(d[0] + lam[0] - 5 * KAP[0], d[1] + lam[1] - 5 * KAP[1])
        cfin_hi = max(e4[1], sec[1], hi3)
        # lower bound of c_frz: e^delta [ e^{-1} + bracket(n) ] at the best n in 4..400
        ed = exp_iv(d[0], d[1])
        best = 0
        for n in range(4, 401):
            a = neg_exp((KAP[0] // 2 - 2 * dp[0]) * n, (KAP[0] // 2 - 2 * dp[0]) * n)  # rate uses dp upper/lower outward below
            a = neg_exp((KAP[0] // 2 - 2 * dp[0]) * n, (KAP[0] // 2 - 2 * dp[0]) * n)
            # e^{-(k/2 - 2dp)n} is increasing in dp: its lower bound uses dp lower
            b = neg_exp(KAP[0] // 2 * n, KAP[0] // 2 * n)
            best = max(best, a[0] - b[1])
        cfrz_lo = mul_pos(ed[0], e4[0] + best, False)
        rows.append("L3_FROZEN_CMP|delta=%d/1000|cfin_upper=%s|cfrz_lower=%s|cfin_le_cfrz=%d"
                    % (num, show((cfin_hi, cfin_hi)), show((cfrz_lo, cfrz_lo)), int(cfin_hi <= cfrz_lo)))
    for r in rows: print(r + "|tag=MEASURED|json=0")

if __name__ == "__main__":
    main()
