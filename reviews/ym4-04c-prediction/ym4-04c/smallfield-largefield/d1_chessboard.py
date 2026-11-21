"""Derivation check: chessboard large-field exponent Phi_0(beta) on fine L^4 tori."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from ri import I, sqrt_i, log_i, arcsin_small, pi_i, dec

PI = pi_i()


def h_cap(t):
    t = Fr(t)
    th = 2 * arcsin_small(sqrt_i(t / 2))
    s = sqrt_i(2 * t - t * t)
    sin2 = 2 * s * (1 - t)
    return (2 * th - sin2) / (2 * PI)


def phi0(L, beta):
    Ns = L ** 4
    Nl = 4 * Ns
    Np = 6 * Ns
    Nf = Nl - Ns + 1
    t = Fr(3 * Nf, 32 * Np) / beta
    h = h_cap(t)
    val = (-Nf * log_i(h) + Fr(3, 2) * Nf) / Ns
    return Nf, t, h, val


for L in (4, 8):
    for beta in (16, 64, 256, 1024, 4096):
        Nf, t, h, v = phi0(L, beta)
        lb = log_i(I(beta))
        c = (v - Fr(3 * (4 * L**4 - L**4 + 1), 2 * L**4) * lb)
        print("L=%d beta=%d Nf=%d t*=%s Phi0=%s  p0^2=Phi0/2=%s  p1^2=32Phi0=%s  Phi0-(3Nf/2Ns)log(beta)=%s"
              % (L, beta, Nf, t, v, v * Fr(1, 2), v * 32, c))
