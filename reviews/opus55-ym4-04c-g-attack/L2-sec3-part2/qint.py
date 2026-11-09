# Integer-only rational helpers for lane L2-sec3-part2 (G_attack on YM4-04C).
# A rational is a pair (num, den) of Python ints with den > 0, reduced.
# No float, no fractions module, no decimal module, no true division.
from math import gcd, comb, factorial

def q(n, d=1):
    if d == 0:
        raise ZeroDivisionError("zero denominator")
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    return (n // g, d // g)

ZERO = (0, 1)
ONE = (1, 1)

def add(a, b): return q(a[0] * b[1] + b[0] * a[1], a[1] * b[1])
def sub(a, b): return q(a[0] * b[1] - b[0] * a[1], a[1] * b[1])
def mul(a, b): return q(a[0] * b[0], a[1] * b[1])
def div(a, b): return q(a[0] * b[1], a[1] * b[0])
def neg(a): return (-a[0], a[1])
def ip(b, k):
    # integer power that refuses a negative exponent (square and multiply)
    if k < 0:
        raise ValueError("negative exponent")
    r = 1
    while k:
        if k & 1:
            r *= b
        b *= b
        k >>= 1
    return r

def sgn(k):  # (-1)^k for an integer k
    return -1 if k % 2 else 1

def ipow(a, k): return (ip(a[0], k), ip(a[1], k))
def le(a, b): return a[0] * b[1] <= b[0] * a[1]
def lt(a, b): return a[0] * b[1] < b[0] * a[1]
def qsum(xs):
    s = ZERO
    for x in xs:
        s = add(s, x)
    return s

def floordiv(n, d):  # floor(n/d), d > 0
    return n // d

def ceildiv(n, d):  # ceil(n/d), d > 0
    return -((-n) // d)

def up(a, bits):
    # outward (upward) rounding to a dyadic of denominator 2^bits
    return q(ceildiv(a[0] << bits, a[1]), 1 << bits)

def down(a, bits):
    return q(floordiv(a[0] << bits, a[1]), 1 << bits)

def dec(a, places, mode="floor"):
    # decimal string of a rational, rounded down (floor) or up (ceil) at `places`
    scale = ip(10, places)
    n = a[0] * scale
    v = floordiv(n, a[1]) if mode == "floor" else ceildiv(n, a[1])
    sign = "-" if v < 0 else ""
    v = abs(v)
    s = str(v).rjust(places + 1, "0")
    return sign + s[:-places] + "." + s[-places:] if places > 0 else sign + s

def iroot_floor(n, k):
    # floor of the k-th root of a nonnegative int
    if n < 2:
        return n
    lo, hi = 0, 1 << ((n.bit_length() + k - 1) // k + 1)
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if ip(mid, k) <= n:
            lo = mid
        else:
            hi = mid
    return lo

def exp_lo_hi(r, terms=60):
    # rational enclosure of e^r for a rational 0 <= r < 1:
    # lower = partial sum; upper = partial sum + 3 r^(J+1)/(J+1)!  (remainder <= r^(J+1)/(J+1)! * e^r, e^r < 3)
    assert le(ZERO, r) and lt(r, ONE)
    s = ZERO
    t = ONE
    for j in range(terms + 1):
        s = add(s, t)
        t = div(mul(t, r), q(j + 1))
    lo = s
    hi = add(s, mul(q(3), t))
    return lo, hi

def F(n, D=20):
    # Fuss-Catalan F_D(n) = C(Dn, n)/((D-1)n + 1), exact
    num = comb(D * n, n)
    den = (D - 1) * n + 1
    assert num % den == 0
    return num // den
