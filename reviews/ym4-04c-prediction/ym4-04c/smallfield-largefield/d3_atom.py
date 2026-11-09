"""Derivation check (asymptotic, not the engine's convergent series): the one-link atom.

Z_beta(Q) = sum_m (beta^2 Q/4)^m/(m!(m+1)!) = 2 I_1(x)/x, x = beta sqrt(Q), Q = |sum v_i|^2 = 36 - 2D.
S_ind = -log Z.  beta_loop = dS_ind/dD at D=0 = (beta/6) I_2(6beta)/I_1(6beta).
R(D) = S_ind(36-2D) - S_ind(36) - beta_loop*D.
Asymptotic expansion of I_nu with K terms, as a check on the predicted brackets only.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from ri import I, sqrt_i, log_i, dec

K = 12


def a_coef(nu, K):
    out = [Fr(1)]
    for k in range(1, K + 1):
        out.append(out[-1] * (4 * nu * nu - (2 * k - 1) ** 2) / (k * 8))
    return out  # I_nu ~ e^x/sqrt(2 pi x) sum (-1)^k a_k / x^k


A1 = a_coef(1, K)
A2 = a_coef(2, K)


def series_mul(a, b, K):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]


def series_inv(a, K):
    inv = [Fr(1) / a[0]]
    for k in range(1, K + 1):
        inv.append(-sum(a[i] * inv[k - i] for i in range(1, k + 1)) / a[0])
    return inv


s1 = [(-1) ** k * A1[k] for k in range(K + 1)]
s2 = [(-1) ** k * A2[k] for k in range(K + 1)]
ratio = series_mul(s2, series_inv(s1, K), K)  # I_2/I_1 in powers of 1/x
print("I2/I1 ~", [str(c) for c in ratio[:6]])
# beta_loop = (beta/6) * sum ratio_k /(6 beta)^k
bl = [ratio[k] / Fr(6) ** (k + 1) for k in range(K + 1)]  # coefficient of beta^(1-k)
print("beta_loop ~ beta*%s + %s + %s/beta + %s/beta^2 + %s/beta^3" % tuple(str(c) for c in bl[:5]))


def log_series(a, K):
    # log(a) for a[0]=1
    b = a[:]
    b[0] = Fr(0)
    out = [Fr(0)] * (K + 1)
    p = [Fr(1)] + [Fr(0)] * K
    for n in range(1, K + 1):
        p = series_mul(p, b, K)
        for k in range(K + 1):
            out[k] += (-1) ** (n + 1) * p[k] / n
    return out


L1 = log_series(s1, K)  # log S_1 in powers of 1/x


def logZ_rel(beta, Q):
    """log Z(Q) - const, const = log2 - log(2pi)/2, truncated asymptotic (good for x >> K)."""
    x = beta * sqrt_i(Q)
    val = x - Fr(3, 2) * log_i(x)
    ux = x.inv()
    p = I(1)
    for k in range(1, 7):
        p = p * ux
        val = val + L1[k] * p
    return val


for beta in (64, 256, 1024, 4096):
    blv = sum(bl[k] * Fr(beta) ** (1 - k) for k in range(8))
    print("beta=%d beta_loop~%s  minus(beta/6-1/24)=%s  *beta=%s" % (
        beta, dec(blv), dec(blv - Fr(beta, 6) + Fr(1, 24)), dec((blv - Fr(beta, 6) + Fr(1, 24)) * beta)))
    for p2 in (Fr(1, 2), Fr(2)):
        D = 30 * p2 / beta
        R = -(logZ_rel(beta, 36 - 2 * D) - logZ_rel(beta, 36)) - blv * D
        lead = Fr(25, 12) * p2 * p2 / beta
        print("   p^2=%s D=30p^2/beta=%s R=%s  R/(25p^4/(12beta))=%s" % (p2, D, R, R / lead))
