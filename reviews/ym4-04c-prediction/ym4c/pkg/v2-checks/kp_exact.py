#!/usr/bin/env python3
"""YM4-04C v2 repair lane: exact two-sided KP certificate helpers (Fractions, directed dyadic rounding).

g(alpha) = S(eps * e^{2 alpha + theta}) - alpha with S(x) = sum_{n=4..ncut} c_n x^n [+ 6 F_20(ncut+1) x^(ncut+1)/(1 - mu x)].
c_n = head[n] for n in head (n <= 10), else 6 F_20(n). S has nonnegative coefficients, so g is convex in alpha
and S(eps e^{2 alpha + theta}) increases in alpha and in theta.
MET: a rational alpha with S^+(x^+(alpha)) <= alpha <= 1/4.  NOT_MET certificate (convexity): with g' = 2 x S'(x) - 1,
g(alpha) >= g(alpha_m) + g'(alpha_m)(alpha - alpha_m) for all alpha in [0,1/4], so min g >= g^-(alpha_m) - |g'|^+(alpha_m)/4 > 0;
if g'^-(0) >= 0 then min g = g(0). theta = 1/4 decides for every theta >= 1/4 by monotonicity in theta.
"""
import sys
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from derive_estimates import norms, root_bracket, exp_bounds

BITS = 160
MU = Fr(20**20, 19**19)
def F20(n): return comb(20 * n, n) // (19 * n + 1)

def rnd(x, upward):
    if x == 0: return Fr(0)
    neg = x < 0
    if neg: x = -x; upward = not upward
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = BITS - e
    num, den = (x.numerator << sh, x.denominator) if sh >= 0 else (x.numerator, x.denominator << (-sh))
    q, r = divmod(num, den)
    if upward and r: q += 1
    v = Fr(q, 2**sh) if sh >= 0 else Fr(q * 2**(-sh))
    return -v if neg else v
def up(x): return rnd(x, True)
def dn(x): return rnd(x, False)
def exp_lo(y): return dn(exp_bounds(Fr(y), Fr(1, 2**(BITS + 8)))[0])
def exp_hi(y): return up(exp_bounds(Fr(y), Fr(1, 2**(BITS + 8)))[1])

def eps6_bounds(beta, den=10**12):
    _, _, (k6lo, k6hi) = norms(beta)
    return Fr(root_bracket(k6lo, 6, den)[0]), Fr(root_bracket(k6hi, 6, den)[1])

def coeffs(head, ncut):
    return {n: (Fr(head[n]) if (n in head and n <= 10) else Fr(6 * F20(n))) for n in range(4, ncut + 1)}

def S_and_xdS(x, c, ncut, tail, upward):
    """S(x) and x S'(x) rounded in the given direction; None when the tail pole is reached."""
    r = up if upward else dn
    s = Fr(0); xs = Fr(0); xn = r(x ** 4)
    for n in range(4, ncut + 1):
        t = r(c[n] * xn); s += t; xs += n * t
        xn = r(xn * x)
    if tail:
        q = 1 - MU * x
        if q <= 0: return None, None
        T = r(Fr(6 * F20(ncut + 1)) * xn / q)   # xn = x^(ncut+1) here
        s += T; xs += r(T * (ncut + 1 + MU * x / q))
    return r(s), r(xs)

def x_of(eps, alpha, theta, upward):
    return up(eps * exp_hi(2 * alpha + theta)) if upward else dn(eps * exp_lo(2 * alpha + theta))

def met_at(epsU, alpha, theta, c, ncut, tail):
    s, _ = S_and_xdS(x_of(epsU, alpha, theta, True), c, ncut, tail, True)
    return s is not None and s <= alpha <= Fr(1, 4), s

def gprime_bounds(epsL, epsU, alpha, theta, c, ncut, tail):
    _, lo = S_and_xdS(x_of(epsL, alpha, theta, False), c, ncut, tail, False)
    _, hi = S_and_xdS(x_of(epsU, alpha, theta, True), c, ncut, tail, True)
    return (None if lo is None else 2 * lo - 1), (None if hi is None else 2 * hi - 1)

def not_met_certificate(epsL, epsU, theta, c, ncut, tail, iters=70):
    """returns (True, bound) if min_{[0,1/4]} g > 0 is proved, else (False, info)."""
    s0, _ = S_and_xdS(x_of(epsL, Fr(0), theta, False), c, ncut, tail, False)
    if s0 is None: return True, "pole_at_alpha=0"
    if s0 > Fr(1, 4): return True, ("S^-(x(0))>1/4", s0)
    glo0, _ = gprime_bounds(epsL, epsU, Fr(0), theta, c, ncut, tail)
    if glo0 is not None and glo0 >= 0:
        return (s0 > 0), ("g'(0)>=0,min_g=g(0)>=", s0)
    lo, hi = Fr(0), Fr(1, 4)
    for _ in range(iters):   # bisection on the sign of g' (increasing)
        m = (lo + hi) / 2
        gl, gh = gprime_bounds(epsL, epsU, m, theta, c, ncut, tail)
        if gl is None or gl > 0: hi = m
        elif gh is not None and gh < 0: lo = m
        else: lo = hi = m; break
    am = (lo + hi) / 2
    sL, _ = S_and_xdS(x_of(epsL, am, theta, False), c, ncut, tail, False)
    if sL is None: return True, "pole_before_alpha_m"
    gL, gH = gprime_bounds(epsL, epsU, am, theta, c, ncut, tail)
    gabs = max(abs(gL), abs(gH)) if gH is not None else None
    if gabs is None: return False, "pole_in_derivative"
    bound = (sL - am) - gabs * max(am, Fr(1, 4) - am)
    return bound > 0, ("alpha_m", am, "lower_bound_on_min_g", bound)

def newton_from_zero(epsU, theta, c, ncut, tail, steps=80):
    """monotone Newton from alpha = 0 on the convex g (proposes only); returns the last iterate or None."""
    a = Fr(0)
    for _ in range(steps):
        s, xs = S_and_xdS(x_of(epsU, a, theta, True), c, ncut, tail, True)
        if s is None: return None
        g = s - a; gp = 2 * xs - 1
        if gp >= 0: return None
        an = dn(a - g / gp)
        if an > Fr(1, 4): return None
        if abs(an - a) < Fr(1, 2**60): return an
        a = an
    return a
