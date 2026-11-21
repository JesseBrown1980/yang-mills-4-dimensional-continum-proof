#!/usr/bin/env python3
"""Scratch derivation checks for a YM4-04C polymer-norm prediction (design lane only).

Exact rationals and integers only. Closed-form quantities a frozen prediction can quote:
c0(x)=2 I1(x)/x, the L^2, L^6 and sup norms of K=e^{beta a}/c0-1 on SU(2), Fuss-Catalan
counts F_D(n)=C(Dn,n)/((D-1)n+1), the crude Kotecky-Preiss window, and two bracket walls.
"""
from fractions import Fraction as Fr
from math import comb, factorial
import sys

def c0(x, terms=None):
    # c0(x) = sum_m (x/2)^(2m)/(m!(m+1)!) , all terms positive; return [lo,hi]
    x = Fr(x)
    s = Fr(0)
    m = 0
    q = (x / 2) ** 2
    term = Fr(1)
    while True:
        s += term
        nxt = term * q / ((m + 1) * (m + 2))
        # ratio of subsequent terms <= q/((m+2)(m+3)) decreasing
        r = q / ((m + 2) * (m + 3))
        if m > 4 and r < Fr(1, 2) and nxt < Fr(1, 10**60):
            tail_hi = nxt / (1 - r)
            return s, s + tail_hi
        term = nxt
        m += 1

def exp_bounds(x, eps=Fr(1, 10**60)):
    x = Fr(x)
    neg = x < 0
    y = -x if neg else x
    s = Fr(0); term = Fr(1); n = 0
    while True:
        s += term
        nxt = term * y / (n + 1)
        r = y / (n + 2)
        if n > 2 and r < Fr(1, 2) and nxt < eps:
            lo, hi = s, s + nxt / (1 - r)
            break
        term = nxt; n += 1
    if neg:
        return 1 / hi, 1 / lo
    return lo, hi

def norms(beta):
    beta = Fr(beta)
    c0lo, c0hi = c0(beta)
    elo, ehi = exp_bounds(beta)
    sup_lo = elo / c0hi - 1
    sup_hi = ehi / c0lo - 1
    # ||K||_2^2 = c0(2b)/c0(b)^2 - 1
    c2lo, c2hi = c0(2 * beta)
    l2sq_lo = c2lo / c0hi**2 - 1
    l2sq_hi = c2hi / c0lo**2 - 1
    # E[K^6] = sum_k C(6,k)(-1)^(6-k) c0(k b)/c0(b)^k ; need tight: use high-precision c0
    # cancellations: compute with interval arithmetic carefully
    lo = Fr(0); hi = Fr(0)
    for k in range(7):
        ck_lo, ck_hi = c0(k * beta) if k else (Fr(1), Fr(1))
        coef = comb(6, k) * (-1) ** (6 - k)
        # term = coef * ck / c0^k
        t_lo = ck_lo / c0hi**k
        t_hi = ck_hi / c0lo**k
        if coef > 0:
            lo += coef * t_lo; hi += coef * t_hi
        else:
            lo += coef * t_hi; hi += coef * t_lo
    return (sup_lo, sup_hi), (l2sq_lo, l2sq_hi), (lo, hi)

def root_bracket(v, n, den=10**9):
    # rational bracket of v^(1/n) on grid 1/den
    v = Fr(v)
    lo, hi = 0, den * 10
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Fr(mid, den) ** n <= v:
            lo = mid
        else:
            hi = mid
    return Fr(lo, den), Fr(hi, den)

def dec(x, digits=8):
    x = Fr(x)
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x == 0:
        return "0"
    # scientific
    e = 0
    while x >= 10:
        x /= 10; e += 1
    while x < 1:
        x *= 10; e -= 1
    m = int(x * 10**digits)
    s = str(m)
    return f"{sign}{s[0]}.{s[1:]}e{e}"

def F(D, n):
    return comb(D * n, n) // ((D - 1) * n + 1)

def eps6_upper(beta):
    _, _, (k6lo, k6hi) = norms(beta)
    return root_bracket(k6hi, 6)[1]

def main():
    out = []
    D = 20
    mu = Fr(D**D, (D - 1) ** (D - 1))
    out.append(("mu_20=20^20/19^19", dec(mu)))
    for n in range(4, 13):
        fn = F(D, n)
        out.append((f"F_20({n})", str(fn)))
        if (D * n) % 1 == 0:
            pass
    # check F(n+1)/F(n) increasing to mu
    rats = [Fr(F(D, n + 1), F(D, n)) for n in range(1, 60)]
    out.append(("F ratio increasing", str(all(rats[i] < rats[i + 1] for i in range(len(rats) - 1)))))
    out.append(("F ratio < mu all n<=59", str(all(r < mu for r in rats))))
    # sum_{n>=N} F(n) mu^-n  (converges like n^-3/2)
    for N in (4, 11):
        s = sum(Fr(F(D, n)) / mu**n for n in range(N, 400))
        out.append((f"sum_n={N}..399 F(n)/mu^n", dec(s)))
    betas = [Fr(1, 2000), Fr(1, 1000), Fr(1, 500), Fr(1, 100), Fr(1, 64), Fr(1, 50), Fr(1, 45), Fr(1, 40), Fr(1, 35), Fr(1, 30), Fr(1, 20), Fr(1, 18), Fr(1, 10), Fr(1), Fr(4)]
    for b in betas:
        (slo, shi), (l2lo, l2hi), (k6lo, k6hi) = norms(b)
        e6lo = root_bracket(k6lo, 6)[0] if k6lo > 0 else Fr(0)
        e6hi = root_bracket(k6hi, 6)[1]
        l2 = root_bracket(l2hi, 2)[1]
        out.append((f"beta={b}", f"sup in [{dec(slo)},{dec(shi)}] L2<= {dec(l2)} L6 in [{dec(e6lo)},{dec(e6hi)}] L6/beta~{dec(e6hi/b)} mu*L6~{dec(mu*e6hi)} mu*e^(1/4)*L6~{dec(mu*e6hi*Fr(1284026,1000000))}"))
    for line in out:
        print("|".join(line))

if __name__ == "__main__":
    main()
