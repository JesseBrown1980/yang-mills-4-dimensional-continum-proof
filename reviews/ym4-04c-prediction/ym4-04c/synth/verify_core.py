"""Synthesis-lane spot check of the repaired polymer-norm rows. Decimal at 60 digits; not an engine.
The a-search is the convex form pinned in the synthesis: g(a) = S(eps e^{2a+b}) - a is convex in a."""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from math import comb
import sys

getcontext().prec = 60
ONE = D(1)
KAP = D(1) / 4


def c0(x):
    x = D(x); s = D(0); t = ONE; m = 0; h2 = (x / 2) ** 2
    while True:
        s += t
        t = t * h2 / ((m + 1) * (m + 2)); m += 1
        if t < D(10) ** -58 and m > 4:
            return s


def eps6(beta):
    b = D(beta.numerator) / D(beta.denominator) if isinstance(beta, F) else D(beta)
    cb = c0(b)
    tot = sum(comb(6, k) * (-1) ** (6 - k) * c0(k * b) / cb ** k for k in range(7))
    return tot ** (ONE / 6)


def Fc(n):
    return comb(20 * n, n) // (19 * n + 1)


MU = D(20) ** 20 / D(19) ** 19
FC = {n: D(Fc(n)) for n in range(1, 60)}


def S(x, head):
    if MU * x >= 1:
        return None
    s = D(0)
    for n in range(4, 49):
        c = D(head[n]) if (n <= 10 and n in head) else 6 * FC[n]
        s += c * x ** n
    return s + 6 * FC[49] * x ** 49 / (1 - MU * x)


def g(a, e, b, head):
    s = S(e * (2 * a + b).exp(), head)
    return None if s is None else s - a


def least_a(e, b, head):
    lo, hi = D(0), D(1) / 4
    # ternary search for the minimum of convex g on [0, 1/4], None = +inf
    for _ in range(140):
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        g1 = g(m1, e, b, head); g2 = g(m2, e, b, head)
        if g1 is None:
            hi = m1; continue
        if g2 is None or g1 <= g2:
            hi = m2
        else:
            lo = m1
    am = (lo + hi) / 2
    gm = g(am, e, b, head)
    if gm is None or gm > 0:
        return None
    lo, hi = D(0), am  # g(0) > 0 >= g(am); g decreasing on [0, am]
    for _ in range(140):
        mid = (lo + hi) / 2
        if g(mid, e, b, head) <= 0:
            hi = mid
        else:
            lo = mid
    return hi


def C0(beta, head, imax=128, weight="delta"):
    e = eps6(beta); best = None
    for i in range(imax + 1):
        b = KAP + D(i) / 64
        a = least_a(e, b, head)
        if a is None:
            continue
        v = 12 * a * (-4 * (b - KAP)).exp() if weight == "delta" else D("0.8489") * 12 * a * (-8 * b).exp()
        if best is None or v < best[0]:
            best = (v, a, b, i)
    return best


def cfun(d):
    dp = d * d.exp()
    if 2 * dp > KAP / 2:
        return None
    m = max((-(KAP / 2 - 2 * dp) * n).exp() - (-KAP * n / 2).exp() for n in range(4, 600))
    return d.exp() * ((-4 * KAP).exp() + m)


CRUDE = {}
FREE = {n: 0 for n in range(4, 11)}
MEAS = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}


def P10(b):
    return b ** 4 / 128 - b ** 6 / 768 + b ** 8 / 1536 - 467 * b ** 10 / 2211840


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "dcrit":
        lo, hi = D("0.049"), D("0.050")
        for _ in range(50):
            mid = (lo + hi) / 2
            c = cfun(mid)
            if c is not None and c < 1:
                lo = mid
            else:
                hi = mid
        print("delta_crit in", lo, hi)
        for d in ("0.049", "0.0496", "0.0497", "0.050"):
            print("c(", d, ")=", cfun(D(d)))
    elif what == "points":
        for name, head in (("crude", CRUDE), ("free", FREE), ("meas", MEAS)):
            for beta in (F(1, 100), F(1, 64), F(1, 50)):
                r = C0(beta, head)
                if r is None:
                    print(name, beta, "NOT_MET"); continue
                c = cfun(r[0])
                print(name, beta, "delta1=%.7e a=%.6e b_i=%d c=%s" % (r[0], r[1], r[3], None if c is None else "%.6f" % c),
                      "2d'=%.6f" % (2 * r[0] * r[0].exp()))
    elif what == "edge":
        name = sys.argv[2]; head = {"crude": CRUDE, "free": FREE, "meas": MEAS}[name]
        dmax = None if sys.argv[3] == "none" else D(sys.argv[3])
        for j in [int(x) for x in sys.argv[4].split(",")]:
            r = C0(F(j, 100000), head)
            ok = r is not None and (dmax is None or r[0] < dmax)
            print(name, j, "MET" if ok else "NOT_MET", None if r is None else "%.6e" % r[0], flush=True)
    elif what == "c09":
        for beta in (F(1, 4000), F(1, 2000), F(1, 1000), F(1, 700), F(1, 100)):
            p = P10(D(beta.numerator) / D(beta.denominator))
            for imax in (128, 320):
                r = C0(beta, MEAS, imax, weight="T")
                print("C09", beta, imax, "T/P10=%.4e" % (r[0] / p), "b_i", r[3], flush=True)
