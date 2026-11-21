"""Rational interval helpers for derivation checks (integers and Fractions only)."""
from fractions import Fraction as Fr

PREC = 160  # dyadic rounding precision (bits)


def rd(x, up):
    """Round Fraction x outward to a dyadic with PREC bits."""
    s = 1 << PREC
    n = x.numerator * s
    d = x.denominator
    q, r = divmod(n, d)
    if up and r:
        q += 1
    return Fr(q, s)


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        lo = Fr(lo)
        hi = lo if hi is None else Fr(hi)
        assert lo <= hi, (lo, hi)
        self.lo, self.hi = rd(lo, False), rd(hi, True)

    def __add__(self, o):
        o = o if isinstance(o, I) else I(o)
        return I(self.lo + o.lo, self.hi + o.hi)
    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        o = o if isinstance(o, I) else I(o)
        return self + (-o)

    def __rsub__(self, o):
        return I(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, I) else I(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return I(min(p), max(p))
    __rmul__ = __mul__

    def inv(self):
        assert self.lo > 0 or self.hi < 0
        return I(1 / self.hi, 1 / self.lo)

    def __truediv__(self, o):
        o = o if isinstance(o, I) else I(o)
        return self * o.inv()

    def __rtruediv__(self, o):
        return I(o) * self.inv()

    def mid(self):
        return (self.lo + self.hi) / 2

    def __repr__(self):
        return "[%s, %s]" % (dec(self.lo), dec(self.hi))


def dec(x, n=12):
    x = Fr(x)
    sign = "-" if x < 0 else ""
    x = abs(x)
    ip = x.numerator // x.denominator
    fp = x - ip
    digs = []
    for _ in range(n):
        fp *= 10
        d = fp.numerator // fp.denominator
        digs.append(str(d))
        fp -= d
    return sign + str(ip) + "." + "".join(digs)


def sqrt_i(x):
    x = x if isinstance(x, I) else I(x)
    def s(v, up):
        v = Fr(v)
        assert v >= 0
        sc = 1 << (2 * PREC)
        n = v.numerator * sc // v.denominator
        r = isqrt(n)
        if up:
            r += 2
        return Fr(r, 1 << PREC)
    return I(s(x.lo, False), s(x.hi, True))


def isqrt(n):
    import math
    return math.isqrt(n)


def atanh_series(y, terms=None):
    """atanh(y) for rational 0<=y<1/2, interval."""
    y = Fr(y)
    s = Fr(0)
    p = y
    n = 0
    y2 = y * y
    while True:
        t = p / (2 * n + 1)
        s += t
        p *= y2
        n += 1
        if p < Fr(1, 1 << (PREC + 8)):
            break
    tail = p / ((2 * n + 1) * (1 - y2))
    return I(s, s + tail)


def log_r(x):
    """log of positive rational x as interval."""
    x = Fr(x)
    assert x > 0
    k = 0
    while x > 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1
    # now 1<=x<=2 ; log x = 2 atanh((x-1)/(x+1)), y<=1/3
    lx = 2 * atanh_series((x - 1) / (x + 1))
    l2 = 2 * atanh_series(Fr(1, 3))
    return lx + k * l2


def log_i(x):
    return I(log_r(x.lo).lo, log_r(x.hi).hi)


def exp_r(x):
    """exp of rational x as interval."""
    x = Fr(x)
    k = 0
    while abs(x) > Fr(1, 8):
        x /= 2
        k += 1
    s = Fr(0)
    t = Fr(1)
    n = 0
    while True:
        s += t
        n += 1
        t = t * x / n
        if abs(t) < Fr(1, 1 << (PREC + 8)):
            break
    tail = abs(t) * 2
    r = I(s - tail, s + tail)
    for _ in range(k):
        r = r * r
    return r


def exp_i(x):
    return I(exp_r(x.lo).lo, exp_r(x.hi).hi)


def pi_i():
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239)
    def atan_series(y):
        y = Fr(y)
        s = Fr(0)
        p = y
        n = 0
        y2 = y * y
        while True:
            t = p / (2 * n + 1)
            s += t if n % 2 == 0 else -t
            p *= y2
            n += 1
            if p < Fr(1, 1 << (PREC + 8)):
                break
        e = p / (2 * n + 1)
        return I(s - e, s + e)
    return 16 * atan_series(Fr(1, 5)) - 4 * atan_series(Fr(1, 239))


def arcsin_small(z):
    """arcsin(z) for 0<=z<=1/2 interval of rational/ interval z (monotone)."""
    def a(zz):
        zz = Fr(zz)
        s = Fr(0)
        c = Fr(1)  # (2n)!/(4^n n!^2)
        p = zz
        z2 = zz * zz
        n = 0
        while True:
            s += c * p / (2 * n + 1)
            n += 1
            c = c * (2 * n - 1) / (2 * n)
            p *= z2
            if p < Fr(1, 1 << (PREC + 8)):
                break
        tail = p / (1 - z2)
        return I(s, s + tail)
    z = z if isinstance(z, I) else I(z)
    return I(a(z.lo).lo, a(z.hi).hi)
