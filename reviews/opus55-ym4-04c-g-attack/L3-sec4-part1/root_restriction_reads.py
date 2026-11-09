#!/usr/bin/env python3
# L3-sec4-part1, entry G1_root_restriction: what m >= 1 does to the flat range of c_fin.
# Object-channel entry with the e^{-kappa/2} root factor (m >= 1) versus without it (m = 0
# roots allowed, route A's Q), each under the final rate lambda = delta'+ln(1+delta') and
# under the fallback rate 2 delta'.  Integer interval arithmetic from cfin_intervals.py,
# outward rounding, no float / fractions / decimal.  Finite reads = evidence only.
import sys
sys.path.insert(0, "/mnt/c/tmp/opus55/ym4-04c-gattack/work/L3-sec4-part1")
from cfin_intervals import ONE, KAP, dec, lam_iv, neg_exp, exp_iv, mul_pos, show

def obj_entry(d, rate, with_root_factor, F=400):
    best_lo = None; best_hi = 0; arg = None
    k = KAP[0]
    for f in range(4, F + 1):
        a = neg_exp((k - rate[1]) * f, (k - rate[0]) * f)
        b = neg_exp(k * f, k * f)
        lo, hi = a[0] - b[1], a[1] - b[0]
        if best_lo is None or lo > best_lo: best_lo, arg = lo, f
        best_hi = max(best_hi, hi)
    tail = neg_exp((k - rate[1]) * F, (k - rate[0]) * F)[1]
    assert tail < best_lo
    shift = k // 2 if with_root_factor else 0
    pre = exp_iv(d[0] - shift, d[1] - shift)
    return mul_pos(pre[0], best_lo, False), mul_pos(pre[1], best_hi, True), arg

em1 = exp_iv(-ONE, -ONE)
def rate_of(d, which):
    dp, lam = lam_iv(d)
    return lam if which == "lambda" else (2 * dp[0], 2 * dp[1])

def side(d, which, rf):
    lo, hi, arg = obj_entry(d, rate_of(d, which), rf)
    if hi <= em1[0]: return -1, (lo, hi), arg
    if lo > em1[1]: return 1, (lo, hi), arg
    return 0, (lo, hi), arg

def crossing(which, rf, a, b, digits=9):
    # integer bisection on delta = n/10^digits between a and b (side(a) = -1, side(b) = +1)
    sa = side(dec(a, 10 ** digits), which, rf)[0]; sb = side(dec(b, 10 ** digits), which, rf)[0]
    assert sa == -1 and sb == 1, (which, rf, sa, sb)
    while b - a > 1:
        m = (a + b) // 2
        s = side(dec(m, 10 ** digits), which, rf)[0]
        if s == 0: raise SystemExit("undecided at %d" % m)
        if s < 0: a = m
        else: b = m
    return a, b

for which, rf, lo, hi in (("lambda", True, 70000000, 90000000), ("2delta'", True, 70000000, 90000000),
                          ("lambda", False, 60000000, 80000000), ("2delta'", False, 60000000, 80000000)):
    a, b = crossing(which, rf, lo, hi)
    _, va, fa = side(dec(a, 10 ** 9), which, rf); _, vb, fb = side(dec(b, 10 ** 9), which, rf)
    print("L3_ROOT_RESTRICTION|rate=%s|roots=%s|flat_end_last_delta=%d/10^9|object_entry=%s|f=%d|first_delta_above=%d/10^9|object_entry=%s|f=%d|tag=MEASURED|json=0"
          % (which, "m>=1(e^{-k/2})" if rf else "m>=0(no_factor)", a, show(va), fa, b, show(vb), fb))
