"""Design-lane SANITY CHECK of derived 2D asymptotics (Decimal, 80 digits; not evidence, not an engine).

Exact 2D b = 2 one-step map (YM4-03 Theorem 8): c_n -> c_n^4, t_n = I_n(beta)/I_1(beta).
 small-field coupling   beta_q(beta; m) = (1/3) sum n^2 (n^2-1) t_n^m / sum n^2 t_n^m,  m = 4^k (k steps)
 character matching     t_2(beta_chi) = t_2(beta)^4
Derived (Laplace + Euler-Maclaurin): beta_q(beta; m) = beta/m - 1/(2m) + 5/(6 m^2) - 1/3 + O(m/beta),
                                    beta_chi = beta/4 + 3/8 + O(1/beta).
Heat kernel K_q = sum n q^(n^2-1) chi_n: beta_q(q) = 1/(2 tau) - 1/3 + (images), q = e^-tau.
"""
from decimal import Decimal as D, getcontext

getcontext().prec = 90


def ratios(beta, N):
    # r_n = I_n/I_{n-1} by backward continued fraction; t_n = I_n/I_1 = prod_{j=2..n} r_j
    beta = D(beta)
    r = [D(0)] * (N + 2)
    for n in range(N, 0, -1):
        r[n] = 1 / (2 * n / beta + r[n + 1])
    t = [D(0), D(1)]
    for n in range(2, N + 1):
        t.append(t[-1] * r[n])
    return t


def beta_q_from_t(t, m):
    num = D(0)
    den = D(0)
    for n in range(1, len(t)):
        w = n * n * t[n] ** m
        num += w * (n * n - 1)
        den += w
        if n > 10 and w < den * D(10) ** -85:
            break
    return num / den / 3


def t2_of(beta):
    return ratios(beta, 40 + int(4 * D(beta).sqrt()) + int(D(beta)))[2]


def beta_chi(beta):
    target = t2_of(beta) ** 4
    lo, hi = D(0), D(beta)
    for _ in range(200):
        mid = (lo + hi) / 2
        if t2_of(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


for beta in (64, 256, 1024, 4096):
    N = 60 + int(12 * D(beta).sqrt()) + 200
    t = ratios(beta, N)
    b1 = beta_q_from_t(t, 1)
    bq = {m: beta_q_from_t(t, m) for m in (4, 16, 64)}
    pred = {m: D(beta) / m - D(1) / (2 * m) + D(5) / (6 * m * m) - D(1) / 3 for m in (4, 16, 64)}
    print("beta=%d  beta_q(m=1)-beta=%.3e" % (beta, b1 - beta))
    for m in (4, 16, 64):
        res = bq[m] - pred[m]
        print("   m=%2d beta_q=%.12f  minus derived=%.6e  *beta/m=%.6f" % (m, bq[m], res, res * beta / m))
    s1 = bq[4] - D(beta) / 4
    s2 = bq[16] - bq[4] / 4
    s3 = bq[64] - bq[16] / 4
    print("   one-step constants: k=0 %.9f (pred %.9f)  k=1 %.9f (pred %.9f)  k=2 %.9f (pred %.9f)" % (
        s1, D(-13) / 32, s2, D(-1) / 4 - D(5) / (32 * 16), s3, D(-1) / 4 - D(5) / (32 * 256)))
    if beta <= 1024:
        bc = beta_chi(beta)
        print("   beta_chi - beta/4 = %.9f (pred 3/8 = 0.375)  *beta: %.6f ; beta_chi - beta_q = %.9f (pred 25/32=0.78125)" % (
            bc - D(beta) / 4, (bc - D(beta) / 4 - D(3) / 8) * beta, bc - bq[4]))
    print("   beta_q(m=4) < beta:", bq[4] < beta)

# strong end: beta = 1/16, compare with the polynomial through beta^10
for beta in (D(1) / 16, D(1) / 4, D(1)):
    t = ratios(beta, 60)
    bq = beta_q_from_t(t, 4)
    poly = beta ** 4 / 64 - beta ** 6 / 384 + 17 * beta ** 8 / 110592 + 61 * beta ** 10 / 2211840
    print("beta=%s beta_q=%.20e poly=%.20e diff=%.3e diff/beta^12=%.6e" % (beta, bq, poly, bq - poly, (bq - poly) / beta ** 12))

# heat kernel control
for qn, qd in ((63, 64), (255, 256)):
    q = D(qn) / D(qd)
    def bq_hk(qq):
        num = D(0); den = D(0)
        n = 1
        while True:
            w = n * n * qq ** (n * n - 1)
            num += w * (n * n - 1); den += w
            if n > 5 and w < den * D(10) ** -88:
                break
            n += 1
        return num / den / 3
    a = bq_hk(q)
    b = bq_hk(q ** 4)
    print("heat kernel q=%d/%d: beta_q=%.10f, beta_q(q^4)-((beta_q+1/3)/4-1/3)=%.3e" % (qn, qd, a, b - ((a + D(1) / 3) / 4 - D(1) / 3)))
