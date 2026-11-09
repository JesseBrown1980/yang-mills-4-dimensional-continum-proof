# polylib.py -- L5-numbers lane: c_0, eps_6, the closed form S and its derivative, and the
# certified least root alpha_-(theta). Own code, integer only, outward rounding.
import ilib as L
from ilib import rat, add, sub, mul, div, muli, divi, exp_iv, exp_point, root6_iv, cdiv


def comb(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def F(n):
    v = comb(20 * n, n)
    assert v % (19 * n + 1) == 0
    return v // (19 * n + 1)


MU_N, MU_D = 20 ** 20, 19 ** 19
F49x6 = 6 * F(49)
HEADS = {
    'crude': [6 * F(n) for n in range(4, 11)],
    'C03': [1, 0, 12, 0, 32, 32, 304],
    'headfree': [0, 0, 0, 0, 0, 0, 0],
}


def coef_list(head):
    c = [0] * 49
    for n in range(4, 11):
        c[n] = head[n - 4]
    for n in range(11, 49):
        c[n] = 6 * F(n)
    return c


def c0(p, q):
    """c_0(p/q) = sum_m (p/(2q))^{2m}/(m!(m+1)!), p >= 0, enclosure"""
    G = 64
    W = L.P + G
    one = 1 << W
    a2 = p * p
    b2 = 4 * q * q
    s = one
    t = one
    m = 1
    while True:
        t = (t * a2) // (b2 * m * (m + 1))
        if t == 0:
            break
        s += t
        m += 1
    lo = s >> G
    s = one
    t = one
    m = 1
    while True:
        t = cdiv(t * a2, b2 * m * (m + 1))
        s += t
        if t <= 1 and 2 * a2 <= b2 * (m + 1) * (m + 2):
            break
        m += 1
    s += 1
    return (lo, cdiv(s, 1 << G))


def eps6_pow6(p, q):
    C = c0(p, q)
    tot = (0, 0)
    Ck = (L.ONE, L.ONE)
    for k in range(0, 7):
        rk = (L.ONE, L.ONE) if k == 0 else div(c0(k * p, q), Ck)
        tot = add(tot, muli(rk, comb(6, k) * (1 if (6 - k) % 2 == 0 else -1)))
        Ck = mul(Ck, C)
    return tot


def eps6(p, q):
    return root6_iv(eps6_pow6(p, q))


class SV:
    pass


def S_eval(x, coef, deriv=False, tail=True):
    """S(x) for an interval x >= 0 with coefficients coef[4..48] and the closed tail.
    Returns lo/hi of S; pole_hi (mu x^+ < 1); for the derivative dlo/dhi."""
    xl, xh = x
    P = L.P
    ONE = L.ONE
    r = SV()
    pl = ONE
    ph = ONE
    Slo = 0
    Shi = 0
    dlo = 0
    dhi = 0
    for n in range(1, 50):
        ql, qh = pl, ph
        pl = (pl * xl) >> P
        ph = cdiv(ph * xh, ONE)
        if 4 <= n <= 48 and coef[n]:
            c = coef[n]
            Slo += c * pl
            Shi += c * ph
            if deriv:
                dlo += n * c * ql
                dhi += n * c * qh
    r.pole_ok = True
    r.lo_finite = True
    if tail:
        mux_l = (xl * MU_N) // MU_D
        mux_h = cdiv(xh * MU_N, MU_D)
        den_h = ONE - mux_l
        den_l = ONE - mux_h
        r.pole_ok = den_l > 0
        r.lo_finite = den_h > 0
        if r.lo_finite:
            Slo += (F49x6 * pl << P) // den_h
            if deriv:
                dlo += (F49x6 * 49 * ql << P) // den_h
                dlo += ((F49x6 * pl * MU_N << (2 * P)) // MU_D) // (den_h * den_h)
        if r.pole_ok:
            Shi += cdiv(F49x6 * ph << P, den_l)
            if deriv:
                dhi += cdiv(F49x6 * 49 * qh << P, den_l)
                dhi += cdiv(cdiv(F49x6 * ph * MU_N << (2 * P), MU_D), den_l * den_l)
    r.lo = Slo
    r.hi = Shi
    r.dlo = dlo
    r.dhi = dhi
    return r


def theta_point(i):
    """theta = 1/4 + i/64, exact at scale 2^P"""
    return (16 + i) << (L.P - 6)


def A_of(eps, i):
    th = theta_point(i)
    return mul(eps, exp_point(th))


def x_at(A, a):
    """x = A e^{2 alpha} at an exact dyadic alpha (integer at scale 2^P)"""
    return mul(A, exp_point(2 * a))


def x_at_iv(A, a_iv):
    return mul(A, exp_iv(muli(a_iv, 2)))


def newton_root(A, coef, tail=True):
    a = 0
    for _ in range(3000):
        x = x_at(A, a)
        r = S_eval(x, coef, deriv=True, tail=tail)
        if not r.lo_finite:
            return None
        g = r.lo - a
        gp = ((2 * x[0] * r.dlo) >> L.P) - L.ONE
        if gp >= 0:
            if g > 0:
                return None
            return a
        step = (g << L.P) // (-gp)
        a += step
        if abs(step) <= (1 << 30):
            return a
    return a


def certify_upper(A, coef, a, tail=True):
    x = x_at(A, a)
    r = S_eval(x, coef, tail=tail)
    return r.pole_ok and r.hi <= a


def certify_lower(A, coef, a, tail=True):
    """alpha_- > a: g(a) > 0 and g'(a) < 0 (then g > 0 on [0, a] by convexity)"""
    if a < 0:
        return True
    x = x_at(A, a)
    r = S_eval(x, coef, deriv=True, tail=tail)
    if not r.pole_ok:
        return False
    gp_hi = cdiv(2 * x[1] * r.dhi, L.ONE) - L.ONE
    return r.lo > a and gp_hi < 0


def least_root(A, coef, tail=True):
    """returns (alpha_lo, alpha_hi) with alpha_lo < alpha_- <= alpha_hi, or None"""
    a = newton_root(A, coef, tail=tail)
    if a is None:
        return None
    for sh in (L.P - 400, L.P - 300, L.P - 220, L.P - 160, L.P - 120, L.P - 90, L.P - 70, L.P - 56, L.P - 48):
        if sh < 0:
            continue
        m = 1 << sh
        if certify_upper(A, coef, a + m, tail) and certify_lower(A, coef, a - m, tail):
            return (a - m, a + m)
    return None


def met_read(A, coef, alpha_iv, tail=True, pole=True):
    """C_0 MET read at a rational alpha (an enclosure): S^+(x^+(alpha)) <= alpha, pole test first"""
    x = x_at_iv(A, alpha_iv)
    r = S_eval(x, coef, tail=tail)
    if pole and tail and not r.pole_ok:
        return False, r, x
    if pole and not tail:
        mux_h = cdiv(x[1] * MU_N, MU_D)
        if mux_h >= L.ONE:
            return False, r, x
    return r.hi <= alpha_iv[0], r, x


def notmet_read(A, coef, alpha_iv, tail=True):
    """least root above alpha: g^-(alpha) > 0 and g'^+(alpha) < 0"""
    x = x_at_iv(A, alpha_iv)
    r = S_eval(x, coef, deriv=True, tail=tail)
    if not r.pole_ok:
        return False, r, x
    gp_hi = cdiv(2 * x[1] * r.dhi, L.ONE) - L.ONE
    return (r.lo > alpha_iv[1] and gp_hi < 0), r, x
