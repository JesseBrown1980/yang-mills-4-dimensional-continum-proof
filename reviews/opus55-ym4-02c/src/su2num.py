#!/usr/bin/env python3
"""Second seat: the SU(2) enclosures from a separate integer route. Scaled integers at 10^80, with l_n from the Bessel recurrence check, series summed to 80 terms. Also the coefficient of beta^3 extracted from the l_n series rather than typed. Standard library, integers only, json=0."""
import math

SCALE = 10 ** 80


def l_scaled(n, beta_num=1):
    """l_n(1) = sum_k (1/2)^(2k+n) / (k! (k+n+1)!) scaled by SCALE, rounded down, with an upper bound equal to the value plus 200 units."""
    total = 0
    for k in range(0, 80):
        total += SCALE // (2 ** (2 * k + n) * math.factorial(k) * math.factorial(k + n + 1))
    return total


def exp_minus(m):
    """exp(-m) scaled, from the alternating series to 200 terms."""
    total = 0
    for k in range(0, 200):
        total += (-1) ** k * m ** k * SCALE // math.factorial(k)
    return total


def main():
    ls = [l_scaled(n) for n in range(0, 30)]
    e1 = exp_minus(1)
    # Z = sum_n (exp(-1) l_n)^F
    for F in (4, 6):
        z = 0
        for v in ls:
            t = v * e1 // SCALE
            p = SCALE
            for _ in range(F):
                p = p * t // SCALE
            z += p
        print("SU2_TORUS_SEPARATE|F=%d|Z_times_10^15=%d|exp(-F)_times_10^15=%d|json=0" % (F, z // 10 ** 65, exp_minus(F) // 10 ** 65))
    # Numerator on (Z/3)x(Z/2): (1/2) sum_n (l_n l_(n+1))^3 at beta=1, over exp(-6).
    s = 0
    for n in range(0, 29):
        t = ls[n] * ls[n + 1] // SCALE
        s += t * t // SCALE * t // SCALE
    print("SU2_GRAM_SEPARATE|half_sum_times_10^15=%d|json=0" % (s // 2 // 10 ** 65))
    # The polynomial in beta of (1/2) sum_n (l_n l_(n+1))^3 through beta^7, in rationals, as coefficient lists over 2^k style integers. l_n(beta) = sum_k beta^(2k+n) / (2^(2k+n) k! (k+n+1)!).
    deg = 9
    D = 2 ** 40 * math.factorial(12) ** 4

    def series(n):
        out = [0] * (deg + 1)
        k = 0
        while 2 * k + n <= deg:
            out[2 * k + n] = (2 ** (2 * k + n) * math.factorial(k) * math.factorial(k + n + 1))
            k += 1
        return out  # stored as denominators, 0 means zero coefficient

    def to_pairs(den):
        return [(0, 1) if d == 0 else (1, d) for d in den]

    def rat(a, b):
        g = math.gcd(a, b)
        return (a // g, b // g)

    def padd(x, y):
        return rat(x[0] * y[1] + y[0] * x[1], x[1] * y[1])

    def pmul(x, y):
        return rat(x[0] * y[0], x[1] * y[1])

    def smul(a, b):
        out = [(0, 1)] * (deg + 1)
        for i, x in enumerate(a):
            if x[0] == 0:
                continue
            for j, y in enumerate(b):
                if y[0] != 0 and i + j <= deg:
                    out[i + j] = padd(out[i + j], pmul(x, y))
        return out
    total = [(0, 1)] * (deg + 1)
    for n in range(0, deg + 1):
        a = smul(to_pairs(series(n)), to_pairs(series(n + 1)))
        c = smul(smul(a, a), a)
        total = [padd(x, pmul((1, 2), y)) for x, y in zip(total, c)]
    print("SU2_GRAM_SERIES|numerator_exp(6beta)_coefficients_through_beta^9=%s|json=0" % ",".join("%d/%d" % p for p in total))


main()
