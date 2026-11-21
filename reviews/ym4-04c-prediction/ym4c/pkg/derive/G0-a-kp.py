#!/usr/bin/env python3
"""Scratch arithmetic for G0-a.md (not an engine, not evidence): exact upward-rounded rationals.

For a coupling beta and a head model: eps6^+ (upper enclosure), a certified KP parameter alpha at
theta = kappa (S^+(eps^+ e^{2 alpha + kappa}) <= alpha checked exactly), the frozen output 12*alpha,
the proved output 6*S^+(eps^+ e^{2 alpha + kappa}) <= 6*alpha, and the C_1 test 2 d e^d <= 1/8.
Floats appear only in display.
"""
from fractions import Fraction as Fr
from math import comb, isqrt
import sys

BITS = 160
KAPPA = Fr(1, 4)
MU = Fr(20**20, 19**19)


def F(n):
    return comb(20 * n, n) // (19 * n + 1)


FN = {n: F(n) for n in range(1, 60)}


def up(x):
    if x <= 0:
        return x
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = BITS - e
    if sh >= 0:
        return Fr(-((-x.numerator * 2**sh) // x.denominator), 2**sh)
    return Fr(-((-x.numerator) // (x.denominator * 2 ** (-sh))) * 2 ** (-sh))


def down(x):
    if x <= 0:
        return x
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = BITS - e
    if sh >= 0:
        return Fr((x.numerator * 2**sh) // x.denominator, 2**sh)
    return Fr((x.numerator // (x.denominator * 2 ** (-sh))) * 2 ** (-sh))


def exp_pos(y):
    """[lo, hi] for e^y, y >= 0 rational."""
    s = Fr(0); t = Fr(1); j = 0
    while True:
        s += t
        t = t * y / (j + 1)
        j += 1
        r = y / (j + 1)
        if j > 3 and r < Fr(1, 2) and t < Fr(1, 2**(BITS + 20)):
            return s, s + t / (1 - r)


def exp_up(y):
    if y >= 0:
        return up(exp_pos(y)[1])
    return up(1 / exp_pos(-y)[0])


def exp_down(y):
    if y >= 0:
        return down(exp_pos(y)[0])
    return down(1 / exp_pos(-y)[1])


def c0_int(x):
    """[lo, hi] for c_0(x) = sum_m (x/2)^{2m}/(m!(m+1)!), x >= 0."""
    q = (x / 2) ** 2
    s = Fr(0); t = Fr(1); m = 0
    while True:
        s += t
        t = t * q / ((m + 1) * (m + 2))
        m += 1
        r = q / ((m + 1) * (m + 2))
        if m > 6 and r < Fr(1, 2) and t < Fr(1, 2**400):
            return s, s + t / (1 - r)


def eps6_int(beta):
    lo1, hi1 = c0_int(beta)
    lo = Fr(0); hi = Fr(0)
    for k in range(7):
        lk, hk = (Fr(1), Fr(1)) if k == 0 else c0_int(k * beta)
        coef = comb(6, k) * (-1) ** (6 - k)
        tl, th = lk / hi1**k, hk / lo1**k
        if coef > 0:
            lo += coef * tl; hi += coef * th
        else:
            lo += coef * th; hi += coef * tl
    sc = 2**(6 * 128)
    rh = isqrt_n(-((-hi.numerator * sc) // hi.denominator), 6, up_=True)
    rl = isqrt_n((lo.numerator * sc) // lo.denominator, 6, up_=False)
    return Fr(rl, 2**128), Fr(rh, 2**128)


def isqrt_n(v, n, up_):
    lo, hi = 0, 1
    while hi**n < v:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**n <= v:
            lo = mid
        else:
            hi = mid
    if lo**n == v:
        return lo
    return hi if up_ else lo


def S_up(x, head):
    if MU * x >= 1:
        return None
    s = Fr(0); xn = up(x**4)
    for n in range(4, 49):
        c = head[n] if n in head else 6 * FN[n]
        s += c * xn
        xn = up(xn * x)
    s += 6 * FN[49] * xn / down(1 - MU * x)  # xn = x^49 rounded up
    return up(s)


def S_approx(x, head):
    s = Fr(0); ds = Fr(0)
    for n in range(4, 49):
        c = head[n] if n in head else 6 * FN[n]
        s += c * x**n; ds += n * c * x**n
    q = 1 - MU * x
    T = 6 * FN[49] * x**49 / q
    return s + T, ds + T * (49 + MU * x / q)


def rnd(x, bits=96):
    return Fr(round(x * 2**bits), 2**bits)


def certify(beta, head, theta=KAPPA):
    """Return (eps_hi, alpha) with S^+(eps^+ e^{2 alpha+theta}) <= alpha exactly, or None."""
    _, eps = eps6_int(beta)
    eps = up(eps)
    a = Fr(0)
    for _ in range(80):
        x = rnd(eps * exp_up(2 * a + theta))
        if MU * x >= 1:
            return eps, None
        s, xs = S_approx(x, head)
        g = s - a; gp = 2 * xs - 1
        if gp >= 0:
            return eps, None
        an = rnd(a - g / gp)
        if abs(an - a) < Fr(1, 2**80) * max(an, Fr(1, 2**40)):
            a = an
            break
        a = an
    for bump in (Fr(1, 10**12), Fr(1, 10**9), Fr(1, 10**6)):
        cand = up(a * (1 + bump))
        s = S_up(up(eps * exp_up(2 * cand + theta)), head)
        if s is not None and s <= cand:
            return eps, cand
    return eps, None


CRUDE = {}
FREE = {n: 0 for n in range(4, 11)}
REFINED = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}
HEADS = {"crude": CRUDE, "head-free": FREE, "refined(C03)": REFINED}


def report(beta, name):
    eps, a = certify(beta, HEADS[name])
    if a is None:
        print(f"beta={beta} {name}: no certified alpha at theta=kappa (search read, not a proof of NOT_MET)")
        return None
    s_k = S_up(up(eps * exp_up(2 * a + KAPPA)), HEADS[name])
    d_frozen = 12 * a
    d_proved = 6 * s_k
    dp = up(d_proved * exp_up(d_proved))
    c1 = 2 * dp <= Fr(1, 8)
    print(f"beta={beta} {name}: eps6^+={float(eps):.10e} alpha={float(a):.10e} "
          f"frozen 12*alpha={float(d_frozen):.8e} proved 6*S={float(d_proved):.8e} (<= 6*alpha={float(6*a):.8e}) "
          f"ratio proved/frozen={float(d_proved/d_frozen):.8f} 2d'e^d(proved)={float(2*dp):.6f} C_1(proved) MET: {c1}")
    return d_proved


def proved_edge(name, dcrit, lo, hi, den=100000):
    """Largest beta = j/den on the grid with a certified alpha and 6*S < dcrit (bisection locates only)."""
    def ok(j):
        eps, a = certify(Fr(j, den), HEADS[name])
        if a is None:
            return False
        return 6 * S_up(up(eps * exp_up(2 * a + KAPPA)), HEADS[name]) < dcrit
    assert ok(lo), ("lo not MET", lo)
    assert not ok(hi), ("hi MET", hi)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if ok(m):
            lo = m
        else:
            hi = m
    print(f"{name}: proved-constant self-map edge: certified at {lo}/{den}, not certified by the search at {hi}/{den}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "pts"
    if what == "pts":
        for beta in (Fr(1, 100), Fr(1, 64), Fr(1, 50)):
            for name in HEADS:
                report(beta, name)
    elif what == "edge":
        DCRIT_LO = Fr(496174, 10**7)  # frozen G1 bracket lower end (C13), used as given
        proved_edge("crude", DCRIT_LO, 1370, 1563)
        proved_edge("refined(C03)", DCRIT_LO, 2000, 2076)
        proved_edge("head-free", DCRIT_LO, 2000, 2077)


def readout(beta, head=REFINED, imax=320):
    """min over the grid theta_i = 1/4 + i/64 of the frozen T and of the proved T (both rounded up)."""
    best_f = best_p = None
    for i in range(imax + 1):
        th = KAPPA + Fr(i, 64)
        eps, a = certify(beta, head, th)
        if a is None:
            continue
        e8 = exp_up(-8 * th)
        Tf = Fr(8489, 10000) * 12 * a * e8
        Tp = Fr(8489, 10000) * 6 * S_up(up(eps * exp_up(2 * a + th)), head) * e8
        if best_f is None or Tf < best_f[0]:
            best_f = (Tf, i)
        if best_p is None or Tp < best_p[0]:
            best_p = (Tp, i)
    P10 = beta**4 / 128 - beta**6 / 768 + beta**8 / 1536 - Fr(467, 2211840) * beta**10
    print(f"beta={beta}: frozen T/P_10={float(best_f[0]/P10):.6e} (i={best_f[1]})  "
          f"proved T/P_10={float(best_p[0]/P10):.6e} (i={best_p[1]})")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "readout":
    for b in (Fr(1, 4000), Fr(1, 2000), Fr(1, 1000), Fr(1, 700), Fr(1, 600), Fr(1, 550), Fr(1, 500), Fr(1, 100)):
        readout(b)
