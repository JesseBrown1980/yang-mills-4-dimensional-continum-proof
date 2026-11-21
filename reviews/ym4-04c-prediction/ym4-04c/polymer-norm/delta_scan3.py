#!/usr/bin/env python3
"""Scratch: minimal KP parameter a by monotone fixed-point iteration, dyadic outward rounding.

For fixed b, a_{k+1} = S(eps e^{2 a_k + b}) from a_0 = 0 increases to the least a with S <= a,
if one exists. Readout tail T = 0.8489*12*a*e^{-8b}; norm tail delta = 12*a*e^{-8(b-kappa)}.
"""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from derive_estimates import eps6_upper, dec, exp_bounds, F

D = 20
MU = Fr(D**D, (D - 1) ** (D - 1))
FN = {n: F(D, n) for n in range(1, 80)}
KAPPA = Fr(1, 4)
BITS = 160

def up(x):
    # upward rounding to BITS significant bits (x >= 0)
    if x == 0:
        return x
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = BITS - e
    if sh >= 0:
        n = -((-x.numerator * 2**sh) // x.denominator)
        return Fr(n, 2**sh)
    n = -((-x.numerator) // (x.denominator * 2**(-sh)))
    return Fr(n * 2**(-sh))

EC = {}
def eup(y):
    y = up(y)
    if y not in EC:
        EC[y] = up(exp_bounds(y, Fr(1, 2**BITS))[1])
    return EC[y]
def elo(y):
    return exp_bounds(y, Fr(1, 2**BITS))[0]

def S(x, nmin_exact, N=48):
    if MU * x >= 1:
        return None
    s = Fr(0)
    xn = x ** 4
    for n in range(4, N + 1):
        if n >= nmin_exact:
            s += 6 * FN[n] * xn
        xn = up(xn * x)
    s += 6 * FN[N + 1] * x ** (N + 1) / (1 - MU * x)
    return up(s)

def least_a(eps, b, nmin_exact, amax=Fr(1, 4)):
    a = Fr(0)
    for _ in range(200):
        s = S(up(eps * eup(2 * a + b)), nmin_exact)
        if s is None or s > amax:
            return None
        if s <= a:
            return a
        a = up(s * Fr(1001, 1000))
    return None

def best(beta, nmin_exact, m, weight_kappa=True):
    eps = up(eps6_upper(beta))
    bestv = None
    for i in range(0, 81):
        b = KAPPA + Fr(i, 16)
        a = least_a(eps, b, nmin_exact)
        if a is None:
            continue
        shift = (b - KAPPA) if weight_kappa else b
        v = 12 * a / elo(m * shift)
        if bestv is None or v < bestv[0]:
            bestv = (v, a, b)
    return bestv

if __name__ == "__main__":
    for beta in (Fr(1, 2000), Fr(1, 1000), Fr(1, 700), Fr(1, 500), Fr(1, 300), Fr(1, 200), Fr(1, 100), Fr(1, 64), Fr(1, 50)):
        c_half = beta**4 / 128 - beta**6 / 768 + beta**8 / 1536 - Fr(467, 2211840) * beta**10
        crude = best(beta, 4, 4)
        hf = best(beta, 11, 11)
        T = best(beta, 4, 8, weight_kappa=False)
        line = f"beta={beta}|beta1_P10={dec(2*c_half)}"
        if crude:
            line += f"|crude_delta1<={dec(crude[0])}(b={crude[2]},a={dec(crude[1])})"
        if hf:
            line += f"|headfree_delta1<={dec(hf[0])}(b={hf[2]})"
        if T:
            TT = Fr(8489, 10000) * T[0]
            line += f"|T_readout_crudecounts<={dec(TT)}(b={T[2]})|T/c_half={dec(TT/c_half)}"
        print(line, flush=True)
