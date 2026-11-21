#!/usr/bin/env python3
"""Final-critic spot checks for YM4-04C. Fractions only, outward rounding; floats only in display.
Independent of the package's scripts: own exp/ln/pi, own eps_6, own KP root bracket."""
import sys
from fractions import Fraction as Fr
from math import comb, factorial

P = 220  # relative bits kept after each rounding


def rnd(x, up):
    if x == 0:
        return Fr(0)
    if x < 0:
        return -rnd(-x, not up)
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = P - e
    if sh >= 0:
        q, r = divmod(x.numerator << sh, x.denominator)
        if up and r:
            q += 1
        return Fr(q, 1 << sh)
    q, r = divmod(x.numerator, x.denominator << (-sh))
    if up and r:
        q += 1
    return Fr(q << (-sh))


U = lambda x: rnd(x, True)
D = lambda x: rnd(x, False)


def exp_iv(y):
    """[lo, hi] with lo <= e^y <= hi for rational y (any sign), by halving and Taylor with a geometric tail."""
    y = Fr(y)
    neg = y < 0
    a = -y if neg else y
    h = 0
    while a > Fr(1, 8):
        a /= 2
        h += 1
    s = Fr(0)
    t = Fr(1)
    K = 40
    for k in range(K + 1):
        s += t
        t = t * a / (k + 1)
    lo = D(s)
    hi = U(s + t * 2)  # t = a^{K+1}/(K+1)!, tail <= t/(1-a) <= 2t
    for _ in range(h):
        lo = D(lo * lo)
        hi = U(hi * hi)
    if neg:
        lo, hi = D(1 / hi), U(1 / lo)
    return lo, hi


def ln1p_iv(x):
    """ln(1+x) for 0 <= x < 1/2 by the alternating series."""
    x = Fr(x)
    s = Fr(0)
    t = x
    k = 1
    terms = []
    while True:
        term = t / k
        terms.append(term)
        if term < Fr(1, 2 ** (P + 20)):
            break
        t *= x
        k += 1
    for i, term in enumerate(terms[:-1]):
        s += term if i % 2 == 0 else -term
    # partial sum through len-1 terms; the next term bounds the error, with the sign of its index
    last = terms[-1]
    n = len(terms) - 1  # index of last (0-based) not included
    if n % 2 == 0:
        return D(s), U(s + last)
    return D(s - last), U(s)


def arctan_inv_iv(m, K=60):
    s = Fr(0)
    for k in range(K):
        s += Fr((-1) ** k, (2 * k + 1) * m ** (2 * k + 1))
    nxt = Fr(1, (2 * K + 1) * m ** (2 * K + 1))
    return (s - nxt, s + nxt) if True else None


def pi_iv():
    a5 = arctan_inv_iv(5)
    a239 = arctan_inv_iv(239)
    return D(16 * a5[0] - 4 * a239[1]), U(16 * a5[1] - 4 * a239[0])


PI = pi_iv()
MU = Fr(20 ** 20, 19 ** 19)


def F20(n):
    return comb(20 * n, n) // (19 * n + 1)


def c0_iv(x, M=None):
    """c_0(x) = sum_m (x/2)^{2m}/(m!(m+1)!), exact partial sum and a geometric tail bound."""
    x = Fr(x)
    q = (x / 2) ** 2
    s = Fr(0)
    t = Fr(1)
    m = 0
    while True:
        s += t
        t = t * q / ((m + 1) * (m + 2))
        m += 1
        if m > 5 and t < Fr(1, 2 ** (P + 40)) * s and q / ((m + 1) * (m + 2)) < Fr(1, 2):
            break
    return s, s + 2 * t


def eps6_iv(beta):
    beta = Fr(beta)
    c1 = c0_iv(beta)
    lo = Fr(0)
    hi = Fr(0)
    for k in range(7):
        ck = c0_iv(k * beta) if k else (Fr(1), Fr(1))
        coef = comb(6, k) * (-1) ** (6 - k)
        # term = coef * ck / c1^k
        tl = ck[0] / c1[1] ** k
        th = ck[1] / c1[0] ** k
        if coef > 0:
            lo += coef * tl
            hi += coef * th
        else:
            lo += coef * th
            hi += coef * tl
    assert lo > 0, (beta, lo)
    # sixth root by bisection on each end
    def root6(v, up):
        a, b = Fr(0), Fr(1)
        while b ** 6 < v:
            b *= 2
        for _ in range(P + 10):
            m = (a + b) / 2
            if m ** 6 <= v:
                a = m
            else:
                b = m
            a, b = D(a), U(b)
        return b if up else a
    return root6(lo, False), root6(hi, True)


C03 = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}
HEADS = {"crude": {n: 6 * F20(n) for n in range(4, 11)}, "C03": C03, "headfree": {n: 0 for n in range(4, 11)}}


def coef(head):
    return [Fr(0)] * 4 + [Fr(head[n]) if n <= 10 else Fr(6 * F20(n)) for n in range(4, 49)]


def S_dS(x, c, up, mu=MU):
    """S(x) and x S'(x), rounded in direction up; None at or past the pole."""
    r = U if up else D
    q = 1 - mu * x
    if q <= 0:
        return None, None
    s = Fr(0)
    xs = Fr(0)
    xn = r(x ** 4)
    for n in range(4, 49):
        t = r(c[n] * xn)
        s += t
        xs += n * t
        xn = r(xn * x)
    T = r(6 * F20(49) * xn / q)
    s += T
    xs += r(T * (49 + mu * x / q))
    return r(s), r(xs)


def x_iv(eps, alpha, theta):
    e = exp_iv(2 * Fr(alpha) + Fr(theta))
    return D(eps[0] * e[0]), U(eps[1] * e[1])


def met(eps, alpha, theta, c):
    xl, xh = x_iv(eps, alpha, theta)
    s, _ = S_dS(xh, c, True)
    return s is not None and s <= alpha


def g_lo_gp_hi(eps, alpha, theta, c):
    xl, xh = x_iv(eps, alpha, theta)
    sl, _ = S_dS(xl, c, False)
    _, xsh = S_dS(xh, c, True)
    if sl is None or xsh is None:
        return None, None
    return sl - alpha, 2 * xsh - 1


def root_bracket(eps, theta, c, iters=60):
    """[a_lo, a_hi] containing the least root of g; a_lo certified by g^-(a_lo)>0, g'^+(a_lo)<0; a_hi by MET."""
    lo, hi = Fr(0), None
    for k in range(1, 1025):
        if met(eps, Fr(k, 2 ** 13), theta, c):
            hi = Fr(k, 2 ** 13)
            break
    if hi is None:
        return None
    for _ in range(iters):
        m = (lo + hi) / 2
        if met(eps, m, theta, c):
            hi = m
        else:
            lo = m
    gl, gph = g_lo_gp_hi(eps, lo, theta, c)
    assert gl is not None and gl > 0 and gph < 0, ("lower end not certified", float(lo))
    return lo, hi


def not_met_c0(eps, theta, c):
    """Proof that S(eps e^{2a+theta}) > a on [0,1/4]: pole at 0, or convex tangent bound."""
    xl, _ = x_iv(eps, 0, theta)
    if 1 - MU * xl <= 0:
        return True, "pole"
    # bisection on sign of g'
    lo, hi = Fr(0), Fr(1, 4)
    for _ in range(60):
        m = (lo + hi) / 2
        xl, xh = x_iv(eps, m, theta)
        _, xsl = S_dS(xl, c, False)
        if xsl is None or 2 * xsl - 1 > 0:
            hi = m
        else:
            lo = m
    am = lo
    xl, xh = x_iv(eps, am, theta)
    sl, _ = S_dS(xl, c, False)
    _, xsh = S_dS(xh, c, True)
    _, xsl = S_dS(xl, c, False)
    if sl is None or xsh is None:
        return False, "pole_near_alpha_m"
    gabs = max(abs(2 * xsh - 1), abs(2 * xsl - 1))
    bound = (sl - am) - gabs * max(am, Fr(1, 4) - am)
    return bound > 0, float(bound)


def lam_iv(d):
    e = exp_iv(d)
    dpl, dph = D(d * e[0]), U(d * e[1])
    return D(dpl + ln1p_iv(dpl)[0]), U(dph + ln1p_iv(dph)[1])


def cfin_iv(d, kappa=Fr(1, 4)):
    ll, lh = lam_iv(d)
    e1 = exp_iv(-4 * kappa)
    e2l, e2h = exp_iv(d + ll - 5 * kappa)[0], exp_iv(d + lh - 5 * kappa)[1]
    pre_l, pre_h = exp_iv(d - kappa / 2)
    best_l, best_h, arg = Fr(0), Fr(0), None
    f = 4
    while True:
        gl = exp_iv(-(kappa - ll) * f)[0] - exp_iv(-kappa * f)[1]
        gh = exp_iv(-(kappa - lh) * f)[1] - exp_iv(-kappa * f)[0]
        if gl > best_l:
            best_l, arg = gl, f
        best_h = max(best_h, gh)
        if exp_iv(-(kappa - lh) * f)[1] <= best_l:
            break
        f += 1
    t3l, t3h = D(pre_l * best_l), U(pre_h * best_h)
    lo = max(e1[0], e2l, t3l)
    hi = max(e1[1], e2h, t3h)
    return lo, hi, arg, (e1, (e2l, e2h), (t3l, t3h))


def show(name, val, lo, hi):
    v = val if isinstance(val, tuple) else (val, val)
    ok = Fr(lo) <= v[0] and v[1] <= Fr(hi)
    print(f"{'OK ' if ok else 'BAD'} {name}: [{float(v[0]):.12g}, {float(v[1]):.12g}] in frozen [{lo}, {hi}]")
    return ok


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    if part in ("const", "all"):
        show("pi", PI, Fr(314159265358979, 10 ** 14), Fr(314159265358980, 10 ** 14))
        show("8/(3pi)", (D(8 / (3 * PI[1])), U(8 / (3 * PI[0]))), Fr(8488263, 10 ** 7), Fr(8488264, 10 ** 7))
        show("mu", MU, Fr(5300068, 10 ** 5), Fr(5300069, 10 ** 5))
        l2 = ln1p_iv(Fr(1))  if False else None
        # ln 2 = 2 atanh(1/3)
        s = sum(Fr(2, (2 * k + 1) * 3 ** (2 * k + 1)) for k in range(80))
        ln2 = (s, s + Fr(1, 3 ** 150))
        db = (D(11 * ln2[0] / (3 * PI[1] ** 2)), U(11 * ln2[1] / (3 * PI[0] ** 2)))
        show("Delta_beta", db, Fr(2575118068, 10 ** 10), Fr(2575118069, 10 ** 10))
        e15 = exp_iv(Fr(-3, 2))
        show("e^{-3/2}/4", (e15[0] / 4, e15[1] / 4), Fr(5578254, 10 ** 8), Fr(5578255, 10 ** 8))
        show("e^{-1}", exp_iv(-1), Fr(3678794, 10 ** 7), Fr(3678795, 10 ** 7))
        print("F_20(4..12)", [F20(n) for n in range(4, 13)])
        # W06 cubic
        p = lambda y: y ** 3 - 18 * y ** 2 + 80 * y - 48
        a, b = Fr(7084973778, 10 ** 10), Fr(7084973779, 10 ** 10)
        print("W06 cubic sign change on frozen bracket:", p(a) < 0 < p(b), "; no root below:", p(Fr(0)) < 0 and all(p(Fr(k, 100)) < 0 for k in range(0, 70)))
    if part in ("eps", "all"):
        frozen = [(Fr(1, 1000), "6.53830e-4", "6.53831e-4"), (Fr(1, 100), "6.538419e-3", "6.538420e-3"),
                  (Fr(1, 64), "1.0216544e-2", "1.0216545e-2"), (Fr(1, 50), "1.3077541e-2", "1.3077542e-2"),
                  (Fr(1, 45), "1.4530846e-2", "1.4530847e-2"), (Fr(1, 40), "1.6347585e-2", "1.6347586e-2"),
                  (Fr(1, 10), "6.5499695e-2", "6.5499696e-2"), (Fr(1), "0.740642074", "0.740642075"),
                  (Fr(4), "4.29699629", "4.29699630")]
        e14 = exp_iv(Fr(1, 4))
        for b, lo, hi in frozen:
            e = eps6_iv(b)
            show(f"C02 eps_6({b})", e, Fr(lo), Fr(hi))
        walls = [(Fr(1, 45), "0.9888", "0.9889"), (Fr(1, 40), "1.1125", "1.1126"), (Fr(1, 18), "2.473", "2.474"),
                 (Fr(1, 10), "4.4575", "4.4576"), (Fr(1), "50.40", "50.41"), (Fr(4), "292.4", "292.5")]
        for b, lo, hi in walls:
            e = eps6_iv(b)
            show(f"C15 wall mu e^1/4 eps_6({b})", (D(MU * e14[0] * e[0]), U(MU * e14[1] * e[1])), Fr(lo), Fr(hi))
        for b, side in ((Fr(2247, 10 ** 5), "<1"), (Fr(2248, 10 ** 5), ">1")):
            e = eps6_iv(b)
            w = (D(MU * e14[0] * e[0]), U(MU * e14[1] * e[1]))
            print(f"C04 wall at {float(b)}: [{float(w[0]):.10f}, {float(w[1]):.10f}] expected {side}")
        for b, side in ((Fr(2885, 10 ** 5), "<1"), (Fr(2886, 10 ** 5), ">1")):
            e = eps6_iv(b)
            print(f"C04 kappa->0 crossing at {float(b)}: mu*eps in [{float(MU*e[0]):.10f}, {float(MU*e[1]):.10f}] expected {side}")
