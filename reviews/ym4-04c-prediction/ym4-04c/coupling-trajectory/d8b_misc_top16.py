"""Design-lane derivation checks (Fractions/integers): 2D beta^12 coefficient, the global-Cauchy certified window, AF targets."""
from fractions import Fraction as F
from math import factorial

TOP = 16


def bessel_series(n, top=TOP + 4):
    # I_n(b) = sum_k (b/2)^(2k+n) / (k! (k+n)!)
    return {2 * k + n: F(1, 2 ** (2 * k + n) * factorial(k) * factorial(k + n)) for k in range(0, (top - n) // 2 + 1)}


def mul(a, b, top=TOP + 4):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i + j <= top:
                out[i + j] = out.get(i + j, 0) + x * y
    return out


def inv_shifted(a):
    # a = b * (a1 + a3 b^2 + ...): return series of 1/(a/b) up to order TOP+2
    lead = a[1]
    rest = {k - 1: v / lead for k, v in a.items() if k > 1}
    # 1/(1 + rest)
    out = {0: F(1)}
    term = {0: F(1)}
    for _ in range(12):
        term = {k: -v for k, v in mul(term, rest).items()}
        for k, v in term.items():
            out[k] = out.get(k, 0) + v
    return {k: v / lead for k, v in out.items()}


I1 = bessel_series(1)
inv = inv_shifted(I1)  # 1/(I1/b)


def t(n):
    In = bessel_series(n)
    # t_n = I_n / I_1 = (I_n / b) * (b / I_1)
    Inb = {k - 1: v for k, v in In.items()}
    return {k: v for k, v in mul(Inb, inv).items() if k <= TOP}


def pw(a, e):
    out = {0: F(1)}
    for _ in range(e):
        out = mul(out, a)
    return {k: v for k, v in out.items() if k <= TOP}


t2, t3, t4 = t(2), t(3), t(4)
print("t2 =", {k: t2[k] for k in sorted(t2) if k <= 9})
T2, T3, T4 = pw(t2, 4), pw(t3, 4), pw(t4, 4)
num = {}
den = {0: F(1)}
for n, Tn in ((2, T2), (3, T3), (4, T4)):
    for k, v in Tn.items():
        num[k] = num.get(k, 0) + F(n * n * (n * n - 1), 3) * v
        den[k] = den.get(k, 0) + n * n * v
# num/den
small = {k: v for k, v in den.items() if k > 0}
invd = {0: F(1)}
term = {0: F(1)}
for _ in range(6):
    term = {k: -v for k, v in mul(term, small).items() if k <= TOP}
    for k, v in term.items():
        invd[k] = invd.get(k, 0) + v
bq2 = {k: v for k, v in mul(num, invd).items() if k <= 14 and v != 0}
print("2D beta'_q series through beta^12:", dict(sorted(bq2.items())))
print("  beta^12 coefficient =", bq2.get(12), float(bq2.get(12)))

# global Cauchy window on fine 6^4 for beta'_S = 2 c_half
Np = 6 * 6 ** 4
R = F(1, 4 * Np)
M = F(1, 2)
poly = lambda b: 2 * (b ** 4 / 128 - b ** 6 / 768 + b ** 8 / 1536 - F(467, 2211840) * b ** 10)
for e in range(26, 19, -1):
    b = F(1, 2 ** e)
    x = b / R
    w = 2 * M * x ** 12 / (1 - x * x)
    c = poly(b)
    print("beta=2^-%d: centre=%.6e half-width=%.6e rel=%.6e contains0=%s" % (e, float(c), float(w), float(w / c), w >= c))

# AF targets: c0 = 11 ln2/(3 pi^2), c1 = 17 ln2/(3 pi^4), by rational enclosures
def ln2_bounds(K=200):
    # ln 2 = sum_{k>=1} 1/(k 2^k); tail after K terms < 1/(K 2^K)
    s = sum(F(1, k * 2 ** k) for k in range(1, K + 1))
    return s, s + F(1, K * 2 ** K)


def atan_inv_bounds(x, K):
    s = F(0)
    for k in range(K):
        s += F((-1) ** k, (2 * k + 1) * x ** (2 * k + 1))
    tail = F(1, (2 * K + 1) * x ** (2 * K + 1))
    return (s - tail, s + tail)


a5 = atan_inv_bounds(5, 60)
a239 = atan_inv_bounds(239, 30)
pi_lo = 4 * (4 * a5[0] - a239[1])
pi_hi = 4 * (4 * a5[1] - a239[0])
l_lo, l_hi = ln2_bounds()
c0 = (F(11) * l_lo / (3 * pi_hi ** 2), F(11) * l_hi / (3 * pi_lo ** 2))
c1 = (F(17) * l_lo / (3 * pi_hi ** 4), F(17) * l_hi / (3 * pi_lo ** 4))
print("c0 in [%.15f, %.15f]" % (float(c0[0]), float(c0[1])))
print("c1 in [%.15f, %.15f]" % (float(c1[0]), float(c1[1])))
print("c0 lo > 25751/100000:", c0[0] > F(25751, 100000), " c0 hi < 25752/100000:", c0[1] < F(25752, 100000))
print("c1 lo > 4032/100000:", c1[0] > F(4032, 100000), " c1 hi < 4033/100000:", c1[1] < F(4033, 100000))
