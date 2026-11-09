# ilib.py -- L5-numbers lane, second seat (local Opus 5.5 seat, pid 8467a937cba309f7).
# Integer-only outward-rounded interval arithmetic. Written fresh for G_attack on YM4-04C;
# it imports nothing from the package (derive_checks.py is not imported).
# Every real number is an interval (lo, hi) of Python integers, read as [lo/2^P, hi/2^P].
# Rules kept: no float literal, no true division operator, no fractions or decimal module.
# Floor is '//' or '>>'; ceiling is cdiv. Every operation rounds outward.

P = 640
ONE = 1 << P


def setP(p):
    global P, ONE
    P = p
    ONE = 1 << p


def cdiv(a, b):
    """ceil(a/b) for b > 0"""
    return -((-a) // b)


def rat(p, q):
    """interval enclosing the rational p/q, q > 0"""
    return ((p << P) // q, cdiv(p << P, q))


def const(n):
    return (n << P, n << P)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    ps = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(ps) >> P, -((-max(ps)) >> P))


def div(a, b):
    assert b[0] > 0, "division by an interval that is not positive"
    los = []
    his = []
    for x in a:
        for y in b:
            los.append((x << P) // y)
            his.append(cdiv(x << P, y))
    return (min(los), max(his))


def muli(a, k):
    if k >= 0:
        return (a[0] * k, a[1] * k)
    return (a[1] * k, a[0] * k)


def divi(a, k):
    assert k > 0
    return (a[0] // k, cdiv(a[1], k))


def mulrat(a, p, q):
    """a * (p/q) with p >= 0, q > 0, exact rational factor"""
    assert p >= 0 and q > 0
    return ((a[0] * p) // q, cdiv(a[1] * p, q))


def powi(a, n):
    assert a[0] >= 0
    r = (ONE, ONE)
    b = a
    while n:
        if n & 1:
            r = mul(r, b)
        n >>= 1
        if n:
            b = mul(b, b)
    return r


def hull(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def imax(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]))


# ---------------- exponential -----------------

def exp_point(v):
    """enclosure of e^(v/2^P) for an integer v (the argument is exact)"""
    if v == 0:
        return (ONE, ONE)
    if v < 0:
        lo, hi = exp_point(-v)
        return ((ONE << P) // hi, cdiv(ONE << P, lo))
    r = max(0, v.bit_length() - P + 16)
    G = 64 + r
    W = P + G
    t = v << (G - r)          # the value v/2^(P+r) < 2^-16 at scale 2^W, exact
    one = 1 << W
    s_lo = one
    term = one
    k = 1
    while True:
        term = ((term * t) >> W) // k
        if term == 0:
            break
        s_lo += term
        k += 1
    s_hi = one
    term = one
    k = 1
    while True:
        term = cdiv(term * t, k << W)
        s_hi += term
        if term <= 1:
            break
        k += 1
    s_hi += 1                 # remainder after the last term is below one unit, since t < 2^-16
    for _ in range(r):
        s_lo = (s_lo * s_lo) >> W
        s_hi = cdiv(s_hi * s_hi, one)
    return (s_lo >> G, cdiv(s_hi, 1 << G))


def exp_iv(a):
    return (exp_point(a[0])[0], exp_point(a[1])[1])


# ---------------- ln(1+u), 0 <= u <= 1 -----------------

def _ln1p_point(v, up):
    assert 0 <= v <= ONE
    if v == 0:
        return 0
    G = 64
    W = P + G
    one = 1 << W
    num = v << W
    den = (2 << P) + v
    z = cdiv(num, den) if up else num // den      # z = u/(2+u) <= 1/3
    z2 = cdiv(z * z, one) if up else (z * z) >> W
    s = 0
    pw = z
    k = 1
    while True:
        term = cdiv(pw, k) if up else pw // k
        s += term
        if up:
            if pw <= 1:
                break
        else:
            if term == 0:
                break
        pw = cdiv(pw * z2, one) if up else (pw * z2) >> W
        k += 2
    if up:
        s += 1                # remainder < pw/8 <= one unit, z^2 <= 1/9
    s = 2 * s
    return cdiv(s, 1 << G) if up else s >> G


def ln1p_iv(a):
    return (_ln1p_point(a[0], False), _ln1p_point(a[1], True))


# ---------------- arctan(1/n), pi -----------------

def atan_inv(n):
    """enclosure of arctan(1/n), n >= 2, by the alternating series with a lower partial sum
    ending in a negative term and an upper partial sum ending in a positive term"""
    G = 64
    W = P + G
    one = 1 << W
    lo = 0
    hi = 0
    k = 0
    while True:
        D = (2 * k + 1) * n ** (2 * k + 1)
        a_lo = one // D
        a_hi = cdiv(one, D)
        if k % 2 == 0:
            lo += a_lo
            hi += a_hi
        else:
            lo -= a_hi
            hi -= a_lo
        if k % 2 == 1 and a_hi <= 1:
            # lo is a partial sum ending in a negative term (a lower bound);
            # hi through this odd k is also a lower partial sum, so add the next positive term
            D2 = (2 * k + 3) * n ** (2 * k + 3)
            hi += cdiv(one, D2)
            break
        k += 1
    return (lo >> G, cdiv(hi, 1 << G))


def pi_iv():
    a5 = atan_inv(5)
    a239 = atan_inv(239)
    return sub(muli(a5, 16), muli(a239, 4))


# ---------------- cos for |x| <= 4, sqrt -----------------

def cos_iv(x):
    """enclosure of cos on an interval x with max|x| <= 4, Taylor with a remainder interval"""
    m = max(abs(x[0]), abs(x[1]))
    assert m <= (4 << P)
    if x[0] <= 0 <= x[1]:
        x2 = (0, mul((m, m), (ONE, ONE))[1])
    else:
        x2 = mul(x, x)
        x2 = (max(0, x2[0]), x2[1])
    s = (ONE, ONE)
    term = (ONE, ONE)
    k = 1
    while True:
        term = divi(mul(term, x2), (2 * k - 1) * (2 * k))
        if k % 2 == 1:
            s = sub(s, term)
        else:
            s = add(s, term)
        if term[1] <= 1 and k > 8:
            break
        k += 1
    # next term bounds the remainder in absolute value (terms decrease once 2k > |x|)
    nxt = divi(mul(term, x2), (2 * k + 1) * (2 * k + 2))
    R = nxt[1] + 2
    return (s[0] - R, s[1] + R)


def isqrt_floor(n):
    return iroot(n, 2)


def sqrt_iv(a):
    assert a[0] >= 0
    lo = isqrt_floor(a[0] << P)
    hi = isqrt_floor(a[1] << P)
    if hi * hi < (a[1] << P):
        hi += 1
    return (lo, hi)


def iroot(n, k):
    """floor of the k-th root of a nonnegative integer n"""
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // (x ** (k - 1))) // k
        if y >= x:
            break
        x = y
    while x ** k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


def root6_iv(a):
    assert a[0] > 0
    lo = iroot(a[0] << (5 * P), 6)
    N = a[1] << (5 * P)
    hi = iroot(N, 6)
    if hi ** 6 < N:
        hi += 1
    return (lo, hi)


# ---------------- decimal input/output, integer only -----------------

def dec(s):
    """parse a decimal string such as 0.114846768 or 1.96e-7 into an integer pair (num, den)"""
    s = s.strip()
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    e = 0
    if 'e' in s:
        s, ex = s.split('e')
        e = int(ex)
    if '.' in s:
        ip, fp = s.split('.')
    else:
        ip, fp = s, ''
    num = int(ip + fp)
    den = 10 ** len(fp)
    if e > 0:
        num *= 10 ** e
    elif e < 0:
        den *= 10 ** (-e)
    return (sign * num, den)


def ge_rat(v, r):
    """v/2^P >= r[0]/r[1]"""
    return v * r[1] >= (r[0] << P)


def le_rat(v, r):
    return v * r[1] <= (r[0] << P)


def lt_rat(v, r):
    return v * r[1] < (r[0] << P)


def gt_rat(v, r):
    return v * r[1] > (r[0] << P)


def inside(a, lo_s, hi_s):
    """the whole interval a lies in [lo_s, hi_s] (decimal strings)"""
    return ge_rat(a[0], dec(lo_s)) and le_rat(a[1], dec(hi_s))


def fmt(v, d, up):
    """v/2^P rounded to d decimals, down (up=False) or up (up=True), as a string"""
    sc = 10 ** d
    q = cdiv(v * sc, ONE) if up else (v * sc) // ONE
    sign = '-' if q < 0 else ''
    q = abs(q)
    ip = q // sc
    fp = q % sc
    return sign + str(ip) + '.' + str(fp).rjust(d, '0')


def fmti(a, d=12):
    return '[' + fmt(a[0], d, False) + ',' + fmt(a[1], d, True) + ']'


def sci(v, sig, up):
    """v/2^P > 0 as an integer mantissa q and exponent x, the string 'q e x' meaning q*10^x,
    with q of sig digits (sig+1 if an upward rounding carried), rounded down or up"""
    assert v > 0
    if v >= ONE:
        e = 0
        while (10 ** (e + 1)) * ONE <= v:
            e += 1
    else:
        e = -1
        while v * (10 ** (-e)) < ONE:
            e -= 1
    shift = sig - 1 - e
    if shift >= 0:
        num = v * (10 ** shift)
        q = cdiv(num, ONE) if up else num // ONE
    else:
        den = ONE * (10 ** (-shift))
        q = cdiv(v, den) if up else v // den
    s = str(q)
    return s[0] + '.' + s[1:] + 'e' + str(e + (len(s) - sig))


def scii(a, sig=10):
    return '[' + sci(a[0], sig, False) + ',' + sci(a[1], sig, True) + ']'
