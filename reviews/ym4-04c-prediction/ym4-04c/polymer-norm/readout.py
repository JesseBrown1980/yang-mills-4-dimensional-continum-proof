#!/usr/bin/env python3
"""Scratch: filling-only readout tail T = (8489/10000)*12*a*e^{-8b} under count models (design lane)."""
from fractions import Fraction as Fr
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from window2 import least_a, SMALL, CRUDE
from delta_scan3 import up, elo, KAPPA
from derive_estimates import eps6_upper, dec

def bestT(beta, head):
    eps = up(eps6_upper(beta)); bestv = None
    for i in range(0, 321):
        b = KAPPA + Fr(i, 64)
        a = least_a(eps, b, head)
        if a is None:
            if bestv is not None:
                break
            continue
        T = Fr(8489, 10000) * 12 * a / elo(8 * b)
        if bestv is None or T < bestv[0]:
            bestv = (T, a, b)
    return bestv

for beta in (Fr(1, 4000), Fr(1, 2000), Fr(1, 1500), Fr(1, 1000), Fr(1, 700), Fr(1, 500), Fr(1, 100)):
    c = beta**4 / 128 - beta**6 / 768 + beta**8 / 1536 - Fr(467, 2211840) * beta**10
    r = bestT(beta, SMALL)
    print(f"beta={beta}|P10={dec(c)}|T_small={dec(r[0])}|T/P10={dec(r[0]/c)}|b={r[2]}", flush=True)
