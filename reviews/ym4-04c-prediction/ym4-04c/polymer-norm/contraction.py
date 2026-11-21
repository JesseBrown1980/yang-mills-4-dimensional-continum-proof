#!/usr/bin/env python3
"""Scratch: pinned contraction bound c(delta) for steps k>=1 (design lane, exact rationals).

c(d) = e^d [ e^{-4k} + max_{n>=4} ( e^{-(k/2 - 2d')n} - e^{-k n/2} ) ],  d' = d e^d, k = 1/4,
valid while 2d' <= k/2 (a = t = d', b = k). Upper bounds via exp_bounds; max over n scanned to 4000
(terms decay geometrically once n exceeds the maximiser).
"""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from derive_estimates import exp_bounds, dec
K = Fr(1, 4)
def eu(y): return exp_bounds(Fr(y), Fr(1, 10**25))[1]
def el(y): return exp_bounds(Fr(y), Fr(1, 10**25))[0]

def c_upper(d):
    d = Fr(d)
    dp = d * eu(d)
    if 2 * dp > K / 2:
        return None
    r = K / 2 - 2 * dp
    best = Fr(0)
    # f(n) = e^{-r n} - e^{-K n/2}; maximiser n* = ln((K/2)/r)/(K/2 - r); scan integers near it
    import math
    if r > 0:
        lo = 4
        # integer scan with a coarse bound on n*
        nstar_hi = int(4 * 8 / max(1e-9, float(r))) + 50
    else:
        return None
    for n in range(4, min(nstar_hi, 4000)):
        v = el(-r * n) if False else eu(-r * n) - el(-K * n / 2)
        if v > best:
            best = v
    return eu(d) * (eu(-4 * K) + best)

if __name__ == "__main__":
    for d in (Fr(943, 10**8), Fr(1105, 10**5), Fr(203, 10**5), Fr(3, 100), Fr(4, 100), Fr(45, 1000), Fr(48, 1000), Fr(49, 1000), Fr(50, 1000), Fr(52, 1000)):
        c = c_upper(d)
        print("delta", dec(d), "c<=", dec(c) if c else None, flush=True)
    # bisection for delta_c with c < 1
    lo, hi = Fr(40, 1000), Fr(55, 1000)
    for _ in range(14):
        m = (lo + hi) / 2
        c = c_upper(m)
        if c is not None and c < 1: lo = m
        else: hi = m
    print("delta_c in", dec(lo), dec(hi))
