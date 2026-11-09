#!/usr/bin/env python3
"""
L4-sec4-part2 lane, second seat (local Opus 5.5, pid 8467a937cba309f7).
Integer-only outward-rounded interval arithmetic. A real number v is enclosed by a pair of integers
(lo, hi) with lo <= v * 2^P <= hi. No float, no fraction type, no decimal type, no true-division operator:
every quotient is an integer floor (//) or an integer ceiling (neg of floor of neg). Rationals enter as
integer pairs (n, d) and are rounded outward once.
"""
import io
import sys
import tokenize

P = 704
ONE = 1 << P


def fdiv(a, b):
    assert b > 0
    return a // b


def cdiv(a, b):
    assert b > 0
    return -((-a) // b)


def rat(n, d=1):
    """outward enclosure of n/d."""
    if d < 0:
        n, d = -n, -d
    return (fdiv(n * ONE, d), cdiv(n * ONE, d))


def pt(v):
    return (v, v)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (fdiv(min(ps), ONE), cdiv(max(ps), ONE))


def imul(a, k):
    """interval times an exact integer k."""
    if k >= 0:
        return (a[0] * k, a[1] * k)
    return (a[1] * k, a[0] * k)


def div(a, b):
    """a / b for an interval b with b > 0 throughout."""
    assert b[0] > 0, "divisor interval not positive"
    qs_lo = [fdiv(a[0] * ONE, b[0]), fdiv(a[0] * ONE, b[1]), fdiv(a[1] * ONE, b[0]), fdiv(a[1] * ONE, b[1])]
    qs_hi = [cdiv(a[0] * ONE, b[0]), cdiv(a[0] * ONE, b[1]), cdiv(a[1] * ONE, b[0]), cdiv(a[1] * ONE, b[1])]
    return (min(qs_lo), max(qs_hi))


def powi(a, k):
    r = (ONE, ONE)
    for _ in range(k):
        r = mul(r, a)
    return r


def hull(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def imax(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]))


def le(a, b):
    """certified a <= b."""
    return a[1] <= b[0]


def lt(a, b):
    """certified a < b."""
    return a[1] < b[0]


def _exp_nonneg(Y):
    """(lo, hi) enclosure of e^(Y/ONE) * ONE for an exact integer Y >= 0."""
    assert Y >= 0
    k = 0
    while (Y >> k) > (ONE >> 20):
        k += 1
    k += 0
    # z = Y / (ONE * 2^k) <= 2^-20 exactly; Taylor series with rounding outward per term.
    D = ONE << k
    tlo, thi = ONE, ONE
    slo, shi = ONE, ONE
    j = 0
    while thi > 1:
        j += 1
        tlo = fdiv(tlo * Y, D * j)
        thi = cdiv(thi * Y, D * j)
        slo += tlo
        shi += thi
        if j > 2000:
            raise RuntimeError("exp did not converge")
    # the dropped tail after term j is at most term_j * (z + z^2 + ...) <= 2 z term_j <= 1 unit here
    shi += 2
    for _ in range(k):
        slo = fdiv(slo * slo, ONE)
        shi = cdiv(shi * shi, ONE)
    return (slo, shi)


def exp_point(Y):
    if Y >= 0:
        return _exp_nonneg(Y)
    lo, hi = _exp_nonneg(-Y)
    return (fdiv(ONE * ONE, hi), cdiv(ONE * ONE, lo))


def iexp(a):
    """enclosure of e^x for x in the interval a (e^x is increasing)."""
    return (exp_point(a[0])[0], exp_point(a[1])[1])


def _ln1p_point(X):
    """(lo, hi) enclosure of ln(1 + X/ONE) * ONE for an exact integer 0 <= X <= ONE/2, alternating series."""
    assert 0 <= X <= ONE // 2
    if X == 0:
        return (0, 0)
    plo, phi = ONE, ONE
    lo, hi = 0, 0
    j = 0
    while True:
        j += 1
        plo = fdiv(plo * X, ONE)
        phi = cdiv(phi * X, ONE)
        tlo, thi = fdiv(plo, j), cdiv(phi, j)
        if j % 2 == 1:
            lo += tlo
            hi += thi
        else:
            lo -= thi
            hi -= tlo
        if thi <= 1 and j % 2 == 0:
            # partial sum with an even number of terms is a lower bound; add the next (odd) term's upper bound to hi
            nphi = cdiv(phi * X, ONE)
            hi_extra = cdiv(nphi, j + 1)
            return (lo - 2, hi + hi_extra + 2)
        if j > 4000:
            raise RuntimeError("ln1p did not converge")


def iln1p(a):
    assert a[0] >= 0
    return (_ln1p_point(a[0])[0], _ln1p_point(a[1])[1])


def isqrt_floor(n):
    assert n >= 0
    if n == 0:
        return 0
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def iroot_floor(n, k):
    """floor(n^(1/k)) for an integer n >= 0."""
    assert n >= 0 and k >= 1
    if n < 2:
        return n
    x = 1 << (n.bit_length() // k + 1)
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


def iroot6(a):
    """enclosure of the sixth root of an interval a >= 0."""
    assert a[0] >= 0
    lo = iroot_floor(a[0] * ONE ** 5, 6)
    hi = iroot_floor(a[1] * ONE ** 5, 6)
    if hi ** 6 < a[1] * ONE ** 5:
        hi += 1
    return (lo, hi)


def dec(v, places, up=False):
    """decimal string of floor (or ceil) of v/ONE to `places` places, integer arithmetic only."""
    scale = 10 ** places
    if up:
        n = cdiv(v * scale, ONE)
    else:
        n = fdiv(v * scale, ONE)
    sign = "-" if n < 0 else ""
    n = abs(n)
    s = str(n).rjust(places + 1, "0")
    return sign + s[:-places] + "." + s[-places:]


def ds(a, places):
    return "[" + dec(a[0], places) + "," + dec(a[1], places, up=True) + "]"


def self_check(path):
    src = open(path, encoding="utf-8").read()
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    bad_num = [t.string for t in toks if t.type == tokenize.NUMBER
               and any(c in t.string.lower() for c in ".ej") and not t.string.lower().startswith("0x")]
    bad_div = [t.start[0] for t in toks if t.type == tokenize.OP and t.string in ("/", "/=")]
    bad_pow = [toks[i].start[0] for i in range(len(toks) - 1)
               if toks[i].type == tokenize.OP and toks[i].string == "**" and toks[i + 1].string == "-"]
    bad_name = [t.string for t in toks if t.type == tokenize.NAME and t.string in
                ("float", "Fraction", "Decimal", "fractions", "decimal", "math")]
    return (len(bad_num), len(bad_div), len(bad_pow), len(bad_name))
