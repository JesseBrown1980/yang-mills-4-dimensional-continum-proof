#!/usr/bin/env python3
"""Scratch: KP windows with least-a fixed point, b on 1/64 grid, three head models (design lane)."""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from delta_scan3 import up, eup, elo, MU, FN, KAPPA
from derive_estimates import eps6_upper, dec

def S(x, head):
    if MU * x >= 1:
        return None
    s = Fr(0); xn = x ** 4
    for n in range(4, 49):
        c = head.get(n, 6 * FN[n]) if n <= 10 else 6 * FN[n]
        s += c * xn
        xn = up(xn * x)
    s += 6 * FN[49] * x ** 49 / (1 - MU * x)
    return up(s)

def least_a(eps, b, head, amax=Fr(1, 4)):
    a = Fr(0)
    for _ in range(400):
        x = up(eps * eup(2 * a + b))
        s = S(x, head)
        if s is None or s > amax:
            return None
        if s <= a:
            return a
        a = up(s * Fr(10001, 10000))
    return None

def best_delta(beta, head):
    eps = up(eps6_upper(beta)); bestv = None
    for i in range(0, 129):
        b = KAPPA + Fr(i, 64)
        a = least_a(eps, b, head)
        if a is None:
            if bestv is not None:
                break
            continue
        v = 12 * a / elo(4 * (b - KAPPA))
        if bestv is None or v < bestv[0]:
            bestv = (v, a, b)
    return bestv

def window(head, dmax=None, den=100000, jlo=1000, jhi=2500):
    def ok(j):
        r = best_delta(Fr(j, den), head)
        return r is not None and (dmax is None or r[0] <= dmax)
    assert ok(jlo) and not ok(jhi)
    while jhi - jlo > 1:
        m = (jlo + jhi) // 2
        if ok(m): jlo = m
        else: jhi = m
    return Fr(jlo, den), Fr(jhi, den)

CRUDE = {}
FREE = {n: 0 for n in range(4, 11)}
SMALL = {4: 1, 5: 0, 6: 12, 7: 0, 8: 200, 9: 0, 10: 20000}
if __name__ == "__main__":
    DCRIT = Fr(303, 10000)
    for name, head in (("crude", CRUDE), ("small_counts", SMALL), ("head_free", FREE)):
        w = window(head)
        wi = window(head, DCRIT)
        print(name, "step0_window", dec(w[0]), dec(w[1]), "induction_window(delta1<=0.0303)", dec(wi[0]), dec(wi[1]), flush=True)
    for beta in (Fr(1, 100), Fr(1, 64), Fr(1, 50)):
        for name, head in (("crude", CRUDE), ("small_counts", SMALL)):
            r = best_delta(beta, head)
            print(beta, name, dec(r[0]) if r else None, (str(r[2]), dec(r[1])) if r else "", flush=True)
