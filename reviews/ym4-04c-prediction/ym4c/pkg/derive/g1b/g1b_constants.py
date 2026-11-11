#!/usr/bin/env python3
"""G1-b lane: exact enclosures of the frozen c(delta) and the route-B proved c_B(delta).
Integers and Fractions only. Fixed point at scale 2^P with directed rounding. Floats only in display."""
from fractions import Fraction as F
import sys
P = 256
ONE = 1 << P
def fl(x): x = F(x); return (x.numerator << P) // x.denominator
def ce(x): x = F(x); return -((-x.numerator << P) // x.denominator)
def fx(i): return F(i, ONE)
def mul_lo(a, b): return (a * b) >> P            # a, b >= 0
def mul_hi(a, b): return -((-(a * b)) >> P)
def exp_small(q):
    """enclosure of e^q for a Fraction q with |q| <= 1/2, as fixed-point (lo, hi)."""
    q = F(q); assert abs(q) <= F(1, 2)
    s = F(0); t = F(1); k = 0
    while True:
        s += t; k += 1; t = t * q / k
        if k > 3 and abs(t) < F(1, 1 << (P + 20)):
            break
    rem = abs(t) / (1 - abs(q) / (k + 1))
    return fl(s - rem), ce(s + rem)
def exp_enc(q):
    """e^q for any Fraction q: e^q = (e^{q/2^m})^{2^m}, positive interval, rounding outward."""
    q = F(q); m = 0
    while abs(q) / (1 << m) > F(1, 2):
        m += 1
    lo, hi = exp_small(q / (1 << m))
    for _ in range(m):
        lo, hi = mul_lo(lo, lo), mul_hi(hi, hi)
    return lo - 1, hi + 1
def exp_iv(qlo, qhi):
    """e^q for q in [qlo, qhi] (Fractions): monotone."""
    return exp_enc(qlo)[0], exp_enc(qhi)[1]
def pw(lo, hi, n):
    a, b = ONE, ONE
    for _ in range(n):
        a, b = mul_lo(a, lo), mul_hi(b, hi)
    return a, b
KAP = F(1, 4)
def dprime(d):
    d = F(d); elo, ehi = exp_enc(d)
    return (fl(d * fx(elo)), ce(d * fx(ehi)))
def ck_met(d):
    """C_k: 2 delta' <= kappa/2. Returns True (certainly MET), False (certainly NOT_MET) or None."""
    lo, hi = dprime(d)
    if 2 * fx(hi) <= KAP / 2: return True
    if 2 * fx(lo) > KAP / 2: return False
    return None
def cB(d):
    """route-B proved c_B(delta) = exp(delta + 16 delta' - 4 kappa) (kappa = 1/4)."""
    d = F(d); lo, hi = dprime(d)
    return exp_iv(d + 16 * fx(lo) - 4 * KAP, d + 16 * fx(hi) - 4 * KAP)
def c_frozen(d, nmax=4000):
    """frozen c(delta) = e^delta [e^{-4k} + max_{n>=4}(e^{-(k/2-2d')n} - e^{-kn/2})]; returns (lo, hi, argmax set)."""
    d = F(d); dlo, dhi = dprime(d)
    rlo, rhi = KAP / 2 - 2 * fx(dhi), KAP / 2 - 2 * fx(dlo)
    assert rlo >= 0
    Alo, Ahi = exp_iv(-rhi, -rlo)          # e^{-r}
    Blo, Bhi = exp_enc(-KAP / 2)            # e^{-kappa/2}
    alo, ahi = ONE, ONE; blo, bhi = ONE, ONE
    best_lo = best_hi = None; arg = []
    vals = {}
    for n in range(1, nmax + 1):
        alo, ahi = mul_lo(alo, Alo), mul_hi(ahi, Ahi)
        blo, bhi = mul_lo(blo, Blo), mul_hi(bhi, Bhi)
        if n < 4: continue
        flo, fhi = alo - bhi, ahi - blo
        vals[n] = (flo, fhi)
        if best_lo is None or flo > best_lo: best_lo = flo
        if best_hi is None or fhi > best_hi: best_hi = fhi
        if ahi < best_lo and n > 8: break     # f(m) <= e^{-r m} <= e^{-r n} < max for all m >= n
    else:
        raise RuntimeError("tail not closed")
    arg = [n for n, (a, b) in vals.items() if b >= best_lo]
    elo, ehi = exp_enc(d); e1lo, e1hi = exp_enc(-4 * KAP)
    return mul_lo(elo, e1lo + best_lo), mul_hi(ehi, e1hi + best_hi), arg
def show(i, k=10): return ("%." + str(k) + "f") % float(fx(i))   # display only
if __name__ == "__main__":
    pts = [("C07 crude 1/100 lo", F(11044, 10**6)), ("C07 crude 1/100 hi", F(11045, 10**6)),
           ("C07 critic", F(110444507, 10**10)),
           ("C08 refined lo", F(942, 10**8)), ("C08 refined hi", F(945, 10**8)),
           ("C08 headfree", F(93723, 10**10)),
           ("C14 1/64 refined lo", F(20347, 10**7)), ("C14 1/64 refined hi", F(20348, 10**7)),
           ("C10b s=1/2000 lo", F(26890, 10**6)), ("C10b s=1/2000 hi", F(26891, 10**6)),
           ("C10b s=1/4096 lo", F(13129, 10**6)), ("C10b s=1/4096 hi", F(13131, 10**6)),
           ("C13 49/1000", F(49, 1000)), ("C13 1/20", F(1, 20)),
           ("dcrit frozen lo", F(496174, 10**7)), ("dcrit frozen hi", F(496175, 10**7))]
    for name, d in pts:
        flo, fhi, arg = c_frozen(d)
        blo, bhi = cB(d)
        dl, dh = dprime(d)
        print(f"{name}|delta={d}|2d'=[{show(2*dl,7)},{show(2*dh,7)}]|C_k={ck_met(d)}|c_frozen=[{show(flo)},{show(fhi)}]|argmax_n={arg}|c_B=[{show(blo)},{show(bhi)}]|equal={'yes' if (fhi < blo or bhi < flo) is False else 'no'}", flush=True)
