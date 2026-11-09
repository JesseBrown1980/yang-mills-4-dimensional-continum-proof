# Judge sanity (Decimal, not an engine): coupling-flow CT08-CT10 in d = 2.
from decimal import Decimal as Dd, getcontext
getcontext().prec = 50
def tn(beta, nmax):
    beta = Dd(beta)
    # r_n = I_n/I_{n-1} by backward continued fraction
    N = nmax + 400
    r = Dd(0)
    rs = {}
    for n in range(N, 1, -1):
        r = 1 / (2 * n / beta + r)
        rs[n] = r
    t = {1: Dd(1)}
    for n in range(2, nmax + 1):
        t[n] = t[n - 1] * rs[n]
    return t
def bq(beta, m, t):
    num = sum(Dd(n * n * (n * n - 1)) * t[n] ** m for n in t)
    den = sum(Dd(n * n) * t[n] ** m for n in t)
    return num / den / 3
def t2(beta):
    return tn(beta, 3)[2]
for beta in (256, 1024, 4096):
    nmax = int(12 * (beta ** 0.5)) + 50
    t = tn(beta, nmax)
    vals = [bq(beta, m, t) for m in (1, 4, 16, 64)]
    print("beta", beta, "bq(m=1)-beta %.3e" % (vals[0] - beta))
    print("  CT09 beta*(bq4 - beta/4 + 13/32) = %.6f" % (beta * (vals[1] - Dd(beta) / 4 + Dd(13) / 32)))
    s = [vals[k + 1] - vals[k] / 4 for k in range(3)]
    tgt = [Dd(-13) / 32, Dd(-133) / 512, Dd(-2053) / 8192]
    print("  CT10 s_k - target:", ["%.3e" % (s[k] - tgt[k]) for k in range(3)], "tol 2^-14 = %.3e" % (Dd(1) / 16384))
    # beta_chi: t2(bc) = t2(beta)^4, bisection
    target = t[2] ** 4
    lo, hi = Dd(beta) / 4 - 2, Dd(beta) / 4 + 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if t2(mid) < target: lo = mid
        else: hi = mid
    bc = lo
    print("  CT09 beta*(bchi - beta/4 - 3/8) = %.4f ; beta*((bchi-bq4) - 25/32) = %.4f" % (beta * (bc - Dd(beta) / 4 - Dd(3) / 8), beta * (bc - vals[1] - Dd(25) / 32)))
