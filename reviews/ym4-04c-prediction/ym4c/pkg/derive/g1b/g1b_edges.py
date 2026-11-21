#!/usr/bin/env python3
"""G1-b lane: where the self-map stops when the proved c_B replaces the frozen c (C13/C14 edges).
Exact: Fractions and dyadic outward rounding. The C_0 certificate at b = 1/4 only (the G0 claim that
b = 1/4 decides existence and carries every delta_1 optimum is relied on, not reproved here)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g1b_constants import F, fl, ce, fx, exp_enc, ONE, P
from math import comb, factorial
Q = 1 << 200
def dn(x): x = F(x); return F((x.numerator * Q) // x.denominator, Q)
def up(x): x = F(x); return F(-((-x.numerator * Q) // x.denominator), Q)
def c0(x):
    x = F(x); s = F(0); t = F(1); m = 0; h2 = (x / 2) ** 2
    while True:
        s += t; t = t * h2 / ((m + 1) * (m + 2)); m += 1
        r = h2 / ((m + 1) * (m + 2))
        if m > 3 and r < F(1, 2) and t < F(1, 1 << 400):
            return s, s + t / (1 - r)
def eps6(beta):
    beta = F(beta); clo, chi = c0(beta)
    lo = hi = F(0)
    for k in range(7):
        cklo, ckhi = c0(k * beta) if k else (F(1), F(1))
        coef = comb(6, k) * (-1) ** (6 - k)
        tlo, thi = cklo / chi ** k, ckhi / clo ** k
        if coef > 0: lo += coef * tlo; hi += coef * thi
        else: lo += coef * thi; hi += coef * tlo
    assert lo > 0
    def root6(v, upward):
        a, b = F(0), F(1)
        for _ in range(120):
            m = (a + b) / 2
            if m ** 6 <= v: a = m
            else: b = m
        return b if upward else a
    return root6(lo, False), root6(hi, True)
def Fc(n): return comb(20 * n, n) // (19 * n + 1)
MU = F(20 ** 20, 19 ** 19)
HEADS = {"crude": {n: 6 * Fc(n) for n in range(4, 11)},
         "headfree": {n: 0 for n in range(4, 11)},
         "refined": {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}}
def S(x, head):
    if MU * x >= 1: return None
    s = F(0); xn = x ** 4
    for n in range(4, 49):
        c = head[n] if n <= 10 else 6 * Fc(n)
        s += c * xn; xn *= x
    return s + 6 * Fc(49) * xn / (1 - MU * x)     # xn = x^49 here
def xval(e, a, upward):
    lo, hi = exp_enc(2 * a + F(1, 4))
    return up(e * fx(hi)) if upward else dn(e * fx(lo))
def admissible(beta, head, dcrit_minus, maxit=4000):
    elo, ehi = eps6(beta)
    astar = dn(dcrit_minus / 12) - F(1, 1 << 80)
    s = S(xval(ehi, astar, True), head)
    if s is not None and s <= astar <= F(1, 4):
        return True, astar
    a = F(0)                                      # monotone iteration from below with lower bounds
    for it in range(maxit):
        s = S(xval(elo, a, False), head)
        if s is None: return False, a
        s = dn(s)
        if s > astar: return False, s
        if s <= a: return None, a                 # stalled below astar: undecided
        a = s
    return None, a
if __name__ == "__main__":
    which = sys.argv[1]; dcm = F(sys.argv[2]); lo_i, hi_i = int(sys.argv[3]), int(sys.argv[4])
    head = HEADS[which]
    # bisection on the 10^-5 grid: lo_i admissible, hi_i not
    for i in (lo_i, hi_i):
        print(which, i, admissible(F(i, 10 ** 5), head, dcm)[0], flush=True)
    while hi_i - lo_i > 1:
        m = (lo_i + hi_i) // 2
        r = admissible(F(m, 10 ** 5), head, dcm)[0]
        print(which, m, r, flush=True)
        if r is True: lo_i = m
        elif r is False: hi_i = m
        else: print("undecided at", m); break
    print(f"EDGE|{which}|delta_crit^-={dcm}|MET_at={lo_i/1e5:.5f}|NOT_MET_at={hi_i/1e5:.5f}")
