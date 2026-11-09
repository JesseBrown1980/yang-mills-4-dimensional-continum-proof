#!/usr/bin/env python3
"""Scratch: best delta_1 and readout tail T on the pinned (a,b) grid (design lane)."""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from window_scan import S, eup, KAPPA, MU
from derive_estimates import eps6_upper, dec, exp_bounds

def elo(y):
    return exp_bounds(y, Fr(1, 10**30))[0]

def best(beta, head_free, m):
    eps = eps6_upper(beta)
    bestv = None
    for i in range(0, 129):
        b = KAPPA + Fr(i, 16)
        for j in range(1, 129):
            a = Fr(j, 512)
            x = eps * eup(2 * a + b)
            s = S(x, head_free)
            if s is None or s > a:
                continue
            v = 12 * a / elo(m * (b - KAPPA))
            if bestv is None or v < bestv[0]:
                bestv = (v, a, b)
            break  # smallest feasible a for this b
    return bestv

for beta in (Fr(1, 2000), Fr(1, 1000), Fr(1, 700), Fr(1, 500), Fr(1, 300), Fr(1, 100), Fr(1, 64), Fr(1, 50)):
    c_half = beta**4 / 128 - beta**6 / 768 + beta**8 / 1536 - Fr(467, 2211840) * beta**10
    crude = best(beta, False, 4)
    hf = best(beta, True, 11)
    line = f"beta={beta}|c_half_P10={dec(c_half)}|beta1_P10={dec(2*c_half)}"
    if crude:
        line += f"|crude_delta1<={dec(crude[0])}(a={crude[1]},b={crude[2]})"
    if hf:
        T = Fr(8489, 10000) * hf[0]
        line += f"|refined_delta1_tail<={dec(hf[0])}(a={hf[1]},b={hf[2]})|T_readout<={dec(T)}|T/c_half={dec(T/c_half)}"
    print(line)
