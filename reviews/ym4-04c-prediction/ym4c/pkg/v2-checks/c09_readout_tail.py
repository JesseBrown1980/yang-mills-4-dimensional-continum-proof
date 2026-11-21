#!/usr/bin/env python3
"""YM4-04C v2 repair lane: P_10 - 2 t_2^4 at beta = 1/4000, 1/2000, 1/1000 (readout_without_tail), exact enclosures.
t_2 = I_2/I_1, I_n(x) = sum_m (x/2)^{2m+n}/(m!(m+n)!), positive series with a geometric tail bound."""
from fractions import Fraction as Fr
from math import factorial
def I(n, x, M=40):
    h = x / 2; s = Fr(0)
    for m in range(M):
        s += h**(2*m+n) / (factorial(m)*factorial(m+n))
    nxt = h**(2*M+n) / (factorial(M)*factorial(M+n)); r = h*h/((M+1)*(M+1+n))
    return s, s + nxt/(1 - r)
def P10(b): return b**4/128 - b**6/768 + b**8/1536 - Fr(467, 2211840)*b**10
for b in (Fr(1, 4000), Fr(1, 2000), Fr(1, 1000)):
    i1, i2 = I(1, b), I(2, b)
    t2 = (i2[0]/i1[1], i2[1]/i1[0])
    d = (P10(b) - 2*t2[1]**4, P10(b) - 2*t2[0]**4)
    lead = b**8/2048
    print(f"beta={b}: P_10-2t_2^4 in [{float(d[0]):.10e},{float(d[1]):.10e}] > 0: {d[0] > 0}; ratio to beta^8/2048 in [{float(d[0]/lead):.10f},{float(d[1]/lead):.10f}]")
