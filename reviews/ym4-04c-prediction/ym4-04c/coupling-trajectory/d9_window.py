"""Design-lane derivation check (Fractions with outward dyadic rounding): the global-Cauchy certified window, fine 6^4.

On |z| <= r/N_p, r < ln 2: |F_V(z) - 1| <= e^r - 1 < 1, so |log F_V(z)| <= M(r) = -ln(2 - e^r), and the chi_1/2(V_P)
projection c(z) of log F_V obeys |c(z)| <= M(r).  Even orders only (P3).
beta'_S = 2c: enclosure poly_10(beta) +- 2 M x^12/(1 - x^2), x = beta N_p / r.
"""
from fractions import Fraction as F
import math

Np = 6 * 6 ** 4
P = 2 ** 160


def dn(x):
    return F(math.floor(x * P), P)


def up(x):
    return F(math.ceil(x * P), P)


def exp_bounds(r, K=60):
    s, t = F(0), F(1)
    for k in range(K):
        s += t
        t = t * r / (k + 1)
    return dn(s), up(s + 2 * t)


def ln_small(u, K=200):  # ln(1/(1-u)) = sum u^k/k for 0 <= u <= 1/2; tail <= 2 u^(K+1)/(K+1)
    s, p = F(0), F(1)
    for k in range(1, K + 1):
        p = up(p * u)
        s += p / k
    lo = s - 0  # partial sums with upward-rounded powers: use separate lower pass
    s2, p2 = F(0), F(1)
    for k in range(1, K + 1):
        p2 = dn(p2 * u)
        s2 += p2 / k
    return dn(s2), up(s + 2 * p * u / (K + 1))


LN2 = ln_small(F(1, 2))


def neglog_bounds(y):  # -ln y for 0 < y < 1: y = 2^-m w, w in [1/2, 1)
    m = 0
    w = y
    while w < F(1, 2):
        w *= 2
        m += 1
    a_lo, a_hi = ln_small(1 - w)
    return m * LN2[0] + a_lo, m * LN2[1] + a_hi


def poly(b):
    return 2 * (b ** 4 / 128 - b ** 6 / 768 + b ** 8 / 1536 - F(467, 2211840) * b ** 10)


def rel(beta, r, M):
    x = beta * Np / r
    return 2 * M * x ** 12 / (1 - x * x) / poly(beta)


for e in (24, 23):
    v = rel(F(1, 2 ** e), F(1, 4), F(1, 2))
    print("YM4-04A disk, beta=2^-%d: rel half-width = %.9f, <=1/64: %s, contains 0: %s" % (e, float(v), v <= F(1, 64), v >= 1))
best = None
for j in range(600, 710):
    r = F(j, 1024)
    elo, ehi = exp_bounds(r)
    assert ehi < 2
    Mhi = neglog_bounds(2 - ehi)[1]
    v = rel(F(1, 2 ** 22), r, Mhi)
    if best is None or v < best[0]:
        best = (v, j)
print("best grid disk at 2^-22: j=%d rel=%.6f <=1/16: %s" % (best[1], float(best[0]), best[0] <= F(1, 16)))
worst = None
for j in range(1, 710):
    r = F(j, 1024)
    elo, ehi = exp_bounds(r)
    Mlo = neglog_bounds(2 - elo)[0]
    v = rel(F(1, 2 ** 21), r, Mlo)
    if worst is None or v < worst[0]:
        worst = (v, j)
print("at 2^-21: smallest rel over grid r (M lower bound): j=%d rel=%.4f; contains 0 for every j<=709: %s" % (worst[1], float(worst[0]), worst[0] >= 1))
print("709/1024 < ln2 < 710/1024:", F(709, 1024) < LN2[0], LN2[1] < F(710, 1024))
