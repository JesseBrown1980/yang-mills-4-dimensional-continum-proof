"""Design-lane derivation check: tree-level (Gaussian, abelian-linearized) one-step couplings.

r(p) = C'_W(p)/C'(p) for a transverse coarse mode: polarization e_mu, momentum p = kappa e_nu (p_mu = 0).
Line map (YM4-03 B_b):   C'(p) = b^(2-d) sum_{n_perp in Z_b^(d-1)} 1/khat^2(k_n),  k_n = (p + 2 pi n)/b, n_mu = 0.
Averaged map (b-step transporters averaged over all b^d starting points of the block):
                          C'(p) = b^(2-d) sum_{n_nu} T_nu(k) / khat^2(k),  n_lambda = 0 for lambda not in {mu, nu},
                          T_nu(k) = sin^2(b k_nu/2) / (b^2 sin^2(k_nu/2)).
Coarse Wilson: C'_W(p) = 1/(4 sin^2(kappa/2)).
Scratch only: b = 2 in Fractions; b = 4, 8 in Decimal at 60 digits (not evidence; the engine uses rational enclosures).
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
import itertools

getcontext().prec = 60


def pi_dec():
    getcontext().prec += 10
    # Machin
    def arctan_inv(x):
        x = D(x)
        s, t, n, sign = D(0), 1 / x, 1, 1
        x2 = x * x
        while True:
            term = t / n
            if term < D(10) ** (-(getcontext().prec)):
                break
            s += sign * term
            t /= x2
            n += 2
            sign = -sign
        return s
    p = 4 * (4 * arctan_inv(5) - arctan_inv(239))
    getcontext().prec -= 10
    return +p


PI = pi_dec()


def sin_dec(x):
    getcontext().prec += 10
    x = D(x)
    s, t, n = D(0), x, 1
    while abs(t) > D(10) ** (-(getcontext().prec)):
        s += t
        t = -t * x * x / ((n + 1) * (n + 2))
        n += 2
    getcontext().prec -= 10
    return +s


def s2(x):  # 4 sin^2(x/2)
    v = sin_dec(x / 2)
    return 4 * v * v


def line_C(d, b, kappa):
    tot = D(0)
    for n in itertools.product(range(b), repeat=d - 1):  # n[0] is the nu direction, rest transverse
        kn = (kappa + 2 * PI * n[0]) / b
        den = s2(kn) + sum(s2(2 * PI * m / b) for m in n[1:])
        tot += 1 / den
    return D(b) ** (2 - d) * tot


def avg_C(d, b, kappa):
    tot = D(0)
    for n0 in range(b):
        kn = (kappa + 2 * PI * n0) / b
        T = (sin_dec(b * kn / 2) ** 2) / (b * b * sin_dec(kn / 2) ** 2)
        tot += T / s2(kn)
    return D(b) ** (2 - d) * tot


def CW(kappa):
    return 1 / s2(kappa)


print("pi =", str(PI)[:30])
for d in (2, 3, 4):
    for b in (2, 3, 4, 8):
        rl = CW(PI) / line_C(d, b, PI)
        ra = CW(PI) / avg_C(d, b, PI)
        print("d=%d b=%d  r_line(pi)=%.15f  b^(4-d) r_line=%.15f  r_avg(pi)=%.15f" % (d, b, rl, rl * D(b) ** (4 - d), ra))

# exact b = 2, d = 4 corner value
tot = F(0)
for n in itertools.product(range(2), repeat=3):
    den = F(2) + sum(4 * m for m in n[1:])  # 4 sin^2((pi + 2 pi n0)/4) = 2; 4 sin^2(pi m/2) = 4 m
    tot += 1 / den
C = F(1, 4) * tot
print("exact d=4 b=2: C'(pi) =", C, " r =", F(1, 4) / C)

# small-p slope A_b(0): r = 1/(1 + A phat^2 + ...), A = b^(2-d) sum_{n_perp != 0, n_nu = anything but not all zero} 1/khat^2(2 pi n/b) - (1 - 1/b^2)/12
for d in (3, 4):
    for b in (2, 4, 8):
        tot = D(0)
        for n in itertools.product(range(b), repeat=d - 1):
            if all(m == 0 for m in n):
                continue
            tot += 1 / sum(s2(2 * PI * m / b) for m in n)
        A = D(b) ** (2 - d) * tot - (1 - D(1) / (b * b)) / 12
        print("d=%d b=%d A_b(0)=%.15f  A/b=%.15f" % (d, b, A, A / b))
# check by finite difference at small kappa
for b in (2, 4):
    kap = D(1) / 1000
    r = CW(kap) / line_C(4, b, kap)
    print("b=%d kappa=1e-3: (1/r - 1)/phat^2 = %.10f" % (b, (1 / r - 1) / s2(kap)))
# exact b=2 A_2(0) in d=4
tot = F(0)
for n in itertools.product(range(2), repeat=3):
    if n == (0, 0, 0):
        continue
    tot += F(1, 4 * sum(n))
print("exact d=4 b=2 A_2(0) =", F(1, 4) * tot - F(3, 4) / 12)

# averaged map closed form check: sum csc^4((2n+1)pi/(2b)) = b^2 (b^2 + 2)/3
for b in (2, 3, 4, 5, 8, 16):
    s = sum(1 / sin_dec((2 * n + 1) * PI / (2 * b)) ** 4 for n in range(b))
    print("b=%d sum csc^4 = %.20f  b^2(b^2+2)/3 = %s" % (b, s, F(b * b * (b * b + 2), 3)))

# Watson-type limit: b * r_line(pi; b) -> 1/(4 G_3(0)), G_3(0) = 0.2527310098586...
print("1/(4*0.2527310098586) =", 1 / (4 * D("0.2527310098586")))
