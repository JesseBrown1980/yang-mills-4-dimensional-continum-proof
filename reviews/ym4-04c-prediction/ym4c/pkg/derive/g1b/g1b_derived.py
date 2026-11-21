#!/usr/bin/env python3
"""G1-b lane: delta_crit for c_B and frozen c, the coincidence edge delta_eq, and the C07/C08/C16 chains."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g1b_constants import *
def bis(pred_lo_ok, lo, hi, steps):
    """pred_lo_ok(x): True if certainly 'inside', False if certainly outside; returns bracket."""
    for _ in range(steps):
        m = (lo + hi) / 2
        r = pred_lo_ok(m)
        if r is True: lo = m
        elif r is False: hi = m
        else: return lo, hi, "undecided"
    return lo, hi, "ok"
def inside_B(d):
    ck = ck_met(d)
    if ck is False: return False
    lo, hi = cB(d)
    if ck and hi < ONE: return True
    if lo >= ONE: return False
    return None
def inside_F(d):
    ck = ck_met(d)
    if ck is False: return False
    lo, hi, _ = c_frozen(d)
    if ck and hi < ONE: return True
    if lo >= ONE: return False
    return None
def f89(d):
    """sign of f(8)-f(9): True if f(8) > f(9) certainly."""
    d = F(d); dlo, dhi = dprime(d)
    # f(9)-f(8) = B^8(1-B) - A^8(1-A), A = e^{-r}, B = e^{-1/8}; increasing in delta'
    def g(dp):
        r = KAP / 2 - 2 * dp
        Alo, Ahi = exp_enc(-r); Blo, Bhi = exp_enc(-KAP / 2)
        A8lo, A8hi = pw(Alo, Ahi, 8); B8lo, B8hi = pw(Blo, Bhi, 8)
        lo = mul_lo(B8lo, ONE - Bhi) - mul_hi(A8hi, ONE - Alo)
        hi = mul_hi(B8hi, ONE - Blo) - mul_lo(A8lo, ONE - Ahi)
        return lo, hi
    lo1, hi1 = g(fx(dlo)); lo2, hi2 = g(fx(dhi))
    lo, hi = min(lo1, lo2), max(hi1, hi2)
    if hi < 0: return True
    if lo > 0: return False
    return None
if __name__ == "__main__":
    lo, hi, st = bis(inside_B, F(5, 100), F(6, 100), 40)
    print("delta_crit_B in", show(fl(lo), 11), show(ce(hi), 11), st)
    print("  2delta' at delta_crit_B hi:", show(2 * dprime(hi)[1], 9), "(<= 1/8 needed)")
    lo, hi, st = bis(inside_F, F(49, 1000), F(50, 1000), 40)
    print("delta_crit_frozen in", show(fl(lo), 11), show(ce(hi), 11), st)
    lo, hi, st = bis(f89, F(1, 10**4), F(2, 100), 40)
    print("delta_eq (frozen c == c_B for delta <= delta_eq) in", show(fl(lo), 11), show(ce(hi), 11), st)
    # C_k edge alone: 2 delta e^delta = 1/8
    lo, hi, st = bis(ck_met, F(5, 100), F(7, 100), 40)
    print("C_k edge (2 delta e^delta = kappa/2) in", show(fl(lo), 11), show(ce(hi), 11), st)
    # chains
    for name, d1lo, d1hi in (("C07 crude 1/100", F(11044, 10**6), F(11045, 10**6)),
                             ("C08 refined 1/100", F(942, 10**8), F(945, 10**8)),
                             ("C14 refined 1/64", F(20347, 10**7), F(20348, 10**7))):
        for lab, cfun in (("frozen", lambda d: c_frozen(d)[:2]), ("c_B", cB)):
            clo, chi = cfun(d1hi)                       # c increasing: upper bound at the bracket top
            d2 = mul_hi(chi, ce(d1hi))
            ssum = d1hi / (1 - fx(chi))
            c19lo, c19hi = pw(*cfun(d1lo), 19)
            c19 = pw(*cfun(d1hi), 19)[1]
            d20lo, d20hi = mul_lo(c19lo, fl(d1lo)), mul_hi(c19, ce(d1hi))
            osc = F(512) * fx(d20hi) * fx(exp_enc(-1)[1])
            print(f"{name}|{lab}|c(delta1_hi)<={show(chi,6)}|delta2<={float(fx(d2)):.6e}|sum<={float(ssum):.6e}|delta20 in [{float(fx(d20lo)):.4e},{float(fx(d20hi)):.4e}]|osc20<={float(osc):.4e}")
    for name, d in (("C11 crude 1/64", F(10165, 10**5)), ("C12 headfree 1/50", F(72645, 10**6))):
        dl, dh = dprime(d)
        print(name, "2delta' >=", show(2 * dl, 6), "C_k:", ck_met(d))
