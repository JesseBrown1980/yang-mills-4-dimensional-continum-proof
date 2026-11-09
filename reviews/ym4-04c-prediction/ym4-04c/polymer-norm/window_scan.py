#!/usr/bin/env python3
"""Scratch: crude and head-free Kotecky-Preiss windows for the b=2 line blocking (design lane).

Exact rationals. KP(beta;a,b): sum_{n>=4} c_n x^n <= a with x = eps6(beta) e^(2a+b), b >= kappa,
c_n = 6 F_20(n) (crude) or c_n = 0 for n<=10, 6 F_20(n) beyond (head-free upper limit).
Tail beyond N: F(n+1)/F(n) < mu, so sum_{n>N} <= 6F(N+1)x^(N+1)/(1-mu x).
"""
from fractions import Fraction as Fr
from math import comb
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from derive_estimates import exp_bounds, eps6_upper, dec, F

D = 20
MU = Fr(D**D, (D - 1) ** (D - 1))
FN = {n: F(D, n) for n in range(1, 80)}

def S(x, head_free, N=60):
    if MU * x >= 1:
        return None
    s = Fr(0)
    xn = x ** 4
    for n in range(4, N + 1):
        if not (head_free and n <= 10):
            s += 6 * FN[n] * xn
        xn *= x
    s += 6 * FN[N + 1] * x ** (N + 1) / (1 - MU * x)
    return s

KAPPA = Fr(1, 4)
EXP_CACHE = {}
def eup(y):
    if y not in EXP_CACHE:
        EXP_CACHE[y] = exp_bounds(y, Fr(1, 10**30))[1]
    return EXP_CACHE[y]

def feasible(beta, head_free, need_delta=None):
    eps = eps6_upper(beta)
    best = None
    for i in range(0, 25):
        b = KAPPA + Fr(i, 16)
        for j in range(1, 129):
            a = Fr(j, 512)
            x = eps * eup(2 * a + b)
            s = S(x, head_free)
            if s is None or s > a:
                continue
            if need_delta is not None:
                # delta_1 <= 12 a e^{-m(b-kappa)}, m = 4 (crude) or 11 (head-free, exact head)
                m = 11 if head_free else 4
                d1 = 12 * a / eup(m * (b - KAPPA)) if b > KAPPA else 12 * a
                # use lower bound of e^{..} -> upper bound on d1: divide by lower bound
                if d1 > need_delta:
                    continue
            return (a, b, s)
    return None

def window(head_free, need_delta=None, lo=Fr(1, 1000), hi=Fr(1, 25), den=10000):
    # largest beta=j/den feasible, assuming monotone
    jlo, jhi = int(lo * den), int(hi * den)
    assert feasible(Fr(jlo, den), head_free, need_delta)
    assert not feasible(Fr(jhi, den), head_free, need_delta)
    while jhi - jlo > 1:
        mid = (jlo + jhi) // 2
        if feasible(Fr(mid, den), head_free, need_delta):
            jlo = mid
        else:
            jhi = mid
    return Fr(jlo, den), Fr(jhi, den), feasible(Fr(jlo, den), head_free, need_delta)

def wall(kappa_factor, den=100000):
    # largest beta=j/den with mu*e^{kappa_factor}*eps6 < 1
    jlo, jhi = 100, 4000
    f = eup(kappa_factor) if kappa_factor else Fr(1)
    while jhi - jlo > 1:
        mid = (jlo + jhi) // 2
        if MU * f * eps6_upper(Fr(mid, den)) < 1:
            jlo = mid
        else:
            jhi = mid
    return Fr(jlo, den), Fr(jhi, den)

if __name__ == "__main__":
    print("wall_b0", [dec(v) for v in wall(0)])
    print("wall_kappa", [dec(v) for v in wall(KAPPA)])
    for hf in (False, True):
        lo, hi, w = window(hf)
        print("window head_free=%s" % hf, dec(lo), dec(hi), "a=%s b=%s S=%s" % (w[0], w[1], dec(w[2])))
    DCRIT = Fr(589, 10000)
    for hf in (False, True):
        lo, hi, w = window(hf, need_delta=DCRIT)
        print("induction head_free=%s" % hf, dec(lo), dec(hi), "a=%s b=%s" % (w[0], w[1]))
    for beta in (Fr(1, 1000), Fr(1, 100), Fr(1, 64), Fr(1, 50)):
        for hf in (False, True):
            r = feasible(beta, hf)
            print("beta", beta, "head_free", hf, "feasible", bool(r), (str(r[0]), str(r[1]), dec(r[2])) if r else "")
