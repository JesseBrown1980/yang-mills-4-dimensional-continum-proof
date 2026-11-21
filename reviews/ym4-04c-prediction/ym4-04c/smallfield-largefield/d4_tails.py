"""Derivation check: Q(3/2,y) = Gamma(3/2,y)/Gamma(3/2) = erfc(sqrt y) + 2 sqrt(y/pi) e^{-y},
the first-order atom correction c(p) = y^{3/2} e^{-y} / (24 Gamma(3/2,y)), and the
AF summability control arithmetic. Rational intervals only."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from ri import I, sqrt_i, log_i, exp_r, pi_i, dec, log_r

PI = pi_i()
SQPI = sqrt_i(PI)


def erf_r(z):
    """erf of interval z (0<=z<=6) via alternating Taylor series, monotone in z."""
    def e(zz):
        zz = Fr(zz)
        s = Fr(0)
        t = zz  # z^{2n+1}/n!
        n = 0
        while True:
            term = t / (2 * n + 1)
            s += term if n % 2 == 0 else -term
            n += 1
            t = t * zz * zz / n
            if t / (2 * n + 1) < Fr(1, 1 << 200) and n > 2 * zz * zz:
                break
        err = t / (2 * n + 1)
        return I(s - err, s + err)
    lo = e(z.lo) * 2 / SQPI
    hi = e(z.hi) * 2 / SQPI
    return I(lo.lo, hi.hi)


def Q32(y):
    y = Fr(y)
    z = sqrt_i(y)
    erfc = 1 - erf_r(z)
    ey = exp_r(-y)
    return erfc + 2 * sqrt_i(y) / SQPI * ey


def c_atom(y):
    y = Fr(y)
    G = Q32(y) * SQPI / 2  # Gamma(3/2,y)
    num = y * sqrt_i(y) * exp_r(-y)
    return num / (24 * G)


for y in (Fr(2), Fr(4), Fr(6), Fr(8), Fr(12), Fr(16), Fr(24)):
    print("Q(3/2,%s) = %s   [P(chi2_3 > %s)]" % (y, Q32(y), 2 * y))
for p2 in (Fr(1, 2), Fr(1)):
    y = 12 * p2
    print("atom p^2=%s y=%s c(p)=%s" % (p2, y, c_atom(y)))
# 2D fine first-order coefficient (kappa = beta): (Gamma(5/2,y)/Gamma(3/2,y)-3/2)/4
for c in (2, 8, 16):
    y = Fr(c)
    G = Q32(y) * SQPI / 2
    print("2D fine c=%d first-order coeff %s" % (c, y * sqrt_i(y) * exp_r(-y) / (4 * G)))
# Gaussian line-map LF at fixed p^2=2: Q(3/2, 4p^2/r)
for r in (Fr(1), Fr(275, 100), Fr(65, 10)):
    print("Q(3/2, 8/r) r=%s : %s" % (r, Q32(8 / r)))
# AF summability: b = 11 log 2 /(3 pi^2)
b = 11 * log_i(I(2)) / (3 * PI * PI)
print("b0' =", b)
for e0 in (20, 40, 80):
    beta0 = Fr(2) ** e0
    lower = log_i(I(beta0 / 16)) / b
    print("beta0=2^%d: sum_k 1/beta_k >= (1/b) log(beta0/16) = %s" % (e0, lower))
