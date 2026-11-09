"""Synthesis-lane arithmetic for the added rows (C10b two-object instance, C03b counting gap, C16). Decimal, not an engine."""
from decimal import Decimal as D, getcontext
from math import comb
import verify_core as v

getcontext().prec = 60
E = D(1).exp()
PI = D("3.14159265358979323846264338327950288419716939937510582097494")

def Fc(n):
    return comb(20 * n, n) // (19 * n + 1)

N = {4: 1, 5: 0, 6: 12, 7: 0, 8: 32, 9: 32, 10: 304, 11: 284, 12: 2326}
for n in (8, 10, 12):
    print("gap n=%d 6F/N = %.4e" % (n, D(6 * Fc(n)) / N[n]))
print("N(10)/N(8)=%.4f N(12)/N(10)=%.4f F(10)/F(8)=%.2f F(12)/F(10)=%.2f" % (
    D(304) / 32, D(2326) / 304, D(Fc(10)) / Fc(8), D(Fc(12)) / Fc(10)))
print("F20(12)=", Fc(12))

# C10b: rectangles split of each coarse filling, input s chi_1/2(rect)
for s in (D(1) / 4096, D(1) / 2000):
    din = 12 * s * D("1.5").exp()
    lc = v.c0(4 * s).ln()
    dout = 3 * E * lc
    # chi_1/2 coefficient of log c0(2 s sqrt(2+chi)) by exact projection: series in chi
    # projection via Gauss-type quadrature on the class angle: chi = 2cos t, weight (2/pi) sin^2 t
    M = 4000
    # midpoint rule is plenty for a display check: use cos via series
    def cos(x):
        x = x % (2 * PI)
        s_ = D(0); term = D(1); k = 0
        while abs(term) > D(10) ** -55:
            s_ += term; k += 2; term = -term * x * x / (k * (k - 1))
        return s_
    acc = D(0)
    for j in range(M):
        t = (D(j) + D(1) / 2) * PI / M
        ct = cos(t); st2 = 1 - ct * ct
        chi = 2 * ct
        f = v.c0(2 * s * (2 + chi).sqrt()).ln()
        acc += f * chi * st2
    cP = acc * 2 / M  # (2/pi) * (pi/M) * sum
    lower = E * abs(cP) * 3 * PI / 8
    cc = v.cfun(din)
    print("s=%s din=%.6e dout=%.6e dout/din=%.4e c(din)=%s cP=%.6e s^2/2=%.6e lower=%.4e lower/(c din)=%.3e" % (
        s, din, dout, dout / din, "%.6f" % cc, cP, s * s / 2, lower, lower / (cc * din)))

# C16
d1 = D("0.0110444506776221312780013577155515476435828765844806436733792")
c = v.cfun(d1)
d20 = c ** 19 * d1
print("c=%.7f sum<=%.6f d2<=%.6e d20<=%.4e osc<=%.4e" % (c, d1 / (1 - c), c * d1, d20, 512 / E * d20))
print("global route", [str(D(1) / (8 * 6 * L ** 4)) for L in (8, 12, 16)])
