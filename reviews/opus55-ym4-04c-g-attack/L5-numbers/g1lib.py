# g1lib.py -- L5-numbers lane: lambda(delta) and c_fin(delta) at kappa = 1/4, own code, integer only.
# c_fin's sup over integer f >= 4 is an exact maximum with a certified tail cut:
# the scan stops at the first f with e^{-(kappa-lambda^+) f} at or below the best lower value so far,
# since every later g(f') is below e^{-(kappa-lambda) f'} <= e^{-(kappa-lambda^+) f}.
import ilib as L
from ilib import rat, add, sub, mul, muli, neg, exp_iv, exp_point, ln1p_iv, imax

K4 = None
EM1 = None


def _init():
    global K4, EM1
    K4 = rat(1, 4)
    EM1 = exp_point(-L.ONE)


def lam_iv(d):
    if K4 is None:
        _init()
    dp = mul(d, exp_iv(d))
    return dp, add(dp, ln1p_iv(dp))


def cfin(d, fallback=False):
    if K4 is None:
        _init()
    dp, lm = lam_iv(d)
    if fallback:
        lm = muli(dp, 2)
    E2 = exp_iv(sub(add(d, lm), rat(5, 4)))
    a = sub(K4, lm)
    assert a[0] > 0, 'lambda not below kappa'
    best_lo = -1
    best_hi = -1
    farg = None
    gs = {}
    f = 4
    while True:
        eu = exp_iv(muli(neg(a), f))
        ev = exp_point(-(f << (L.P - 2)))
        g = sub(eu, ev)
        gs[f] = g
        if g[0] > best_lo:
            best_lo = g[0]
            farg = f
        if g[1] > best_hi:
            best_hi = g[1]
        if eu[1] <= best_lo:
            break
        f += 1
    unique = all(gs[h][1] < gs[farg][0] for h in gs if h != farg)
    E3 = mul(exp_iv(sub(d, rat(1, 8))), (best_lo, best_hi))
    c = imax(imax(EM1, E2), E3)
    return c, E2, E3, farg, unique, f


def is_e1(E2, E3):
    if K4 is None:
        _init()
    return E2[1] <= EM1[0] and E3[1] <= EM1[0]
