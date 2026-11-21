#!/usr/bin/env python3
"""G1-b lane: the sharper bookkeeping c_sharp(delta) = max{e^{-4k}, e^delta max_{n>=4} g(n)},
g(n) = e^{-(k/2-2d')n} - e^{-kn/2} + [n>=9] e^{-k(n+1)/2}. Exact enclosures, as g1b_constants."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g1b_constants import *
from g1b_derived import bis
def c_sharp(d, nmax=6000):
    d = F(d); dlo, dhi = dprime(d)
    rlo, rhi = KAP / 2 - 2 * fx(dhi), KAP / 2 - 2 * fx(dlo)
    Alo, Ahi = exp_iv(-rhi, -rlo); Blo, Bhi = exp_enc(-KAP / 2)
    Clo, Chi = exp_enc(-KAP / 2)               # e^{-k(n+1)/2} = B^n * e^{-k/2}
    alo = ahi = blo = bhi = ONE
    best_lo = best_hi = None; arg = []
    for n in range(1, nmax + 1):
        alo, ahi = mul_lo(alo, Alo), mul_hi(ahi, Ahi)
        blo, bhi = mul_lo(blo, Blo), mul_hi(bhi, Bhi)
        if n < 4: continue
        glo, ghi = alo - bhi, ahi - blo
        if n >= 9:
            glo += mul_lo(blo, Clo); ghi += mul_hi(bhi, Chi)
        if best_lo is None or glo > best_lo: best_lo, arg = glo, n
        if best_hi is None or ghi > best_hi: best_hi = ghi
        if n > 9 and ahi + mul_hi(bhi, Chi) < best_lo: break
    else:
        raise RuntimeError("tail")
    elo, ehi = exp_enc(d); e1lo, e1hi = exp_enc(-4 * KAP)
    return max(e1lo, mul_lo(elo, best_lo)), max(e1hi, mul_hi(ehi, best_hi)), arg, mul_hi(ehi, best_hi) <= e1lo
def inside(d):
    ck = ck_met(d)
    if ck is False: return False
    lo, hi, _, _ = c_sharp(d)
    if ck and hi < ONE: return True
    if lo >= ONE: return False
    return None
def floor_reached(d):
    return c_sharp(d)[3] if ck_met(d) else False
if __name__ == "__main__":
    for name, d in (("C07 lo", F(11044, 10**6)), ("C07 hi", F(11045, 10**6)), ("C08 hi", F(945, 10**8)),
                    ("C14 1/64 hi", F(20348, 10**7)), ("C10b 1/2000 lo", F(26890, 10**6)), ("C10b 1/2000 hi", F(26891, 10**6)),
                    ("C10b 1/4096 lo", F(13129, 10**6)), ("C10b 1/4096 hi", F(13131, 10**6)),
                    ("C13 49/1000", F(49, 1000)), ("C13 1/20", F(1, 20))):
        lo, hi, arg, fl_ = c_sharp(d)
        print(f"{name}|c_sharp=[{show(lo,10)},{show(hi,10)}]|argmax_n={arg}|equals_e^-4k={fl_}")
    lo, hi, st = bis(floor_reached, F(1, 10**3), F(5, 100), 40)
    print("c_sharp = e^{-4k} exactly for delta <=", show(fl(lo), 11), "(edge in [", show(fl(lo), 11), ",", show(ce(hi), 11), "])", st)
    lo, hi, st = bis(inside, F(5, 100), F(589, 10**4), 40)
    print("delta_crit_sharp in", show(fl(lo), 11), show(ce(hi), 11), st)
