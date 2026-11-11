import sys
sys.path.insert(0, '.')
from kp_check import *

def lfp(e, b, counts):
    a = Dd(0)
    for _ in range(2000000):
        x = e * (2 * a + b).exp()
        s = S(x, counts)
        if s is None or s > Dd(1) / 4: return None
        if s <= a * (1 + Dd(10) ** -40): return a
        a = s
    raise RuntimeError("no convergence")

def C0all(beta, counts):
    e = eps6(beta)
    out = []
    for i in range(129):
        b = Dd(1) / 4 + Dd(i) / 64
        a = lfp(e, b, counts)
        if a is not None: out.append((a, b))
    return out

def met(beta, counts):
    return bool(C0all(beta, counts))

getcontext().prec = 40
for name, cnt, pts in [("crude", crude, [1900, 1901, 1902, 1903, 1904, 1905]),
                       ("headfree", headfree, [2073, 2074, 2075, 2076])]:
    for p in pts:
        beta = Dd(p) / 100000
        o = C0all(beta, cnt)
        print(name, p, "MET" if o else "NOT_MET", ("a=%.5f b=%s" % (min(o)[0], min(o)[1])) if o else "")
def P10(b):
    return b**4/128 - b**6/768 + b**8/1536 - 467*b**10/2211840
for nm, cnt in [("measured", measured), ("N4=N6=0", dict(measured, **{4: 0, 6: 0})), ("headfree", headfree)]:
    for beta in [Dd(1)/4000, Dd(1)/2000, Dd(1)/1000]:
        o = C0all(beta, cnt)
        T = min(Dd('0.8489') * 12 * a * (-8 * b).exp() for a, b in o)
        print("C09", nm, "beta", beta, "T/P10 %.4e" % (T / P10(beta)))
