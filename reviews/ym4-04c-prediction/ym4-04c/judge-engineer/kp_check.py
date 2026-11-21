"""Judge spot check of polymer-norm closed-form rows (C02, C04, C05, C07, C11-C15).
Decimal at 80 digits (a judge sanity check, not an engine; no binary floats)."""
from decimal import Decimal as Dd, getcontext
from math import comb, factorial

getcontext().prec = 80
ONE = Dd(1)


def c0(x):
    s = Dd(0)
    term = ONE
    m = 0
    h2 = (x / 2) ** 2
    while True:
        s += term
        term = term * h2 / ((m + 1) * (m + 2))
        m += 1
        if term < Dd(10) ** -78 and m > 5:
            break
    return s


def eps6(beta):
    b = Dd(beta)
    cb = c0(b)
    tot = Dd(0)
    for k in range(7):
        tot += comb(6, k) * (-1) ** (6 - k) * c0(k * b) / cb ** k
    return tot ** (ONE / 6)


def F(n, Dg=20):
    return comb(Dg * n, n) // ((Dg - 1) * n + 1)


MU = Dd(20) ** 20 / Dd(19) ** 19
KAP = Dd(1) / 4


def S(x, counts):
    s = Dd(0)
    for n in range(4, 11):
        s += counts[n] * x ** n
    for n in range(11, 49):
        s += 6 * F(n) * x ** n
    if MU * x >= 1:
        return None
    s += 6 * F(49) * x ** 49 / (1 - MU * x)
    return s


def C0(beta, counts, want_readout=False):
    e = eps6(beta)
    best = None
    for i in range(129):
        b = Dd(1) / 4 + Dd(i) / 64
        a = Dd(0)
        ok = False
        for _ in range(400):
            x = e * (2 * a + b).exp()
            s = S(x, counts)
            if s is None or s > Dd(1) / 4:
                break
            if s <= a * (1 + Dd(10) ** -40):
                ok = True
                break
            a = s
        if ok and a <= Dd(1) / 4:
            d1 = 12 * a * (-4 * (b - KAP)).exp()
            T = Dd("0.8489") * 12 * a * (-8 * b).exp()
            if best is None or d1 < best[0]:
                best = (d1, a, b, T)
    return e, best


def cfun(delta):
    dp = delta * delta.exp()
    if 2 * dp > KAP / 2:
        return None
    m = Dd(0)
    for n in range(4, 400):
        v = (-(KAP / 2 - 2 * dp) * n).exp() - (-KAP * n / 2).exp()
        if v > m:
            m = v
    return delta.exp() * ((-4 * KAP).exp() + m)


crude = {n: 6 * F(n) for n in range(4, 11)}
headfree = {n: 0 for n in range(4, 11)}
measured = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304}  # judge prototype, fine 8^4

print("F20(4..11)", [F(n) for n in range(4, 12)])
print("mu", MU)
for beta in ["0.001", "0.01", "0.015625", "0.02", "0.0222222222222222222222222222", "0.025", "0.1", "1", "4"]:
    print("eps6", beta, eps6(beta), " mu e^1/4 eps6", MU * Dd("0.25").exp() * eps6(beta))

for name, cnt in [("crude", crude), ("headfree", headfree), ("measured", measured)]:
    for beta in ["0.01", "0.015625", "0.02"]:
        e, best = C0(beta, cnt)
        if best is None:
            print(name, beta, "C0 NOT_MET")
        else:
            d1, a, b, T = best
            cc = cfun(d1)
            print(name, beta, "C0 MET delta1 %.6e a %.6e b %s 2d'e %.5e c %s" % (
                d1, a, b, 2 * d1 * d1.exp(), cc if cc is None else "%.6f" % cc))
